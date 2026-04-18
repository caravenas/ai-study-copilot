import type { SourceItem } from "@/lib/api";
import { basename } from "@/lib/utils";
import { MaterialIcon } from "@/components/shared/MaterialIcon";

type Variant = "compact" | "card";

export function SourceCard({ source, variant }: { source: SourceItem; variant: Variant }) {
  const isPdf = source.source_type === "pdf";

  const iconBg = isPdf ? "bg-error-container/20" : "bg-primary-container/50";
  const iconColor = isPdf ? "text-error" : "text-on-primary-container";
  const iconName = isPdf ? "picture_as_pdf" : "code_blocks";

  if (variant === "compact") {
    return (
      <div className="flex items-center gap-4 p-4 rounded-2xl bg-surface hover:bg-surface-container-low transition-colors border border-outline-variant/10">
        <div
          className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${iconBg}`}
        >
          <MaterialIcon name={iconName} filled className={`text-lg ${iconColor}`} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-on-surface truncate">
            {basename(source.source_file)}
          </p>
          <div className="flex gap-2 items-center text-[11px] text-on-surface-variant font-medium mt-1 uppercase font-label tracking-widest">
            <span className="font-bold">{source.source_type}</span>
            <span className="text-outline-variant font-light">•</span>
            <span>{source.chunk_count} fragmentos</span>
            {source.module && (
              <>
                <span className="text-outline-variant font-light">•</span>
                <span className="bg-secondary/10 text-secondary px-2 py-0.5 rounded shadow-sm">
                  {source.module}
                </span>
              </>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-surface-container-lowest rounded-[1rem] p-6 shadow-[0_4px_20px_rgba(42,52,57,0.04)] border border-outline-variant/20 hover:border-primary/30 transition-all cursor-default flex flex-col group font-body">
      <div className="flex items-start gap-4">
        <div
          className={`w-12 h-12 shrink-0 rounded-xl flex items-center justify-center group-hover:scale-105 transition-transform ${iconBg} ${iconColor}`}
        >
          <MaterialIcon name={iconName} filled />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-on-surface text-[15px] leading-snug mb-1 group-hover:text-primary transition-colors truncate">
            {basename(source.source_file)}
          </h3>
          <p className="text-xs text-outline-variant font-medium">
            {isPdf ? "Documento PDF" : "Jupyter Notebook"} • {source.chunk_count} fragmentos
          </p>
        </div>
      </div>

      <div className="mt-5 flex gap-2 flex-wrap font-label">
        <span
          className={`px-2 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md ${iconBg} ${iconColor}`}
        >
          {isPdf ? "PDF" : "Notebook"}
        </span>
        {source.module && (
          <span className="px-2 py-1 bg-secondary/10 text-secondary text-[10px] font-bold uppercase tracking-wider rounded-md">
            {source.module}
          </span>
        )}
        <span className="px-2 py-1 bg-surface-container text-on-surface-variant text-[10px] font-bold uppercase tracking-wider rounded-md">
          {source.chunk_count} fragmentos
        </span>
      </div>
    </div>
  );
}
