import ReactMarkdown from "react-markdown";

interface MarkdownMessageProps {
  content: string;
  isStreaming?: boolean;
}

export function MarkdownMessage({
  content,
  isStreaming = false,
}: MarkdownMessageProps) {
  return (
    <div className="prose prose-invert max-w-none text-sm leading-7 text-white/70 sm:text-base">
      <ReactMarkdown
        components={{
          h1: ({ children }) => (
            <h3 className="mb-3 mt-0 text-xl font-semibold tracking-tight text-white">
              {children}
            </h3>
          ),
          h2: ({ children }) => (
            <h4 className="mb-2 mt-5 text-lg font-semibold text-white">
              {children}
            </h4>
          ),
          h3: ({ children }) => (
            <h5 className="mb-2 mt-4 text-base font-semibold text-white">
              {children}
            </h5>
          ),
          p: ({ children }) => <p className="my-3 first:mt-0 last:mb-0">{children}</p>,
          ul: ({ children }) => (
            <ul className="my-3 list-disc space-y-1 pl-5">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="my-3 list-decimal space-y-1 pl-5">{children}</ol>
          ),
          blockquote: ({ children }) => (
            <blockquote className="my-3 border-l-2 border-[var(--signal)] pl-4 text-white/55">
              {children}
            </blockquote>
          ),
          code: ({ className, children }) => (
            <code
              className={
                className
                  ? "block overflow-x-auto rounded-none border border-white/10 bg-black/35 p-3 font-mono text-xs leading-6 text-[var(--signal)]"
                  : "rounded border border-white/10 bg-black/25 px-1.5 py-0.5 font-mono text-[0.9em] text-[var(--signal)]"
              }
            >
              {children}
            </code>
          ),
          pre: ({ children }) => (
            <pre className="my-4 overflow-x-auto border border-white/10 bg-black/35 p-0">
              {children}
            </pre>
          ),
          a: ({ children, href }) => (
            <a
              href={href}
              target="_blank"
              rel="noreferrer"
              className="text-[var(--signal)] underline decoration-[var(--signal)]/40 underline-offset-4 hover:decoration-[var(--signal)]"
            >
              {children}
            </a>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
      {isStreaming ? (
        <span
          aria-label="正在接收流式回答"
          className="ml-1 inline-block h-4 w-1.5 animate-pulse bg-[var(--signal)] align-middle"
        />
      ) : null}
    </div>
  );
}
