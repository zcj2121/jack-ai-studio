"use client";

import { type FormEvent, useRef, useState } from "react";

import {
  ChatApiError,
  type ChatMessage,
  streamChatCompletion,
} from "@/lib/chat-api";

const MAX_PROMPT_LENGTH = 2_000;

interface WorkspaceMessage extends ChatMessage {
  id: number;
}

export function ChatWorkspace() {
  const nextMessageId = useRef(1);
  const [model, setModel] = useState("");
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState<WorkspaceMessage[]>([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [streamingMessageId, setStreamingMessageId] = useState<number | null>(
    null,
  );

  const normalizedModel = model.trim();
  const normalizedPrompt = prompt.trim();
  const canSubmit =
    normalizedModel.length > 0 &&
    normalizedPrompt.length > 0 &&
    !isSubmitting;

  function createWorkspaceMessage(message: ChatMessage): WorkspaceMessage {
    const workspaceMessage = {
      ...message,
      id: nextMessageId.current,
    };

    nextMessageId.current += 1;

    return workspaceMessage;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!canSubmit) {
      return;
    }

    const userMessage = createWorkspaceMessage({
      role: "user",
      content: normalizedPrompt,
    });
    const requestMessages: ChatMessage[] = [
      {
        role: userMessage.role,
        content: userMessage.content,
      },
    ];
    const assistantMessage = createWorkspaceMessage({
      role: "assistant",
      content: "",
    });

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
      assistantMessage,
    ]);
    setPrompt("");
    setErrorMessage("");
    setIsSubmitting(true);
    setStreamingMessageId(assistantMessage.id);

    try {
      await streamChatCompletion(
        {
          model: normalizedModel,
          messages: requestMessages,
          temperature: 0.7,
        },
        (content) => {
          setMessages((currentMessages) =>
            currentMessages.map((message) =>
              message.id === assistantMessage.id
                ? {
                    ...message,
                    content: message.content + content,
                  }
                : message,
            ),
          );
        },
      );
    } catch (error) {
      setMessages((currentMessages) =>
        currentMessages.filter(
          (message) =>
            message.id !== assistantMessage.id ||
            message.content.length > 0,
        ),
      );
      setErrorMessage(
        error instanceof ChatApiError
          ? error.message
          : "发送消息时发生未知错误，请稍后重试。",
      );
    } finally {
      setIsSubmitting(false);
      setStreamingMessageId(null);
    }
  }

  function handleClearSession() {
    setMessages([]);
    setErrorMessage("");
  }

  return (
    <div className="relative flex min-h-[560px] flex-col border border-white/15 bg-white/[0.025]">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 px-5 py-4 font-mono text-[10px] tracking-[0.16em] text-white/38">
        <span>POST /CHAT/STREAM · SSE</span>
        <span className="flex items-center gap-2 text-[var(--signal)]">
          <span className="size-1.5 rounded-full bg-[var(--signal)]" />
          STREAM READY
        </span>
      </div>

      <div
        aria-live="polite"
        className="flex min-h-80 flex-1 flex-col gap-5 overflow-y-auto px-5 py-7 sm:px-8"
      >
        {messages.length === 0 ? (
          <div className="my-auto max-w-2xl py-10">
            <p className="font-mono text-xs tracking-[0.2em] text-[var(--signal)]">
              STREAM / RESPONSE
            </p>
            <h1 className="mt-5 text-[clamp(2.7rem,6vw,6rem)] font-semibold leading-[0.88] tracking-[-0.065em]">
              Watch the answer
              <span className="block font-mono text-[0.62em] font-normal tracking-[-0.04em] text-white/30">
                arrive in motion.
              </span>
            </h1>
            <p className="mt-7 max-w-xl text-sm leading-7 text-white/50 sm:text-base">
              输入 Provider 支持的 Model ID 和 Prompt。Assistant Message
              会随着 SSE Delta 到达逐段增长，API Key 始终留在 FastAPI 服务端。
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <article
              key={message.id}
              className={`max-w-3xl border-l px-4 py-3 ${
                message.role === "user"
                  ? "ml-auto border-white/25 bg-white/[0.035]"
                  : "border-[var(--signal)] bg-black/15"
              }`}
            >
              <p className="font-mono text-[10px] tracking-[0.16em] text-white/35">
                {message.role === "user" ? "YOU" : "ASSISTANT"}
              </p>
              <p className="mt-2 whitespace-pre-wrap text-sm leading-7 text-white/70 sm:text-base">
                {message.content}
                {message.id === streamingMessageId ? (
                  <span
                    aria-label="正在接收流式回答"
                    className="ml-1 inline-block h-4 w-1.5 animate-pulse bg-[var(--signal)] align-middle"
                  />
                ) : null}
              </p>
            </article>
          ))
        )}

        {isSubmitting ? (
          <div className="flex items-center gap-3 font-mono text-[10px] tracking-[0.16em] text-white/40">
            <span className="size-2 animate-pulse rounded-full bg-[var(--signal)]" />
            RECEIVING SSE DELTA
          </div>
        ) : null}

        {errorMessage ? (
          <div
            role="alert"
            className="border-l border-amber-300 bg-amber-300/5 px-4 py-3 text-sm leading-6 text-amber-100/75"
          >
            {errorMessage}
          </div>
        ) : null}
      </div>

      <form
        onSubmit={handleSubmit}
        className="border-t border-white/10 p-4 sm:p-5"
      >
        <div className="grid gap-3 sm:grid-cols-[minmax(180px,0.32fr)_1fr]">
          <div>
            <label
              htmlFor="chat-model"
              className="font-mono text-[10px] tracking-[0.16em] text-white/45"
            >
              MODEL ID
            </label>
            <input
              id="chat-model"
              value={model}
              onChange={(event) => setModel(event.target.value)}
              disabled={isSubmitting}
              placeholder="provider-model-id"
              autoComplete="off"
              className="mt-2 h-12 w-full border border-white/15 bg-black/20 px-3 font-mono text-xs text-white outline-none transition-colors placeholder:text-white/20 focus:border-[var(--signal)] disabled:opacity-40"
            />
          </div>

          <div>
            <label
              htmlFor="chat-prompt"
              className="font-mono text-[10px] tracking-[0.16em] text-white/45"
            >
              PROMPT
            </label>
            <textarea
              id="chat-prompt"
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              disabled={isSubmitting}
              maxLength={MAX_PROMPT_LENGTH}
              rows={3}
              placeholder="输入一条消息，观察 Assistant 回答逐段出现。"
              className="mt-2 w-full resize-y border border-white/15 bg-black/20 p-3 text-sm leading-6 text-white outline-none transition-colors placeholder:text-white/20 focus:border-[var(--signal)] disabled:opacity-40"
            />
          </div>
        </div>

        <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
          <span className="font-mono text-[10px] tracking-[0.14em] text-white/30">
            {prompt.length} / {MAX_PROMPT_LENGTH} · NO PERSISTED CONTEXT
          </span>

          <div className="flex gap-2">
            <button
              type="button"
              onClick={handleClearSession}
              disabled={messages.length === 0 || isSubmitting}
              className="border border-white/20 px-4 py-2 font-mono text-[10px] tracking-[0.16em] text-white/55 transition-colors hover:border-white/50 hover:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--signal)] disabled:cursor-not-allowed disabled:opacity-30"
            >
              清空会话
            </button>
            <button
              type="submit"
              disabled={!canSubmit}
              className="border border-[var(--signal)] bg-[var(--signal)] px-5 py-2 font-mono text-[10px] font-bold tracking-[0.16em] text-[var(--ink)] transition-opacity hover:opacity-85 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--signal)] disabled:cursor-not-allowed disabled:opacity-30"
            >
              {isSubmitting ? "生成中" : "流式发送"}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
