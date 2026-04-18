import { MaterialIcon } from "./MaterialIcon";

export function ThinkingIndicator({
  message = "Buscando documentos y generando respuesta…",
}: {
  message?: string;
}) {
  return (
    <div className="flex flex-col items-start animate-[fadeSlideUp_0.3s_ease]">
      <div className="flex items-start gap-4">
        <div className="mt-1 w-8 h-8 rounded-lg bg-primary-container flex items-center justify-center flex-shrink-0">
          <MaterialIcon name="auto_awesome" filled className="text-primary text-lg animate-pulse" />
        </div>
        <div className="bg-tertiary-container/40 backdrop-blur-sm p-6 rounded-3xl rounded-tl-none border border-white/50">
          <div className="flex items-center gap-3 text-on-surface-variant font-body text-sm">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:0ms]" />
              <span className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:150ms]" />
              <span className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:300ms]" />
            </div>
            {message}
          </div>
        </div>
      </div>
    </div>
  );
}
