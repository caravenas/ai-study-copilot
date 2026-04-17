"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { summaryApi, quizApi, QueryResponse, QuizItem } from "@/lib/api";

function stripThinkTags(text: string): string {
  return text.replace(/<think>[\s\S]*?<\/think>\s*/g, "").trim();
}

// ─── FlashCard ────────────────────────────────────────────────────────

function FlashCard({ item, index }: { item: QuizItem; index: number }) {
  const [selected, setSelected] = useState<string | null>(null);

  // La letra de la opción es el primer carácter antes del ")"
  const letterOf = (opt: string) => opt.split(")")[0].trim();
  const isCorrect = (opt: string) => letterOf(opt) === item.correct;
  const isSelected = (opt: string) => opt === selected;

  function optionStyle(opt: string) {
    if (!selected)
      return "bg-surface-container text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface cursor-pointer";
    if (isCorrect(opt))
      return "bg-[#d4edda] text-[#1a5c2e] border border-[#1a5c2e]/30 cursor-default";
    if (isSelected(opt))
      return "bg-[#fce8e8] text-[#8b1a1a] border border-[#8b1a1a]/30 cursor-default";
    return "bg-surface-container text-on-surface-variant opacity-50 cursor-default";
  }

  function optionIcon(opt: string) {
    if (!selected) return null;
    if (isCorrect(opt))
      return (
        <span className="material-symbols-outlined text-[18px] text-[#1a5c2e] shrink-0"
          style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
      );
    if (isSelected(opt))
      return (
        <span className="material-symbols-outlined text-[18px] text-[#8b1a1a] shrink-0"
          style={{ fontVariationSettings: "'FILL' 1" }}>cancel</span>
      );
    return null;
  }

  const answered = selected !== null;
  const correct = answered && isCorrect(selected);

  return (
    <div className="bg-surface-container-lowest rounded-2xl p-6 border border-outline-variant/20 shadow-sm flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center gap-2">
        <span className="w-7 h-7 rounded-lg bg-primary-container flex items-center justify-center text-[11px] font-bold text-on-primary-container font-label shrink-0">
          {index + 1}
        </span>
        <span className="text-[10px] font-bold text-primary uppercase tracking-widest font-label">
          Pregunta
        </span>
        {answered && (
          <span className={`ml-auto text-[10px] font-bold uppercase tracking-widest font-label ${correct ? "text-[#1a5c2e]" : "text-[#8b1a1a]"}`}>
            {correct ? "✓ Correcto" : "✗ Incorrecto"}
          </span>
        )}
      </div>

      {/* Pregunta */}
      <p className="font-semibold text-on-surface text-[15px] font-body leading-snug">
        {item.question}
      </p>

      {/* Opciones */}
      <ul className="space-y-2">
        {item.options.map((opt) => (
          <li key={opt}>
            <button
              disabled={answered}
              onClick={() => setSelected(opt)}
              className={`w-full text-left text-sm font-body px-4 py-2.5 rounded-xl transition-colors flex items-center justify-between gap-3 ${optionStyle(opt)}`}
            >
              <span>{opt}</span>
              {optionIcon(opt)}
            </button>
          </li>
        ))}
      </ul>

      {/* Explicación (aparece tras responder) */}
      {answered && (
        <div className="mt-1 bg-surface-container rounded-xl px-4 py-3 border border-outline-variant/20">
          <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest font-label mb-1">
            Explicación
          </p>
          <p className="text-sm text-on-surface font-body leading-relaxed">
            {item.explanation}
          </p>
        </div>
      )}

      {/* Reintentar */}
      {answered && (
        <button
          onClick={() => setSelected(null)}
          className="self-end text-[11px] font-semibold text-primary hover:underline font-label"
        >
          Reintentar →
        </button>
      )}
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────

export default function StudyView() {
  const [topic, setTopic] = useState("");
  const [activeTab, setActiveTab] = useState<"summary" | "quiz">("summary");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<QueryResponse | null>(null);

  async function handleGenerate(mode: "summary" | "quiz") {
    if (!topic.trim()) return;
    setIsLoading(true);
    setError(null);
    setActiveTab(mode);
    setResponse(null);

    try {
      if (mode === "summary") {
        const data = await summaryApi(topic);
        setResponse(data);
      } else {
        const data = await quizApi({ question: topic, level: "intermedio" });
        setResponse(data);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unknown error occurred");
    } finally {
      setIsLoading(false);
    }
  }

  function ThinkingIndicator() {
    return (
      <div className="flex justify-center my-12 animate-[fadeSlideUp_0.3s_ease] w-full">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-primary-container flex items-center justify-center animate-pulse shadow-lg">
            <span
              className="material-symbols-outlined text-primary text-2xl"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              school
            </span>
          </div>
          <div className="flex items-center gap-2 text-on-surface-variant font-body font-medium text-sm">
            <div className="flex gap-1">
              <span className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce [animation-delay:0ms]" />
              <span className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce [animation-delay:150ms]" />
              <span className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce [animation-delay:300ms]" />
            </div>
            <span className="ml-2">
              {activeTab === "summary"
                ? "Consultando la bibliografía y resumiendo..."
                : "Diseñando quiz interactivo basado en las lecturas..."}
            </span>
          </div>
        </div>
      </div>
    );
  }

  const hasFlashcards =
    activeTab === "quiz" &&
    response?.quiz_items &&
    response.quiz_items.length > 0;

  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-12 flex flex-col items-center pb-12">
      <div className="w-full max-w-3xl mb-8 flex flex-col items-center text-center gap-3">
        <h1 className="text-3xl font-headline font-black text-on-surface">
          Study Center
        </h1>
        <p className="text-on-surface-variant font-body">
          Ingresa una materia (ej: Redes Neuronales) para generar un resumen
          ejecutivo o un quiz autoevaluable.
        </p>
      </div>

      {/* Input Area */}
      <div className="w-full max-w-3xl bg-surface-container-lowest rounded-3xl p-3 shadow-lg shadow-black/5 border border-outline-variant/20 mb-8 flex gap-2 flex-col sm:flex-row focus-within:ring-2 focus-within:ring-primary/20 transition-all">
        <div className="flex items-center px-4 opacity-50">
          <span className="material-symbols-outlined">search</span>
        </div>
        <input
          type="text"
          placeholder="¿Qué rama quieres repasar hoy?"
          className="flex-1 bg-transparent py-4 text-on-surface font-body outline-none placeholder:text-outline-variant/60 text-lg"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleGenerate("summary");
          }}
        />
        <div className="flex gap-2">
          <button
            disabled={!topic.trim() || isLoading}
            onClick={() => handleGenerate("summary")}
            className="px-6 py-4 bg-secondary-container text-on-secondary-container hover:bg-secondary-container/80 transition-colors rounded-2xl font-semibold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="material-symbols-outlined text-[20px]">subject</span>
            Resumir
          </button>
          <button
            disabled={!topic.trim() || isLoading}
            onClick={() => handleGenerate("quiz")}
            className="px-6 py-4 bg-primary text-white hover:bg-primary/90 transition-colors rounded-2xl font-semibold flex items-center gap-2 shadow-lg shadow-primary/20 disabled:opacity-50 disabled:cursor-not-allowed hover:-translate-y-0.5 active:translate-y-0"
          >
            <span className="material-symbols-outlined text-[20px]">quiz</span>
            Test
          </button>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="bg-error-container text-on-error-container px-6 py-4 rounded-2xl mb-8 flex items-center gap-3 max-w-2xl text-sm font-medium animate-[fadeSlideUp_0.2s_ease]">
          <span className="material-symbols-outlined">error</span>
          {error}
        </div>
      )}

      {/* Loading state */}
      {isLoading && <ThinkingIndicator />}

      {/* Result Area */}
      {response && !isLoading && (
        <div className="w-full max-w-3xl animate-[fadeSlideUp_0.4s_ease]">
          <div className="bg-surface-container-lowest rounded-[2rem] p-8 md:p-14 shadow-[0_12px_40px_rgba(42,52,57,0.06)] border border-outline-variant/10 relative">

            {/* Badge */}
            <div className="absolute -top-4 right-8 inline-flex items-center gap-2 px-4 py-2 bg-primary-container text-on-primary-container border border-white/50 rounded-full text-[10px] font-bold uppercase tracking-widest font-label shadow-sm">
              <span className="material-symbols-outlined text-[16px]">
                {activeTab === "summary" ? "history_edu" : "psychology_alt"}
              </span>
              {activeTab === "summary" ? "Resumen de Clase" : "Evaluación Rápida"}
            </div>

            {/* Flashcards (quiz con JSON estructurado) */}
            {hasFlashcards ? (
              <div className="space-y-4">
                <p className="text-[11px] font-bold text-on-surface-variant uppercase tracking-widest font-label mb-6">
                  {response.quiz_items.length} preguntas — selecciona una alternativa para ver si acertaste
                </p>
                {response.quiz_items.map((item, i) => (
                  <FlashCard key={i} item={item} index={i} />
                ))}
              </div>
            ) : (
              /* Markdown fallback (resumen o quiz sin JSON) */
              <div className="prose prose-sm md:prose-base max-w-none text-on-surface leading-loose font-body
                prose-headings:font-headline prose-headings:text-on-primary-container prose-headings:font-bold
                prose-h1:text-3xl prose-h2:text-xl prose-h2:mt-10 prose-h2:mb-6
                prose-strong:text-on-surface prose-strong:font-bold
                prose-ul:my-6 prose-li:my-3
                prose-p:my-5
                prose-blockquote:border-l-4 prose-blockquote:border-secondary prose-blockquote:bg-surface-container-low prose-blockquote:py-1 prose-blockquote:px-5 prose-blockquote:not-italic prose-blockquote:rounded-r-xl"
              >
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {stripThinkTags(response.answer)}
                </ReactMarkdown>
              </div>
            )}

            {/* Citations (solo en summary) */}
            {response.citations && response.citations.length > 0 && activeTab === "summary" && (
              <div className="mt-14 pt-8 border-t border-outline-variant/20 flex flex-col items-center">
                <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-6">
                  Fuentes consultadas
                </span>
                <div className="flex flex-wrap justify-center gap-3">
                  {response.citations.map((cit, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-2 bg-surface-container px-4 py-2.5 rounded-xl text-xs font-medium border border-outline-variant/10 shadow-sm"
                    >
                      <span className="material-symbols-outlined text-[16px] text-primary">
                        description
                      </span>
                      <span className="text-on-surface">
                        {cit.source_file.split("/").pop()}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Empty state */}
      {!response && !isLoading && !error && (
        <div className="mt-20 flex flex-col items-center opacity-30 select-none pointer-events-none">
          <span
            className="material-symbols-outlined text-8xl mb-6 text-on-surface"
            style={{ fontVariationSettings: "'wght' 100" }}
          >
            menu_book
          </span>
          <p className="font-headline text-2xl font-bold tracking-tight">
            Selecciona un tema para repasar
          </p>
        </div>
      )}

      <div className="h-32 w-full flex-shrink-0 pointer-events-none" />
    </div>
  );
}
