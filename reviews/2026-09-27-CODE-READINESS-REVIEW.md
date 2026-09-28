# Code readiness for an engineering design package

Reviewed 27 September 2026 against requirements **SPEC-2026-09-27-R18**. Scope: both Python generators, their inputs/output paths, repository implementation inventory and selected geometry. Source and existing output artifacts were not changed. See [recorded measurements and source hashes](2026-09-27-CODE-READINESS-EVIDENCE.json).

## Verdict

**The present code cannot produce a 90%-complete engineered architectural/civil package.** It is a pair of fixed-coordinate drawing generators. It can produce illustrated floor-plan sheets, but neither imports the current requirements, computes a coordinated building design, nor rejects known invalid geometry. Re-running it will reproduce rejected requirements and inconsistencies.

No numeric completion percentage is assigned: there is no agreed weighted deliverable baseline, and several entire engineering disciplines and critical architectural checks are absent. Rendering success must not count as architectural or structural acceptance. The documentation is ahead of the implementation.

## Blocking findings

| Priority / finding | Source evidence | Consequence and correction |
| --- | --- | --- |
| P1 — confirmed requirements are not inputs | [Blender constants](../src/generate_2d_plans.py#L23) and [SVG constants](../src/export_2d_vector_blueprints.py#L20); neither module loads requirements JSON | Changing docs does not change the plan. Both retain six-person lift, old shrine layout, office NW/Bedroom 2 north, enclosed owner kitchen and NE sitout. Build one requirements-driven design model; trace each fixed requirement to geometry and a check. |
| P1 — rejected living/dining wall is generated | Blender lines 556–558; SVG lines 447–448 | Both floors get a 3,505 mm divider. The adjacent TV unit can obstruct the connection even after wall removal. Model one room with living/dining zones and reject any obstructing geometry. |
| P1 — some doors/windows overlay solid walls | Blender lines 567–575 retain the full wall through main/pooja door positions; lines 501–502 overlay a bathroom window on solid masonry. SVG lines 456–462 similarly overlay the pooja door. | Symbols are not physical openings; room reachability and ventilation are unproven. Use hosted wall cutouts and clearance/path checks. Not every opening is broken; several exterior walls are manually segmented. |
| P1 — two outputs describe different buildings | Blender Mallanna south-wall centre y=4.80 m vs SVG y=5.40 m (lines 580 and 474); main door at an interior x=7.315 m wall in Blender vs north exterior in SVG (lines 570 and 391) | One output cannot validate the other. Generate both from the same entities, openings, geometry and revision. |
| P1 — full-site fit is not checked | Blender core x=-2.40 m and plot west x=-2.4384 m (lines 209 and 43) | Only 38.4 mm remains to the assumed plot boundary, despite the claimed 8 ft west setback. Include core, wall, balcony and approach geometry in a surveyed/permitted envelope check. This is not a determination of the legally required setback. |
| P1 — stair/lift are schematic | Blender lines 221–244; SVG lines 585–599 | Landing depth is 850 mm but labelled 4 ft; stair heights are symbolic increments, not a floor-to-floor calculation. No resolved headroom, pit, overhead or supplier design. Derive the staircase from levels and model the selected four-person lift with three stops, no terrace stop. |
| P1 — structure is drawn without engineering | Blender lines 48–57, 195–200, 441–457, 465 | Fixed 230 × 450 mm columns, thin slab symbols and cantilever galleries have no load analysis, soil inputs, foundation/reinforcement design or coordinated structural system. A 115 mm partition cannot conceal a centred 230 mm column. Require engineer-supplied structure and verify architectural coordination. |
| P1 — dimensions and spatial arrangement fail the current brief | Blender lines 561–590, 653–673; SVG lines 459–479, 614, 639–658 | Blender kitchen/shrine gap is 621 mm vs required 1,219.2 mm. Master bounding clear size is about 3,522.5 × 3,776.5 mm before column intrusions, not the labelled 13 ft 3 in square. Shrine axes/order/shared wall and daily deity facing do not match the latest decisions. Measure actual usable geometry and derive labels from it. |

Further requirement drift: the ground plan represents a 24 ft south road, two cars and four bikes, versus the confirmed 30 ft road, one car and two bikes (Blender lines 337–342, 383–392; SVG lines 184–190, 240–249). The generated six-person label must not be changed to four without obtaining an appropriate cabin/shaft layout.

## Capability coverage

| Workstream | Current implementation |
| --- | --- |
| Floor-plan graphics and furniture symbols | Present; three SVG sheets can be generated |
| Current requirement ingestion / generic property support | Absent; fixed Property 2 coordinates duplicated in two modules |
| Corrected room plan and verified circulation | Incomplete and failing current fixed requirements |
| Geometry-derived dimension/area/opening schedules | Absent; many labels are literals |
| Actual integrated multi-storey model | Absent; Blender builds separate cut-plane scenes around z=0 |
| Stair section, roof plan, elevations and construction details | No generators found for these deliverables |
| Foundation, beam/slab/column design and reinforcement | No analysis or detailing implementation found |
| Plumbing, electrical and coordinated service drawings | No designed networks/calculations; fixture/sump symbols are not service design |
| Survey-specific permission, fire/accessibility and ventilation checks | No implemented validation found |
| Vaasthu / ritual checks | Hardcoded positions and claims; no implemented selected-rule evaluation or complete ritual fit |
| Cross-export consistency | Fails: independent coordinates and different openings/shrine positions |
| Automated architectural acceptance | A01–A20 are documented future checks, not executable tests |

For scope context, [BIS describes the National Building Code](https://www.bis.gov.in/national-building-code/) as covering development control, fire safety, materials, structural design, construction and building/plumbing services. Its overview also identifies competent-professional structural safety certification. This supports treating those as substantive design disciplines, not a small final sign-off task. It does not establish this plot's particular statutory requirements.

## What a credible near-complete architectural draft would require

Use a deliverable checklist rather than an unsupported “90%” label:

1. **Requirements/model:** load the latest brief; store units, axes, physical boundaries, openings, unknowns and decision origins once. Keep living/dining as one space. Do not infer walls from every activity-zone boundary.
2. **Dimensioned NW trial:** coordinate ground, brother's 3BHK, owner's floor and roof. Preserve agreed clear shrine dimensions, daily/Mallanna facing, open kitchen/NE living and north windows. Draw the north entry approach explicitly. Report every unresolved conflict.
3. **Independent checks:** implement A01–A20 plus the latest four-person/three-stop lift requirement, no roof stop, north room swap and fixed 4 ft passage. Check actual collisions, paths, clear sizes, openings and vertical relationships. Critical failures block acceptance; a high average score cannot hide one.
4. **Architectural drawing set:** produce site and dimensioned floor/roof plans, elevations, stair/lift sections, opening/area schedules and key wet-area/threshold/balcony details from the same model. Record source revision and assumptions on all outputs.
5. **Professional coordination:** incorporate surveyed boundaries and authority-confirmed envelope, structural engineer's scheme, supplier lift drawings and service design. Resolve their clashes before treating the architectural draft as near complete.

This is a feasible development direction, not a promise that the present layout will fit. The code can automate substantial drafting and consistency checking. A full engineered building package additionally requires actual structural, geotechnical and service work; these must inform the design during development, not be deferred to an assumed final 10%.

## Checks performed and limits

- Both Python files passed syntax parsing.
- The SVG exporter generated ground, brother and owner sheets in a temporary directory; all three parsed as XML. Temporary outputs were removed. This proves execution/file structure, not visual or design correctness.
- Instrumented the Blender layout functions with recording substitutes for geometry/material/render calls to inspect their requested coordinates. Independently captured both residential floors. Reconfirmed the divider, 850 mm landing, 38.4 mm boundary margin, master dimensions and 621 mm service gap.
- These substitutes did not execute Blender mesh/render operations. No fresh Blender render, structural calculation, complete collision/path audit or statutory validation was performed.
- No existing implementation test suite or validator module was found. The review measurements are evidence, not the future acceptance suite.

Recommended next implementation milestone: **one requirements-driven, dimensioned NW candidate with explicit failed/pending checks**, followed by matched exports. Further styling of the old sheets will not close these gaps.
