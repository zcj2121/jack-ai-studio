"use client";

import { type ChangeEvent, type FormEvent, useState } from "react";

const MAX_PROMPT_LENGTH = 280;

export function PromptComposer() {
  const [prompt, setPrompt] = useState("");
  const [submittedPrompt, setSubmittedPrompt] = useState("");

  const normalizedPrompt = prompt.trim();
  const canSubmit = normalizedPrompt.length > 0;

  function handlePromptChange(event: ChangeEvent<HTMLTextAreaElement>) {
    setPrompt(event.target.value);
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!canSubmit) {
      return;
    }

    setSubmittedPrompt(normalizedPrompt);
    setPrompt("");
  }

  function handleClear() {
    setPrompt("");
  }

  return (
    <section
      aria-labelledby="prompt-composer-title"
      className="border border-white/15 bg-white/[0.025] p-4 sm:p-6"
    >
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="font-mono text-[10px] tracking-[0.2em] text-[var(--signal)]">
            DAY 04 / INTERACTION LAB
          </p>
          <h2
            id="prompt-composer-title"
            className="mt-2 text-xl font-semibold tracking-[-0.03em] sm:text-2xl"
          >
            Prompt Composer
          </h2>
        </div>
        <p className="max-w-md text-sm leading-6 text-white/45">
          本地交互练习：输入内容只保存在当前页面，不会调用模型或 API。
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <label
          htmlFor="prompt"
          className="font-mono text-[10px] tracking-[0.16em] text-white/55"
        >
          YOUR PROMPT
        </label>
        <textarea
          id="prompt"
          name="prompt"
          value={prompt}
          maxLength={MAX_PROMPT_LENGTH}
          onChange={handlePromptChange}
          placeholder="例如：用 Vue 的响应式原理类比 React State。"
          className="mt-3 min-h-32 w-full resize-y border border-white/15 bg-black/20 p-4 text-sm leading-6 text-white outline-none transition-colors placeholder:text-white/25 focus:border-[var(--signal)] sm:text-base"
        />

        <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
          <span
            aria-live="polite"
            className="font-mono text-[10px] tracking-[0.14em] text-white/38"
          >
            {prompt.length} / {MAX_PROMPT_LENGTH} CHARACTERS
          </span>

          <div className="flex gap-2">
            <button
              type="button"
              onClick={handleClear}
              disabled={prompt.length === 0}
              className="border border-white/20 px-4 py-2 font-mono text-[10px] tracking-[0.16em] text-white/55 transition-colors hover:border-white/50 hover:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--signal)] disabled:cursor-not-allowed disabled:opacity-30"
            >
              清空
            </button>
            <button
              type="submit"
              disabled={!canSubmit}
              className="border border-[var(--signal)] bg-[var(--signal)] px-4 py-2 font-mono text-[10px] font-bold tracking-[0.16em] text-[var(--ink)] transition-opacity hover:opacity-85 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--signal)] disabled:cursor-not-allowed disabled:opacity-30"
            >
              本地提交
            </button>
          </div>
        </div>
      </form>

      <div
        aria-live="polite"
        className="mt-5 min-h-20 border-l border-[var(--signal)] bg-black/15 px-4 py-3"
      >
        <p className="font-mono text-[10px] tracking-[0.16em] text-white/35">
          SUBMIT PREVIEW
        </p>
        <p className="mt-2 text-sm leading-6 text-white/60">
          {submittedPrompt || "提交后，最后一条 Prompt 会显示在这里。"}
        </p>
      </div>
    </section>
  );
}
