# Generic plot and residential design specification

Revision: SPEC-2026-09-27-R1. Status: design contract for concept development; no approved geometry.

This specification applies to any plot, road orientation or household programme. It defines how a design is described and checked. Family-specific requirements belong in [common rules](../requirements/COMMON-DESIGN-RULES.md); dimensions, floor roles and exceptions belong in a [property extension](../properties/README.md). A new property inherits rules, never another property's coordinates.

## 1. Authority, decisions and results

Mandatory legal and safety constraints cannot be overridden. If a fixed owner requirement conflicts with them or with another fixed requirement, report the conflict and develop alternatives; do not silently discard the requirement. Within that boundary, use the latest explicit owner decision, current family brief, property facts and selected consultant guidance. A generated drawing, code comment or previous AI statement is not an owner decision.

Every rule has an ID, scope, requirement, origin and strength:

| Strength | Meaning |
| --- | --- |
| FIXED | Owner requirement or necessary design-contract invariant; changes require an explicit decision |
| TARGET | Numeric concept-design target; deviations require a reason and fit evidence |
| PREFERENCE | Ranked design choice; report trade-offs |
| PROPOSAL | Candidate solution, not an approved owner requirement |
| HOLD | Missing survey, authority, engineering, supplier or ritual information |

Keep strength separate from check result: `PASS`, `FAIL`, `NOT_CHECKED`, `HOLD`, or `NOT_APPLICABLE` with a reason. PASS means only the named test passed for the named revision. Never use an overall “Vaastu compliant” or “structurally verified” badge as a substitute for evidence. Numeric targets below are project planning proposals, not statutory minima.

## 2. Plot input contract

| ID | Required input or rule | Evidence / acceptance |
| --- | --- | --- |
| G-SITE-01 | Boundary polygon, units, origin, bearing and survey status | Polygon closes, has positive area, no self-intersection; rectangular dimensions are explicitly an assumption until surveyed |
| G-SITE-02 | All roads independently recorded with side, width and source | Site gate connects to a real road; road width is not inferred from image scale |
| G-SITE-03 | True north is independent of page/camera rotation | North arrow and stored transform agree; assumed north remains unverified |
| G-SITE-04 | Authority, land use, widening, setbacks, coverage, height/floor and parking rules | Store applicable document, date, clause and reviewer; unknown values stay null/HOLD |
| G-SITE-05 | Entire development checked against permitted envelope | Include stair/lift core, walls, balconies, roof projections, ramps and services as applicable; classify any permitted projection explicitly |
| G-SITE-06 | Site gate, dwelling door position and outward door facing are separate | A west road does not force a west-facing dwelling door |

Use millimetres for model geometry; 1 ft = 304.8 mm exactly. Preferred site origin is the south-west reference corner, x east, y north, z up. For a rotated/irregular site, store a transform; never pretend its bounding box is the boundary. North-up drawings must reflect the same transform.

For an axis-aligned rectangle only: plot width = west offset + building width + east offset; plot depth = south offset + building depth + north offset. These are **building offsets**, not guaranteed clear statutory setbacks when a core or balcony projects into them. Report both wall-envelope and total-development extents.

## 3. Programme and area budget

G-PROG-01: Give each level a role, occupant household, required room counts and permitted optional spaces. Unknown counts remain unresolved. An office cannot satisfy a required bedroom count unless an owner decision changes the programme.

G-PROG-02: Create an area budget before room placement. Separate clear internal room areas, internal circulation, wall footprints, shafts, common core, covered external circulation, balconies, open terraces and ground garden. Calculate unions to avoid counting shared space twice. Never add living and dining zones to their enclosing shared-room area again.

G-PROG-03: For each space record ID, level, function, privacy, required neighbours, forbidden neighbours, clear-size target, furniture, ventilation, zone preference and source. A room rectangle alone is insufficient.

G-PROG-04: Test alternatives by changing envelope, adjacency or core strategy. If no feasible option is found, identify competing constraints and measured shortfall; one failed arrangement does not establish plot infeasibility. Remove optional additions before proposing changes to required rooms.

## 4. Adjacency and boundaries — decide before drawing walls

Separate **where people can move** from **what physically divides spaces**.

| Boundary type | Meaning | Representation |
| --- | --- | --- |
| OPEN_CONTINUOUS | Two activity zones in one room | No separating wall, door, arch infill, glass screen, jaali or built-in divider |
| WIDE_OPENING | Separate spaces with an unhinged opening | Explicit opening width, jambs and head height in a wall |
| DOOR | Enclosed space entered through a door | Wall opening, frame, usable clear width, leaf and swing |
| SOLID | Physical enclosure with no passage | Wall polygon and thickness |
| EXTERIOR_OPENING | Exterior door/window/vent | Actual cutout and external destination/air space |

G-OPEN-01: If the brief says open living–dining, model **one enclosed room `living_dining` containing two furniture/activity zones**. Their common edge is OPEN_CONTINUOUS. No wall or TV unit may be generated along that edge. A wall with a normal door or an arch does not satisfy this requirement. Kitchen enclosure is a separate, floor-specific decision; do not infer it from the living–dining rule.

G-OPEN-02: Store the living–dining shared edge and an obstacle-free connection strip in the property layout. Its width must meet the resolved primary-circulation target. The strip connects usable living and dining floor areas without leaving the shared room. Fixed obstructions must not intersect it; chair-use and door-swing envelopes must also be considered. Furniture elsewhere in the shared room is allowed when circulation and visual openness remain intact.

G-OPEN-03: A structural grid line is not a wall command. Do not introduce masonry to hide a column at an OPEN_CONTINUOUS boundary. Change the candidate structural arrangement with engineering review or report the conflict. An overhead beam must be identified separately and must not be represented as floor-to-ceiling infill.

G-ACCESS-01: Prove paths from site gate to common core to each independent dwelling entry. Repeat with each other household locked. Prove ordinary indoor access from the entry to living/dining, each bedroom, office, kitchen and common bath. A balcony detour does not replace required indoor access.

G-ACCESS-02: Bedrooms, offices, pooja rooms and bathrooms are not through-routes to unrelated spaces. An attached bath is deliberately accessed through its own master bedroom. A utility may be accessed through its kitchen only when the selected brief permits it and the working aisle remains safe. Do not encode this exception as a general right to route traffic through a kitchen.

G-ACCESS-03: Preserve a short common lobby for the common bath; screen its doorway from entrance, dining and pooja sightlines. Test these sightlines from actual standing/seated positions. A “private lobby” label does not prove privacy.

## 5. Rooms, openings and interiors

G-DIM-01: State finished internal dimensions, wall thickness and structural module dimensions separately. Labels, areas and schedules must be calculated from the same geometry. A rectangle bounded by wall centre lines cannot be labelled clear finished size.

G-WALL-01: Give every wall an ID, endpoints/polygon, thickness, height, role and adjacent space IDs. Keep partitions, exterior infill and structural elements distinct. Record finish build-up where it affects clear width.

G-DOOR-01: Every opening has a host wall or open-edge ID, interval/coordinates, type, clear width/height, sill/head and connected spaces. Physically subtract wall material at doors and windows. Reject a door symbol painted over a continuous wall, a floating door, or an opening that reaches the wrong space.

G-DOOR-02: Main-door facing is its outward normal, not the swing arc direction or a text label. Door leaves, handles and approach space must not clash with columns, fixtures or each other.

G-FIT-01: Model beds, wardrobes, sofa, TV, table/chairs, desks, appliances, sanitary fittings and shrines with both physical footprints and use clearances. Test occupied chairs and opening wardrobes. Do not pass a layout solely because bare furniture rectangles fit.

G-FIT-02: Document delivery routes for a sofa component, bed/mattress, wardrobe modules and refrigerator, including stair turns and doors. Record which items are flexible, disassembled or assembled in the room.

G-LIGHT-01: Every bedroom and office needs a useful exterior window. Living/dining needs direct exterior light and a demonstrated ventilation path. Kitchen/bath/utility openings must face exterior air or a real connected shaft/court; a remote “OTS” label does not ventilate a room. Show neighbouring obstructions and shading assumptions.

G-KITCHEN-01: Show hob, standing position/facing, sink, preparation worktop, refrigerator, storage, exhaust and service route. Utility stays a smaller service space and must not occupy the entire kitchen's required directional zone.

G-CLIMATE-01: Include west/south shading, rain-protected entry circulation and maintainable external access. Do not prescribe a full perimeter cantilever merely to make windows maintainable.

## 6. Whole-building coordination

G-CORE-01: Resolve stair floor-to-floor rise, integer riser count, tread/going, flight widths, landings, handrails, headroom and exit paths in plan and section. Total rises must equal the level difference. Repeated decorative treads are not a stair design.

G-CORE-02: Obtain lift supplier requirements for shaft, car, doors, pit, overhead and maintenance. Keep arrival outside private rooms, with clear landing and stair access. A “6-person” label does not establish usable capacity or equipment fit.

G-STRUCT-01: Develop load paths from roof through both homes to foundations while maintaining open ground use. Record spans and column/beam candidates. Member sizes, reinforcement, material grades, soil, seismic and wind design are engineering holds. Wall alignment alone does not verify an open-stilt structure.

G-STACK-01: Overlay wet areas, shafts, kitchens, pooja, columns, core and slab openings at every level. Test horizontal adjacency and vertical overlap separately. Shafts require physical space and service access; stacking sinks does not eliminate horizontal branch pipework.

G-OUT-01: Show parking mode and temporary event mode separately. Measure actual vehicles, gate openings and swept paths. Maintain pedestrian and core routes in both modes and state if a car must be moved for an event.

G-ROOF-01: Show roof access, tanks, solar, maintainable clear routes and structure/shading conflicts. Mark “open to sky” only when no upper slab, canopy or roof covers the marked polygon. Drawing-layer exclusions do not remove engineering obligations.

## 7. Vaasthu rule selection

Use the [project Vaasthu profile](../knowledge/VAASTU-RULE-PROFILE.md) when requested. For other families record their own selected tradition and requirements. Do not equate cultural preferences with proven health/wealth outcomes or municipal rules.

G-VAASTHU-01: Record which reference outline is assessed (plot, dwelling or room), its north transform, centre, zone method and revision. A conceptual 3×3 overlay is an analytical aid, not a nine-room construction grid or final pada calculation.

G-VAASTHU-02: Report room footprint overlap with preferred zones and the location of the relevant activity (sleeping area, hob or altar). Do not award PASS solely from a label/centroid. Until a consultant-specific zone threshold is selected, report measured overlap and HOLD on final zone acceptance.

G-VAASTHU-03: Keep room position, door facing, deity facing, worshipper facing and sleeping head direction separate. If preferences conflict, preserve fixed family needs and record alternatives for review.

## 8. Required drawing pack and release gates

Each candidate requires a common revision on the site plan; every occupied floor; open ground; roof; stair/core section; room/area schedule; wall/opening schedule; furniture and circulation plan; vertical coordination overlay; Vaasthu matrix; assumptions and validation report. Include a legend for solids, openings, windows and annotation-only lines.

| Gate | Evidence required | Permitted next step |
| --- | --- | --- |
| D0 Requirements reconciled | Fixed decisions traced; unresolved items identified with alternatives | Specification/validator development; exploratory layouts clearly marked provisional |
| D1 Concept feasibility | Envelope assumptions, area budget, adjacency, furniture, core and parking tested | Dimensioned candidate review, with survey/legal holds visible |
| D2 Geometry checked | No failed fixed functional checks; real openings; coordinated floors and consistent exports | Owner review of a named candidate; no blanket compliance claim |
| D3 Design selected | Owner selection recorded; all requested changes incorporated and rechecked | Presentation renders from frozen geometry |
| D4 Professional issue | Survey/authority, engineering, supplier and selected ritual reviews completed as applicable | Professional submission/construction documentation by responsible parties |

Current drawings have not passed D2. Documentation does not itself certify a candidate. Legal holds may coexist with an explicitly provisional concept, but never with a sanctioned/construction-ready claim.

## 9. Change control

Changes to programme, room boundary type, orientation, access, geometry or envelope must update the property revision and affected checks. Never edit SVG/Blender geometry independently to make an output look correct. Retain unresolved choices as separate alternatives, not silent defaults.

See [implementation and acceptance contract](IMPLEMENTATION-AND-ACCEPTANCE.md) for the model and regression requirements.
