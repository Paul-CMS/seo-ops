# FILE NAMING CONVENTION
### Every file in every `[Client Name] - TMS` folder. Checked by `scripts/naming.py`.
Based on Drive v3 `Resources/FILE-NAMING-CONVENTION.md`, plus Paul's content codes and the
LNKD change (2 Oct 2026).

---

## 1 · Content briefs and drafts

```
[CODE] - [Service or Location Name] - [Client Name]
```

| Code | Means | Code | Means |
|---|---|---|---|
| SB | Service brief | SD | Service draft — approved content before implementation |
| LB | Location brief | LD | Location draft — approved content |
| LBCH | County hub brief | LDCH | County hub draft |
| HB | Homepage brief | HD | Homepage draft |
| AB | About brief | AD | About draft |
| PB | Blog post brief | PD | Blog post draft |

Examples: `SB - Roof Repair - Red Rover Roofing` · `LD - Franklin TN - Exodus Chiropractic of Franklin`

- **No status suffix and no extension in the title.** The code carries the meaning: a draft
  only gets its `SD` / `LD` name once Paul approves it. Unapproved content stays in the repo.
- The client name is the folder's client name exactly (e.g. "Exodus Chiropractic of Franklin").
- Page order (Red Rover's S2.1 / L1.7 numbers) lives in the client's page-order table, not
  the file name.

## 2 · Deliverables

```
[Client Name] - [Artifact] - [DRAFT | REVIEW | APPROVED | SUPERSEDED | RETURNED].md
```

`DRAFT` in progress · `REVIEW` awaiting Paul · `APPROVED` signed — the only status an agent
acts on (the Drive copy is stamped with Paul's name, date and sha) · `SUPERSEDED` → move to `_Archive/` ·
`RETURNED` the client's returned proof sheet, as given. The proof sheet's native Google Doc is
`[Client Name] - Client Proof Sheet - CLIENT COPY` (no extension). Paul's own notes and answers:
`[Client Name] - INTERNAL - [description] - [YYYY-MM-DD].md`.

## 3 · Living records — no status, never versioned

`[Client Name] - Brand Guide.md` · `- Approval Record.md` · `- Document Checklist.md` · `- Handoff Log.md` · `- Status.md`
(all copied into the client folder by the scripts — R4)

## 4 · Evidence

```
[Client Name] - [Source] - [Export] - [YYYY-MM-DD].[ext]
```

| Tag | Tool | Tag | Tool |
|---|---|---|---|
| DFS | DataforSEO (crawl, rankings, backlinks) | GSC | Search Console |
| SF | Screaming Frog (fallback) | GA4 | Google Analytics |
| LNKD | Linkdominator — **legacy files only** (was LD); no longer used | CMS | WordPress export |
| BL | BrightLocal | MANUAL | Built by hand |

**LD means location draft only.** Old evidence files tagged `LD` are not renamed
automatically — they go on the rename list for Paul's approval.

## 5 · Reference material

`[Client Name] - [Description] - REFERENCE.[ext]`

## 6 · Client-facing copies

`[Client Name] - Client Proof Sheet - CLIENT COPY` (Google Doc, generated from the `.md`).
A distinct name, so it never forms a same-name pair with the Markdown record.

## Never

- Two files with the same name in one folder (delete a Drive-converted duplicate; the `.md` governs)
- `(1)`, `(2)`, `copy of`
- A file name without the client name (content files: client name last)
- Tool-default names with IDs and timestamps
- A deliverable without a status
- `&` in folder names

## Renaming existing files

Never automatic. `naming.py rename-list` produces old → new for Paul to approve; only
approved rows are renamed.
