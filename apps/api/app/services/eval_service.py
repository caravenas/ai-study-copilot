import json
from app.schemas.eval import EvalRequest, EvalResponse, MetricScore
from packages.rag_core.src.retrieval.retriever import retrieve_documents
from packages.rag_core.src.retrieval.filters import build_where_filter
from packages.rag_core.src.pipeline import answer_question
from packages.rag_core.src.prompts.eval_prompt import build_eval_prompt
from packages.rag_core.src.llm.client import generate_answer


async def run_eval(request: EvalRequest) -> EvalResponse:
    # 1. Recuperar docs
    where_filter = build_where_filter(module=request.module)
    docs = retrieve_documents(question=request.question, top_k=5, where_filter=where_filter)

    # 2. Generar respuesta con el pipeline
    pipeline_result = answer_question(question=request.question, module=request.module)
    generated_answer = pipeline_result["answer"]

    # 3. Evaluar con LLM-as-judge
    eval_prompt = build_eval_prompt(
        question=request.question,
        docs=docs,
        generated_answer=generated_answer,
        expected_answer=request.expected_answer,
    )
    raw = generate_answer(eval_prompt)

    # 4. Parsear JSON (el LLM puede agregar texto extra, extrae solo el JSON)
    start = raw.find("{")
    end = raw.rfind("}") + 1
    metrics = json.loads(raw[start:end])

    scores = [
        metrics["retrieval_score"]["score"],
        metrics["grounding_score"]["score"],
        metrics["answer_relevance"]["score"],
    ]

    return EvalResponse(
        question=request.question,
        generated_answer=generated_answer,
        retrieval_score=MetricScore(**metrics["retrieval_score"]),
        grounding_score=MetricScore(**metrics["grounding_score"]),
        answer_relevance=MetricScore(**metrics["answer_relevance"]),
        overall_score=round(sum(scores) / len(scores), 3),
    )
