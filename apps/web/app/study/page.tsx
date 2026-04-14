"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { summaryApi, quizApi, QueryResponse } from "@/lib/api";

// Strip <think>...</think> blocks from LLM responses if the model uses explicit reasoning mode
function stripThinkTags(text: string): string {
  return text.replace(/<think>[\s\S]*?<\/think>\s*/g, "").trim();
}

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
    } catch (err: any) {
      setError(err.message || "Unknown error occurred");
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
              {activeTab === "summary" ? "Consultando la bibliografía y resumiendo..." : "Diseñando quiz interactivo basado en las lecturas..."}
            </span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-12 flex flex-col items-center pb-12">
        
      <div className="w-full max-w-3xl mb-8 flex flex-col items-center text-center gap-3">
        <h1 className="text-3xl font-headline font-black text-on-surface">Study Center</h1>
        <p className="text-on-surface-variant font-body">Ingresa una materia (ej: Redes Neuronales) para generar un resumen ejecutivo o un quiz autoevaluable.</p>
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
            
            {/* Badge for Mode */}
            <div className="absolute -top-4 right-8 inline-flex items-center gap-2 px-4 py-2 bg-primary-container text-on-primary-container border border-white/50 rounded-full text-[10px] font-bold uppercase tracking-widest font-label shadow-sm">
              <span className="material-symbols-outlined text-[16px]">
                {activeTab === "summary" ? "history_edu" : "psychology_alt"}
              </span>
              {activeTab === "summary" ? "Resumen de Clase" : "Evaluación Rápida"}
            </div>

            <div className="prose prose-sm md:prose-base max-w-none text-on-surface leading-loose font-body
              prose-headings:font-headline prose-headings:text-on-primary-container prose-headings:font-bold
              prose-h1:text-3xl prose-h2:text-xl prose-h2:mt-10 prose-h2:mb-6
              prose-strong:text-on-surface prose-strong:font-bold
              prose-ul:my-6 prose-li:my-3
              prose-p:my-5
              
              /* Custom styling for standard Markdown blockquotes */
              prose-blockquote:border-l-4 prose-blockquote:border-secondary prose-blockquote:bg-surface-container-low prose-blockquote:py-1 prose-blockquote:px-5 prose-blockquote:not-italic prose-blockquote:rounded-r-xl
              
              /* Custom CSS to inject magic into the details/summary elements of Quizzes */
              [&_details]:bg-surface-container-low [&_details]:p-5 [&_details]:rounded-2xl [&_details]:mt-5 [&_details]:border [&_details]:border-outline-variant/30 [&_details]:transition-all
              [&_details[open]]:bg-surface-container-lowest [&_details[open]]:shadow-inner
              
              [&_summary]:font-bold [&_summary]:text-primary [&_summary]:cursor-pointer [&_summary]:list-none [&_summary]:flex [&_summary]:items-center [&_summary]:gap-2 [&_summary]:select-none
              [&_summary::-webkit-details-marker]:hidden
              
              /* Add a tiny icon before the summary */
              [&_summary::before]:content-['►'] [&_summary::before]:inline-block [&_summary::before]:text-[10px] [&_details[open]_summary::before]:content-['▼']
              
              /* Sub-answers text color */
              [&_details_p]:text-sm [&_details_p]:text-on-surface-variant [&_details_p]:mt-4
              "
            >
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {stripThinkTags(response.answer)}
              </ReactMarkdown>
            </div>
            
            {/* Citations at the bottom */}
            {response.citations && response.citations.length > 0 && activeTab === "summary" && (
              <div className="mt-14 pt-8 border-t border-outline-variant/20 flex flex-col items-center">
                <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-6">Fuentes consultadas</span>
                <div className="flex flex-wrap justify-center gap-3">
                  {response.citations.map((cit, idx) => (
                    <div key={idx} className="flex items-center gap-2 bg-surface-container px-4 py-2.5 rounded-xl text-xs font-medium border border-outline-variant/10 shadow-sm">
                      <span className="material-symbols-outlined text-[16px] text-primary">description</span>
                      <span className="text-on-surface">{cit.source_file.split('/').pop()}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
          </div>
        </div>
      )}
      
      {/* Empty visual state if nothing is loaded */}
      {!response && !isLoading && !error && (
        <div className="mt-20 flex flex-col items-center opacity-30 select-none pointer-events-none">
          <span className="material-symbols-outlined text-8xl mb-6 text-on-surface" style={{ fontVariationSettings: "'wght' 100" }}>menu_book</span>
          <p className="font-headline text-2xl font-bold tracking-tight">Selecciona un tema para repasar</p>
        </div>
      )}

      {/* Spacer at the bottom */}
      <div className="h-32 w-full flex-shrink-0 pointer-events-none" />

    </div>
  );
}
