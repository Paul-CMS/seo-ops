# Index rate, consolidation, redirects

IDX-01 Rule out technical causes FIRST: noindex, canonical, robots.txt, sitemap, status codes.
IDX-02 Then content causes in order: duplicate pages, competing posts, padded location pages, empty hubs, utility pages eating index budget.
IDX-03 Fix order: consolidate sub-services into H2s + 301; redirect competing posts (after BLG-05); strip location pages; noindex utility/category pages; redirect or delete empty hubs.
RDR-01 Redirects are implemented by the executor (Novamira), only from the approved URL Decision Map via the handoff.
RDR-02 Every redirect row: from, to, type (301), reason, finding_id, has_backlinks_or_traffic.
RDR-03 No redirect without approval.
RDR-04 No chains: point to the final URL; update existing redirects that pointed at a now-redirected URL.
RDR-05 After redirects go live, internal links are updated to point straight at the destination (handoff `link_updates`).
