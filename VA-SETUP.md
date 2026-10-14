# seo-ops on a VA's Mac — setup and daily use

This guide puts the Coastal Marketing SEO system (seo-ops) on a VA's Mac, so the VA can run every stage
themselves. **Paul still makes every decision.** On the VA's Mac the system runs, prepares, checks and
logs. When it reaches a decision it stops and prints an `/approve` line. The VA sends that line to Paul,
and Paul approves on his own Mac. The VA's Mac is set up so that it **cannot** approve.

Both Macs share one GitHub repository (`Paul-CMS/seo-ops`, private). Each finished run is committed
and pushed automatically, so both Macs see the same records once they `git pull`.

The full procedure (who does what, in what order) is in `CLAUDE.md`. Claude reads it on every session,
so the VA does not need to learn it by heart. This guide covers only setup and the daily routine.

---

## Part A — Paul does these first (once)

1. **GitHub:** add the VA as a collaborator on `github.com/Paul-CMS/seo-ops`: Settings →
   Collaborators → Add people, with **Write** access.
2. **Google Drive:** share the folder **`v3. CMS Technical SEO Audit 2026`** with the VA's Google
   account as **Editor**. Share nothing else. The system only ever touches v3.
3. **Claude:** the VA needs a Claude plan that includes Claude Code and the Opus model (Max, Team or
   Enterprise). On a Team or Enterprise plan, add them to the organization.
4. **Credentials:** decide what to give the VA, and send it through a password manager (never by
   email or chat):
   - DataforSEO API login and password (app.dataforseo.com → API Access). The VA's runs spend from
     the same balance.
   - For each client site the VA will work on: **a separate WordPress Application Password**
     (wp-admin → Users → seo-ops → Application Passwords → name it `seo-ops-va`). With a separate
     password you can revoke the VA's access without breaking your own.
5. **Push your own work first:** on your Mac, run `git push` in `~/Documents/seo-ops`, or finish a run,
   which pushes for you. The VA then starts from your latest records.
6. Send the VA the zip, `seo-ops-va.zip`, and this guide.

---

## Part B — The VA sets up the Mac (once, about 45 minutes)

### B1. Install the tools

1. **Command-line tools** (git and Python). Open **Terminal** and run:

   ```bash
   xcode-select --install
   ```

   Click *Install* in the window that appears and wait for it to finish. Check it worked:

   ```bash
   python3 --version
   ```

   It should print `Python 3.9` or newer. Then run `git --version`, which should print a version.

2. **Homebrew**, then **GitHub CLI** (this signs git in to GitHub). Follow the one-line install at
   https://brew.sh, then:

   ```bash
   brew install gh
   ```

   ```bash
   gh auth login
   ```

   Choose GitHub.com, HTTPS, *Yes* to authenticate git, and *Login with a web browser*. Sign in with
   the GitHub account Paul invited, and accept the invitation email from GitHub if you haven't yet.

3. **Google Drive for desktop:** install it from https://www.google.com/drive/download/ and sign in
   with the Google account Paul shared v3 with.
   - Open https://drive.google.com → *Shared with me* → right-click **v3. CMS Technical SEO Audit
     2026** → *Organize* → *Add shortcut* → *My Drive*. The folder then appears on your Mac.
   - Open Drive for desktop's settings and choose **Stream files**.

4. **Claude desktop app:** install it from https://claude.ai/download, sign in, and open the **Code** tab.

### B2. Put the system in place

1. Unzip `seo-ops-va.zip`. You get a folder named `seo-ops`. Move it into your **Documents** folder,
   so its path is exactly `~/Documents/seo-ops`. The system expects that path.
2. In Terminal, run these one at a time. Use your own name and email:

   ```bash
   cd ~/Documents/seo-ops
   ```

   ```bash
   git config user.name "Your Name"
   ```

   ```bash
   git config user.email "you@example.com"
   ```

   ```bash
   git pull
   ```

   `git pull` should say *Already up to date* or list some files. If it asks for a password, redo
   `gh auth login`.

### B3. Tell the system about this Mac — `machine.json`

1. Find your local path to v3. In Finder, open *Google Drive* → *My Drive*, then right-click
   **v3. CMS Technical SEO Audit 2026** while holding **Option** → *Copy "v3…" as Pathname*.
2. In `~/Documents/seo-ops`, create a file named **`machine.json`** (TextEdit → Format → *Make Plain
   Text*, or ask Claude to create it). Paste your path in place of the example:

   ```json
   {
     "drive_local_root": "/Users/YOU/Library/CloudStorage/GoogleDrive-you@example.com/My Drive/v3. CMS Technical SEO Audit 2026",
     "can_approve": false,
     "can_change_system": false
   }
   ```

   - `drive_local_root`: where v3 is on **this** Mac.
   - `can_approve: false`: this Mac runs the work but never approves. Do not change it.
   - `can_change_system: false`: this Mac never changes the workflow (scripts, rules, specs). If something in
     the workflow looks wrong, the session flags it for Paul (`run.py flag`) and carries on. Do not change it.
   - Git never uploads `machine.json`, because each Mac keeps its own.

### B4. Credentials — `.env`

1. In Terminal, run:

   ```bash
   cp ~/Documents/seo-ops/.env.example ~/Documents/seo-ops/.env
   ```

2. Open `.env` in TextEdit and fill in the values Paul sent you through the password manager:
   `DFS_LOGIN` and `DFS_PASSWORD`, then one three-line WordPress block per client. Claude can print
   the exact three lines for a client without seeing any password. In a Claude session, ask:
   *"show me the env lines for <client-slug>"*.
3. **Never** paste a password into the Claude chat, an email or Slack. Git never uploads `.env`, and
   Claude is blocked from reading it, so the scripts load it themselves.

### B5. Check that everything works

1. **The test suite (fast tier).** It uses no network, no money and no client data, and takes under a minute:

   ```bash
   cd ~/Documents/seo-ops && python3 tests/run_all.py
   ```

   The last line must say `… passed, 0 failed`. If anything fails, send Paul the output. (The full tier, `--full`,
   takes 10–15 minutes; Paul runs it before changing the system — a VA never needs it.)

2. **Drive:**

   ```bash
   python3 scripts/drive.py where apex-roofing-of-the-lowcountry
   ```

   It should print the client's `… - TMS` folder inside your v3 path. *Not set up* or *not there*
   means the path in `machine.json` is wrong, or Drive isn't syncing.

3. **Claude:** in the Claude app's Code tab, start a new session in the client's own folder
   (`python3 scripts/worktree.py open <client-slug>` prints it). The first message should be the seo-ops reminder
   about one session per stage. Type `/where <client-slug>`. It should tell you where that client stands.

4. **WordPress**, for each client you'll work on: in a session, type `/wp-check <client-slug>`. It
   must pass before any WordPress work.

---

## Part C — Daily routine for the VA

### Every session

1. **Pull first, then open the client's own folder.** In Terminal:

   ```bash
   cd ~/Documents/seo-ops && git pull && python3 scripts/worktree.py open <client-slug>
   ```

   It prints a folder like `~/Documents/seo-ops-clients/<client-slug>` (made the first time, reused after).
   Each client has its own folder, so two clients can run at the same time in two chats without mixing.

2. **New session per stage.** In the Code tab, start a **new** session **in that client folder** with
   the model set to **Haiku**. The heavy work runs in Opus agents automatically. Never switch a
   session's model halfway; start a new session instead.
3. Type **`/next <client-slug>`**. The system runs whatever comes next and stops at the next decision
   or review point.
4. If it says *"Start a new session"*, the stage changed. Open a new session (step 2) and type
   `/next <client-slug>` again.

**The folder rule.** Client work runs **only in the client's own folder** (`python3 scripts/worktree.py open
<client-slug>` prints it). `~/Documents/seo-ops` itself is for system sessions only — if `run.py` or `publish.py`
says *"Client work runs in the client's folder"*, you are in the wrong folder: close that chat, open the client's
folder, start a new chat there and type `/next <client-slug>` again. Never start a run for a client from two folders,
and never run a script by its full path into `~/Documents/seo-ops`.

### Place research — Deep Research for a new town (before location pages)

Research for a town and a niche is done once and reused by every client. When `/next` says place research is
missing (or to check): 

1. In the client's folder, run `python3 scripts/places.py status <client-slug>` — it lists the planned towns with no
   place or niche research and gives the command for each.
2. For each town: `python3 scripts/places.py prompt <client-slug> "<Town>"` — it writes the prompt to
   `clients/<client-slug>/build/places/prompts/<town>-<niche>.md`. Open that file and paste the whole prompt into
   **Gemini Deep Research**.
3. Save Gemini's report (Markdown, with its tables) as `clients/<client-slug>/inputs/places/<town>-<niche>.md`
   (lowercase, hyphens, for example `okatie-roofing.md`).
4. `python3 scripts/places.py ingest <client-slug> clients/<client-slug>/inputs/places/<town>-<niche>.md` — it sorts
   the tables into the store. Then run the `verify` command it prints; the system checks every link loads and every
   quote is on its page, and drops what fails. A researcher agent checks the rest by meaning. Nothing in this step
   is ever sent to a client.

### When it stops at a decision (`/approve …`)

1. The session prints a line like `/approve apex-roofing-of-the-lowcountry audit_approved brand_guide_approved`
   and lists the files it covers. **Do not type it yourself.** On your Mac it is refused.
2. Send Paul the `/approve` line, plus links to the files in Drive (they are already in the client's
   v3 folder).
3. Paul runs `git pull`, reviews, and types the `/approve` line on his Mac (or asks for revisions).
   His approval is committed and pushed.
4. Run `git pull` again, then `/next <client-slug>`.

### Also stop and ask Paul when

- **Money:** the session asks for a "cost yes" on DataforSEO **over $2**, or says the balance is too low.
- **An unfinished run** (the session asks: resume, verify, roll back or abort). Paul decides.
- **A live page:** anything touching a page that is already published (`--live`) needs Paul's ManageWP backup confirmation.
- **Sensitive industry:** `/new-client` can't tell whether an industry is health, legal, insurance or financial.
- **Old instruction files:** `/archive-old-instructions` asks Paul, file by file.
- **Anything to a client:** the system never sends anything to a client. Paul sends the proof sheet and every question set.

### The VA Worklist — one document per client

Everything a person has to do for a client is one row of its **VA Worklist** (Drive: "<Client> - VA Worklist",
in the client folder; repo: `clients/<slug>/handoffs/VA-WORKLIST.md` and `.csv`). It opens with a one-page cover (what
it is, the order to work in, who owns what, how to tick rows) and then has one section per type: 1 Setup · 2 Blockers ·
3 Redirects · 4 Publish · 5 After publish · 6 Manual lookups. Setup, Blockers and Manual lookups can be worked any
time; Redirects, Publish and After publish arrive in one handover, once every service and location page is a
WordPress draft — then every page is published together. The system does not hand a worklist over until its checker
(`worklist.py check`) passes, so every row is complete on its own.

**Every row has the same fields:**

| Field | What it tells you |
|---|---|
| `id` | The row's name — quote it when you ask about it |
| `task` | One action in plain words ("Publish the Okatie page") |
| `where` | The live URL **and** the WordPress edit link — start there |
| `how` | Numbered steps; follow them in order |
| `values` | Exactly what to type: slug, SEOPress title, meta description, redirect from → to, menu label, alt text |
| `depends_on` | Rows that must be done first (a redirect waits for its target page to be published) |
| `done_check` | How to confirm it worked (the URL loads; the old URL answers 301 to the new one; the title shows in the page source) |
| `owner` | Jonie, Gwen or Paul |
| `status` | `open` · `done` · `superseded` (a newer decision replaced it — skip it) |

**Ticking:** work the rows from top to bottom inside each section. Check the current value first (`old`): already
done → mark `done` and write `already done` in `note`; something else there → change nothing, mark `blocked` and
say what you found. Set `status` to **done**, **blocked** or **deviated** (a `note` on every blocked or deviated row)
and give the CSV back. Never add rows and never publish a page that shows an "Open items on this page" notice until
its row is resolved. The next `/next` reads your ticks and **checks every done row against its `done_check`** — a row
whose check fails comes back as `open`, with the reason in `note`.

### If something in the workflow looks wrong

Don't work around it and don't change anything. The session flags it for Paul (`run.py flag …`), carries on with
the current rules, and the flag shows in the client's STATUS.md under "Flagged for Paul (system)".

### One chat per client at a time

Each client runs in its own folder (`worktree.py open <slug>`), and each run commits only that client's
files, so different clients never mix. While a run is open for a client, no other chat may start one ("another
chat is working on …") — not even a new chat in the same folder; when that run finishes, the next chat may go on.
If the first chat is really gone with its run still open, ask Paul — only he clears the lock.

**Paul and the VA never work on the same client at the same time** (a manual rule — the lock only sees runs, not
two people reading and planning). Agree who has which client before starting, and `git pull` before you begin. If a run ends with `NOT PUSHED` or `push failed`, the work is safe on your Mac; send Paul
the message. Don't try to fix it yourself.

### Never

- Never type `/approve`, and never edit `machine.json` to allow approvals.
- Never run client work in `~/Documents/seo-ops` — only in the client's own folder (the folder rule above).
- Never edit `status.json`, `log.md`, `changes.jsonl`, or the generated records (`handoff-log.md`,
  `decisions.md`, `approval-record.md`, `document-checklist.md`, `STATUS.md`, `decisions-settled.md`).
  Scripts write them.
- Never delete or rename files in Drive. Never look outside the v3 folder.
- Never publish in WordPress through the system. It makes drafts only, and Jonie publishes.
- Never change scripts, hooks, commands, agents, `CLAUDE.md` or the methodology. That is Paul's
  design work, done on Opus with the test suite.

---

## Command reference

| Command | What it does |
|---|---|
| `/next <slug>` | Runs whatever comes next for a client and stops at the next decision or review point |
| `/where <slug>` | Where the client stands, what ran last, what's next |
| `/new-client` | Sets up a new client: intake, Drive folder, CMS, document checklist |
| `/wp-check <slug>` | Tests the WordPress connection |
| `/verify <slug>` | Re-checks changed pages against the live site (system changes and VA handoffs marked done) |
| `/rollback <slug>` | Restores old values from a run, only after Paul approves the plan |
| `/discovery`, `/crawl`, `/build`, `/finish`, `/blog`, `/interview`, `/implement` | The stage commands. `/next` picks the right one, so you rarely type them |

Quick terminal checks (from `~/Documents/seo-ops`):

```bash
python3 scripts/records.py top <slug>
```

```bash
python3 scripts/status.py view <slug>
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `REFUSED — this Mac runs the stages but does not approve` | Expected. Send the `/approve` line to Paul. |
| `Drive for desktop is not set up` / `folder … is not there` | Check the path in `machine.json`, and that Drive for desktop is signed in and shows v3 under My Drive. |
| `push failed (commit is safe locally)` | `git pull`, then `git push`. A conflict → send it to Paul. |
| A `/next` refusal saying something is missing (exit 4) | Do what the message says first. Never work around it. |
| WordPress 401 / `wp-check` fails | The Application Password in `.env` is wrong or was revoked. Ask Paul for a new one. |
| Test suite fails after a `git pull` | Send Paul the output. Don't run client work until it passes. |
