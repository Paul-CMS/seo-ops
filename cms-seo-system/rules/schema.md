# Schema (decided further at the first schema step)

SCH-01 Homepage: root WebPage; Corporation nested as author, creator, publisher, provider, all one @id (the ID page URL).
SCH-02 Homepage `about`: Wikipedia + kgmid refs for service category, area entity, county, metro, state. `mentions` for context; `disambiguatingDescription`.
SCH-03 Homepage `sameAs`: every citation URL; add each new citation immediately.
SCH-04 GBP location entity type: deferred to the first schema step. Default: the most specific schema type matching the GBP category (not HomeAndConstructionBusiness for non-home-service clients).
SCH-05 Service pages: Service or WebPage; no LocalBusiness, no location data.
SCH-06 Non-GBP location pages: Article or WebPage; never LocalBusiness.
SCH-07 GBP landing location page: LocalBusiness subtype with sameAs and hasMap.
SCH-08 Blog posts: Article with author (company owner unless told otherwise), datePublished, dateModified.
SCH-09 Follow bb-schema-builder node sets; no schema for pages whose URL or content isn't final.
SCH-10 Reference implementation: woodlawntrees.com (maricopa.felling.pro superseded). Compare against Local Schema output at Finish.
