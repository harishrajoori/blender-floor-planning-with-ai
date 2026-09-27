# Blender Floor Planning with AI — Civil Engineering & Vaastu CAD Engine

[![Blender Version](https://img.shields.io/badge/Blender-5.2.2%20LTS-E87D0D?logo=blender&logoColor=white)](https://www.blender.org/)
[![License](https://img.shields.io/badge/License-Proprietary-blue.svg)](#)
[![Vaastu](https://img.shields.io/badge/Vaastu-Telugu%20%2F%20Telangana%20Compliant-gold)](#)
[![Status](https://img.shields.io/badge/Civil%20Status-Verified%203--Bay%20Structural-emerald)](#)

> **Civil Engineering & Vaastu-Compliant 2D Architectural Floor Plan Engine** powered by local Blender 5.2.2 LTS and Python constraint geometry.  
> Directly tackles and eliminates the "disconnected boxes" problem by enforcing a continuous **3-bay structural grid (16 RCC columns)**, verified load-bearing wall stacks, 1:1 vertical plumbing shafts, and strict **Telugu/Telangana Vaastu Shastra** alignment.

---

## 🏛️ Project Brief: Property 2 (54' × 66' Plot, SW Corner)

- **Location & Orientation:** South-West corner plot with **30'-0" West Road** (primary access & gate) and **30'-0" South Road** (secondary corner access).
- **Plot Dimensions:** $54'\text{-}0" \text{ (EW)} \times 66'\text{-}0" \text{ (NS)} = 3,564 \text{ sq.ft}$.
- **Approved Plinth Footprint:** $37'\text{-}0" \text{ (EW)} \times 40'\text{-}0" \text{ (NS)} = 1,480 \text{ sq.ft}$.
- **Setback Clearances:** South: $9'\text{-}0"$, West: $8'\text{-}0"$, North: $6'\text{-}0"$, East: $5'\text{-}0"$.
- **Structural Core:** 16 RCC Columns ($9" \times 18"$) spanning a 3-bay structural grid ($12'\text{-}6", 11'\text{-}6", 13'\text{-}0"$).

---

## 📐 Floor-by-Floor Program Breakdown

### 1. Ground Floor (Level 0, +0.00m) — Stilt Parking, Pavilion & Gardens
- **Sheltered Function Pavilion ($37'\text{-}0" \times 20'\text{-}4" \approx 750\text{ sq.ft}$):** Open-air plinth verandah for traditional family gatherings, festival pandals, and celebrations.
- **Covered Parking Bay:** $9'\text{-}0" \times 18'\text{-}0"$ sedan/SUV car stall + dedicated 4 two-wheeler parking stalls in the East driveway zone.
- **North & East Gardens:** $15'\text{-}0"$ deep North front lawn and expansive East morning plantation setback.
- **External Vertical Core (NW Vayu Zone):** Dog-legged staircase ($7'\text{-}3" \times 11'\text{-}0"$) and 6-PAX passenger elevator shaft ($1.6\text{m} \times 1.6\text{m}$ clear) located **completely outside the residential envelope** for independent access.

### 2. First Floor (Level 1, +3.00m) — Brother's 2BHK Residence
- **Master Bedroom (SW Niruthi):** $12'\text{-}6" \times 13'\text{-}4"$ with full-width built-in wardrobe, headboard facing South, and private access to spacious attached bath.
- **Spacious Bathrooms (West Varuna):** $6'\text{-}0" \times 8'\text{-}6"$ attached and common bathrooms with separate wet/dry zones over a continuous plumbing duct (OTS).
- **Modular Kitchen (SE Agneya):** $12'\text{-}6" \times 11'\text{-}6"$ with L-shaped granite counter, East-facing cooktop, corner sink, and pantry cupboards.
- **External Out-of-House Utility Balcony:** Washing machine, laundry sink, and gas cylinder station situated outside the kitchen envelope.
- **Grand Living & Dining (Brahmasthana):** $18'\text{-}0" \times 14'\text{-}0"$ completely open hall with built-in TV console, L-shaped sectional sofa, and 6-seater dining table.
- **Bedroom 2 (North Vayu):** $11'\text{-}6" \times 11'\text{-}6"$ with full wardrobe, study desk, and North balcony door.
- **Pooja Mandir (East-NE):** $4'\text{-}6" \times 6'\text{-}6"$ sacred altar.
- **Open Ishanya (NE) Sitout Balcony:** $13'\text{-}0" \times 12'\text{-}0"$ open-to-sky terrace kept **completely unencumbered and light** to honor classical Ishanya Vaastu.
- **Dual Light Doors:** NNE Simhadwaram entrance door `D1` ($3'\text{-}6" \times 7'\text{-}0"$) and glazed double door on the East/NE sitout align for continuous morning illumination and cross-ventilation.
- **Three Balconies:** North front balcony ($11'\text{-}6" \times 4'\text{-}3"$), East/NE open sitout ($13'\text{-}0" \times 12'\text{-}0"$), and South shaded balcony ($12'\text{-}6" \times 4'\text{-}0"$).

### 3. Second Floor (Level 2, +6.00m) — Owner's Residence & Home Office
- **Master Bedroom (SW Niruthi):** $12'\text{-}6" \times 13'\text{-}4"$ with full-width built-in wardrobe, stacked 1:1 with Level 1.
- **Spacious Bathrooms (West Varuna):** $6'\text{-}0" \times 8'\text{-}6"$ stacked 1:1 with continuous vertical wet stack.
- **North-Facing Home Office / Executive Study:** $11'\text{-}6" \times 11'\text{-}0"$ with wide North exterior window overlooking the front garden, executive desk facing East/North, and full wall bookcase cupboards (completely unblocked by the external core).
- **Modular Kitchen (SE Agneya) & Out-of-House Utility:** Stacked 1:1 with Level 1.
- **Grand Family Living Hall:** $18'\text{-}0" \times 14'\text{-}0"$ open central Brahmasthana.
- **NE Dual Pooja Suite (Detached from Kitchen):**
  - **Daily Pooja Room:** $5'\text{-}6" \times 6'\text{-}6"$ for routine household morning prayers.
  - **Mallanna Temple Shrine:** $8'\text{-}6" \times 10'\text{-}0"$ dedicated sacred room accommodating a permanent deity altar platform and a $4.65\text{ m}^2$ clear prayer carpet area for 4 adult worshippers.
- **Open Ishanya (NE) Sitout:** Left open to the sky for morning sunlight and cosmic energy, with glazed light double door.
- **Three Balconies:** North garden balcony, East/NE open sitout, and South shaded balcony.

---

## 🛠️ Why Blender for 2D Engineering CAD?

1. **Deterministic Geometry & True Slicing:** Unlike 2D bounding-box heuristics, Blender models exact wall thicknesses ($9"$ exterior brickwork, $4.5"$ internal partitions, $8"$ RCC elevator core) and hosted door swings (90° arcs) with zero floating dead space.
2. **Headless Execution in < 2 Seconds:** Python scripting interface (`bpy`) generates all 3 levels, sets up orthographic workbench cameras, creates dimension chains and grid bubbles, and renders high-resolution blueprints in under 2 seconds.
3. **Open directly in Blender GUI:** The generated `property2_engineering_cad.blend` allows the user or architect to inspect, edit, and extrude walls immediately.

---

## 🚀 Quickstart & Usage

### 1. Generate 2D Plans via Headless Blender
```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python src/generate_2d_plans.py
```
*Outputs:*
- `output/ground_stilt_2d.png` ($2800 \times 2200$)
- `output/first_floor_brother_2d.png` ($2800 \times 2200$)
- `output/second_floor_owner_2d.png` ($2800 \times 2200$)
- `output/property2_engineering_cad.blend` (Master Blender Project)

### 2. Export High-Precision Vector Blueprints (SVG)
```bash
python3 src/export_2d_vector_blueprints.py
```
*Outputs:*
- `output/ground_stilt_blueprint.svg`
- `output/first_floor_brother_blueprint.svg`
- `output/second_floor_owner_blueprint.svg`

### 3. Open Interactive Web Blueprint Viewer
```bash
open output/cad_blueprint_viewer.html
```

---

## 📂 Repository File Structure

```
blender-floor-planning-with-ai/
├── DESIGN-BRIEF.md                       # Complete multi-family architectural design brief
├── README.md                             # Repository overview and technical documentation
├── requirements/
│   ├── home-requirements.json            # Machine-readable program specs (JSON)
│   └── COMMON-DESIGN-RULES.md            # Structural, civil, and egress validation rules
├── properties/
│   ├── PROPERTY-2-CORNER-WEST-SOUTH-54x66.md  # Selected plot survey & setback boundaries
│   └── README.md                         # Property comparison matrix
├── knowledge/
│   ├── VAASTU-KNOWLEDGE.md               # Shastra principles & 9x9 Pada orientation rules
│   └── TELUGU-TELANGANA-VAASTU.md        # Regional Telangana traditions (Simhadwaram, Niruthi)
├── reviews/
│   └── DECISION-LOG.md                   # Chronological decision record & owner sign-offs
├── src/
│   ├── generate_2d_plans.py              # Blender headless CAD engine (walls, columns, text)
│   └── export_2d_vector_blueprints.py    # Standalone vector SVG generator
└── output/
    ├── ground_stilt_2d.png               # High-res Ground Stilt render
    ├── first_floor_brother_2d.png        # High-res First Floor (Brother) render
    ├── second_floor_owner_2d.png         # High-res Second Floor (Owner) render
    ├── ground_stilt_blueprint.svg        # Scalable Vector Blueprint
    ├── first_floor_brother_blueprint.svg # Scalable Vector Blueprint
    ├── second_floor_owner_blueprint.svg  # Scalable Vector Blueprint
    ├── property2_engineering_cad.blend   # Master 3D/2D Blender CAD file
    └── cad_blueprint_viewer.html         # Interactive multi-level web viewer
```

---

## ⚖️ Telugu & Telangana Vaastu Alignment Table

| Space / Room | Assigned Zone | Deity / Element | Civil / Architectural Implementation |
| :--- | :--- | :--- | :--- |
| **Master Bedroom** | South-West (Niruthi) | Earth / Heavy | Heaviest corner, thickest walls, king bed placed South-head, full cupboards |
| **Kitchen** | South-East (Agneya) | Fire (Agni) | L-shaped granite counter, East-facing cooktop, pantry cupboards |
| **Out-of-House Utility** | External East (SE) | Water / Drainage | Cantilevered wash & gas cylinder balcony outside kitchen envelope |
| **External Vertical Core** | North-West (Vayu) | Air / Movement | Dog-legged stairs + 6-PAX lift located **outside** home envelope |
| **Spacious Bathrooms** | West (Varuna) | Water / Drainage | 6'0" x 8'6" wet/dry zones, continuous vertical OTS shaft |
| **Living & Dining** | Central | Brahmasthana | 18'0" x 14'0" expansive open hall, unencumbered by shear walls, sofas + TV wall |
| **North Home Office** | North Facade | Mercury / Focus | Wide window overlooking North garden, unblocked by external core |
| **Mallanna Shrine & Pooja** | East-NE Axis | Sacred / Divine | Detached from kitchen, sacred altar, 4-person prayer carpet area |
| **Open Ishanya Sitout** | North-East Corner | Water / Light | **Kept open to sky / unencumbered** for sacred dawn light & positive prana |
| **Dual Light Doors** | NNE & East/NE | Surya / Vayu | NNE Simhadwaram & East glazed door align for cross-ventilation corridor |
| **Three Balconies** | North, East, South | Climate & Shading | Cross-ventilation, morning sunrise view, and southern sun-shading |
| **Ground Stilt & Gardens** | Ground Level | Multi-functional | 750 sq ft pavilion, covered SUV parking, 4 bike bays, North & East gardens |
