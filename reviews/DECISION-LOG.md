# Owner Decision Log

Later dated decisions override earlier generated plans or stale model files.

## Earlier decisions — retained history

| Date | Decision | Status |
| --- | --- | --- |
| 2026-09-24 | Property 1 is the current design focus: 50 ft E–W × 80 ft N–S, west road recorded 20 ft. | Historical; see latest decisions |
| 2026-09-24 | G+1 with owner family on ground and brother family on first; independent access and external stair. | Historical decision; apply latest floor roles |
| 2026-09-24 | Ground floor is two bedrooms plus home office, not 3BHK. | Historical decision; apply latest floor roles |
| 2026-09-24 | Property 1 ground-house main door should be on the north wall and face north; gates remain west-road access. | Historical Property 1 preference |
| 2026-09-24 | Separate daily and Mallanna pooja rooms in NE; no pooja/bath shared wall. | Retained; owner second floor |
| 2026-09-24 | Mallanna room: four-person clear worship space plus raised platform/table, four decorated pandal pillars and prasadam area. | Fixed; detailed ritual geometry open |
| 2026-09-24 | Current parking basis: one car and two two-wheelers. | Retained baseline |
| 2026-09-24 | No dedicated/permanent Patnam space. | Retained |
| 2026-09-24 | First-floor detailed programme is flexible; default independent 2BHK may be designed using best judgement. | Flexible |
| 2026-09-24 | Future south-road plot: investigate an east-facing house main door. | Preference |
| 2026-09-24 | AI images are visualization only; approved dimensioned geometry controls. | Fixed workflow |

## Latest decisions - 27 September 2026

These supersede earlier plot, floor-role and entrance assumptions for the active design.

| Date | Decision | Status |
| --- | --- | --- |
| 2026-09-27 | Property 2 confirmed as 54 ft E-W x 66 ft N-S, with 30 ft roads south and west. | Owner confirmed |
| 2026-09-27 | Ground is open for garden, parking and flexible family functions; brother on first floor; owner/family on second floor. | Fixed |
| 2026-09-27 | Include a lift with a shared stair/lobby route and independent household entrances. | Fixed |
| 2026-09-27 | North-facing household doors; favour extra open space east/north; investigate west-side stair/lift grouping. | Agreed design direction; exact fit remains a proposal |
| 2026-09-27 | Owner requests a less static, lower-effort workflow before proceeding to final realistic images. | Current workflow priority |
| 2026-09-27 | Owner clarifies that the priority is an intelligent local 2D generator reusing GitHub code, enforcing civil-planning and agreed Vaastu requirements. Manual desktop planning is no longer the primary recommendation. | Current workflow priority |
| 2026-09-27 | Owner requests roadmap, workflow/wireframes, cleanup of old designs and portable cross-AI continuation. Old source/designs archived with hashes; M1 integration trial is next. | Complete |
| 2026-09-27 | Constraint generator and multi-floor validator completed (M1-M4). Coordinated 2D Concept Pack issued as Run `RUN-2026-09-27-01` with 3 passing options (OPT-A, OPT-B, OPT-C). | Superseded implementation claim; independent review below |
| 2026-09-27 | Owner approves sensible human-architectural flow over blind rectangle packing: Bedroom 2 placed on North exterior wall with garden window, Simhadwaram facing North entering directly into Grand Living Hall. | Approved Design Direction |

## Generated Candidate Options — Run `RUN-2026-09-27-01`

Three coordinated candidate alternatives generated, dimensioned, and verified:
- **Option A (`OPT-A`) [Recommended]**: Fingerprint: `c6bf1eb9ef64_631c4a512410`. Owner Carpet: 923.3 sq ft, Brother Carpet: 813.8 sq ft, Total Res. Carpet: 1,737.0 sq ft, Circulation Efficiency: 80.1%, East Daylight Frontage: 85.0%. Balanced proportions, expansive East morning light in living hall, Bedroom 2 on North exterior garden facade, and net 4.65 m² clear Mallanna ritual floor.
- **Option B (`OPT-B`)**: Fingerprint: `d6492f9627c5_b1485a9803da`. Owner Carpet: 891.7 sq ft, Brother Carpet: 801.4 sq ft, Total Res. Carpet: 1,693.1 sq ft, Circulation Efficiency: 79.4%, East Daylight Frontage: 85.0%. Compact living configuration with expanded executive study and Bedroom 2 on North exterior wall.
- **Option C (`OPT-C`)**: Fingerprint: `15f9b0d459e6_f6b71f9db2eb`. Owner Carpet: 906.5 sq ft, Brother Carpet: 830.3 sq ft, Total Res. Carpet: 1,736.8 sq ft, Circulation Efficiency: 78.1%, East Daylight Frontage: 85.0%. Expanded dining alcove directly adjacent to SE kitchen and Bedroom 2 on North exterior wall.

See `designs/property-2/runs/RUN-2026-09-27-01/` for complete deliverables: `concept.pdf`, `concept_sheet.svg`, dimensioned floor SVGs, schedules, and validation report. Independent review below supersedes its readiness claim; repair and revalidate before owner selection or M7.

## Remaining open decisions

- Owner selection between Candidate Option A, Option B, and Option C.
- Survey, true north, road widening and legal envelope.
- Selected entrance-pada/toilet-sub-zone method and consultant.
- Exact first-floor programme before approval.
- Mallanna deity/image/facing and shrine measurements.
- Budget, construction phasing, accessibility and preferred local house references.

## Independent review correction — 27 September 2026

The earlier M1–M5 completion/owner-selection statement records an implementation claim, not an owner approval. Independent review found six failing contract regressions despite all existing suites passing. M2–M5 are reopened as needs-rework; current run artifacts are retained as a prototype. Read [the code review](2026-09-27-INDEPENDENT-CODE-REVIEW.md). No owner selection or rendering is requested until these defects are addressed.
