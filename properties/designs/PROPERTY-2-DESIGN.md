# Property 2 — extended architectural design specification

Revision: P2-SPEC-2026-09-27-R18. Active design. Status: owner programme reconciled; spatial design contract, **not a dimensioned or approved construction plan**.

Inherits [generic plot specification](../../specifications/GENERIC-PLOT-SPECIFICATION.md), [family rules](../../requirements/COMMON-DESIGN-RULES.md), [Vaasthu profile](../../knowledge/VAASTU-RULE-PROFILE.md) and [acceptance contract](../../specifications/IMPLEMENTATION-AND-ACCEPTANCE.md). [Site record](../PROPERTY-2-CORNER-WEST-SOUTH-54x66.md) contains owner-confirmed plot facts.

Latest conversation decisions: [owner-floor placement record](PROPERTY-2-PLACEMENT-DECISIONS.md). Mallanna axes are confirmed: 7 ft E–W × at least 9 ft N–S. Daily pooja is confirmed 7 ft E–W × 4 ft N–S, sharing the same E–W span. Both sizes are confirmed clear inside finished walls, with wall/finish thickness additional.

## 1. Site facts and unresolved envelope

| Item | Value | Status |
| --- | --- | --- |
| E–W × N–S | 54 × 66 ft = 16,459.2 × 20,116.8 mm | Owner-confirmed; rectangular survey assumption |
| Arithmetic area | 3,564 sq ft = 331.10643456 m² = 396 sq yd | Arithmetic, not title/survey area |
| Roads | West 30 ft; south 30 ft | Owner-confirmed; widening/levels unverified |
| Location | Lakshmipur near Chintakunta, Karimnagar area, Telangana | Owner-confirmed locality; survey/parcel authority unresolved |
| Main doors | North-facing for both homes | Fixed; not a north-road claim |
| Core | Shared NW stair/lift is the owner-selected first trial | Exact footprint, approach and fit unresolved |
| Open space | Favour usable east/north garden; NE open and linked to hall | Owner requirement/direction |
| Setbacks, permitted height/coverage | Unknown | HOLD; obtain applicable authority/survey requirements |

Use north-up site coordinates, origin at assumed plot SW: `(0,0)`, SE `(16459.2,0)`, NE `(16459.2,20116.8)`, NW `(0,20116.8)` mm. This is a concept convention until surveyed; do not confuse it with the old code's plinth-local origin.

The former 37 × 40 ft rectangle at west 8 ft / south 9 ft leaves east 9 ft / north 17 ft **to that rectangle**. Its 1,480 sq ft footprint is 41.53% of plot area, excluding the external core and projections. This calculation neither approves the envelope nor establishes statutory coverage. The 2.40 m-wide external core consumes almost all of that 2.4384 m west offset, leaving only 38.4 mm to the assumed plot edge before other construction. Retire “8 ft clear west setback/driveway” as a verified claim.

P2-SITE-01: dimension the entire site/core/building arrangement before choosing a dwelling rectangle. Keep corner access, road sightlines, pedestrian approach and garden usable. Do not fix a gate simply because a prior SVG drew one.

## 2. Locked programme and optional spaces

| Level | Required design programme | Optional / unresolved |
| --- | --- | --- |
| G / L0 | Open parking for one car + two bikes; garden/play; temporary family use; shared independent core | Guest toilet, event counter and storage are proposals; no permanent event capacity |
| First / L1 | Brother's **3BHK**, open living–dining, enclosed SE kitchen, utility, common bath, master attached bath, independent north entry | Daily pooja proposed; additional lounge/terraces only if fit and budget permit |
| Second / L2 | Owner's **2 bedrooms + office**, open living–dining and SE kitchen, utility, common bath, master attached bath, separate daily/Mallanna rooms, independent north entry | Exact room sizes, shrine details and balcony treatment |
| Roof | Access, tanks, solar, maintainable circulation | Tank capacity, equipment, structure and layout unresolved |

The owner fixed 3BHK during this review. There is no pending 2BHK selection. NE openness and inward pooja replace the former requirement that both pooja rooms occupy NE. Do not convert the owner's office into a third bedroom.

## 3. Intended spatial arrangement

This is zoning and connectivity, not a grid of nine rooms and not a scale drawing.

| Region | L2 design intent | L1 adaptation |
| --- | --- | --- |
| SW | Master sleeping and cupboards | Master bedroom |
| West interior | Attached bath immediately north of SW master, master-only access; common bath farther north, entered from short shared lobby near Bedroom 2/office, screened from living/dining | Coordinate same service band |
| NW frontage | Bedroom 2 after owner-requested swap; north-facing window and independent common indoor door | Bedroom 2 |
| North frontage immediately east of Bedroom 2 | Personal office after owner-requested swap; north-facing window and common indoor door; NE living extension farther east | Bedroom 3 |
| Centre / connected family zone | One living–dining room; no divider; north entry leads directly into this room | Same open-space rule |
| NE | Indoor living area / extension, no separating wall or terrace | Preserve open connection; L1 coverage separately unresolved |
| East side after NE living | Mallanna then daily pooja, enclosed with shared wall and independent west doors | One daily pooja candidate; remaining space may expand family area |
| SE | Cooking counter on east wall; cook faces east; west side open to dining; counters/work aisle clear of utility passage | Stack kitchen where practical |
| Immediately south of daily pooja, north of kitchen | 4 ft clear passage, running east from dining to utility | Match service route where possible |
| Outside dwelling on east side | Covered, ventilated service balcony with washing machine and sink; reached at east end of 4 ft passage | Match services and maintain privacy |

P2-ZONE-01: reserve NE open space and the living–dining route **before** placing shrines. Do not push Mallanna to a leftover box merely to preserve an arbitrary grid. Pooja may be central as the owner requested, but its precise location must show the centre reference and Vaasthu trade-off rather than claiming blanket compliance.

P2-ZONE-02: the inward pooja grouping is not permission to create a central block that divides living and dining. If the two rooms, service gap and living routes do not fit, revise the envelope/adjacency and report the shortfall. Do not add a hall partition as a workaround.

## 4. Connections and boundary schedule

The IDs below identify design relationships; actual wall/opening IDs and coordinates are supplied by the later dimensioned candidate.

| ID | Connection | Required boundary / route |
| --- | --- | --- |
| P2-C01 | Road → gate → common stair/lift | Outdoor/common route; separate pedestrian and vehicle movement |
| P2-C02 | Core arrival → each north home door → living/hall | Protected common approach, independent lockable entry |
| P2-C03 | Living ↔ dining | **OPEN_CONTINUOUS**; one room; no wall, doorway, TV partition or fixed divider |
| P2-C04 | Living/hall ↔ NE area | On L2, continuous indoor living extension, no terrace or separating wall |
| P2-C05 | Living/common circulation → office / non-master bedrooms | Individual doors; no through-room route |
| P2-C06 | Common/private lobby → SW master → attached bath immediately north | Master door then private bath door; attached bath has no common-circulation entrance; SW corner remains sleeping |
| P2-C07 | Short shared lobby near Bedroom 2/office → common bath | Bath on west side north of attached bath; doorway screened from living/dining; no bedroom transit |
| P2-C08 | Hall/pooja approach → daily pooja; → Mallanna | Independent west-wall doors; rooms share one wall, no through-shrine route |
| P2-C09 | Dining → kitchen | L2 kitchen west side is open toward dining, with east-wall cooking and cook facing east; do not add an enclosing wall/door at the west interface. L1 separately specified. |
| P2-C10 | Dining → passage → utility | 4 ft (1,219.2 mm) clear N–S width; passage runs east, with daily pooja north and open kitchen south |

P2-C10 follows the clarified sequence: Mallanna → daily pooja → utility passage → open SE kitchen. No shared kitchen/pooja wall is assumed for this candidate; do not introduce a hidden double-wall cavity. Exact side-by-side placement and door swings must be shown in the next dimensioned layout. If a different contact relationship is requested later, record that change before drawing it.

The owner has fixed this service passage at **4 ft / 1,219.2 mm clear width**, measured N–S after finishes. This overrides the generic 1,200 mm target; do not shrink it or apply the short-route deviation allowance. Pooja/utility doors and kitchen counters must not consume the required path when used. The existing 600–700 mm residual slot must not be called a usable passage.

## 5. Provisional room and area schedule

Numbers below are **starting reservations**, selected from family targets to test feasibility. They are not measured clear sizes of the old plans and are not approved dimensions. The later model must compute actual sizes and furnish each room. Pooja dimensions come from the owner. Both room axes are confirmed: Mallanna 7 ft E–W × at least 9 ft N–S, daily pooja 7 ft E–W × 4 ft N–S. Both sizes are owner-confirmed clear inside finished walls. Area entries use the stated daily dimensions and minimum Mallanna length; add all wall/finish thickness separately.

| Space | L2 starting clear target | Area sq ft | L1 change |
| --- | --- | ---: | --- |
| Living activity zone | 14 × 12 ft | 168 | Same |
| Dining activity zone | 10 × 9 ft | 90 | Same; no dividing wall |
| Master sleeping | 12 × 14 ft | 168 | Same |
| Bedroom 2 | 11 × 12 ft | 132 | Same |
| Office | 9 × 10 ft | 90 | Replace with Bedroom 3, 11 × 12 ft / 132 sq ft |
| Kitchen | 9 × 11 ft | 99 | Same |
| Utility | 4 × 6 ft provisional reservation; covered exterior balcony with washer/sink | 24 | L1 type/fit separately unresolved; appliance fit may enlarge |
| Master bath | 5 × 8 ft | 40 | Same |
| Common bath | 5 × 8 ft | 40 | Same |
| Daily pooja | Owner confirms 7 ft E–W × 4 ft N–S; clear inside finished walls, wall thickness additional | 28 | L1 retains proposed 5 × 5 ft / 25 sq ft |
| Mallanna pooja | Owner 7 ft E–W × at least 9 ft N–S; clear inside finished walls, wall thickness additional | 63 at minimum length | Not required on L1 |
| Total room/activity reservations | — | **942** | **918** including proposed daily pooja |

Living + dining = 258 sq ft within **one** room. Do not count another 258 sq ft enclosing space. Entry niche is within living in this budget. Owner utility is confirmed external and covered. Its 24 sq ft provisional reservation remains in this mixed space budget and must be classified separately from internal room area in the final schedule; size is not yet owner-confirmed. Include its slab/roof projections in the full site-envelope check.

Additional provisional reservations per level: common/private/service circulation 100–150 sq ft (excluding paths already inside rooms); walls/shafts 120–180; shared core/landing 180–260. On L2, NE living is part of the living reservation, not an extra terrace area; enlarge the living reservation if fit requires it. At the minimum Mallanna length this gives **1,342–1,532 sq ft on L2**, before any living enlargement, balconies or separate covered approach. L1 retains its separate unresolved NE reservation of 120–150 sq ft and total **1,438–1,658 sq ft**. These sums mix differently classified areas for space budgeting; they are not statutory floor area/coverage.

Consequently a 1,480 sq ft dwelling rectangle alone does not prove the complete arrangement fits. Avoid forcing this schedule into it. Measure polygon unions and final circulation before reporting feasibility. Wall thickness and core dimensions remain design inputs requiring resolution.

## 6. Mallanna and daily pooja fit

P2-RITUAL-01: in Mallanna draw the localized raised platform/table, deity, prasadam zone in front, all four decorated pillars, four worshipper positions, storage and clear doorway/approach. Pandal pillars are not RCC columns. Do not overlap the four-person reservation with offerings, door swings or circulation needed during worship.

The prior 1.6 × 1.25 m carpet is only 2.0 m²; its label does not prove four-person usability. Nor is the historical 4.65 m² figure an owner-approved universal minimum. Test the actual ritual arrangement in the owner's 7 ft E–W × minimum 9 ft N–S room specification (clear inside finished walls, wall thickness additional) and revise with family/pujari dimensions.

P2-RITUAL-02: both west door positions are owner-confirmed. Mallanna deity faces north, altar toward south, opposite worshipper faces south. Daily deity faces west, altar toward east, opposite worshipper faces east. The two closed rooms share a wall, with Mallanna north of daily pooja. Daily room is 7 ft E–W × 4 ft N–S, matching Mallanna's E–W span. Their shared wall runs E–W; it is Mallanna's south wall and daily pooja's north wall.

P2-RITUAL-03: the kitchen/passage buffer provides physical separation and utility access, not proof of religious compliance. Keep exhaust, heat, wet services and bathroom conflicts out of shrine use zones. Ventilation requires a real opening/duct route.

## 7. Ground, core, section and roof

Ground: draw normal parking and temporary event modes. The car/bike positions, garden and core must remain usable; state whether vehicles move for family functions. Fixed stage, catering equipment, second car and four-bike programme are not required. Keep play space separate from vehicle turning.

Owner selects **NW as the first core option to test** in the [civil feasibility study](PROPERTY-2-STAIR-LIFT-STUDY.md). Exact geometry and the covered north gallery remain unapproved. First test Bedroom 2/office north windows, common arrival and the full building envelope. Retain west-central as a fallback if NW cannot fit; do not silently relocate confirmed rooms. Owner is unsure of layout/LRS approval, which remains unverified.

Lift capacity is owner-confirmed as **four persons**. Select supplier/model and verify cabin, door, shaft, pit, overhead and landing dimensions before fixing the core. Ground and both residential floors are the three required stops; owner confirms no terrace stop. The shared staircase continues to the terrace. Wheelchair fit is not established by this capacity choice.

Core: resolve full stair/lift footprint inside the lawful development envelope. The common arrival route should not run through bedroom balconies or a shrine. Detail last-flight arrival, lift door, landing, north entrance and overhead cover on **both** upper floors. Select floor heights before stair calculation; the historical 3.0 m and 3.3 m values conflict.

Structure: preserve open ground without claiming 16 columns or 230 × 450 mm members are engineered. Test spans and loads, including rooftop tanks and projected balconies; no ad hoc living–dining wall for structural concealment. A narrower partition cannot fully conceal a wider column without a real thickening and reduced clear dimensions.

Roof: coordinate tank, solar, stair headroom, lift overhead and maintenance access. Omit bore/drain-system indicators from owner sheets; drainage/waterproofing remain required in engineering coordination. L2 NE is indoor living; do not create a terrace void. Resolve L1 coverage separately in section.

## 8. Current validation status and decisions still needed

| Check | Status at this documentation revision | Next evidence |
| --- | --- | --- |
| Plot dimensions/roads and floor roles | Recorded; not surveyed | Survey/authority inputs |
| Brother 3BHK; owner 2 bedrooms + office | Requirement resolved | Future programme geometry check |
| Open living–dining | Existing code FAIL | Replace partition-generating logic and obstructing TV arrangement |
| NE open and connected | L2 indoor living confirmed; geometry NOT_CHECKED | Internal continuity; separate L1 coverage decision |
| Inward/central pooja | Owner direction recorded; Vaasthu HOLD | Footprint overlap, selected centre rule and consultant review |
| Kitchen-gap utility route | Route and 4 ft clear width owner-confirmed; fit NOT_CHECKED | Door/counter placement and maintained width |
| Room, stair, parking and full-site fit | NOT_CHECKED for revised programme | New coordinated candidate |
| Structure/legal/pada/ritual detail | HOLD | Named professional/family decisions |
| Drawing consistency | Existing source FAIL | Shared model, matching exports and independent checks |

Before freezing coordinates, resolve the survey/envelope or declare a specific provisional envelope, choose floor heights and core equipment assumptions, fit the central shrine/service arrangement, and record actual furniture/ritual dimensions. Budget, accessibility needs, parcel-level jurisdiction and first-floor optional daily pooja remain open. Locality is now owner-confirmed as Lakshmipur near Chintakunta. They do not prevent generic model/validator development.

No current floor plan is accepted by this document. Use the [review findings](../../reviews/2026-09-27-DESIGN-REVIEW.md) and acceptance cases A01–A20 when implementing the next revision.
