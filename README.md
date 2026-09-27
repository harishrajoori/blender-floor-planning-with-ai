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

### 1. Ground Floor (Level 0, +0.00m) — Stilt Parking & Pavilion
- **Sheltered Function Pavilion ($37'\text{-}0" \times 20'\text{-}0" \approx 740\text{ sq.ft}$):** Open-air plinth verandah for traditional family gatherings and festivals.
- **Covered Parking Bay:** $8'\text{-}6" \times 17'\text{-}0"$ car stall + dedicated 4 two-wheeler parking stalls in the North-East driveway zone.
- **Vertical Circulation Core (NW Vayu Zone):** Dog-legged staircase ($7'\text{-}3" \times 14'\text{-}6"$) and 6-PAX passenger elevator shaft ($1.6\text{m} \times 1.6\text{m}$ clear).

### 2. First Floor (Level 1, +3.00m) — Brother's 2BHK Residence
- **Master Bedroom (SW Niruthi):** $12'\text{-}6" \times 13'\text{-}4"$ ($167\text{ sq.ft}$) with built-in wardrobe and attached toilet ($5'\text{-}0" \times 6'\text{-}6"$).
- **Common Toilet (West Varuna):** $5'\text{-}0" \times 6'\text{-}6"$ stacked directly adjacent to master bath over a continuous plumbing duct (OTS).
- **Modular Kitchen (SE Agneya):** $12'\text{-}6" \times 11'\text{-}0"$ ($138\text{ sq.ft}$) with L-shaped granite counter, East-facing cooktop, and corner sink.
- **Central Living & Dining (Brahmasthana):** $14'\text{-}0" \times 13'\text{-}6"$ formal living hall + $10'\text{-}0" \times 11'\text{-}6"$ dining area with zero obstructive partition walls.
- **Bedroom 2 (North Vayu):** $9'\text{-}6" \times 12'\text{-}6"$ ($119\text{ sq.ft}$) with North-facing natural ventilation window.
- **Pooja Mandir (NE Ishanya):** $6'\text{-}0" \times 7'\text{-}9"$ sacred altar.
- **East Sitout Balcony:** $7'\text{-}0" \times 12'\text{-}6"$ ($88\text{ sq.ft}$) open-to-sky terrace for morning eastern light.
- **Simhadwaram (Main Entrance):** North-facing threshold door `D1` ($3'\text{-}6" \times 7'\text{-}0"$).

### 3. Second Floor (Level 2, +6.00m) — Owner's 2BHK + Office + Dual Pooja
- **Master Bedroom (SW Niruthi):** $12'\text{-}6" \times 13'\text{-}4"$ with attached toilet ($5'\text{-}0" \times 6'\text{-}6"$), stacked 1:1 with Level 1.
- **Common Toilet (West Varuna):** $5'\text{-}0" \times 6'\text{-}6"$ stacked 1:1 with continuous vertical wet stack.
- **Dedicated Home Office / Study (Center Bay):** $11'\text{-}6" \times 8'\text{-}0"$ ($92\text{ sq.ft}$) high-focus executive workstation with bookcase and private doorway.
- **Modular Kitchen (SE Agneya):** $12'\text{-}6" \times 11'\text{-}0"$ stacked 1:1.
- **Family Living Hall:** $14'\text{-}0" \times 13'\text{-}6"$.
- **Bedroom 2 (North Vayu):** $9'\text{-}6" \times 12'\text{-}6"$ stacked 1:1.
- **NE Dual Pooja Suite:**
  - **Daily Pooja Room:** $4'\text{-}0" \times 4'\text{-}0"$ for routine household morning prayers.
  - **Mallanna Temple Shrine:** $9'\text{-}0" \times 9'\text{-}0" = 81\text{ sq.ft}$ dedicated sacred room accommodating a permanent deity altar platform and a $4.65\text{ m}^2$ prayer carpet area for 4 adult worshippers.

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
| **Master Bedroom** | South-West (Niruthi) | Earth / Heavy | Maximum mass, thickest exterior wall, bed placed South-head |
| **Kitchen** | South-East (Agneya) | Fire (Agni) | L-counter, cooking cooktop facing East, corner sink |
| **Vertical Core** | North-West (Vayu) | Air / Movement | Dog-legged staircase turning clockwise, 6-PAX lift shaft |
| **Attached & Common Baths** | West (Varuna) | Water / Drainage | Stacked 1:1, continuous OTS shaft down to stilt |
| **Living & Dining** | Central | Brahmasthana | Completely open, unobstructed span, natural cross ventilation |
| **Pooja & Mallanna Shrine** | North-East (Ishanya) | Water / Divine | Northeast light, sacred altar platforms, prayer floor space |
| **Main Entrance Door** | North Face | Simhadwaram | North-facing opening D1, unobstructed threshold |
