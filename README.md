# AI Study Copilot

**AI Study Copilot** es una plataforma avanzada de aprendizaje asistido por Inteligencia Artificial diseñada para transformar material educativo denso (PDFs, Jupyter Notebooks) en experiencias de estudio interactivas y personalizadas. 

El sistema utiliza arquitecturas de **RAG (Retrieval-Augmented Generation)** y flujos de trabajo agentes basados en **LangGraph** para ofrecer respuestas fundamentadas, tutoría adaptativa y generación automática de material de estudio.

---

## Características Principales

* **Ingesta Multi-formato:** Procesamiento inteligente de archivos PDF y Jupyter Notebooks (`.ipynb`), extrayendo estructura, código y contexto técnico.
* **RAG de Alta Precisión:** Implementación de recuperación avanzada con *embeddings* vectoriales y técnicas de *re-ranking* para asegurar respuestas precisas y libres de alucinaciones.
* **Tutoría con Estado (Stateful):** Uso de **LangGraph** para gestionar sesiones de estudio que mantienen la memoria del progreso del usuario y permiten flujos de tutoría dinámicos.
* **Framework de Evaluación:** Módulo dedicado para medir la calidad del *retrieval* y la fidelidad de las respuestas, asegurando una mejora continua del sistema.
* **Interfaz Moderna:** Dashboard intuitivo construido con **Next.js** para una navegación fluida entre fuentes de consulta y modos de estudio.

---

## Arquitectura del Sistema

El proyecto está organizado como un **Monorepo**, garantizando una separación clara de responsabilidades y facilitando el escalado de cada componente.

### Estructura de Carpetas

* **`apps/api`**: Backend robusto construido con **FastAPI**. Implementa una arquitectura modular dividida en rutas, esquemas y servicios.
* **`apps/web`**: Frontend moderno en **Next.js (App Router)**, diseñado para ofrecer una experiencia de usuario rápida y reactiva.
* **`packages/ingestion`**: Pipeline especializado en la transformación de archivos crudos en *chunks* de datos enriquecidos.
* **`packages/rag_core`**: El núcleo del sistema. Contiene la lógica de *embeddings*, almacenes vectoriales, prompts y los grafos de estudio.
* **`packages/evals`**: Herramientas de evaluación para auditar la calidad de la IA de forma explícita.
* **`packages/shared`**: Modelos de datos y constantes compartidas entre el backend y los pipelines de datos.

---

## Stack Tecnológico

* **Lenguaje:** Python 3.10+ & TypeScript.
* **IA/ML:** LangChain, LangGraph, PyTorch (para procesamiento de modelos).
* **Base de Datos:** ChromaDB / pgvector (Vector Stores).
* **Backend:** FastAPI.
* **Frontend:** React, Next.js, Tailwind CSS.
* **Infraestructura:** Docker & Docker Compose.

---

## Organización del Repositorio

```bash
ai-study-copilot/
├── apps/               # Aplicaciones desplegables (API y Web)
├── packages/           # Librerías de lógica de negocio (RAG, Ingesta, Evals)
├── data/               # Almacenamiento de documentos (Raw, Processed, Indexes)
├── scripts/            # Scripts de utilidad (Ingesta masiva, tests de humo)
└── docs/               # Documentación detallada de arquitectura y decisiones
```

## Guía de Inicio Rápido
1. Clonar el repositorio:

```bash
git clone [https://github.com/tu-usuario/ai-study-copilot.git](https://github.com/tu-usuario/ai-study-copilot.git)
cd ai-study-copilot
```

2. Configurar variables de entorno:

```Bash
cp .env.example .env
# Configura tus llaves de API y credenciales de base de datos
```

3. Levantar el entorno de desarrollo:

```bash
docker-compose up --build
```

4. Ejecutar la ingesta inicial:
Coloca tus archivos en data/raw/ y ejecuta:

```bash
python scripts/ingest_all.py