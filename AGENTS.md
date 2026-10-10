# Repository instructions

Main editable source is `src/`; build output is `dist/`, never edit it by hand.
Read `docs/architecture.md` and `docs/content-guide.md` before changing structure or data.
For UI work read applicable instructions in `tools/skills/taste-skill/skills/taste-skill/SKILL.md` and `tools/skills/ui-ux-pro-max-skill/cli/assets/skills/design-system/SKILL.md`, and use the UI/UX search tools when helpful. Apply rules according to the static HTML/Jinja stack; do not introduce React solely for a skill default.
Preserve public routes, author order and research facts. Do not invent missing metadata. Never publish `legacy`, `tools`, `.env`, or backup files.
Use Conda environment UITweb (Python 3.10); see README for its actual prefix. Run build and check_site for template/data changes; node --check for JS. Public deployment remains deferred.
