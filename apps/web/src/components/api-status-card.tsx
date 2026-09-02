import type { ApiHealth } from "@/lib/api";

interface ApiStatusCardProps {
  health: ApiHealth;
}

export function ApiStatusCard({ health }: ApiStatusCardProps) {
  const isOnline = health.state === "online";

  return (
    <section
      aria-labelledby="api-status-title"
      className="grid gap-5 border border-white/15 bg-white/[0.025] p-4 sm:grid-cols-[auto_1fr_auto] sm:items-center sm:p-6"
    >
      <div
        className={`grid size-12 place-items-center border font-mono text-[10px] font-bold tracking-[0.12em] ${
          isOnline
            ? "border-[var(--signal)] text-[var(--signal)]"
            : "border-amber-300/70 text-amber-300"
        }`}
      >
        API
      </div>

      <div>
        <p
          id="api-status-title"
          className="font-mono text-[10px] tracking-[0.18em] text-white/38"
        >
          FASTAPI CONNECTION / DAY 09
        </p>
        <p className="mt-2 text-sm text-white/65">
          {isOnline ? health.data.name : health.message}
        </p>
      </div>

      <div className="flex items-center gap-3 sm:justify-self-end">
        <span
          aria-hidden="true"
          className={`size-2 rounded-full ${
            isOnline
              ? "animate-pulse bg-[var(--signal)]"
              : "bg-amber-300"
          }`}
        />
        <span className="font-mono text-[10px] tracking-[0.18em] text-white/55">
          {isOnline
            ? `ONLINE · PYTHON ${health.data.python_version}`
            : "OFFLINE · RETRY ON REFRESH"}
        </span>
      </div>
    </section>
  );
}
