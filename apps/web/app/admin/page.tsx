"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { uploadFile, fetchSources, IngestResponse, SourceItem } from "@/lib/api";

// ─── Helpers ─────────────────────────────────────────────────────────
function basename(path: string): string {
  return path.split("/").pop() || path;
}

// ─── Sub-components ──────────────────────────────────────────────────

interface UploadItemProps {
  file: File;
  status: "pending" | "uploading" | "done" | "error";
  result?: IngestResponse;
  error?: string;
}

function UploadItem({ file, status, result, error }: UploadItemProps) {
  const isPdf = file.name.endsWith(".pdf");
  const icon = isPdf ? "picture_as_pdf" : "code";
  const sizeKb = (file.size / 1024).toFixed(0);

  return (
    <div className="flex items-center gap-4 bg-surface-container-lowest p-4 rounded-2xl border border-outline-variant/10 shadow-sm">
      <div
        className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
          isPdf ? "bg-primary-container" : "bg-tertiary-container"
        }`}
      >
        <span
          className={`material-symbols-outlined text-lg ${
            isPdf ? "text-primary" : "text-tertiary"
          }`}
          style={{ fontVariationSettings: "'FILL' 1" }}
        >
          {icon}
        </span>
      </div>

      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold text-on-surface truncate">{file.name}</p>
        <p className="text-[11px] text-on-surface-variant">
          {sizeKb} KB
          {status === "done" && result && (
            <span className="text-green-600 ml-2">
              ✓ {result.chunks_indexed} chunks indexed
            </span>
          )}
          {status === "error" && (
            <span className="text-error ml-2">✗ {error}</span>
          )}
        </p>
      </div>

      <div className="flex-shrink-0">
        {status === "uploading" && (
          <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
        )}
        {status === "done" && (
          <span className="material-symbols-outlined text-green-600 text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>
            check_circle
          </span>
        )}
        {status === "error" && (
          <span className="material-symbols-outlined text-error text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>
            error
          </span>
        )}
        {status === "pending" && (
          <span className="material-symbols-outlined text-outline-variant text-xl">
            schedule
          </span>
        )}
      </div>
    </div>
  );
}

function SourceCard({ source }: { source: SourceItem }) {
  const isPdf = source.source_type === "pdf";
  return (
    <div className="flex items-center gap-4 p-4 rounded-2xl bg-surface hover:bg-surface-container-low transition-colors border border-outline-variant/10">
      <div
        className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
          isPdf ? "bg-primary-container" : "bg-tertiary-container"
        }`}
      >
        <span
          className={`material-symbols-outlined text-lg ${
            isPdf ? "text-primary" : "text-tertiary"
          }`}
          style={{ fontVariationSettings: "'FILL' 1" }}
        >
          {isPdf ? "picture_as_pdf" : "code"}
        </span>
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold text-on-surface truncate">{basename(source.source_file)}</p>
        <div className="flex gap-2 items-center text-[11px] text-on-surface-variant font-medium mt-1 uppercase font-label tracking-widest">
          <span className="font-bold">{source.source_type}</span>
          <span className="text-outline-variant font-light">•</span>
          <span>{source.chunk_count} fragmentos de memoria</span>
          {source.module && (
            <>
              <span className="text-outline-variant font-light">•</span>
              <span className="bg-secondary/10 text-secondary px-2 py-0.5 rounded shadow-sm">{source.module}</span>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Main Page ───────────────────────────────────────────────────────

export default function AdminView() {
  const [files, setFiles] = useState<UploadItemProps[]>([]);
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [loadingSources, setLoadingSources] = useState(true);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Load sources on mount
  useEffect(() => {
    loadSources();
  }, []);

  async function loadSources() {
    setLoadingSources(true);
    try {
      const data = await fetchSources();
      setSources(data.sources);
    } catch {
      // silently fail — sources section will show empty
    } finally {
      setLoadingSources(false);
    }
  }

  const processFiles = useCallback(async (newFiles: File[]) => {
    const validFiles = newFiles.filter((f) => {
      const ext = f.name.split(".").pop()?.toLowerCase();
      return ext === "pdf" || ext === "ipynb";
    });

    if (validFiles.length === 0) return;

    // Add all files as pending
    const items: UploadItemProps[] = validFiles.map((f) => ({
      file: f,
      status: "pending" as const,
    }));

    setFiles((prev) => [...prev, ...items]);

    // Upload sequentially
    for (let i = 0; i < validFiles.length; i++) {
      const file = validFiles[i];

      setFiles((prev) =>
        prev.map((item) =>
          item.file === file ? { ...item, status: "uploading" as const } : item
        )
      );

      try {
        const result = await uploadFile(file);
        setFiles((prev) =>
          prev.map((item) =>
            item.file === file
              ? { ...item, status: "done" as const, result }
              : item
          )
        );
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : "Upload failed";
        setFiles((prev) =>
          prev.map((item) =>
            item.file === file
              ? { ...item, status: "error" as const, error: msg }
              : item
          )
        );
      }
    }

    // Refresh sources after all uploads
    await loadSources();
  }, []);

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setIsDragOver(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    processFiles(droppedFiles);
  }

  function handleFileInput(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files) {
      processFiles(Array.from(e.target.files));
      e.target.value = ""; // reset so same file can be re-selected
    }
  }

  const completedCount = files.filter((f) => f.status === "done").length;
  const totalChunks = files.reduce(
    (sum, f) => sum + (f.result?.chunks_indexed ?? 0),
    0
  );

  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-12 space-y-8 pb-32">
      <div className="mb-4">
        <h1 className="text-3xl font-bold text-on-surface font-headline">Knowledge Admin</h1>
        <p className="text-on-surface-variant mt-2 font-body">
          Manage your RAG data sources, index PDFs, and control the vector database.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
        {/* Upload Section */}
        <section className="bg-surface-container-lowest rounded-[2rem] p-8 md:p-10 border border-outline-variant/10 shadow-[0_4px_20px_rgba(42,52,57,0.04)] font-body flex flex-col max-h-[calc(100vh-220px)] h-full">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-14 h-14 rounded-2xl bg-primary-fixed text-primary-fixed-dim flex items-center justify-center">
              <span
                className="material-symbols-outlined text-2xl text-on-primary-fixed"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                upload_file
              </span>
            </div>
            <div>
              <h2 className="text-lg font-bold text-on-surface font-headline">
                Ingest Documents
              </h2>
              <p className="text-xs text-on-surface-variant">
                PDF and Jupyter Notebook (.ipynb)
              </p>
            </div>
          </div>

          {/* Drop zone */}
          <div
            className={`w-full border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-200 group ${
              isDragOver
                ? "border-primary bg-primary-container/20 scale-[1.01]"
                : "border-outline-variant/30 bg-surface hover:bg-surface-container hover:border-primary/40"
            }`}
            onClick={() => fileInputRef.current?.click()}
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragOver(true);
            }}
            onDragLeave={() => setIsDragOver(false)}
            onDrop={handleDrop}
          >
            <span
              className={`material-symbols-outlined text-4xl mb-3 transition-colors ${
                isDragOver ? "text-primary" : "text-outline-variant group-hover:text-primary"
              }`}
            >
              cloud_upload
            </span>
            <p className="text-sm font-semibold text-on-surface-variant">
              {isDragOver ? "Drop files here" : "Drag & Drop your files here"}
            </p>
            <p className="text-xs text-outline-variant mt-1">
              or click to browse • .pdf, .ipynb
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.ipynb"
              multiple
              className="hidden"
              onChange={handleFileInput}
            />
          </div>

          {/* Upload queue */}
          {files.length > 0 && (
            <div className="mt-6 flex flex-col min-h-0 flex-1">
              <div className="flex items-center justify-between shrink-0 mb-3">
                <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest font-label">
                  Upload Queue
                </span>
                {completedCount > 0 && (
                  <span className="text-[11px] font-medium text-green-600">
                    {completedCount} done • {totalChunks} chunks
                  </span>
                )}
              </div>
              <div className="space-y-3 overflow-y-auto pr-2 flex-1">
                {files.map((item, i) => (
                  <UploadItem key={`${item.file.name}-${i}`} {...item} />
                ))}
              </div>
            </div>
          )}
        </section>

        {/* Sources Section */}
        <section className="bg-surface-container-lowest rounded-[2rem] p-8 md:p-10 border border-outline-variant/10 shadow-[0_4px_20px_rgba(42,52,57,0.04)] font-body flex flex-col max-h-[calc(100vh-220px)] h-full">
          <div className="flex items-center justify-between mb-6 shrink-0">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 rounded-2xl bg-tertiary-fixed text-on-tertiary-fixed flex items-center justify-center">
                <span
                  className="material-symbols-outlined text-2xl"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  database
                </span>
              </div>
              <div>
                <h2 className="text-lg font-bold text-on-surface font-headline">
                  Indexed Sources
                </h2>
                <p className="text-xs text-on-surface-variant">
                  {sources.length} source{sources.length !== 1 ? "s" : ""} in vector store
                </p>
              </div>
            </div>
            <button
              onClick={loadSources}
              className="p-2 rounded-xl hover:bg-surface-container-low transition-colors text-on-surface-variant hover:text-primary"
              title="Refresh"
            >
              <span className="material-symbols-outlined text-xl">refresh</span>
            </button>
          </div>

          <div className="flex-1 space-y-2 overflow-y-auto pr-2 min-h-0">
            {loadingSources ? (
              <div className="flex items-center justify-center py-12 text-on-surface-variant">
                <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin mr-3" />
                Loading sources...
              </div>
            ) : sources.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <span className="material-symbols-outlined text-4xl text-outline-variant mb-3">
                  folder_off
                </span>
                <p className="text-sm font-semibold text-on-surface-variant">
                  No sources indexed yet
                </p>
                <p className="text-xs text-outline-variant mt-1">
                  Upload PDFs or notebooks to get started
                </p>
              </div>
            ) : (
              sources.map((s) => (
                <SourceCard key={s.source_file} source={s} />
              ))
            )}
          </div>

          {/* Stats bar */}
          {sources.length > 0 && (
            <div className="mt-6 pt-6 border-t border-outline-variant/10 flex items-center gap-6 shrink-0">
              <div>
                <p className="text-2xl font-bold text-on-surface font-headline">
                  {sources.reduce((sum, s) => sum + s.chunk_count, 0)}
                </p>
                <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest font-label">
                  Total Chunks
                </p>
              </div>
              <div>
                <p className="text-2xl font-bold text-on-surface font-headline">
                  {sources.filter((s) => s.source_type === "pdf").length}
                </p>
                <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest font-label">
                  PDFs
                </p>
              </div>
              <div>
                <p className="text-2xl font-bold text-on-surface font-headline">
                  {sources.filter((s) => s.source_type === "notebook").length}
                </p>
                <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest font-label">
                  Notebooks
                </p>
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
