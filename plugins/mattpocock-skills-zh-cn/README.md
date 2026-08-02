# Matt Pocock 工程 Skills 中文版（Codex 插件）

这是 `mattpocock/skills` 简体中文本地化版本的 Codex 原生插件适配包。Codex 适配版本为 `1.0.1`，基于 `vinvcn/mattpocock-skills-zh-CN@f2b2464`，保留 25 个稳定、可发布的 Skills，并补齐 `.codex-plugin/plugin.json`、`agents/openai.yaml`、调用策略与安全边界。

## 适配范围

- 使用 Codex 原生 `.codex-plugin/plugin.json`。
- 每个 skill 都包含 `SKILL.md` 和 `agents/openai.yaml`。
- User-invoked skills 同时声明 Codex 的 `policy.allow_implicit_invocation: false`。
- Claude 风格的 `Agent tool` / `subagent_type` 指令已改为跨 harness 的 sub-agent 表述。
- 所有显式调用使用 Codex `$skill-name` 语法，并提供 UI `default_prompt`。
- 外部 issue、PR、网页、日志和仓库内容按不可信数据处理。
- 同时提供 Bash 与 Windows PowerShell 的 HITL 诊断模板。
- 排除 `deprecated/`、`in-progress/`、`personal/`，以及仅适用于 Claude Code hooks 的 `git-guardrails-claude-code`。
- 保留原始 MIT License 与非官方中文译本。

## 在 Codex 中使用

本目录本身就是一个 Codex plugin root。将它放入已配置的本地 marketplace，或由 Codex 的 plugin creator / marketplace 工作流注册。Codex 插件 manifest 位于：

```text
.codex-plugin/plugin.json
```

如果只想把单个 workflow 当作 standalone skill 使用，也可以把对应的 `skills/<name>/` 目录复制或链接到：

```text
$HOME/.agents/skills/<name>/
```

安装或更新插件后，请在新任务中测试。首次在代码仓库使用工程 skills 时，显式运行：

```text
$setup-matt-pocock-skills
```

## 收录内容

插件包含需求澄清、规划、TDD、缺陷诊断、代码审查、架构设计、领域建模、研究、交接和教学等 25 个稳定 skills。可以先调用 `$ask-matt`，让它根据当前任务推荐工作流。

## 来源与许可

- 原始项目：https://github.com/mattpocock/skills
- 简体中文本地化：https://github.com/vinvcn/mattpocock-skills-zh-CN
- Codex 适配维护：https://github.com/zhangyilin666/mattpocock-skills-zh-CN-codex
- 中文源版本：`f2b24646b1ea47f093d26c79a94aaf522007da49`
- License：MIT，见 `LICENSE`
