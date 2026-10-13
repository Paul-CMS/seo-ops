# Area source lists (rewrite 2 P6)

One file per area, `<state>-<area>.md` (e.g. `sc-lowcountry.md`, `pa-south-central.md`). The researcher agent reads the
client's area file first when it looks up a public fact (a place, a permit rule, a licence, the state code), then other
official sources. Every link carries the date it was checked. A list is built once and reused for every client in the
area; the researcher suggests new sources with `run.py flag`, and Paul adds them in `/system-review`.

| File | Area | Clients |
|---|---|---|
| `sc-lowcountry.md` | Beaufort, Jasper, Charleston, Berkeley, Dorchester counties, SC | Apex Roofing of the Lowcountry, Home Mobile Medical |
| *(to build)* `pa-south-central.md` | Adams County, PA | Gettysburg Mold Remediation Pros — the researcher drafts it on first use and flags it |

## Public lookups — verify, never ask (CM-061 part 2)

A client fact with a public lookup is verified by the researcher, not asked. Each lookup is logged (`research.py log`);
only a lookup logged `not_found` at the minimum may become an Ask (kind 2, a legal or money claim).

| Fact | Where | States |
|---|---|---|
| Contractor licence (number, class, status, expiry) | The state licensing board lookup — SC LLR (`sc-lowcountry.md` → State); TN Board for Licensing Contractors; PA Attorney General Home Improvement Contractor search | SC, TN, PA |
| Manufacturer certification | The manufacturer's own contractor finder: GAF (gaf.com → Find a contractor), CertainTeed (certainteed.com → Find a pro), Owens Corning (owenscorning.com → Find a contractor), Velux, DaVinci Roofscapes | all |
| Business registration (legal name, status) | The state business entity search — SC Secretary of State (`sc-lowcountry.md` → State); TN SOS business search; PA DOS business search | SC, TN, PA |
| Insurance | Only a public certificate (a state or board listing). None → it stays a client fact | all |
