# Repository instructions

Main editable source is `src/`; build output is `dist/`, never edit it by hand.
Read `docs/architecture.md` and `docs/content-guide.md` before changing structure or data.
For UI work read applicable instructions in `tools/skills/taste-skill/skills/taste-skill/SKILL.md` and `tools/skills/ui-ux-pro-max-skill/cli/assets/skills/design-system/SKILL.md`, and use the UI/UX search tools when helpful. Apply rules according to the static HTML/Jinja stack; do not introduce React solely for a skill default.
Preserve public routes, author order and research facts. Do not invent missing metadata. Never publish `legacy`, `tools`, `.env`, or backup files.
Use Conda environment UITweb (Python 3.10); see README for its actual prefix. Run build and check_site for template/data changes; node --check for JS. Public deployment remains deferred.

## Anti-Slop UI/UX Instructions

For all UI/UX development and redesign tasks:

1. Read `.agents/skills/antislop/SKILL.md` first.
2. Apply `.agents/skills/antislop-ui/SKILL.md` for visual design.
3. Apply `.agents/skills/antislop-human/SKILL.md` for accessibility.
4. Apply `.agents/skills/antislop-layoutmobile/SKILL.md` for responsive design.
5. Apply `.agents/skills/antislop-copywriting/SKILL.md` for website text.
6. Apply `.agents/skills/antislop-code/SKILL.md` when reviewing code comments.

Use Anti-Slop in "during" mode when implementing UI changes.

Preserve the existing website architecture, Jinja2 templates,
Python build pipeline, research data, and public routes.

Do not introduce React, Next.js, or another frontend framework
unless explicitly requested.

Follow existing project-specific UI/UX instructions alongside
Anti-Slop. Do not overwrite the original design rules.

Before modifying UI, analyze the existing design and propose
a concrete improvement plan.

After implementation, run applicable build and validation checks.
