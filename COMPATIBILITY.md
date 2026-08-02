# Compatibility

| 环境 | 状态 | 说明 |
|---|---|---|
| Codex Desktop | 支持 | 使用插件 Marketplace 和 Skills UI 元数据 |
| Codex CLI | 支持 | 在新任务中加载已安装插件 |
| Windows PowerShell | 支持 | 提供 `.ps1` HITL 模板；验证脚本使用 UTF-8 |
| macOS / Linux | 支持 | 提供 Bash HITL 模板 |
| GitHub connector | 推荐 | 优先用于 GitHub 读写 |
| `gh` CLI | 可选降级 | 必须安装并完成认证 |
| GitLab connector | 推荐 | 可用时优先使用 |
| `glab` CLI | 可选降级 | 必须安装并完成认证 |

插件不声明强制 MCP 依赖：大多数 Skills 可在本地仓库独立工作，需要 tracker 或网页能力时才进行 capability detection。
