# Codex Plugin Guidance

This directory is a distributable Codex plugin. Keep the outer folder name and `.codex-plugin/plugin.json` name equal to `mattpocock-skills-zh-cn`.

- Stable plugin skills live directly under `skills/<skill-name>/`.
- Every skill must contain `SKILL.md` and `agents/openai.yaml`.
- Keep Claude-only, deprecated, personal, and in-progress skills out of this package.
- For user-invoked skills, use `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; keep Codex `SKILL.md` frontmatter limited to `name` and `description`.
- Validate the plugin and every skill before packaging.
- Preserve the upstream and localization attribution in `README.md` and `LICENSE`.
