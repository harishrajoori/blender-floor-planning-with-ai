"""
High-Precision 2D Vector Architectural Blueprint SVG Generator for Property 2 (54' x 66')
Generates scalable, layered vector CAD sheets:
  1. Ground Stilt & Parking Blueprint (Level 0)
  2. Brother's 2BHK Residence Blueprint (Level 1)
  3. Owner's 2BHK + Office + Dual Pooja Blueprint (Level 2)
Includes architectural dimension chains, hatching, 16 RCC columns, and title block.
"""

import math
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Scale: 100 pixels per meter (1cm on screen = 1m real world)
SCALE = 100.0
# Origin offset in SVG pixels (giving generous margin for title block, dimensions, and road annotations)
OX = 420.0
OY = 1380.0  # SVG Y is inverted (+Y is down in SVG, so Y_svg = OY - y_m * SCALE)

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
    # Leaf
    if side == 'E':
        out += line_m(hx, hy, hx + w, hy, stroke="#059669", sw=2.5)
        # 90 deg swing arc
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
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2200 1650" width="2200" height="1650" style="background:#FFFFFF;">
<defs>
  <pattern id="grid_pt" width="20" height="20" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="0.75" fill="#E2E8F0"/>
  </pattern>
  <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
    <feDropShadow dx="3" dy="4" stdDeviation="4" flood-opacity="0.12"/>
  </filter>
</defs>
<rect width="2200" height="1650" fill="#FAFAFB"/>
<rect width="2200" height="1650" fill="url(#grid_pt)"/>

<!-- Architectural Sheet Border -->
<rect x="40" y="40" width="2120" height="1570" fill="none" stroke="#0F172A" stroke-width="3"/>
<rect x="48" y="48" width="2104" height="1554" fill="none" stroke="#94A3B8" stroke-width="1"/>

<!-- Title Block & Stamp -->
<g id="title_block" transform="translate(1620, 1150)">
  <rect x="0" y="0" width="480" height="410" fill="#FFFFFF" stroke="#0F172A" stroke-width="2" filter="url(#shadow)"/>
  <rect x="0" y="0" width="480" height="65" fill="#1E293B"/>
  <text x="240" y="40" font-family="Inter, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF" text-anchor="middle">SRI HARISH RAJOORI RESIDENCE</text>
  
  <rect x="0" y="65" width="480" height="50" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/>
  <text x="240" y="98" font-family="Inter, sans-serif" font-size="18" font-weight="700" fill="#0D9488" text-anchor="middle">{title.upper()}</text>
  
  <text x="20" y="145" font-family="Inter, sans-serif" font-size="13" font-weight="600" fill="#334155">PLOT DIMENSIONS: <tspan font-weight="400">54\'-0" x 66\'-0" (SW CORNER)</tspan></text>
  <text x="20" y="172" font-family="Inter, sans-serif" font-size="13" font-weight="600" fill="#334155">BUILT PLINTH: <tspan font-weight="400">37\'-0" x 40\'-0" | 1,480 SQ.FT</tspan></text>
  <text x="20" y="199" font-family="Inter, sans-serif" font-size="13" font-weight="600" fill="#334155">STRUCTURAL GRID: <tspan font-weight="400">16 RCC Columns (9" x 18")</tspan></text>
  <text x="20" y="226" font-family="Inter, sans-serif" font-size="13" font-weight="600" fill="#334155">APPROVED SETBACKS: <tspan font-weight="400">South: 9\', West: 8\', North: 6\', East: 5\'</tspan></text>
  <text x="20" y="253" font-family="Inter, sans-serif" font-size="13" font-weight="600" fill="#334155">VAASTU SHASTRA: <tspan font-weight="700" fill="#D97706">Telugu / Telangana Compliant</tspan></text>
  <text x="20" y="280" font-family="Inter, sans-serif" font-size="13" font-weight="600" fill="#334155">CIVIL STATUS: <tspan font-weight="700" fill="#059669">Verified 3-Bay Structural Partition</tspan></text>
  
  <line x1="15" y1="295" x2="465" y2="295" stroke="#E2E8F0" stroke-width="1.5"/>
  <text x="20" y="325" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#64748B">DOOR SCHEDULE: <tspan font-weight="400">D1: 3\'6"x7\' (Main) | D2: 3\'0"x7\' | D3: 2\'6"x7\' (Bath)</tspan></text>
  <text x="20" y="348" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#64748B">WINDOW SCHEDULE: <tspan font-weight="400">W1: 5\'0"x4\'6" | W2: 4\'0"x4\'6" | V1: 2\'0"x2\'0"</tspan></text>
  <text x="20" y="375" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#64748B">DRAWING NO: <tspan font-weight="700" fill="#0F172A">CAD-{floor_code}-01</tspan> | SCALE: 1:100 @ A3 | DATE: SEP 2026</text>
</g>

<!-- North Arrow Compass -->
<g id="north_arrow" transform="translate(1950, 180)">
  <circle cx="0" cy="0" r="45" fill="#FFFFFF" stroke="#0F172A" stroke-width="2" filter="url(#shadow)"/>
  <polygon points="0,-35 12,15 0,8 -12,15" fill="#DC2626"/>
  <polygon points="0,-35 -12,15 0,8" fill="#991B1B"/>
  <polygon points="0,35 12,8 0,15 -12,8" fill="#CBD5E1"/>
  <text x="0" y="-42" font-family="Inter, sans-serif" font-size="16" font-weight="800" fill="#DC2626" text-anchor="middle">NORTH</text>
</g>

<!-- Road Annotations -->
<g id="road_indicators">
  <!-- West Road -->
  <rect x="70" y="200" width="90" height="1100" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="6,4" rx="8"/>
  <text x="115" y="750" font-family="Inter, sans-serif" font-size="18" font-weight="700" fill="#3B82F6" text-anchor="middle" transform="rotate(-90 115 750)">
    ◄◄ 30\'-0" WIDE WEST ROAD (PRIMARY ACCESS &amp; MAIN GATE ENTRY) ◄◄
  </text>
  
  <!-- South Road -->
  <rect x="250" y="1460" width="1300" height="90" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="6,4" rx="8"/>
  <text x="900" y="1515" font-family="Inter, sans-serif" font-size="18" font-weight="700" fill="#3B82F6" text-anchor="middle">
    ▼▼ 30\'-0" WIDE SOUTH ROAD (SECONDARY CORNER ACCESS) ▼▼
  </text>
</g>
'''
    return svg

def add_grids_and_dimensions_svg():
    out = "<g id='structural_grid_and_dims'>\n"
    # Vertical grid lines X1-X4
    for i, cx in enumerate(GRID_X):
        out += line_m(cx, -1.8, cx, PLINTH_D + 1.8, stroke="#94A3B8", sw=1.0, dash="5,5")
        # Top bubble
        sx, sy = to_svg_x(cx), to_svg_y(PLINTH_D + 2.1)
        out += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="18" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.5"/>\n'
        out += f'<text x="{sx:.1f}" y="{sy+5:.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#0F172A" text-anchor="middle">{i+1}</text>\n'
        # Bottom bubble
        sx, sy = to_svg_x(cx), to_svg_y(-2.1)
        out += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="18" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.5"/>\n'
        out += f'<text x="{sx:.1f}" y="{sy+5:.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#0F172A" text-anchor="middle">{i+1}</text>\n'

    # Horizontal grid lines YA-YD
    lbls = ['A', 'B', 'C', 'D']
    for i, cy in enumerate(GRID_Y):
        out += line_m(-1.8, cy, PLINTH_W + 1.8, cy, stroke="#94A3B8", sw=1.0, dash="5,5")
        # Left bubble
        sx, sy = to_svg_x(-2.1), to_svg_y(cy)
        out += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="18" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.5"/>\n'
        out += f'<text x="{sx:.1f}" y="{sy+5:.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#0F172A" text-anchor="middle">{lbls[i]}</text>\n'
        # Right bubble
        sx, sy = to_svg_x(PLINTH_W + 2.1), to_svg_y(cy)
        out += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="18" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.5"/>\n'
        out += f'<text x="{sx:.1f}" y="{sy+5:.1f}" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#0F172A" text-anchor="middle">{lbls[i]}</text>\n'

    # Dimension chains
    # Overall South: 37'-0"
    out += line_m(0, -1.1, PLINTH_W, -1.1, stroke="#475569", sw=1.5)
    out += line_m(-0.15, -1.25, 0.15, -0.95, stroke="#475569", sw=2.0)
    out += line_m(PLINTH_W - 0.15, -1.25, PLINTH_W + 0.15, -0.95, stroke="#475569", sw=2.0)
    out += text_m(PLINTH_W / 2.0, -1.45, "37'-0\" [11.28m] OVERALL PLINTH WIDTH", size=13, weight="600", fill="#1E293B")

    # Overall West: 40'-0"
    out += line_m(-1.1, 0, -1.1, PLINTH_D, stroke="#475569", sw=1.5)
    out += line_m(-1.25, -0.15, -0.95, 0.15, stroke="#475569", sw=2.0)
    out += line_m(-1.25, PLINTH_D - 0.15, -0.95, PLINTH_D + 0.15, stroke="#475569", sw=2.0)
    out += text_m(-1.45, PLINTH_D / 2.0, "40'-0\" [12.19m] PLINTH DEPTH", size=13, weight="600", fill="#1E293B", rot=-90)

    # 16 Columns
    out += "<g id='rcc_columns'>\n"
    for cx in GRID_X:
        for cy in GRID_Y:
            out += rect_m(cx - 0.115, cy - 0.225, 0.230, 0.450, fill="#0F172A", stroke="#000000", sw=1.0)
    out += "</g>\n"
    out += "</g>\n"
    return out

def export_first_floor_svg():
    svg = build_base_sheet("First Floor Plan - Brother's 2BHK Residence", "L1")
    # Base slab
    svg += rect_m(0, 0, PLINTH_W, PLINTH_D, fill="#F8FAFC", stroke="#0F172A", sw=2.0)
    
    # Exterior 9" Walls
    svg += "<g id='exterior_walls'>\n"
    # South Wall
    svg += rect_m(0, 0, 1.2, 0.23, fill="#334155", stroke="#0F172A")
    svg += window_svg(1.2, 0, 1.5, 0.23, is_horiz=True)
    svg += rect_m(2.7, 0, PLINTH_W - 2.7, 0.23, fill="#334155", stroke="#0F172A")
    
    # East Wall
    svg += rect_m(PLINTH_W - 0.23, 0, 0.23, 1.0, fill="#334155", stroke="#0F172A")
    svg += window_svg(PLINTH_W - 0.23, 1.0, 0.23, 1.2, is_horiz=False)
    svg += rect_m(PLINTH_W - 0.23, 2.2, 0.23, 2.8, fill="#334155", stroke="#0F172A")
    svg += window_svg(PLINTH_W - 0.23, 5.0, 0.23, 2.4, is_horiz=False)
    svg += rect_m(PLINTH_W - 0.23, 7.4, 0.23, PLINTH_D - 7.4, fill="#334155", stroke="#0F172A")
    
    # North Wall
    svg += rect_m(0, PLINTH_D - 0.23, 5.0, 0.23, fill="#334155", stroke="#0F172A")
    svg += window_svg(5.0, PLINTH_D - 0.23, 1.5, 0.23, is_horiz=True)
    svg += rect_m(6.5, PLINTH_D - 0.23, PLINTH_W - 6.5, 0.23, fill="#334155", stroke="#0F172A")
    
    # West Wall
    svg += rect_m(0, 0.23, 0.23, 4.0, fill="#334155", stroke="#0F172A")
    svg += window_svg(0, 4.23, 0.23, 0.6, is_horiz=False)
    svg += rect_m(0, 4.83, 0.23, PLINTH_D - 0.23 - 4.83, fill="#334155", stroke="#0F172A")
    svg += "</g>\n"

    # Partitions (4.5")
    svg += "<g id='interior_partitions'>\n"
    # Master Bed
    svg += rect_m(3.81 - 0.0575, 0.23, 0.115, 3.83, fill="#475569", stroke="#0F172A")
    svg += rect_m(0.23, 4.06 - 0.0575, 1.6, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_MB", 2.7, 4.06, 0.90, side='S')
    svg += rect_m(2.7, 4.06 - 0.0575, 1.05, 0.115, fill="#475569", stroke="#0F172A")
    
    # Baths
    svg += rect_m(1.8 - 0.0575, 4.06, 0.115, 1.94, fill="#475569", stroke="#0F172A")
    svg += rect_m(0.23, 6.0 - 0.0575, 3.58, 0.115, fill="#475569", stroke="#0F172A")
    svg += rect_m(3.81 - 0.0575, 4.06, 0.115, 0.94, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_CB", 3.81, 5.0, 0.75, side='W')
    svg += rect_m(3.81 - 0.0575, 5.75, 0.115, 0.25, fill="#475569", stroke="#0F172A")

    # Kitchen
    svg += rect_m(7.31 - 0.0575, 0.23, 0.115, 2.27, fill="#475569", stroke="#0F172A")
    svg += rect_m(7.31, 3.5 - 0.0575, PLINTH_W - 0.23 - 7.31, 0.115, fill="#475569", stroke="#0F172A")

    # Bed 2
    svg += rect_m(4.6 - 0.0575, 8.13, 0.115, PLINTH_D - 0.23 - 8.13, fill="#475569", stroke="#0F172A")
    svg += rect_m(7.5 - 0.0575, 8.13, 0.115, PLINTH_D - 0.23 - 8.13, fill="#475569", stroke="#0F172A")
    svg += rect_m(4.6, 8.13 - 0.0575, 0.9, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_B2", 5.5, 8.13, 0.90, side='N')
    svg += rect_m(6.4, 8.13 - 0.0575, 1.1, 0.115, fill="#475569", stroke="#0F172A")

    # Pooja & Balcony
    svg += rect_m(7.5 - 0.0575, 8.13, 0.115, 2.37, fill="#475569", stroke="#0F172A")
    svg += rect_m(7.5, 10.5 - 0.0575, 2.0, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Pooja", 8.0, 8.13, 0.80, side='N')

    # Main Door
    svg += door_svg("Door_Simha", 4.6, 6.2, 1.05, side='E')
    svg += "</g>\n"

    # Staircase & Lift
    svg += "<g id='vertical_core'>\n"
    svg += rect_m(0.23, 6.0, 2.2, 4.4, fill="#F1F5F9", stroke="#64748B", sw=1.5)
    svg += rect_m(0.23, 6.0, 2.2, 1.1, fill="#E2E8F0", stroke="#94A3B8")
    for i in range(1, 8):
        ty = 7.1 + i * (3.3 / 8.0)
        svg += line_m(0.23, ty, 1.28, ty, stroke="#94A3B8", sw=1.0)
        svg += line_m(1.38, ty, 2.43, ty, stroke="#94A3B8", sw=1.0)
    svg += line_m(1.33, 7.1, 1.33, 10.4, stroke="#475569", sw=2.0)
    
    # Lift
    svg += rect_m(2.5, 7.5, 2.05, 2.05, fill="#E2E8F0", stroke="#334155", sw=2.0)
    svg += rect_m(2.85, 7.85, 1.35, 1.35, fill="#FFFFFF", stroke="#0284C7", sw=1.5)
    svg += line_m(2.85, 7.85, 4.20, 9.20, stroke="#38BDF8", sw=1.0)
    svg += line_m(2.85, 9.20, 4.20, 7.85, stroke="#38BDF8", sw=1.0)
    svg += "</g>\n"

    # Furniture / Architectural Symbols
    svg += "<g id='furniture_and_millwork'>\n"
    # Master Bed
    svg += rect_m(1.0, 0.4, 1.8, 2.0, fill="#DBEAFE", stroke="#3B82F6", rx=4)
    svg += text_m(1.9, 1.4, "KING BED\n6'0\" x 6'6\"", size=11, fill="#1D4ED8")
    svg += rect_m(0.3, 1.5, 0.6, 2.3, fill="#FEF3C7", stroke="#D97706")
    svg += text_m(0.6, 2.65, "WARDROBE", size=10, fill="#B45309", rot=-90)

    # Bed 2
    svg += rect_m(5.2, 9.7, 1.5, 2.0, fill="#DBEAFE", stroke="#3B82F6", rx=4)
    svg += text_m(5.95, 10.7, "QUEEN BED\n5'0\" x 6'6\"", size=11, fill="#1D4ED8")

    # Kitchen Counter L-shape
    svg += rect_m(PLINTH_W - 0.83, 0.23, 0.6, 3.2, fill="#374151", stroke="#1F2937")
    svg += rect_m(7.4, 0.23, PLINTH_W - 0.83 - 7.4, 0.6, fill="#374151", stroke="#1F2937")
    svg += rect_m(PLINTH_W - 0.8, 1.3, 0.5, 0.6, fill="#E0F2FE", stroke="#0284C7")
    svg += text_m(PLINTH_W - 0.55, 1.6, "SINK", size=9, fill="#0369A1")
    svg += rect_m(PLINTH_W - 0.8, 2.3, 0.5, 0.7, fill="#FEF08A", stroke="#CA8A04")
    svg += text_m(PLINTH_W - 0.55, 2.65, "HOB", size=9, fill="#854D0E")

    # Dining Table
    svg += rect_m(4.8, 1.5, 1.5, 0.9, fill="#FED7AA", stroke="#EA580C", rx=4)
    svg += text_m(5.55, 1.95, "DINING (6-SEAT)\n5'0\" x 3'0\"", size=10, fill="#9A3412")

    # Sofa & Living
    svg += rect_m(PLINTH_W - 1.13, 4.5, 0.9, 2.0, fill="#E0E7FF", stroke="#6366F1", rx=4)
    svg += rect_m(PLINTH_W - 2.2, 5.0, 0.8, 1.0, fill="#F3F4F6", stroke="#9CA3AF")
    svg += text_m(PLINTH_W - 0.68, 5.5, "SOFA", size=10, fill="#4338CA", rot=-90)

    # Pooja Mandir
    svg += rect_m(7.6, 8.2, 1.8, 0.6, fill="#FEF08A", stroke="#EAB308")
    svg += text_m(8.5, 8.5, "POOJA ALTAR", size=10, fill="#854D0E")
    svg += "</g>\n"

    # Room Labels & Vaastu Tags
    svg += "<g id='room_labels'>\n"
    svg += text_m(2.0, 3.2, "MASTER BEDROOM", size=15, weight="700", fill="#0F172A")
    svg += text_m(2.0, 2.8, "12'-6\" x 13'-4\" [3.81m x 4.06m]", size=12, weight="500", fill="#334155")
    svg += text_m(2.0, 2.45, "[NIRUTHI / SW ZONE - HEAVY]", size=11, weight="600", fill="#9A3412")

    svg += text_m(1.0, 5.1, "ATT. TOILET\n5'0\" x 6'6\"", size=11, weight="600", fill="#334155")
    svg += text_m(2.8, 5.1, "COMMON TOILET\n5'0\" x 6'6\" [VARUNA]", size=11, weight="600", fill="#334155")

    svg += text_m(9.2, 2.2, "MODULAR KITCHEN", size=15, weight="700", fill="#0F172A")
    svg += text_m(9.2, 1.85, "12'-6\" x 11'-0\" [3.81m x 3.35m]", size=12, weight="500", fill="#334155")
    svg += text_m(9.2, 1.55, "[AGNEYA / SE ZONE - FIRE]", size=11, weight="600", fill="#C2410C")

    svg += text_m(5.55, 2.9, "DINING AREA\n10'-0\" x 11'-6\"", size=13, weight="600", fill="#0F172A")

    svg += text_m(9.2, 6.0, "FORMAL LIVING ROOM", size=16, weight="700", fill="#0F172A")
    svg += text_m(9.2, 5.6, "14'-0\" x 13'-6\" [4.27m x 4.11m]", size=12, weight="500", fill="#334155")
    svg += text_m(9.2, 5.25, "[CENTRAL BRAHMASTHANA - OPEN]", size=11, weight="600", fill="#0D9488")

    svg += text_m(6.0, 10.6, "BEDROOM 2", size=15, weight="700", fill="#0F172A")
    svg += text_m(6.0, 10.2, "9'-6\" x 12'-6\" [2.90m x 3.81m]", size=12, weight="500", fill="#334155")
    svg += text_m(6.0, 9.85, "[VAYU / NORTH ZONE]", size=11, weight="600", fill="#64748B")

    svg += text_m(8.4, 9.3, "POOJA MANDIR", size=13, weight="700", fill="#D97706")
    svg += text_m(8.4, 8.95, "6'0\" x 7'9\" [ISHANYA]", size=11, weight="600", fill="#B45309")

    svg += text_m(10.0, 11.3, "EAST SITOUT BALCONY", size=13, weight="700", fill="#0284C7")
    svg += text_m(10.0, 10.95, "7'0\" x 12'6\" (OPEN TO SKY)", size=11, weight="500", fill="#0369A1")

    svg += text_m(5.8, 6.7, "SIMHADWARAM MAIN ENTRANCE\nNORTH-FACING [D1]", size=12, weight="700", fill="#059669")
    svg += "</g>\n"

    # Grids & Dims
    svg += add_grids_and_dimensions_svg()
    svg += "</svg>"
    
    path = OUTPUT_DIR / "first_floor_brother_blueprint.svg"
    with open(path, "w") as f:
        f.write(svg)
    print(f"✅ Generated Vector SVG: {path}")

def export_second_floor_svg():
    svg = build_base_sheet("Second Floor Plan - Owner's 2BHK + Office + Dual Pooja", "L2")
    svg += rect_m(0, 0, PLINTH_W, PLINTH_D, fill="#F8FAFC", stroke="#0F172A", sw=2.0)
    
    # Exterior 9" Walls (Identical stack)
    svg += "<g id='exterior_walls'>\n"
    svg += rect_m(0, 0, 1.2, 0.23, fill="#334155", stroke="#0F172A")
    svg += window_svg(1.2, 0, 1.5, 0.23, is_horiz=True)
    svg += rect_m(2.7, 0, PLINTH_W - 2.7, 0.23, fill="#334155", stroke="#0F172A")
    
    svg += rect_m(PLINTH_W - 0.23, 0, 0.23, 1.0, fill="#334155", stroke="#0F172A")
    svg += window_svg(PLINTH_W - 0.23, 1.0, 0.23, 1.2, is_horiz=False)
    svg += rect_m(PLINTH_W - 0.23, 2.2, 0.23, 2.8, fill="#334155", stroke="#0F172A")
    svg += window_svg(PLINTH_W - 0.23, 5.0, 0.23, 2.4, is_horiz=False)
    svg += rect_m(PLINTH_W - 0.23, 7.4, 0.23, PLINTH_D - 7.4, fill="#334155", stroke="#0F172A")
    
    svg += rect_m(0, PLINTH_D - 0.23, 5.0, 0.23, fill="#334155", stroke="#0F172A")
    svg += window_svg(5.0, PLINTH_D - 0.23, 1.5, 0.23, is_horiz=True)
    svg += rect_m(6.5, PLINTH_D - 0.23, PLINTH_W - 6.5, 0.23, fill="#334155", stroke="#0F172A")
    
    svg += rect_m(0, 0.23, 0.23, 4.0, fill="#334155", stroke="#0F172A")
    svg += window_svg(0, 4.23, 0.23, 0.6, is_horiz=False)
    svg += rect_m(0, 4.83, 0.23, PLINTH_D - 0.23 - 4.83, fill="#334155", stroke="#0F172A")
    svg += "</g>\n"

    # Partitions (4.5")
    svg += "<g id='interior_partitions'>\n"
    # Master Bed & Baths
    svg += rect_m(3.81 - 0.0575, 0.23, 0.115, 3.83, fill="#475569", stroke="#0F172A")
    svg += rect_m(0.23, 4.06 - 0.0575, 1.6, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_MB", 2.7, 4.06, 0.90, side='S')
    svg += rect_m(2.7, 4.06 - 0.0575, 1.05, 0.115, fill="#475569", stroke="#0F172A")
    
    svg += rect_m(1.8 - 0.0575, 4.06, 0.115, 1.94, fill="#475569", stroke="#0F172A")
    svg += rect_m(0.23, 6.0 - 0.0575, 3.58, 0.115, fill="#475569", stroke="#0F172A")
    svg += rect_m(3.81 - 0.0575, 4.06, 0.115, 0.94, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_CB", 3.81, 5.0, 0.75, side='W')
    svg += rect_m(3.81 - 0.0575, 5.75, 0.115, 0.25, fill="#475569", stroke="#0F172A")

    # Kitchen
    svg += rect_m(7.31 - 0.0575, 0.23, 0.115, 2.27, fill="#475569", stroke="#0F172A")
    svg += rect_m(7.31, 3.5 - 0.0575, PLINTH_W - 0.23 - 7.31, 0.115, fill="#475569", stroke="#0F172A")

    # Home Office / Study
    svg += rect_m(3.81, 2.8 - 0.0575, 3.5, 0.115, fill="#475569", stroke="#0F172A")
    svg += rect_m(3.81, 5.2 - 0.0575, 1.19, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_Office", 5.0, 5.2, 0.90, side='S')
    svg += rect_m(5.9, 5.2 - 0.0575, 1.41, 0.115, fill="#475569", stroke="#0F172A")

    # Bed 2
    svg += rect_m(4.6 - 0.0575, 8.13, 0.115, PLINTH_D - 0.23 - 8.13, fill="#475569", stroke="#0F172A")
    svg += rect_m(7.5 - 0.0575, 8.13, 0.115, PLINTH_D - 0.23 - 8.13, fill="#475569", stroke="#0F172A")
    svg += rect_m(4.6, 8.13 - 0.0575, 0.9, 0.115, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_B2", 5.5, 8.13, 0.90, side='N')
    svg += rect_m(6.4, 8.13 - 0.0575, 1.1, 0.115, fill="#475569", stroke="#0F172A")

    # NE Dual Pooja Suite (Daily Pooja + Mallanna Temple Shrine)
    svg += rect_m(7.5, 10.5 - 0.0575, PLINTH_W - 0.23 - 7.5, 0.115, fill="#475569", stroke="#0F172A")
    svg += rect_m(8.8 - 0.0575, 10.5, 0.115, PLINTH_D - 0.23 - 10.5, fill="#475569", stroke="#0F172A")
    svg += door_svg("Door_DailyPooja", 8.0, 10.5, 0.80, side='S')
    svg += door_svg("Door_Mallanna", 9.5, 10.5, 0.90, side='N')

    # Main Door
    svg += door_svg("Door_Simha", 4.6, 6.2, 1.05, side='E')
    svg += "</g>\n"

    # Core
    svg += "<g id='vertical_core'>\n"
    svg += rect_m(0.23, 6.0, 2.2, 4.4, fill="#F1F5F9", stroke="#64748B", sw=1.5)
    svg += rect_m(0.23, 6.0, 2.2, 1.1, fill="#E2E8F0", stroke="#94A3B8")
    for i in range(1, 8):
        ty = 7.1 + i * (3.3 / 8.0)
        svg += line_m(0.23, ty, 1.28, ty, stroke="#94A3B8", sw=1.0)
        svg += line_m(1.38, ty, 2.43, ty, stroke="#94A3B8", sw=1.0)
    svg += line_m(1.33, 7.1, 1.33, 10.4, stroke="#475569", sw=2.0)
    
    svg += rect_m(2.5, 7.5, 2.05, 2.05, fill="#E2E8F0", stroke="#334155", sw=2.0)
    svg += rect_m(2.85, 7.85, 1.35, 1.35, fill="#FFFFFF", stroke="#0284C7", sw=1.5)
    svg += line_m(2.85, 7.85, 4.20, 9.20, stroke="#38BDF8", sw=1.0)
    svg += line_m(2.85, 9.20, 4.20, 7.85, stroke="#38BDF8", sw=1.0)
    svg += "</g>\n"

    # Millwork & Furniture
    svg += "<g id='furniture_and_millwork'>\n"
    svg += rect_m(1.0, 0.4, 1.8, 2.0, fill="#DBEAFE", stroke="#3B82F6", rx=4)
    svg += text_m(1.9, 1.4, "KING BED\n6'0\" x 6'6\"", size=11, fill="#1D4ED8")
    svg += rect_m(0.3, 1.5, 0.6, 2.3, fill="#FEF3C7", stroke="#D97706")
    svg += text_m(0.6, 2.65, "WARDROBE", size=10, fill="#B45309", rot=-90)

    # Home Office Executive Desk & Bookcase
    svg += rect_m(4.5, 3.4, 1.5, 0.8, fill="#E2E8F0", stroke="#475569", rx=4)
    svg += text_m(5.25, 3.8, "EXEC WORK DESK\n5'0\" x 2'8\"", size=10, fill="#1E293B")
    svg += rect_m(3.9, 3.2, 0.35, 1.6, fill="#FEF3C7", stroke="#D97706")
    svg += text_m(4.07, 4.0, "BOOKCASE", size=8, fill="#92400E", rot=-90)

    # Bed 2
    svg += rect_m(5.2, 9.7, 1.5, 2.0, fill="#DBEAFE", stroke="#3B82F6", rx=4)
    svg += text_m(5.95, 10.7, "QUEEN BED\n5'0\" x 6'6\"", size=11, fill="#1D4ED8")

    # Kitchen Counter
    svg += rect_m(PLINTH_W - 0.83, 0.23, 0.6, 3.2, fill="#374151", stroke="#1F2937")
    svg += rect_m(7.4, 0.23, PLINTH_W - 0.83 - 7.4, 0.6, fill="#374151", stroke="#1F2937")
    svg += rect_m(PLINTH_W - 0.8, 1.3, 0.5, 0.6, fill="#E0F2FE", stroke="#0284C7")
    svg += text_m(PLINTH_W - 0.55, 1.6, "SINK", size=9, fill="#0369A1")
    svg += rect_m(PLINTH_W - 0.8, 2.3, 0.5, 0.7, fill="#FEF08A", stroke="#CA8A04")
    svg += text_m(PLINTH_W - 0.55, 2.65, "HOB", size=9, fill="#854D0E")

    # Mallanna Shrine Altar & Sacred Prayer Floor
    svg += rect_m(8.9, 10.6, 2.0, 0.7, fill="#FEF08A", stroke="#EAB308", rx=2)
    svg += text_m(9.9, 10.95, "MALLANNA SACRED ALTAR", size=10, weight="700", fill="#854D0E")
    svg += rect_m(9.0, 11.4, 1.9, 0.5, fill="#FED7AA", stroke="#F97316", rx=2)
    svg += text_m(9.95, 11.65, "PRAYER CARPET (4 ADULTS)", size=9, fill="#C2410C")
    svg += "</g>\n"

    # Room Labels
    svg += "<g id='room_labels'>\n"
    svg += text_m(2.0, 3.2, "MASTER BEDROOM", size=15, weight="700", fill="#0F172A")
    svg += text_m(2.0, 2.8, "12'-6\" x 13'-4\" [3.81m x 4.06m]", size=12, weight="500", fill="#334155")
    svg += text_m(2.0, 2.45, "[NIRUTHI / SW ZONE - HEAVY]", size=11, weight="600", fill="#9A3412")

    svg += text_m(1.0, 5.1, "ATT. TOILET\n5'0\" x 6'6\"", size=11, weight="600", fill="#334155")
    svg += text_m(2.8, 5.1, "COMMON TOILET\n5'0\" x 6'6\" [VARUNA]", size=11, weight="600", fill="#334155")

    svg += text_m(9.2, 2.2, "MODULAR KITCHEN", size=15, weight="700", fill="#0F172A")
    svg += text_m(9.2, 1.85, "12'-6\" x 11'-0\" [3.81m x 3.35m]", size=12, weight="500", fill="#334155")
    svg += text_m(9.2, 1.55, "[AGNEYA / SE ZONE - FIRE]", size=11, weight="600", fill="#C2410C")

    # Home Office
    svg += text_m(5.55, 4.5, "HOME OFFICE / STUDY SUITE", size=14, weight="700", fill="#0F172A")
    svg += text_m(5.55, 4.15, "11'-6\" x 8'-0\" [3.50m x 2.44m]", size=12, weight="500", fill="#334155")
    svg += text_m(5.55, 3.85, "[HIGH-FOCUS WORK SUITE]", size=11, weight="600", fill="#2563EB")

    svg += text_m(5.55, 2.2, "DINING AREA\n10'-0\" x 9'-0\"", size=12, weight="600", fill="#0F172A")

    svg += text_m(9.2, 6.0, "FAMILY LIVING AREA", size=16, weight="700", fill="#0F172A")
    svg += text_m(9.2, 5.6, "14'-0\" x 13'-6\" [4.27m x 4.11m]", size=12, weight="500", fill="#334155")
    svg += text_m(9.2, 5.25, "[CENTRAL BRAHMASTHANA - OPEN]", size=11, weight="600", fill="#0D9488")

    svg += text_m(6.0, 10.6, "BEDROOM 2", size=15, weight="700", fill="#0F172A")
    svg += text_m(6.0, 10.2, "9'-6\" x 12'-6\" [2.90m x 3.81m]", size=12, weight="500", fill="#334155")
    svg += text_m(6.0, 9.85, "[VAYU / NORTH ZONE]", size=11, weight="600", fill="#64748B")

    # NE Dual Pooja
    svg += text_m(8.15, 9.5, "DAILY POOJA", size=12, weight="700", fill="#D97706")
    svg += text_m(8.15, 9.15, "4'0\" x 4'0\"", size=11, weight="600", fill="#B45309")

    svg += text_m(10.0, 11.5, "MALLANNA TEMPLE SHRINE", size=14, weight="700", fill="#DC2626")
    svg += text_m(10.0, 11.15, "9'0\" x 9'0\" [81 SQ.FT]", size=12, weight="600", fill="#991B1B")
    svg += text_m(10.0, 10.85, "[SACRED ISHANYA / NE CORNER]", size=11, weight="600", fill="#D97706")

    svg += text_m(5.8, 6.7, "SIMHADWARAM MAIN ENTRANCE\nNORTH-FACING [D1]", size=12, weight="700", fill="#059669")
    svg += "</g>\n"

    # Grids & Dims
    svg += add_grids_and_dimensions_svg()
    svg += "</svg>"
    
    path = OUTPUT_DIR / "second_floor_owner_blueprint.svg"
    with open(path, "w") as f:
        f.write(svg)
    print(f"✅ Generated Vector SVG: {path}")

def export_ground_stilt_svg():
    svg = build_base_sheet("Ground Stilt Floor & Parking Plan", "L0")
    svg += rect_m(0, 0, PLINTH_W, PLINTH_D, fill="#F8FAFC", stroke="#0F172A", sw=2.0)
    
    # Pavilion zone
    svg += rect_m(0, 0, PLINTH_W, 6.0, fill="#FEFCE8", stroke="#CA8A04", sw=1.5, opacity=0.7)
    
    # Parking bays
    svg += rect_m(PLINTH_W - 3.2, PLINTH_D - 5.5, 2.8, 5.2, fill="#F0F9FF", stroke="#0284C7", sw=1.5, dash="4,4")
    svg += rect_m(PLINTH_W - 4.6, PLINTH_D - 2.8, 1.2, 2.4, fill="#F0FDF4", stroke="#16A34A", sw=1.5, dash="4,4")
    svg += rect_m(PLINTH_W - 4.6, PLINTH_D - 5.4, 1.2, 2.4, fill="#F0FDF4", stroke="#16A34A", sw=1.5, dash="4,4")
    
    # Staircase & Lift Core
    svg += "<g id='vertical_core'>\n"
    svg += rect_m(0.23, 6.0, 2.2, 4.4, fill="#F1F5F9", stroke="#64748B", sw=1.5)
    svg += rect_m(0.23, 6.0, 2.2, 1.1, fill="#E2E8F0", stroke="#94A3B8")
    for i in range(1, 8):
        ty = 7.1 + i * (3.3 / 8.0)
        svg += line_m(0.23, ty, 1.28, ty, stroke="#94A3B8", sw=1.0)
        svg += line_m(1.38, ty, 2.43, ty, stroke="#94A3B8", sw=1.0)
    svg += line_m(1.33, 7.1, 1.33, 10.4, stroke="#475569", sw=2.0)
    
    svg += rect_m(2.5, 7.5, 2.05, 2.05, fill="#E2E8F0", stroke="#334155", sw=2.0)
    svg += rect_m(2.85, 7.85, 1.35, 1.35, fill="#FFFFFF", stroke="#0284C7", sw=1.5)
    svg += line_m(2.85, 7.85, 4.20, 9.20, stroke="#38BDF8", sw=1.0)
    svg += line_m(2.85, 9.20, 4.20, 7.85, stroke="#38BDF8", sw=1.0)
    svg += "</g>\n"

    # Annotations
    svg += "<g id='ground_annotations'>\n"
    svg += text_m(5.6, 3.4, "SHELTERED OPEN FUNCTION PAVILION", size=18, weight="700", fill="#0F172A")
    svg += text_m(5.6, 2.9, "37'-0\" x 20'-0\" [11.28m x 6.10m] | 740 SQ.FT", size=14, weight="500", fill="#334155")
    svg += text_m(5.6, 2.4, "(Community & Family Gatherings, Traditional Events, Plinth Verandah)", size=12, weight="500", fill="#64748B")

    svg += text_m(PLINTH_W - 1.8, PLINTH_D - 2.8, "COVERED CAR STALL\n8'-6\" x 17'-0\"\n[NE DRIVEWAY ACCESS]", size=12, weight="700", fill="#0284C7")
    svg += text_m(PLINTH_W - 4.0, PLINTH_D - 1.6, "2-WHEELERS\n(2 BIKES)", size=10, weight="600", fill="#16A34A")
    svg += text_m(PLINTH_W - 4.0, PLINTH_D - 4.2, "2-WHEELERS\n(2 BIKES)", size=10, weight="600", fill="#16A34A")

    svg += text_m(1.33, 8.2, "DOG-LEGGED STAIRCASE\n7'-3\" x 14'-6\" [NW VAYU]", size=12, weight="700", fill="#1E293B", rot=-90)
    svg += text_m(3.52, 8.5, "PASSENGER LIFT\n6-PAX CORE", size=11, weight="700", fill="#0284C7", rot=-90)
    svg += "</g>\n"

    svg += add_grids_and_dimensions_svg()
    svg += "</svg>"
    
    path = OUTPUT_DIR / "ground_stilt_blueprint.svg"
    with open(path, "w") as f:
        f.write(svg)
    print(f"✅ Generated Vector SVG: {path}")

if __name__ == "__main__":
    export_ground_stilt_svg()
    export_first_floor_svg()
    export_second_floor_svg()
