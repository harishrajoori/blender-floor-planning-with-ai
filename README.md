# Family-home planning — specifications before drawings

Latest owner-floor detail: [room placements agreed in conversation](properties/designs/PROPERTY-2-PLACEMENT-DECISIONS.md). NE is indoor living; Mallanna and daily pooja share a wall with west doors; deity facings north/west; kitchen open toward dining.

The active design is Property 2 in Lakshmipur near Chintakunta, Karimnagar area: **54 ft E–W × 66 ft N–S, west and south roads 30 ft each**. Ground is open for parking/garden/functions, first floor is the brother's **3BHK**, second floor is the owner's **two bedrooms plus office**, with a shared stair/lift and independent homes.

**Current status:** specifications revised 27 September 2026. Existing drawings/code are unapproved prototypes with known failures. No legal, structural, complete geometric or final Vaasthu validation is claimed.

## Start here

| Document | Purpose |
| --- | --- |
| [Owner brief](DESIGN-BRIEF.md) | Current family requirements and latest clarifications |
| [Generic plot specification](specifications/GENERIC-PLOT-SPECIFICATION.md) | Reusable plot, geometry, adjacency and building rules |
| [Family design rules](requirements/COMMON-DESIGN-RULES.md) | Required rooms, open-space rules, targets and ritual needs |
| [Property 2 extended design](properties/designs/PROPERTY-2-DESIGN.md) | Active site, floor programme, connections, area budget and holds |
| [Property 2 civil feasibility study](properties/designs/PROPERTY-2-STAIR-LIFT-STUDY.md) | Local authority research; NW stair/lift selected for trial, geometry pending |
| [Property 1 extended design](properties/designs/PROPERTY-1-DESIGN.md) | Separate west-road comparison study |
| [Property 3 extended design](properties/designs/PROPERTY-3-DESIGN.md) | Separate north-road comparison study |
| [Vaasthu rule profile](knowledge/VAASTU-RULE-PROFILE.md) | Owner choices, source preferences and unresolved consultant decisions |
| [Implementation and acceptance](specifications/IMPLEMENTATION-AND-ACCEPTANCE.md) | Shared model contract and 20 regression scenarios |
| [Code readiness review](reviews/2026-09-27-CODE-READINESS-REVIEW.md) | Current implementation gaps and evidence against an engineering design package |
| [Design review](reviews/2026-09-27-DESIGN-REVIEW.md) | Evidence of current defects and required corrections |
| [Decision log](reviews/DECISION-LOG.md) | Current clarifications followed by historical decisions |
| [Requirements JSON](requirements/home-requirements.json) | Machine-readable brief; current exporters do not consume it |
| [Property register](properties/README.md) | Site facts, active/inactive status and new-property template |

## Design decisions to preserve

- Living and dining are zones in **one open room** on both residential floors. No dividing wall, screen or TV partition.
- NE remains open and connects directly to living/hall. The owner permits the two separate pooja rooms farther inward/central; this needs explicit Vaasthu reconciliation.
- On the owner’s floor, a 4 ft clear passage runs east between daily pooja and the open SE kitchen to the covered utility balcony.
- Both Property 2 household main doors face north; the common core is approached independently from the site.
- One car and two bikes. No invented extra parking requirement, fixed column grid, shrine-facing direction or approved setback.

## What exists in this checkout

[src/generate_2d_plans.py](src/generate_2d_plans.py) builds Blender geometry; [src/export_2d_vector_blueprints.py](src/export_2d_vector_blueprints.py) independently builds SVG geometry. Both contain fixed coordinates and conflicting assumptions. Existing PNG/SVG/Blender files in [output](output/README.md) are evidence for review, not approved plans. This documentation revision does not regenerate them or change the source code.

Historical references to solver runs, ROADMAP/HANDOFF documents and passing validation suites describe files not present here. They must not be presented as current implementation status.

Next implementation should use one shared geometry model, explicit boundary types and independent checks, then issue dimensioned candidates for review. Only a selected, checked revision should drive presentation renders. The [specification index](ARCHITECTURAL-CIVIL-PLAN-SPECIFICATION.md) replaces the previous overconfident civil-plan document; its original and other pre-review documents are retained in the [archive](reviews/archive/2026-09-27-before-spec-review/README-ARCHIVE.md).
