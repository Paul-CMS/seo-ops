# Area source lists (rewrite 2 P6)

One file per area, `<state>-<area>.md` (e.g. `sc-lowcountry.md`, `pa-south-central.md`). The researcher agent reads the
client's area file first when it looks up a public fact (a place, a permit rule, a licence, the state code), then other
official sources. Every link carries the date it was checked. A list is built once and reused for every client in the
area; the researcher suggests new sources with `run.py flag`, and Paul adds them in `/system-review`.

| File | Area | Clients |
|---|---|---|
| `sc-lowcountry.md` | Beaufort, Jasper, Charleston, Berkeley, Dorchester counties, SC | Apex Roofing of the Lowcountry, Home Mobile Medical |
| *(to build)* `pa-south-central.md` | Adams County, PA | Gettysburg Mold Remediation Pros — the researcher drafts it on first use and flags it |
