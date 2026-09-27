"""
Vector SVG Architectural Blueprint Generator for Property 2 (54' x 66' Plot)
Generates high-precision, publication-grade SVG blueprints for:
  - Ground Floor: Entire Plot (54'x66') + Built-up Plinth (37'x40') + Setbacks + Gardens + Parking
  - Level 1: Brother's Full 3 BHK (Master SW, Bed 2 NW, Bed 3 North, Daily Pooja, Family Lounge, 360° Walk-Around Slab)
  - Level 2: Owner's 2 BHK + North Home Office + Mallanna Shrine (Faces North) + Daily Pooja (4' max width, faces East)
Features:
  - Independent Private Lobby (Zero walking through bedrooms!)
  - All 16 RCC Columns (9"x18") 100% Embedded in Walls (Zero Free-Standing Columns)
  - Continuous 360° Cantilever Walk-Around Slab Gallery
  - Utility Balcony entered from Dining Lobby, NEVER from Kitchen
  - 10-Tread Stair Flights with Mid-Landing and 6-PAX Lift
"""

from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Metric & Imperial Constants (1 ft = 0.3048 m)
PLOT_W = 54.0 * 0.3048   # 16.4592m
PLOT_D = 66.0 * 0.3048   # 20.1168m
PLINTH_W = 37.0 * 0.3048 # 11.2776m
PLINTH_D = 40.0 * 0.3048 # 12.1920m

SETBACK_W = 8.0 * 0.3048  # 2.4384m
SETBACK_S = 9.0 * 0.3048  # 2.7432m
SETBACK_E = 9.0 * 0.3048  # 2.7432m
SETBACK_N = 17.0 * 0.3048 # 5.1816m

PLOT_X0 = -SETBACK_W
PLOT_X1 = PLINTH_W + SETBACK_E
PLOT_Y0 = -SETBACK_S
PLOT_Y1 = PLINTH_D + SETBACK_N

# Column Grid Coordinates
GRID_X = [0.115, 3.810, 7.315, PLINTH_W - 0.115]
GRID_Y = [0.115, 4.064, 8.128, PLINTH_D - 0.115]

# Upper Floor Plan Canvas & Scaling (2400 x 1850)
U_OX = 320
U_OY = 1450
U_SCALE = 100.0

# Ground Floor Plan Canvas & Scaling (2400 x 2000)
G_OX = 360
G_OY = 1680
G_SCALE = 78.0

def to_u_x(x): return U_OX + x * U_SCALE
def to_u_y(y): return U_OY - y * U_SCALE

def to_g_x(x): return G_OX + x * G_SCALE
def to_g_y(y): return G_OY - y * G_SCALE

def xml_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def rect_svg(x, y, w, h, is_ground=False, fill="#E5E7EB", stroke="#1F2937", sw=1.5, rx=0, opacity=1.0, dash="", extra=""):
    fx = to_g_x if is_ground else to_u_x
    fy = to_g_y if is_ground else to_u_y
    sc = G_SCALE if is_ground else U_SCALE
    sx = fx(x)
    sy = fy(y + h)
    sw_px = w * sc
    sh_px = h * sc
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    op_attr = f' fill-opacity="{opacity}"' if opacity < 1.0 else ""
    return f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{sw_px:.1f}" height="{sh_px:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash_attr}{op_attr} {extra}/>\n'

def line_svg(x0, y0, x1, y1, is_ground=False, stroke="#4B5563", sw=1.0, dash="", extra=""):
    fx = to_g_x if is_ground else to_u_x
    fy = to_g_y if is_ground else to_u_y
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{fx(x0):.1f}" y1="{fy(y0):.1f}" x2="{fx(x1):.1f}" y2="{fy(y1):.1f}" stroke="{stroke}" stroke-width="{sw}"{dash_attr} {extra}/>\n'

def text_svg(x, y, text, is_ground=False, size=14, weight="normal", fill="#111827", anchor="middle", rot=0, extra=""):
    fx = to_g_x if is_ground else to_u_x
    fy = to_g_y if is_ground else to_u_y
    sx = fx(x)
    sy = fy(y)
    rot_attr = f' transform="rotate({rot} {sx:.1f} {sy:.1f})"' if rot != 0 else ""
    
    lines = text.split("\\n")
    if len(lines) == 1:
        escaped = xml_escape(lines[0])
        return f'<text x="{sx:.1f}" y="{sy:.1f}" font-family="Inter, -apple-system, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{rot_attr} {extra}>{escaped}</text>\n'
    else:
        out = f'<text x="{sx:.1f}" y="{sy:.1f}" font-family="Inter, -apple-system, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{rot_attr} {extra}>\n'
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
    bx = to_g_x(PLOT_X1 + 1.2) if is_ground else to_u_x(PLINTH_W + 1.8)
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
  <text x="{bx+18:.1f}" y="{by+197:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">SLAB:</tspan> Continuous 360° Walk-Around Cantilever</text>
  <text x="{bx+18:.1f}" y="{by+220:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#0D9488"><tspan font-weight="700">COLUMNS:</tspan> 16 RCC (9"x18") 100% Embedded in Walls</text>
  <text x="{bx+18:.1f}" y="{by+243:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">UTILITY:</tspan> External Balcony via Dining Lobby</text>
  <text x="{bx+18:.1f}" y="{by+266:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#334155"><tspan font-weight="700">DAILY POOJA:</tspan> Compact 4' Width (Faces East)</text>
  <text x="{bx+18:.1f}" y="{by+289:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#D97706"><tspan font-weight="700">PRIVATE LOBBY:</tspan> Unblocked Independent Access</text>
  <text x="{bx+18:.1f}" y="{by+312:.1f}" font-family="Inter, sans-serif" font-size="11" fill="#0D9488"><tspan font-weight="700">SIMHADWARAM:</tspan> North-North-East (NNE) Entrance</text>
  
  <line x1="{bx+15:.1f}" y1="{by+330:.1f}" x2="{bx+bw-15:.1f}" y2="{by+330:.1f}" stroke="#CBD5E1" stroke-width="1"/>
  
  <text x="{bx+18:.1f}" y="{by+355:.1f}" font-family="Inter, sans-serif" font-size="10" fill="#64748B">DOORS: D1: 3'6"x7' | D2: 3'0"x7' | D3: 2'8"x7'</text>
  <text x="{bx+18:.1f}" y="{by+375:.1f}" font-family="Inter, sans-serif" font-size="10" fill="#64748B">VAASTU: Telangana Vaastu Compliant</text>
  <text x="{bx+18:.1f}" y="{by+395:.1f}" font-family="Inter, sans-serif" font-size="10" fill="#64748B">DRAWING NO: CAD-2026-P2-01 | REV: C</text>
</g>'''

# =============================================================================
# EXPORT 1: GROUND FLOOR STILT & SITE PLAN
# =============================================================================
def export_ground_stilt_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 2000" width="2400" height="2000">
  <defs>
    <pattern id="gridPattern" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#F1F5F9" stroke-width="0.8"/>
    </pattern>
  </defs>

  <!-- Canvas Background -->
  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <rect x="25" y="25" width="2350" height="1950" fill="none" stroke="#CBD5E1" stroke-width="2"/>
  <rect x="35" y="35" width="2330" height="1930" fill="url(#gridPattern)" stroke="#0F172A" stroke-width="1"/>

  <!-- Public Roads (West 30' & South 24') -->
  <g id="roads">
    {rect_svg(PLOT_X0 - 9.144, PLOT_Y0 - 7.315, 9.144, PLOT_D + 8.315, is_ground=True, fill="#F1F5F9", stroke="#94A3B8", sw=1.5)}
    {text_svg(PLOT_X0 - 4.5, (PLOT_Y0 + PLOT_Y1)/2.0, "30'-0\" WIDE WEST ROAD (PRIMARY ACCESS & MAIN GATES)", is_ground=True, size=15, weight="700", fill="#475569", rot=-90)}

    {rect_svg(PLOT_X0 - 9.144, PLOT_Y0 - 7.315, PLOT_W + 10.144, 7.315, is_ground=True, fill="#F1F5F9", stroke="#94A3B8", sw=1.5)}
    {text_svg((PLOT_X0 + PLOT_X1)/2.0, PLOT_Y0 - 3.6, "24'-0\" WIDE SOUTH ROAD (SECONDARY CORNER ACCESS)", is_ground=True, size=15, weight="700", fill="#475569")}
  </g>

  <!-- Total Plot (54' x 66') -->
  <g id="plot_boundary">
    {rect_svg(PLOT_X0, PLOT_Y0, PLOT_W, PLOT_D, is_ground=True, fill="#FAFAFA", stroke="#0F172A", sw=2.5)}
  </g>

  <!-- Setback Zones & Gardens -->
  <g id="setbacks">
    {rect_svg(0, PLINTH_D, PLINTH_W + SETBACK_E - 0.15, SETBACK_N - 0.15, is_ground=True, fill="#DCFCE7", stroke="#86EFAC", sw=1.5, opacity=0.8)}
    {text_svg((PLINTH_W + SETBACK_E)/2.0, PLINTH_D + 2.8, "NORTH FRONT LAWN & VAASTU GARDEN (17'-0\" SETBACK - OPEN TO SKY)", is_ground=True, size=14, weight="800", fill="#166534")}
    {text_svg((PLINTH_W + SETBACK_E)/2.0, PLINTH_D + 2.1, "Maximum Morning Sunlight & North Energy Flow", is_ground=True, size=11, fill="#15803D")}

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
    {text_svg(9.25, PLOT_Y0 - 0.6, "SECONDARY CORNER GATE (10' WIDE)", is_ground=True, size=11, weight="700", fill="#2563EB")}
    {rect_svg(11.0, PLOT_Y0, PLOT_X1 - 11.0, 0.15, is_ground=True, fill="#1E293B", stroke="#0F172A")}
    
    {rect_svg(PLOT_X0, PLOT_Y0, 0.15, 8.5 - PLOT_Y0, is_ground=True, fill="#1E293B", stroke="#0F172A")}
    {door_symbol("Gate_Pedestrian", PLOT_X0 + 0.15, 8.5, 1.2, is_ground=True, side='N')}
    {text_svg(PLOT_X0 - 0.6, 9.1, "PEDESTRIAN GATE", is_ground=True, size=10, weight="700", fill="#059669", rot=-90)}
    {rect_svg(PLOT_X0, 9.7, 0.15, 2.3, is_ground=True, fill="#1E293B", stroke="#0F172A")}
    {door_symbol("Gate_Vehicle_Main", PLOT_X0 + 0.15, 12.0, 4.5, is_ground=True, side='N')}
    {text_svg(PLOT_X0 - 0.6, 14.2, "MAIN VEHICLE SLIDING GATE (14'-0\")", is_ground=True, size=12, weight="700", fill="#2563EB", rot=-90)}
    {rect_svg(PLOT_X0, 16.5, 0.15, PLOT_Y1 - 16.5, is_ground=True, fill="#1E293B", stroke="#0F172A")}
  </g>

  <!-- Built-Up Plinth (37' x 40' = 1,480 sq ft) -->
  <g id="plinth_builtup">
    {rect_svg(0, 0, PLINTH_W, PLINTH_D, is_ground=True, fill="#FFFFFF", stroke="#0F172A", sw=2.5)}
    {rect_svg(3.810, 4.064, PLINTH_W - 3.810, PLINTH_D - 4.064, is_ground=True, fill="#FEF3C7", stroke="#D97706", sw=1.5, opacity=0.85)}
    {text_svg(7.5, 8.5, "SHELTERED OPEN FUNCTION PAVILION", is_ground=True, size=16, weight="800", fill="#92400E")}
    {text_svg(7.5, 7.8, "APPROX 750 SQ FT CLEAR SPACE", is_ground=True, size=13, weight="600", fill="#78350F")}
    {text_svg(7.5, 7.1, "(Family Gatherings, Rituals & Festivals)", is_ground=True, size=11, fill="#B45309")}

    <!-- Covered Car Parking -->
    {rect_svg(3.810, 0, 3.505, 4.064, is_ground=True, fill="#E0F2FE", stroke="#0284C7", sw=1.5, rx=4)}
    {text_svg(5.5, 2.0, "CAR PARKING 1\\n(COVERED)", is_ground=True, size=12, weight="700", fill="#075985")}

    {rect_svg(7.315, 0, PLINTH_W - 7.315, 4.064, is_ground=True, fill="#E0F2FE", stroke="#0284C7", sw=1.5, rx=4)}
    {text_svg(9.3, 2.0, "CAR PARKING 2\\n(COVERED)", is_ground=True, size=12, weight="700", fill="#075985")}

    <!-- 4x Bike Parking -->
    {rect_svg(0, 0, 3.810, 4.064, is_ground=True, fill="#F0FDF4", stroke="#16A34A", sw=1.5, rx=4)}
    {text_svg(1.9, 2.0, "4x BIKE PARKING\\n+ EV CHARGING", is_ground=True, size=12, weight="700", fill="#15803D")}
  </g>

  <!-- External NW Core (Stairs + Lift) -->
  <g id="external_core">
    {rect_svg(-2.4, 6.5, 2.4, 5.69, is_ground=True, fill="#F1F5F9", stroke="#475569", sw=1.5)}
    <!-- Stair Treads -->
    {rect_svg(-2.25, 7.5, 1.0, 2.2, is_ground=True, fill="#E2E8F0", stroke="#64748B", sw=1.2)}
    {rect_svg(-1.15, 7.5, 1.0, 2.2, is_ground=True, fill="#E2E8F0", stroke="#64748B", sw=1.2)}
    {rect_svg(-2.25, 6.65, 2.1, 0.85, is_ground=True, fill="#CBD5E1", stroke="#475569", sw=1.2)}
    {text_svg(-1.2, 7.05, "MID LANDING (4'x8')", is_ground=True, size=9, weight="600", fill="#334155")}
    {text_svg(-1.75, 8.6, "UP ->", is_ground=True, size=10, weight="700", fill="#2563EB", rot=-90)}
    {text_svg(-0.65, 8.6, "<- DN", is_ground=True, size=10, weight="700", fill="#DC2626", rot=-90)}

    <!-- 6-PAX Lift -->
    {rect_svg(-2.3, 9.9, 2.1, 2.14, is_ground=True, fill="#E2E8F0", stroke="#334155", sw=2.0)}
    {rect_svg(-2.0, 10.15, 1.5, 1.6, is_ground=True, fill="#FFFFFF", stroke="#0284C7", sw=1.5)}
    {text_svg(-1.25, 11.0, "6-PAX LIFT\\n(AUTOMATIC)", is_ground=True, size=11, weight="700", fill="#0369A1", rot=-90)}
  </g>

  <!-- 16 RCC Columns -->
  <g id="rcc_columns">
'''
    for cx in GRID_X:
        for cy in GRID_Y:
            svg += rect_svg(cx - 0.115, cy - 0.225, 0.230, 0.450, is_ground=True, fill="#0F172A", stroke="#000000", sw=1.0)
            
    svg += f'''  </g>

  <!-- Vaastu Sump & RWH -->
  <g id="vaastu_water">
    {rect_svg(10.5, 13.5, 2.0, 2.0, is_ground=True, fill="#E0F2FE", stroke="#0284C7", sw=1.5, rx=4)}
    {text_svg(11.5, 14.5, "UNDERGROUND SUMP\\n(ISHANYA / NE)", is_ground=True, size=10, weight="700", fill="#0369A1")}
    {rect_svg(12.8, 14.0, 0.8, 1.5, is_ground=True, fill="#BAE6FD", stroke="#0284C7", sw=1.2, rx=2)}
    {text_svg(13.2, 14.75, "RWH", is_ground=True, size=9, weight="700", fill="#0284C7", rot=-90)}
  </g>

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
# EXPORT 2 & 3: UPPER FLOORS SVG GENERATOR (L1 BROTHER 3BHK & L2 OWNER 2BHK+OFFICE)
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

  <!-- Plinth Base Slab (37'x40') -->
  {rect_svg(0, 0, PLINTH_W, PLINTH_D, is_ground=False, fill="#F8FAFC", stroke="#0F172A", sw=2.0)}

  <!-- Continuous 360° Cantilever Walk-Around Slab Gallery -->
  <g id="continuous_360_slab_gallery">
    <!-- North Cantilever Promenade (4'-3\" wide = 1.30m) -->
    {rect_svg(0, PLINTH_D, PLINTH_W, 1.30, is_ground=False, fill="#EFF6FF", stroke="#2563EB", sw=1.5)}
    {line_svg(0, PLINTH_D + 1.25, PLINTH_W, PLINTH_D + 1.25, is_ground=False, stroke="#1D4ED8", sw=2.0)}
    {text_svg(PLINTH_W / 2.0, PLINTH_D + 0.65, "CONTINUOUS NORTH CANTILEVER VERANDAH / ENTRY PROMENADE (4'-3\" WIDE DECK)", is_ground=False, size=11, weight="700", fill="#1D4ED8")}

    <!-- East Cantilever Gallery & Utility Balcony (3'-6\" to 4'-8\" wide) -->
    {rect_svg(PLINTH_W, 0, 1.07, PLINTH_D, is_ground=False, fill="#EFF6FF", stroke="#2563EB", sw=1.5)}
    {rect_svg(PLINTH_W, 0, 1.42, 4.80, is_ground=False, fill="#F1F5F9", stroke="#475569", sw=1.5)}
    {line_svg(PLINTH_W + 1.37, 0, PLINTH_W + 1.42, 4.80, is_ground=False, stroke="#334155", sw=2.0)}
    {text_svg(PLINTH_W + 0.7, 2.4, "OUT-OF-HOUSE UTILITY BALCONY\\n(WASH, WM & GAS CAGE)", is_ground=False, size=10, weight="600", fill="#334155", rot=-90)}

    <!-- South Shaded Balcony (3'-6\" wide across full South facade) -->
    {rect_svg(0, -1.07, PLINTH_W, 1.07, is_ground=False, fill="#EFF6FF", stroke="#2563EB", sw=1.5, dash="4,4")}
    {text_svg(PLINTH_W / 2.0, -0.55, "SOUTH SHADED SITOUT BALCONY (37'-0\" x 3'-6\" CANTILEVER DECK)", is_ground=False, size=11, weight="600", fill="#1D4ED8")}

    <!-- West Service Walkway (3'-0\" wide connecting South Balcony to NW Core) -->
    {rect_svg(-0.91, -1.07, 0.91, 7.57, is_ground=False, fill="#EFF6FF", stroke="#2563EB", sw=1.2, dash="4,4")}
    {text_svg(-0.45, 2.5, "WEST 360° WALKWAY", is_ground=False, size=9, weight="600", fill="#2563EB", rot=-90)}
  </g>

  <!-- Open Ishanya (NE) Sitout Terrace (x=8.535 to PLINTH_W, y=8.128 to PLINTH_D) -->
  <g id="ishanya_open_terrace">
    {rect_svg(8.535, 8.128, PLINTH_W - 8.535, PLINTH_D - 8.128, is_ground=False, fill="#EFF6FF", stroke="#0284C7", sw=1.8)}
    {text_svg(9.8, 11.2, "OPEN ISHANYA (NE) SITOUT", is_ground=False, size=13, weight="800", fill="#0369A1")}
    {text_svg(9.8, 10.7, "12'-6\" x 8'-0\" [OPEN TO SKY]", is_ground=False, size=11, weight="600", fill="#0284C7")}
    {text_svg(9.8, 10.2, "(Morning Sunlight & Cross-Ventilation Corridor)", is_ground=False, size=9, fill="#075985")}
  </g>

  <!-- Exterior 9\" Walls -->
  <g id="exterior_walls">
    <!-- South Exterior Wall -->
    {rect_svg(0, 0, 1.2, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {door_symbol("Door_MB_S_Balcony", 1.2, 0.23, 0.90, is_ground=False, side='S')}
    {rect_svg(2.1, 0, 2.7, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {door_symbol("Door_Dining_S_Balcony", 4.8, 0.23, 1.50, is_ground=False, side='S')}
    {rect_svg(6.3, 0, PLINTH_W - 6.3, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}

    <!-- East Exterior Wall -->
    {rect_svg(PLINTH_W - 0.23, 0, 0.23, 2.0, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(PLINTH_W - 0.23, 2.0, 0.23, 1.4, is_ground=False, is_horiz=False)}
    {rect_svg(PLINTH_W - 0.23, 3.4, 0.23, 1.0, is_ground=False, fill="#334155", stroke="#0F172A")}
    <!-- UTILITY DOOR FROM DINING LOBBY (y=4.40 to 5.25) - NEVER FROM KITCHEN! -->
    {door_symbol("Door_Utility_from_Lobby", PLINTH_W - 0.23, 4.40, 0.85, is_ground=False, side='E')}
    {text_svg(PLINTH_W + 0.15, 4.85, "DOOR TO UTILITY (FROM DINING LOBBY)", is_ground=False, size=9, weight="700", fill="#059669")}
    {rect_svg(PLINTH_W - 0.23, 5.25, 0.23, 0.55, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(PLINTH_W - 0.23, 5.80, 0.23, 1.4, is_ground=False, is_horiz=False)}
    {rect_svg(PLINTH_W - 0.23, 7.20, 0.23, PLINTH_D - 7.20, is_ground=False, fill="#334155", stroke="#0F172A")}

    <!-- North Exterior Wall -->
    {rect_svg(0, PLINTH_D - 0.23, 1.0, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(1.0, PLINTH_D - 0.23, 1.5, 0.23, is_ground=False, is_horiz=True)}
    {rect_svg(2.5, PLINTH_D - 0.23, 0.10, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {door_symbol("Door_NW_Balcony", 2.6, PLINTH_D - 0.23, 0.90, is_ground=False, side='N')}
    {rect_svg(3.5, PLINTH_D - 0.23, 0.70, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(4.2, PLINTH_D - 0.23, 1.4, 0.23, is_ground=False, is_horiz=True)}
    {rect_svg(5.6, PLINTH_D - 0.23, 0.20, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {door_symbol("Door_NC_Balcony", 5.8, PLINTH_D - 0.23, 0.90, is_ground=False, side='N')}
    {rect_svg(6.7, PLINTH_D - 0.23, 0.615, 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}

    <!-- West Exterior Wall -->
    {rect_svg(0, 0.23, 0.23, 3.834, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(0, 1.5, 0.23, 1.5, is_ground=False, is_horiz=False)}
    {rect_svg(0, 4.064, 0.23, 4.064, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(0, 5.2, 0.23, 2.0, is_ground=False, is_horiz=False)}
    {rect_svg(0, 8.128, 0.23, PLINTH_D - 8.128 - 0.23, is_ground=False, fill="#334155", stroke="#0F172A")}
    {window_symbol(0, 9.2, 0.23, 1.4, is_ground=False, is_horiz=False)}
  </g>

  <!-- Interior Partitions (Aligned with Column Grid Lines x=3.810, 7.315 and y=4.064, 8.128) -->
  <g id="interior_partitions">
    <!-- Master Bedroom East Wall (x=3.810) -->
    {rect_svg(3.810 - 0.06, 0.23, 0.115, 3.834, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Master Bed North Wall (y=4.064) with private Attached Bath door & Lobby Entry -->
    {rect_svg(0.23, 4.064 - 0.06, 0.57, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_AttBath_Private", 0.80, 4.064, 0.80, is_ground=False, side='N')}
    {rect_svg(1.60, 4.064 - 0.06, 1.00, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    <!-- Door into Master Bed from Private Lobby (y=4.064, x=2.60 to 3.46) -->
    {door_symbol("Door_MB_Entry", 2.60, 4.064, 0.86, is_ground=False, side='S')}
    {rect_svg(3.46, 4.064 - 0.06, 0.35, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Bathrooms Divider (Horizontal wall at y=6.10, x=0.23 to 2.10) -->
    {rect_svg(0.23, 6.10 - 0.06, 1.87, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    <!-- Common Bath North Wall (y=8.128, x=0.23 to 2.10) -->
    {rect_svg(0.23, 8.128 - 0.06, 1.87, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Common Bathroom East Wall (x=2.10) - SHIELDED DOOR INSIDE PRIVATE LOBBY -->
    {rect_svg(2.10 - 0.06, 4.064, 0.115, 2.836, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_ComBath_East", 2.10, 6.90, 0.80, is_ground=False, side='W')}
    {rect_svg(2.10 - 0.06, 7.70, 0.115, 0.428, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- PRIVATE LOBBY NORTH WALL (y=8.128, x=2.10 to 3.810): DIRECT DOOR TO NW ROOM! -->
    {rect_svg(2.10, 8.128 - 0.06, 0.30, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_NWRoom_Entry", 2.40, 8.128, 0.90, is_ground=False, side='N')}
    {rect_svg(3.30, 8.128 - 0.06, 0.51, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Private Lobby East Wall & Archway (x=3.810): Vanity at South, Archway at North -->
    {rect_svg(3.810 - 0.06, 4.064, 0.115, 2.036, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {line_svg(3.810, 6.10, 3.810, 8.128, is_ground=False, stroke="#0D9488", sw=2.0, dash="5,5")}
    {text_svg(3.810, 7.1, "OPEN ARCHWAY TO LOBBY (6'-4\" WIDE)", is_ground=False, size=9, weight="700", fill="#0D9488", rot=-90)}

    <!-- SOLID SOUNDPROOF PARTITION BETWEEN NORTH ROOMS (x=3.810, y=8.128 to PLINTH_D) -->
    {rect_svg(3.810 - 0.06, 8.128, 0.115, PLINTH_D - 8.128 - 0.23, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- North-Central Bedroom Entrance from Living (y=8.128, x=3.810 to 7.315) -->
    {rect_svg(3.810, 8.128 - 0.06, 0.69, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_NC_Room_Entry", 4.50, 8.128, 0.90, is_ground=False, side='N')}
    {rect_svg(5.40, 8.128 - 0.06, 1.915, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Dining/Living Partition (y=4.064, x=3.810 to 7.315) -->
    {rect_svg(3.810, 4.064 - 0.06, 3.505, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- Kitchen Walls (SE Agneya) -->
    {rect_svg(7.315, 4.064 - 0.06, PLINTH_W - 7.315 - 0.23, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(7.315 - 0.06, 0.23, 0.115, 1.97, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_Kit_Entry", 7.315, 2.20, 0.90, is_ground=False, side='W')}
    {rect_svg(7.315 - 0.06, 3.10, 0.115, 0.964, is_ground=False, fill="#64748B", stroke="#0F172A")}

    <!-- GRID LINE x=7.315: ENCASES COLUMN C11 (7.315, 8.128) - ZERO EXPOSED COLUMNS! -->
    {rect_svg(7.315 - 0.06, 7.20, 0.115, PLINTH_D - 7.20 - 0.23, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Simhadwaram_D1_NNE", 7.315, 10.60, 1.10, is_ground=False, side='W')}
    {text_svg(7.315 - 0.45, 11.15, "SIMHADWARAM (D1)\\n[NNE ENTRANCE]", is_ground=False, size=10, weight="700", fill="#059669", rot=-90)}

    <!-- Compact Daily Pooja Room (4'-0\" Width Max: x=7.315 to 8.535, y=8.128 to 10.45) -->
    {rect_svg(7.315, 10.45 - 0.06, 1.22, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(8.535 - 0.06, 8.128, 0.115, 2.322, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_DailyPooja_West", 7.315, 8.50, 0.80, is_ground=False, side='E')}
'''

    if is_owner_level:
        # L2: Mallanna Shrine (8'-4" x 8'-0", detached from kitchen, faces North)
        svg += f'''
    <!-- Mallanna Temple Room (x=7.315 to 9.855, y=4.80 to 7.24) -->
    {rect_svg(7.315, 4.80 - 0.06, 2.54, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(9.855 - 0.06, 4.80, 0.115, 2.44, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(7.315, 7.24 - 0.06, 2.54, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(7.315 - 0.06, 4.80, 0.115, 0.80, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {door_symbol("Door_Mallanna_West", 7.315, 5.60, 0.90, is_ground=False, side='E')}
    {rect_svg(7.315 - 0.06, 6.50, 0.115, 0.74, is_ground=False, fill="#64748B", stroke="#0F172A")}
'''
    else:
        # L1: Family Lounge (Open East Room)
        svg += f'''
    <!-- Family Lounge (x=7.315 to PLINTH_W, y=4.80 to 8.128) -->
    {rect_svg(7.315, 4.80 - 0.06, PLINTH_W - 7.315 - 0.23, 0.115, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {rect_svg(7.315 - 0.06, 4.80, 0.115, 0.60, is_ground=False, fill="#64748B", stroke="#0F172A")}
    {line_svg(7.315, 5.40, 7.315, 7.00, is_ground=False, stroke="#0D9488", sw=2.0, dash="5,5")}
    {text_svg(7.315, 6.2, "OPEN LOUNGE ARCHWAY", is_ground=False, size=9, weight="700", fill="#0D9488", rot=-90)}
    {rect_svg(7.315 - 0.06, 7.00, 0.115, 1.128, is_ground=False, fill="#64748B", stroke="#0F172A")}
'''

    svg += f'''  </g>

  <!-- Built-In Millwork & Furniture Layout -->
  <g id="furniture_and_millwork">
    <!-- Master Bedroom (SW Niruthi) -->
    {rect_svg(0.33, 0.35, 0.60, 3.45, is_ground=False, fill="#FEF3C7", stroke="#D97706", sw=1.2)}
    {text_svg(0.63, 2.05, "FULL WARDROBES", is_ground=False, size=9, fill="#92400E", rot=-90)}
    {rect_svg(1.4, 0.38, 2.0, 2.0, is_ground=False, fill="#DBEAFE", stroke="#2563EB", rx=4)}
    {text_svg(2.4, 1.38, "KING BED\\n(HEAD SOUTH)", is_ground=False, size=10, fill="#1E40AF")}

    <!-- Baths Fixtures -->
    {rect_svg(0.33, 5.2, 0.8, 0.8, is_ground=False, fill="#F0FDF4", stroke="#16A34A")}
    {text_svg(0.73, 5.6, "SHOWER", is_ground=False, size=8, fill="#15803D")}
    {rect_svg(1.3, 4.2, 0.65, 0.7, is_ground=False, fill="#E2E8F0", stroke="#334155")}
    {text_svg(1.62, 4.55, "VANITY", is_ground=False, size=8, fill="#334155")}

    {rect_svg(0.33, 7.2, 0.8, 0.8, is_ground=False, fill="#F0FDF4", stroke="#16A34A")}
    {text_svg(0.73, 7.6, "SHOWER", is_ground=False, size=8, fill="#15803D")}
    {rect_svg(1.3, 6.2, 0.65, 0.7, is_ground=False, fill="#E2E8F0", stroke="#334155")}
    {text_svg(1.62, 6.55, "VANITY", is_ground=False, size=8, fill="#334155")}

    <!-- Private Lobby Handwash Counter -->
    {rect_svg(3.25, 4.25, 0.50, 1.05, is_ground=False, fill="#FEF3C7", stroke="#D97706", rx=2)}
    {text_svg(3.50, 4.77, "HANDWASH\\nVANITY", is_ground=False, size=8, weight="700", fill="#B45309", rot=-90)}

    <!-- Kitchen (SE Agneya) -->
    {rect_svg(PLINTH_W - 0.23 - 0.65, 0.23, 0.65, 3.45, is_ground=False, fill="#1E293B", stroke="#000000", sw=1.2)}
    {rect_svg(7.4, 0.23, PLINTH_W - 0.23 - 7.4 - 0.65, 0.65, is_ground=False, fill="#1E293B", stroke="#000000", sw=1.2)}
    {rect_svg(PLINTH_W - 0.23 - 0.60, 2.2, 0.50, 0.8, is_ground=False, fill="#F59E0B", stroke="#B45309", rx=2)}
    {text_svg(PLINTH_W - 0.23 - 0.35, 2.6, "EAST HOB", is_ground=False, size=9, fill="#FFFFFF")}

    <!-- Out-of-House Utility Balcony Fixtures -->
    {rect_svg(PLINTH_W + 0.2, 0.4, 0.7, 0.7, is_ground=False, fill="#E2E8F0", stroke="#334155")}
    {text_svg(PLINTH_W + 0.55, 0.75, "WM", is_ground=False, size=9, fill="#334155")}
    {rect_svg(PLINTH_W + 0.2, 1.6, 0.6, 0.8, is_ground=False, fill="#E2E8F0", stroke="#334155")}
    {text_svg(PLINTH_W + 0.5, 2.0, "SINK", is_ground=False, size=9, fill="#334155")}
    {rect_svg(PLINTH_W + 0.2, 3.0, 0.6, 0.8, is_ground=False, fill="#E2E8F0", stroke="#334155")}
    {text_svg(PLINTH_W + 0.5, 3.4, "GAS", is_ground=False, size=9, fill="#334155")}

    <!-- Dining Table -->
    {rect_svg(4.8, 1.6, 1.6, 1.4, is_ground=False, fill="#FEF3C7", stroke="#D97706", rx=4)}
    {text_svg(5.6, 2.3, "DINING TABLE\\n(6-SEATER)", is_ground=False, size=10, fill="#B45309")}

    <!-- Grand Living Hall -->
    {rect_svg(4.6, 4.12, 2.0, 0.38, is_ground=False, fill="#334155", stroke="#0F172A", rx=2)}
    {text_svg(5.6, 4.31, "TV CONSOLE", is_ground=False, size=9, fill="#FFFFFF")}
    {rect_svg(4.6, 5.5, 2.4, 0.9, is_ground=False, fill="#DBEAFE", stroke="#2563EB", rx=4)}
    {text_svg(5.8, 5.95, "SECTIONAL SOFA", is_ground=False, size=10, fill="#1E40AF")}
    {rect_svg(5.2, 6.6, 1.2, 0.8, is_ground=False, fill="#FEF3C7", stroke="#D97706", rx=3)}
    {text_svg(5.8, 7.0, "COFFEE TABLE", is_ground=False, size=9, fill="#B45309")}

    <!-- North-Central Bedroom Furniture -->
    {rect_svg(4.8, 8.4, 1.8, 2.0, is_ground=False, fill="#DBEAFE", stroke="#2563EB", rx=4)}
    {text_svg(5.7, 9.4, "BEDROOM BED\\n(QUEEN)", is_ground=False, size=10, fill="#1E40AF")}
    {rect_svg(3.91, 10.0, 0.55, 1.8, is_ground=False, fill="#FEF3C7", stroke="#D97706")}
    {text_svg(4.18, 10.9, "WARDROBES", is_ground=False, size=8, fill="#B45309", rot=-90)}

    <!-- Daily Pooja Altar (Compact 4' width, faces East) -->
    {rect_svg(7.42, 8.6, 0.50, 1.2, is_ground=False, fill="#FEF3C7", stroke="#D97706", rx=3)}
    {text_svg(7.67, 9.2, "ALTAR (FACES EAST)", is_ground=False, size=8, weight="700", fill="#B45309", rot=-90)}
'''

    if is_owner_level:
        svg += f'''
    <!-- Level 2: Home Office / Executive Study in NW -->
    {rect_svg(1.2, 9.6, 1.6, 1.0, is_ground=False, fill="#E0E7FF", stroke="#4338CA", rx=4)}
    {text_svg(2.0, 10.1, "EXECUTIVE DESK\\n[GARDEN VIEW]", is_ground=False, size=10, weight="700", fill="#3730A3")}
    {rect_svg(0.35, 8.4, 0.40, 3.0, is_ground=False, fill="#FEF3C7", stroke="#D97706")}
    {text_svg(0.55, 9.9, "EXECUTIVE LIBRARY &amp; BOOKSHELVES", is_ground=False, size=8, fill="#B45309", rot=-90)}

    <!-- Mallanna Shrine in East-Central (Faces North) -->
    {rect_svg(7.8, 4.95, 1.6, 0.60, is_ground=False, fill="#FEF3C7", stroke="#D97706", rx=3)}
    {text_svg(8.6, 5.25, "MALLANNA ALTAR (FACES NORTH)", is_ground=False, size=9, weight="700", fill="#B45309")}
    {rect_svg(7.8, 5.75, 1.6, 1.25, is_ground=False, fill="#FEF2F2", stroke="#DC2626", rx=2)}
    {text_svg(8.6, 6.37, "PUJA RITUAL CARPET", is_ground=False, size=9, fill="#991B1B")}
'''
    else:
        svg += f'''
    <!-- Level 1: Bedroom 2 in NW -->
    {rect_svg(1.4, 9.2, 1.8, 2.0, is_ground=False, fill="#DBEAFE", stroke="#2563EB", rx=4)}
    {text_svg(2.3, 10.2, "BEDROOM 2\\nKING BED", is_ground=False, size=10, fill="#1E40AF")}
    {rect_svg(0.35, 8.4, 0.40, 3.0, is_ground=False, fill="#FEF3C7", stroke="#D97706")}
    {text_svg(0.55, 9.9, "BUILT-IN WARDROBES", is_ground=False, size=8, fill="#B45309", rot=-90)}

    <!-- Family Lounge in East-Central (Replacing Mallanna on L1) -->
    {rect_svg(7.8, 5.2, 2.7, 1.0, is_ground=False, fill="#DBEAFE", stroke="#2563EB", rx=4)}
    {text_svg(9.15, 5.7, "FAMILY LOUNGE SOFA", is_ground=False, size=10, fill="#1E40AF")}
    {rect_svg(7.8, 6.8, 2.7, 0.8, is_ground=False, fill="#FEF3C7", stroke="#D97706")}
    {text_svg(9.15, 7.2, "STUDY / LIBRARY DESK", is_ground=False, size=9, fill="#B45309")}
'''

    svg += f'''  </g>

  <!-- External NW Core (Stairs & Lift) -->
  <g id="external_core">
    {rect_svg(-2.4, 6.5, 2.4, 5.69, is_ground=False, fill="#F1F5F9", stroke="#475569", sw=1.5)}
    <!-- Stair Flights -->
    {rect_svg(-2.25, 7.5, 1.0, 2.2, is_ground=False, fill="#E2E8F0", stroke="#64748B", sw=1.2)}
    {rect_svg(-1.15, 7.5, 1.0, 2.2, is_ground=False, fill="#E2E8F0", stroke="#64748B", sw=1.2)}
    {rect_svg(-2.25, 6.65, 2.1, 0.85, is_ground=False, fill="#CBD5E1", stroke="#475569", sw=1.2)}
    {text_svg(-1.2, 7.05, "MID LANDING (4'x8')", is_ground=False, size=9, weight="600", fill="#334155")}
    {text_svg(-1.75, 8.6, "UP ->", is_ground=False, size=10, weight="700", fill="#2563EB", rot=-90)}
    {text_svg(-0.65, 8.6, "<- DN", is_ground=False, size=10, weight="700", fill="#DC2626", rot=-90)}

    <!-- 6-PAX Lift -->
    {rect_svg(-2.3, 9.9, 2.1, 2.14, is_ground=False, fill="#E2E8F0", stroke="#334155", sw=2.0)}
    {rect_svg(-2.0, 10.15, 1.5, 1.6, is_ground=False, fill="#FFFFFF", stroke="#0284C7", sw=1.5)}
    {text_svg(-1.25, 11.0, "6-PAX LIFT\\n(AUTOMATIC)", is_ground=False, size=11, weight="700", fill="#0369A1", rot=-90)}
  </g>

  <!-- 16 RCC Columns (ALL 100% EMBEDDED IN WALLS) -->
  <g id="rcc_columns">
'''
    for cx in GRID_X:
        for cy in GRID_Y:
            svg += rect_svg(cx - 0.115, cy - 0.225, 0.230, 0.450, is_ground=False, fill="#0F172A", stroke="#000000", sw=1.0)
            
    svg += f'''  </g>

  <!-- Labels -->
  <g id="room_labels">
    {text_svg(2.2, 3.0, "MASTER BEDROOM (BED 1)", is_ground=False, size=13, weight="700", fill="#0F172A")}
    {text_svg(2.2, 2.65, "13'-3\" x 13'-3\" [4.04m x 4.04m]", is_ground=False, size=11, weight="600", fill="#334155")}
    {text_svg(2.2, 2.35, "[NIRUTHI / SW - HEAVY | PRIVATE SUITE]", is_ground=False, size=9, fill="#9A3412")}

    {text_svg(1.15, 5.1, "ATT. BATH\\n6'-3\" x 6'-8\"\\n[PRIVATE]", is_ground=False, size=9, weight="600", fill="#0F172A")}
    {text_svg(1.15, 7.1, "COMMON BATH\\n6'-3\" x 6'-8\"\\n[SHIELDED DOOR]", is_ground=False, size=9, weight="600", fill="#047857")}

    {text_svg(2.95, 6.2, "PRIVATE LOBBY\\n5'-7\" WIDE GALLERY\\n(DIRECT ACCESS)", is_ground=False, size=9, weight="700", fill="#1E40AF")}

    {text_svg(9.3, 2.0, "MODULAR KITCHEN", is_ground=False, size=13, weight="700", fill="#0F172A")}
    {text_svg(9.3, 1.65, "12'-4\" x 13'-3\" [SE AGNEYA]", is_ground=False, size=10, weight="600", fill="#C2410C")}

    {text_svg(5.6, 6.7, "GRAND LIVING HALL (BRAHMASTHANA)", is_ground=False, size=14, weight="800", fill="#0F172A")}
    {text_svg(5.6, 6.35, "18'-0\" x 14'-0\" [ZERO EXPOSED COLUMNS | FULLY EMBEDDED]", is_ground=False, size=10, weight="600", fill="#047857")}
'''

    if is_owner_level:
        svg += f'''
    {text_svg(2.0, 11.2, "HOME OFFICE / EXECUTIVE STUDY", is_ground=False, size=12, weight="800", fill="#0F172A")}
    {text_svg(2.0, 10.85, "12'-6\" x 12'-7\" [NORTH GARDEN VIEW]", is_ground=False, size=10, weight="600", fill="#1D4ED8")}
    {text_svg(2.0, 10.55, "(Direct Interior Door + North Verandah Door)", is_ground=False, size=9, fill="#64748B")}

    {text_svg(5.6, 11.2, "BEDROOM 2 (GUEST / KIDS)", is_ground=False, size=12, weight="800", fill="#0F172A")}
    {text_svg(5.6, 10.85, "11'-6\" x 12'-7\" [NORTH GARDEN VIEW]", is_ground=False, size=10, weight="600", fill="#1D4ED8")}
    {text_svg(5.6, 10.55, "(Direct Living Door + North Verandah Door)", is_ground=False, size=9, fill="#64748B")}

    {text_svg(8.6, 6.4, "MALLANNA TEMPLE ROOM", is_ground=False, size=11, weight="700", fill="#D97706")}
    {text_svg(8.6, 6.05, "8'-4\" x 8'-0\" [WEST DOOR | FACES NORTH]", is_ground=False, size=9, weight="600", fill="#B45309")}
'''
    else:
        svg += f'''
    {text_svg(2.0, 11.2, "BEDROOM 2 (VAYU / NW)", is_ground=False, size=12, weight="800", fill="#0F172A")}
    {text_svg(2.0, 10.85, "12'-6\" x 12'-7\" [NORTH GARDEN VIEW]", is_ground=False, size=10, weight="600", fill="#1D4ED8")}
    {text_svg(2.0, 10.55, "(Direct Interior Door + North Verandah Door)", is_ground=False, size=9, fill="#64748B")}

    {text_svg(5.6, 11.2, "BEDROOM 3 (NORTH)", is_ground=False, size=12, weight="800", fill="#0F172A")}
    {text_svg(5.6, 10.85, "11'-6\" x 12'-7\" [NORTH GARDEN VIEW]", is_ground=False, size=10, weight="600", fill="#1D4ED8")}
    {text_svg(5.6, 10.55, "(Direct Living Door + North Verandah Door)", is_ground=False, size=9, fill="#64748B")}

    {text_svg(9.3, 6.4, "FAMILY LOUNGE / STUDY", is_ground=False, size=11, weight="700", fill="#1D4ED8")}
    {text_svg(9.3, 6.05, "12'-4\" x 12'-8\" [EAST MORNING VIEW]", is_ground=False, size=9, weight="600", fill="#1E40AF")}
'''

    svg += f'''
    {text_svg(7.9, 9.6, "DAILY POOJA", is_ground=False, size=10, weight="700", fill="#D97706")}
    {text_svg(7.9, 9.25, "4'x7'6\" [W-DOOR]", is_ground=False, size=8, weight="600", fill="#B45309")}
  </g>

  <!-- Dimensions -->
  <g id="plinth_dims">
    {line_svg(0, -1.5, PLINTH_W, -1.5, is_ground=False, stroke="#475569", sw=1.5)}
    {text_svg(PLINTH_W / 2.0, -1.85, "37'-0\" [11.28m] OVERALL PLINTH WIDTH", is_ground=False, size=12, weight="600", fill="#1E293B")}
    {line_svg(-1.5, 0, -1.5, PLINTH_D, is_ground=False, stroke="#475569", sw=1.5)}
    {text_svg(-1.85, PLINTH_D / 2.0, "40'-0\" [12.19m] PLINTH DEPTH", is_ground=False, size=12, weight="600", fill="#1E293B", rot=-90)}
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
    export_upper_floor_svg("first_floor_brother_blueprint.svg", "First Floor - Brother's 3BHK Residence", is_owner_level=False)
    export_upper_floor_svg("second_floor_owner_blueprint.svg", "Second Floor - Owner's 2BHK & Office", is_owner_level=True)
    print("All Vector SVGs Exported Successfully.")
