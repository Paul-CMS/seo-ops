# [Client Name] - Handoff Log
### Append-only. Each agent run writes its section as its LAST action.
The repo safety log (`clients/<slug>/log.md`) records every change; this file is the
human-readable summary that the next person — or VA — reads cold.

## Section template

```
## [Agent] · [date] · run [RUN_ID]

**What I did**
-

**What was decided, and why**
-

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|

**What I could not check**
-

**Anything the next agent would otherwise get wrong**
-
```

The last field is the important one: the sentence you would say out loud handing over in person.

---

## Entries
