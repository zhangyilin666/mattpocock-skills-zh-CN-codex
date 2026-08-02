# Changelog

本项目遵循 [Semantic Versioning](https://semver.org/)。

## 1.0.0 - 2026-08-02

### Added

- 25 个稳定工程 Skills 的 Codex 原生插件布局。
- 每个 Skill 的 `agents/openai.yaml` UI 元数据和 `$skill-name` 默认 Prompt。
- 仓库级 Codex Marketplace 清单。
- 外部内容信任边界与外部写入确认规则。
- Windows PowerShell HITL 诊断模板。
- Activation eval 数据集、无依赖验证器、可复现 ZIP 打包脚本和 GitHub Actions。

### Changed

- 将 Claude 风格 `/skill` 调用改为 Codex `$skill` 调用。
- 将 Claude 专属 invocation 配置改为 `policy.allow_implicit_invocation`。
- GitHub/GitLab 工作流改为连接器优先、认证 CLI 降级。
- 合并冲突流程仅暂存任务相关文件，并在提交前检查 staged diff。

### Removed

- Deprecated、in-progress、personal Skills。
- 依赖 Claude Code hooks 的 `git-guardrails-claude-code`。
