import { MaterialIcon } from "@/components/shared/MaterialIcon";

export default function HistoryView() {
  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-12 flex flex-col items-center justify-center">
      <div className="bg-primary-container/30 p-5 rounded-2xl mb-6">
        <MaterialIcon name="history" filled className="text-primary text-5xl" />
      </div>
      <h1 className="text-2xl font-headline font-black text-on-surface mb-2">
        Historial
      </h1>
      <p className="text-on-surface-variant font-body max-w-md text-center leading-relaxed">
        Próximamente podrás revisar tus conversaciones y sesiones de estudio anteriores.
      </p>
    </div>
  );
}
