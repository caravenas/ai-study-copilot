"use client";

import { useState, useEffect } from "react";
import { fetchSources, SourceItem } from "@/lib/api";

// ─── Helpers ─────────────────────────────────────────────────────────

function basename(path: string): string {
  return path.split("/").pop() || path;
}

// ─── Sub-components ──────────────────────────────────────────────────

function SourceCard({ source }: { source: SourceItem }) {
  const isPdf = source.source_type === "pdf";

  return (
    <div className="bg-surface-container-lowest rounded-[1rem] p-6 shadow-[0_4px_20px_rgba(42,52,57,0.04)] border border-outline-variant/20 hover:border-primary/30 transition-all cursor-default flex flex-col group font-body">
      <div className="flex items-start gap-4">
        <div
          className={`w-12 h-12 shrink-0 rounded-xl flex items-center justify-center group-hover:scale-105 transition-transform ${
            isPdf
              ? "bg-error-container/20 text-error"
              : "bg-primary-container/50 text-on-primary-container"
          }`}
        >
          <span
            className="material-symbols-outlined"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            {isPdf ? "picture_as_pdf" : "code_blocks"}
          </span>
        </div>

        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-on-surface text-[15px] leading-snug mb-1 group-hover:text-primary transition-colors truncate">
            {basename(source.source_file)}
          </h3>
          <p className="text-xs text-outline-variant font-medium">
            {isPdf ? "PDF Document" : "Jupyter Notebook"} • {source.chunk_count} chunks
          </p>
        </div>
      </div>

      <div className="mt-5 flex gap-2 flex-wrap font-label">
        <span
          className={`px-2 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md ${
            isPdf
              ? "bg-error-container/20 text-error"
              : "bg-primary-container/40 text-on-primary-container"
          }`}
        >
          {isPdf ? "PDF" : "Notebook"}
        </span>
        {source.module && (
          <span className="px-2 py-1 bg-secondary/10 text-secondary text-[10px] font-bold uppercase tracking-wider rounded-md">
            {source.module}
          </span>
        )}
        <span className="px-2 py-1 bg-surface-container text-on-surface-variant text-[10px] font-bold uppercase tracking-wider rounded-md">
          {source.chunk_count} chunks
        </span>
      </div>
    </div>
  );
}

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
        <span
          className={`material-symbols-outlined text-lg ${colorClass}`}
          style={{ fontVariationSettings: "'FILL' 1" }}
        >
          {icon}
        </span>
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
      setError(err instanceof Error ? err.message : "Failed to load sources");
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
          <h1 className="text-3xl font-bold text-on-surface font-headline">Explore Resources</h1>
          <p className="text-on-surface-variant mt-2 font-body">
            Browse indexed study materials — PDFs and Jupyter Notebooks.
          </p>
        </div>
        <button
          onClick={loadSources}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-surface-container-lowest border border-outline-variant/30 rounded-xl shadow-[0_4px_20px_rgba(42,52,57,0.04)] text-sm font-semibold text-on-surface hover:text-primary transition-colors font-body disabled:opacity-50"
          title="Refresh"
        >
          <span className={`material-symbols-outlined text-lg ${loading ? "animate-spin" : ""}`}>
            refresh
          </span>
          Refresh
        </button>
      </div>

      {/* Stats bar */}
      {!loading && !error && sources.length > 0 && (
        <div className="flex gap-6 bg-surface-container-lowest rounded-2xl px-8 py-5 border border-outline-variant/10 shadow-[0_4px_20px_rgba(42,52,57,0.04)] font-body">
          <div>
            <p className="text-2xl font-bold text-on-surface font-headline">{sources.length}</p>
            <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest font-label">
              Sources
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
              Total Chunks
            </p>
          </div>
        </div>
      )}

      {/* Loading state */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-24 text-on-surface-variant gap-4">
          <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
          <p className="text-sm font-medium font-body">Loading sources…</p>
        </div>
      )}

      {/* Error state */}
      {!loading && error && (
        <div className="flex flex-col items-center justify-center py-24 gap-4 text-center">
          <div className="w-14 h-14 rounded-2xl bg-error-container/30 flex items-center justify-center">
            <span
              className="material-symbols-outlined text-3xl text-error"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              error
            </span>
          </div>
          <div>
            <p className="text-sm font-semibold text-on-surface font-body">
              Could not load sources
            </p>
            <p className="text-xs text-outline-variant mt-1 font-body">{error}</p>
          </div>
          <button
            onClick={loadSources}
            className="mt-2 px-4 py-2 bg-primary text-on-primary text-sm font-semibold rounded-xl hover:opacity-90 transition-opacity font-body"
          >
            Try again
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
              No sources indexed yet
            </p>
            <p className="text-xs text-outline-variant mt-1 font-body">
              Upload PDFs or notebooks from the Admin panel to get started.
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
              <SourceCard key={source.source_file} source={source} />
            ))}
          </div>
        </section>
      )}

      {/* Notebooks Section */}
      {!loading && !error && notebooks.length > 0 && (
        <section>
          <SectionHeader
            icon="code_blocks"
            label="Notebooks — Labs"
            count={notebooks.length}
            colorClass="text-on-primary-container"
            bgClass="bg-primary-container/50"
          />
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {notebooks.map((source) => (
              <SourceCard key={source.source_file} source={source} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
