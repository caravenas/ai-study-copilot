# Project Instructions: AI Study Copilot

Este archivo contiene las directrices de arquitectura, convenciones y flujos de trabajo para el proyecto AI Study Copilot.

## Arquitectura y Flujo de Datos

- **Monorepo**: Se utiliza una estructura de monorepo con `apps/` (api, web) y `packages/` (rag_core, ingestion, evals, shared).
- **LangGraph**: El núcleo del sistema RAG es un grafo de estados (`packages/rag_core/src/graph/study_graph.py`).
- **Corrective RAG (CRAG)**: El flujo incluye nodos de evaluación de relevancia (`grade_documents`) y reescritura de queries (`rewrite_query`).
- **Orquestación**: La API usa `StudyOrchestrator` para invocar el grafo.

## Convenciones de Código

- **Idioma**: Todo el código (prompts, logs, documentación, UI) debe estar en **español**.
- **Imports**: Los paquetes internos deben importarse desde la raíz del repo (ej: `from packages.rag_core.src...`). El `sys.path` se configura en `apps/api/app/main.py`.
- **Tipado**: Uso estricto de Pydantic para esquemas de API y tipos de Python para el resto del código.

## Desarrollo y Tests

- **Entorno**: Se requiere Python 3.12+ y Node.js 18.17+.
- **Tests**: Ejecutar `make test-api` para el backend. Los tests se encuentran en `apps/api/tests/` y `packages/*/tests/`.
- **Validación**: Antes de considerar una tarea terminada, verificar que el grafo de LangGraph compile y que los nodos respondan correctamente.

## Referencias de Documentación

- `README.md`: Resumen del proyecto, setup y estado actual.
- `AGENTS.md`: Instrucciones específicas para el rol de Tutor de Proyecto.
- `docs/`: Documentación técnica detallada (arquitectura, ADRs).
