"""
High-Precision 2D Vector Architectural Blueprint SVG Generator for Property 2 (54' x 66')
Fully calibrated SVG canvas with zero clipping and true coordinate mapping:
  - Level 0 (Ground): Entire Plot (54'x66') + Plinth (37'x40') + Roads + Setbacks + Compound Wall + Gates + Gardens + Parking
  - Level 1 (Brother 2BHK): NNE Simhadwaram, North Verandah from NW Core, West-Door Pooja, Unblocked Common Bath, Balcony from B2
  - Level 2 (Owner Suite): NNE Simhadwaram, North Verandah from NW Core, North Office with Balcony Door, West-Door Dual Pooja
"""

import html
import math
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Metric dimensions: 1 ft = 0.3048 m
PLINTH_W = 37.0 * 0.3048 # 11.2776m
PLINTH_D = 40.0 * 0.3048 # 12.1920m
PLOT_W = 54.0 * 0.3048   # 16.4592m
PLOT_D = 66.0 * 0.3048   # 20.1168m

SETBACK_W = 8.0 * 0.3048  # 2.4384m
SETBACK_S = 9.0 * 0.3048  # 2.7432m
SETBACK_E = 9.0 * 0.3048  # 2.7432m
SETBACK_N = 17.0 * 0.3048 # 5.1816m

PLOT_X0 = -SETBACK_W               # -2.4384m
PLOT_X1 = PLINTH_W + SETBACK_E     # 14.0208m
PLOT_Y0 = -SETBACK_S               # -2.7432m
PLOT_Y1 = PLINTH_D + SETBACK_N     # 17.3736m

GRID_X = [0.115, 3.810, 7.315, PLINTH_W - 0.115]
GRID_Y = [0.115, 4.064, 8.128, PLINTH_D - 0.115]

# Upper Floor Parameters (Scale: 100 px/m)
U_SCALE = 100.0
U_OX = 480.0
U_OY = 1500.0

# Ground Floor Parameters (Scale: 80 px/m)
G_SCALE = 80.0
G_OX = 750.0
G_OY = 1750.0

def to_u_x(x): return U_OX + x * U_SCALE
def to_u_y(y): return U_OY - y * U_SCALE

def to_g_x(x): return G_OX + x * G_SCALE
def to_g_y(y): return G_OY - y * G_SCALE

def xml_escape(text):
    text = html.unescape(str(text))
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def rect_svg(x, y, w, h, is_ground=False, fill="#E5E7EB", stroke="#1F2937", sw=1.5, rx=0, opacity=1.0, dash="", extra=""):
    if dash: extra = f'stroke-dasharray="{dash}" ' + extra
    fx = to_g_x if is_ground else to_u_x
    fy = to_g_y if is_ground else to_u_y
    sc = G_SCALE if is_ground else U_SCALE
    sx = fx(x)
    sy = fy(y + h)
    sw_px = w * sc
    sh_px = h * sc
    return f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{sw_px:.1f}" height="{sh_px:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}" opacity="{opacity}" {extra}/>\n'

def line_svg(x0, y0, x1, y1, is_ground=False, stroke="#4B5563", sw=1.0, dash="", extra=""):
    fx = to_g_x if is_ground else to_u_x
    fy = to_g_y if is_ground else to_u_y
    sx0, sy0 = fx(x0), fy(y0)
    sx1, sy1 = fx(x1), fy(y1)
    dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{sx0:.1f}" y1="{sy0:.1f}" x2="{sx1:.1f}" y2="{sy1:.1f}" stroke="{stroke}" stroke-width="{sw}" {dash_attr} {extra}/>\n'

def text_svg(x, y, text, is_ground=False, size=14, weight="normal", fill="#111827", anchor="middle", rot=0, extra=""):
    fx = to_g_x if is_ground else to_u_x
    fy = to_g_y if is_ground else to_u_y
    sx, sy = fx(x), fy(y)
    transform = f'transform="rotate({rot} {sx:.1f} {sy:.1f})"' if rot != 0 else ""
    text_clean = str(text).replace("\\n", "\n")
    lines = text_clean.split("\n")
    if len(lines) == 1:
        escaped = xml_escape(lines[0])
        return f'<text x="{sx:.1f}" y="{sy:.1f}" font-family="Inter, -apple-system, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {transform} {extra}>{escaped}</text>\n'
    else:
        out = f'<text x="{sx:.1f}" y="{sy:.1f}" font-family="Inter, -apple-system, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {transform} {extra}>\n'
        for i, l in enumerate(lines):
            dy = "-0.3em" if i == 0 and len(lines) > 1 else "1.25em"
            escaped = xml_escape(l)
            out += f'  <tspan x="{sx:.1f}" dy="{dy}">{escaped}</tspan>\n'
        out += '</text>\n'
        return out

def door_symbol(name, hx, hy, w, is_ground=False, side='E'):
    fx = to_g_x if is_ground else to_u_x
    fy = to_g_y if is_ground else to_u_y
    sc = G_SCALE if is_ground else U_SCALE
    r = w * sc
    out = ""
    if side == 'E':
        out += line_svg(hx, hy, hx + w, hy, is_ground=is_ground, stroke="#059669", sw=2.5)
        sx0, sy0 = fx(hx + w), fy(hy)
        sx1, sy1 = fx(hx), fy(hy + w)
        out += f'<path d="M {sx0:.1f} {sy0:.1f} A {r:.1f} {r:.1f} 0 0 0 {sx1:.1f} {sy1:.1f}" fill="none" stroke="#10B981" stroke-width="1.2" stroke-dasharray="3,3"/>\n'
    elif side == 'W':
        out += line_svg(hx, hy, hx - w, hy, is_ground=is_ground, stroke="#059669", sw=2.5)
        sx0, sy0 = fx(hx - w), fy(hy)
        sx1, sy1 = fx(hx), fy(hy + w)
        out += f'<path d="M {sx0:.1f} {sy0:.1f} A {r:.1f} {r:.1f} 0 0 1 {sx1:.1f} {sy1:.1f}" fill="none" stroke="#10B981" stroke-width="1.2" stroke-dasharray="3,3"/>\n'
    elif side == 'N':
        out += line_svg(hx, hy, hx, hy + w, is_ground=is_ground, stroke="#059669", sw=2.5)
        sx0, sy0 = fx(hx), fy(hy + w)
        sx1, sy1 = fx(hx + w), fy(hy)
        out += f'<path d="M {sx0:.1f} {sy0:.1f} A {r:.1f} {r:.1f} 0 0 0 {sx1:.1f} {sy1:.1f}" fill="none" stroke="#10B981" stroke-width="1.2" stroke-dasharray="3,3"/>\n'
    else: # 'S'
        out += line_svg(hx, hy, hx, hy - w, is_ground=is_ground, stroke="#059669", sw=2.5)
        sx0, sy0 = fx(hx), fy(hy - w)
        sx1, sy1 = fx(hx + w), fy(hy)
        out += f'<path d="M {sx0:.1f} {sy0:.1f} A {r:.1f} {r:.1f} 0 0 1 {sx1:.1f} {sy1:.1f}" fill="none" stroke="#10B981" stroke-width="1.2" stroke-dasharray="3,3"/>\n'
    return out

def window_symbol(x0, y0, w, h, is_ground=False, is_horiz=True):
    out = rect_svg(x0, y0, w, h, is_ground=is_ground, fill="#EFF6FF", stroke="#2563EB", sw=1.5)
    if is_horiz:
        out += line_svg(x0, y0 + h/2.0, x0 + w, y0 + h/2.0, is_ground=is_ground, stroke="#3B82F6", sw=1.2)
    else:
        out += line_svg(x0 + w/2.0, y0, x0 + w/2.0, y0 + h, is_ground=is_ground, stroke="#3B82F6", sw=1.2)
    return out

def title_block_svg(sheet_title, is_ground=False):
    bx = to_g_x(PLOT_X1 + 1.2) if is_ground else to_u_x(PLINTH_W + 1.2)
    by = to_g_y(2.6) if is_ground else to_u_y(2.6)
    bw = 480
    bh = 650
    cx = bx + bw / 2.0
    safe_title = xml_escape(sheet_title.upper())
    
    return f'''<g id="title_block">
  <rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="#F8FAFC" stroke="#0F172A" stroke-width="2"/>
  <rect x="{bx+6:.1f}" y="{by+6:.1f}" width="{bw-12:.1f}" height="{bh-12:.1f}" fill="none" stroke="#64748B" stroke-width="1"/>
  
  <text x="{cx:.1f}" y="{by+35:.1f}" font-family="Inter, sans-serif" font-size="17" font-weight="800" fill="#0F172A" text-anchor="middle">PROPERTY 2 RESIDENCE</text>
  <text x="{cx:.1f}" y="{by+62:.1f}" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="#0D9488" text-anchor="middle">{safe_title}</text>
  
  <line x1="{bx+15:.1f}" y1="{by+78:.1f}" x2="{bx+bw-15:.1f}" y2="{by+78:.1f}" stroke="#CBD5E1" stroke-width="1"/>
  
  <text x="{bx+18:.1f}" y="{by+105:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">PLOT:</tspan> 54'-0" x 66'-0" (SW Corner, 3,564 sq ft)</text>
  <text x="{bx+18:.1f}" y="{by+128:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">PLINTH:</tspan> 37'-0" x 40'-0" (1,480 sq ft Footprint)</text>
  <text x="{bx+18:.1f}" y="{by+151:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">SETBACKS:</tspan> N:17' E:9' S:9' W:8' (Vaastu Compliant)</text>
  <text x="{bx+18:.1f}" y="{by+174:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">CORE:</tspan> External NW Stairs &amp; 6-PAX Lift</text>
  <text x="{bx+18:.1f}" y="{by+197:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#0D9488"><tspan font-weight="700">VAASTU:</tspan> Telugu / Telangana (Open Ishanya NE)</text>
  <text x="{bx+18:.1f}" y="{by+220:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">ENTRANCE:</tspan> North-North-East (NNE) Simhadwaram</text>
  <text x="{bx+18:.1f}" y="{by+243:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">POOJA:</tspan> Both Doors West-Facing (Detached)</text>
  <text x="{bx+18:.1f}" y="{by+266:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">BATHS:</tspan> 6'0" x 8'6" Wet/Dry (Unblocked East Door)</text>
  
  <line x1="{bx+15:.1f}" y1="{by+284:.1f}" x2="{bx+bw-15:.1f}" y2="{by+284:.1f}" stroke="#CBD5E1" stroke-width="1"/>
  
  <text x="{bx+18:.1f}" y="{by+308:.1f}" font-family="Inter, sans-serif" font-size="10" fill="#64748B">DOORS: D1: 3'6"x7' | D2: 3'0"x7' | D3: 2'8"x7'</text>
  <text x="{bx+18:.1f}" y="{by+326:.1f}" font-family="Inter, sans-serif" font-size="10" fill="#64748B">WINDOWS: W1: 5'0"x4'6" | W2: 4'0"x4'6" | V1: 2'0"x2'0"</text>
  <text x="{bx+18:.1f}" y="{by+344:.1f}" font-family="Inter, sans-serif" font-size="10" fill="#64748B">BALCONIES: North (from Office), East (Ishanya), &amp; South</text>
</g>
'''

# =============================================================================
# EXPORT 1: GROUND FLOOR — ENTIRE PLOT (54'x66') + BUILT-UP PLINTH (37'x40')
# =============================================================================
def export_ground_stilt_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2600 2300" width="2600" height="2300">
  <defs>
    <pattern id="gridPattern" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#F1F5F9" stroke-width="0.8"/>
    </pattern>
  </defs>

  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <rect x="25" y="25" width="2550" height="2250" fill="none" stroke="#CBD5E1" stroke-width="2"/>
  <rect x="35" y="35" width="2530" height="2230" fill="url(#gridPattern)" stroke="#0F172A" stroke-width="1"/>

  <!-- 30' Roads -->
  <g id="roads">
    {rect_svg(PLOT_X0 - 8.0, PLOT_Y0 - 6.0, 8.0, PLOT_D + 12.0, is_ground=True, fill="#F8FAFC", stroke="#CBD5E1", dash="6,4")}
    {text_svg(PLOT_X0 - 4.0, (PLOT_Y0 + PLOT_Y1)/2.0, "◄◄ 30'-0\" WIDE WEST ROAD (PRIMARY ACCESS & MAIN GATES) ◄◄", is_ground=True, size=15, weight="700", fill="#2563EB", rot=-90)}
    {rect_svg(PLOT_X0 - 8.0, PLOT_Y0 - 6.0, PLOT_W + 15.0, 6.0, is_ground=True, fill="#F8FAFC", stroke="#CBD5E1", dash="6,4")}
    {text_svg((PLOT_X0 + PLOT_X1)/2.0, PLOT_Y0 - 3.5, "▼▼ 30'-0\" WIDE SOUTH ROAD (SECONDARY CORNER ACCESS) ▼▼", is_ground=True, size=15, weight="700", fill="#2563EB")}
  </g>

  <!-- Entire Plot Boundary (54'x66') -->
  <g id="plot_boundary">
    {rect_svg(PLOT_X0, PLOT_Y0, PLOT_W, PLOT_D, is_ground=True, fill="#F8FAFC", stroke="#0F172A", sw=2.5)}
  </g>

  <!-- Landscaped Gardens & Setbacks -->
  <g id="gardens_and_driveway">
    {rect_svg(PLOT_X0 + 0.15, PLINTH_D, PLOT_W - 0.30, SETBACK_N - 0.15, is_ground=True, fill="#DCFCE7", stroke="#86EFAC", sw=1.5, opacity=0.7)}
    {text_svg((PLOT_X0 + PLOT_X1)/2.0, (PLINTH_D + PLOT_Y1)/2.0 + 0.4, "NORTH FRONT GARDEN & LAWN (17'-0\" CLEAR SETBACK)", is_ground=True, size=15, weight="800", fill="#166534")}
    {text_svg((PLOT_X0 + PLOT_X1)/2.0, (PLINTH_D + PLOT_Y1)/2.0 - 0.3, "[OPEN, LIGHT & UNENCUMBERED — VAASTU ALIGNED]", is_ground=True, size=12, weight="600", fill="#15803D")}

    {rect_svg(PLINTH_W, PLOT_Y0 + 0.15, SETBACK_E - 0.15, PLINTH_D - PLOT_Y0 - 0.15, is_ground=True, fill="#DCFCE7", stroke="#86EFAC", sw=1.5, opacity=0.7)}
    {text_svg(PLINTH_W + 1.4, 6.0, "EAST MORNING GARDEN (9'-0\" SETBACK)", is_ground=True, size=13, weight="700", fill="#166534", rot=-90)}

    {rect_svg(0, PLOT_Y0 + 0.15, PLINTH_W, SETBACK_S - 0.15, is_ground=True, fill="#DCFCE7", stroke="#86EFAC", sw=1.0, opacity=0.5)}
    {text_svg(PLINTH_W/2.0, PLOT_Y0 / 2.0, "SOUTH SETBACK: 9'-0\" [2.74m]", is_ground=True, size=12, weight="600", fill="#166534")}

    {rect_svg(PLOT_X0 + 0.15, PLOT_Y0 + 0.15, SETBACK_W - 0.15, PLINTH_D - PLOT_Y0, is_ground=True, fill="#E2E8F0", stroke="#CBD5E1", sw=1.0)}
    {text_svg(PLOT_X0 / 2.0, 3.0, "WEST DRIVEWAY: 8'-0\" SETBACK", is_ground=True, size=11, weight="600", fill="#475569", rot=-90)}
  </g>

  <!-- 6\" Compound Boundary Wall with Gates -->
  <g id="compound_walls">
    {rect_svg(PLOT_X0, PLOT_Y1 - 0.15, PLOT_W, 0.15, is_ground=True, fill="#1E293B", stroke="#0F172A")}
    {rect_svg(PLOT_X1 - 0.15, PLOT_Y0, 0.15, PLOT_D, is_ground=True, fill="#1E293B", stroke="#0F172A")}
    {rect_svg(PLOT_X0, PLOT_Y0, 7.5 - PLOT_X0, 0.15, is_ground=True, fill="#1E293B", stroke="#0F172A")}
    {door_symbol("Gate_South", 7.5, PLOT_Y0 + 0.15, 3.5, is_ground=True, side='E')}
    {text_svg(9.25, PLOT_Y0 - 0.6, "SECONDARY CORNER GATE (30' SOUTH ROAD)", is_ground=True, size=11, weight="700", fill="#2563EB")}
    {rect_svg(11.0, PLOT_Y0, PLOT_X1 - 11.0, 0.15, is_ground=True, fill="#1E293B", stroke="#0F172A")}
    
    {rect_svg(PLOT_X0, PLOT_Y0, 0.15, 8.5 - PLOT_Y0, is_ground=True, fill="#1E293B", stroke="#0F172A")}
    {door_symbol("Gate_Pedestrian", PLOT_X0 + 0.15, 8.5, 1.2, is_ground=True, side='N')}
    {text_svg(PLOT_X0 - 0.6, 9.1, "PEDESTRIAN GATE", is_ground=True, size=10, weight="700", fill="#059669", rot=-90)}
    {rect_svg(PLOT_X0, 9.7, 0.15, 2.3, is_ground=True, fill="#1E293B", stroke="#0F172A")}
    {door_symbol("Gate_Vehicle_Main", PLOT_X0 + 0.15, 12.0, 4.5, is_ground=True, side='N')}
    {text_svg(PLOT_X0 - 0.6, 14.2, "MAIN VEHICLE SLIDING GATE (15'-0\")", is_ground=True, size=12, weight="700", fill="#2563EB", rot=-90)}
    {rect_svg(PLOT_X0, 16.5, 0.15, PLOT_Y1 - 16.5, is_ground=True, fill="#1E293B", stroke="#0F172A")}
  </g>

  <!-- Built-Up Plinth (37' x 40' = 1,480 sq ft) -->
  <g id="plinth_builtup">
    {rect_svg(0, 0, PLINTH_W, PLINTH_D, is_ground=True, fill="#FFFFFF", stroke="#0F172A", sw=2.5)}
    {rect_svg(0, 0, PLINTH_W, 6.2, is_ground=True, fill="#FEF3C7", stroke="#D97706", sw=1.5, opacity=0.8)}
    {text_svg(5.6, 3.5, "SHELTERED OPEN FUNCTION PAVILION", is_ground=True, size=18, weight="800", fill="#92400E")}
    {text_svg(5.6, 2.8, "37'-0\" x 20'-4\" [11.28m x 6.20m] | 750 SQ.FT", is_ground=True, size=14, weight="600", fill="#78350F")}
    {text_svg(5.6, 2.2, "(Family Festivals, Ritual Gathering, Open Plinth Verandah)", is_ground=True, size=12, fill="#B45309")}

    {rect_svg(3.8, PLINTH_D - 5.8, 2.8, 5.5, is_ground=True, fill="#E0F2FE", stroke="#0284C7", sw=1.5, rx=6)}
    {rect_svg(4.1, PLINTH_D - 5.5, 2.2, 4.8, is_ground=True, fill="#BAE6FD", stroke="#0369A1", sw=1.5, rx=12)}
    {text_svg(5.2, PLINTH_D - 3.1, "COVERED CAR PARKING\\n9'-0\" x 18'-0\" [SEDAN/SUV]", is_ground=True, size=13, weight="700", fill="#075985")}

    {rect_svg(7.0, PLINTH_D - 3.0, 2.5, 2.5, is_ground=True, fill="#F0FDF4", stroke="#16A34A", sw=1.5, rx=4)}
    {text_svg(8.25, PLINTH_D - 1.7, "2-WHEELER PARKING\\n(4 MOTORCYCLES)", is_ground=True, size=12, weight="600", fill="#15803D")}
  </g>

  <!-- External NW Core (Stairs + Lift) -->
  <g id="external_core">
    {rect_svg(-2.4, 6.5, 2.4, 5.69, is_ground=True, fill="#F1F5F9", stroke="#475569", sw=1.5)}
    {rect_svg(-2.35, 6.65, 2.1, 3.15, is_ground=True, fill="#E2E8F0", stroke="#64748B", sw=1.2)}
    {text_svg(-1.3, 8.2, "EXTERNAL STAIRS\\n7'3\"x11'0\" [NW VAYU]", is_ground=True, size=11, weight="600", fill="#0F172A", rot=-90)}
    {rect_svg(-2.3, 9.9, 1.9, 2.14, is_ground=True, fill="#E2E8F0", stroke="#334155", sw=2.0)}
    {rect_svg(-1.95, 10.15, 1.2, 1.6, is_ground=True, fill="#FFFFFF", stroke="#0284C7", sw=1.5)}
    {text_svg(-1.3, 11.0, "6-PAX LIFT\\n1.6m x 1.6m", is_ground=True, size=11, weight="700", fill="#0369A1", rot=-90)}
  </g>

  <!-- 16 RCC Columns -->
  <g id="rcc_columns">
'''
    for cx in GRID_X:
        for cy in GRID_Y:
            svg += rect_svg(cx - 0.115, cy - 0.225, 0.230, 0.450, is_ground=True, fill="#0F172A", stroke="#000000", sw=1.0)
            
    svg += f'''  </g>

  <!-- Dual Dimensions (Plot + Plinth) -->
  <g id="dimensions">
    {line_svg(PLOT_X0, PLOT_Y0 - 1.8, PLOT_X1, PLOT_Y0 - 1.8, is_ground=True, stroke="#0F172A", sw=2.0)}
    {line_svg(PLOT_X0, PLOT_Y0 - 2.1, PLOT_X0, PLOT_Y0 - 1.5, is_ground=True, stroke="#0F172A", sw=2.5)}
    {line_svg(PLOT_X1, PLOT_Y0 - 2.1, PLOT_X1, PLOT_Y0 - 1.5, is_ground=True, stroke="#0F172A", sw=2.5)}
    {text_svg((PLOT_X0 + PLOT_X1)/2.0, PLOT_Y0 - 2.3, "54'-0\" [16.46m] TOTAL PLOT WIDTH (EAST-WEST)", is_ground=True, size=15, weight="800", fill="#0F172A")}

    {line_svg(PLOT_X0 - 1.8, PLOT_Y0, PLOT_X0 - 1.8, PLOT_Y1, is_ground=True, stroke="#0F172A", sw=2.0)}
    {line_svg(PLOT_X0 - 2.1, PLOT_Y0, PLOT_X0 - 1.5, PLOT_Y0, is_ground=True, stroke="#0F172A", sw=2.5)}
    {line_svg(PLOT_X0 - 2.1, PLOT_Y1, PLOT_X0 - 1.5, PLOT_Y1, is_ground=True, stroke="#0F172A", sw=2.5)}
    {text_svg(PLOT_X0 - 2.4, (PLOT_Y0 + PLOT_Y1)/2.0, "66'-0\" [20.12m] TOTAL PLOT DEPTH (NORTH-SOUTH)", is_ground=True, size=15, weight="800", fill="#0F172A", rot=-90)}

    {line_svg(0, -1.0, PLINTH_W, -1.0, is_ground=True, stroke="#059669", sw=1.5)}
    {text_svg(PLINTH_W / 2.0, -1.35, "37'-0\" [11.28m] BUILT-UP PLINTH WIDTH", is_ground=True, size=12, weight="700", fill="#059669")}
    {line_svg(-1.0, 0, -1.0, PLINTH_D, is_ground=True, stroke="#059669", sw=1.5)}
    {text_svg(-1.35, PLINTH_D / 2.0, "40'-0\" [12.19m] BUILT-UP PLINTH DEPTH", is_ground=True, size=12, weight="700", fill="#059669", rot=-90)}
  </g>

  <!-- Title Block -->
  {title_block_svg("Ground Floor — Entire Plot & Built-up Plinth", is_ground=True)}
</svg>'''
    
    p = OUTPUT_DIR / "ground_stilt_blueprint.svg"
    p.write_text(svg, encoding="utf-8")
    print(f"✅ Generated Ground Vector SVG: {p}")

# =============================================================================
# EXPORT 2 & 3: UPPER FLOORS SVG GENERATOR (L1 BROTHER & L2 OWNER RESIDENCE)
# =============================================================================
def export_upper_floor_svg(filename, sheet_title, is_owner_level=False):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 1850" width="2400" height="1850">
  <defs>
    <pattern id="gridPattern" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#F1F5F9" stroke-width="0.8"/>
    </pattern>
  </defs>

  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <rect x="25" y="25" width="2350" height="1800" fill="none" stroke="#CBD5E1" stroke-width="2"/>
  <rect x="35" y="35" width="2330" height="1780" fill="url(#gridPattern)" stroke="#0F172A" stroke-width="1"/>

  <!-- Plinth Base Slab -->
  {rect_svg(0, 0, PLINTH_W, PLINTH_D, is_ground=False, fill="#F8FAFC", stroke="#0F172A", sw=2.0)}

  <!-- Covered North Verandah / Walkway Deck (Linking NW Core to NNE Simhadwaram) -->
  <g id="north_verandah">
    {rect_svg(0, PLINTH_D, 7.315, 1.31, is_ground=False, fill="#EFF6FF", stroke="#2563EB", sw=1.5)}
    {line_svg(0, PLINTH_D + 1.28, 7.315, PLINTH_D + 1.28, is_ground=False, stroke="#1D4ED8", sw=2.0)}
    {text_svg(3.6, PLINTH_D + 0.65, "COVERED NORTH VERANDAH / ENTRY WALKWAY (4'-3\" WIDE DECK)", is_ground=False, size=11, weight="700", fill="#1D4ED8")}
  </g>

  <!-- Open Ishanya (NE) Sitout Terrace (Left Open for Sacred Morning Light) -->
  <g id="ishanya_open_terrace">
    {rect_svg(7.315, 9.72, PLINTH_W - 7.315, PLINTH_D - 9.72, is_ground=False, fill="#EFF6FF", stroke="#0284C7", sw=1.8)}
    {text_svg(9.3, 11.4, "OPEN ISHANYA (NE) SITOUT", is_ground=False, size=13, weight="800", fill="#0369A1")}
    {text_svg(9.3, 10.9, "13'-0\" x 8'-0\" [OPEN TO SKY]", is_ground=False, size=11, weight="600", fill="#0284C7")}
    {text_svg(9.3, 10.4, "(Morning Ishanya Sunlight Corridor)", is_ground=False, size=10, fill="#075985")}
  </g>

  <!-- South Shaded Balcony -->
  <g id="south_balcony">
    {rect_svg(0, -1.2, 7.315, 1.2, is_ground=False, fill="#EFF6FF", stroke="#2563EB", sw=1.5, dash="4,4")}
    {text_svg(3.6, -0.6, "SOUTH SHADED SITOUT BALCONY (24'-0\" x 4'-0\")", is_ground=False, size=11, weight="600", fill="#1D4ED8")}
  </g>

  <!-- Out-of-House Utility Balcony (Attached to Kitchen) -->
  <g id="utility_balcony">
    {rect_svg(PLINTH_W, 0, 1.40, 3.80, is_ground=False, fill="#F1F5F9", stroke="#475569", sw=1.5)}
    {text_svg(PLINTH_W + 0.7, 1.9, "OUT-OF-HOUSE UTILITY\\n(WASH & GAS BALCONY)", is_ground=False, size=10, weight="600", fill="#334155", rot=-90)}
  </g>

  <!-- Exterior 9\" Walls -->
  <g id="exterior_walls">
    <!-- South Wall -->
    {rect_svg(0, 0, 1.2, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {door_symbol("Door_MB_S_Balcony", 1.2, 0.23, 0.90, is_ground=False, side='S')}
    {rect_svg(2.1, 0, 1.71, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {rect_svg(3.81, 0, 1.19, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {door_symbol("Door_Dining_S_Balcony", 5.0, 0.23, 1.20, is_ground=False, side='S')}
    {rect_svg(6.2, 0, PLINTH_W - 6.2, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}

    <!-- East Wall -->
    {rect_svg(PLINTH_W - 0.23, 0, 0.23, 1.2, is_ground=False, fill="#334155", stroke="#0F172A")}
    {door_symbol("Door_Kit_Utility", PLINTH_W - 0.23, 1.2, 0.85, is_ground=False, side='E')}
    {rect_svg(PLINTH_W - 0.23, 2.05, 0.23, 0.15, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(PLINTH_W - 0.23, 2.2, 0.23, 1.2, is_ground=False, is_horiz=False)}
    {rect_svg(PLINTH_W - 0.23, 3.4, 0.23, 0.40, is_ground=False, fill="#334155", stroke="#0F172A")}
    {rect_svg(PLINTH_W - 0.23, 4.6, 0.23, 5.0, is_ground=False, fill="#334155", stroke="#0F172A")}

    <!-- North Wall with NNE Simhadwaram & Office Balcony Door -->
    {rect_svg(0, PLINTH_D - 0.23, 1.2, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(1.2, PLINTH_D - 0.23, 1.5, 0.23, is_ground=False, is_horiz=True)}
    {rect_svg(2.7, PLINTH_D - 0.23, 0.20, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    <!-- Direct Balcony Entrance from Office / Bedroom 2! -->
    {door_symbol("Door_NW_Balcony", 2.9, PLINTH_D - 0.23, 0.90, is_ground=False, side='N')}
    {rect_svg(3.8, PLINTH_D - 0.23, 2.2, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    <!-- Grand Simhadwaram (Main Entrance) at North-North-East (NNE) -->
    {door_symbol("Simhadwaram_NNE", 6.0, PLINTH_D - 0.23, 1.10, is_ground=False, side='S')}
    {text_svg(6.55, PLINTH_D - 0.45, "SIMHADWARAM (D1)\\n[NNE PADA]", is_ground=False, size=10, weight="700", fill="#059669")}
    {rect_svg(7.10, PLINTH_D - 0.23, 0.215, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}

    <!-- West Wall -->
    {rect_svg(0, 0.23, 0.23, 3.83, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(0, 1.5, 0.23, 1.5, is_ground=False, is_horiz=False)}
    {rect_svg(0, 4.06, 0.23, 3.54, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(0, 5.2, 0.23, 1.0, is_ground=False, is_horiz=False)}
    {rect_svg(0, 7.60, 0.23, PLINTH_D - 7.60 - 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
  </g>

  <!-- Interior Partitions (4.5\" / 0.115m) -->
  <g id="interior_partitions">
    <!-- Master Bedroom (SW Niruthi) -->
    {rect_svg(3.81 - 0.06, 0.23, 0.115, 2.97, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_MB_Entry", 3.81, 3.20, 0.86, is_ground=False, side='W')}
    {rect_svg(0.23, 4.06 - 0.06, 0.57, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_MB_AttBath", 0.80, 4.06, 0.76, is_ground=False, side='N')}
    {rect_svg(1.56, 4.06 - 0.06, 2.25, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Spacious West Bathrooms (6'0\" x 8'6\" Stacks in Varuna) -->
    {rect_svg(1.95 - 0.06, 4.18, 0.115, 3.42, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(0.23, 7.60 - 0.06, 3.58, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    <!-- Common Bath East Door - 100% UNBLOCKED into Living Hall! -->
    {rect_svg(3.81 - 0.06, 4.18, 0.115, 1.02, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_CommonBath_East", 3.81, 5.20, 0.80, is_ground=False, side='W')}
    {rect_svg(3.81 - 0.06, 6.00, 0.115, 1.60, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Kitchen (SE Agneya) -->
    {rect_svg(7.315 - 0.06, 0.23, 0.115, 1.77, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_Kit_Entry", 7.315, 2.00, 0.90, is_ground=False, side='W')}
    {rect_svg(7.315 - 0.06, 2.90, 0.115, 0.90, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(7.315, 3.80 - 0.06, PLINTH_W - 7.315 - 0.23, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- NW Room (Office on L2 / Bedroom 2 on L1) -->
    {rect_svg(0.23, 7.72 - 0.06, 3.77, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(4.00 - 0.06, 7.72, 0.115, 0.58, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_NW_Room_Entry", 4.00, 8.30, 0.90, is_ground=False, side='W')}
    {rect_svg(4.00 - 0.06, 9.20, 0.115, PLINTH_D - 9.20 - 0.23, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Pooja Complex (East Zone, Detached from Kitchen) -->
    <!-- Mallanna Temple Room (8'-4\" x 8'-0\") -->
    {rect_svg(8.50, 4.60 - 0.06, PLINTH_W - 8.50 - 0.23, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(8.50, 7.04 - 0.06, PLINTH_W - 8.50 - 0.23, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(8.50 - 0.06, 4.60, 0.115, 0.60, is_ground=False, fill="#64748B", stroke="#0F172A")}
    <!-- Mallanna Door on WEST Wall! -->
    {door_symbol("Door_Mallanna_West", 8.50, 5.20, 0.90, is_ground=False, side='E')}
    {rect_svg(8.50 - 0.06, 6.10, 0.115, 0.94, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Daily Pooja Room (8'-4\" x 8'-0\" matching Mallanna width) -->
    {rect_svg(8.50, 9.60 - 0.06, PLINTH_W - 8.50 - 0.23, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(8.50 - 0.06, 7.16, 0.115, 0.64, is_ground=False, fill="#64748B", stroke="#0F172A")}
    <!-- Daily Pooja Door on WEST Wall! -->
    {door_symbol("Door_DailyPooja_West", 8.50, 7.80, 0.80, is_ground=False, side='E')}
    {rect_svg(8.50 - 0.06, 8.60, 0.115, 1.00, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Ishanya Glazed Light Door on West wall of Ishanya Open Sitout -->
    {rect_svg(7.315 - 0.06, 9.60, 1.185, 0.12, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(7.315 - 0.06, 9.72, 0.115, 0.58, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_Ishanya_Glazed_Light", 7.315, 10.30, 1.20, is_ground=False, side='W')}
    {rect_svg(7.315 - 0.06, 11.50, 0.115, PLINTH_D - 11.50 - 0.23, is_ground=False, fill="#64748B", stroke="#0F172A")}
  </g>

  <!-- Built-In Millwork & Furniture Layout -->
  <g id="furniture_and_millwork">
    <!-- Master Bedroom (SW Niruthi) -->
    {rect_svg(0.33, 0.35, 0.60, 3.45, is_ground=False, fill="#FEF3C7", stroke="#D97706", sw=1.2)}
    {text_svg(0.63, 2.05, "FULL WARDROBES", is_ground=False, size=9, fill="#92400E", rot=-90)}
    {rect_svg(1.4, 0.38, 2.0, 2.0, is_ground=False, fill="#DBEAFE", stroke="#2563EB", rx=4)}
    {text_svg(2.4, 1.38, "KING BED\\n(HEAD SOUTH)", is_ground=False, size=10, fill="#1E40AF")}

    <!-- Baths Fixtures -->
    {rect_svg(0.33, 6.2, 1.5, 1.3, is_ground=False, fill="#F0FDF4", stroke="#16A34A")}
    {text_svg(1.08, 6.85, "SHOWER", is_ground=False, size=9, fill="#15803D")}
    {rect_svg(2.15, 6.2, 1.55, 1.3, is_ground=False, fill="#F0FDF4", stroke="#16A34A")}
    {text_svg(2.92, 6.85, "SHOWER", is_ground=False, size=9, fill="#15803D")}

    <!-- Kitchen (SE Agneya) -->
    {rect_svg(PLINTH_W - 0.23 - 0.65, 0.23, 0.65, 3.45, is_ground=False, fill="#1E293B", stroke="#000000", sw=1.2)}
    {rect_svg(7.4, 0.23, PLINTH_W - 0.23 - 7.4 - 0.65, 0.65, is_ground=False, fill="#1E293B", stroke="#000000", sw=1.2)}
    {rect_svg(PLINTH_W - 0.23 - 0.60, 2.2, 0.50, 0.8, is_ground=False, fill="#F59E0B", stroke="#B45309", rx=2)}
    {text_svg(PLINTH_W - 0.23 - 0.35, 2.6, "EAST HOB", is_ground=False, size=9, fill="#FFFFFF")}
    {rect_svg(PLINTH_W + 0.2, 0.4, 0.7, 0.7, is_ground=False, fill="#E2E8F0", stroke="#334155")}
    {text_svg(PLINTH_W + 0.55, 0.75, "WM", is_ground=False, size=10, fill="#334155")}

    <!-- Dining Table -->
    {rect_svg(5.0, 1.8, 1.6, 1.4, is_ground=False, fill="#FEF3C7", stroke="#D97706", rx=4)}
    {text_svg(5.8, 2.5, "DINING TABLE\\n(6-SEATER)", is_ground=False, size=10, fill="#B45309")}

    <!-- Grand Living Hall: TV Console on Dining Divider (Leaving West Bath Passage 100% Clear!) -->
    {rect_svg(4.8, 3.86, 2.0, 0.40, is_ground=False, fill="#334155", stroke="#0F172A", rx=2)}
    {text_svg(5.8, 4.06, "TV ENTERTAINMENT CONSOLE", is_ground=False, size=9, fill="#FFFFFF")}
    {rect_svg(4.8, 6.2, 2.8, 0.9, is_ground=False, fill="#DBEAFE", stroke="#2563EB", rx=4)}
    {text_svg(6.2, 6.65, "LUXURY SECTIONAL SOFA", is_ground=False, size=10, fill="#1E40AF")}
    {rect_svg(6.0, 7.3, 1.2, 0.9, is_ground=False, fill="#FEF3C7", stroke="#D97706", rx=3)}
    {text_svg(6.6, 7.75, "COFFEE TABLE", is_ground=False, size=9, fill="#B45309")}

    <!-- Mallanna Altar (South wall facing North) -->
    {rect_svg(8.8, 4.66, 1.9, 0.65, is_ground=False, fill="#FEF3C7", stroke="#D97706", rx=3)}
    {text_svg(9.75, 4.98, "MALLANNA ALTAR (FACES NORTH)", is_ground=False, size=9, weight="700", fill="#B45309")}
    {rect_svg(8.8, 5.5, 1.9, 1.2, is_ground=False, fill="#FEF2F2", stroke="#DC2626", rx=2)}
    {text_svg(9.75, 6.1, "4-PERSON PUJA CARPET", is_ground=False, size=8, fill="#991B1B")}

    <!-- Daily Pooja Altar (West wall facing East) -->
    {rect_svg(8.56, 8.0, 0.65, 1.4, is_ground=False, fill="#FEF3C7", stroke="#D97706", rx=3)}
    {text_svg(8.88, 8.7, "ALTAR (FACES EAST)", is_ground=False, size=8, weight="700", fill="#B45309", rot=-90)}
'''

    if is_owner_level:
        svg += f'''
    <!-- Level 2: Home Office / Executive Study -->
    {rect_svg(1.8, 9.2, 1.6, 1.0, is_ground=False, fill="#E0E7FF", stroke="#4338CA", rx=4)}
    {text_svg(2.6, 9.7, "EXECUTIVE DESK\\n[GARDEN VIEW]", is_ground=False, size=10, weight="700", fill="#3730A3")}
    {rect_svg(0.4, 8.0, 3.4, 0.5, is_ground=False, fill="#FEF3C7", stroke="#D97706")}
    {text_svg(2.1, 8.25, "EXECUTIVE LIBRARY & BOOKSHELVES", is_ground=False, size=9, fill="#B45309")}
'''
    else:
        svg += f'''
    <!-- Level 1: Bedroom 2 -->
    {rect_svg(1.5, 8.8, 1.8, 2.0, is_ground=False, fill="#DBEAFE", stroke="#2563EB", rx=4)}
    {text_svg(2.4, 9.8, "QUEEN BED", is_ground=False, size=10, fill="#1E40AF")}
    {rect_svg(0.4, 8.0, 3.4, 0.5, is_ground=False, fill="#FEF3C7", stroke="#D97706")}
    {text_svg(2.1, 8.25, "BUILT-IN WARDROBE", is_ground=False, size=9, fill="#B45309")}
'''

    svg += f'''  </g>

  <!-- External NW Core (Stairs & Lift) -->
  <g id="external_core">
    {rect_svg(-2.4, 6.5, 2.4, 5.69, is_ground=False, fill="#F1F5F9", stroke="#475569", sw=1.5)}
    {rect_svg(-2.35, 6.65, 2.1, 3.15, is_ground=False, fill="#E2E8F0", stroke="#64748B", sw=1.2)}
    {text_svg(-1.3, 8.2, "EXTERNAL STAIRS\\n7'3\"x11'0\" [NW VAYU]", is_ground=False, size=11, weight="600", fill="#0F172A", rot=-90)}
    {rect_svg(-2.3, 9.9, 1.9, 2.14, is_ground=False, fill="#E2E8F0", stroke="#334155", sw=2.0)}
    {rect_svg(-1.95, 10.15, 1.2, 1.6, is_ground=False, fill="#FFFFFF", stroke="#0284C7", sw=1.5)}
    {text_svg(-1.3, 11.0, "6-PAX LIFT\\n1.6m x 1.6m", is_ground=False, size=11, weight="700", fill="#0369A1", rot=-90)}
  </g>

  <!-- 16 RCC Columns -->
  <g id="rcc_columns">
'''
    for cx in GRID_X:
        for cy in GRID_Y:
            svg += rect_svg(cx - 0.115, cy - 0.225, 0.230, 0.450, is_ground=False, fill="#0F172A", stroke="#000000", sw=1.0)
            
    svg += f'''  </g>

  <!-- Labels -->
  <g id="room_labels">
    {text_svg(2.0, 3.0, "MASTER BEDROOM", is_ground=False, size=13, weight="700", fill="#0F172A")}
    {text_svg(2.0, 2.65, "12'-6\" x 13'-4\" [3.81m x 4.06m]", is_ground=False, size=11, weight="600", fill="#334155")}
    {text_svg(2.0, 2.35, "[NIRUTHI / SW - HEAVY | PRIVATE SUITE]", is_ground=False, size=9, fill="#9A3412")}

    {text_svg(1.1, 5.4, "SPACIOUS ATT. BATH\\n6'0\" x 8'6\" [PRIVATE]", is_ground=False, size=10, weight="600", fill="#0F172A")}
    {text_svg(2.9, 5.4, "SPACIOUS COM. BATH\\n6'0\" x 8'6\" [EAST DOOR]", is_ground=False, size=10, weight="600", fill="#047857")}

    {text_svg(9.2, 2.0, "MODULAR KITCHEN", is_ground=False, size=13, weight="700", fill="#0F172A")}
    {text_svg(9.2, 1.65, "12'-3\" x 11'-8\" [SE AGNEYA]", is_ground=False, size=10, weight="600", fill="#C2410C")}

    {text_svg(6.3, 8.8, "GRAND LIVING HALL", is_ground=False, size=15, weight="800", fill="#0F172A")}
    {text_svg(6.3, 8.4, "18'-0\" x 14'-0\" [BRAHMASTHANA - OPEN ILLUMINATED CORE]", is_ground=False, size=11, weight="600", fill="#047857")}

    {text_svg(9.8, 6.2, "MALLANNA TEMPLE ROOM", is_ground=False, size=11, weight="700", fill="#D97706")}
    {text_svg(9.8, 5.85, "8'-4\" x 8'-0\" [WEST DOOR | FACES NORTH]", is_ground=False, size=9, weight="600", fill="#B45309")}

    {text_svg(9.8, 8.7, "DAILY POOJA MANDIR", is_ground=False, size=11, weight="700", fill="#D97706")}
    {text_svg(9.8, 8.35, "8'-4\" x 8'-0\" [WEST DOOR | FACES EAST]", is_ground=False, size=9, weight="600", fill="#B45309")}
'''

    if is_owner_level:
        svg += f'''
    {text_svg(2.1, 10.8, "HOME OFFICE / EXECUTIVE STUDY", is_ground=False, size=13, weight="800", fill="#0F172A")}
    {text_svg(2.1, 10.45, "12'-4\" x 13'-11\" [NORTH GARDEN VIEW]", is_ground=False, size=10, weight="600", fill="#1D4ED8")}
    {text_svg(2.1, 10.15, "(Direct Balcony Door | Executive Library)", is_ground=False, size=9, fill="#64748B")}
'''
    else:
        svg += f'''
    {text_svg(2.1, 10.8, "BEDROOM 2 (VAYU / NW)", is_ground=False, size=13, weight="800", fill="#0F172A")}
    {text_svg(2.1, 10.45, "12'-4\" x 13'-11\" [NORTH GARDEN VIEW]", is_ground=False, size=10, weight="600", fill="#1D4ED8")}
    {text_svg(2.1, 10.15, "(Direct Door to North Balcony)", is_ground=False, size=9, fill="#64748B")}
'''

    svg += f'''  </g>

  <!-- Dimensions -->
  <g id="plinth_dims">
    {line_svg(0, -1.0, PLINTH_W, -1.0, is_ground=False, stroke="#475569", sw=1.5)}
    {text_svg(PLINTH_W / 2.0, -1.35, "37'-0\" [11.28m] OVERALL PLINTH WIDTH", is_ground=False, size=12, weight="600", fill="#1E293B")}
    {line_svg(-1.0, 0, -1.0, PLINTH_D, is_ground=False, stroke="#475569", sw=1.5)}
    {text_svg(-1.35, PLINTH_D / 2.0, "40'-0\" [12.19m] PLINTH DEPTH", is_ground=False, size=12, weight="600", fill="#1E293B", rot=-90)}
  </g>

  <!-- Title Block -->
  {title_block_svg(sheet_title, is_ground=False)}
</svg>'''
    
    p = OUTPUT_DIR / filename
    p.write_text(svg, encoding="utf-8")
    print(f"✅ Generated Vector SVG: {p}")

if __name__ == "__main__":
    print("Starting High-Precision Vector SVG Blueprints Export (Full Plot & Setbacks)...")
    export_ground_stilt_svg()
    export_upper_floor_svg("first_floor_brother_blueprint.svg", "First Floor - Brother's 2BHK Residence", is_owner_level=False)
    export_upper_floor_svg("second_floor_owner_blueprint.svg", "Second Floor - Owner's Residence & Office", is_owner_level=True)
    print("All Vector SVGs Exported Successfully.")
