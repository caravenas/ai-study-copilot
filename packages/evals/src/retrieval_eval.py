import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any

from packages.rag_core.src.retrieval.filters import build_where_filter
from packages.rag_core.src.retrieval.retriever import retrieve_documents


BASE_DIR = Path(__file__).resolve().parents[3]
DEFAULT_DATASET = BASE_DIR / "packages" / "evals" / "src" / "datasets" / "benchmark_questions.json"
DEFAULT_OUTPUT_DIR = BASE_DIR / "data" / "processed" / "evals"


@dataclass
class PerQuestionResult:
    question: str
    module: str | None
    top_k: int
    hit: int
    reciprocal_rank: float
    matched_rank: int | None
    retrieved_chunk_ids: list[str]
    retrieved_sources: list[str]


def _normalize_text(value: str) -> str:
    return value.strip().lower()


def _doc_matches_expectation(doc: dict[str, Any], row: dict[str, Any]) -> bool:
    expected_sources = {_normalize_text(s) for s in row.get("expected_sources", []) if isinstance(s, str)}
    expected_topics = {_normalize_text(t) for t in row.get("expected_topics", []) if isinstance(t, str)}
    expected_module = row.get("expected_module") or row.get("module")

    if expected_sources:
        source_file = _normalize_text(str(doc.get("source_file", "")))
        source_name = _normalize_text(Path(source_file).name)
        if source_file in expected_sources or source_name in expected_sources:
            return True

    if expected_topics:
        doc_topics = doc.get("topics") or []
        if isinstance(doc_topics, str):
            doc_topics = [t.strip() for t in doc_topics.split(",")]
        if any(_normalize_text(str(t)) in expected_topics for t in doc_topics):
            return True

    if expected_module:
        return _normalize_text(str(doc.get("module", ""))) == _normalize_text(str(expected_module))

    return False


def _first_match_rank(docs: list[dict[str, Any]], row: dict[str, Any]) -> int | None:
    for idx, doc in enumerate(docs, start=1):
        if _doc_matches_expectation(doc, row):
            return idx
    return None


def run_retrieval_eval(
    dataset_path: Path = DEFAULT_DATASET,
    top_k: int = 5,
) -> dict[str, Any]:
    payload = json.loads(dataset_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Benchmark dataset must be a JSON array.")
    if not payload:
        raise ValueError(f"Benchmark dataset is empty: {dataset_path}")

    per_question: list[PerQuestionResult] = []
    per_module_hits: dict[str, list[int]] = defaultdict(list)

    for row in payload:
        question = row["question"]
        module = row.get("module")
        difficulty = row.get("difficulty")
        where_filter = build_where_filter(module=module, difficulty=difficulty)
        docs = retrieve_documents(question=question, top_k=top_k, where_filter=where_filter)

        match_rank = _first_match_rank(docs, row)
        hit = 1 if match_rank is not None else 0
        rr = 1.0 / match_rank if match_rank is not None else 0.0
        module_key = module or "__no_module__"
        per_module_hits[module_key].append(hit)

        per_question.append(
            PerQuestionResult(
                question=question,
                module=module,
                top_k=top_k,
                hit=hit,
                reciprocal_rank=rr,
                matched_rank=match_rank,
                retrieved_chunk_ids=[str(d.get("chunk_id", "")) for d in docs],
                retrieved_sources=[str(d.get("source_file", "")) for d in docs],
            )
        )

    hit_at_k = mean([r.hit for r in per_question])
    mrr = mean([r.reciprocal_rank for r in per_question])
    module_coverage = {
        module: round(mean(hits), 4) for module, hits in sorted(per_module_hits.items(), key=lambda x: x[0])
    }

    return {
        "dataset_path": str(dataset_path),
        "num_questions": len(per_question),
        "top_k": top_k,
        "metrics": {
            "hit_at_k": round(hit_at_k, 4),
            "mrr": round(mrr, 4),
            "module_coverage": module_coverage,
        },
        "results": [r.__dict__ for r in per_question],
    }


def _build_output_path(output_dir: Path) -> Path:
    from datetime import datetime

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return output_dir / f"retrieval_eval_{ts}.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run retrieval evaluation benchmark.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET, help="Path to benchmark JSON dataset.")
    parser.add_argument("--top-k", type=int, default=5, help="Top-k docs to retrieve for each question.")
    parser.add_argument("--output", type=Path, default=None, help="Optional output file path.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory if --output is not provided.",
    )
    args = parser.parse_args()

    report = run_retrieval_eval(dataset_path=args.dataset, top_k=args.top_k)
    output_path = args.output
    if output_path is None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = _build_output_path(args.output_dir)
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved retrieval eval report: {output_path}")
    print(json.dumps(report["metrics"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
