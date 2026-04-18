import type { CSSProperties } from "react";

export function MaterialIcon({
  name,
  filled,
  className = "",
  style,
}: {
  name: string;
  filled?: boolean;
  className?: string;
  style?: CSSProperties;
}) {
  const variationStyle = filled ? { fontVariationSettings: "'FILL' 1" as const } : undefined;
  return (
    <span className={`material-symbols-outlined ${className}`} style={{ ...variationStyle, ...style }}>
      {name}
    </span>
  );
}
