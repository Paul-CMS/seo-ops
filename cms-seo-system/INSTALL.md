# Install (5 minutes, once)

1. Unzip `cms-seo-system.zip` into the ROOT of your seo-ops repo, so you have `seo-ops/cms-seo-system/`.
2. Make the two skills visible to Claude Code (from the repo root):
   ```bash
   mkdir -p .claude/skills
   cp -r cms-seo-system/skills/novamira-executor .claude/skills/
   cp -r cms-seo-system/skills/implementation-qa .claude/skills/
   ```
   (The skill files point back to `cms-seo-system/` for rules and scripts, so keep that folder too.)
3. Add these lines to the repo's `CLAUDE.md`:
   ```
   ## Rules
   Bradley rules live in cms-seo-system/rules/. Load only the files the current step needs
   (map: cms-seo-system/rules/README.md). They override older skill text.
   Handoffs follow cms-seo-system/handoff/HANDOFF-SPEC.md.
   ```
4. Start a SYSTEM session (`/clear`, Sonnet) and send:
   > Read cms-seo-system/CONFLICT-PATCHES.md and apply patches 1–7 to the listed files exactly as
   > written. One-line summary per file. Touch no client data.
5. Archive the boss's old Bradley prompt (patch 6) so it isn't active anywhere.
6. Commit: `git add -A && git commit -m "CMS SEO system v1: rules, handoff, executor, QA"`.

Then follow runbook/TEST-RUN.md for the Carolina Carpet Cleaning run.
