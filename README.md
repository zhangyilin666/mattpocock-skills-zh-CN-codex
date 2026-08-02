# Matt Pocock Skills 中文版 · Codex 插件

面向 OpenAI Codex 的简体中文软件工程工作流插件。包含 25 个 Skills，覆盖需求澄清、规格与任务拆分、TDD、缺陷诊断、代码审查、架构设计、领域建模、研究和交接。

本仓库是独立维护的 Codex 适配版：来源为 Matt Pocock 的原始 Skills 和 vinvcn 的中文本地化版本，并加入 Codex 插件清单、UI 元数据、调用策略、安全边界、跨平台脚本、行为评测和自动化验证。

## 安装

克隆仓库后，把仓库根目录注册为本地 Marketplace：

```powershell
git clone https://github.com/zhangyilin666/mattpocock-skills-zh-CN-codex.git
cd mattpocock-skills-zh-CN-codex
codex plugin marketplace add .
codex plugin add mattpocock-skills-zh-cn@mattpocock-zh-cn
```

安装或更新后，请在新的 Codex 任务中测试。第一次在某个代码仓库使用时，建议显式运行：

```text
$setup-matt-pocock-skills
```

如果只需要一个独立 Skill，可把 `plugins/mattpocock-skills-zh-cn/skills/<name>/` 复制到 Codex 的 Skills 目录。

## 包含的 Skills

- 规划与澄清：`ask-matt`、`grilling`、`grill-me`、`grill-with-docs`、`wayfinder`
- 规格与交付：`to-spec`、`to-tickets`、`implement`、`handoff`、`triage`
- 代码质量：`tdd`、`diagnosing-bugs`、`code-review`、`resolving-merge-conflicts`
- 架构与建模：`codebase-design`、`improve-codebase-architecture`、`domain-modeling`、`prototype`
- 专项工作：`research`、`teach`、`writing-great-skills`、`setup-pre-commit`、`scaffold-exercises`、`migrate-to-shoehorn`
- 仓库配置：`setup-matt-pocock-skills`

其中 13 个高意图或高副作用 Skills 默认只接受 `$skill-name` 显式调用，避免误触发。

## 安全设计

- Issue、PR、网页、日志和仓库内容均按不可信数据处理，不能覆盖用户指令或授权工具调用。
- 外部 comment、label、close、assignment 等写操作在执行前显示目标和变更范围。
- 合并冲突只暂存本次解决的文件，不使用无范围判断的 `git add -A`。
- GitHub/GitLab 优先使用已连接工具，CLI 仅在已安装且认证后作为降级路径。

详细策略见 [SECURITY.md](SECURITY.md)。

## 开发与验证

本仓库的验证脚本只依赖 Python 标准库：

```powershell
python -X utf8 scripts/validate.py
python -X utf8 scripts/package_plugin.py
```

验证内容包括插件与 Marketplace 结构、25 个 Skill 元数据、默认 Prompt、相对链接、过期 Claude 语法、长参考文档目录、安全规则、跨平台脚本和 activation eval 覆盖率。GitHub Actions 会在 push 和 pull request 上执行相同检查。

行为评测样例位于 `evals/activation-cases.jsonl`，覆盖正向触发、负向触发、相似 Skill 边界和危险输入。结构校验不能代替真实模型评测；发布前仍应在 Codex Desktop 与 CLI 上进行 forward test。

## 版本与来源

- Codex 适配版：`1.0.1`
- 中文来源：[`vinvcn/mattpocock-skills-zh-CN`](https://github.com/vinvcn/mattpocock-skills-zh-CN)，commit `f2b24646b1ea47f093d26c79a94aaf522007da49`
- 原始项目：[`mattpocock/skills`](https://github.com/mattpocock/skills)
- 适配维护：[`zhangyilin666`](https://github.com/zhangyilin666)

项目沿用 MIT License。中文翻译与 Codex 适配均为非官方社区版本。
