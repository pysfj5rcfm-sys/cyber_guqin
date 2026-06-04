# Skill Install Instructions

## Why Direct Install Was Not Completed

The requested target path was:

```text
.agents/skills/
```

During the prior Phase S0 run, the managed sandbox exposed `.agents` as readable but not writable. Because the task explicitly prohibited forcing permissions or changing `.agents` access, the two `SKILL.md` files were staged under `reports/skill_install_staging/` instead of being written directly to `.agents/skills/`.

## Staging Files

The staged skill files are:

```text
reports/skill_install_staging/guqin-canon-builder/SKILL.md
reports/skill_install_staging/guqin-dapu-parser/SKILL.md
```

## Manual Install Targets

Install them to:

```text
.agents/skills/guqin-canon-builder/SKILL.md
.agents/skills/guqin-dapu-parser/SKILL.md
```

## Linux/macOS Install Commands

Run from the repository root:

```bash
mkdir -p .agents/skills/guqin-canon-builder .agents/skills/guqin-dapu-parser
cp reports/skill_install_staging/guqin-canon-builder/SKILL.md .agents/skills/guqin-canon-builder/SKILL.md
cp reports/skill_install_staging/guqin-dapu-parser/SKILL.md .agents/skills/guqin-dapu-parser/SKILL.md
```

## Windows PowerShell Install Commands

Run from the repository root:

```powershell
New-Item -ItemType Directory -Force .agents\skills\guqin-canon-builder | Out-Null
New-Item -ItemType Directory -Force .agents\skills\guqin-dapu-parser | Out-Null
Copy-Item reports\skill_install_staging\guqin-canon-builder\SKILL.md .agents\skills\guqin-canon-builder\SKILL.md -Force
Copy-Item reports\skill_install_staging\guqin-dapu-parser\SKILL.md .agents\skills\guqin-dapu-parser\SKILL.md -Force
```

## Post-Install Checks

Linux/macOS:

```bash
test -f .agents/skills/guqin-canon-builder/SKILL.md
test -f .agents/skills/guqin-dapu-parser/SKILL.md
```

Windows PowerShell:

```powershell
Test-Path .agents\skills\guqin-canon-builder\SKILL.md
Test-Path .agents\skills\guqin-dapu-parser\SKILL.md
```

After both files exist at the target paths, Phase S0 can be treated as complete, assuming the existing validators still pass.
