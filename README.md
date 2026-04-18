# AI Study Copilot

Sistema RAG pedagógico que conecta PDFs de clases y Jupyter Notebooks de un diplomado en IA. Expone tutoría adaptativa por nivel, quizzes y respuestas con citas *grounded* sobre el material del curso.

**Stack:** FastAPI · LangChain · LangGraph · ChromaDB · OpenAI embeddings · MiniMax chat LLM · Next.js 14 (App Router) · Tailwind

---

## Estructura del monorepo

```
ai-study-copilot/
├── apps/
│   ├── api/                 # FastAPI backend (app/main.py)
│   └── web/                 # Next.js 14 frontend
├── packages/
│   ├── rag_core/            # retrieval, embeddings, LLM, prompts, grafo
│   ├── ingestion/           # parsers PDF/notebook, chunking, metadata
│   ├── evals/               # evaluación de retrieval y respuestas
│   └── shared/              # schemas y constantes compartidas
├── data/
│   ├── raw/{pdfs,notebooks} # fuentes originales (gitignored)
│   ├── processed/           # chunks procesados
│   └── indexes/chroma/      # índice vectorial persistido
├── scripts/                 # utilidades (ingesta, smoke test, rebuild)
├── docs/                    # documentación y ADRs
├── docker-compose.yml
└── Makefile
```

Los imports del backend resuelven `packages.*` agregando la raíz del repo a `sys.path` desde `apps/api/app/main.py`. No uses `pip install -e .` para los paquetes internos.

---

## Requisitos previos

| Herramienta | Versión mínima | Notas |
|-------------|----------------|-------|
| Python      | 3.12           | Probado con 3.12.1 |
| Node.js     | 18.17+         | Requerido por Next.js 14 |
| npm         | 9+             | Viene con Node |
| OpenAI API key | —           | Para embeddings `text-embedding-3-small` |
| MiniMax API key | —          | Para el chat LLM `MiniMax-M2.7` |

ChromaDB corre en modo embebido (persistencia en disco bajo `data/indexes/chroma`). No requiere servicio externo.

---

## Setup paso a paso

### 1. Clonar y entrar al repo

```bash
git clone <url-del-repo> ai-study-copilot
cd ai-study-copilot
```

### 2. Variables de entorno

```bash
cp .env.example .env
# Edita .env y completa OPENAI_API_KEY y MINIMAX_API_KEY
```

`apps/api/app/core/config.py` carga `.env` desde la raíz del monorepo automáticamente.

### 3. Backend (Python)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Frontend (Next.js)

```bash
cd apps/web
npm install
cd ../..
```

### 5. Colocar material de estudio

```
data/raw/pdfs/         # PDFs de clases
data/raw/notebooks/    # Jupyter notebooks (.ipynb)
```

El directorio `data/` está en `.gitignore`; cada desarrollador trae su propio material.

### 6. Ingestar y construir el índice vectorial

La API expone el endpoint de ingesta. Con el backend corriendo (ver paso 7):

```bash
curl -X POST http://localhost:8000/api/ingest
```

Esto parsea PDFs + notebooks, genera chunks con metadatos, calcula embeddings y persiste el índice Chroma en `data/indexes/chroma`.

> Los scripts en `scripts/` (`ingest_all.py`, `rebuild_index.py`, `smoke_test.py`) son stubs en este momento. Usa el endpoint `/api/ingest` como fuente de verdad.

---

## Correr en desarrollo

Con `.venv` activo y desde la raíz del repo:

```bash
# Backend (http://localhost:8000, docs en /docs)
make run-api

# Frontend (http://localhost:3000)
make run-web
```

Equivalentes sin Make:

```bash
cd apps/api && uvicorn app.main:app --reload --port 8000
cd apps/web && npm run dev
```

---

## Endpoints principales

| Método | Ruta           | Propósito                                  |
|--------|----------------|--------------------------------------------|
| GET    | `/api/health`  | Health check                               |
| POST   | `/api/ingest`  | Ingesta de PDFs y notebooks                |
| POST   | `/api/query`   | Pregunta RAG con citas y labs relacionados |
| POST   | `/api/study`   | Explicación adaptada por nivel / resumen   |
| POST   | `/api/eval`    | Evaluación de respuestas (WIP)             |

Documentación interactiva: `http://localhost:8000/docs`.

---

## Tests

```bash
make test-api
# equivalente: cd apps/api && pytest
```

Los tests viven en `apps/api/tests/` y `packages/*/tests/`.

---

## Docker

Con el `.env` configurado en la raíz:

```bash
docker compose up --build
```

- `api` → `http://localhost:8000`
- `web` → `http://localhost:3000`
- El índice Chroma persiste en `./data/indexes/chroma` (volumen montado).

Para la ingesta en este modo, tras levantar los servicios:

```bash
# Copia PDFs/notebooks a ./data/raw/ antes o durante la ejecución
curl -X POST http://localhost:8000/api/ingest
```

---

## Problemas conocidos

- `packages/rag_core/src/prompts/coder_prompt.py` está incompleto; el modo `coder_agent` del grafo LangGraph aún no es funcional end-to-end.
- La API usa el pipeline directo (`packages.rag_core.src.pipeline`) — el grafo LangGraph todavía no está enganchado al router.

---

## Idioma

Todo el sistema (prompts, UI, documentación) está en **español**. Mantén ese contrato al contribuir nuevos prompts o copy.
