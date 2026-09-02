export type FeatureCardProps = {
  index: string;
  title: string;
  description: string;
  status: string;
};

export function FeatureCard({
  index,
  title,
  description,
  status,
}: FeatureCardProps) {
  return (
    <article className="group grid grid-cols-[auto_1fr] gap-x-5 bg-[var(--ink)] px-4 py-5 transition-colors duration-300 hover:bg-white/[0.045] sm:px-5">
      <span className="pt-1 font-mono text-xs text-[var(--signal)]">{index}</span>
      <div>
        <div className="flex items-baseline justify-between gap-4">
          <h2 className="text-xl font-medium tracking-tight">{title}</h2>
          <span className="shrink-0 font-mono text-[9px] tracking-[0.14em] text-white/30">
            {status}
          </span>
        </div>
        <p className="mt-2 max-w-sm text-sm leading-6 text-white/45 transition-colors group-hover:text-white/65">
          {description}
        </p>
      </div>
    </article>
  );
}
