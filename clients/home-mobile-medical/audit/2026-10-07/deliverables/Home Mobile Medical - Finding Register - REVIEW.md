# Home Mobile Medical - Finding Register - REVIEW

**Status:** REVIEW - awaiting Paul (gate audit_approved). Rendered 2026-10-08 from the audit registers in `clients/home-mobile-medical/audit/2026-10-07/` (run 20261007-203219-discovery-784c). Rendered, never edited: to change anything, change the register row and re-render.

Severity scale CM-028 (High / Medium / Low only). One finding per issue, every affected URL listed. Effective revision shown (after the independent S17 review, CM-026); superseded revisions stay in findings.csv. All page specs are DRAFT, so failed spec checks are advisory recommendations, not gates.

**Totals (after review):** 40 findings - High 12, Medium 13, Low 15. Reviewed: 28 confirmed as written, 12 revised by superseding row, 0 withdrawn.

| ID | Severity | Category | Observation | Affected (count) | Recommendation | Owner | Client conf. | Paul approval | Rev |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | High | 3 Brand & entity (HP-02); 6 On-page (HP-01) | Homepage SEO title is "Home Mobile Medical — Home Medical Equipment — South Carolina Lowcountry"; the category slot reads "Home Medical Equipment". The GBP primary category entity is "Mobility equipment supplier" (Brand Guide A2). The homepage meta description reads "Stair lift installation and home medical equipment across the Lowcountry...". Title order (brand, category, area) is correct; the category term is not the GBP category or an approved variant (Brand Guide A3 excludes "medical equipment supplier"). | 1 | Rebuild the homepage title to the Brand - GB Category - Area Entity format with the approved category entity, in the homepage batch (final1). Expected impact: the brand hub stops signalling broad home-medical-equipment (the discontinued DME entity) and matches the GBP category. Title changes are structural (handoff to Jonie; structural_changes_allowed is met). | Jonie (handoff) after Build | No | Yes | 1 |
| F-002 | High | 3 Brand & entity; 5 Architecture | The site-wide navigation/footer on all 102 pages in the link-level export links to the Georgia hub /service-area/savannah/ (SF Unique Inlinks = 96 on that URL). Every service page links to /service-area/savannah-ga/, /service-area/pooler-ga/ and /service-area/rincon-ga/. Nine Georgia city pages (titles "Stair Lift Installation in <City>, GA \| Home Mobile Medical") are indexable (meta robots "index, follow"), self-canonical and listed in the XML sitemap. /service-area/georgetown-ga/ links out to georgetown-mi.gov (Michigan). The approved area entity is South Carolina Lowcountry (Brand Guide A5) and Georgia is served only from a separate microsite (Brand Guide E, H; Paul 2026-10-06). | 15 | Per Paul's decision: do NOT redirect any Georgia URL to an SC page; all 18 Georgia URLs are "Hold - microsite" in the URL Decision Map (301 to the equivalent microsite page once it exists, each CM-019-checked). Now: remove the Georgia hub from site navigation and the Georgia links from SC service pages (menu/link changes - non-destructive; menu changes are a Jonie handoff). Expected impact: the site expresses one area entity (South Carolina Lowcountry) that contains every linked city. | Jonie (menu handoff) | No | Yes | 1 |
| F-003 | High | 3 Brand & entity; 5 Architecture | Live, indexable pages describe services the business does not offer (Brand Guide D "Not offered": broad DME, rentals, power chairs, scooters/scooter lifts, mobility ramps): (a) the site-wide navigation links to /services/power-chairs/, /services/scooter-lifts/ and /services/mobility-ramps/ from every page (SF Unique Inlinks 96 each); (b) /services/ is titled "Mobility Devices \| Home Mobile Medical" with meta "From wheelchairs and scooters to lifts and ramps..."; (c) /service-area/mt-pleasant-sc/ and /service-area/ladys-island-sc/ are titled "Medical Equipment In ..."; (d) /bluffton-sc/ H2 "Medical Equipment Sales & Rentals in Bluffton, SC"; (e) /bluffton-sc/wheelchair-lift-repair/ H2 "We Rent and Sell Mobility Equipment in the Lowcountry"; (f) /service-area/hilton-head-island-sc/ meta "installs stair lifts, porch lifts, and scooter lifts"; (g) discontinued service pages /charleston-sc/power-chairs/, /charleston-sc/mobility-ramps/ and post /mobility-scooter-repair-near-me/ are indexable; (h) uncrawled CMS pages /power-chairs/, /beaufort-sc/, /charleston-sc/, /hilton-head/ carry rental/power-chair wording in their CMS excerpts; (i) the Beaufort page states "We rent and sell mobility equipment in the Lowcountry." (Brand Guide D2). | 17 | Remove the discontinued-service links from navigation now (non-destructive, menu handoff). Rewrite the kept pages (/services/, Hilton Head Island, Lady's Island, Beaufort content) in Build to the confirmed services only. URL dispositions are in the URL Decision Map: /services/power-chairs/, /services/scooter-lifts/, /services/mobility-ramps/, /charleston-sc/power-chairs/ and /power-chairs/ pass CM-019 C1-C3 and stay Needs Evidence until the client confirms no leads (C4, Q1) - 301 only, never 410 (Paul 2026-10-06). /charleston-sc/mobility-ramps/, /bluffton-sc/, /bluffton-sc/wheelchair-lift-repair/ and /service-area/mt-pleasant-sc/ FAIL CM-019 C1 (they rank): no destructive recommendation - keep live, strip the discontinued/DME claims, de-link; only a Paul Exception (Q3) could change that. Expected impact: the site stops asserting a DME/rental entity the GBP and Brand Guide no longer represent. | Jonie (menu/redirect handoffs) after Paul | Yes | Yes | 2 |
| F-005 | High | 3 Brand & entity (HP-25, LOC-27; CM-025/CM-040) | Safety claims without a named authoritative source appear on commercial pages of a health-adjacent client: homepage "Safety is our top priority, and we adhere to the highest standards and regulations."; Beaufort page "...installation meets the highest standards of safety and care." and "...ensure your stair lift is ready for safe use the same day it is installed." (quotes from the 2026-09-18 crawl as recorded in Brand Guide D2). | 2 | Replace with the Paul-approved safety statement (Brand Guide D: "Safety comes first. Jason holds every installation to the highest industry standards and the manufacturer's installation instructions.") and add "in most cases" to same-day wording; no regulatory-compliance claim (CM-040). Paul approves the page with the human review recorded (CM-025 rule 1). Expected impact: removes an unsupported safety/regulatory claim from a health-adjacent site. | Build writer -> Paul -> Jonie | No | Yes | 1 |
| F-013 | High | 5 Architecture (SVC-01, LOC-01; BB-202/203/204; CM-001, CM-019) | 20 SC URLs duplicate the intent of a canonical service or location page through legacy patterns: service+city combinations (/charleston-sc/stair-lifts/, /charleston-sc/wheelchair-lifts/, /hilton-head/stair-lift/, /hilton-head/wheelchair-lift/, /hilton-head/stair-lift-repair/, /bluffton-sc/stair-lift-installer/, /bluffton-sc/wheelchair-lift-repair/, /charleston/stair-lift/), old city roots (/charleston-sc/, /beaufort-sc/, /hilton-head/, /bluffton-sc/), /stair-lift-installer/<city>/ (5 SC), the /stair-lift-installer/ hub, /service-area/mt-pleasant-sc/ (duplicate of /service-area/mount-pleasant-sc/) and the sub-service page /services/straight-stair-lifts/ (Paul: consolidate into the parent). 7 are crawled (internally linked, including the straight page); 12 are in the CMS/XML sitemap only; /charleston/stair-lift/ appears only in backlink data. DataforSEO shows 0 cannibalization clusters (no two URLs ranking for one query). | 20 | No cannibalization finding (RULE-005: overlap without observed conflict). Each URL is recorded in the URL Decision Map with its CM-019 check: 14 pass C1-C3 and wait only for client confirmation of no leads (C4, Q1) before becoming a 301 candidate for Paul; 6 fail C1/C2/C3 and stay Needs Evidence - no destructive recommendation (safer alternative: keep live, strip discontinued/DME claims, de-link). Never delete; 301 only (Paul 2026-10-06). Expected impact: one URL per city and per service once evidence allows. | Paul decides; Jonie (redirect handoffs) | Yes | Yes | 1 |
| F-014 | High | 5 Architecture (BB-201; analysis-rules section 5 new-page test) | Repair and maintenance of any stair lift or lift is a confirmed service (Brand Guide D Services; Paul 2026-10-07) with no service page. Repair intent is served only by two service+city pages: /bluffton-sc/wheelchair-lift-repair/ (7 keywords in the top 100, best #34; "wheelchair lift repair" vol 320 at #48) and /hilton-head/stair-lift-repair/ (CMS/sitemap only, not crawled). People Also Ask returns repair questions ("How much does it cost to repair a stair lift?", "How often should a stairlift be serviced?") routed to a repair service page. The approved site plan names /services/stair-lift-repair/. | 3 | Create /services/stair-lift-repair/ in Build (svc1) to the service spec; only after it exists can the two repair URLs be checked as merge candidates (both Needs Evidence now; the Bluffton one ranks). Expected impact: a home for repair/maintenance intent that the current service set lacks. | Build | No | No | 1 |
| F-015 | High | 5 Architecture; 3 Brand & entity (CM-019) | 17 Florida and Michigan pages (6 FL, 11 MI) are published in the CMS (status Publish) and listed in the XML page-sitemap, but no internal link points to them (not reached by the crawl). DataforSEO shows 0 ranking keywords and 0 referring domains for every one; none is a GBP or tracked citation destination. Live HTTP status was not checked. Florida and Michigan are not served (Decision 010; Paul 2026-10-06: drop, 301 not 410). | 17 | Sitemap removal for these 17 URLs is carried by F-035 (one finding per issue; exclusion must not set noindex). After the client confirms no leads (C4, Q1) they become 301 candidates for Paul to a target he chooses (Q2; proposed default /services/stair-lifts/ - the pages are stair-lift-installer pages; never blanket to an unrelated page). Never 410 (Paul). VA confirms live status first (Q6). Expected impact: the site stops presenting out-of-area cities to search engines. | Jonie (sitemap + redirect handoffs) after Paul | Yes | Yes | 2 |
| F-016 | High | 5 Architecture (SVC-16; BB-205, BB-314) | Each service page links to only 4 of the 24 SC location pages (/service-area/hardeeville-sc/, /service-area/ladys-island-sc/, /service-area/ridgeland-sc/, /service-area/walterboro-sc/), plus Georgia pages (/service-area/savannah-ga/, /pooler-ga/, /rincon-ga/), redirecting stubs (/service-area/beaufort-sc-2/, /bluffton-sc-2/, /charleston-sc-2/, /hilton-head-sc/) and the duplicate /service-area/mt-pleasant-sc/. | 5 | In the service rebuilds (svc1), the service-areas H2 links (H3) to every location page; rows are left as Finish placeholders (CM-005). Expected impact: every location page is associated with every service. DRAFT spec - advisory. | Build / Finish | No | No | 1 |
| F-017 | High | 5 Architecture (LOC-18; BB-205, BB-315; CM-022) | Each SC location page links to 9-10 of its 23 sibling location pages - only the cities of its own metro cluster (e.g. /service-area/beaufort-sc/ links Beaufort-area cities; /service-area/charleston-sc/ links Charleston-area cities); /service-area/ladys-island-sc/ links 3 siblings plus Georgia pages and redirect stubs. Hardeeville and Ridgeland are linked through redirecting "-2" URLs. | 24 | Each location rebuild carries a sibling-cities section linking every other location page (Finish placeholders). Expected impact: full city mesh across the area entity. DRAFT spec - advisory. | Build / Finish | No | No | 1 |
| F-022 | High | 6 On-page (SVC-05, LOC-04, HUB-05; COM-04; RULE-002) | 54 of the 96 crawled 200 pages have no H1: all 5 service pages, all 24 SC location pages, the 3 hubs, /services/, /terms-conditions/, and 20 Georgia/legacy pages. On the location pages the first H2 repeats the SEO title string including the brand (e.g. "Stair Lift Installation in Beaufort, SC \| Home Mobile Medical"), i.e. the visible main heading is marked up as H2 (COM-04). One H1 per page is a house standard (RULE-002), not a platform requirement. | 54 | Every rebuilt page gets exactly one H1 in the spec format (no brand); no interim edit of these legacy pages is needed since all are scheduled for rebuild. None of the affected pages ranks top 3 for its main keyword, so the CM-020 H1 lock does not apply. Expected impact: each page states its primary entity in the H1. DRAFT specs - advisory. | Build | No | No | 1 |
| F-023 | High | 6 On-page (LOC-02; BB-301/302) - High (wrong title entity order) | All 24 SC location titles lead with a service phrase: 22 read "Stair Lift Installation in <City>, SC \| Home Mobile Medical" (brand last); /service-area/folly-island-sc/ uses that pattern but names Folly Beach (F-007); /service-area/ladys-island-sc/ reads "Medical Equipment In Lady's Island, SC" (no brand at all). None carries the GB category; all abbreviate the state. Spec format: Brand - GB Category - City, Full State Name (RULE-003 brand-led location pages). The 9 Georgia location pages use the same pattern (held for microsite). Rev 1 said all 24 end with the brand; Lady's Island does not. | 24 | Retitle each location page to the spec format in its rebuild (structural change, handoff). Expected impact: brand-led location titles that name the category entity and the city with the full state name. DRAFT spec - advisory. | Build -> Jonie | No | No | 2 |
| F-032 | High | 3 Brand & entity (BLG-19, BLG-16; CM-025, CM-040, CM-016) | Posts make coverage, tax, legal, health and product-spec claims with no named authoritative source recorded: Medicare/Medicaid/insurance coverage of stair lifts (two posts; the larger ranks #2 for "will medicare pay for a stairlift"), tax deductibility, ADA compliance, semaglutide side effects (a drug-health claim), long-term care, weight limits, battery/power and outdoor use, and prices ("Straight stairlifts range from $2,000 to $5,000 on average. Curved or outdoor stairlifts can range from $8,000 to $15,000..."). | 10 | No disposition change now - posts stay as-is until the Blog Decision Map (Paul 2026-10-07). When each is handled: rewrite only from Medicare.gov/CMS, IRS Publication 502, ADA.gov/US Access Board and manufacturer spec sheets; prices only from client-confirmed figures (CM-016); Paul approves with human review recorded (CM-025). Expected impact: coverage/health statements become sourced or are removed. | Blog agent -> Paul | No | Yes | 1 |
| F-004 | Medium | 3 Brand & entity (HP-18, LOC-19, BB-504) | The site publishes a second address, "106 Arrow Road, Hilton Head, SC 29928": (a) an outbound Google Maps directions link (SRC-001 row 12: 1 inlink, crawl depth 2, so it sits on one page at crawl depth 1 - not the homepage, which is depth 0, and not the site-wide footer, which would give ~96 inlinks); (b) the /service-area/beaufort-sc/ closing copy (Brand Guide D2; body text is not in the crawl exports). The confirmed NAP is "Home Mobile Medical - 2127 Boundary St #5, Beaufort, SC 29902 - (843) 476-1329" (Brand Guide F). The MANUAL entity profile (2026-09-18) also lists 106 Arrow Road as the "Headquarters". Rev 1 listed the homepage as affected; the evidence does not support that. | 2 | VA (Jonie) locates the page carrying the 106 Arrow Road directions link (a depth-1 page, i.e. one linked from the homepage or navigation) and removes the link (content fix after audit_approved); the Beaufort closing-copy address goes in the Beaufort rebuild. The footer keeps the GBP address per Paul 2026-10-06 (SAB, no walk-in wording). Expected impact: one consistent NAP across site, GBP and citations. | Jonie (handoff) | No | Yes | 2 |
| F-006 | Medium | 3 Brand & entity (HP-21, LOC-25, SVC-19; CM-016) | Claims not supported by Brand Guide Section D appear on live pages: homepage "Our experienced technicians..."/"skilled professionals" (Section D: Jason plus one helper) and three placeholder testimonials (Paul: placeholders, remove); Beaufort page "Every lift is custom-fit to your staircase..." and "All of our stair lifts come with battery backup systems..."; /services/wheelchair-lifts/ "...guaranteeing your lift blends seamlessly with your surroundings" (Section D: guarantees none); /service-area/ "...extend our reach to guarantee mobility and independence for all"; /bluffton-sc/wheelchair-lift-repair/ meta "Our experienced technicians will fix your lift quickly...". (The rentals claim is in F-003; the safety claims in F-005.) | 5 | Rewrite each claim to the Section D wording during Build (technicians -> "Jason and his helper"; custom-fit -> "fitted to your staircase"; remove placeholder testimonials; drop "all ... battery backup" unless manufacturer spec sheets cover every model; remove guarantee wording). Expected impact: every on-page claim traces to Section D (CM-016). | Build writer -> Paul | No | Yes | 1 |
| F-007 | Medium | 3 Brand & entity (LOC-03 / LOC-06 city naming) | The Folly Island page names two different places: title "Stair Lift Installation in Folly Beach, SC \| Home Mobile Medical", meta "...stair lift installation in Folly Beach, SC...", city map embed q=Folly Beach, SC, while the H2-1 reads "Stair Lift Installation in Folly Island, SC \| Home Mobile Medical" and the URL slug is folly-island-sc. Paul set the location name as Folly Island (Brand Guide C2; 2026-10-07). | 1 | Use "Folly Island" consistently (title, meta, H1, map) in the location rebuild. Expected impact: one unambiguous city entity per page. | Build | No | No | 1 |
| F-008 | Medium | 3 Brand & entity; 6 On-page (LOC-24 copied content) | The Yemassee page's first H2 reads "Stair Lift Installation in Port Royal, SC \| Home Mobile Medical" (the CMS excerpt opens with the same Port Royal heading) while its title, meta, slug and second H2 name Yemassee. | 1 | Correct in the Yemassee rebuild; until then a one-line content fix after audit_approved. Expected impact: the page names only its own city. | Build / Jonie | No | No | 1 |
| F-009 | Medium | 4 GBP & local; 3 Brand & entity (CM-004, CM-027; HP-13 input) | The Google listing shows 2.9 stars from 19 reviews (pulled 2026-10-07). All reviews date 2017 to 2023-03; they describe a walk-in medical-supply/rental store (wheelchair and lift-chair rentals, a breathing machine, mastectomy products, compression socks); none mentions stair lifts, porch lifts, wheelchair lifts or lift repair; ten are 1-star. Two reviews tie the listing to the former business: 2022-11-02 "The staff of Beaufort Medical is awsome" and 2022-09-26 "I had to rent a lift chair ... Jason was so nice". The live post /embracing-a-new-era-from-beaufort-medical-equipment-to-home-mobile-medical/ is titled "Home Mobile Medical: Our Evolution from Beaufort Medical Equipment" and opens "it's important to reflect on our roots. Beaufort Medical Equipment started with...". Brand Guide D History (Client Confirmed) says Beaufort Medical Equipment was sold and Home Mobile Medical is not a rebrand of it. The listing evidence and the live post are in tension with that approved fact; this review does not resolve it (PROC-02: evidence that contradicts itself goes to a conflicts record). Brand Guide D "Google rating and review count" is Unknown [NEED]. | 1 | Before any review plan or GBP change, Paul asks the client to confirm the listing's history: was this GBP the Beaufort Medical Equipment listing, renamed, and who owns it after the sale? Official platform guidance decides what the listing may keep (RULE-006); the answer either corrects Brand Guide D History or explains the reviews. Then record the rating and count in Brand Guide D with the date (CM-027); show no rating bar on the site until then (HP-13); any review plan from lift customers stays within Google's review policy (no gating or incentives). The rebrand framing of the blog post is handled in the Blog Decision Map with the client's answer. "The Best" fails CM-020 conditions 3 and 4 on this evidence. Working Hypothesis (labelled): the old-store reviews depress map visibility - validation: grid re-scan after new reviews. Expected impact: the GBP's visible reputation and history describe the current lift business. | Gwen (GBP) / client | Yes | Yes | 2 |
| F-018 | Medium | 5 Architecture (HP-11; BB-201, BB-313 sections 5-6) | The homepage links to 2 of the 4 core service pages (/services/stair-lifts/, /services/wheelchair-lifts/ - both via the site-wide navigation); it does not link to /services/curved-stair-lifts/ or /services/porch-lifts/, and it links to three discontinued service pages through the navigation (F-003). Its two exported H2s are "Stair Lifts Available Throughout The Lowcountry" and "Stair Lift Solutions Tailored to You". | 1 | Homepage rebuild (final1): one services H2 with H3 links to every service page (max 5-6). Expected impact: the brand hub links each service entity. DRAFT spec - advisory. | Build | No | No | 1 |
| F-019 | Medium | 5 Architecture / 6 On-page (HP-16; BB-313 section 13) | The homepage links to none of the 24 location pages (only the three hub pages and the Georgia hub via navigation). | 1 | Add the service-areas grid (cities listed, not H-tagged) in the homepage rebuild. Expected impact: the homepage shows the full area entity. DRAFT spec - advisory. | Build | No | No | 1 |
| F-024 | Medium | 6 On-page (HP-03, SVC-04, LOC-03, ABT-02; CM-014) | Title separators are mixed across the site: 46 titles use a pipe, 1 an em dash, 21 a hyphen, 3 an en dash, and three older service titles use the word "From" ("Stair Lifts From Home Mobile Medical", "Wheelchair Lifts From Home Mobile Medical", "Power Chairs From Home Mobile Medical"). The house separator is a single hyphen (Brand Guide A7). CM-014: consistency is the finding, not the glyph. | 31 | Use the Brand Guide A7 separator on every rebuilt title; check SEOPress title templates when S20 returns. Expected impact: consistent title structure. DRAFT specs - advisory. | Build / Jonie | No | No | 1 |
| F-025 | Medium | 6 On-page (LOC-10, LOC-24; CM-015 portability) | 16 of the 24 SC location pages open with the same sentence frame "Stay safe and independent with professional (or expert) stair lift installation from Home Mobile Medical, your trusted mobility experts serving <City> ..." - portable across siblings with only the city swapped. | 16 | Each rebuilt location opening is unique to its city (verified facts only; [NEED] where missing). Expected impact: openings pass the portability test. DRAFT spec - advisory. | Build | No | No | 1 |
| F-026 | Medium | 3 Brand & entity (HP-06; BB-304, CM-024) - see OPEN audit-local conflict CF-LOCAL-001 (renumbered from CF-001, which is a resolved register entry in rulings.md section E) | Homepage H1 "Enhance Your Independence And Mobility With Our Stair Lift Solutions" uses neither reserved homepage variant (B1: "Mobility equipment supplier", "South Carolina Lowcountry") and names no area. HP-08 / BB-313 section 3 say the homepage H1 is never changed once live. | 1 | Follow the current production rule: no recommendation to change the live homepage H1 (HP-08). Paul rules the conflict CF-LOCAL-001 (Q4). PROC-01 step 4 done: the proposed ruling is filed as methodology/lessons.md L-009 (PROPOSED, 2026-10-08). Paul's 2026-10-08 Apex ruling on the same tension is client-specific and is not applied here. Expected impact if Paul allows a change: the H1 expresses the reserved category and area variants. DRAFT spec - advisory. | Paul | No | Yes | 3 |
| F-029 | Medium | 3 Brand & entity (BLG-05; CM-039, CM-004) | All 21 blog posts are authored by the WordPress user "wittycow"; the blog author must be the owner (Jason Workens, Brand Guide D named staff) unless the client states otherwise. | 21 | Reassign authorship to the owner when each post is handled in the Blog Decision Map (posts stay as-is until then, Paul 2026-10-07). Expected impact: a real, checkable author (CM-004). | Blog agent | No | No | 1 |
| F-030 | Medium | 6 On-page (BLG-03; BB-302, BB-704) | 20 of 21 post titles do not follow "Post Title - Brand": 18 omit the brand; 2 lead with it ("Introducing Home Mobile Medical - Revolutionizing Mobility Solutions", "Home Mobile Medical: Our Evolution from Beaufort Medical Equipment"). Only /costs-and-financing-options-for-stairlift-installation/ follows the format. Rev 1 said 20 omit the brand. | 20 | Apply the format when posts are handled in the Blog Decision Map. Expected impact: brand on every post title. DRAFT spec - advisory. | Blog agent | No | No | 2 |
| F-031 | Medium | 7 Blog (entity scope; BB-701 via the Blog Decision Map) | Four posts sit outside the entity: telemedicine history, long-term care, semaglutide side effects, and mobility-scooter repair (a discontinued service). DataforSEO shows 0 ranking keywords and 0 referring domains for all four. | 4 | Route to the Blog Decision Map (bb-blog-analysis: Test B first, CM-007; CM-021 for any redirect). No disposition change now (Paul 2026-10-07). Expected impact: blog content supports the lift entity only. | Blog agent | No | Yes | 1 |
| F-010 | Low | 8 Citations & authority | Of 9 active citations in the BrightLocal tracker, names and phone match the confirmed NAP; address format varies: Yelp "2127 Boundary St, Beaufort, SC" (suite #5 missing); Hotfrog ZIP "Not found"; marketersmedia.com and locable.com have no NAP fields recorded; the Chamber of Commerce listing URL sits under /medical-equipment-supplier/ (a broad-DME category signal excluded by Brand Guide A3). | 1 | Gwen corrects the Yelp suite, Hotfrog ZIP and Chamber category to the Brand Guide F NAP/category and confirms the marketersmedia/locable NAP. Expected impact: consistent NAP across citations (BB-504). | Gwen (citations) | No | No | 1 |
| F-011 | Low | 8 Citations & authority (CM-006, RULE-004, RULE-014) | The tracker lists 9 active citations and 30 "Potential" sites not found, including Apple Maps, BBB, MapQuest, Yellow Pages and Manta; it also lists google.com as "Potential" although the GBP exists (tracker matching defect - not a finding). Brand Guide F records Apple Maps as [NEED]. | 1 | No citation order during the audit (RULE-009). Paul decides any citation build per RULE-014 (provider, cost, renewal, duplicate plan) after NAP/GBP facts are reconciled; Apple Maps is the first gap (also a Finish schema input). Expected impact: wider NAP corroboration. Quantity is a planning benchmark, not a Google requirement (CM-006). | Gwen / Paul | No | Yes | 1 |
| F-012 | Low | 8 Citations & authority (CM-006) | DataforSEO shows 708 referring domains (717 backlinks, 694 dofollow) to the homepage; only 8 referring domains have a spam score of 30 or below; median backlink spam score 55. Four other URLs each have 1 referring domain (storeboard.com -> http homepage; news.marketersmedia.com -> /charleston/stair-lift/, /savannah/stair-lift/, /hilton-head/stair-lift/). | 1 | No removal or disavow recommendation (CM-006: where a client exceeds the link average, stop adding and correct relevance; a disavow would rest on a Working Hypothesis - publication gate). Monitor; Paul may review in Finish. Expected impact: none now; the profile is recorded as a baseline. | Paul (monitor) | No | No | 1 |
| F-020 | Low | 5 Architecture / 6 On-page (HUB-01, HUB-02, HUB-05, HUB-11) - Low at most (county-hub spec DRAFT; metro-hub rule L-008 PROPOSED) | Hub pages: /service-area/charleston/ (161 words) and /service-area/hhi-beaufort/ (175 words) carry little more than a link list; /service-area/ has 795 words. None has an H1. Titles: "Service Area", "Charleston Service Area - Home Mobile Medical", "Hilton Head & Beaufort, SC Service Area \| Home Mobile Medical" (no GB category, brand last). /service-area/hhi-beaufort/ omits Lady's Island and links Hardeeville and Ridgeland via redirecting "-2" URLs; /service-area/charleston/ also links Walterboro; /service-area/ links no location page. | 3 | Rebuild each hub in its location batch once Paul rules L-008 and approves the county-hub spec; give each real area substance (BB-207). Expected impact: hubs stop being thin link lists. Low - DRAFT spec and PROPOSED hub rule. | Build | No | Yes | 1 |
| F-021 | Low | 5 Architecture (page type questioned - no spec) | /services/ is a services hub (title "Mobility Devices \| Home Mobile Medical", 980 words, no H1). No page spec in methodology/specs covers a services hub; Brand Guide C1 lists it as "Services hub - Planned (rewrite)". | 1 | Paul decides whether /services/ gets a spec (or follows the homepage services-section pattern) before it is rebuilt; content scope per F-003. Expected impact: the hub has a defined role. Low - no spec to fail. | Paul | No | Yes | 1 |
| F-027 | Low | 6 On-page (ABT-01; BB-302) - Low at most: "Area Category" meaning is a Coastal default (about.md element 2) | About page title "About Us - Home Mobile Medical" lacks the area/category part of the spec format "About Brand - Area Category". | 1 | Retitle in the about rebuild (final2) once Paul confirms the "Area Category" meaning. Expected impact: the about title carries the entity. Low - Coastal default; DRAFT spec - advisory. | Build | No | No | 2 |
| F-028 | Low | 6 On-page (ABT-04; BB-304) - Low at most: H1 format is a Coastal default (about.md element 4) | About page H1 is "About us" - no category or area variant. | 1 | Use a B2-pool variant H1 in the about rebuild once Paul rules the about H1 format. Expected impact: the about H1 names the entity. Low - Coastal default; DRAFT spec - advisory. | Build | No | No | 2 |
| F-033 | Low | 2 Technical & crawl | Internal links point at redirecting URLs: /equipment-rentals/ (from 3 pages); /service-area/beaufort-sc-2/ (from 10 pages); /service-area/bluffton-sc-2/ (from 10 pages); /service-area/charleston-sc-2/ (from 10 pages); /service-area/hardeeville-sc-2/ (from 18 pages); /service-area/hilton-head-sc/ (from 10 pages); /service-area/ridgeland-sc-2/ (from 18 pages); /services/stair-lift/ (from 8 pages). The redirects /service-area/bluffton-sc-2/, /service-area/charleston-sc-2/ and /service-area/beaufort-sc-2/ each take two hops (to the slash-less URL, then to the final URL). | 36 | Point internal links at the final URLs; repoint the three "-2" redirects straight to the canonical slash URL (one hop). Most links disappear with the Build rebuilds; the redirect repoint is a VA handoff. Expected impact: cleaner crawl paths. | Jonie | No | No | 2 |
| F-034 | Low | 2 Technical & crawl | /services/stair-lift/ (a service-pattern URL) 301-redirects to the legacy city page /hilton-head/stair-lift/, which is itself Needs Evidence (CM-019 C2/C3 fail). | 1 | Revisit the target when /hilton-head/stair-lift/ is decided; /services/stair-lifts/ is the natural target. Changing a redirect target is a structural handoff (Paul). Expected impact: the service URL resolves to the service page. | Jonie | No | Yes | 1 |
| F-035 | Low | 2 Technical & crawl (orphan candidates - reconciled) | The XML page-sitemap lists 37 URLs that no crawled page links to (orphan candidates): Florida/Michigan pages, /stair-lift-installer/*, Georgia /savannah-ga/* pages, /hilton-head/*, /charleston-sc/, /beaufort-sc/, /power-chairs/, /about-us-across-the-web/ and /bluffton-sc/stair-lift-installer/. Reconciled against CMS (all published), DataforSEO rankings/backlinks (2 rank: /savannah-ga/, /bluffton-sc/stair-lift-installer/), GBP (homepage only) and citations. | 37 | Remove from the XML sitemap (VA handoff - SEOPress settings are handoffs) the 29 URLs that pass CM-019 C1-C3 and are headed for retirement: the 17 FL/MI URLs (F-015), /stair-lift-installer/ and /stair-lift-installer/{walterboro, ladys-island, mt-pleasant, hardeeville, ridgeland}/, /beaufort-sc/, /charleston-sc/, /hilton-head/, /hilton-head/wheelchair-lift/, /hilton-head/stair-lift-repair/ and /power-chairs/. The exclusion must not change meta robots: if SEOPress can only drop a URL from the sitemap by setting noindex, that is a noindex (destructive, CM-019) and waits with the rest of the URL's disposition. Leave unchanged: the 6 Georgia URLs (/savannah-ga/ and its 3 children, /stair-lift-installer/pooler/, /stair-lift-installer/rincon/ - Hold, no action on this site now, Paul), /bluffton-sc/stair-lift-installer/ (fails CM-019 C1 - Q3) and /about-us-across-the-web/ (Q6 and the Finish ID-page decision). Removing from the sitemap does not delete pages. URL dispositions per the URL Decision Map. Expected impact: the sitemap lists only canonical, in-area pages, without pre-empting Paul's Georgia and value-URL decisions. | Jonie | No | Yes | 2 |
| F-036 | Low | 6 On-page / 2 Technical (meta descriptions; WC-C2) | Meta descriptions: 12 pages have none (blog index, category and pagination archives); 20 exceed 160 characters (legal pages, /contact/ 288, /about/ 328, /service-area/charleston/ 327, costs post 321 - several are truncated body text); the service pages /services/curved-stair-lifts/, /services/porch-lifts/, /services/straight-stair-lifts/ and /services/scooter-lifts/ describe the service "in Hilton Head, SC" rather than the area entity. | 35 | Rebuilt pages get spec meta descriptions; for kept utility/blog pages, fix in the batched Low handoff (meta descriptions are a safe fix after audit_approved). Expected impact: accurate snippets naming the area. | Jonie | No | No | 1 |
| F-037 | Low | 2 Technical & crawl (outbound links) | Outbound links return errors: https://summervilledream.org/farmers-market/ (404, SRC-001 row 119); https://parks.chathamcountyga.gov/CommunityParks/TomTriplett (404, SRC-001 row 130); https://parks.chathamcountyga.gov/BoatRampsAndFishingPiers/TybeeIslandFishingPierAndPavilion (404, SRC-001 row 133); https://visittybee.com/article/guide-to-back-river-beach (403, SRC-001 row 137); https://home.army.mil/stewart/about/Garrison/hunter-army-airfield (404, SRC-001 row 146); https://www.niche.com/places-to-live/bluffton-beaufort-sc/ (403, SRC-001 row 150); https://www.suncityhiltonhead.org/ (502, SRC-001 row 168); https://www.farmersmarketbluffton.org/ (Connection Timeout, SRC-001 row 173). The export gives the inlink count, not the source page; by subject the sources are the Summerville, Bluffton and Hilton Head Island location pages and Georgia pages (held). | 1 | VA re-checks and replaces/removes dead outbound links on SC pages (safe fix: broken links) - or the rebuilds drop them; ignore Georgia pages (held). Expected impact: no dead links in Things to Do/Top Sites sections. | Jonie | No | No | 1 |
| F-038 | Low | 2 Technical & crawl | Two published CMS pages of unclear purpose are not linked internally: /new-homepage/ (CMS page "New Homepage", published 2026-09-10, not in the sitemap) and /about-us-across-the-web/ (in the sitemap; a list of directory names). Live status and robots directives unknown. The /new-homepage/ CMS excerpt opens "Locally owned - Beaufort, SC - Free in-home estimates The Best Stair Lift Installation in the Lowcountry ... installs stair lifts, wheelchair lifts and mobility ramps": if live and indexable it would carry a "The Best" opener with no CM-020 decision (Brand Guide H2 empty; proof fails at 2.9 stars / 19 reviews; sensitive client) and a discontinued service (mobility ramps - Brand Guide D Not offered). | 2 | VA checks HTTP status and robots for both (Q5). If /new-homepage/ is live and indexable, it is a duplicate homepage carrying unapproved claims: Paul decides, and any noindex/redirect is destructive (CM-019); severity is re-set after Q5. /about-us-across-the-web/ is reviewed in Finish as a possible sameAs/ID-page input. Expected impact: no duplicate homepage in the index. | Jonie (check) / Paul | No | Yes | 2 |
| F-039 | Low | 2 Technical / 7 Blog | 11 category and pagination archives are indexable ("index, follow"), have no meta description and 38-282 words; categories include off-entity topics (Telemedicine, Long Term Care, Health). | 11 | Handle with the blog in the Blog Decision Map (taxonomy cleanup; any noindex is destructive -> CM-019). No change now. Expected impact: archives stop adding thin, off-entity pages. | Blog agent | No | Yes | 1 |
| F-040 | Low | 1 Baseline & measurement | A GA4 tag (gtag.js?id=G-5GX2RP9PYX) and WordPress.com stats are loaded, but no GA4, GSC, call-tracking or form-delivery access exists for this audit; the conversion path (phone, form, upcoming photo-quote upload) is unvalidated. | 1 | Paul asks the client for GA4/GSC read access (or a VA check that forms deliver) before Build launches; measurement plan in the S18 package. Expected impact: a baseline to judge the rebuild. | Paul | Yes | Yes | 1 |

## Detail per finding

### F-001 - High - 3 Brand & entity (HP-02); 6 On-page (HP-01)

- **Observation:** Homepage SEO title is "Home Mobile Medical — Home Medical Equipment — South Carolina Lowcountry"; the category slot reads "Home Medical Equipment". The GBP primary category entity is "Mobility equipment supplier" (Brand Guide A2). The homepage meta description reads "Stair lift installation and home medical equipment across the Lowcountry...". Title order (brand, category, area) is correct; the category term is not the GBP category or an approved variant (Brand Guide A3 excludes "medical equipment supplier").
- **Evidence / Locator:** SRC-008 page_titles_all row 2; SRC-007 meta_description_all row 2; SRC-025 Brand Guide A2/A3
- **Classification:** Bradley Methodology Rule (BB-105, BB-106, BB-301/302) + Project Evidence
- **Confidence:** Corroborated (SRC-008 and SRC-005 javascript_all HTML Title agree)
- **Alternative Explanation:** The title may have been set before the 2026-10-02 category decision (Decision 038) and never revisited.
- **Alternative tested:** Checked SRC-010 CMS modified date for "/" (2026-09-10): page edited after the decision, title unchanged.
- **Recommendation:** Rebuild the homepage title to the Brand - GB Category - Area Entity format with the approved category entity, in the homepage batch (final1). Expected impact: the brand hub stops signalling broad home-medical-equipment (the discontinued DME entity) and matches the GBP category. Title changes are structural (handoff to Jonie; structural_changes_allowed is met).
- **Risk if Acted:** Low - the homepage ranks for no lift/area keyword in the top 3 (SRC-022); off-entity DME rankings (e.g. "carolina home medical" #60) may fall, which is consistent with the entity cleanup.
- **Risk if Deferred:** The homepage keeps telling Google the business is a home medical equipment store, contradicting the GBP category and the service pages.
- **Dependency:** Build homepage batch (final1); title change is a VA handoff (CLAUDE.md section 4)
- **Publication gate:** n/a
- **Affected:** /
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-002 - High - 3 Brand & entity; 5 Architecture

- **Observation:** The site-wide navigation/footer on all 102 pages in the link-level export links to the Georgia hub /service-area/savannah/ (SF Unique Inlinks = 96 on that URL). Every service page links to /service-area/savannah-ga/, /service-area/pooler-ga/ and /service-area/rincon-ga/. Nine Georgia city pages (titles "Stair Lift Installation in <City>, GA | Home Mobile Medical") are indexable (meta robots "index, follow"), self-canonical and listed in the XML sitemap. /service-area/georgetown-ga/ links out to georgetown-mi.gov (Michigan). The approved area entity is South Carolina Lowcountry (Brand Guide A5) and Georgia is served only from a separate microsite (Brand Guide E, H; Paul 2026-10-06).
- **Evidence / Locator:** SRC-020 LNKD Anchor_Text (target /service-area/savannah/ present on every source page; service-page sources -> GA targets); SRC-004 internal_all row 63 (Unique Inlinks 96); SRC-008 rows for GA pages; SRC-011 page-sitemap; SRC-001 external_all row 139; SRC-025 Brand Guide A5, E, H
- **Classification:** Client Constraint (Georgia on microsite, Paul 2026-10-06) + Project Evidence
- **Confidence:** Corroborated (LNKD link export and SF inlink counts agree)
- **Alternative Explanation:** Georgia links may be intentional cross-promotion until the microsite exists.
- **Alternative tested:** Paul's decision record (2026-10-06 12:01 and 12:05 entries) states Georgia comes off homemobilemedical.com entirely; no exception recorded.
- **Recommendation:** Per Paul's decision: do NOT redirect any Georgia URL to an SC page; all 18 Georgia URLs are "Hold - microsite" in the URL Decision Map (301 to the equivalent microsite page once it exists, each CM-019-checked). Now: remove the Georgia hub from site navigation and the Georgia links from SC service pages (menu/link changes - non-destructive; menu changes are a Jonie handoff). Expected impact: the site expresses one area entity (South Carolina Lowcountry) that contains every linked city.
- **Risk if Acted:** Georgia pages lose internal links before the microsite exists; /service-area/savannah-ga/ and /savannah-ga/ rank (positions 16-46, SRC-022) and may lose some visibility.
- **Risk if Deferred:** The SC site keeps asserting a two-state service area, diluting the Lowcountry area entity (BB-105) the entity foundation was approved on.
- **Dependency:** Microsite project (separate /new-client); menu handoff to Jonie
- **Publication gate:** n/a
- **Affected:** /service-area/savannah/; /service-area/savannah-ga/; /service-area/pooler-ga/; /service-area/rincon-ga/; /service-area/tybee-island-ga/; /service-area/bloomingdale-ga/; /service-area/port-wentworth-ga/; /service-area/richmond-hill-ga/; /service-area/skidaway-island-ga/; /service-area/georgetown-ga/; /services/stair-lifts/; /services/curved-stair-lifts/; /services/porch-lifts/; /services/wheelchair-lifts/; /services/straight-stair-lifts/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-003 - High - 3 Brand & entity; 5 Architecture

- **Observation:** Live, indexable pages describe services the business does not offer (Brand Guide D "Not offered": broad DME, rentals, power chairs, scooters/scooter lifts, mobility ramps): (a) the site-wide navigation links to /services/power-chairs/, /services/scooter-lifts/ and /services/mobility-ramps/ from every page (SF Unique Inlinks 96 each); (b) /services/ is titled "Mobility Devices | Home Mobile Medical" with meta "From wheelchairs and scooters to lifts and ramps..."; (c) /service-area/mt-pleasant-sc/ and /service-area/ladys-island-sc/ are titled "Medical Equipment In ..."; (d) /bluffton-sc/ H2 "Medical Equipment Sales & Rentals in Bluffton, SC"; (e) /bluffton-sc/wheelchair-lift-repair/ H2 "We Rent and Sell Mobility Equipment in the Lowcountry"; (f) /service-area/hilton-head-island-sc/ meta "installs stair lifts, porch lifts, and scooter lifts"; (g) discontinued service pages /charleston-sc/power-chairs/, /charleston-sc/mobility-ramps/ and post /mobility-scooter-repair-near-me/ are indexable; (h) uncrawled CMS pages /power-chairs/, /beaufort-sc/, /charleston-sc/, /hilton-head/ carry rental/power-chair wording in their CMS excerpts; (i) the Beaufort page states "We rent and sell mobility equipment in the Lowcountry." (Brand Guide D2).
- **Evidence / Locator:** SRC-004 internal_all rows 17/57/61 (Unique Inlinks 96); SRC-008 rows 9, 63, 69; SRC-003 h2_all rows 94, 86; SRC-007 row 60; SRC-010 CMS excerpts (rows 80, 20, 18, 10); SRC-025 Brand Guide D and D2
- **Classification:** Client Constraint (Brand Guide D "Not offered", Decisions 007/008) + Project Evidence
- **Confidence:** Corroborated (SF titles/H2s and CMS excerpts agree; nav corroborated by LNKD)
- **Alternative Explanation:** Some pages may be intended as historical/brand-transition content.
- **Alternative tested:** Paul's decisions list these services as discontinued with no exception; the transition story belongs to the about page/blog (claims list B7).
- **Recommendation:** Remove the discontinued-service links from navigation now (non-destructive, menu handoff). Rewrite the kept pages (/services/, Hilton Head Island, Lady's Island, Beaufort content) in Build to the confirmed services only. URL dispositions are in the URL Decision Map: /services/power-chairs/, /services/scooter-lifts/, /services/mobility-ramps/, /charleston-sc/power-chairs/ and /power-chairs/ pass CM-019 C1-C3 and stay Needs Evidence until the client confirms no leads (C4, Q1) - 301 only, never 410 (Paul 2026-10-06). /charleston-sc/mobility-ramps/, /bluffton-sc/, /bluffton-sc/wheelchair-lift-repair/ and /service-area/mt-pleasant-sc/ FAIL CM-019 C1 (they rank): no destructive recommendation - keep live, strip the discontinued/DME claims, de-link; only a Paul Exception (Q3) could change that. Expected impact: the site stops asserting a DME/rental entity the GBP and Brand Guide no longer represent.
- **Risk if Acted:** Navigation changes remove internal links to pages that may still receive visits; /charleston-sc/mobility-ramps/ ranks (#60, SRC-022) - it stays live (Needs Evidence).
- **Risk if Deferred:** Visitors and search engines keep seeing a broad medical-equipment/rental business; enquiries for services HMM does not offer continue.
- **Dependency:** CM-019 C4 (Q1) for the C1-C3-pass URLs; Q3 for the four C1-fail URLs; Build batches; menu handoff
- **Publication gate:** passed - Client Constraint + Project Evidence, not a Working Hypothesis
- **Affected:** /services/power-chairs/; /services/scooter-lifts/; /services/mobility-ramps/; /services/; /service-area/mt-pleasant-sc/; /service-area/ladys-island-sc/; /bluffton-sc/; /bluffton-sc/wheelchair-lift-repair/; /service-area/hilton-head-island-sc/; /charleston-sc/power-chairs/; /charleston-sc/mobility-ramps/; /mobility-scooter-repair-near-me/; /service-area/beaufort-sc/; /power-chairs/; /beaufort-sc/; /charleston-sc/; /hilton-head/
- **Revision:** 2 (supersedes F-003.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-004 - Medium - 3 Brand & entity (HP-18, LOC-19, BB-504)

- **Observation:** The site publishes a second address, "106 Arrow Road, Hilton Head, SC 29928": (a) an outbound Google Maps directions link (SRC-001 row 12: 1 inlink, crawl depth 2, so it sits on one page at crawl depth 1 - not the homepage, which is depth 0, and not the site-wide footer, which would give ~96 inlinks); (b) the /service-area/beaufort-sc/ closing copy (Brand Guide D2; body text is not in the crawl exports). The confirmed NAP is "Home Mobile Medical - 2127 Boundary St #5, Beaufort, SC 29902 - (843) 476-1329" (Brand Guide F). The MANUAL entity profile (2026-09-18) also lists 106 Arrow Road as the "Headquarters". Rev 1 listed the homepage as affected; the evidence does not support that.
- **Evidence / Locator:** SRC-001 external_all row 12 (Crawl Depth 2, Inlinks 1); SRC-004 internal_all Crawl Depth (/ = 0; /service-area/beaufort-sc/ = 2); SRC-025 Brand Guide F and D2; SRC-026 claims list A5 (Paul: "CONFIRMED - NEEDS REMOVAL"); SRC-019 entity profile section 2
- **Classification:** Bradley Methodology Rule (BB-504) + Client Constraint (Paul A5)
- **Confidence:** Corroborated (SRC-001 and SRC-025/026)
- **Alternative Explanation:** The directions link may be a template leftover from the former business location.
- **Alternative tested:** Paul marked A5 "CONFIRMED - NEEDS REMOVAL"; the cause does not change the remedy.
- **Recommendation:** VA (Jonie) locates the page carrying the 106 Arrow Road directions link (a depth-1 page, i.e. one linked from the homepage or navigation) and removes the link (content fix after audit_approved); the Beaufort closing-copy address goes in the Beaufort rebuild. The footer keeps the GBP address per Paul 2026-10-06 (SAB, no walk-in wording). Expected impact: one consistent NAP across site, GBP and citations.
- **Risk if Acted:** None material - the address is not the business address.
- **Risk if Deferred:** Conflicting NAP undermines entity corroboration (CM-004) and can send customers to the wrong place.
- **Dependency:** VA locates the source page; audit_approved (content fix) or Build rebuild of /service-area/beaufort-sc/
- **Publication gate:** n/a
- **Affected:** /service-area/beaufort-sc/ (closing-copy address, Brand Guide D2); directions link: source page not identified in the exports - one page at crawl depth 1
- **Revision:** 2 (supersedes F-004.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-005 - High - 3 Brand & entity (HP-25, LOC-27; CM-025/CM-040)

- **Observation:** Safety claims without a named authoritative source appear on commercial pages of a health-adjacent client: homepage "Safety is our top priority, and we adhere to the highest standards and regulations."; Beaufort page "...installation meets the highest standards of safety and care." and "...ensure your stair lift is ready for safe use the same day it is installed." (quotes from the 2026-09-18 crawl as recorded in Brand Guide D2).
- **Evidence / Locator:** SRC-025 Brand Guide D2 rows 2, 3, 6; SRC-026 claims list E1, E3, D3. Body text is not in the crawl exports (SF free, no body extraction) - the quotes come from the approved Brand Guide.
- **Classification:** Legal/truth constraint per CM-040 (named source or remove) + Project Evidence
- **Confidence:** Single-source (Brand Guide D2 quoting the crawl; no body-text export to re-verify)
- **Alternative Explanation:** The claims may already have been edited since 2026-09-18.
- **Alternative tested:** Not tested - no later crawl; the CMS modified date for "/" is 2026-09-10 (before the crawl), Beaufort 2025-10-03.
- **Recommendation:** Replace with the Paul-approved safety statement (Brand Guide D: "Safety comes first. Jason holds every installation to the highest industry standards and the manufacturer's installation instructions.") and add "in most cases" to same-day wording; no regulatory-compliance claim (CM-040). Paul approves the page with the human review recorded (CM-025 rule 1). Expected impact: removes an unsupported safety/regulatory claim from a health-adjacent site.
- **Risk if Acted:** None - the replacement wording is Paul-approved.
- **Risk if Deferred:** An unsourced safety/regulation claim stays live (legal/truth risk, CM-040).
- **Dependency:** Paul review recorded (CM-025)
- **Publication gate:** n/a
- **Affected:** /; /service-area/beaufort-sc/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-006 - Medium - 3 Brand & entity (HP-21, LOC-25, SVC-19; CM-016)

- **Observation:** Claims not supported by Brand Guide Section D appear on live pages: homepage "Our experienced technicians..."/"skilled professionals" (Section D: Jason plus one helper) and three placeholder testimonials (Paul: placeholders, remove); Beaufort page "Every lift is custom-fit to your staircase..." and "All of our stair lifts come with battery backup systems..."; /services/wheelchair-lifts/ "...guaranteeing your lift blends seamlessly with your surroundings" (Section D: guarantees none); /service-area/ "...extend our reach to guarantee mobility and independence for all"; /bluffton-sc/wheelchair-lift-repair/ meta "Our experienced technicians will fix your lift quickly...". (The rentals claim is in F-003; the safety claims in F-005.)
- **Evidence / Locator:** SRC-025 Brand Guide D2 rows 4, 5, 7, 8; SRC-010 CMS excerpts rows 7 (/services/wheelchair-lifts/) and 84 (/service-area/); SRC-007 meta_description_all row 86
- **Classification:** Project Evidence + Client Constraint (Brand Guide D/D2)
- **Confidence:** Corroborated for the CMS/meta quotes; Single-source for the D2 body quotes
- **Alternative Explanation:** "Guarantee" may be read as marketing language rather than a warranty claim.
- **Alternative tested:** Brand Guide D records "Guarantees: None" (Client Confirmed); the reading is Paul's call - treated as a claim by default.
- **Recommendation:** Rewrite each claim to the Section D wording during Build (technicians -> "Jason and his helper"; custom-fit -> "fitted to your staircase"; remove placeholder testimonials; drop "all ... battery backup" unless manufacturer spec sheets cover every model; remove guarantee wording). Expected impact: every on-page claim traces to Section D (CM-016).
- **Risk if Acted:** None material.
- **Risk if Deferred:** Unsupported claims stay live; placeholder reviews present as real testimonials.
- **Dependency:** Build batches
- **Publication gate:** n/a
- **Affected:** /; /service-area/beaufort-sc/; /services/wheelchair-lifts/; /service-area/; /bluffton-sc/wheelchair-lift-repair/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-007 - Medium - 3 Brand & entity (LOC-03 / LOC-06 city naming)

- **Observation:** The Folly Island page names two different places: title "Stair Lift Installation in Folly Beach, SC | Home Mobile Medical", meta "...stair lift installation in Folly Beach, SC...", city map embed q=Folly Beach, SC, while the H2-1 reads "Stair Lift Installation in Folly Island, SC | Home Mobile Medical" and the URL slug is folly-island-sc. Paul set the location name as Folly Island (Brand Guide C2; 2026-10-07).
- **Evidence / Locator:** SRC-008 row 47; SRC-007 row 47; SRC-003 row 47; SRC-001 row 92; SRC-025 Brand Guide C2
- **Classification:** Client Constraint (Paul: Folly Island) + Project Evidence
- **Confidence:** Corroborated
- **Alternative Explanation:** Folly Beach is the incorporated city on Folly Island; both names are real (BB-109).
- **Alternative tested:** Paul ruled the name; no further test needed.
- **Recommendation:** Use "Folly Island" consistently (title, meta, H1, map) in the location rebuild. Expected impact: one unambiguous city entity per page.
- **Risk if Acted:** Searchers using "Folly Beach" may match less exactly; Paul accepted that.
- **Risk if Deferred:** Mixed naming weakens the page's city entity.
- **Dependency:** Build Charleston-metro location batch
- **Publication gate:** n/a
- **Affected:** /service-area/folly-island-sc/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-008 - Medium - 3 Brand & entity; 6 On-page (LOC-24 copied content)

- **Observation:** The Yemassee page's first H2 reads "Stair Lift Installation in Port Royal, SC | Home Mobile Medical" (the CMS excerpt opens with the same Port Royal heading) while its title, meta, slug and second H2 name Yemassee.
- **Evidence / Locator:** SRC-003 h2_all row 56; SRC-010 CMS row 95; SRC-008 row 56
- **Classification:** Project Evidence
- **Confidence:** Corroborated (SF H2 and CMS excerpt agree)
- **Alternative Explanation:** Template copied from the Port Royal page without editing the heading.
- **Alternative tested:** The cause does not change the remedy.
- **Recommendation:** Correct in the Yemassee rebuild; until then a one-line content fix after audit_approved. Expected impact: the page names only its own city.
- **Risk if Acted:** None.
- **Risk if Deferred:** The page tells visitors and search engines it is about Port Royal.
- **Dependency:** Build HHI-metro location batch or a content fix
- **Publication gate:** n/a
- **Affected:** /service-area/yemassee-sc/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-009 - Medium - 4 GBP & local; 3 Brand & entity (CM-004, CM-027; HP-13 input)

- **Observation:** The Google listing shows 2.9 stars from 19 reviews (pulled 2026-10-07). All reviews date 2017 to 2023-03; they describe a walk-in medical-supply/rental store (wheelchair and lift-chair rentals, a breathing machine, mastectomy products, compression socks); none mentions stair lifts, porch lifts, wheelchair lifts or lift repair; ten are 1-star. Two reviews tie the listing to the former business: 2022-11-02 "The staff of Beaufort Medical is awsome" and 2022-09-26 "I had to rent a lift chair ... Jason was so nice". The live post /embracing-a-new-era-from-beaufort-medical-equipment-to-home-mobile-medical/ is titled "Home Mobile Medical: Our Evolution from Beaufort Medical Equipment" and opens "it's important to reflect on our roots. Beaufort Medical Equipment started with...". Brand Guide D History (Client Confirmed) says Beaufort Medical Equipment was sold and Home Mobile Medical is not a rebrand of it. The listing evidence and the live post are in tension with that approved fact; this review does not resolve it (PROC-02: evidence that contradicts itself goes to a conflicts record). Brand Guide D "Google rating and review count" is Unknown [NEED].
- **Evidence / Locator:** SRC-024 data/reviews/reviews.csv (19 rows; rows dated 2022-11-02 and 2022-09-26); SRC-008 page_titles_all (post title); SRC-010 CMS excerpt for /embracing-a-new-era-from-beaufort-medical-equipment-to-home-mobile-medical/; SRC-025 Brand Guide D (History; rating Unknown)
- **Classification:** Project Evidence
- **Confidence:** Corroborated for the tension (reviews + live post title + CMS excerpt); Single-source for the rating (DataforSEO Business Data)
- **Alternative Explanation:** Reviews may predate the sale of Beaufort Medical Equipment and belong to the old business that shared the listing.
- **Alternative tested:** Tested against the reviews text and the live post: two reviews name the former business/owner and the post presents HMM as its continuation; whether the listing was transferred cannot be settled from the evidence - client confirmation.
- **Recommendation:** Before any review plan or GBP change, Paul asks the client to confirm the listing's history: was this GBP the Beaufort Medical Equipment listing, renamed, and who owns it after the sale? Official platform guidance decides what the listing may keep (RULE-006); the answer either corrects Brand Guide D History or explains the reviews. Then record the rating and count in Brand Guide D with the date (CM-027); show no rating bar on the site until then (HP-13); any review plan from lift customers stays within Google's review policy (no gating or incentives). The rebrand framing of the blog post is handled in the Blog Decision Map with the client's answer. "The Best" fails CM-020 conditions 3 and 4 on this evidence. Working Hypothesis (labelled): the old-store reviews depress map visibility - validation: grid re-scan after new reviews. Expected impact: the GBP's visible reputation and history describe the current lift business.
- **Risk if Acted:** A review drive done badly can breach Google policy (RULE-006).
- **Risk if Deferred:** The listing keeps presenting the former retail business and a 2.9-star average to every lift prospect.
- **Dependency:** Client confirmation of the GBP history (new question, routed by Paul); then client action; GBP is outside the site (Gwen)
- **Publication gate:** n/a
- **Affected:** GBP "Home Mobile Medical" (2127 Boundary St #5, Beaufort) - https://homemobilemedical.com/
- **Revision:** 2 (supersedes F-009.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-010 - Low - 8 Citations & authority

- **Observation:** Of 9 active citations in the BrightLocal tracker, names and phone match the confirmed NAP; address format varies: Yelp "2127 Boundary St, Beaufort, SC" (suite #5 missing); Hotfrog ZIP "Not found"; marketersmedia.com and locable.com have no NAP fields recorded; the Chamber of Commerce listing URL sits under /medical-equipment-supplier/ (a broad-DME category signal excluded by Brand Guide A3).
- **Evidence / Locator:** SRC-009 BL citation-tracker rows 4 (yelp), 6 (chamberofcommerce), 7 (hotfrog), 8 (marketersmedia), 10 (locable); SRC-025 Brand Guide F NAP
- **Classification:** Project Evidence
- **Confidence:** Single-source (tracker); measured against the Brand Guide F NAP, not the tracker's stored NAP
- **Alternative Explanation:** The tracker may not have parsed suite numbers.
- **Alternative tested:** Not tested - listings not opened (no live checks this session).
- **Recommendation:** Gwen corrects the Yelp suite, Hotfrog ZIP and Chamber category to the Brand Guide F NAP/category and confirms the marketersmedia/locable NAP. Expected impact: consistent NAP across citations (BB-504).
- **Risk if Acted:** Low.
- **Risk if Deferred:** Minor NAP inconsistency persists.
- **Dependency:** None
- **Publication gate:** n/a
- **Affected:** yelp.com, hotfrog.com, chamberofcommerce.com, news.marketersmedia.com, home-mobile-medical.locable.com
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-011 - Low - 8 Citations & authority (CM-006, RULE-004, RULE-014)

- **Observation:** The tracker lists 9 active citations and 30 "Potential" sites not found, including Apple Maps, BBB, MapQuest, Yellow Pages and Manta; it also lists google.com as "Potential" although the GBP exists (tracker matching defect - not a finding). Brand Guide F records Apple Maps as [NEED].
- **Evidence / Locator:** SRC-009 rows 11-40 (Status "Potential"); SRC-025 Brand Guide F
- **Classification:** Bradley Methodology Rule (planning benchmark, CM-006) + Project Evidence
- **Confidence:** Single-source
- **Alternative Explanation:** Some listings may exist under the old Beaufort Medical Equipment name (excluded by Brand Guide F).
- **Alternative tested:** Not tested.
- **Recommendation:** No citation order during the audit (RULE-009). Paul decides any citation build per RULE-014 (provider, cost, renewal, duplicate plan) after NAP/GBP facts are reconciled; Apple Maps is the first gap (also a Finish schema input). Expected impact: wider NAP corroboration. Quantity is a planning benchmark, not a Google requirement (CM-006).
- **Risk if Acted:** Spend without a duplicate plan can create conflicting listings (old BME name).
- **Risk if Deferred:** Thin citation corroboration continues.
- **Dependency:** RULE-014 approval
- **Publication gate:** n/a
- **Affected:** Citation profile - Home Mobile Medical
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-012 - Low - 8 Citations & authority (CM-006)

- **Observation:** DataforSEO shows 708 referring domains (717 backlinks, 694 dofollow) to the homepage; only 8 referring domains have a spam score of 30 or below; median backlink spam score 55. Four other URLs each have 1 referring domain (storeboard.com -> http homepage; news.marketersmedia.com -> /charleston/stair-lift/, /savannah/stair-lift/, /hilton-head/stair-lift/).
- **Evidence / Locator:** SRC-023 DFS backlinks csv rows 2-6
- **Classification:** Project Evidence
- **Confidence:** Single-source
- **Alternative Explanation:** Spam scores are a third-party estimate, not a Google signal.
- **Alternative tested:** Not tested.
- **Recommendation:** No removal or disavow recommendation (CM-006: where a client exceeds the link average, stop adding and correct relevance; a disavow would rest on a Working Hypothesis - publication gate). Monitor; Paul may review in Finish. Expected impact: none now; the profile is recorded as a baseline.
- **Risk if Acted:** A disavow without evidence could remove useful links.
- **Risk if Deferred:** None material.
- **Dependency:** None
- **Publication gate:** blocked for any disavow - Working Hypothesis only
- **Affected:** /
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-013 - High - 5 Architecture (SVC-01, LOC-01; BB-202/203/204; CM-001, CM-019)

- **Observation:** 20 SC URLs duplicate the intent of a canonical service or location page through legacy patterns: service+city combinations (/charleston-sc/stair-lifts/, /charleston-sc/wheelchair-lifts/, /hilton-head/stair-lift/, /hilton-head/wheelchair-lift/, /hilton-head/stair-lift-repair/, /bluffton-sc/stair-lift-installer/, /bluffton-sc/wheelchair-lift-repair/, /charleston/stair-lift/), old city roots (/charleston-sc/, /beaufort-sc/, /hilton-head/, /bluffton-sc/), /stair-lift-installer/<city>/ (5 SC), the /stair-lift-installer/ hub, /service-area/mt-pleasant-sc/ (duplicate of /service-area/mount-pleasant-sc/) and the sub-service page /services/straight-stair-lifts/ (Paul: consolidate into the parent). 7 are crawled (internally linked, including the straight page); 12 are in the CMS/XML sitemap only; /charleston/stair-lift/ appears only in backlink data. DataforSEO shows 0 cannibalization clusters (no two URLs ranking for one query).
- **Evidence / Locator:** SRC-004 internal_all; SRC-010 CMS; SRC-011 sitemap; SRC-022 cannibalization.csv (0 rows) and url-rankings.csv; SRC-023 backlinks; URL Decision Map rows (ext_cm019_* columns)
- **Classification:** Bradley Methodology Rule (BB-202/203/204) for construction; destruction governed by CM-019 (Project Evidence)
- **Confidence:** Corroborated (crawl + CMS + sitemap)
- **Alternative Explanation:** Some legacy pages may carry unique local content worth keeping.
- **Alternative tested:** Checked rankings and links per URL: 6 of the 20 hold rankings or links (CM-019 C1/C2 fail): /bluffton-sc/, /bluffton-sc/wheelchair-lift-repair/, /bluffton-sc/stair-lift-installer/, /service-area/mt-pleasant-sc/, /hilton-head/stair-lift/, /charleston/stair-lift/.
- **Recommendation:** No cannibalization finding (RULE-005: overlap without observed conflict). Each URL is recorded in the URL Decision Map with its CM-019 check: 14 pass C1-C3 and wait only for client confirmation of no leads (C4, Q1) before becoming a 301 candidate for Paul; 6 fail C1/C2/C3 and stay Needs Evidence - no destructive recommendation (safer alternative: keep live, strip discontinued/DME claims, de-link). Never delete; 301 only (Paul 2026-10-06). Expected impact: one URL per city and per service once evidence allows.
- **Risk if Acted:** Redirecting a URL with unseen leads loses enquiries - that is what C4 guards.
- **Risk if Deferred:** Duplicate patterns keep splitting signals and confuse the page-type model; legacy pages keep DME claims (F-003).
- **Dependency:** Q1 (C4 client confirmation); Q3 for the 6 value URLs; F-014 (repair page) for the two repair URLs
- **Publication gate:** passed - Project Evidence (DataforSEO); no Working Hypothesis relied on
- **Affected:** /charleston-sc/stair-lifts/; /charleston-sc/wheelchair-lifts/; /charleston-sc/; /beaufort-sc/; /hilton-head/; /hilton-head/wheelchair-lift/; /hilton-head/stair-lift/; /hilton-head/stair-lift-repair/; /bluffton-sc/; /bluffton-sc/stair-lift-installer/; /bluffton-sc/wheelchair-lift-repair/; /service-area/mt-pleasant-sc/; /charleston/stair-lift/; /stair-lift-installer/; /stair-lift-installer/walterboro/; /stair-lift-installer/ladys-island/; /stair-lift-installer/mt-pleasant/; /stair-lift-installer/hardeeville/; /stair-lift-installer/ridgeland/; /services/straight-stair-lifts/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-014 - High - 5 Architecture (BB-201; analysis-rules section 5 new-page test)

- **Observation:** Repair and maintenance of any stair lift or lift is a confirmed service (Brand Guide D Services; Paul 2026-10-07) with no service page. Repair intent is served only by two service+city pages: /bluffton-sc/wheelchair-lift-repair/ (7 keywords in the top 100, best #34; "wheelchair lift repair" vol 320 at #48) and /hilton-head/stair-lift-repair/ (CMS/sitemap only, not crawled). People Also Ask returns repair questions ("How much does it cost to repair a stair lift?", "How often should a stairlift be serviced?") routed to a repair service page. The approved site plan names /services/stair-lift-repair/.
- **Evidence / Locator:** SRC-025 Brand Guide C1 and D; SRC-022 ranked-keywords.csv rows for /bluffton-sc/wheelchair-lift-repair/; SRC-027 data/paa/paa-routing.md rows 3, 8, 12, 13; build/Home Mobile Medical - Site Plan - IMPORTED.md (svc-repair-maintenance)
- **Classification:** Client Constraint (confirmed service) + Project Evidence
- **Confidence:** Corroborated
- **Alternative Explanation:** Repair could be covered as a section of each lift page instead.
- **Alternative tested:** The new-page test passes: distinct intent (repair vs purchase), truthful service, business value, an architecture role; Paul's site plan already chose a page.
- **Recommendation:** Create /services/stair-lift-repair/ in Build (svc1) to the service spec; only after it exists can the two repair URLs be checked as merge candidates (both Needs Evidence now; the Bluffton one ranks). Expected impact: a home for repair/maintenance intent that the current service set lacks.
- **Risk if Acted:** Overlap with the Bluffton page until its disposition is decided - monitor with DataforSEO (CM-021-style observed evidence).
- **Risk if Deferred:** A confirmed revenue service keeps no canonical page.
- **Dependency:** Build svc1
- **Publication gate:** n/a
- **Affected:** /services/stair-lift-repair/ (to create); /hilton-head/stair-lift-repair/; /bluffton-sc/wheelchair-lift-repair/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-015 - High - 5 Architecture; 3 Brand & entity (CM-019)

- **Observation:** 17 Florida and Michigan pages (6 FL, 11 MI) are published in the CMS (status Publish) and listed in the XML page-sitemap, but no internal link points to them (not reached by the crawl). DataforSEO shows 0 ranking keywords and 0 referring domains for every one; none is a GBP or tracked citation destination. Live HTTP status was not checked. Florida and Michigan are not served (Decision 010; Paul 2026-10-06: drop, 301 not 410).
- **Evidence / Locator:** SRC-010 CMS rows (Post Type page); SRC-011 page-sitemap lines; SRC-004 (absent); SRC-022; SRC-023; SRC-009; URL Decision Map rows (ext_cm019_*)
- **Classification:** Client Constraint + Project Evidence
- **Confidence:** Corroborated (CMS + sitemap; DataforSEO whole-domain)
- **Alternative Explanation:** The pages may already return 404/410 or be noindexed; the sitemap may be stale.
- **Alternative tested:** Not tested - live status not checked (VA question Q6).
- **Recommendation:** Sitemap removal for these 17 URLs is carried by F-035 (one finding per issue; exclusion must not set noindex). After the client confirms no leads (C4, Q1) they become 301 candidates for Paul to a target he chooses (Q2; proposed default /services/stair-lifts/ - the pages are stair-lift-installer pages; never blanket to an unrelated page). Never 410 (Paul). VA confirms live status first (Q6). Expected impact: the site stops presenting out-of-area cities to search engines.
- **Risk if Acted:** Redirecting to a weak equivalent may be treated as a soft 404 by Google - acceptable, and better than leaving false geography live.
- **Risk if Deferred:** Out-of-area cities stay discoverable through the sitemap, contradicting the area entity.
- **Dependency:** Q1, Q2, Q6
- **Publication gate:** passed - Client Constraint + Project Evidence
- **Affected:** /stair-lift-installer/florida/; /stair-lift-installer/florida/hobe-sound/; /stair-lift-installer/florida/limestone-creek/; /stair-lift-installer/florida/north-palm-beach/; /stair-lift-installer/florida/juno-beach/; /stair-lift-installer/florida/jupiter/; /stair-lift-installer/michigan/; /stair-lift-installer/michigan/stair-lift-installer-warren-mi/; /stair-lift-installer/michigan/stair-lift-installer-troy-mi/; /stair-lift-installer/michigan/stair-lift-installer-sterling-heights-mi/; /stair-lift-installer/michigan/stair-lift-installer-st-clair-shores-mi/; /stair-lift-installer/michigan/stair-lift-installer-southfield-mi/; /stair-lift-installer/michigan/stair-lift-installer-roseville-mi/; /stair-lift-installer/michigan/rochester-hills/; /stair-lift-installer/michigan/novi/; /stair-lift-installer/farmington-hills/; /stair-lift-installer/eastpointe/
- **Revision:** 2 (supersedes F-015.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-016 - High - 5 Architecture (SVC-16; BB-205, BB-314)

- **Observation:** Each service page links to only 4 of the 24 SC location pages (/service-area/hardeeville-sc/, /service-area/ladys-island-sc/, /service-area/ridgeland-sc/, /service-area/walterboro-sc/), plus Georgia pages (/service-area/savannah-ga/, /pooler-ga/, /rincon-ga/), redirecting stubs (/service-area/beaufort-sc-2/, /bluffton-sc-2/, /charleston-sc-2/, /hilton-head-sc/) and the duplicate /service-area/mt-pleasant-sc/.
- **Evidence / Locator:** SRC-020 LNKD Anchor_Text (sources = the 5 service URLs); SRC-006 links_all Unique Outlinks (34 per service page) consistent
- **Classification:** Bradley Methodology Rule (BB-205, BB-314)
- **Confidence:** Corroborated (LNKD link export; SF outlink counts consistent)
- **Alternative Explanation:** A service-areas table may exist but be rendered by JavaScript.
- **Alternative tested:** LNKD reports DOM parity "Yes" for all pages (rendered DOM = raw) - a JS-only table is unlikely; residual risk noted.
- **Recommendation:** In the service rebuilds (svc1), the service-areas H2 links (H3) to every location page; rows are left as Finish placeholders (CM-005). Expected impact: every location page is associated with every service. DRAFT spec - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** Service pages keep associating with Georgia and redirect stubs instead of the 24 served towns.
- **Dependency:** Build svc1; Finish link wheel
- **Publication gate:** n/a
- **Affected:** /services/stair-lifts/; /services/curved-stair-lifts/; /services/porch-lifts/; /services/wheelchair-lifts/; /services/straight-stair-lifts/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-017 - High - 5 Architecture (LOC-18; BB-205, BB-315; CM-022)

- **Observation:** Each SC location page links to 9-10 of its 23 sibling location pages - only the cities of its own metro cluster (e.g. /service-area/beaufort-sc/ links Beaufort-area cities; /service-area/charleston-sc/ links Charleston-area cities); /service-area/ladys-island-sc/ links 3 siblings plus Georgia pages and redirect stubs. Hardeeville and Ridgeland are linked through redirecting "-2" URLs.
- **Evidence / Locator:** SRC-020 LNKD Anchor_Text (sources = 24 location URLs); SRC-004 internal_all Unique Inlinks 11-13 per location page (a full mesh would give 23 or more)
- **Classification:** Bradley Methodology Rule (BB-205, BB-315; CM-022 full city mesh)
- **Confidence:** Corroborated (LNKD links and SF inlink counts agree)
- **Alternative Explanation:** The partial mesh may be a deliberate metro-cluster design (L-008).
- **Alternative tested:** CM-022 (APPROVED) requires the full city mesh on location pages; L-008 concerns hubs, not the sibling table.
- **Recommendation:** Each location rebuild carries a sibling-cities section linking every other location page (Finish placeholders). Expected impact: full city mesh across the area entity. DRAFT spec - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** Location pages stay grouped in two clusters; cross-cluster association is missing.
- **Dependency:** Build location batches; Finish link wheel
- **Publication gate:** n/a
- **Affected:** /service-area/beaufort-sc/; /service-area/bluffton-sc/; /service-area/hilton-head-island-sc/; /service-area/port-royal-sc/; /service-area/ladys-island-sc/; /service-area/laurel-bay-sc/; /service-area/daufuskie-island-sc/; /service-area/okatie-sc/; /service-area/yemassee-sc/; /service-area/hardeeville-sc/; /service-area/ridgeland-sc/; /service-area/levy-sc/; /service-area/walterboro-sc/; /service-area/edisto-island-sc/; /service-area/charleston-sc/; /service-area/north-charleston-sc/; /service-area/mount-pleasant-sc/; /service-area/summerville-sc/; /service-area/goose-creek-sc/; /service-area/hanahan-sc/; /service-area/moncks-corner-sc/; /service-area/hollywood-sc/; /service-area/kiawah-island-sc/; /service-area/folly-island-sc/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-018 - Medium - 5 Architecture (HP-11; BB-201, BB-313 sections 5-6)

- **Observation:** The homepage links to 2 of the 4 core service pages (/services/stair-lifts/, /services/wheelchair-lifts/ - both via the site-wide navigation); it does not link to /services/curved-stair-lifts/ or /services/porch-lifts/, and it links to three discontinued service pages through the navigation (F-003). Its two exported H2s are "Stair Lifts Available Throughout The Lowcountry" and "Stair Lift Solutions Tailored to You".
- **Evidence / Locator:** SRC-020 LNKD Anchor_Text (source "/"); SRC-003 h2_all row 2
- **Classification:** Bradley Methodology Rule (BB-313)
- **Confidence:** Single-source for links (LNKD); H2s corroborated by SF
- **Alternative Explanation:** Curved/porch links may sit in a JS slider.
- **Alternative tested:** DOM parity "Yes" (SRC-020 Pages); residual risk.
- **Recommendation:** Homepage rebuild (final1): one services H2 with H3 links to every service page (max 5-6). Expected impact: the brand hub links each service entity. DRAFT spec - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** Two core services get no homepage association.
- **Dependency:** Build final1
- **Publication gate:** n/a
- **Affected:** /
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-019 - Medium - 5 Architecture / 6 On-page (HP-16; BB-313 section 13)

- **Observation:** The homepage links to none of the 24 location pages (only the three hub pages and the Georgia hub via navigation).
- **Evidence / Locator:** SRC-020 LNKD Anchor_Text (source "/"); SRC-004 row 2 Unique Outlinks 19 (nav-sized)
- **Classification:** Bradley Methodology Rule (BB-313)
- **Confidence:** Corroborated (LNKD links; SF outlink count consistent)
- **Alternative Explanation:** A city list may exist as plain text without links.
- **Alternative tested:** Not tested (no body export). HP-16 needs the grid present; linking per BB-313 section 13.
- **Recommendation:** Add the service-areas grid (cities listed, not H-tagged) in the homepage rebuild. Expected impact: the homepage shows the full area entity. DRAFT spec - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** The homepage does not express the 24 served towns.
- **Dependency:** Build final1
- **Publication gate:** n/a
- **Affected:** /
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-020 - Low - 5 Architecture / 6 On-page (HUB-01, HUB-02, HUB-05, HUB-11) - Low at most (county-hub spec DRAFT; metro-hub rule L-008 PROPOSED)

- **Observation:** Hub pages: /service-area/charleston/ (161 words) and /service-area/hhi-beaufort/ (175 words) carry little more than a link list; /service-area/ has 795 words. None has an H1. Titles: "Service Area", "Charleston Service Area - Home Mobile Medical", "Hilton Head & Beaufort, SC Service Area | Home Mobile Medical" (no GB category, brand last). /service-area/hhi-beaufort/ omits Lady's Island and links Hardeeville and Ridgeland via redirecting "-2" URLs; /service-area/charleston/ also links Walterboro; /service-area/ links no location page.
- **Evidence / Locator:** SRC-004 rows 64, 40, 31 (Word Count); SRC-002 h1_all; SRC-008; SRC-020 Anchor_Text
- **Classification:** Coastal default (county-hub spec DRAFT) + Bradley Methodology Rule (BB-207 empty hubs, BB-302 title)
- **Confidence:** Corroborated
- **Alternative Explanation:** Hubs may be intended as navigation only until L-008 is ruled.
- **Alternative tested:** Paul kept the three hubs (2026-10-06); the hub rule is proposed, so severity is capped at Low.
- **Recommendation:** Rebuild each hub in its location batch once Paul rules L-008 and approves the county-hub spec; give each real area substance (BB-207). Expected impact: hubs stop being thin link lists. Low - DRAFT spec and PROPOSED hub rule.
- **Risk if Acted:** None.
- **Risk if Deferred:** Thin hubs persist.
- **Dependency:** L-008 ruling; county-hub spec approval
- **Publication gate:** n/a
- **Affected:** /service-area/; /service-area/charleston/; /service-area/hhi-beaufort/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-021 - Low - 5 Architecture (page type questioned - no spec)

- **Observation:** /services/ is a services hub (title "Mobility Devices | Home Mobile Medical", 980 words, no H1). No page spec in methodology/specs covers a services hub; Brand Guide C1 lists it as "Services hub - Planned (rewrite)".
- **Evidence / Locator:** SRC-004 row 21; SRC-008 row 9; SRC-025 Brand Guide C1; methodology/specs/README.md
- **Classification:** Project Evidence
- **Confidence:** Corroborated
- **Alternative Explanation:** The page could follow the homepage services-section pattern.
- **Alternative tested:** No ruling exists - the type is questioned, not decided.
- **Recommendation:** Paul decides whether /services/ gets a spec (or follows the homepage services-section pattern) before it is rebuilt; content scope per F-003. Expected impact: the hub has a defined role. Low - no spec to fail.
- **Risk if Acted:** None.
- **Risk if Deferred:** The page has no build standard.
- **Dependency:** Paul (spec decision)
- **Publication gate:** n/a
- **Affected:** /services/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-022 - High - 6 On-page (SVC-05, LOC-04, HUB-05; COM-04; RULE-002)

- **Observation:** 54 of the 96 crawled 200 pages have no H1: all 5 service pages, all 24 SC location pages, the 3 hubs, /services/, /terms-conditions/, and 20 Georgia/legacy pages. On the location pages the first H2 repeats the SEO title string including the brand (e.g. "Stair Lift Installation in Beaufort, SC | Home Mobile Medical"), i.e. the visible main heading is marked up as H2 (COM-04). One H1 per page is a house standard (RULE-002), not a platform requirement.
- **Evidence / Locator:** SRC-002 h1_all (Occurrences = 0, 54 rows); SRC-003 h2_all H2-1 on location rows; SRC-020 LNKD Issues "Missing H1 tag" (56 URLs) with DOM parity "Yes"
- **Classification:** Bradley Methodology Rule (BB-307; RULE-002 house standard)
- **Confidence:** Corroborated (SF raw HTML and LNKD rendered DOM agree)
- **Alternative Explanation:** An H1 might be injected by JavaScript.
- **Alternative tested:** LNKD DOM parity "Yes" (rendered = raw) and LNKD also reports the H1 missing.
- **Recommendation:** Every rebuilt page gets exactly one H1 in the spec format (no brand); no interim edit of these legacy pages is needed since all are scheduled for rebuild. None of the affected pages ranks top 3 for its main keyword, so the CM-020 H1 lock does not apply. Expected impact: each page states its primary entity in the H1. DRAFT specs - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** Pages lack their primary heading signal.
- **Dependency:** Build batches
- **Publication gate:** n/a
- **Affected:** /services/stair-lifts/; /services/wheelchair-lifts/; /services/curved-stair-lifts/; /services/porch-lifts/; /services/straight-stair-lifts/; /service-area/summerville-sc/; /service-area/north-charleston-sc/; /service-area/goose-creek-sc/; /service-area/hollywood-sc/; /service-area/kiawah-island-sc/; /service-area/folly-island-sc/; /service-area/charleston-sc/; /service-area/moncks-corner-sc/; /service-area/mount-pleasant-sc/; /service-area/hanahan-sc/; /service-area/levy-sc/; /service-area/laurel-bay-sc/; /service-area/port-royal-sc/; /service-area/okatie-sc/; /service-area/yemassee-sc/; /service-area/daufuskie-island-sc/; /service-area/edisto-island-sc/; /service-area/beaufort-sc/; /service-area/hilton-head-island-sc/; /service-area/bluffton-sc/; /service-area/hardeeville-sc/; /service-area/walterboro-sc/; /service-area/ladys-island-sc/; /service-area/ridgeland-sc/; /service-area/hhi-beaufort/; /service-area/charleston/; /service-area/; /services/power-chairs/; /services/; /terms-conditions/; /services/scooter-lifts/; /services/mobility-ramps/; /service-area/savannah/; /service-area/georgetown-ga/; /service-area/tybee-island-ga/; /service-area/bloomingdale-ga/; /service-area/port-wentworth-ga/; /service-area/richmond-hill-ga/; /service-area/skidaway-island-ga/; /service-area/mt-pleasant-sc/; /service-area/savannah-ga/; /service-area/pooler-ga/; /service-area/rincon-ga/; /charleston-sc/stair-lifts/; /savannah-ga/stair-lifts/; /bluffton-sc/; /charleston-sc/mobility-ramps/; /charleston-sc/power-chairs/; /charleston-sc/wheelchair-lifts/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-023 - High - 6 On-page (LOC-02; BB-301/302) - High (wrong title entity order)

- **Observation:** All 24 SC location titles lead with a service phrase: 22 read "Stair Lift Installation in <City>, SC | Home Mobile Medical" (brand last); /service-area/folly-island-sc/ uses that pattern but names Folly Beach (F-007); /service-area/ladys-island-sc/ reads "Medical Equipment In Lady's Island, SC" (no brand at all). None carries the GB category; all abbreviate the state. Spec format: Brand - GB Category - City, Full State Name (RULE-003 brand-led location pages). The 9 Georgia location pages use the same pattern (held for microsite). Rev 1 said all 24 end with the brand; Lady's Island does not.
- **Evidence / Locator:** SRC-008 page_titles_all rows for the 24 SC location URLs
- **Classification:** Bradley Methodology Rule (BB-301, BB-302, RULE-003)
- **Confidence:** Corroborated (SRC-008 and SRC-005 HTML Title agree)
- **Alternative Explanation:** The service-led pattern may have been chosen to target "stair lift installation <city>" queries.
- **Alternative tested:** DataforSEO shows no location page ranking top 20 for a lift query (best: /service-area/charleston-sc/ #39, SRC-022) - no performance reason to keep it.
- **Recommendation:** Retitle each location page to the spec format in its rebuild (structural change, handoff). Expected impact: brand-led location titles that name the category entity and the city with the full state name. DRAFT spec - advisory.
- **Risk if Acted:** Short-term ranking movement on the few location keywords (all positions 39 or lower).
- **Risk if Deferred:** Location titles keep omitting the category entity and leading with a service phrase.
- **Dependency:** Build location batches
- **Publication gate:** n/a
- **Affected:** /service-area/beaufort-sc/; /service-area/bluffton-sc/; /service-area/hilton-head-island-sc/; /service-area/port-royal-sc/; /service-area/ladys-island-sc/; /service-area/laurel-bay-sc/; /service-area/daufuskie-island-sc/; /service-area/okatie-sc/; /service-area/yemassee-sc/; /service-area/hardeeville-sc/; /service-area/ridgeland-sc/; /service-area/levy-sc/; /service-area/walterboro-sc/; /service-area/edisto-island-sc/; /service-area/charleston-sc/; /service-area/north-charleston-sc/; /service-area/mount-pleasant-sc/; /service-area/summerville-sc/; /service-area/goose-creek-sc/; /service-area/hanahan-sc/; /service-area/moncks-corner-sc/; /service-area/hollywood-sc/; /service-area/kiawah-island-sc/; /service-area/folly-island-sc/
- **Revision:** 2 (supersedes F-023.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-024 - Medium - 6 On-page (HP-03, SVC-04, LOC-03, ABT-02; CM-014)

- **Observation:** Title separators are mixed across the site: 46 titles use a pipe, 1 an em dash, 21 a hyphen, 3 an en dash, and three older service titles use the word "From" ("Stair Lifts From Home Mobile Medical", "Wheelchair Lifts From Home Mobile Medical", "Power Chairs From Home Mobile Medical"). The house separator is a single hyphen (Brand Guide A7). CM-014: consistency is the finding, not the glyph.
- **Evidence / Locator:** SRC-008 page_titles_all (all 96 rows; counts by glyph)
- **Classification:** Bradley Methodology Rule (BB-302 consistency) + Coastal ruling CM-014 (OPEN - consistency only)
- **Confidence:** Corroborated
- **Alternative Explanation:** Different templates (theme vs SEOPress) may produce different separators.
- **Alternative tested:** SEOPress title templates not yet read (S20 pending with Jonie).
- **Recommendation:** Use the Brand Guide A7 separator on every rebuilt title; check SEOPress title templates when S20 returns. Expected impact: consistent title structure. DRAFT specs - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** Inconsistent title structure persists.
- **Dependency:** S20 (SEOPress settings worksheet)
- **Publication gate:** n/a
- **Affected:** /; /services/stair-lifts/; /services/curved-stair-lifts/; /services/porch-lifts/; /services/wheelchair-lifts/; /services/straight-stair-lifts/; /service-area/beaufort-sc/; /service-area/bluffton-sc/; /service-area/hilton-head-island-sc/; /service-area/port-royal-sc/; /service-area/ladys-island-sc/; /service-area/laurel-bay-sc/; /service-area/daufuskie-island-sc/; /service-area/okatie-sc/; /service-area/yemassee-sc/; /service-area/hardeeville-sc/; /service-area/ridgeland-sc/; /service-area/levy-sc/; /service-area/walterboro-sc/; /service-area/edisto-island-sc/; /service-area/charleston-sc/; /service-area/north-charleston-sc/; /service-area/mount-pleasant-sc/; /service-area/summerville-sc/; /service-area/goose-creek-sc/; /service-area/hanahan-sc/; /service-area/moncks-corner-sc/; /service-area/hollywood-sc/; /service-area/kiawah-island-sc/; /service-area/folly-island-sc/; /about/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-025 - Medium - 6 On-page (LOC-10, LOC-24; CM-015 portability)

- **Observation:** 16 of the 24 SC location pages open with the same sentence frame "Stay safe and independent with professional (or expert) stair lift installation from Home Mobile Medical, your trusted mobility experts serving <City> ..." - portable across siblings with only the city swapped.
- **Evidence / Locator:** SRC-010 CMS Excerpt column (rows for the 16 URLs)
- **Classification:** Coastal PILOT (CM-015) + Project Evidence
- **Confidence:** Single-source (CMS excerpt; body text not exported)
- **Alternative Explanation:** The excerpt may not be the rendered opening.
- **Alternative tested:** The CMS excerpt is the page's own content start (matches the SF H2-1 order); residual risk noted.
- **Recommendation:** Each rebuilt location opening is unique to its city (verified facts only; [NEED] where missing). Expected impact: openings pass the portability test. DRAFT spec - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** Location openings stay functionally duplicate.
- **Dependency:** Build location batches; facts interview if the evidence gate blocks (CM-041/042)
- **Publication gate:** n/a
- **Affected:** /service-area/beaufort-sc/; /service-area/bluffton-sc/; /service-area/laurel-bay-sc/; /service-area/daufuskie-island-sc/; /service-area/okatie-sc/; /service-area/yemassee-sc/; /service-area/hardeeville-sc/; /service-area/ridgeland-sc/; /service-area/levy-sc/; /service-area/edisto-island-sc/; /service-area/charleston-sc/; /service-area/north-charleston-sc/; /service-area/mount-pleasant-sc/; /service-area/summerville-sc/; /service-area/goose-creek-sc/; /service-area/hanahan-sc/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-026 - Medium - 3 Brand & entity (HP-06; BB-304, CM-024) - see OPEN audit-local conflict CF-LOCAL-001 (renumbered from CF-001, which is a resolved register entry in rulings.md section E)

- **Observation:** Homepage H1 "Enhance Your Independence And Mobility With Our Stair Lift Solutions" uses neither reserved homepage variant (B1: "Mobility equipment supplier", "South Carolina Lowcountry") and names no area. HP-08 / BB-313 section 3 say the homepage H1 is never changed once live.
- **Evidence / Locator:** SRC-002 h1_all row 2; SRC-025 Brand Guide B1
- **Classification:** Bradley Methodology Rule (BB-304, BB-313 section 3)
- **Confidence:** Assumed (PROC-01 step 3 - open conflict); the observation itself is Corroborated (SRC-002, SRC-005)
- **Alternative Explanation:** The BB-313 section 3 lock may be meant only for H1s built to the Standard, not legacy H1s.
- **Alternative tested:** Unresolved - recorded as conflict CF-LOCAL-001 (PROC-01), not decided here.
- **Recommendation:** Follow the current production rule: no recommendation to change the live homepage H1 (HP-08). Paul rules the conflict CF-LOCAL-001 (Q4). PROC-01 step 4 done: the proposed ruling is filed as methodology/lessons.md L-009 (PROPOSED, 2026-10-08). Paul's 2026-10-08 Apex ruling on the same tension is client-specific and is not applied here. Expected impact if Paul allows a change: the H1 expresses the reserved category and area variants. DRAFT spec - advisory.
- **Risk if Acted:** If changed without a ruling, a methodology rule is broken.
- **Risk if Deferred:** The brand hub H1 keeps omitting the entity.
- **Dependency:** Q4 / conflict CF-LOCAL-001; lessons.md L-009 (PROPOSED)
- **Publication gate:** n/a
- **Affected:** /
- **Revision:** 3 (supersedes F-026.2) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-027 - Low - 6 On-page (ABT-01; BB-302) - Low at most: "Area Category" meaning is a Coastal default (about.md element 2)

- **Observation:** About page title "About Us - Home Mobile Medical" lacks the area/category part of the spec format "About Brand - Area Category".
- **Evidence / Locator:** SRC-008 row 11
- **Classification:** Coastal default - needs Paul's ruling (about.md element 2: meaning of "Area Category"); BB-302 order. specs/README.md: a Coastal default element may be reported but never above Low until Paul rules.
- **Confidence:** Corroborated
- **Alternative Explanation:** The about format is partly a Coastal default.
- **Alternative tested:** ABT-01 is listed as High in the DRAFT spec; the "Area Category" meaning is unruled.
- **Recommendation:** Retitle in the about rebuild (final2) once Paul confirms the "Area Category" meaning. Expected impact: the about title carries the entity. Low - Coastal default; DRAFT spec - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** About title stays generic.
- **Dependency:** Build final2
- **Publication gate:** n/a
- **Affected:** /about/
- **Revision:** 2 (supersedes F-027.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-028 - Low - 6 On-page (ABT-04; BB-304) - Low at most: H1 format is a Coastal default (about.md element 4)

- **Observation:** About page H1 is "About us" - no category or area variant.
- **Evidence / Locator:** SRC-002 row 11
- **Classification:** Coastal default - needs Paul's ruling (about.md element 4: H1 format); BB-304. specs/README.md: never above Low until Paul rules.
- **Confidence:** Corroborated
- **Alternative Explanation:** The H1 may be a deliberate plain label.
- **Alternative tested:** Not tested; BB-304 requires a variant of the title entities.
- **Recommendation:** Use a B2-pool variant H1 in the about rebuild once Paul rules the about H1 format. Expected impact: the about H1 names the entity. Low - Coastal default; DRAFT spec - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** Generic H1 persists.
- **Dependency:** Build final2
- **Publication gate:** n/a
- **Affected:** /about/
- **Revision:** 2 (supersedes F-028.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-029 - Medium - 3 Brand & entity (BLG-05; CM-039, CM-004)

- **Observation:** All 21 blog posts are authored by the WordPress user "wittycow"; the blog author must be the owner (Jason Workens, Brand Guide D named staff) unless the client states otherwise.
- **Evidence / Locator:** SRC-010 CMS Author column (21 post rows)
- **Classification:** Coastal ruling (CM-039) + Project Evidence
- **Confidence:** Single-source (CMS export)
- **Alternative Explanation:** The byline shown on the page may differ from the CMS author.
- **Alternative tested:** Not tested - byline not in the crawl exports.
- **Recommendation:** Reassign authorship to the owner when each post is handled in the Blog Decision Map (posts stay as-is until then, Paul 2026-10-07). Expected impact: a real, checkable author (CM-004).
- **Risk if Acted:** None.
- **Risk if Deferred:** Posts keep a non-owner author.
- **Dependency:** Blog Decision Map
- **Publication gate:** n/a
- **Affected:** /are-stair-lifts-covered-by-medicare/; /understanding-your-home-how-do-stair-lifts-work/; /are-stair-lifts-tax-deductible-know-your-rights-and-benefits/; /is-there-a-weight-limit-on-stairlifts/; /how-are-stair-lifts-installed-and-attached/; /do-stair-lifts-use-a-lot-of-electricity/; /can-stairlifts-be-used-outside/; /can-stair-lifts-turn-corners-or-go-around-corners/; /are-stair-lifts-safe-and-ada-compliant/; /are-stair-lifts-noisy/; /are-stair-lifts-expensive-to-run/; /are-stair-lifts-covered-by-medicare-medicaid-or-health-insurance/; /are-stair-lifts-battery-operated-and-how-are-they-powered/; /are-stair-lifts-adjustable-reversible-and-can-they-be-fitted-to-any-stairs/; /launching-home-mobile-medical-a-new-era-in-mobility-solutions/; /embracing-a-new-era-from-beaufort-medical-equipment-to-home-mobile-medical/; /mobility-scooter-repair-near-me/; /the-history-and-growth-of-telemedicine/; /what-you-should-know-about-long-term-care/; /costs-and-financing-options-for-stairlift-installation/; /the-most-common-side-effects-of-semaglutide-and-how-to-manage-them/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-030 - Medium - 6 On-page (BLG-03; BB-302, BB-704)

- **Observation:** 20 of 21 post titles do not follow "Post Title - Brand": 18 omit the brand; 2 lead with it ("Introducing Home Mobile Medical - Revolutionizing Mobility Solutions", "Home Mobile Medical: Our Evolution from Beaufort Medical Equipment"). Only /costs-and-financing-options-for-stairlift-installation/ follows the format. Rev 1 said 20 omit the brand.
- **Evidence / Locator:** SRC-008 page_titles_all (post rows)
- **Classification:** Bradley Methodology Rule (BB-302, BB-704)
- **Confidence:** Corroborated
- **Alternative Explanation:** A SEOPress template may append the brand only on some post types.
- **Alternative tested:** S20 pending.
- **Recommendation:** Apply the format when posts are handled in the Blog Decision Map. Expected impact: brand on every post title. DRAFT spec - advisory.
- **Risk if Acted:** None.
- **Risk if Deferred:** Posts lack the brand in titles.
- **Dependency:** Blog Decision Map; S20
- **Publication gate:** n/a
- **Affected:** /are-stair-lifts-covered-by-medicare/; /understanding-your-home-how-do-stair-lifts-work/; /are-stair-lifts-tax-deductible-know-your-rights-and-benefits/; /is-there-a-weight-limit-on-stairlifts/; /how-are-stair-lifts-installed-and-attached/; /do-stair-lifts-use-a-lot-of-electricity/; /can-stairlifts-be-used-outside/; /can-stair-lifts-turn-corners-or-go-around-corners/; /are-stair-lifts-safe-and-ada-compliant/; /are-stair-lifts-noisy/; /are-stair-lifts-expensive-to-run/; /are-stair-lifts-covered-by-medicare-medicaid-or-health-insurance/; /are-stair-lifts-battery-operated-and-how-are-they-powered/; /are-stair-lifts-adjustable-reversible-and-can-they-be-fitted-to-any-stairs/; /launching-home-mobile-medical-a-new-era-in-mobility-solutions/; /embracing-a-new-era-from-beaufort-medical-equipment-to-home-mobile-medical/; /mobility-scooter-repair-near-me/; /the-history-and-growth-of-telemedicine/; /what-you-should-know-about-long-term-care/; /the-most-common-side-effects-of-semaglutide-and-how-to-manage-them/
- **Revision:** 2 (supersedes F-030.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-031 - Medium - 7 Blog (entity scope; BB-701 via the Blog Decision Map)

- **Observation:** Four posts sit outside the entity: telemedicine history, long-term care, semaglutide side effects, and mobility-scooter repair (a discontinued service). DataforSEO shows 0 ranking keywords and 0 referring domains for all four.
- **Evidence / Locator:** SRC-008 titles; SRC-010 CMS rows; SRC-022; SRC-023
- **Classification:** Project Evidence
- **Confidence:** Corroborated
- **Alternative Explanation:** They may attract caregiver audiences.
- **Alternative tested:** Not tested - no GSC/GA4.
- **Recommendation:** Route to the Blog Decision Map (bb-blog-analysis: Test B first, CM-007; CM-021 for any redirect). No disposition change now (Paul 2026-10-07). Expected impact: blog content supports the lift entity only.
- **Risk if Acted:** n/a now.
- **Risk if Deferred:** Off-entity health content stays on a health-adjacent site (see F-032).
- **Dependency:** Blog Decision Map
- **Publication gate:** n/a
- **Affected:** /the-history-and-growth-of-telemedicine/; /what-you-should-know-about-long-term-care/; /the-most-common-side-effects-of-semaglutide-and-how-to-manage-them/; /mobility-scooter-repair-near-me/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-032 - High - 3 Brand & entity (BLG-19, BLG-16; CM-025, CM-040, CM-016)

- **Observation:** Posts make coverage, tax, legal, health and product-spec claims with no named authoritative source recorded: Medicare/Medicaid/insurance coverage of stair lifts (two posts; the larger ranks #2 for "will medicare pay for a stairlift"), tax deductibility, ADA compliance, semaglutide side effects (a drug-health claim), long-term care, weight limits, battery/power and outdoor use, and prices ("Straight stairlifts range from $2,000 to $5,000 on average. Curved or outdoor stairlifts can range from $8,000 to $15,000...").
- **Evidence / Locator:** SRC-008 titles; SRC-007 meta row 76 (costs post quote); SRC-026 claims list E4-E7; SRC-025 Brand Guide D2 last two rows; SRC-022 ranked-keywords (Medicare post)
- **Classification:** Legal/truth constraint (CM-040: named source or remove) + Project Evidence
- **Confidence:** Corroborated for the topics; Single-source for individual sentences (no body export)
- **Alternative Explanation:** The posts may already cite sources in the body.
- **Alternative tested:** Not tested - body text not exported.
- **Recommendation:** No disposition change now - posts stay as-is until the Blog Decision Map (Paul 2026-10-07). When each is handled: rewrite only from Medicare.gov/CMS, IRS Publication 502, ADA.gov/US Access Board and manufacturer spec sheets; prices only from client-confirmed figures (CM-016); Paul approves with human review recorded (CM-025). Expected impact: coverage/health statements become sourced or are removed.
- **Risk if Acted:** Changing the Medicare post could disturb its #2 ranking - the Blog Decision Map weighs that.
- **Risk if Deferred:** Unsourced coverage and health claims stay live on a health-adjacent site.
- **Dependency:** Blog Decision Map; Paul review
- **Publication gate:** n/a
- **Affected:** /are-stair-lifts-covered-by-medicare-medicaid-or-health-insurance/; /are-stair-lifts-covered-by-medicare/; /are-stair-lifts-tax-deductible-know-your-rights-and-benefits/; /are-stair-lifts-safe-and-ada-compliant/; /the-most-common-side-effects-of-semaglutide-and-how-to-manage-them/; /what-you-should-know-about-long-term-care/; /is-there-a-weight-limit-on-stairlifts/; /are-stair-lifts-battery-operated-and-how-are-they-powered/; /can-stairlifts-be-used-outside/; /costs-and-financing-options-for-stairlift-installation/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-033 - Low - 2 Technical & crawl

- **Observation:** Internal links point at redirecting URLs: /equipment-rentals/ (from 3 pages); /service-area/beaufort-sc-2/ (from 10 pages); /service-area/bluffton-sc-2/ (from 10 pages); /service-area/charleston-sc-2/ (from 10 pages); /service-area/hardeeville-sc-2/ (from 18 pages); /service-area/hilton-head-sc/ (from 10 pages); /service-area/ridgeland-sc-2/ (from 18 pages); /services/stair-lift/ (from 8 pages). The redirects /service-area/bluffton-sc-2/, /service-area/charleston-sc-2/ and /service-area/beaufort-sc-2/ each take two hops (to the slash-less URL, then to the final URL).
- **Evidence / Locator:** SRC-020 Anchor_Text (targets); SRC-004 internal_all rows 116, 122, 139, 142, 156, 158 (301 + Redirect URL)
- **Classification:** Platform guidance (Google Search Central recommends avoiding redirect chains; it is not a requirement - Googlebot follows several hops) + Project Evidence
- **Confidence:** Corroborated
- **Alternative Explanation:** n/a
- **Alternative tested:** n/a
- **Recommendation:** Point internal links at the final URLs; repoint the three "-2" redirects straight to the canonical slash URL (one hop). Most links disappear with the Build rebuilds; the redirect repoint is a VA handoff. Expected impact: cleaner crawl paths.
- **Risk if Acted:** None.
- **Risk if Deferred:** Minor crawl waste.
- **Dependency:** Batched Low handoff
- **Publication gate:** n/a
- **Affected:** /are-stair-lifts-covered-by-medicare-medicaid-or-health-insurance/; /are-stair-lifts-covered-by-medicare/; /are-stair-lifts-expensive-to-run/; /are-stair-lifts-noisy/; /are-stair-lifts-safe-and-ada-compliant/; /can-stair-lifts-turn-corners-or-go-around-corners/; /can-stairlifts-be-used-outside/; /is-there-a-weight-limit-on-stairlifts/; /service-area/beaufort-sc-2/; /service-area/beaufort-sc/; /service-area/bluffton-sc-2/; /service-area/bluffton-sc/; /service-area/daufuskie-island-sc/; /service-area/edisto-island-sc/; /service-area/hardeeville-sc-2/; /service-area/hardeeville-sc/; /service-area/hhi-beaufort/; /service-area/hilton-head-island-sc/; /service-area/hilton-head-sc/; /service-area/ladys-island-sc/; /service-area/laurel-bay-sc/; /service-area/levy-sc/; /service-area/mt-pleasant-sc/; /service-area/okatie-sc/; /service-area/port-royal-sc/; /service-area/ridgeland-sc-2/; /service-area/ridgeland-sc/; /service-area/yemassee-sc/; /services/curved-stair-lifts/; /services/mobility-ramps/; /services/porch-lifts/; /services/power-chairs/; /services/scooter-lifts/; /services/stair-lifts/; /services/straight-stair-lifts/; /services/wheelchair-lifts/
- **Revision:** 2 (supersedes F-033.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-034 - Low - 2 Technical & crawl

- **Observation:** /services/stair-lift/ (a service-pattern URL) 301-redirects to the legacy city page /hilton-head/stair-lift/, which is itself Needs Evidence (CM-019 C2/C3 fail).
- **Evidence / Locator:** SRC-004 row 209
- **Classification:** Project Evidence
- **Confidence:** Single-source
- **Alternative Explanation:** The redirect may have been set to preserve an old campaign URL.
- **Alternative tested:** Not tested.
- **Recommendation:** Revisit the target when /hilton-head/stair-lift/ is decided; /services/stair-lifts/ is the natural target. Changing a redirect target is a structural handoff (Paul). Expected impact: the service URL resolves to the service page.
- **Risk if Acted:** None.
- **Risk if Deferred:** A service URL lands on a city page.
- **Dependency:** Disposition of /hilton-head/stair-lift/
- **Publication gate:** n/a
- **Affected:** /services/stair-lift/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-035 - Low - 2 Technical & crawl (orphan candidates - reconciled)

- **Observation:** The XML page-sitemap lists 37 URLs that no crawled page links to (orphan candidates): Florida/Michigan pages, /stair-lift-installer/*, Georgia /savannah-ga/* pages, /hilton-head/*, /charleston-sc/, /beaufort-sc/, /power-chairs/, /about-us-across-the-web/ and /bluffton-sc/stair-lift-installer/. Reconciled against CMS (all published), DataforSEO rankings/backlinks (2 rank: /savannah-ga/, /bluffton-sc/stair-lift-installer/), GBP (homepage only) and citations.
- **Evidence / Locator:** SRC-011 sitemap lines vs SRC-004 crawl; SRC-010; SRC-022; SRC-023
- **Classification:** Project Evidence
- **Confidence:** Corroborated (sitemap + CMS + crawl)
- **Alternative Explanation:** The sitemap export (2026-09-18) may be stale.
- **Alternative tested:** Not tested (live sitemap not re-read).
- **Recommendation:** Remove from the XML sitemap (VA handoff - SEOPress settings are handoffs) the 29 URLs that pass CM-019 C1-C3 and are headed for retirement: the 17 FL/MI URLs (F-015), /stair-lift-installer/ and /stair-lift-installer/{walterboro, ladys-island, mt-pleasant, hardeeville, ridgeland}/, /beaufort-sc/, /charleston-sc/, /hilton-head/, /hilton-head/wheelchair-lift/, /hilton-head/stair-lift-repair/ and /power-chairs/. The exclusion must not change meta robots: if SEOPress can only drop a URL from the sitemap by setting noindex, that is a noindex (destructive, CM-019) and waits with the rest of the URL's disposition. Leave unchanged: the 6 Georgia URLs (/savannah-ga/ and its 3 children, /stair-lift-installer/pooler/, /stair-lift-installer/rincon/ - Hold, no action on this site now, Paul), /bluffton-sc/stair-lift-installer/ (fails CM-019 C1 - Q3) and /about-us-across-the-web/ (Q6 and the Finish ID-page decision). Removing from the sitemap does not delete pages. URL dispositions per the URL Decision Map. Expected impact: the sitemap lists only canonical, in-area pages, without pre-empting Paul's Georgia and value-URL decisions.
- **Risk if Acted:** None (sitemap only).
- **Risk if Deferred:** Search engines keep discovering out-of-area/legacy URLs.
- **Dependency:** S20 (SEOPress sitemap settings); audit_approved
- **Publication gate:** n/a
- **Affected:** /about-us-across-the-web/; /beaufort-sc/; /bluffton-sc/stair-lift-installer/; /charleston-sc/; /hilton-head/; /hilton-head/stair-lift-repair/; /hilton-head/wheelchair-lift/; /power-chairs/; /savannah-ga/; /savannah-ga/mobility-ramps/; /savannah-ga/power-chairs/; /savannah-ga/wheelchair-lift/; /stair-lift-installer/; /stair-lift-installer/eastpointe/; /stair-lift-installer/farmington-hills/; /stair-lift-installer/florida/; /stair-lift-installer/florida/hobe-sound/; /stair-lift-installer/florida/juno-beach/; /stair-lift-installer/florida/jupiter/; /stair-lift-installer/florida/limestone-creek/; /stair-lift-installer/florida/north-palm-beach/; /stair-lift-installer/hardeeville/; /stair-lift-installer/ladys-island/; /stair-lift-installer/michigan/; /stair-lift-installer/michigan/novi/; /stair-lift-installer/michigan/rochester-hills/; /stair-lift-installer/michigan/stair-lift-installer-roseville-mi/; /stair-lift-installer/michigan/stair-lift-installer-southfield-mi/; /stair-lift-installer/michigan/stair-lift-installer-st-clair-shores-mi/; /stair-lift-installer/michigan/stair-lift-installer-sterling-heights-mi/; /stair-lift-installer/michigan/stair-lift-installer-troy-mi/; /stair-lift-installer/michigan/stair-lift-installer-warren-mi/; /stair-lift-installer/mt-pleasant/; /stair-lift-installer/pooler/; /stair-lift-installer/ridgeland/; /stair-lift-installer/rincon/; /stair-lift-installer/walterboro/
- **Revision:** 2 (supersedes F-035.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-036 - Low - 6 On-page / 2 Technical (meta descriptions; WC-C2)

- **Observation:** Meta descriptions: 12 pages have none (blog index, category and pagination archives); 20 exceed 160 characters (legal pages, /contact/ 288, /about/ 328, /service-area/charleston/ 327, costs post 321 - several are truncated body text); the service pages /services/curved-stair-lifts/, /services/porch-lifts/, /services/straight-stair-lifts/ and /services/scooter-lifts/ describe the service "in Hilton Head, SC" rather than the area entity.
- **Evidence / Locator:** SRC-007 meta_description_all (Occurrences, Length, text)
- **Classification:** Project Evidence (WC-C2 house standard)
- **Confidence:** Corroborated (SRC-007, SRC-005)
- **Alternative Explanation:** Theme may auto-generate from body text when the field is empty.
- **Alternative tested:** Not tested.
- **Recommendation:** Rebuilt pages get spec meta descriptions; for kept utility/blog pages, fix in the batched Low handoff (meta descriptions are a safe fix after audit_approved). Expected impact: accurate snippets naming the area.
- **Risk if Acted:** None.
- **Risk if Deferred:** Weak or truncated snippets.
- **Dependency:** audit_approved (safe fix)
- **Publication gate:** n/a
- **Affected:** /; /about/; /are-stair-lifts-adjustable-reversible-and-can-they-be-fitted-to-any-stairs/; /are-stair-lifts-battery-operated-and-how-are-they-powered/; /blog/; /blog/page/2/; /blog/page/3/; /bluffton-sc/wheelchair-lift-repair/; /category/announcements/; /category/faqs/; /category/faqs/page/2/; /category/health/; /category/insurance-questions/; /category/long-term-care/; /category/mobility-equipment/; /category/telemedicine/; /category/uncategorized/; /charleston-sc/wheelchair-lifts/; /contact/; /costs-and-financing-options-for-stairlift-installation/; /do-stair-lifts-use-a-lot-of-electricity/; /embracing-a-new-era-from-beaufort-medical-equipment-to-home-mobile-medical/; /mobility-scooter-repair-near-me/; /service-area/charleston/; /service-area/mt-pleasant-sc/; /services/; /services/curved-stair-lifts/; /services/porch-lifts/; /services/scooter-lifts/; /services/straight-stair-lifts/; /terms-conditions/; /terms-conditions/accessibility-statement/; /terms-conditions/cookie-policy/; /terms-conditions/copyright-policy/; /terms-conditions/privacy-policy/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-037 - Low - 2 Technical & crawl (outbound links)

- **Observation:** Outbound links return errors: https://summervilledream.org/farmers-market/ (404, SRC-001 row 119); https://parks.chathamcountyga.gov/CommunityParks/TomTriplett (404, SRC-001 row 130); https://parks.chathamcountyga.gov/BoatRampsAndFishingPiers/TybeeIslandFishingPierAndPavilion (404, SRC-001 row 133); https://visittybee.com/article/guide-to-back-river-beach (403, SRC-001 row 137); https://home.army.mil/stewart/about/Garrison/hunter-army-airfield (404, SRC-001 row 146); https://www.niche.com/places-to-live/bluffton-beaufort-sc/ (403, SRC-001 row 150); https://www.suncityhiltonhead.org/ (502, SRC-001 row 168); https://www.farmersmarketbluffton.org/ (Connection Timeout, SRC-001 row 173). The export gives the inlink count, not the source page; by subject the sources are the Summerville, Bluffton and Hilton Head Island location pages and Georgia pages (held).
- **Evidence / Locator:** SRC-001 external_all rows 119, 130, 133, 137, 146, 150, 168, 173
- **Classification:** Project Evidence
- **Confidence:** Single-source (one crawl)
- **Alternative Explanation:** Transient outages (502, timeout, 403 bot blocks).
- **Alternative tested:** Not re-tested.
- **Recommendation:** VA re-checks and replaces/removes dead outbound links on SC pages (safe fix: broken links) - or the rebuilds drop them; ignore Georgia pages (held). Expected impact: no dead links in Things to Do/Top Sites sections.
- **Risk if Acted:** None.
- **Risk if Deferred:** Dead links on location pages.
- **Dependency:** audit_approved
- **Publication gate:** n/a
- **Affected:** Pages linking out to: https://summervilledream.org/farmers-market/; https://parks.chathamcountyga.gov/CommunityParks/TomTriplett; https://parks.chathamcountyga.gov/BoatRampsAndFishingPiers/TybeeIslandFishingPierAndPavilion; https://visittybee.com/article/guide-to-back-river-beach; https://home.army.mil/stewart/about/Garrison/hunter-army-airfield; https://www.niche.com/places-to-live/bluffton-beaufort-sc/; https://www.suncityhiltonhead.org/; https://www.farmersmarketbluffton.org/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-038 - Low - 2 Technical & crawl

- **Observation:** Two published CMS pages of unclear purpose are not linked internally: /new-homepage/ (CMS page "New Homepage", published 2026-09-10, not in the sitemap) and /about-us-across-the-web/ (in the sitemap; a list of directory names). Live status and robots directives unknown. The /new-homepage/ CMS excerpt opens "Locally owned - Beaufort, SC - Free in-home estimates The Best Stair Lift Installation in the Lowcountry ... installs stair lifts, wheelchair lifts and mobility ramps": if live and indexable it would carry a "The Best" opener with no CM-020 decision (Brand Guide H2 empty; proof fails at 2.9 stars / 19 reviews; sensitive client) and a discontinued service (mobility ramps - Brand Guide D Not offered).
- **Evidence / Locator:** SRC-010 CMS rows 125 (Excerpt, Published Date) and 44; SRC-011
- **Classification:** Project Evidence
- **Confidence:** Single-source
- **Alternative Explanation:** They may be private/draft-protected despite "Publish".
- **Alternative tested:** Not tested - VA question Q5.
- **Recommendation:** VA checks HTTP status and robots for both (Q5). If /new-homepage/ is live and indexable, it is a duplicate homepage carrying unapproved claims: Paul decides, and any noindex/redirect is destructive (CM-019); severity is re-set after Q5. /about-us-across-the-web/ is reviewed in Finish as a possible sameAs/ID-page input. Expected impact: no duplicate homepage in the index.
- **Risk if Acted:** None until checked.
- **Risk if Deferred:** A duplicate homepage could compete with "/".
- **Dependency:** Q5
- **Publication gate:** n/a
- **Affected:** /new-homepage/; /about-us-across-the-web/
- **Revision:** 2 (supersedes F-038.1) · status reviewed · reviewer: audit-reviewer (S17, CM-026 fresh context)

### F-039 - Low - 2 Technical / 7 Blog

- **Observation:** 11 category and pagination archives are indexable ("index, follow"), have no meta description and 38-282 words; categories include off-entity topics (Telemedicine, Long Term Care, Health).
- **Evidence / Locator:** SRC-004 Meta Robots / Word Count; SRC-007 (Occurrences 0)
- **Classification:** Project Evidence
- **Confidence:** Corroborated
- **Alternative Explanation:** Archives can help crawl discovery of posts.
- **Alternative tested:** Not tested.
- **Recommendation:** Handle with the blog in the Blog Decision Map (taxonomy cleanup; any noindex is destructive -> CM-019). No change now. Expected impact: archives stop adding thin, off-entity pages.
- **Risk if Acted:** None now.
- **Risk if Deferred:** Thin archives stay indexable.
- **Dependency:** Blog Decision Map
- **Publication gate:** n/a
- **Affected:** /category/mobility-equipment/; /category/telemedicine/; /blog/page/2/; /blog/page/3/; /category/long-term-care/; /category/faqs/; /category/faqs/page/2/; /category/insurance-questions/; /category/uncategorized/; /category/announcements/; /category/health/
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

### F-040 - Low - 1 Baseline & measurement

- **Observation:** A GA4 tag (gtag.js?id=G-5GX2RP9PYX) and WordPress.com stats are loaded, but no GA4, GSC, call-tracking or form-delivery access exists for this audit; the conversion path (phone, form, upcoming photo-quote upload) is unvalidated.
- **Evidence / Locator:** SRC-001 external_all row 2 (googletagmanager gtag G-5GX2RP9PYX); S11 skipped (step outcomes)
- **Classification:** Project Evidence
- **Confidence:** Single-source
- **Alternative Explanation:** The client may hold GA4 access through another agency.
- **Alternative tested:** Not tested.
- **Recommendation:** Paul asks the client for GA4/GSC read access (or a VA check that forms deliver) before Build launches; measurement plan in the S18 package. Expected impact: a baseline to judge the rebuild.
- **Risk if Acted:** None.
- **Risk if Deferred:** Every performance claim after the rebuild stays unmeasurable.
- **Dependency:** Client access
- **Publication gate:** n/a
- **Affected:** /
- **Revision:** 1 (supersedes N/A) · status draft · reviewer: audit-reviewer (S17, fresh context)

