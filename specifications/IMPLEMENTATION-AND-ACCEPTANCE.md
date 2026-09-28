# Implementation and acceptance contract

Revision: SPEC-2026-09-27-R1. Future implementation contract; validators described here do not yet exist in this checkout.

Read the [generic specification](GENERIC-PLOT-SPECIFICATION.md), [family rules](../requirements/COMMON-DESIGN-RULES.md), [requirements JSON](../requirements/home-requirements.json), and selected [property extension](../properties/README.md) before changing code.

## 1. One design model, multiple outputs

Required flow: requirements → property parameters → programme/area budget → adjacency and boundary decisions → dimensioned layout → independent geometry checks → SVG/Blender/schedules → visual review. Code must not invent partitions while exporting room rectangles.

The present two Python exporters each contain their own coordinates. Neither consumes the requirements JSON. They are prototypes to replace or refactor after design reconciliation, not a validated model or solver. Do not restore missing historical solver/version claims without checking the checkout.

| Model entity | Required fields |
| --- | --- |
| Revision | ID, parent, property ID, rules revision, source/input hashes, status |
| Site | Polygon, units, true-north transform, survey state, road segments, approved/provisional envelope |
| Level | ID, role, elevation, floor-to-floor rise, envelope |
| Space | ID, level, function, household, clear polygon, target range, origin, status |
| Activity zone | ID, parent-space ID, polygon, furniture/use requirements; no automatic walls |
| Boundary | ID, adjacent spaces/zones, type, geometry; OPEN_CONTINUOUS explicitly supported |
| Wall | ID, boundary ID, physical polygon, height, role, thickness/finish convention |
| Opening | Unique instance ID, host, cutout, connected spaces, usable width, sill/head, swing/facing |
| Furniture/fixture | ID, space, footprint, use clearance, orientation and delivery assumption |
| Structure/core | IDs, physical envelopes, level continuity, engineering/supplier state |
| Rule result | Rule ID, revision, PASS/FAIL/NOT_CHECKED/HOLD/NOT_APPLICABLE, measurements, evidence, reviewer |
| Exception | Rule ID, reason, alternative, owner/consultant decision where required, affected revisions |

Use `null` for unknown numeric inputs. A missing field cannot become zero, “not applicable” or PASS. A TARGET deviation needs an explicit record. A FIXED violation fails acceptance unless the underlying requirement is explicitly revised.

## 2. Living–dining contract example

This is a semantic example, not executable geometry:

```json
{
  "space": {"id": "L2_living_dining", "function": "living_dining"},
  "zones": [
    {"id": "L2_living", "parent": "L2_living_dining"},
    {"id": "L2_dining", "parent": "L2_living_dining"}
  ],
  "boundary": {
    "id": "L2_living_dining_interface",
    "between": ["L2_living", "L2_dining"],
    "type": "OPEN_CONTINUOUS",
    "wallAllowed": false,
    "doorAllowed": false,
    "fixedDividerAllowed": false
  }
}
```

The dimensioned candidate supplies zone polygons, shared-edge geometry, clear connection-strip polygon and resolved width. The validator reads actual wall/column/furniture polygons. It must detect a divider even if renamed `TV_backing`, drawn only by an exporter, or accompanied by an “open hall” label. Kitchen boundary type follows the floor-specific brief: the owner's L2 kitchen is now explicitly open toward dining; do not reinstate its former enclosure. Other floors retain their recorded decision.

## 3. Independent acceptance scenarios

Run these on every floor/candidate as applicable, against physical geometry rather than generator booleans. Report a failing object ID and location.

| Test | Positive evidence | Required negative regression |
| --- | --- | --- |
| A01 Programme | Counts match selected family/property option | Owner office replaced by bedroom; third brother bedroom silently added/removed |
| A02 Open living–dining | Shared room, no divider, clear direct connection | Add the existing 3.505 m wall at local y=4.064 m; must FAIL on both residential floors |
| A03 Furniture connection | Clear route with occupied chairs and sofa/TV | Remove wall but retain obstructing TV backing/unit; must FAIL where strip is obstructed |
| A04 Real openings | Host wall has physical cutout | Paint door/window symbol over solid wall; must FAIL |
| A05 Room reachability | Indoor paths to every room through permitted spaces | Require passage through bedroom, pooja or outside balcony; must FAIL |
| A06 Independent homes | Gate → common core → each entry while other locked | Reach L2 only through L1 dwelling; must FAIL |
| A07 Door facing | Outward normal matches selected property facing | Label east/west wall doorway “north entrance”; must FAIL |
| A08 Envelope | All occupied/projection/core geometry accounted for | Check only 37 × 40 ft rectangle while ignoring external core; must FAIL |
| A09 Dimensions/areas | Measured clear polygons agree with labels and schedules | Keep 13 ft 3 in master label on smaller geometry; must FAIL |
| A10 Pooja separation | No bath shared wall, opposing door or forbidden vertical overlap | Move bath above either shrine; must FAIL |
| A11 Vaasthu location | Footprint/activity overlap measured under selected method | Place east-central Mallanna and label it NE; must not PASS |
| A12 Ritual fit | Four places, altar, offerings, four pillars and entry all fit | Label a 1.6 × 1.25 m carpet “four-person verified” without fit evidence; must not PASS |
| A13 Light/air | Window cutout connects room to usable exterior/shaft | Window sits behind a core or wall; must FAIL relevant ventilation claim |
| A14 Parking/event use | Vehicle swept path and uninterrupted pedestrian/core routes | Extra stall blocks stair or parked car blocks sole route; must FAIL |
| A15 Core | Rises, run, landing, headroom and lift data agree | Draw symbolic flights without resolved level rise; HOLD, not PASS |
| A16 Vertical coordination | All levels/roof overlaid; load paths and service reservations identified | Claim open-to-sky on L1 beneath an L2 slab; must FAIL |
| A17 Export parity | SVG, Blender and schedules share object IDs, geometry/revision hash | Move Mallanna 600 mm in one exporter; must FAIL |
| A18 Evidence status | Unknowns remain HOLD/NOT_CHECKED | Missing survey yields “legal verified”; must FAIL |
| A19 Owner shrine arrangement | Mallanna north of daily, shared wall, separate west doors; deity vectors N/W respectively | Reverse shrine order, deity facing or remove shared wall; must FAIL |
| A20 Owner open kitchen / NE interior | L2 kitchen open to dining; NE is indoor living extension | Reinstate kitchen enclosure or replace NE living with terrace; must FAIL |

A12's capacity test must place people and use/entry clearances, not merely divide net area by a guessed area-per-person. A11's provisional zoning result cannot become final consultant acceptance.

## 4. Geometry and reporting conventions

Use one named geometric tolerance (proposed 1 mm for numeric comparisons) and separate display rounding. Tolerance must never relax an agreed minimum clear width. Calculate true clear sizes after wall/finish/column intersections; for irregular rooms report limiting dimensions and polygon area. Boundary contact, shared wall and vertical overlap require separate tests.

Access graphs require actual collision-free openings and routes of the specified width; connectivity between labels is insufficient. Furniture and door-swing tests must include dimensions and movement assumptions. Coverage is a classified geometric quantity under the applicable authority's definition, not automatically plinth area / plot area.

The report must enumerate all applicable rule IDs. Missing checks fail the completeness gate. Include measured values, selected thresholds, failed geometry, assumptions, deferred professional checks and summary by status. A high weighted score cannot override a failed fixed constraint.

## 5. Implementation sequence

1. Load the resolved brother 3BHK / NE-open / inward-pooja requirements; dimension the service passage and shrine placement while recording the Vaasthu hold.
2. Implement the shared model and input/status validation.
3. Build adjacency/boundary semantics and negative regression cases A01–A07 before rendering walls.
4. Develop a Property 2 site/core and room candidate with actual clear dimensions; run A08–A16.
5. Make both exporters consume that model; verify A17–A18 and inspect every sheet.
6. Issue a dimensioned candidate pack for owner review; record revisions before presentation rendering.

Generic model/validator work can proceed with unresolved property details represented explicitly. Final coordinate design cannot be declared frozen while envelope, critical dimensions or an applicable property programme remain unresolved. This documentation task intentionally leaves existing source and drawing artifacts unchanged.
