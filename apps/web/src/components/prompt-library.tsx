"use client";

import { type FormEvent, useState } from "react";

import {
  PROMPT_TEMPLATES,
  type PromptVariableValues,
  renderPromptTemplate,
} from "@/lib/prompt-library";

interface PromptLibraryProps {
  disabled?: boolean;
  onApply: (prompt: string) => void;
}

export function PromptLibrary({
  disabled = false,
  onApply,
}: PromptLibraryProps) {
  const [selectedTemplateId, setSelectedTemplateId] = useState(
    PROMPT_TEMPLATES[0].id,
  );
  const [variableValues, setVariableValues] =
    useState<PromptVariableValues>({});
  const [appliedTemplateId, setAppliedTemplateId] = useState("");

  const selectedTemplate =
    PROMPT_TEMPLATES.find(
      (template) => template.id === selectedTemplateId,
    ) ?? PROMPT_TEMPLATES[0];
  const canApply =
    !disabled &&
    selectedTemplate.variables.every(
      (variable) => variableValues[variable.id]?.trim().length > 0,
    );

  function handleTemplateChange(templateId: string) {
    setSelectedTemplateId(templateId);
    setVariableValues({});
    setAppliedTemplateId("");
  }

  function handleVariableChange(variableId: string, value: string) {
    setVariableValues((currentValues) => ({
      ...currentValues,
      [variableId]: value,
    }));
    setAppliedTemplateId("");
  }

  function handleApply(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!canApply) {
      return;
    }

    onApply(renderPromptTemplate(selectedTemplate, variableValues));
    setAppliedTemplateId(selectedTemplate.id);
  }

  return (
    <section
      aria-labelledby="prompt-library-title"
      className="border-t border-white/10 bg-black/15 px-4 py-4 sm:px-5"
    >
      <div className="flex flex-wrap items-end justify-between gap-2">
        <div>
          <p
            id="prompt-library-title"
            className="font-mono text-[10px] tracking-[0.18em] text-[var(--signal)]"
          >
            PROMPT LIBRARY
          </p>
          <p className="mt-1 text-xs leading-5 text-white/40">
            {selectedTemplate.description}
          </p>
        </div>
        <span className="font-mono text-[9px] tracking-[0.14em] text-white/30">
          {PROMPT_TEMPLATES.length.toString().padStart(2, "0")} LOCAL
        </span>
      </div>

      <form
        onSubmit={handleApply}
        className="mt-3 grid gap-3 md:grid-cols-[minmax(170px,0.36fr)_minmax(220px,1fr)_auto] md:items-end"
      >
        <div className="min-w-0">
          <label
            htmlFor="prompt-template"
            className="font-mono text-[9px] tracking-[0.14em] text-white/38"
          >
            TEMPLATE
          </label>
          <select
            id="prompt-template"
            value={selectedTemplate.id}
            onChange={(event) => handleTemplateChange(event.target.value)}
            disabled={disabled}
            className="mt-2 h-10 w-full border border-white/15 bg-[var(--ink)] px-3 font-mono text-xs text-white outline-none transition-colors focus:border-[var(--signal)] disabled:opacity-40"
          >
            {PROMPT_TEMPLATES.map((template) => (
              <option key={template.id} value={template.id}>
                {template.title}
              </option>
            ))}
          </select>
        </div>

        {selectedTemplate.variables.map((variable) => (
          <div key={variable.id} className="min-w-0">
            <label
              htmlFor={`prompt-variable-${variable.id}`}
              className="font-mono text-[9px] tracking-[0.14em] text-white/38"
            >
              {variable.label}
            </label>
            <input
              id={`prompt-variable-${variable.id}`}
              value={variableValues[variable.id] ?? ""}
              onChange={(event) =>
                handleVariableChange(variable.id, event.target.value)
              }
              disabled={disabled}
              placeholder={variable.placeholder}
              autoComplete="off"
              className="mt-2 h-10 w-full border border-white/15 bg-black/20 px-3 text-xs text-white outline-none transition-colors placeholder:text-white/20 focus:border-[var(--signal)] disabled:opacity-40"
            />
          </div>
        ))}

        <button
          type="submit"
          disabled={!canApply}
          className="h-10 border border-[var(--signal)]/60 px-4 font-mono text-[10px] tracking-[0.14em] text-[var(--signal)] transition-colors hover:border-[var(--signal)] hover:bg-[var(--signal)]/10 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--signal)] disabled:cursor-not-allowed disabled:opacity-30"
        >
          应用模板
        </button>
      </form>

      <p
        aria-live="polite"
        className="mt-2 min-h-4 font-mono text-[9px] tracking-[0.12em] text-[var(--signal)]/70"
      >
        {appliedTemplateId === selectedTemplate.id
          ? "APPLIED TO PROMPT"
          : ""}
      </p>
    </section>
  );
}
