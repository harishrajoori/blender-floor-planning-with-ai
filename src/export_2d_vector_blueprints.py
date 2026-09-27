"""
High-Precision 2D Vector Architectural Blueprint SVG Generator for Property 2 (54' x 66')
Redesigned according to Owner Requirements & Canonical Telangana Vaastu Principles:
  1. North-East (Ishanya) kept open as an unencumbered light sitout terrace.
  2. External Vertical Core (Dog-legged Stairs + 6-PAX Lift) outside the living envelope in NW.
  3. North-facing Home Office with clear front garden view.
  4. Sequence along East: Kitchen (SE) -> Dining/Living -> Mallanna Shrine -> Daily Pooja -> Open NE Sitout.
  5. Dual light doors (NNE Simhadwaram & East/NE Glazed Door) for continuous cross-ventilation.
  6. External Utility / Wash balcony cantilevered outside the kitchen.
  7. Spacious luxury bathrooms (6'0" x 8'6") with distinct dry/wet zones.
  8. Three balconies: North, East (Ishanya), and South.
  9. Complete built-in millwork: wardrobes/cupboards, executive desk, TV console, sofas, gardens & parking.
"""

import math
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Scale: 100 pixels per meter (1cm = 1m)
SCALE = 100.0
# Origin offset in SVG pixels (generous margin for external core, roads, gardens, dimensions, title block)
OX = 480.0
OY = 1420.0

PLINTH_W = 11.2776
PLINTH_D = 12.192
GRID_X = [0.115, 3.810, 7.315, PLINTH_W - 0.115]
GRID_Y = [0.115, 4.064, 8.128, PLINTH_D - 0.115]

def to_svg_x(x):
    return OX + x * SCALE

def to_svg_y(y):
    return OY - y * SCALE

def rect_m(x, y, w, h, fill="#E5E7EB", stroke="#1F2937", sw=1.5, rx=0, opacity=1.0, dash="", extra=""):
    if dash:
        extra = f'stroke-dasharray="{dash}" ' + extra
    sx = to_svg_x(x)
    sy = to_svg_y(y + h)
    sw_px = w * SCALE
    sh_px = h * SCALE
    return f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{sw_px:.1f}" height="{sh_px:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}" opacity="{opacity}" {extra}/>\n'

def line_m(x0, y0, x1, y1, stroke="#4B5563", sw=1.0, dash="", extra=""):
    sx0, sy0 = to_svg_x(x0), to_svg_y(y0)
    sx1, sy1 = to_svg_x(x1), to_svg_y(y1)
    dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{sx0:.1f}" y1="{sy0:.1f}" x2="{sx1:.1f}" y2="{sy1:.1f}" stroke="{stroke}" stroke-width="{sw}" {dash_attr} {extra}/>\n'

def text_m(x, y, text, size=14, weight="normal", fill="#111827", anchor="middle", rot=0, extra=""):
    sx, sy = to_svg_x(x), to_svg_y(y)
    transform = f'transform="rotate({rot} {sx:.1f} {sy:.1f})"' if rot != 0 else ""
    lines = text.split("\n")
    if len(lines) == 1:
        return f'<text x="{sx:.1f}" y="{sy:.1f}" font-family="Inter, -apple-system, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {transform} {extra}>{text}</text>\n'
    else:
        out = f'<text x="{sx:.1f}" y="{sy:.1f}" font-family="Inter, -apple-system, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {transform} {extra}>\n'
        for i, l in enumerate(lines):
            dy = "-0.3em" if i == 0 and len(lines) > 1 else "1.25em"
            out += f'  <tspan x="{sx:.1f}" dy="{dy}">{l}</tspan>\n'
        out += '</text>\n'
        return out

def door_svg(name, hx, hy, w, side='E'):
    out = ""
    if side == 'E':
        out += line_m(hx, hy, hx + w, hy, stroke="#059669", sw=2.5)
        sx0, sy0 = to_svg_x(hx + w), to_svg_y(hy)
        sx1, sy1 = to_svg_x(hx), to_svg_y(hy + w)
        r = w * SCALE
        out += f'<path d="M {sx0:.1f} {sy0:.1f} A {r:.1f} {r:.1f} 0 0 0 {sx1:.1f} {sy1:.1f}" fill="none" stroke="#10B981" stroke-width="1.2" stroke-dasharray="3,3"/>\n'
    elif side == 'W':
        out += line_m(hx, hy, hx - w, hy, stroke="#059669", sw=2.5)
        sx0, sy0 = to_svg_x(hx - w), to_svg_y(hy)
        sx1, sy1 = to_svg_x(hx), to_svg_y(hy + w)
        r = w * SCALE
        out += f'<path d="M {sx0:.1f} {sy0:.1f} A {r:.1f} {r:.1f} 0 0 1 {sx1:.1f} {sy1:.1f}" fill="none" stroke="#10B981" stroke-width="1.2" stroke-dasharray="3,3"/>\n'
    elif side == 'N':
        out += line_m(hx, hy, hx, hy + w, stroke="#059669", sw=2.5)
        sx0, sy0 = to_svg_x(hx), to_svg_y(hy + w)
        sx1, sy1 = to_svg_x(hx + w), to_svg_y(hy)
        r = w * SCALE
        out += f'<path d="M {sx0:.1f} {sy0:.1f} A {r:.1f} {r:.1f} 0 0 0 {sx1:.1f} {sy1:.1f}" fill="none" stroke="#10B981" stroke-width="1.2" stroke-dasharray="3,3"/>\n'
    else: # 'S'
        out += line_m(hx, hy, hx, hy - w, stroke="#059669", sw=2.5)
        sx0, sy0 = to_svg_x(hx), to_svg_y(hy - w)
        sx1, sy1 = to_svg_x(hx + w), to_svg_y(hy)
        r = w * SCALE
        out += f'<path d="M {sx0:.1f} {sy0:.1f} A {r:.1f} {r:.1f} 0 0 1 {sx1:.1f} {sy1:.1f}" fill="none" stroke="#10B981" stroke-width="1.2" stroke-dasharray="3,3"/>\n'
    return out

def window_svg(x0, y0, w, h, is_horiz=True):
    out = rect_m(x0, y0, w, h, fill="#EFF6FF", stroke="#2563EB", sw=1.5)
    if is_horiz:
        out += line_m(x0, y0 + h/2.0, x0 + w, y0 + h/2.0, stroke="#3B82F6", sw=1.2)
    else:
        out += line_m(x0 + w/2.0, y0, x0 + w/2.0, y0 + h, stroke="#3B82F6", sw=1.2)
    return out

def build_base_sheet(title, floor_code):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 1800" width="2400" height="1800">
  <defs>
    <pattern id="gridPattern" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#F1F5F9" stroke-width="0.8"/>
    </pattern>
    <pattern id="concreteHatch" width="10" height="10" patternUnits="userSpaceOnUse">
      <path d="M0 10 L10 0 M0 0 L10 10" fill="none" stroke="#E2E8F0" stroke-width="0.5"/>
    </pattern>
  </defs>

  <!-- Drafting Sheet Background -->
  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <rect x="30" y="30" width="2340" height="1740" fill="none" stroke="#CBD5E1" stroke-width="2"/>
  <rect x="40" y="40" width="2320" height="1720" fill="url(#gridPattern)" stroke="#0F172A" stroke-width="1"/>

  <!-- Site Setbacks and Roads -->
  <g id="site_context">
    <!-- North Front Garden (15' Setback) -->
    <rect x="{to_svg_x(0):.1f}" y="{to_svg_y(PLINTH_D + 2.5):.1f}" width="{PLINTH_W * SCALE:.1f}" height="{2.5 * SCALE:.1f}" fill="#DCFCE7" stroke="#86EFAC" stroke-dasharray="4,4" opacity="0.6"/>
    <text x="{to_svg_x(PLINTH_W/2.0):.1f}" y="{to_svg_y(PLINTH_D + 1.2):.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#166534" text-anchor="middle">
      NORTH FRONT GARDEN &amp; LAWN (15\'-0" CLEAR FRONT SETBACK)
    </text>

    <!-- East Morning Garden (Setback) -->
    <rect x="{to_svg_x(PLINTH_W + 0.1):.1f}" y="{to_svg_y(PLINTH_D):.1f}" width="{2.2 * SCALE:.1f}" height="{PLINTH_D * SCALE:.1f}" fill="#DCFCE7" stroke="#86EFAC" stroke-dasharray="4,4" opacity="0.6"/>
    <text x="{to_svg_x(PLINTH_W + 1.2):.1f}" y="{to_svg_y(6.0):.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#166534" text-anchor="middle" transform="rotate(-90 {to_svg_x(PLINTH_W + 1.2):.1f} {to_svg_y(6.0):.1f})">
      EAST MORNING GARDEN &amp; PLANTATION SETBACK
    </text>

    <!-- West Road -->
    <rect x="70" y="160" width="90" height="1200" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="6,4" rx="8"/>
    <text x="115" y="750" font-family="Inter, sans-serif" font-size="16" font-weight="700" fill="#3B82F6" text-anchor="middle" transform="rotate(-90 115 750)">
      ◄◄ 30\'-0" WIDE WEST ROAD (PRIMARY VEHICLE &amp; PEDESTRIAN ACCESS) ◄◄
    </text>
    
    <!-- South Road -->
    <rect x="250" y="1520" width="1400" height="90" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="6,4" rx="8"/>
    <text x="950" y="1575" font-family="Inter, sans-serif" font-size="16" font-weight="700" fill="#3B82F6" text-anchor="middle">
      ▼▼ 30\'-0" WIDE SOUTH ROAD (SECONDARY CORNER ACCESS) ▼▼
    </text>
  </g>
'''
    return svg

def add_grids_and_dimensions_svg():
    out = "<g id='structural_grid_and_dims'>\n"
    # Vertical grid lines X1-X4
    for i, cx in enumerate(GRID_X):
        out += line_m(cx, -2.2, cx, PLINTH_D + 2.2, stroke="#94A3B8", sw=1.0, dash="5,5")
        # Top bubble
        sx, sy = to_svg_x(cx), to_svg_y(PLINTH_D + 2.5)
        out += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="18" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.5"/>\n'
        out += f'<text x="{sx:.1f}" y="{sy+5:.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#0F172A" text-anchor="middle">{i+1}</text>\n'
        # Bottom bubble
        sx, sy = to_svg_x(cx), to_svg_y(-2.5)
        out += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="18" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.5"/>\n'
        out += f'<text x="{sx:.1f}" y="{sy+5:.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#0F172A" text-anchor="middle">{i+1}</text>\n'

    # Horizontal grid lines YA-YD
    lbls = ['A', 'B', 'C', 'D']
    for i, cy in enumerate(GRID_Y):
        out += line_m(-3.0, cy, PLINTH_W + 2.0, cy, stroke="#94A3B8", sw=1.0, dash="5,5")
        # Left bubble
        sx, sy = to_svg_x(-3.3), to_svg_y(cy)
        out += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="18" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.5"/>\n'
        out += f'<text x="{sx:.1f}" y="{sy+5:.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#0F172A" text-anchor="middle">{lbls[i]}</text>\n'
        # Right bubble
        sx, sy = to_svg_x(PLINTH_W + 2.3), to_svg_y(cy)
        out += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="18" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.5"/>\n'
        out += f'<text x="{sx:.1f}" y="{sy+5:.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#0F172A" text-anchor="middle">{lbls[i]}</text>\n'

    # Overall South: 37'-0"
    out += line_m(0, -1.3, PLINTH_W, -1.3, stroke="#475569", sw=1.5)
    out += line_m(-0.15, -1.45, 0.15, -1.15, stroke="#475569", sw=2.0)
    out += line_m(PLINTH_W - 0.15, -1.45, PLINTH_W + 0.15, -1.15, stroke="#475569", sw=2.0)
    out += text_m(PLINTH_W / 2.0, -1.65, "37'-0\" [11.28m] OVERALL PLINTH WIDTH", size=13, weight="600", fill="#1E293B")

    # Overall West: 40'-0"
    out += line_m(-2.8, 0, -2.8, PLINTH_D, stroke="#475569", sw=1.5)
    out += line_m(-2.95, -0.15, -2.65, 0.15, stroke="#475569", sw=2.0)
    out += line_m(-2.95, PLINTH_D - 0.15, -2.65, PLINTH_D + 0.15, stroke="#475569", sw=2.0)
    out += text_m(-3.05, PLINTH_D / 2.0, "40'-0\" [12.19m] PLINTH DEPTH", size=13, weight="600", fill="#1E293B", rot=-90)

    # 16 Columns
    out += "<g id='rcc_columns'>\n"
    for cx in GRID_X:
        for cy in GRID_Y:
            out += rect_m(cx - 0.115, cy - 0.225, 0.230, 0.450, fill="#0F172A", stroke="#000000", sw=1.0)
    out += "</g>\n"
    out += "</g>\n"
    return out

def add_external_vertical_core_svg():
    out = "<g id='external_vertical_core'>\n"
    # External Landing Verandah Slab
    out += rect_m(-2.5, 6.0, 2.5, 6.2, fill="#F1F5F9", stroke="#475569", sw=1.5)
    
    # Dog-legged Stairs (-2.4 to -0.3, Y: 6.2 to 9.5)
    out += rect_m(-2.4, 6.2, 2.1, 3.3, fill="#E2E8F0", stroke="#64748B", sw=1.2)
    out += rect_m(-2.4, 6.2, 2.1, 1.1, fill="#CBD5E1", stroke="#64748B", sw=1.0)
    out += line_m(-1.35, 7.3, -1.35, 9.5, stroke="#475569", sw=1.8)
    for i in range(1, 7):
        ty = 7.3 + i * (2.2 / 7.0)
        out += line_m(-2.4, ty, -1.45, ty, stroke="#94A3B8", sw=1.0)
        out += line_m(-1.25, ty, -0.3, ty, stroke="#94A3B8", sw=1.0)
    out += text_m(-1.35, 7.8, "EXTERNAL STAIRS\n7'-3\" x 11'-0\" [NW VAYU]", size=11, weight="600", fill="#0F172A", rot=-90)

    # 6-PAX Passenger Lift (-2.3 to -0.4, Y: 9.8 to 11.9)
    out += rect_m(-2.3, 9.8, 1.9, 2.1, fill="#E2E8F0", stroke="#334155", sw=2.0)
    out += rect_m(-1.95, 10.15, 1.2, 1.4, fill="#FFFFFF", stroke="#0284C7", sw=1.5)
    out += line_m(-1.95, 10.15, -0.75, 11.55, stroke="#38BDF8", sw=1.0)
    out += line_m(-1.95, 11.55, -0.75, 10.15, stroke="#38BDF8", sw=1.0)
    out += text_m(-1.35, 10.8, "6-PAX LIFT\n1.6m x 1.6m", size=11, weight="700", fill="#0369A1", rot=-90)
    
    # Core Perimeter Railing
    out += line_m(-2.5, 6.0, -2.5, 12.2, stroke="#475569", sw=2.0)
    out += "</g>\n"
    return out

def add_title_block_svg(sheet_title):
    bx = to_svg_x(PLINTH_W + 1.2)
    by = to_svg_y(2.6)
    bw = (6.8 - 1.2) * SCALE
    bh = (2.6 - (-4.2)) * SCALE
    cx = bx + bw / 2.0
    
    out = f'''<g id="title_block">
  <rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="#F8FAFC" stroke="#0F172A" stroke-width="2"/>
  <rect x="{bx+6:.1f}" y="{by+6:.1f}" width="{bw-12:.1f}" height="{bh-12:.1f}" fill="none" stroke="#64748B" stroke-width="1"/>
  
  <text x="{cx:.1f}" y="{by+35:.1f}" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="#0F172A" text-anchor="middle">PROPERTY 2 RESIDENCE</text>
  <text x="{cx:.1f}" y="{by+65:.1f}" font-family="Inter, sans-serif" font-size="15" font-weight="700" fill="#0D9488" text-anchor="middle">{sheet_title.upper()}</text>
  
  <line x1="{bx+15:.1f}" y1="{by+85:.1f}" x2="{bx+bw-15:.1f}" y2="{by+85:.1f}" stroke="#CBD5E1" stroke-width="1"/>
  
  <text x="{bx+20:.1f}" y="{by+115:.1f}" font-family="Inter, sans-serif" font-size="12" fill="#334155"><b>PLOT:</b> 54'-0" x 66'-0" (SW Corner, 3,564 sq ft)</text>
  <text x="{bx+20:.1f}" y="{by+140:.1f}" font-family="Inter, sans-serif" font-size="12" fill="#334155"><b>PLINTH:</b> 37'-0" x 40'-0" (1,480 sq ft Footprint)</text>
  <text x="{bx+20:.1f}" y="{by+165:.1f}" font-family="Inter, sans-serif" font-size="12" fill="#334155"><b>CORE:</b> External NW Stairs &amp; 6-PAX Lift</text>
  <text x="{bx+20:.1f}" y="{by+190:.1f}" font-family="Inter, sans-serif" font-size="12" fill="#0D9488"><b>VAASTU:</b> Telugu / Telangana (Open Ishanya NE)</text>
  <text x="{bx+20:.1f}" y="{by+215:.1f}" font-family="Inter, sans-serif" font-size="12" fill="#334155"><b>BALCONIES:</b> North, East (Ishanya), &amp; South</text>
  <text x="{bx+20:.1f}" y="{by+240:.1f}" font-family="Inter, sans-serif" font-size="12" fill="#334155"><b>UTILITY:</b> External Out-of-House Balcony</text>
  <text x="{bx+20:.1f}" y="{by+265:.1f}" font-family="Inter, sans-serif" font-size="12" fill="#334155"><b>BATHS:</b> Spacious 6'0" x 8'6" Wet/Dry Stacks</text>
  
  <line x1="{bx+15:.1f}" y1="{by+285:.1f}" x2="{bx+bw-15:.1f}" y2="{by+285:.1f}" stroke="#CBD5E1" stroke-width="1"/>
  
  <text x="{bx+20:.1f}" y="{by+315:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#64748B">DOORS: D1: 3'6"x7' | D2: 3'0"x7' | D3: 2'6"x7'</text>
  <text x="{bx+20:.1f}" y="{by+335:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#64748B">WINDOWS: W1: 5'0"x4'6" | W2: 4'0"x4'6" | V1: 2'0"x2'0"</text>
  <text x="{bx+20:.1f}" y="{by+355:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#64748B">MILLWORK: Full Wardrobes, Desk, TV Console, Sofas</text>
</g>
'''
    return out

# =============================================================================
# EXPORT 1: GROUND STILT & PARKING BLUEPRINT
# =============================================================================
def export_ground_stilt_svg():
    svg = build_base_sheet("Ground Stilt, Parking & Pavilion Blueprint", "L0")
    # Base slab
    svg += rect_m(0, 0, PLINTH_W, PLINTH_D, fill="#F8FAFC", stroke="#0F172A", sw=2.0)
    
    # Sheltered Function Pavilion
    svg += rect_m(0, 0, PLINTH_W, 6.2, fill="#FEF3C7", stroke="#D97706", sw=1.5, opacity=0.7)
    svg += text_m(5.6, 3.4, "SHELTERED OPEN FUNCTION PAVILION", size=18, weight="800", fill="#92400E")
    svg += text_m(5.6, 2.7, "37'-0\" x 20'-4\" [11.28m x 6.20m] | 750 SQ.FT", size=14, weight="600", fill="#78350F")
    svg += text_m(5.6, 2.1, "(Traditional Family Events, Open Verandah, Cultural Gatherings)", size=12, fill="#B45309")

    # Covered Car Parking Bay
    svg += rect_m(3.8, PLINTH_D - 5.8, 2.8, 5.5, fill="#E0F2FE", stroke="#0284C7", sw=1.5, rx=6)
    # Car Silhouette
    svg += rect_m(4.1, PLINTH_D - 5.5, 2.2, 4.8, fill="#BAE6FD", stroke="#0369A1", sw=1.5, rx=12)
    svg += text_m(5.2, PLINTH_D - 3.1, "COVERED CAR PARKING\n9'-0\" x 18'-0\" [SEDAN/SUV]", size=13, weight="700", fill="#075985")

    # 2-Wheeler Parking (4 Bikes)
    svg += rect_m(7.0, PLINTH_D - 3.0, 2.5, 2.5, fill="#F0FDF4", stroke="#16A34A", sw=1.5, rx=4)
    svg += text_m(8.25, PLINTH_D - 1.7, "2-WHEELER PARKING\n(4 MOTORCYCLES)", size=12, weight="600", fill="#15803D")

    # External Core & Columns
    svg += add_external_vertical_core_svg()
    svg += add_grids_and_dimensions_svg()
    svg += add_title_block_svg("Ground Stilt, Parking & Pavilion")
    svg += "</svg>"
    
    p = OUTPUT_DIR / "ground_stilt_blueprint.svg"
    p.write_text(svg, encoding="utf-8")
    print(f"✅ Generated Vector SVG: {p}")

# =============================================================================
# EXPORT 2: FIRST FLOOR — BROTHER'S 2BHK RESIDENCE
# =============================================================================
def export_first_floor_svg():
    svg = build_base_sheet("First Floor Plan - Brother's 2BHK Residence", "L1")
    svg += rect_m(0, 0, PLINTH_W, PLINTH_D, fill="#F8FAFC", stroke="#0F172A", sw=2.0)

    # 1. BALCONIES (North, East/Ishanya, South) & External Utility
    # North Balcony
    svg += rect_m(3.81, PLINTH_D, 3.50, 1.30, fill="#EFF6FF", stroke="#2563EB", sw=1.5, dash="4,4")
    svg += text_m(5.5, PLINTH_D + 0.65, "NORTH BALCONY (11'-6\" x 4'-3\")", size=11, weight="600", fill="#1D4ED8")
    # East / North-East Open Sitout (LEFT OPEN FOR ISHANYA LIGHT!)
    svg += rect_m(7.31, 8.5, PLINTH_W - 7.31, PLINTH_D - 8.5, fill="#EFF6FF", stroke="#0284C7", sw=1.8)
    svg += text_m(9.2, 11.2, "OPEN ISHANYA (NE) SITOUT", size=14, weight="800", fill="#0369A1")
    svg += text_m(9.2, 10.7, "13'-0\" x 12'-0\" [OPEN TO SKY]", size=12, weight="600", fill="#0284C7")
    svg += text_m(9.2, 10.2, "(Sacred Morning Daylight Corridor)", size=10, fill="#075985")
    # South Balcony
    svg += rect_m(0, -1.2, 3.81, 1.2, fill="#EFF6FF", stroke="#2563EB", sw=1.5, dash="4,4")
    svg += text_m(1.9, -0.6, "SOUTH SHADED BALCONY (12'-6\" x 4'-0\")", size=11, weight="600", fill="#1D4ED8")
    # External Out-of-House Utility Balcony
    svg += rect_m(PLINTH_W, 0, 1.4, 3.5, fill="#F1F5F9", stroke="#475569", sw=1.5)
    svg += text_m(PLINTH_W + 0.7, 1.75, "OUT-OF-HOUSE UTILITY\n(WASH & GAS BALCONY)", size=11, weight="600", fill="#334155", rot=-90)

    # 2. EXTERIOR 9" WALLS
    svg += "<g id='exterior_walls'>\n"
    # South Wall
    svg += rect_m(0, 0, 1.2, 0.23, fill="#334155", stroke="#0F172A")
    svg += door_svg("Door_MB_S_Balcony", 1.2, 0.23, 0.90, side='S')
    svg += rect_m(2.1, 0, 3.81 - 2.1, 0.23, fill="#334155", stroke="#0F172A")
    svg += rect_m(3.81, 0, PLINTH_W - 3.81, 0.23, fill="#334155", stroke="#0F172A")
    # East Wall
    svg += rect_m(PLINTH_W - 0.23, 0, 0.23, 1.2, fill="#334155", stroke="#0F172A")
    svg += door_svg("Door_Kit_Utility", PLINTH_W - 0.23, 1.2, 0.85, side='E')
    svg += rect_m(PLINTH_W - 0.23, 2.05, 0.23, 0.15, fill="#334155", stroke="#0F172A")
    svg += window_svg(PLINTH_W - 0.23, 2.2, 0.23, 1.2, is_horiz=False)
    svg += rect_m(PLINTH_W - 0.23, 3.4, 0.23, 1.6, fill="#334155", stroke="#0F172A")
    svg += window_svg(PLINTH_W - 0.23, 5.0, 0.23, 2.2, is_horiz=False)
    svg += rect_m(PLINTH_W - 0.23, 7.2, 0.23, 1.3, fill="#334155", stroke="#0F172A")
    # North Wall
    svg += rect_m(0, PLINTH_D - 0.23, 1.5, 0.23, fill="#334155", stroke="#0F172A")
    svg += door_svg("Simhadwaram_D1", 1.5, PLINTH_D - 0.23, 1.05, side='S') # NNE Door
    svg += rect_m(2.55, PLINTH_D - 0.23, 3.81 - 2.55, 0.23, fill="#334155", stroke="#0F172A")
    svg += rect_m(3.81, PLINTH_D - 0.23, 0.99, 0.23, fill="#334155", stroke="#0F172A")
    svg += door_svg("Door_B2_North_Balcony", 4.8, PLINTH_D - 0.23, 0.90, side='N')
    svg += window_svg(5.8, PLINTH_D - 0.23, 1.4, 0.23, is_horiz=True)
    svg += rect_m(7.2, PLINTH_D - 0.23, 0.11, 0.23, fill="#334155", stroke="#0F172A")
    # West Wall
    svg += rect_m(0, 0.23, 0.23, 1.27, fill="#334155", stroke="#0F172A")
    svg += window_svg(0, 1.5, 0.23, 1.5, is_horiz=False)
    svg += rect_m(0, 3.0, 0.23, 2.0, fill="#334155", stroke="#0F172A")
    svg += window_svg(0, 5.0, 0.23, 0.8, is_horiz=False)
    svg += rect_m(0, 5.8, 0.23, PLINTH_D - 0.23 - 5.8, fill="#334155", stroke="#0F172A")
    svg += "</g>\n"

    # 3. INTERIOR PARTITIONS (4.5")
    svg += "<g id='interior_partitions'>\n"
    # Master Bed Wall East
    svg += rect_m(3.81 - 0.0575, 0.23, 0.115, 3.83, fill="#475569", stroke="#0F172A")
    # Master Bed North Wall with ATTACHED BATH DOOR & MB MAIN DOOR
    svg += rect_m(0.23, 4.06 - 0.0575, 0.27, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_AttBath", 0.5, 4.06, 0.75, side='N') # Attached Bath Door!
    svg += rect_m(1.25, 4.06 - 0.0575, 1.45, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_MB", 2.7, 4.06, 0.90, side='S')
    svg += rect_m(3.6, 4.06 - 0.0575, 0.21, 0.115, fill="#475569", stroke="#0F172A")

    # Spacious Bathrooms (6'0" x 8'6")
    svg += rect_m(1.83 - 0.0575, 4.06, 0.115, 2.60, fill="#475569", stroke="#0F172A")
    svg += rect_m(0.23, 6.66 - 0.0575, 3.58, 0.115, fill="#475569", stroke="#0F172A")
    svg += rect_m(3.81 - 0.0575, 4.06, 0.115, 1.14, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_CommonBath", 3.81, 5.2, 0.75, side='W')
    svg += rect_m(3.81 - 0.0575, 5.95, 0.115, 0.71, fill="#475569", stroke="#0F172A")

    # Kitchen (SE Agneya)
    svg += rect_m(7.31 - 0.0575, 0.23, 0.115, 1.97, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Kit", 7.31, 2.2, 0.90, side='W')
    svg += rect_m(7.31 - 0.0575, 3.1, 0.115, 0.40, fill="#475569", stroke="#0F172A")
    svg += rect_m(7.31, 3.5 - 0.0575, PLINTH_W - 0.23 - 7.31, 0.115, fill="#475569", stroke="#0F172A")

    # Bedroom 2 (North)
    svg += rect_m(3.81 - 0.0575, 8.5, 0.115, PLINTH_D - 0.23 - 8.5, fill="#475569", stroke="#0F172A")
    svg += rect_m(7.31 - 0.0575, 8.5, 0.115, PLINTH_D - 0.23 - 8.5, fill="#475569", stroke="#0F172A")
    svg += rect_m(3.81, 8.5 - 0.0575, 1.19, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_B2", 5.0, 8.5, 0.90, side='N')
    svg += rect_m(5.9, 8.5 - 0.0575, 1.41, 0.115, fill="#475569", stroke="#0F172A")

    # Pooja & Ishanya Glazed Light Door
    svg += rect_m(7.31, 8.5 - 0.0575, 0.89, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Ishanya_Light", 8.2, 8.5, 1.20, side='E') # Glazed Double Door!
    svg += rect_m(9.4, 8.5 - 0.0575, 0.60, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Pooja", 10.0, 8.5, 0.80, side='N')
    svg += rect_m(10.8, 8.5 - 0.0575, PLINTH_W - 0.23 - 10.8, 0.115, fill="#475569", stroke="#0F172A")
    svg += rect_m(10.0 - 0.0575, 8.5, 0.115, 2.0, fill="#475569", stroke="#0F172A")
    svg += rect_m(10.0, 10.5 - 0.0575, PLINTH_W - 0.23 - 10.0, 0.115, fill="#475569", stroke="#0F172A")
    svg += "</g>\n"

    # 4. BUILT-IN CUPBOARDS & MILLWORK
    svg += "<g id='millwork_and_furniture'>\n"
    # Master Bed Wardrobe (Full width west wall)
    svg += rect_m(0.23, 0.35, 0.60, 3.45, fill="#FEF3C7", stroke="#D97706", sw=1.2)
    svg += text_m(0.53, 2.0, "FULL WARDROBE CUPBOARD", size=10, weight="600", fill="#B45309", rot=-90)
    # Master Bed
    svg += rect_m(1.4, 0.4, 2.0, 2.0, fill="#DBEAFE", stroke="#3B82F6", rx=4)
    svg += text_m(2.4, 1.4, "KING BED\n6'0\" x 6'6\"", size=11, fill="#1D4ED8")
    svg += rect_m(3.81 - 0.40, 1.5, 0.35, 1.7, fill="#E2E8F0", stroke="#475569", sw=1.0)
    svg += text_m(3.81 - 0.22, 2.35, "TV UNIT", size=9, fill="#334155", rot=-90)

    # Bed 2 Wardrobe & Queen Bed
    svg += rect_m(3.81 + 0.06, 9.2, 0.55, 2.6, fill="#FEF3C7", stroke="#D97706", sw=1.2)
    svg += text_m(4.1, 10.5, "WARDROBE", size=10, fill="#B45309", rot=-90)
    svg += rect_m(4.8, PLINTH_D - 2.4, 1.8, 2.0, fill="#DBEAFE", stroke="#3B82F6", rx=4)
    svg += text_m(5.7, PLINTH_D - 1.4, "QUEEN BED\n5'0\" x 6'6\"", size=11, fill="#1D4ED8")

    # L-Shaped Sectional Sofa & Entertainment TV Console in Living
    svg += rect_m(4.2, 5.0, 2.8, 0.9, fill="#EDE9FE", stroke="#7C3AED", rx=4)
    svg += rect_m(4.2, 5.9, 0.9, 1.6, fill="#EDE9FE", stroke="#7C3AED", rx=4)
    svg += rect_m(5.5, 6.2, 1.2, 1.0, fill="#F3F4F6", stroke="#4B5563", rx=2)
    svg += text_m(6.1, 6.7, "COFFEE TABLE", size=9, fill="#374151")
    svg += rect_m(3.81 + 0.06, 4.5, 0.40, 2.0, fill="#FEF3C7", stroke="#D97706", sw=1.2)
    svg += text_m(4.0, 5.5, "LIVING TV WALL UNIT", size=10, weight="600", fill="#B45309", rot=-90)

    # 6-Seater Dining Table
    svg += rect_m(5.0, 2.2, 1.6, 1.4, fill="#FEF3C7", stroke="#D97706", rx=4)
    svg += text_m(5.8, 2.9, "DINING TABLE\n(6-SEATER)", size=11, fill="#B45309")

    # Kitchen Cabinets & Pantry
    svg += rect_m(PLINTH_W - 0.23 - 0.65, 0.23, 0.65, 3.2, fill="#1E293B", stroke="#000000", sw=1.2)
    svg += rect_m(7.4, 0.23, PLINTH_W - 0.23 - 7.4 - 0.65, 0.65, fill="#1E293B", stroke="#000000", sw=1.2)
    svg += rect_m(7.4, 2.5, 0.50, 0.9, fill="#FEF3C7", stroke="#D97706", sw=1.0)
    svg += text_m(7.65, 2.95, "PANTRY", size=9, fill="#B45309", rot=-90)
    svg += rect_m(PLINTH_W - 0.23 - 0.60, 2.1, 0.50, 0.8, fill="#F59E0B", stroke="#B45309", rx=2)
    svg += text_m(PLINTH_W - 0.23 - 0.35, 2.5, "EAST HOB", size=9, fill="#FFFFFF")

    # External Utility Fixtures
    svg += rect_m(PLINTH_W + 0.2, 0.4, 0.7, 0.7, fill="#E2E8F0", stroke="#334155")
    svg += text_m(PLINTH_W + 0.55, 0.75, "WM", size=10, fill="#334155")
    svg += rect_m(PLINTH_W + 0.2, 1.6, 0.6, 0.8, fill="#E2E8F0", stroke="#334155")
    svg += text_m(PLINTH_W + 0.5, 2.0, "SINK", size=10, fill="#334155")
    svg += "</g>\n"

    # 5. ROOM LABELS & VAASTU TAGS
    svg += "<g id='room_labels'>\n"
    svg += text_m(2.0, 3.1, "MASTER BEDROOM", size=14, weight="700", fill="#0F172A")
    svg += text_m(2.0, 2.7, "12'-6\" x 13'-4\" [3.81m x 4.06m]", size=11, weight="600", fill="#334155")
    svg += text_m(2.0, 2.35, "[NIRUTHI / SW - HEAVY | FULL WARDROBE]", size=10, fill="#9A3412")

    svg += text_m(1.0, 5.4, "SPACIOUS ATT. BATH\n6'0\" x 8'6\" [WET/DRY]", size=11, weight="600", fill="#0F172A")
    svg += text_m(2.8, 5.4, "SPACIOUS COM. BATH\n6'0\" x 8'6\" [VARUNA]", size=11, weight="600", fill="#0F172A")

    svg += text_m(9.2, 2.1, "MODULAR KITCHEN", size=14, weight="700", fill="#0F172A")
    svg += text_m(9.2, 1.75, "12'-6\" x 11'-6\" [SE AGNEYA]", size=11, weight="600", fill="#C2410C")

    svg += text_m(5.8, 1.5, "DINING AREA\n10'-6\" x 11'-6\"", size=12, weight="600", fill="#0F172A")

    svg += text_m(6.0, 4.4, "GRAND LIVING HALL", size=15, weight="800", fill="#0F172A")
    svg += text_m(6.0, 4.0, "18'-0\" x 14'-0\" [OPEN BRAHMASTHANA]", size=11, weight="600", fill="#047857")

    svg += text_m(5.5, 10.5, "BEDROOM 2", size=14, weight="700", fill="#0F172A")
    svg += text_m(5.5, 10.1, "11'-6\" x 11'-6\" [VAYU/NORTH]", size=11, weight="600", fill="#334155")

    svg += text_m(10.5, 9.5, "POOJA MANDIR\n4'6\" x 6'6\"", size=11, weight="700", fill="#D97706")
    svg += text_m(2.0, PLINTH_D - 0.7, "SIMHADWARAM (D1)\nNORTH-FACING", size=11, weight="700", fill="#059669")
    svg += "</g>\n"

    svg += add_external_vertical_core_svg()
    svg += add_grids_and_dimensions_svg()
    svg += add_title_block_svg("First Floor - Brother's 2BHK Residence")
    svg += "</svg>"

    p = OUTPUT_DIR / "first_floor_brother_blueprint.svg"
    p.write_text(svg, encoding="utf-8")
    print(f"✅ Generated Vector SVG: {p}")

# =============================================================================
# EXPORT 3: SECOND FLOOR — OWNER'S 2BHK + OFFICE + DUAL POOJA
# =============================================================================
def export_second_floor_svg():
    svg = build_base_sheet("Second Floor Plan - Owner's Residence & Office", "L2")
    svg += rect_m(0, 0, PLINTH_W, PLINTH_D, fill="#F8FAFC", stroke="#0F172A", sw=2.0)

    # 1. BALCONIES & EXTERNAL UTILITY
    # North Balcony
    svg += rect_m(3.81, PLINTH_D, 3.50, 1.30, fill="#EFF6FF", stroke="#2563EB", sw=1.5, dash="4,4")
    svg += text_m(5.5, PLINTH_D + 0.65, "NORTH BALCONY (11'-6\" x 4'-3\")", size=11, weight="600", fill="#1D4ED8")
    # East / North-East Open Sitout (LEFT OPEN FOR ISHANYA LIGHT!)
    svg += rect_m(7.31, 8.5, PLINTH_W - 7.31, PLINTH_D - 8.5, fill="#EFF6FF", stroke="#0284C7", sw=1.8)
    svg += text_m(9.2, 11.2, "OPEN ISHANYA (NE) SITOUT", size=14, weight="800", fill="#0369A1")
    svg += text_m(9.2, 10.7, "13'-0\" x 12'-0\" [OPEN TO SKY]", size=12, weight="600", fill="#0284C7")
    svg += text_m(9.2, 10.2, "(Dual Light Corridor to Simhadwaram)", size=10, fill="#075985")
    # South Balcony
    svg += rect_m(0, -1.2, 3.81, 1.2, fill="#EFF6FF", stroke="#2563EB", sw=1.5, dash="4,4")
    svg += text_m(1.9, -0.6, "SOUTH SHADED BALCONY (12'-6\" x 4'-0\")", size=11, weight="600", fill="#1D4ED8")
    # External Out-of-House Utility Balcony
    svg += rect_m(PLINTH_W, 0, 1.4, 3.5, fill="#F1F5F9", stroke="#475569", sw=1.5)
    svg += text_m(PLINTH_W + 0.7, 1.75, "OUT-OF-HOUSE UTILITY\n(WASH & GAS BALCONY)", size=11, weight="600", fill="#334155", rot=-90)

    # 2. EXTERIOR 9" WALLS
    svg += "<g id='exterior_walls'>\n"
    # South Wall
    svg += rect_m(0, 0, 1.2, 0.23, fill="#334155", stroke="#0F172A")
    svg += door_svg("Door_MB_S_Balcony", 1.2, 0.23, 0.90, side='S')
    svg += rect_m(2.1, 0, 3.81 - 2.1, 0.23, fill="#334155", stroke="#0F172A")
    svg += rect_m(3.81, 0, PLINTH_W - 3.81, 0.23, fill="#334155", stroke="#0F172A")
    # East Wall
    svg += rect_m(PLINTH_W - 0.23, 0, 0.23, 1.2, fill="#334155", stroke="#0F172A")
    svg += door_svg("Door_Kit_Utility", PLINTH_W - 0.23, 1.2, 0.85, side='E')
    svg += rect_m(PLINTH_W - 0.23, 2.05, 0.23, 0.15, fill="#334155", stroke="#0F172A")
    svg += window_svg(PLINTH_W - 0.23, 2.2, 0.23, 1.2, is_horiz=False)
    svg += rect_m(PLINTH_W - 0.23, 3.4, 0.23, 1.6, fill="#334155", stroke="#0F172A")
    svg += window_svg(PLINTH_W - 0.23, 5.0, 0.23, 2.2, is_horiz=False)
    svg += rect_m(PLINTH_W - 0.23, 7.2, 0.23, 1.3, fill="#334155", stroke="#0F172A")
    # North Wall (NORTH-FACING HOME OFFICE WINDOW)
    svg += rect_m(0, PLINTH_D - 0.23, 1.5, 0.23, fill="#334155", stroke="#0F172A")
    svg += door_svg("Simhadwaram_D1", 1.5, PLINTH_D - 0.23, 1.05, side='S')
    svg += rect_m(2.55, PLINTH_D - 0.23, 3.81 - 2.55, 0.23, fill="#334155", stroke="#0F172A")
    svg += rect_m(3.81, PLINTH_D - 0.23, 0.49, 0.23, fill="#334155", stroke="#0F172A")
    svg += window_svg(4.3, PLINTH_D - 0.23, 1.9, 0.23, is_horiz=True) # Wide Office Window looking to garden!
    svg += rect_m(6.2, PLINTH_D - 0.23, 1.11, 0.23, fill="#334155", stroke="#0F172A")
    # West Wall
    svg += rect_m(0, 0.23, 0.23, 1.27, fill="#334155", stroke="#0F172A")
    svg += window_svg(0, 1.5, 0.23, 1.5, is_horiz=False)
    svg += rect_m(0, 3.0, 0.23, 2.0, fill="#334155", stroke="#0F172A")
    svg += window_svg(0, 5.0, 0.23, 0.8, is_horiz=False)
    svg += rect_m(0, 5.8, 0.23, PLINTH_D - 0.23 - 5.8, fill="#334155", stroke="#0F172A")
    svg += "</g>\n"

    # 3. INTERIOR PARTITIONS (4.5")
    svg += "<g id='interior_partitions'>\n"
    # Master Bed
    svg += rect_m(3.81 - 0.0575, 0.23, 0.115, 3.83, fill="#475569", stroke="#0F172A")
    svg += rect_m(0.23, 4.06 - 0.0575, 0.27, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_AttBath", 0.5, 4.06, 0.75, side='N') # Attached Bath Door!
    svg += rect_m(1.25, 4.06 - 0.0575, 1.45, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_MB", 2.7, 4.06, 0.90, side='S')
    svg += rect_m(3.6, 4.06 - 0.0575, 0.21, 0.115, fill="#475569", stroke="#0F172A")

    # Spacious Bathrooms
    svg += rect_m(1.83 - 0.0575, 4.06, 0.115, 2.60, fill="#475569", stroke="#0F172A")
    svg += rect_m(0.23, 6.66 - 0.0575, 3.58, 0.115, fill="#475569", stroke="#0F172A")
    svg += rect_m(3.81 - 0.0575, 4.06, 0.115, 1.14, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_CommonBath", 3.81, 5.2, 0.75, side='W')
    svg += rect_m(3.81 - 0.0575, 5.95, 0.115, 0.71, fill="#475569", stroke="#0F172A")

    # Kitchen
    svg += rect_m(7.31 - 0.0575, 0.23, 0.115, 1.97, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Kit", 7.31, 2.2, 0.90, side='W')
    svg += rect_m(7.31 - 0.0575, 3.1, 0.115, 0.40, fill="#475569", stroke="#0F172A")
    svg += rect_m(7.31, 3.5 - 0.0575, PLINTH_W - 0.23 - 7.31, 0.115, fill="#475569", stroke="#0F172A")

    # NORTH-FACING HOME OFFICE (Executive Study)
    svg += rect_m(3.81 - 0.0575, 8.8, 0.115, PLINTH_D - 0.23 - 8.8, fill="#475569", stroke="#0F172A")
    svg += rect_m(7.31 - 0.0575, 8.8, 0.115, PLINTH_D - 0.23 - 8.8, fill="#475569", stroke="#0F172A")
    svg += rect_m(3.81, 8.8 - 0.0575, 0.99, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Office", 4.8, 8.8, 0.90, side='N')
    svg += rect_m(5.7, 8.8 - 0.0575, 1.61, 0.115, fill="#475569", stroke="#0F172A")

    # DUAL POOJA SUITE (DETACHED FROM KITCHEN) & GLAZED LIGHT DOOR
    svg += rect_m(7.31, 8.5 - 0.0575, 0.89, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Ishanya_Light", 8.2, 8.5, 1.20, side='E') # Glazed Double Door!
    svg += rect_m(9.4, 8.5 - 0.0575, 0.60, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Mallanna_Pooja", 10.0, 8.5, 0.90, side='N')
    svg += rect_m(10.9, 8.5 - 0.0575, PLINTH_W - 0.23 - 10.9, 0.115, fill="#475569", stroke="#0F172A")

    # Mallanna Shrine Partitions: X: 8.8 to 11.05, Y: 5.5 to 8.5
    svg += rect_m(8.8 - 0.0575, 5.5, 0.115, 3.0, fill="#475569", stroke="#0F172A")
    svg += rect_m(8.8, 5.5 - 0.0575, 0.80, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Mallanna_Entry", 9.6, 5.5, 0.90, side='N')
    svg += rect_m(10.5, 5.5 - 0.0575, PLINTH_W - 0.23 - 10.5, 0.115, fill="#475569", stroke="#0F172A")

    # Daily Pooja Room: X: 9.4 to 11.05, Y: 8.5 to 10.5
    svg += rect_m(9.4 - 0.0575, 8.5, 0.115, 2.0, fill="#475569", stroke="#0F172A")
    svg += rect_m(9.4, 10.5 - 0.0575, PLINTH_W - 0.23 - 9.4, 0.115, fill="#475569", stroke="#0F172A")
    svg += "</g>\n"

    # 4. MILLWORK, BUILT-IN CUPBOARDS & FURNITURE
    svg += "<g id='millwork_and_furniture'>\n"
    # Master Bed Wardrobe
    svg += rect_m(0.23, 0.35, 0.60, 3.45, fill="#FEF3C7", stroke="#D97706", sw=1.2)
    svg += text_m(0.53, 2.0, "FULL WARDROBE CUPBOARD", size=10, weight="600", fill="#B45309", rot=-90)
    svg += rect_m(1.4, 0.4, 2.0, 2.0, fill="#DBEAFE", stroke="#3B82F6", rx=4)
    svg += text_m(2.4, 1.4, "KING BED\n6'0\" x 6'6\"", size=11, fill="#1D4ED8")
    svg += rect_m(3.81 - 0.40, 1.5, 0.35, 1.7, fill="#E2E8F0", stroke="#475569", sw=1.0)
    svg += text_m(3.81 - 0.22, 2.35, "TV UNIT", size=9, fill="#334155", rot=-90)

    # Home Office Executive Desk & Cupboards
    svg += rect_m(4.6, 10.0, 1.8, 0.8, fill="#FEF3C7", stroke="#D97706", rx=4)
    svg += text_m(5.5, 10.4, "EXECUTIVE DESK\n(NORTH GARDEN VIEW)", size=10, weight="700", fill="#B45309")
    svg += rect_m(3.81 + 0.06, 9.2, 0.55, 2.6, fill="#FEF3C7", stroke="#D97706", sw=1.2)
    svg += text_m(4.1, 10.5, "BOOKCASE CUPBOARD", size=10, fill="#B45309", rot=-90)

    # Mallanna Altar Platform & Prayer Carpet
    svg += rect_m(9.0, 7.5, PLINTH_W - 0.23 - 9.1, 0.9, fill="#FDE68A", stroke="#D97706", rx=2)
    svg += text_m(10.0, 7.95, "SACRED ALTAR PLATFORM", size=10, weight="700", fill="#92400E")
    svg += rect_m(9.0, 5.8, PLINTH_W - 0.23 - 9.2, 1.6, fill="#FEF08A", stroke="#CA8A04", dash="2,2")
    svg += text_m(10.0, 6.6, "4-PERSON PRAYER CARPET\n(4.65 m² CLEAR)", size=10, fill="#854D0E")

    # Living & Dining
    svg += rect_m(4.2, 5.0, 2.8, 0.9, fill="#EDE9FE", stroke="#7C3AED", rx=4)
    svg += rect_m(4.2, 5.9, 0.9, 1.6, fill="#EDE9FE", stroke="#7C3AED", rx=4)
    svg += rect_m(5.5, 6.2, 1.2, 1.0, fill="#F3F4F6", stroke="#4B5563", rx=2)
    svg += text_m(6.1, 6.7, "COFFEE TABLE", size=9, fill="#374151")
    svg += rect_m(3.81 + 0.06, 4.5, 0.40, 2.0, fill="#FEF3C7", stroke="#D97706", sw=1.2)
    svg += text_m(4.0, 5.5, "LIVING TV WALL UNIT", size=10, weight="600", fill="#B45309", rot=-90)
    svg += rect_m(5.0, 2.2, 1.6, 1.4, fill="#FEF3C7", stroke="#D97706", rx=4)
    svg += text_m(5.8, 2.9, "DINING TABLE\n(6-SEATER)", size=11, fill="#B45309")

    # Kitchen & Utility
    svg += rect_m(PLINTH_W - 0.23 - 0.65, 0.23, 0.65, 3.2, fill="#1E293B", stroke="#000000", sw=1.2)
    svg += rect_m(7.4, 0.23, PLINTH_W - 0.23 - 7.4 - 0.65, 0.65, fill="#1E293B", stroke="#000000", sw=1.2)
    svg += rect_m(7.4, 2.5, 0.50, 0.9, fill="#FEF3C7", stroke="#D97706", sw=1.0)
    svg += text_m(7.65, 2.95, "PANTRY", size=9, fill="#B45309", rot=-90)
    svg += rect_m(PLINTH_W - 0.23 - 0.60, 2.1, 0.50, 0.8, fill="#F59E0B", stroke="#B45309", rx=2)
    svg += text_m(PLINTH_W - 0.23 - 0.35, 2.5, "EAST HOB", size=9, fill="#FFFFFF")
    svg += rect_m(PLINTH_W + 0.2, 0.4, 0.7, 0.7, fill="#E2E8F0", stroke="#334155")
    svg += text_m(PLINTH_W + 0.55, 0.75, "WM", size=10, fill="#334155")
    svg += rect_m(PLINTH_W + 0.2, 1.6, 0.6, 0.8, fill="#E2E8F0", stroke="#334155")
    svg += text_m(PLINTH_W + 0.5, 2.0, "SINK", size=10, fill="#334155")
    svg += "</g>\n"

    # 5. LABELS & VAASTU
    svg += "<g id='room_labels'>\n"
    svg += text_m(2.0, 3.1, "MASTER BEDROOM", size=14, weight="700", fill="#0F172A")
    svg += text_m(2.0, 2.7, "12'-6\" x 13'-4\" [3.81m x 4.06m]", size=11, weight="600", fill="#334155")
    svg += text_m(2.0, 2.35, "[NIRUTHI / SW - HEAVY | FULL WARDROBE]", size=10, fill="#9A3412")

    svg += text_m(1.0, 5.4, "SPACIOUS ATT. BATH\n6'0\" x 8'6\" [WET/DRY]", size=11, weight="600", fill="#0F172A")
    svg += text_m(2.8, 5.4, "SPACIOUS COM. BATH\n6'0\" x 8'6\" [VARUNA]", size=11, weight="600", fill="#0F172A")

    svg += text_m(9.2, 2.1, "MODULAR KITCHEN", size=14, weight="700", fill="#0F172A")
    svg += text_m(9.2, 1.75, "12'-6\" x 11'-6\" [SE AGNEYA]", size=11, weight="600", fill="#C2410C")

    svg += text_m(5.5, 11.4, "HOME OFFICE / EXECUTIVE STUDY", size=14, weight="800", fill="#0F172A")
    svg += text_m(5.5, 11.0, "11'-6\" x 11'-0\" [NORTH FRONT GARDEN VIEW]", size=11, weight="600", fill="#1D4ED8")
    svg += text_m(5.5, 10.65, "(Unobstructed by Lift/Core | Executive Millwork)", size=10, fill="#64748B")

    svg += text_m(6.0, 4.4, "GRAND LIVING HALL", size=15, weight="800", fill="#0F172A")
    svg += text_m(6.0, 4.0, "18'-0\" x 14'-0\" [OPEN BRAHMASTHANA]", size=11, weight="600", fill="#047857")

    svg += text_m(9.9, 7.1, "MALLANNA TEMPLE SHRINE", size=12, weight="700", fill="#D97706")
    svg += text_m(9.9, 6.75, "8'-6\" x 10'-0\" [DETACHED FROM KITCHEN]", size=10, weight="600", fill="#B45309")

    svg += text_m(10.2, 9.5, "DAILY POOJA\n5'6\" x 6'6\"", size=11, weight="700", fill="#D97706")
    svg += text_m(2.0, PLINTH_D - 0.7, "SIMHADWARAM (D1)\nNORTH-FACING", size=11, weight="700", fill="#059669")
    svg += "</g>\n"

    svg += add_external_vertical_core_svg()
    svg += add_grids_and_dimensions_svg()
    svg += add_title_block_svg("Second Floor - Owner's Residence & Office")
    svg += "</svg>"

    p = OUTPUT_DIR / "second_floor_owner_blueprint.svg"
    p.write_text(svg, encoding="utf-8")
    print(f"✅ Generated Vector SVG: {p}")

if __name__ == "__main__":
    print("Starting High-Precision Vector SVG Blueprints Export (Redesigned Plan)...")
    export_ground_stilt_svg()
    export_first_floor_svg()
    export_second_floor_svg()
    print("All Vector SVGs Exported Successfully.")
