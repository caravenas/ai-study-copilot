"use client";

import { useState, useEffect } from "react";
import { fetchSources, SourceItem } from "@/lib/api";
import { MaterialIcon } from "@/components/shared/MaterialIcon";
import { SourceCard } from "@/components/sources/SourceCard";

// ─── Sub-components ──────────────────────────────────────────────────

function SectionHeader({
  icon,
  label,
  count,
  colorClass,
  bgClass,
}: {
  icon: string;
  label: string;
  count: number;
  colorClass: string;
  bgClass: string;
}) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${bgClass}`}>
        <MaterialIcon name={icon} filled className={`text-lg ${colorClass}`} />
      </div>
      <h2 className="text-base font-bold text-on-surface font-headline">{label}</h2>
      <span className="ml-auto text-xs font-semibold text-on-surface-variant bg-surface-container px-2.5 py-1 rounded-full font-label">
        {count}
      </span>
    </div>
  );
}

// ─── Main Page ───────────────────────────────────────────────────────

export default function ExplorerView() {
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSources();
  }, []);

  async function loadSources() {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchSources();
      setSources(data.sources);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "No se pudieron cargar las fuentes");
    } finally {
      setLoading(false);
    }
  }

  const pdfs = sources.filter((s) => s.source_type === "pdf");
  const notebooks = sources.filter((s) => s.source_type !== "pdf");
  const totalChunks = sources.reduce((sum, s) => sum + s.chunk_count, 0);

  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-12 space-y-8 pb-32">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-on-surface font-headline">Explorar recursos</h1>
          <p className="text-on-surface-variant mt-2 font-body">
            Navega los materiales de estudio indexados — PDFs y notebooks de Jupyter.
          </p>
        </div>
        <button
          onClick={loadSources}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-surface-container-lowest border border-outline-variant/30 rounded-xl shadow-[0_4px_20px_rgba(42,52,57,0.04)] text-sm font-semibold text-on-surface hover:text-primary transition-colors font-body disabled:opacity-50"
          title="Actualizar"
        >
          <span className={`material-symbols-outlined text-lg ${loading ? "animate-spin" : ""}`}>
            refresh
          </span>
          Actualizar
        </button>
      </div>

      {/* Stats bar */}
      {!loading && !error && sources.length > 0 && (
        <div className="flex gap-6 bg-surface-container-lowest rounded-2xl px-8 py-5 border border-outline-variant/10 shadow-[0_4px_20px_rgba(42,52,57,0.04)] font-body">
          <div>
            <p className="text-2xl font-bold text-on-surface font-headline">{sources.length}</p>
            <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest font-label">
              Fuentes
            </p>
          </div>
          <div className="w-px bg-outline-variant/20" />
          <div>
            <p className="text-2xl font-bold text-on-surface font-headline">{pdfs.length}</p>
            <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest font-label">
              PDFs
            </p>
          </div>
          <div className="w-px bg-outline-variant/20" />
          <div>
            <p className="text-2xl font-bold text-on-surface font-headline">{notebooks.length}</p>
            <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest font-label">
              Notebooks
            </p>
          </div>
          <div className="w-px bg-outline-variant/20" />
          <div>
            <p className="text-2xl font-bold text-on-surface font-headline">{totalChunks}</p>
            <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest font-label">
              Fragmentos totales
            </p>
          </div>
        </div>
      )}

      {/* Loading state */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-24 text-on-surface-variant gap-4">
          <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
          <p className="text-sm font-medium font-body">Cargando fuentes…</p>
        </div>
      )}

      {/* Error state */}
      {!loading && error && (
        <div className="flex flex-col items-center justify-center py-24 gap-4 text-center">
          <div className="w-14 h-14 rounded-2xl bg-error-container/30 flex items-center justify-center">
            <MaterialIcon name="error" filled className="text-3xl text-error" />
          </div>
          <div>
            <p className="text-sm font-semibold text-on-surface font-body">
              No se pudieron cargar las fuentes
            </p>
            <p className="text-xs text-outline-variant mt-1 font-body">{error}</p>
          </div>
          <button
            onClick={loadSources}
            className="mt-2 px-4 py-2 bg-primary text-on-primary text-sm font-semibold rounded-xl hover:opacity-90 transition-opacity font-body"
          >
            Reintentar
          </button>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && sources.length === 0 && (
        <div className="flex flex-col items-center justify-center py-24 gap-4 text-center">
          <div className="w-14 h-14 rounded-2xl bg-surface-container-high flex items-center justify-center">
            <span className="material-symbols-outlined text-3xl text-outline-variant">
              folder_off
            </span>
          </div>
          <div>
            <p className="text-sm font-semibold text-on-surface-variant font-body">
              Aún no hay fuentes indexadas
            </p>
            <p className="text-xs text-outline-variant mt-1 font-body">
              Sube PDFs o notebooks desde el panel Admin para empezar.
            </p>
          </div>
        </div>
      )}

      {/* PDFs Section */}
      {!loading && !error && pdfs.length > 0 && (
        <section>
          <SectionHeader
            icon="picture_as_pdf"
            label="PDFs — Clases"
            count={pdfs.length}
            colorClass="text-error"
            bgClass="bg-error-container/20"
          />
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {pdfs.map((source) => (
              <SourceCard key={source.source_file} source={source} variant="card" />
            ))}
          </div>
        </section>
      )}

      {/* Notebooks Section */}
      {!loading && !error && notebooks.length > 0 && (
        <section>
          <SectionHeader
            icon="code_blocks"
            label="Notebooks — Prácticas"
            count={notebooks.length}
            colorClass="text-on-primary-container"
            bgClass="bg-primary-container/50"
          />
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {notebooks.map((source) => (
              <SourceCard key={source.source_file} source={source} variant="card" />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
