"use client";

export default function ChatView() {
  return (
    <>
      {/* Chat Canvas */}
      <div className="flex-1 overflow-y-auto p-6 md:p-12 space-y-8 scroll-smooth pb-40">
        
        {/* User Message */}
        <div className="flex flex-col items-end">
          <div className="max-w-[80%] bg-surface-container-lowest p-5 rounded-2xl rounded-tr-none shadow-[0_4px_20px_rgba(42,52,57,0.04)]">
            <p className="text-on-surface leading-relaxed font-body">Can you explain the main concepts of Cellular Respiration mentioned in today's lecture?</p>
          </div>
          <span className="text-[10px] text-outline-variant mt-2 px-1 font-label font-medium uppercase tracking-wider">You • 10:42 AM</span>
        </div>

        {/* AI Message */}
        <div className="flex flex-col items-start">
          <div className="flex items-start gap-4 max-w-[90%]">
            <div className="mt-1 w-8 h-8 rounded-lg bg-primary-container flex items-center justify-center flex-shrink-0">
              <span className="material-symbols-outlined text-primary text-lg" style={{fontVariationSettings: "'FILL' 1"}}>auto_awesome</span>
            </div>
            
            <div className="bg-tertiary-container/40 backdrop-blur-sm p-6 rounded-3xl rounded-tl-none border border-white/50">
              <h3 className="text-headline-md font-headline font-bold text-on-primary-container mb-4">Cellular Respiration Overview</h3>
              <div className="space-y-4 text-on-surface leading-relaxed font-body">
                <p>Cellular respiration is the process by which biological fuels are oxidized in the presence of an inorganic electron acceptor, such as oxygen, to produce large amounts of energy, to drive the bulk production of ATP.</p>
                <p>The process occurs in four main stages:</p>
                <ul className="list-disc pl-5 space-y-2">
                  <li><strong>Glycolysis:</strong> Breaking down glucose into pyruvate.</li>
                  <li><strong>Pyruvate Oxidation:</strong> Converting pyruvate into Acetyl-CoA.</li>
                  <li><strong>Citric Acid Cycle:</strong> Generating high-energy electron carriers (NADH, FADH2).</li>
                  <li><strong>Oxidative Phosphorylation:</strong> Using the electron transport chain to create a proton gradient.</li>
                </ul>
              </div>

              {/* Citations Section */}
              <details className="group mt-6 border-t border-primary/10 pt-4 cursor-pointer">
                <summary className="flex items-center justify-between text-sm font-semibold text-primary/80 hover:text-primary transition-colors list-none">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-sm">menu_book</span>
                    Citations
                  </div>
                  <span className="material-symbols-outlined text-sm group-open:rotate-180 transition-transform">expand_more</span>
                </summary>
                <div className="mt-3 p-3 bg-surface-container-lowest/50 rounded-xl text-xs text-on-surface-variant font-medium">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="material-symbols-outlined text-[14px]">description</span>
                    Source: <span className="font-bold text-on-surface">clase_07.pdf</span>
                    <span className="text-outline mx-1">•</span>
                    Page 12
                  </div>
                </div>
              </details>

              {/* Related Labs Section */}
              <div className="mt-6 pt-6 border-t border-primary/10">
                <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest block mb-3">Related Practice Materials</span>
                <div className="flex flex-wrap gap-2">
                  <button className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-primary-container transition-colors rounded-full text-xs font-semibold text-on-surface border border-outline-variant/20 shadow-sm">
                    <span className="material-symbols-outlined text-sm text-primary">lab_profile</span>
                    Lab 03: Mitochondrial ATP Assay
                  </button>
                  <button className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-primary-container transition-colors rounded-full text-xs font-semibold text-on-surface border border-outline-variant/20 shadow-sm">
                    <span className="material-symbols-outlined text-sm text-primary">quiz</span>
                    Krebs Cycle Practice Quiz
                  </button>
                </div>
              </div>
            </div>
          </div>
          <span className="text-[10px] text-outline-variant mt-2 ml-12 font-label font-medium uppercase tracking-wider">AI Assistant • Just Now</span>
        </div>
      </div>

      {/* Message Input Area */}
      <div className="absolute bottom-0 w-full p-8 md:p-12 pt-0 bg-gradient-to-t from-surface via-surface to-transparent pointer-events-none">
        <div className="max-w-4xl mx-auto pointer-events-auto">
          <div className="bg-surface-container-lowest rounded-3xl p-2 shadow-[0_12px_40px_rgba(42,52,57,0.06)] flex items-end gap-2 border border-outline-variant/10">
            <button className="p-3 text-on-surface-variant hover:text-primary transition-colors rounded-2xl hover:bg-surface-container-low">
              <span className="material-symbols-outlined">attach_file</span>
            </button>
            <textarea 
              className="flex-1 bg-transparent border-none focus:ring-0 py-3 text-on-surface placeholder:text-outline-variant font-body resize-none outline-none" 
              placeholder="Ask Study Copilot anything..." 
              rows={1}
            />
            <button className="bg-primary p-3 rounded-2xl text-white shadow-lg shadow-primary/20 hover:scale-105 active:scale-95 transition-all">
              <span className="material-symbols-outlined">send</span>
            </button>
          </div>
          
          <div className="flex justify-center gap-6 mt-4">
            <button className="text-[11px] font-semibold text-on-surface-variant/60 hover:text-primary transition-colors flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">lightbulb</span>
              Summarize this topic
            </button>
            <button className="text-[11px] font-semibold text-on-surface-variant/60 hover:text-primary transition-colors flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">format_list_bulleted</span>
              Create a study plan
            </button>
            <button className="text-[11px] font-semibold text-on-surface-variant/60 hover:text-primary transition-colors flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">edit_note</span>
              Generate flashcards
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
