"use client";

import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { queryApi, QueryResponse, CitationItem, RelatedLab } from "@/lib/api";

// Strip <think>...</think> blocks from LLM responses (model reasoning traces)
function stripThinkTags(text: string): string {
  return text.replace(/<think>[\s\S]*?<\/think>\s*/g, "").trim();
}

// ─── Types ───────────────────────────────────────────────────────────
interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  citations?: CitationItem[];
  related_labs?: RelatedLab[];
  confidence?: number;
}

// ─── Helpers ─────────────────────────────────────────────────────────
function timeLabel(d: Date) {
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

// ─── Sub-components ──────────────────────────────────────────────────

function UserBubble({ msg }: { msg: Message }) {
  return (
    <div className="flex flex-col items-end animate-[fadeSlideUp_0.3s_ease]">
      <div className="max-w-[80%] bg-surface-container-lowest p-5 rounded-2xl rounded-tr-none shadow-[0_4px_20px_rgba(42,52,57,0.04)]">
        <p className="text-on-surface leading-relaxed font-body">{msg.content}</p>
      </div>
      <span className="text-[10px] text-outline-variant mt-2 px-1 font-label font-medium uppercase tracking-wider">
        You • {timeLabel(msg.timestamp)}
      </span>
    </div>
  );
}

function AssistantBubble({ msg }: { msg: Message }) {
  return (
    <div className="flex flex-col items-start animate-[fadeSlideUp_0.3s_ease]">
      <div className="flex items-start gap-4 max-w-[90%]">
        <div className="mt-1 w-8 h-8 rounded-lg bg-primary-container flex items-center justify-center flex-shrink-0">
          <span
            className="material-symbols-outlined text-primary text-lg"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            auto_awesome
          </span>
        </div>

        <div className="bg-tertiary-container/40 backdrop-blur-sm p-6 rounded-3xl rounded-tl-none border border-white/50">
          {/* Answer text — rendered as markdown */}
          <div className="prose prose-sm max-w-none text-on-surface leading-relaxed font-body
            prose-headings:font-headline prose-headings:text-on-primary-container prose-headings:font-bold
            prose-h1:text-xl prose-h2:text-lg prose-h3:text-base
            prose-strong:text-on-surface prose-strong:font-semibold
            prose-ul:my-2 prose-li:my-0.5
            prose-p:my-2">
            <ReactMarkdown>{stripThinkTags(msg.content)}</ReactMarkdown>
          </div>

          {/* Confidence badge */}
          {msg.confidence !== undefined && (
            <div className="mt-4 flex items-center gap-2">
              <span className="text-[10px] font-label font-bold uppercase tracking-widest text-on-surface-variant">
                Confidence
              </span>
              <div className="h-1.5 w-24 bg-surface-container-high rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{
                    width: `${Math.round((msg.confidence ?? 0) * 100)}%`,
                    backgroundColor:
                      msg.confidence >= 0.7
                        ? "#2e7d32"
                        : msg.confidence >= 0.4
                        ? "#ed6c02"
                        : "#d32f2f",
                  }}
                />
              </div>
              <span className="text-[11px] font-medium text-on-surface-variant">
                {Math.round((msg.confidence ?? 0) * 100)}%
              </span>
            </div>
          )}

          {/* Citations */}
          {msg.citations && msg.citations.length > 0 && (
            <details className="group mt-6 border-t border-primary/10 pt-4 cursor-pointer">
              <summary className="flex items-center justify-between text-sm font-semibold text-primary/80 hover:text-primary transition-colors list-none">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">menu_book</span>
                  {msg.citations.length} Citation{msg.citations.length > 1 ? "s" : ""}
                </div>
                <span className="material-symbols-outlined text-sm group-open:rotate-180 transition-transform">
                  expand_more
                </span>
              </summary>
              <div className="mt-3 space-y-2">
                {msg.citations.map((c, i) => (
                  <div
                    key={i}
                    className="p-3 bg-surface-container-lowest/50 rounded-xl text-xs text-on-surface-variant font-medium"
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span className="material-symbols-outlined text-[14px]">description</span>
                      <span className="font-bold text-on-surface">{c.source_file.split("/").pop()}</span>
                      {c.page && (
                        <>
                          <span className="text-outline mx-1">•</span>
                          Page {c.page}
                        </>
                      )}
                    </div>
                    <p className="text-[11px] text-on-surface-variant/80 mt-1 line-clamp-2 italic">
                      &ldquo;{c.excerpt}&rdquo;
                    </p>
                  </div>
                ))}
              </div>
            </details>
          )}

          {/* Related labs */}
          {msg.related_labs && msg.related_labs.length > 0 && (
            <div className="mt-6 pt-6 border-t border-primary/10">
              <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest block mb-3">
                Related Practice Materials
              </span>
              <div className="flex flex-wrap gap-2">
                {msg.related_labs.map((lab, i) => (
                  <button
                    key={i}
                    className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-primary-container transition-colors rounded-full text-xs font-semibold text-on-surface border border-outline-variant/20 shadow-sm"
                  >
                    <span className="material-symbols-outlined text-sm text-primary">lab_profile</span>
                    {lab.source_file.split("/").pop()}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
      <span className="text-[10px] text-outline-variant mt-2 ml-12 font-label font-medium uppercase tracking-wider">
        AI Assistant • {timeLabel(msg.timestamp)}
      </span>
    </div>
  );
}

function ThinkingIndicator() {
  return (
    <div className="flex flex-col items-start animate-[fadeSlideUp_0.3s_ease]">
      <div className="flex items-start gap-4">
        <div className="mt-1 w-8 h-8 rounded-lg bg-primary-container flex items-center justify-center flex-shrink-0">
          <span
            className="material-symbols-outlined text-primary text-lg animate-pulse"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            auto_awesome
          </span>
        </div>
        <div className="bg-tertiary-container/40 backdrop-blur-sm p-6 rounded-3xl rounded-tl-none border border-white/50">
          <div className="flex items-center gap-3 text-on-surface-variant font-body text-sm">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:0ms]" />
              <span className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:150ms]" />
              <span className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:300ms]" />
            </div>
            Searching documents and generating answer…
          </div>
        </div>
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center px-6 select-none">
      <div className="bg-primary-container/30 p-5 rounded-2xl mb-6">
        <span
          className="material-symbols-outlined text-primary text-5xl"
          style={{ fontVariationSettings: "'FILL' 1" }}
        >
          school
        </span>
      </div>
      <h2 className="text-2xl font-headline font-black text-on-surface mb-2">
        Ask me anything about your courses
      </h2>
      <p className="text-on-surface-variant font-body max-w-md leading-relaxed">
        I'll search through your uploaded PDFs and notebooks to give you grounded answers with citations.
      </p>
    </div>
  );
}

// ─── Main Page ───────────────────────────────────────────────────────

export default function ChatView() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll on new messages
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto";
      ta.style.height = `${Math.min(ta.scrollHeight, 160)}px`;
    }
  }, [input]);

  async function handleSubmit(questionOverride?: string) {
    const question = (questionOverride ?? input).trim();
    if (!question || isLoading) return;

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setError(null);
    setIsLoading(true);

    try {
      const data: QueryResponse = await queryApi({ question });

      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: data.answer,
        timestamp: new Date(),
        citations: data.citations,
        related_labs: data.related_labs,
        confidence: data.confidence,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : "Unknown error";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
      textareaRef.current?.focus();
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  const quickActions = [
    { icon: "lightbulb", label: "Summarize this topic", prompt: "Give me a summary of the main topics in my course materials" },
    { icon: "format_list_bulleted", label: "Create a study plan", prompt: "Create a study plan based on my course materials" },
    { icon: "edit_note", label: "Generate flashcards", prompt: "Generate flashcards for the key concepts in my materials" },
  ];

  return (
    <>
      {/* Chat Canvas */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 md:p-12 space-y-8 scroll-smooth pb-40">
        {messages.length === 0 && !isLoading ? (
          <EmptyState />
        ) : (
          <>
            {messages.map((msg) =>
              msg.role === "user" ? (
                <UserBubble key={msg.id} msg={msg} />
              ) : (
                <AssistantBubble key={msg.id} msg={msg} />
              )
            )}
            {isLoading && <ThinkingIndicator />}
          </>
        )}

        {/* Error toast */}
        {error && (
          <div className="flex justify-center animate-[fadeSlideUp_0.3s_ease]">
            <div className="bg-error-container text-on-error-container px-5 py-3 rounded-2xl text-sm font-medium flex items-center gap-3 shadow-lg max-w-lg">
              <span className="material-symbols-outlined text-lg">error</span>
              <div>
                <p className="font-semibold">Failed to get a response</p>
                <p className="text-xs opacity-80 mt-0.5">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="ml-auto material-symbols-outlined text-sm hover:opacity-70"
              >
                close
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Message Input Area */}
      <div className="absolute bottom-0 w-full p-8 md:p-12 pt-0 bg-gradient-to-t from-surface via-surface to-transparent pointer-events-none">
        <div className="max-w-4xl mx-auto pointer-events-auto">
          <div className="bg-surface-container-lowest rounded-3xl p-2 shadow-[0_12px_40px_rgba(42,52,57,0.06)] flex items-end gap-2 border border-outline-variant/10">
            <button className="p-3 text-on-surface-variant hover:text-primary transition-colors rounded-2xl hover:bg-surface-container-low">
              <span className="material-symbols-outlined">attach_file</span>
            </button>
            <textarea
              ref={textareaRef}
              className="flex-1 bg-transparent border-none focus:ring-0 py-3 text-on-surface placeholder:text-outline-variant font-body resize-none outline-none"
              placeholder="Ask Study Copilot anything..."
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
            />
            <button
              onClick={() => handleSubmit()}
              disabled={isLoading || !input.trim()}
              className="bg-primary p-3 rounded-2xl text-white shadow-lg shadow-primary/20 hover:scale-105 active:scale-95 transition-all disabled:opacity-40 disabled:hover:scale-100"
            >
              <span className="material-symbols-outlined">
                {isLoading ? "hourglass_top" : "send"}
              </span>
            </button>
          </div>

          <div className="flex justify-center gap-6 mt-4">
            {quickActions.map((action) => (
              <button
                key={action.label}
                onClick={() => handleSubmit(action.prompt)}
                disabled={isLoading}
                className="text-[11px] font-semibold text-on-surface-variant/60 hover:text-primary transition-colors flex items-center gap-1 disabled:opacity-40"
              >
                <span className="material-symbols-outlined text-[14px]">{action.icon}</span>
                {action.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
