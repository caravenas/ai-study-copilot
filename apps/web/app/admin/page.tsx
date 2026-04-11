"use client";

export default function AdminView() {
  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-12 space-y-8 pb-32">
      
      <div className="mb-4">
        <h1 className="text-display-lg font-bold text-on-surface font-headline">Knowledge Admin</h1>
        <p className="text-on-surface-variant mt-2 font-body">Manage your RAG data sources, index PDFs, and control the vector database.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Upload PDF Section */}
        <section className="bg-surface-container-lowest rounded-[2rem] p-10 border border-outline-variant/10 shadow-[0_4px_20px_rgba(42,52,57,0.04)] flex flex-col items-center justify-center text-center font-body">
          <div className="w-16 h-16 rounded-2xl bg-primary-fixed text-primary-fixed-dim flex items-center justify-center mb-6">
             <span className="material-symbols-outlined text-3xl text-on-primary-fixed" style={{fontVariationSettings: "'FILL' 1"}}>upload_file</span>
          </div>
          <h2 className="text-lg font-bold text-on-surface mb-2 font-headline">Ingest PDF Documents</h2>
          <p className="text-sm text-on-surface-variant mb-8 max-w-[280px]">Upload classes or reading material to process, chunk, and embed them into the RAG.</p>
          
          <div className="w-full border-2 border-dashed border-outline-variant/30 rounded-2xl p-10 bg-surface hover:bg-surface-container hover:border-primary/40 transition-colors cursor-pointer group">
             <span className="material-symbols-outlined text-4xl text-outline-variant group-hover:text-primary transition-colors mb-3">cloud_upload</span>
             <p className="text-sm font-semibold text-on-surface-variant">Drag & Drop your PDFs here</p>
             <p className="text-xs text-outline-variant mt-1">or click to browse</p>
          </div>
        </section>

        {/* Add Notebook Section */}
        <section className="bg-surface-container-lowest rounded-[2rem] p-10 border border-outline-variant/10 shadow-[0_4px_20px_rgba(42,52,57,0.04)] flex flex-col justify-between font-body">
          <div>
            <div className="w-16 h-16 rounded-2xl bg-tertiary-fixed text-on-tertiary-fixed flex items-center justify-center mb-6">
               <span className="material-symbols-outlined text-3xl" style={{fontVariationSettings: "'FILL' 1"}}>code</span>
            </div>
            <h2 className="text-lg font-bold text-on-surface mb-2 font-headline">Add Jupyter Notebook</h2>
            <p className="text-sm text-on-surface-variant mb-8 max-w-[280px]">Link external Google Colab notebooks or Jupyter files to reference code labs.</p>
            
            <div className="flex flex-col gap-3">
               <label className="text-[10px] font-bold text-outline-variant uppercase tracking-widest font-label">Notebook URL</label>
               <div className="flex gap-2">
                 <input type="url" placeholder="https://colab.research.google.com/..." className="flex-1 bg-surface border border-outline-variant/20 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all text-on-surface placeholder:text-outline-variant/50" />
                 <button className="bg-gradient-to-br from-primary to-primary-dim hover:opacity-90 text-white rounded-xl px-6 py-3 text-sm font-semibold transition-opacity shadow-sm">Add</button>
               </div>
            </div>
          </div>

          {/* Danger Zone */}
          <div className="mt-12 pt-8 border-t border-outline-variant/10">
             <h2 className="text-xs font-bold text-error mb-3 font-label uppercase tracking-widest">Danger Zone</h2>
             <div className="flex items-center justify-between bg-error-container/20 rounded-[1rem] p-5 border border-error-container">
               <div>
                 <h3 className="text-sm font-semibold text-on-surface">Reindex Vector Database</h3>
                 <p className="text-[11px] text-on-surface-variant mt-1">This will wipe ChromaDB and re-process all manifest files.</p>
               </div>
               <button className="bg-white text-error border border-error-container hover:bg-error-container/10 px-4 py-2.5 rounded-xl text-xs font-bold shadow-sm transition-colors">Reindex All</button>
             </div>
          </div>
        </section>

      </div>
    </div>
  );
}
