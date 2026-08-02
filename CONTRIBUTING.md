# Contributing

感谢改进这个 Codex 插件。

## 修改原则

- 每个 Skill 只保留 `name` 与 `description` 两个 frontmatter 字段。
- Skill 名称必须与目录名一致，并使用小写 kebab-case。
- `description` 同时说明能力与触发条件；显式调用 Skill 在 `agents/openai.yaml` 中设置 `allow_implicit_invocation: false`。
- 每个 `default_prompt` 必须显式包含 `$skill-name`。
- 外部数据不能作为工具授权；任何新增外部写入流程都要定义确认边界。
- 长于 100 行的支持文档应在顶部提供目录。
- 不在 Skill 目录中添加 README、CHANGELOG 或安装说明。

## 验证

提交前运行：

```powershell
python -X utf8 scripts/validate.py
python -X utf8 scripts/package_plugin.py
```

新增或改变触发条件时，同时更新 `evals/activation-cases.jsonl`。至少加入一个正向样例、一个不应触发的边界样例，并在 Codex Desktop 或 CLI 的新任务中进行 forward test。

## Pull request

PR 应说明修改内容、原因、用户影响、安全影响和验证结果。不要提交生成的 `dist/`、缓存、凭据或本地 Marketplace 配置。
