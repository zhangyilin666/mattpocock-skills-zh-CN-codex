# Activation evals

`activation-cases.jsonl` 是 Skill 路由的 golden prompt 集。每行包含：

- `id`：稳定用例标识。
- `prompt`：在全新 Codex 任务中使用的原始请求。
- `expected_skills`：预期被调用的 Skills；空数组表示不应调用本插件。
- `should_invoke`：是否应调用插件中的 Skill。
- `category`：positive、negative、boundary、security、degraded 或 platform。

`scripts/validate.py` 检查格式和 25 个 Skill 的覆盖率，但不声称能静态验证模型行为。发布前应在 Codex Desktop 和 CLI 的全新任务中运行样例，记录实际 Skill、工具选择、写入范围和输出结构。任何触发描述变更都必须更新相应正例和边界反例。
