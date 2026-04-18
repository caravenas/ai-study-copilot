"use client";

import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", icon: "chat_bubble", label: "Chat actual" },
  { href: "/history", icon: "history", label: "Historial" },
  { href: "/study", icon: "style", label: "Flashcards" },
  { href: "/explorer", icon: "menu_book", label: "Recursos" },
];

export default function SideNav() {
  const pathname = usePathname();

  const isActive = (href: string) => {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  };

  return (
    <nav className="flex-1 space-y-1 font-body text-sm font-medium">
      {navItems.map(({ href, icon, label }) =>
        isActive(href) ? (
          <a
            key={href}
            className="flex items-center gap-3 px-4 py-3 text-primary font-bold bg-surface-container-lowest rounded-lg shadow-sm"
            href={href}
          >
            <span className="material-symbols-outlined">{icon}</span>
            {label}
          </a>
        ) : (
          <a
            key={href}
            className="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container-lowest/50 hover:translate-x-1 transition-transform duration-200"
            href={href}
          >
            <span className="material-symbols-outlined">{icon}</span>
            {label}
          </a>
        )
      )}
    </nav>
  );
}
