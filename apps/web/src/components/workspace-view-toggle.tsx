"use client";

import { useState } from "react";

type WorkspaceView = "learning" | "product";

const viewContent: Record<WorkspaceView, string> = {
  learning: "当前视图：Day 29 Alembic Migration 已完成，下一步进入 Day 30。",
  product: "产品视图：AI Chat V1 支持多 Provider、流式对话、Structured Output 和固定单轮工具调用。",
};

export function WorkspaceViewToggle() {
  const [activeView, setActiveView] = useState<WorkspaceView>("learning");

  return (
    <div className="max-w-xl border-l border-[var(--signal)] pl-4">
      <div className="flex flex-wrap gap-2">
        {(["learning", "product"] as const).map((view) => {
          const isActive = activeView === view;

          return (
            <button
              key={view}
              type="button"
              aria-pressed={isActive}
              onClick={() => setActiveView(view)}
              className={`border px-4 py-2 font-mono text-[10px] tracking-[0.16em] transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--signal)] ${
                isActive
                  ? "border-[var(--signal)] bg-[var(--signal)] text-[var(--ink)]"
                  : "border-white/20 text-white/50 hover:border-white/50 hover:text-white"
              }`}
            >
              {view === "learning" ? "学习视图" : "产品视图"}
            </button>
          );
        })}
      </div>
      <p aria-live="polite" className="mt-4 text-sm leading-6 text-white/48">
        {viewContent[activeView]}
      </p>
    </div>
  );
}
