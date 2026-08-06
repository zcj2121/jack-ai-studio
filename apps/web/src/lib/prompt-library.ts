export interface PromptTemplateVariable {
  id: string;
  label: string;
  placeholder: string;
}

export interface PromptTemplate {
  id: string;
  title: string;
  description: string;
  content: string;
  variables: readonly PromptTemplateVariable[];
}

export type PromptVariableValues = Record<string, string>;

export const PROMPT_TEMPLATES: readonly PromptTemplate[] = [
  {
    id: "explain-concept",
    title: "概念讲解",
    description: "专业解释、前端类比与短例子",
    content:
      "请使用中文解释 {{topic}}。\n\n" +
      "要求：\n" +
      "1. 先给出准确的专业解释。\n" +
      "2. 再结合 Vue、TypeScript 或企业后台经验做类比。\n" +
      "3. 提供一个可以验证的短例子。\n" +
      "4. 说明它在 Jack AI Studio 中的作用。",
    variables: [
      {
        id: "topic",
        label: "TOPIC",
        placeholder: "例如：React Server Component",
      },
    ],
  },
  {
    id: "compare-options",
    title: "方案对比",
    description: "比较差异、取舍与适用场景",
    content:
      "请比较 {{options}}。\n\n" +
      "要求：\n" +
      "1. 先说明它们解决的共同问题。\n" +
      "2. 使用表格对比核心差异。\n" +
      "3. 给出各自适用场景和主要风险。\n" +
      "4. 结合 Jack AI Studio 给出当前阶段的选择建议。",
    variables: [
      {
        id: "options",
        label: "OPTIONS",
        placeholder: "例如：SSE 与 WebSocket",
      },
    ],
  },
  {
    id: "debug-problem",
    title: "问题排查",
    description: "按概率分析根因与验证步骤",
    content:
      "请帮助我排查这个问题：{{symptom}}\n\n" +
      "要求：\n" +
      "1. 不要直接猜测，先列出需要确认的证据。\n" +
      "2. 按概率从高到低给出可能原因。\n" +
      "3. 每个原因都给出最小验证步骤。\n" +
      "4. 最后再给出修复建议和回归检查。",
    variables: [
      {
        id: "symptom",
        label: "SYMPTOM",
        placeholder: "例如：移动端代码块撑宽页面",
      },
    ],
  },
];

export function renderPromptTemplate(
  template: PromptTemplate,
  values: PromptVariableValues,
): string {
  return template.variables.reduce((content, variable) => {
    return content.replaceAll(
      `{{${variable.id}}}`,
      values[variable.id]?.trim() ?? "",
    );
  }, template.content);
}
