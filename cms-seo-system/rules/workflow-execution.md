# Workflow, gates, execution

The system decides, Paul approves, the executor (Novamira) implements. The executor never decides what to change.

WF-01 Gates in order: entity foundation approved → proof sheet → client returns sheet → Brand Guide / business truth → audit deliverables → Block 1 approval → Build. Agent 1 never starts Agent 2 on its own.
WF-02 Builds run in sections: all briefs → one correction round → all drafts → one correction round → handoff.
WF-03 Minor deviations are applied as defaults and don't stop the run.
WF-04 Brand Guide updated once per section (SVC-17).
WF-05 No workflow changes inside a client session; flag for a system session.
WF-06 One client per session; two clients can run in parallel sessions.
WF-07 Model per step: Opus = audit decisions and entity research; Sonnet = briefs, drafts, handoff build; Sonnet or Haiku = executor and QA.
WF-08 Pages needing the Service Page Optimizer go into the handoff (`route: spo`); Agent 2 doesn't rewrite them.

## Executor rules
NOV-01 Writes only what is in the approved handoff. Anything else is flagged, never improvised.
NOV-02 Title, H1, meta written for every page in the handoff, including `route: spo` pages.
NOV-03 Redirects from the handoff redirect table (RDR-02).
NOV-04 Refuses to run unless the handoff has `backup.confirmed: true` with a timestamp from the last 24 hours (ManageWP or BlogVault).
NOV-05 Logs every change on the server: run id, page, field, old value, new value. The log enables resume and rollback.
NOV-06 New pages are created as drafts in the `stage` run; everything goes live together in the `apply` run (batch publish, no multi-week waits).
NOV-07 Human VA adds images and reviews each drafted page between `stage` and `apply`. Design specs: deferred.
NOV-08 One ongoing handoff file per client; it must be accurate and detailed.
NOV-09 Clear WP Rocket cache for every changed URL after `apply`.

## Testing
TST-01 Rebuilds always publish as a batch. Single-variable testing applies only to already-ranking pages after launch: baseline → one change → resubmit in GSC → evaluate.
TST-02 After launch, a timed Agency OS task re-pulls GSC data to monitor the pages.

## Priority order for action plans
1 homepage title + H1 · 2 brand consistency · 3 service page H tags · 4 location cleanup · 5 sub-service consolidation + redirects · 6 blog redirects · 7 schema · 8 citations (day 1, parallel) · 9 GBP posts · 10 press releases · 11 ID page (month 2)
