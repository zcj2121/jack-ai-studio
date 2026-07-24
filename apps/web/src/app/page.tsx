import Link from "next/link";

import { FeatureCard, type FeatureCardProps } from "@/components/feature-card";
import { PromptComposer } from "@/components/prompt-composer";
import { WorkspaceViewToggle } from "@/components/workspace-view-toggle";

const features: FeatureCardProps[] = [
  {
    index: "01",
    title: "AI Chat",
    description: "连接多个模型 Provider，管理会话、上下文与流式响应。",
    status: "Sprint 2",
  },
  {
    index: "02",
    title: "Knowledge",
    description: "上传文档，建立可检索、可引用的个人知识库。",
    status: "Sprint 4",
  },
  {
    index: "03",
    title: "Agent Center",
    description: "组合模型、工具与 Memory，查看每一步执行过程。",
    status: "Sprint 5",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-[var(--ink)] text-[var(--paper)]">
      <div className="mx-auto flex min-h-screen w-full max-w-[1440px] flex-col px-5 py-5 sm:px-8 sm:py-7 lg:px-12">
        <header className="flex items-center justify-between border-b border-white/15 pb-5">
          <div className="flex items-center gap-3">
            <span className="grid size-9 place-items-center border border-[var(--signal)] font-mono text-xs font-bold text-[var(--signal)]">
              JA
            </span>
            <div>
              <p className="font-mono text-[10px] tracking-[0.22em] text-white/45">
                DEVELOPER WORKSPACE
              </p>
              <p className="text-sm font-semibold tracking-wide">Jack AI Studio</p>
            </div>
          </div>

          <div className="flex items-center gap-2 font-mono text-[10px] tracking-[0.18em] text-white/55">
            <span className="size-2 animate-pulse rounded-full bg-[var(--signal)]" />
            DAY 05 · ONLINE
          </div>
        </header>

        <section className="grid flex-1 gap-10 py-14 lg:grid-cols-[1.15fr_0.85fr] lg:items-center lg:gap-20 lg:py-20">
          <div className="relative">
            <p className="mb-7 font-mono text-xs tracking-[0.24em] text-[var(--signal)]">
              BUILD / LEARN / SHIP
            </p>
            <h1 className="max-w-4xl text-[clamp(3.5rem,9vw,8.6rem)] font-semibold leading-[0.82] tracking-[-0.075em]">
              Your AI
              <span className="block font-mono text-[0.76em] font-normal tracking-[-0.06em] text-white/32">
                workspace.
              </span>
            </h1>
            <p className="mt-9 max-w-xl text-base leading-7 text-white/58 sm:text-lg sm:leading-8">
              一个边学习、边构建、边验证的开发者 AI 工作台。从第一行 React
              代码开始，逐步抵达可部署的完整产品。
            </p>

            <div className="mt-10">
              <WorkspaceViewToggle />
            </div>

            <Link
              href="/chat"
              className="mt-8 inline-flex items-center gap-3 border-b border-[var(--signal)] pb-2 font-mono text-xs tracking-[0.16em] text-[var(--signal)] transition-colors hover:text-white focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[var(--signal)]"
            >
              ENTER CHAT WORKSPACE
              <span aria-hidden="true">→</span>
            </Link>

            <span className="absolute -left-8 top-1/2 hidden h-px w-20 -rotate-90 bg-white/20 xl:block" />
          </div>

          <aside className="relative border border-white/15 bg-white/[0.025] p-4 sm:p-6">
            <div className="absolute -right-3 -top-3 size-6 border-r border-t border-[var(--signal)]" />
            <div className="absolute -bottom-3 -left-3 size-6 border-b border-l border-[var(--signal)]" />

            <div className="mb-4 flex items-center justify-between font-mono text-[10px] tracking-[0.18em] text-white/38">
              <span>MODULE ROADMAP</span>
              <span>05 / 90</span>
            </div>

            <div className="grid gap-px bg-white/10">
              {features.map((feature) => (
                <FeatureCard key={feature.index} {...feature} />
              ))}
            </div>
          </aside>
        </section>

        <div className="pb-14 lg:pb-20">
          <PromptComposer />
        </div>

        <footer className="grid gap-3 border-t border-white/15 pt-5 font-mono text-[10px] tracking-[0.16em] text-white/35 sm:grid-cols-3">
          <span>NEXT.JS / REACT / TYPESCRIPT</span>
          <span className="sm:text-center">SPRINT 01 · FOUNDATION</span>
          <span className="sm:text-right">90 DAY BUILD LOG → V1.0</span>
        </footer>
      </div>
    </main>
  );
}
