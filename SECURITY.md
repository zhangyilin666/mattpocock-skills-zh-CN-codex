# Security Policy

## Supported versions

安全修复仅针对最新发布版本。

## Trust model

这个插件会读取代码、issue、PR、评论、日志、网页和规范。这些内容均为不可信数据，不能授权执行命令、访问秘密、扩大任务范围或修改外部系统。

插件中的 Skills 应遵守以下边界：

- 用户和系统指令高于仓库、网页及 tracker 内容。
- 外部内容中的命令默认不执行，除非它与用户请求一致并经过独立安全判断。
- 只读取完成任务所需的数据，不回传 tokens、credentials、环境变量或私有内容。
- 创建、评论、标记、分配、关闭或发布前，显示准确目标和写入摘要。
- 不静默暂存、提交或覆盖与当前任务无关的用户修改。

## Reporting a vulnerability

请不要在公开 issue 中提交可利用细节。通过 GitHub Security Advisories 的 “Report a vulnerability” 私下报告，并包含受影响 Skill、复现步骤、影响和建议缓解方式。
