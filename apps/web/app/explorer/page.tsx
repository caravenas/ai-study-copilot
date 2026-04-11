"use client";

export default function ExplorerView() {
  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-12 space-y-8 pb-32">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-display-lg font-headline font-bold tracking-tight text-on-surface">Explore Resources</h1>
          <p className="text-on-surface-variant mt-2 font-body">Manage study material including PDFs, Notebooks, and articles.</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-surface-container-lowest border border-outline-variant/30 rounded-xl shadow-[0_4px_20px_rgba(42,52,57,0.04)] text-sm font-semibold text-on-surface hover:text-primary transition-colors font-body">
          <span className="material-symbols-outlined">filter_list</span>
          Filter
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        
        {/* Card PDF */}
        <div className="bg-surface-container-lowest rounded-[1rem] p-6 shadow-[0_4px_20px_rgba(42,52,57,0.04)] border border-outline-variant/20 hover:border-primary/30 transition-all cursor-pointer flex flex-col group font-body">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 shrink-0 rounded-xl bg-error-container/20 text-error flex items-center justify-center group-hover:scale-105 transition-transform">
              <span className="material-symbols-outlined" style={{fontVariationSettings: "'FILL' 1"}}>picture_as_pdf</span>
            </div>
            <div>
              <h3 className="font-semibold text-on-surface text-[15px] leading-snug mb-1 group-hover:text-primary transition-colors">clase_02_evaluacion_rag.pdf</h3>
              <p className="text-xs text-outline-variant font-medium">PDF Document • 24 Pages</p>
            </div>
          </div>
          <div className="mt-6 flex gap-2 font-label">
            <span className="px-2 py-1 bg-surface-container text-on-surface-variant text-[10px] font-bold uppercase tracking-wider rounded-md">Theory</span>
            <span className="px-2 py-1 bg-surface-container text-on-surface-variant text-[10px] font-bold uppercase tracking-wider rounded-md">Metrics</span>
          </div>
        </div>

        {/* Card Notebook */}
        <div className="bg-surface-container-lowest rounded-[1rem] p-6 shadow-[0_4px_20px_rgba(42,52,57,0.04)] border border-outline-variant/20 hover:border-primary/30 transition-all cursor-pointer flex flex-col group font-body">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 shrink-0 rounded-xl bg-primary-container/50 text-on-primary-container flex items-center justify-center group-hover:scale-105 transition-transform">
              <span className="material-symbols-outlined" style={{fontVariationSettings: "'FILL' 1"}}>code_blocks</span>
            </div>
            <div>
              <h3 className="font-semibold text-on-surface text-[15px] leading-snug mb-1 group-hover:text-primary transition-colors">1_Evaluacion_Ragas.ipynb</h3>
              <p className="text-xs text-outline-variant font-medium">Jupyter Notebook • Lab</p>
            </div>
          </div>
          <div className="mt-6 flex gap-2 font-label">
            <span className="px-2 py-1 bg-primary-container/40 text-on-primary-container text-[10px] font-bold uppercase tracking-wider rounded-md">Practice</span>
            <span className="px-2 py-1 bg-surface-container text-on-surface-variant text-[10px] font-bold uppercase tracking-wider rounded-md">Colab</span>
          </div>
        </div>

        {/* Add New Card */}
        <div className="border border-dashed border-outline-variant/50 rounded-[1rem] p-6 hover:border-primary/60 hover:bg-primary-container/10 transition-colors cursor-pointer flex flex-col items-center justify-center min-h-[160px] font-body bg-transparent">
            <div className="w-12 h-12 rounded-full bg-surface-container-high text-on-surface-variant flex items-center justify-center mb-3">
               <span className="material-symbols-outlined">add</span>
            </div>
            <span className="text-sm font-semibold text-on-surface-variant">Import material</span>
        </div>

      </div>
    </div>
  );
}
