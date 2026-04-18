import "./globals.css";
import SideNav from "@/components/layout/SideNav";

export const metadata = {
  title: "Study Copilot | Modo de aprendizaje IA",
  description: "Asistente de estudio impulsado por IA",
};

const USER_INITIALS = "CA";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className="bg-surface text-on-surface min-h-screen flex flex-col font-body">

        {/* TopAppBar */}
        <header className="bg-surface-bright/80 backdrop-blur-xl sticky top-0 z-50 shadow-sm border-b border-outline-variant/20">
          <div className="flex justify-between items-center w-full px-8 py-4 max-w-screen-2xl mx-auto">
            <div className="flex items-center gap-8">
              <span className="text-xl font-bold text-on-surface font-headline">Study Copilot</span>
              <nav className="hidden md:flex items-center gap-6 font-headline text-sm font-medium tracking-tight">
                <a className="text-on-surface hover:text-primary transition-colors duration-200" href="/">Inicio</a>
                <a className="text-on-surface-variant hover:text-primary transition-colors duration-200" href="/admin">Admin</a>
              </nav>
            </div>

            <div className="flex items-center gap-4">
              <button className="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors">notifications</button>
              <button className="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors">settings</button>
              <div className="w-8 h-8 rounded-full overflow-hidden bg-surface-container-high border border-outline-variant/30 flex items-center justify-center text-primary font-bold text-xs uppercase">
                {USER_INITIALS}
              </div>
            </div>
          </div>
        </header>

        <div className="flex flex-1 overflow-hidden max-w-screen-2xl w-full mx-auto relative">

          {/* SideNavBar */}
          <aside className="bg-surface-container-low min-h-[calc(100vh-73px)] w-64 hidden lg:flex flex-col p-6 gap-2 sticky top-[73px]">
            <div className="mb-8">
              <div className="flex items-center gap-3 mb-2">
                <div className="bg-primary-container p-2 rounded-lg">
                  <span className="material-symbols-outlined text-primary" style={{fontVariationSettings: "'FILL' 1"}}>psychology</span>
                </div>
                <div>
                  <h2 className="text-lg font-black text-on-surface leading-tight font-headline">Asistente IA</h2>
                  <p className="text-[10px] uppercase tracking-widest text-on-surface-variant font-semibold font-label">Modo aprendizaje</p>
                </div>
              </div>
              <button className="w-full mt-4 py-2 px-4 bg-gradient-to-br from-primary to-primary-dim text-white rounded-xl text-sm font-semibold shadow-sm flex items-center justify-center gap-2 hover:opacity-90 transition-all font-body">
                <span className="material-symbols-outlined text-sm">add</span>
                Nueva sesión
              </button>
            </div>

            <SideNav />

            <div className="pt-6 border-t border-outline-variant/20 space-y-1 font-body">
              <a className="flex items-center gap-3 px-4 py-2 text-on-surface-variant text-sm hover:translate-x-1 transition-all" href="#">
                <span className="material-symbols-outlined">help</span> Ayuda
              </a>
              <a className="flex items-center gap-3 px-4 py-2 text-on-surface-variant text-sm hover:translate-x-1 transition-all" href="#">
                <span className="material-symbols-outlined">logout</span> Cerrar sesión
              </a>
            </div>
          </aside>

          {/* Main Content Area */}
          <main className="flex-1 flex flex-col bg-surface relative">
            {children}
          </main>

        </div>
      </body>
    </html>
  );
}
