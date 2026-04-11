"use client";

export default function StudyView() {
  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-12 flex flex-col items-center justify-center pb-32">
        
      {/* Progress Bar */}
      <div className="w-full max-w-2xl mb-12">
          <div className="flex justify-between items-center mb-3">
            <span className="text-[10px] font-bold uppercase tracking-widest text-outline-variant font-label">Clase 02: Evaluación RAG</span>
            <span className="text-[10px] font-bold text-primary tracking-widest font-label uppercase">3 / 10 Cards</span>
          </div>
          <div className="w-full h-1.5 bg-surface-container-high rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-primary to-primary-dim w-[30%] rounded-full shadow-[0_0_10px_rgba(0,97,164,0.4)]"></div>
          </div>
      </div>

      {/* Flashcard */}
      <div className="w-full max-w-2xl bg-surface-container-lowest min-h-[400px] rounded-[2rem] p-12 flex flex-col justify-center items-center text-center shadow-[0_12px_40px_rgba(42,52,57,0.06)] border border-outline-variant/10 relative group cursor-pointer hover:shadow-[0_20px_50px_rgba(42,52,57,0.1)] transition-all">
          <span className="absolute top-8 left-8 text-[10px] font-bold tracking-widest uppercase text-outline-variant/50 font-label">Front Side</span>
          
          <h2 className="text-2xl md:text-3xl font-semibold text-on-surface leading-tight font-headline">
            ¿Cuál es la diferencia principal entre <span className="text-primary bg-primary-container/40 px-2 leading-none inline-block pb-1 rounded-md">Faithfulness</span> y <span className="text-primary bg-primary-container/40 px-2 leading-none inline-block pb-1 rounded-md">Answer Relevance</span>?
          </h2>

          <div className="absolute bottom-8 mx-auto text-outline-variant/50 group-hover:text-primary/70 transition-colors flex flex-col items-center gap-1 font-label">
            <span className="text-[10px] font-bold uppercase tracking-widest">Click to flip</span>
            <span className="material-symbols-outlined text-sm">360</span>
          </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-12 flex items-center justify-center gap-4 w-full max-w-2xl font-body">
          <button className="flex-1 py-4 bg-[#fff1f0] text-error font-semibold rounded-2xl hover:bg-[#ffe3e1] transition-colors border border-[#ffcfcc]">Hard</button>
          <button className="flex-1 py-4 bg-[#fff8e6] text-[#b37400] font-semibold rounded-2xl hover:bg-[#ffedcc] transition-colors border border-[#ffe099]">Medium</button>
          <button className="flex-1 py-4 bg-[#e8f7ed] text-[#0f7a3f] font-semibold rounded-2xl hover:bg-[#d4f0df] transition-colors border border-[#b8e5cb]">Easy</button>
      </div>

    </div>
  );
}
