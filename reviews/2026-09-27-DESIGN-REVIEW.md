# Repository and design review — 27 September 2026

Review revision: SPEC-2026-09-27-R1. Scope: requirements, all existing Markdown references, requirements JSON, both Python exporters, available outputs and visual inspection of the owner's second-floor PNG. Static geometry checks were performed; Blender/export generation was not run. Existing source and drawing files were left unchanged during this documentation work.

## 1. Conclusion

The current drawings are **not acceptable as the implementation/design baseline**. Written requirements are not connected to the generators, geometric claims are frequently labels rather than measured results, and the two exporters diverge. The owner's living–dining complaint is confirmed in both sources.

The replacement contract is now layered: [generic plot](../specifications/GENERIC-PLOT-SPECIFICATION.md), [family rules](../requirements/COMMON-DESIGN-RULES.md), [property designs](../properties/README.md), [Vaasthu profile](../knowledge/VAASTU-RULE-PROFILE.md), and [implementation/acceptance](../specifications/IMPLEMENTATION-AND-ACCEPTANCE.md). Existing drawings still need redesign and revalidation against it.

## 2. Findings, evidence and required correction

Line numbers refer to source inspected in this review. Source links identify the files; named objects/coordinates remain useful if line numbers move.

| ID / severity | Evidence | Consequence / required correction |
| --- | --- | --- |
| R01 / blocking | [Blender source](../src/generate_2d_plans.py), lines 556–558, creates `Dining_Living_Partition` across x=3.810…7.315 m at y=4.064 m; [SVG source](../src/export_2d_vector_blueprints.py), lines 447–448, creates the same 3.505 m partition. TV furniture is also placed along it. | Violates open living–dining on both floors. Represent one room/two activity zones; remove wall-generation semantics and redesign TV/furniture location. Test A02/A03. |
| R02 / blocking | Blender lines 567–575 create a continuous x=7.315 m wall, then overlay main-entry and daily-pooja door graphics. SVG lines 456–462 also draw a continuous pooja wall beneath the door symbol. | Door graphics do not create openings. Require physical cutouts and valid connected spaces, A04/A05. |
| R03 / high | Blender lines 501–502 retain solid west wall across the bath ventilation span and place a window over it; SVG west-wall rectangles and window symbols similarly overlap. | Ventilation/light claims are not demonstrated. Subtract openings and check actual external air connection, A04/A13. |
| R04 / blocking | Blender `Simhadwaram_D1_NNE` is on x=7.315 m at y=10.60; SVG places its main door on the north exterior boundary near x=7.35 m. | Entry position/facing differs between outputs. A north-facing label is not evidence of a north-wall opening. Use one model and outward normals, A07/A17. |
| R05 / high | Blender Mallanna uses y=4.80…7.24 m; SVG uses y=5.40…7.84 m. The south boundary differs by 600 mm. | The exports are distinct plans; utility gap and circulation cannot share one validation result. A17 must detect this. |
| R06 / high | Blender master internal bounding faces give about 3.5225 × 3.7765 m before local column intrusions; both outputs label it 13 ft 3 in × 13 ft 3 in (about 4.0386 × 4.0386 m). | Room labels are not derived from geometry. Compute clear dimensions and irregular intrusions, A09. |
| R07 / high | Declared columns are 230 mm wide; the x=7.315 m encasing partition is 115 mm. | “100% embedded / zero exposed columns” is unsupported: equal centre lines leave 57.5 mm projection each side. Redesign/record structural envelopes instead of adding unwanted walls. |
| R08 / high | Main footprint west offset is 2.4384 m; external core extends to x=-2.40 m in the same plinth-local frame. | Only 38.4 mm remains to assumed west plot edge. Main-wall offset is not a clear setback/driveway. Evaluate total development and authority rules, A08. |
| R09 / high | Blender kitchen north wall ends at y=4.1215 m and Mallanna south wall starts at y=4.7425 m. | Candidate passage there is about 621 mm before further obstructions, far below the current 1,200 mm target. SVG's moved shrine creates a different gap. Dimension and fit the revised kitchen–pooja service passage. |
| R10 / high | Blender landing runs y=6.65…7.50 m (850 mm) but is labelled 4 ft × 8 ft. Treads are symbolic; source and prose disagree about floor heights (3.0/3.3 m). | No completed stair/landing/headroom/lift fit evidence. Resolve plan plus section and supplier data, A15. |
| R11 / high | Mallanna carpet is 1.6 × 1.25 m = 2.0 m² in both implementations; claims elsewhere refer to 4.65 m². Four pandal pillars and complete use envelopes are not demonstrated in the shrine layout. | Four-person ritual capacity is unverified. Explicit people/shrine/offering/pillar/entry fit is required, A12. |
| R12 / high | Existing docs alternated 2BHK/3BHK and NE/ENE/east-central pooja. Ground drawings label four bikes; owner requirement is two. | Programme drift. Latest owner clarifications resolve brother 3BHK and allow inward pooja with open NE; parking remains one car/two bikes. Update future model, not just labels. |
| R13 / high | Former root specification asserts a 60% statutory coverage limit, engineered RCC sizes/grades and all-PASS Vaasthu matrix without site-specific approval or calculations. | Claims withdrawn from active documents. Legal, structural and selected ritual/pada checks remain HOLD. |
| R14 / high | README offsets differed from code; root prose had two cars/four bikes and invented infrastructure. Research/JSON referenced absent solver runs, reviews and handoff files. | Documentation could not be treated as one current contract. Reconciled active files, retained original claims only as marked history. |
| R15 / high | NE sitout was labelled open-to-sky without a coordinated roof/upper-floor void demonstration; current user requires openness, not necessarily an unroofed space on every level. | Specify connection and actual coverage separately. Add roof/core section and A16. |

## 3. Owner clarifications incorporated

- Brother first floor: **3BHK** (explicit response in this review).
- NE remains open and connects to living/hall.
- Two separate pooja rooms may be inward/central; do not continue enforcing the old mandatory NE placement.
- Kitchen compartment must leave a gap and usable utility-door approach. Working spatial interpretation: dining/common circulation → passage between kitchen and pooja → utility beyond kitchen. This interpretation remains distinguished from an approved coordinate layout.
- Living–dining has no partition. Existing open-plan brief plus the user's explicit wall complaint make this a fixed rejection condition.

## 4. Specification conflict resolutions

| Earlier conflict | Current disposition |
| --- | --- |
| Owner versus safety hierarchy inconsistent | Safety/legal constraints mandatory; fixed owner conflicts must be surfaced, not silently overridden |
| NE shrine versus NE open | Latest owner NE-open / inward-pooja decision governs; central Vaasthu trade-off remains HOLD |
| 2BHK versus 3BHK brother | 3BHK confirmed; no unresolved bedroom-count choice |
| Open hall versus TV/structural partition | One living–dining room; structure/furniture must adapt or report conflict |
| 37 × 40 ft plinth and 16-column grid called fixed | Retired as approved assumptions; candidate envelope and structural scheme must be developed |
| Conflicting setback numbers | No statutory offsets selected; old main-rectangle offsets retained only as review evidence |
| Fixed east/north deity facing and daily-room cap | Ritual choices unresolved; dimensions must follow actual fit |
| Walkaround slab and sealed 2 ft gap treated as necessities | Optional envelope solution; functional service passage proposal replaces arbitrary cavity |
| Missing P1/P3 records | Reconstructed from existing records, marked historical/unverified, with separate extended studies |
| Missing source PDFs | Existing research preserved as historical synthesis; no claim of independent rereading |
| Old TG-bPASS workflow assumed current | Official BuildNow sources checked; exact site jurisdiction/rules remain unresolved |

The official [BuildNow portal](https://buildnow.telangana.gov.in/) and [GO/Act register](https://buildnow.telangana.gov.in/go-and-act/) were checked for current authority context. No plot-specific legal limit is inferred from them. The practitioner-source reassessment and central-pooja hold are documented in the [Vaasthu profile](../knowledge/VAASTU-RULE-PROFILE.md).

## 5. Handoff and verification scope

Specification revision R1 is sufficient to begin the shared data model and acceptance-check implementation. It is not sufficient to call final room coordinates, stair fit, structure or legal envelope frozen. Each property extension distinguishes required relationships, target sizes, proposals and unresolved inputs.

Next design work must implement A01–A18, refit Property 2's envelope/core and rooms, produce consistent dimensioned outputs, and then request selection of a concrete candidate. No presentation render should be passed off as a corrected design before those checks.

Pre-review documents, including existing uncommitted edits to the common rules and root specification, are preserved with hashes in the [archive](archive/2026-09-27-before-spec-review/README-ARCHIVE.md). Source and existing generated artifacts were not regenerated or changed by this documentation review.

See [documentation verification](2026-09-27-SPECIFICATION-VERIFICATION.md) for the checks performed on the delivered document pack. Those checks validate documentation integrity, not architectural feasibility.
