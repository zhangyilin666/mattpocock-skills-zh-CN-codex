#!/usr/bin/env python3
"""Validate the Codex marketplace and bundled Skills without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "mattpocock-skills-zh-cn"
SKILLS = PLUGIN / "skills"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
EVALS = ROOT / "evals" / "activation-cases.jsonl"

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON/UTF-8: {exc}")
        return {}


def parse_frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: cannot read as UTF-8: {exc}")
        return {}
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            errors.append(f"{path.relative_to(ROOT)}: malformed frontmatter line: {line}")
            continue
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def validate_manifest() -> None:
    manifest_path = PLUGIN / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        return
    check(manifest.get("name") == PLUGIN.name, "plugin name must match plugin directory")
    check(bool(re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", str(manifest.get("version", "")))), "plugin version must be strict semver")
    for field in ("description", "author", "repository", "license", "interface"):
        check(field in manifest, f"plugin manifest missing {field}")
    check(manifest.get("repository") == "https://github.com/zhangyilin666/mattpocock-skills-zh-CN-codex", "plugin repository must point to the Codex adaptation")
    interface = manifest.get("interface", {})
    check(isinstance(interface, dict), "plugin interface must be an object")
    if isinstance(interface, dict):
        prompts = interface.get("defaultPrompt", [])
        check(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "plugin must expose 1-3 default prompts")
        if isinstance(prompts, list):
            check(all(isinstance(item, str) and len(item) <= 128 for item in prompts), "plugin default prompts must be strings <=128 chars")


def validate_marketplace() -> None:
    data = load_json(MARKETPLACE)
    if not isinstance(data, dict):
        return
    check(data.get("name") == "mattpocock-zh-cn", "unexpected marketplace name")
    plugins = data.get("plugins", [])
    check(isinstance(plugins, list) and len(plugins) == 1, "marketplace must contain exactly one plugin")
    if not isinstance(plugins, list) or not plugins:
        return
    entry = plugins[0]
    check(entry.get("name") == PLUGIN.name, "marketplace plugin name mismatch")
    source = entry.get("source", {})
    check(source.get("source") == "local", "marketplace source must be local")
    check(source.get("path") == "./plugins/mattpocock-skills-zh-cn", "marketplace source path mismatch")
    policy = entry.get("policy", {})
    check(policy.get("installation") == "AVAILABLE", "marketplace installation policy mismatch")
    check(policy.get("authentication") == "ON_INSTALL", "marketplace authentication policy mismatch")


def validate_skills() -> set[str]:
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    check(len(skill_dirs) == 25, f"expected 25 Skills, found {len(skill_dirs)}")
    names: set[str] = set()
    description_chars = 0
    explicit_only = 0
    risky = {
        "code-review",
        "diagnosing-bugs",
        "implement",
        "research",
        "resolving-merge-conflicts",
        "to-spec",
        "to-tickets",
        "triage",
        "wayfinder",
    }

    for directory in skill_dirs:
        skill_file = directory / "SKILL.md"
        agent_file = directory / "agents" / "openai.yaml"
        check(skill_file.is_file(), f"{directory.name}: missing SKILL.md")
        check(agent_file.is_file(), f"{directory.name}: missing agents/openai.yaml")
        if not skill_file.is_file() or not agent_file.is_file():
            continue

        frontmatter = parse_frontmatter(skill_file)
        check(set(frontmatter) == {"name", "description"}, f"{directory.name}: frontmatter may contain only name and description")
        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        check(name == directory.name, f"{directory.name}: frontmatter name mismatch")
        check(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)), f"{directory.name}: invalid skill name")
        check(0 < len(name) <= 64, f"{directory.name}: skill name too long")
        check(bool(description), f"{directory.name}: empty description")
        names.add(name)
        description_chars += len(description)

        skill_text = skill_file.read_text(encoding="utf-8")
        if name in risky:
            check("不可信" in skill_text, f"{name}: missing explicit untrusted-content boundary")

        agent_text = agent_file.read_text(encoding="utf-8")
        for field in ("display_name", "short_description", "default_prompt"):
            check(bool(re.search(rf"(?m)^\s*{field}:\s*\".+\"\s*$", agent_text)), f"{name}: missing quoted {field}")
        short_match = re.search(r'(?m)^\s*short_description:\s*"(.+)"\s*$', agent_text)
        if short_match:
            check(25 <= len(short_match.group(1)) <= 64, f"{name}: short_description must be 25-64 chars")
        prompt_match = re.search(r'(?m)^\s*default_prompt:\s*"(.+)"\s*$', agent_text)
        if prompt_match:
            check(f"${name}" in prompt_match.group(1), f"{name}: default_prompt must mention ${name}")
        if re.search(r"(?m)^\s*allow_implicit_invocation:\s*false\s*$", agent_text):
            explicit_only += 1

    check(description_chars <= 8000, f"skill descriptions exceed Codex index budget: {description_chars}")
    check(explicit_only == 13, f"expected 13 explicit-only Skills, found {explicit_only}")
    return names


def validate_markdown(skill_names: set[str]) -> None:
    slash_pattern = re.compile(r"(?<![A-Za-z0-9._-])/(" + "|".join(map(re.escape, sorted(skill_names, key=len, reverse=True))) + r")\b")
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    forbidden = ("disable-model-invocation", "subagent_type", "`Agent` tool calls")

    for path in sorted(SKILLS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        check(not slash_pattern.search(text), f"{relative}: contains Claude-style /skill invocation")
        for token in forbidden:
            check(token not in text, f"{relative}: contains stale Claude token {token}")

        if path.name != "SKILL.md" and len(text.splitlines()) > 100:
            check("## 目录" in "\n".join(text.splitlines()[:30]), f"{relative}: long support document needs a top-level table of contents")

        link_text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for raw_target in link_pattern.findall(link_text):
            target = raw_target.strip().strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            if target == "link" or "<" in raw_target or ">" in raw_target:
                continue
            target_path = target.split("#", 1)[0]
            check((path.parent / target_path).exists(), f"{relative}: broken relative link {raw_target}")


def validate_evals(skill_names: set[str]) -> None:
    seen_ids: set[str] = set()
    covered: set[str] = set()
    count = 0
    try:
        lines = EVALS.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        errors.append(f"evals unavailable: {exc}")
        return
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        count += 1
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"evals line {line_number}: invalid JSON: {exc}")
            continue
        case_id = case.get("id")
        expected = case.get("expected_skills")
        check(isinstance(case_id, str) and bool(case_id), f"evals line {line_number}: missing id")
        check(case_id not in seen_ids, f"evals line {line_number}: duplicate id {case_id}")
        if isinstance(case_id, str):
            seen_ids.add(case_id)
        check(isinstance(case.get("prompt"), str) and bool(case.get("prompt")), f"evals line {line_number}: missing prompt")
        check(isinstance(case.get("should_invoke"), bool), f"evals line {line_number}: should_invoke must be boolean")
        check(isinstance(expected, list), f"evals line {line_number}: expected_skills must be a list")
        if isinstance(expected, list):
            for name in expected:
                check(name in skill_names, f"evals line {line_number}: unknown Skill {name}")
                if name in skill_names:
                    covered.add(name)
    check(count >= 35, f"expected at least 35 activation cases, found {count}")
    check(covered == skill_names, f"activation eval coverage missing: {sorted(skill_names - covered)}")


def validate_repository_files() -> None:
    for name in ("README.md", "CHANGELOG.md", "SECURITY.md", "CONTRIBUTING.md", "COMPATIBILITY.md", "LICENSE"):
        check((ROOT / name).is_file(), f"missing repository file {name}")
    scripts = SKILLS / "diagnosing-bugs" / "scripts"
    check((scripts / "hitl-loop.template.sh").is_file(), "missing Bash HITL template")
    check((scripts / "hitl-loop.template.ps1").is_file(), "missing PowerShell HITL template")


def main() -> int:
    validate_manifest()
    validate_marketplace()
    names = validate_skills()
    validate_markdown(names)
    validate_evals(names)
    validate_repository_files()
    if errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed: marketplace, plugin, 25 Skills, links, safety rules, and eval coverage are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
