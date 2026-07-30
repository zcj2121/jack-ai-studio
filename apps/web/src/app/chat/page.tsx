import Link from "next/link";

const workspaceNotes = [
  "今天先建立 Message、Role 与 ChatRequest 数据契约",
  "Provider、API Key 和真实模型调用将在后续 Day 按顺序接入",
  "Schema 校验通过不代表模型已经生成回答",
];

export default function ChatPage() {
  return (
    <main className="min-h-screen bg-[var(--ink)] text-[var(--paper)]">
      <div className="mx-auto grid min-h-screen w-full max-w-[1440px] grid-rows-[auto_1fr_auto] px-5 py-5 sm:px-8 sm:py-7 lg:px-12">
        <header className="flex flex-wrap items-center justify-between gap-4 border-b border-white/15 pb-5">
          <Link
            href="/"
            aria-label="返回 Jack AI Studio 首页"
            className="flex items-center gap-3 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[var(--signal)]"
          >
            <span className="grid size-9 place-items-center border border-[var(--signal)] font-mono text-xs font-bold text-[var(--signal)]">
              JA
            </span>
            <div>
              <p className="font-mono text-[10px] tracking-[0.22em] text-white/45">
                JACK AI STUDIO
              </p>
              <p className="text-sm font-semibold tracking-wide">Chat Workspace</p>
            </div>
          </Link>

          <div className="flex items-center gap-2 font-mono text-[10px] tracking-[0.18em] text-white/50">
            <span className="size-2 rounded-full bg-amber-300" />
            MESSAGE CONTRACT · DAY 11
          </div>
        </header>

        <section className="grid gap-8 py-10 lg:grid-cols-[280px_1fr] lg:gap-0 lg:py-12">
          <aside className="border border-white/15 bg-white/[0.02] p-5 lg:border-r-0">
            <div className="flex items-center justify-between font-mono text-[10px] tracking-[0.16em] text-white/38">
              <span>CONVERSATIONS</span>
              <span>00</span>
            </div>

            <div className="mt-5 border border-dashed border-white/15 px-4 py-8 text-center">
              <p className="font-mono text-[10px] tracking-[0.14em] text-white/32">
                NO HISTORY YET
              </p>
              <p className="mt-3 text-xs leading-5 text-white/40">
                会话管理将在后续学习日实现。
              </p>
            </div>
          </aside>

          <div className="relative flex min-h-[560px] flex-col border border-white/15 bg-white/[0.025]">
            <div className="flex items-center justify-between border-b border-white/10 px-5 py-4 font-mono text-[10px] tracking-[0.16em] text-white/38">
              <span>CHAT REQUEST SCHEMA</span>
              <span>NO PROVIDER</span>
            </div>

            <div className="grid flex-1 place-items-center px-6 py-12">
              <div className="max-w-2xl">
                <p className="font-mono text-xs tracking-[0.2em] text-[var(--signal)]">
                  ROUTE / CHAT
                </p>
                <h1 className="mt-5 text-[clamp(2.8rem,7vw,6.5rem)] font-semibold leading-[0.9] tracking-[-0.065em]">
                  A quiet place
                  <span className="block font-mono text-[0.62em] font-normal tracking-[-0.04em] text-white/30">
                    the contract before the model.
                  </span>
                </h1>
                <p className="mt-7 max-w-xl text-sm leading-7 text-white/50 sm:text-base">
                  Chat 已经有明确的后端消息边界。今天只定义模型请求需要的数据，
                  不把 Schema 校验伪装成真实的 AI 回答。
                </p>

                <ul className="mt-8 grid gap-3">
                  {workspaceNotes.map((note, index) => (
                    <li
                      key={note}
                      className="grid grid-cols-[auto_1fr] gap-3 border-t border-white/10 pt-3 text-sm leading-6 text-white/45"
                    >
                      <span className="font-mono text-[10px] text-[var(--signal)]">
                        0{index + 1}
                      </span>
                      {note}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="border-t border-white/10 p-4">
              <div
                aria-label="Prompt 输入区域将在 Provider 接入后启用"
                className="flex min-h-14 items-center justify-between border border-white/10 bg-black/15 px-4 text-sm text-white/25"
              >
                <span>Prompt input unlocks after Provider integration.</span>
                <span className="font-mono text-[10px] tracking-[0.14em]">
                  DISABLED
                </span>
              </div>
            </div>
          </div>
        </section>

        <footer className="flex flex-wrap items-center justify-between gap-3 border-t border-white/15 pt-5 font-mono text-[10px] tracking-[0.16em] text-white/35">
          <span>MESSAGE / ROLE / PYDANTIC SCHEMA</span>
          <Link
            href="/"
            className="text-white/55 transition-colors hover:text-[var(--signal)] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[var(--signal)]"
          >
            ← BACK TO HOME
          </Link>
        </footer>
      </div>
    </main>
  );
}
