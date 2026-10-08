---
description: Crawl a client site with the DataforSEO OnPage API and convert it to the audit's Screaming Frog tables
argument-hint: <slug> [domain] [--max-pages 1000] [--mode basic|javascript]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md. Defaults: domain = the client's domain, mode basic, max pages = sitemap size × 1.5 (the estimate says which and why — leave `--max-pages` off unless Paul sets it).

1. `python3 scripts/run.py start <slug> crawl` (the client must exist and
   `/new-client` must have finished; exit 4 → refuse and say so) → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands) — stop on exit 3 (unfinished run → ask Paul).
2. `python3 scripts/crawl.py estimate <slug> --domain <d> --mode <m>` (it prints `Max pages: N — why` and the `Run with:` line)
   - "RESUME" → an earlier crawl exists; resuming downloads its results for free. Go to step 4.
   - exit 6 → the estimate exceeds the balance: **stop**, tell Paul, finish the run with that summary.
3. **Ask Paul to confirm** the estimate and settings (show cost, pages, mode; JavaScript mode
   is 10× the price). Wait for his yes. This step is never skipped, even under $2.
4. `python3 scripts/crawl.py run <slug> --run <RUN_ID> --domain <d> --mode <m> --confirmed` (same max pages as the estimate)
   - Polite: 2,000 ms between hits by default (never below 1,000).
   - exit 10 = still crawling. Run the same command again (each call waits up to ~9 minutes
     and logs progress to log.md). It never posts a second task.
   - exit 8 = an API or network error. Nothing is lost; run the same command again to resume.
   - If the session is interrupted, `/crawl` again resumes from `crawl-state.json` —
     downloads are free for 30 days, so it never pays twice.
5. When it completes: files are in `clients/<slug>/inputs/crawl/` (git-ignored) —
   `<Client> - DFS - internal_all|links_all|page_titles_all|meta_description_all|h1_all|h2_all|all_inlinks|external_all - <date>.csv`
   plus duplicate_titles, duplicate_descriptions, duplicate_content, redirect_chains,
   non_indexable, and the crawl-config `.md`. Copy them to Drive with
   `python3 scripts/drive.py upload <slug> --run <RUN_ID> --file <each file>` (they land in
   `01 - Discovery and Audit/Evidence/`; byte-exact file copies, logged — the model never retypes a file).
5b. `python3 scripts/crawl.py text <slug> --run <RUN_ID>` (S05b, free): the body text of every page →
   `data/crawl/page-text.csv`; the crawl itself leaves `data/crawl/crawl-summary.csv`. Agents read these two,
   never the raw tables. Record S05b with `steps.py record`.
6. Record the step: `python3 scripts/steps.py record <slug> --run <RUN_ID> S05 done --output clients/<slug>/inputs/crawl/`
   (or `failed` / `skipped` with `--reason`). Reuse: if `steps.py fresh <slug> S05` says reuse
   (crawled under 60 days ago), do not crawl again unless Paul asks.
7. `run.py finish <slug> <RUN_ID> --summary "Crawled N pages, $X"`

Never print or commit credentials. Never call DataforSEO except through the scripts.
