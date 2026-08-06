"use client";

import { type FormEvent, useEffect, useRef, useState } from "react";

import { MarkdownMessage } from "@/components/markdown-message";
import { PromptLibrary } from "@/components/prompt-library";
import {
  ChatApiError,
  type ChatMessage,
  type ChatOutputMode,
  type ChatProviderId,
  type ChatProviderSummary,
  type ChatRequest,
  getChatProviders,
  streamChatCompletion,
} from "@/lib/chat-api";
import { streamMarkdownDemo } from "@/lib/markdown-demo";

const MAX_PROMPT_LENGTH = 2_000;

interface WorkspaceMessage extends ChatMessage {
  id: number;
  outputMode: ChatOutputMode;
}

type StreamRunner = (
  request: ChatRequest,
  onDelta: (content: string) => void,
) => Promise<void>;

export function ChatWorkspace() {
  const nextMessageId = useRef(1);
  const [providers, setProviders] = useState<ChatProviderSummary[]>([]);
  const [providerId, setProviderId] = useState<ChatProviderId | "">("");
  const [isProviderCatalogLoading, setIsProviderCatalogLoading] =
    useState(true);
  const [providerCatalogError, setProviderCatalogError] = useState("");
  const [model, setModel] = useState("");
  const [prompt, setPrompt] = useState("");
  const [outputMode, setOutputMode] = useState<ChatOutputMode>("text");
  const [messages, setMessages] = useState<WorkspaceMessage[]>([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [streamingMessageId, setStreamingMessageId] = useState<number | null>(
    null,
  );

  const normalizedModel = model.trim();
  const normalizedPrompt = prompt.trim();
  const selectedProvider = providers.find(
    (provider) => provider.id === providerId,
  );
  const providerStatus = isProviderCatalogLoading
    ? "LOADING SERVER STATUS"
    : providerCatalogError
      ? "SERVER STATUS UNAVAILABLE"
      : selectedProvider?.configured
        ? "SERVER CONFIGURED"
        : "SERVER CONFIG REQUIRED";
  const canSubmit =
    selectedProvider?.configured === true &&
    normalizedModel.length > 0 &&
    normalizedPrompt.length > 0 &&
    !isSubmitting;

  useEffect(() => {
    let isCancelled = false;

    async function loadProviders() {
      try {
        const providerCatalog = await getChatProviders();

        if (isCancelled) {
          return;
        }

        setProviders(providerCatalog);
        setProviderId(
          providerCatalog.find((provider) => provider.configured)?.id ??
            providerCatalog[0]?.id ??
            "",
        );
        setProviderCatalogError("");
      } catch (error) {
        if (isCancelled) {
          return;
        }

        setProviderCatalogError(
          error instanceof ChatApiError
            ? error.message
            : "Provider Catalog 加载失败，请稍后重试。",
        );
      } finally {
        if (!isCancelled) {
          setIsProviderCatalogLoading(false);
        }
      }
    }

    void loadProviders();

    return () => {
      isCancelled = true;
    };
  }, []);

  function createWorkspaceMessage(
    message: ChatMessage,
    messageOutputMode: ChatOutputMode,
  ): WorkspaceMessage {
    const workspaceMessage = {
      ...message,
      id: nextMessageId.current,
      outputMode: messageOutputMode,
    };

    nextMessageId.current += 1;

    return workspaceMessage;
  }

  async function runStream(
    displayPrompt: string,
    request: ChatRequest,
    streamRunner: StreamRunner,
  ) {
    const userMessage = createWorkspaceMessage(
      {
        role: "user",
        content: displayPrompt,
      },
      request.output_mode,
    );
    const assistantMessage = createWorkspaceMessage(
      {
        role: "assistant",
        content: "",
      },
      request.output_mode,
    );

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
      await streamRunner(
        request,
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
            (request.output_mode === "text" &&
              message.content.length > 0),
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

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!canSubmit || selectedProvider === undefined) {
      return;
    }

    await runStream(
      normalizedPrompt,
      {
        provider: selectedProvider.id,
        model: normalizedModel,
        messages: [
          {
            role: "user",
            content: normalizedPrompt,
          },
        ],
        temperature: 0.7,
        output_mode: outputMode,
      },
      streamChatCompletion,
    );
  }

  async function handleMarkdownDemo() {
    if (isSubmitting) {
      return;
    }

    await runStream(
      "请演示 Markdown 标题、列表和代码块。",
      {
        provider: "openai-compatible",
        model: "local-markdown-demo",
        messages: [
          {
            role: "user",
            content: "请演示 Markdown 标题、列表和代码块。",
          },
        ],
        temperature: 0.7,
        output_mode: "text",
      },
      streamMarkdownDemo,
    );
  }

  function handleClearSession() {
    setMessages([]);
    setErrorMessage("");
  }

  return (
    <div className="relative flex min-h-[560px] min-w-0 flex-col border border-white/15 bg-white/[0.025]">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 px-5 py-4 font-mono text-[10px] tracking-[0.16em] text-white/38">
        <span>POST /CHAT/STREAM · SSE</span>
        <span
          className={`flex items-center gap-2 ${
            providerCatalogError ? "text-amber-200" : "text-[var(--signal)]"
          }`}
        >
          <span
            className={`size-1.5 rounded-full ${
              providerCatalogError ? "bg-amber-200" : "bg-[var(--signal)]"
            }`}
          />
          {isProviderCatalogLoading
            ? "LOADING PROVIDERS"
            : providerCatalogError
              ? "CATALOG ERROR"
              : `${providers.filter((provider) => provider.configured).length} / ${providers.length} CONFIGURED`}
        </span>
      </div>

      <div
        aria-live="polite"
        className="flex min-h-80 min-w-0 flex-1 flex-col gap-5 overflow-y-auto px-5 py-7 sm:px-8"
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
              选择已配置的 Provider，输入对应的 Model ID 和 Prompt。Assistant
              Message 会随着 SSE Delta 到达逐段增长，API Key 始终留在 FastAPI
              服务端。
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <article
              key={message.id}
              className={`min-w-0 max-w-3xl border-l px-4 py-3 ${
                message.role === "user"
                  ? "ml-auto border-white/25 bg-white/[0.035]"
                  : "border-[var(--signal)] bg-black/15"
              }`}
            >
              <p className="font-mono text-[10px] tracking-[0.16em] text-white/35">
                {message.role === "user" ? "YOU" : "ASSISTANT"}
              </p>
              {message.role === "assistant" ? (
                message.outputMode === "structured_answer" ? (
                  <pre className="mt-2 overflow-x-auto whitespace-pre-wrap text-xs leading-6 text-white/75">
                    {message.content}
                  </pre>
                ) : (
                  <MarkdownMessage
                    content={message.content}
                    isStreaming={message.id === streamingMessageId}
                  />
                )
              ) : (
                <p className="mt-2 whitespace-pre-wrap text-sm leading-7 text-white/70 sm:text-base">
                  {message.content}
                </p>
              )}
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

        {providerCatalogError ? (
          <div
            role="alert"
            className="border-l border-amber-300 bg-amber-300/5 px-4 py-3 text-sm leading-6 text-amber-100/75"
          >
            {providerCatalogError}
          </div>
        ) : null}
      </div>

      <PromptLibrary disabled={isSubmitting} onApply={setPrompt} />

      <form
        onSubmit={handleSubmit}
        className="border-t border-white/10 p-4 sm:p-5"
      >
        <div className="grid gap-3 lg:grid-cols-[minmax(150px,0.2fr)_minmax(170px,0.24fr)_minmax(170px,0.24fr)_1fr]">
          <div>
            <label
              htmlFor="chat-output-mode"
              className="font-mono text-[10px] tracking-[0.16em] text-white/45"
            >
              OUTPUT MODE
            </label>
            <select
              id="chat-output-mode"
              value={outputMode}
              onChange={(event) =>
                setOutputMode(event.target.value as ChatOutputMode)
              }
              disabled={isSubmitting}
              className="mt-2 h-12 w-full border border-white/15 bg-[var(--ink)] px-3 font-mono text-xs text-white outline-none transition-colors focus:border-[var(--signal)] disabled:opacity-40"
            >
              <option value="text">Text / Markdown</option>
              <option value="structured_answer">Structured JSON</option>
            </select>
            <p className="mt-2 font-mono text-[9px] tracking-[0.12em] text-white/35">
              {outputMode === "structured_answer"
                ? "PYDANTIC SCHEMA"
                : "MARKDOWN TEXT"}
            </p>
          </div>

          <div>
            <label
              htmlFor="chat-provider"
              className="font-mono text-[10px] tracking-[0.16em] text-white/45"
            >
              PROVIDER
            </label>
            <select
              id="chat-provider"
              value={providerId}
              onChange={(event) =>
                setProviderId(event.target.value as ChatProviderId)
              }
              disabled={
                isProviderCatalogLoading ||
                providers.length === 0 ||
                isSubmitting
              }
              className="mt-2 h-12 w-full border border-white/15 bg-[var(--ink)] px-3 font-mono text-xs text-white outline-none transition-colors focus:border-[var(--signal)] disabled:opacity-40"
            >
              {isProviderCatalogLoading ? (
                <option value="">Loading...</option>
              ) : null}
              {providers.map((provider) => (
                <option key={provider.id} value={provider.id}>
                  {provider.label}
                </option>
              ))}
            </select>
            <p
              className={`mt-2 font-mono text-[9px] tracking-[0.12em] ${
                selectedProvider?.configured
                  ? "text-[var(--signal)]"
                  : "text-amber-200/70"
              }`}
            >
              {providerStatus}
            </p>
          </div>

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
            {prompt.length} / {MAX_PROMPT_LENGTH} · NO API KEY IN DEMO
          </span>

          <div className="flex gap-2">
            <button
              type="button"
              onClick={handleMarkdownDemo}
              disabled={isSubmitting}
              className="border border-[var(--signal)]/60 px-4 py-2 font-mono text-[10px] tracking-[0.16em] text-[var(--signal)] transition-colors hover:border-[var(--signal)] hover:bg-[var(--signal)]/10 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--signal)] disabled:cursor-not-allowed disabled:opacity-30"
            >
              Markdown 演示
            </button>
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
