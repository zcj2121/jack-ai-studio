import Link from "next/link";

import { ChatWorkspace } from "@/components/chat-workspace";

const workspaceNotes = [
  "Tool Calling 由服务端固定单轮编排",
  "Text / Structured JSON 可切换",
  "Prompt Library 提供本地可复用模板",
  "Provider Catalog 只返回安全元数据",
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
            AI CHAT V1 · DAY 28
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

            <ul className="mt-6 grid gap-3">
              {workspaceNotes.map((note, index) => (
                <li
                  key={note}
                  className="grid grid-cols-[auto_1fr] gap-3 border-t border-white/10 pt-3 text-xs leading-5 text-white/42"
                >
                  <span className="font-mono text-[10px] text-[var(--signal)]">
                    0{index + 1}
                  </span>
                  {note}
                </li>
              ))}
            </ul>
          </aside>

          <ChatWorkspace />
        </section>

        <footer className="flex flex-wrap items-center justify-between gap-3 border-t border-white/15 pt-5 font-mono text-[10px] tracking-[0.16em] text-white/35">
          <span>OUTPUT CONTRACT / PROVIDER / TOOLS / SSE</span>
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
