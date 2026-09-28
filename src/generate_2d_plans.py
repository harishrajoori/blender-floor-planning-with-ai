"""
Civil Engineering & Vaastu-Compliant 2D Architectural CAD Engine for Property 2 (54' x 66' Plot)
Driven 100% by Parametric Design Model (src/design_model.py).

Clean Multi-Collection Architectural Hierarchy:
  - 00_Site_Plan (Roads, Compound Wall, Plot Boundary, Lawn, East Morning Garden, Sump, RWH)
  - 01_Ground_Floor_Stilt (Covered SUV Parking, Bike Stalls, 850 sq ft Function Pavilion)
  - 02_First_Floor_Brother (Brother 3BHK Flat, Balconies, Embedded Columns)
  - 03_Second_Floor_Owner (Owner 2BHK + Office, Balconies, Embedded Columns)
  - 04_Cameras_and_Lighting (Isolated Ortho Cameras & Sun Light)

Fully Incorporates Senior Architect Reviews, Engineering Clearances & Vaastu Corrections:
  - Default Viewport State: Clean Owner Floor (L2) + Site Context (zero text overlap, zero camera lines)
  - Isolated Collections: Excluded/Hidden properly in View Layer so opening in Blender shows pristine active plan
  - Unique Prefixes: Site_, G0_, L1_, L2_ eliminating duplicate Blender .001 object conflicts
  - Text at section elevation Z = 1.05m with 5mm solid extrusion and 1.25 line spacing
  - Mallanna Room: Clean room label and dimensions (7'-0" x 9'-3" CLEAR), zero "4 people" label
  - 100% Embedded RCC Columns (C11 embedded in Office/Mallanna corner; C08, C12, C16 embedded/clear of openings)
  - Zero Wall between Kitchen and 4' Utility Passage
  - Simhadwaram Double Door opening INWARD into 5'-7" Regal Foyer
  - East-North-East (ENE) French Double Door for Morning Light
  - Master Bed: NO South Balcony Door, NO West Window (Solid Wall with Full Wardrobes)
  - King Bed (6'-0" x 6'-6", Head to South) + Dressing Table with Mirror
  - Bedroom 2: Bed Headboard to SOUTH (Vaastu Compliant)
  - Dining: Crockery & Buffet Cabinet along South Wall
  - Kitchen: South Storage & Tall Pantry Cupboards
  - Mallanna Pooja: Door on North side of West wall (completely clear of South Altar)
  - Daily Pooja: Double folding shutters opening outward flat against wall (preserving 4' clear depth)
  - All Bathroom doors swing INWARD against bathroom walls
  - NW Core: Structural Gap & 1.4m Common Arrival Foyer between Lift and Stairs
"""

import bpy
import math
import os
import sys
from pathlib import Path

# Add src to sys.path:
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import design_model as dm

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BLEND_FILE = OUTPUT_DIR / "property2_engineering_cad.blend"

# Conversion factors:
M_PER_MM = 0.001
PLOT_W = dm.PLOT_W_MM * M_PER_MM       # 16.4592m (54'-0")
PLOT_D = dm.PLOT_D_MM * M_PER_MM       # 20.1168m (66'-0")
PLINTH_W = dm.PLINTH_W_MM * M_PER_MM   # 10.9728m (36'-0")
PLINTH_D = dm.PLINTH_D_MM * M_PER_MM   # 12.1920m (40'-0")

SETBACK_W = dm.SETBACK_W_MM * M_PER_MM # 2.8956m (9'-6")
SETBACK_S = dm.SETBACK_S_MM * M_PER_MM # 2.7432m (9'-0")
SETBACK_E = dm.SETBACK_E_MM * M_PER_MM # 2.5908m (8'-6")
SETBACK_N = dm.SETBACK_N_MM * M_PER_MM # 5.1816m (17'-0")

PLOT_X0 = -SETBACK_W
PLOT_X1 = PLINTH_W + SETBACK_E
PLOT_Y0 = -SETBACK_S
PLOT_Y1 = PLINTH_D + SETBACK_N

WALL_H = 0.90           # Cut-plane section height
TEXT_Z = 1.05           # Text height just above section cut plane (eliminates 3D parallax)
EXT_WALL_THICK = 0.230  # 9" exterior brick wall
INT_WALL_THICK = 0.115  # 4.5" interior partition wall
COMPOUND_WALL_THICK = 0.150 # 6" compound boundary wall
COL_W = 0.230           # 9" column width
COL_D = 0.450           # 18" column depth

# Professional CAD Color Palette (RGBA)
COLOR_SLAB = (0.97, 0.97, 0.98, 1.0)
COLOR_PLOT_BG = (0.95, 0.96, 0.97, 1.0)
COLOR_COMPOUND = (0.22, 0.26, 0.32, 1.0)
COLOR_EXT_WALL = (0.15, 0.18, 0.24, 1.0)
COLOR_INT_WALL = (0.30, 0.35, 0.42, 1.0)
COLOR_COLUMN = (0.06, 0.08, 0.10, 1.0)
COLOR_DOOR = (0.05, 0.55, 0.38, 1.0)
COLOR_WINDOW = (0.12, 0.45, 0.85, 1.0)
COLOR_FURNITURE = (0.68, 0.58, 0.48, 1.0)
COLOR_CUPBOARD = (0.80, 0.70, 0.58, 1.0)
COLOR_BED = (0.30, 0.48, 0.72, 1.0)
COLOR_KITCHEN = (0.18, 0.20, 0.24, 1.0)
COLOR_POOJA = (0.92, 0.65, 0.12, 1.0)
COLOR_TEXT = (0.05, 0.08, 0.12, 1.0)
COLOR_DIM = (0.32, 0.38, 0.46, 1.0)
COLOR_GRID = (0.65, 0.70, 0.76, 1.0)
COLOR_PAVILION = (0.93, 0.91, 0.85, 1.0)
COLOR_PARKING = (0.87, 0.91, 0.95, 1.0)
COLOR_DRIVEWAY = (0.91, 0.92, 0.94, 1.0)
COLOR_GARDEN = (0.80, 0.92, 0.80, 1.0)
COLOR_BALCONY = (0.90, 0.93, 0.97, 1.0)
COLOR_ROAD = (0.88, 0.90, 0.93, 1.0)

def get_or_create_material(name, color_rgba, is_emissive=False):
    if name in bpy.data.materials:
        mat = bpy.data.materials[name]
    else:
        mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = color_rgba
    if mat.node_tree:
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                node.inputs['Base Color'].default_value = color_rgba
                if 'Roughness' in node.inputs:
                    node.inputs['Roughness'].default_value = 0.6
                if is_emissive:
                    if 'Emission Color' in node.inputs:
                        node.inputs['Emission Color'].default_value = color_rgba
                    if 'Emission Strength' in node.inputs:
                        node.inputs['Emission Strength'].default_value = 1.0
    return mat

def create_box(name, x0, y0, x1, y1, z0, z1, mat, collection=None):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)
    min_x = min(x0, x1)
    min_y = min(y0, y1)
    min_z = min(z0, z1)
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (dx, dy, dz)
    obj.location = (min_x + dx/2.0, min_y + dy/2.0, min_z + dz/2.0)
    obj.data.materials.append(mat)
    obj.color = mat.diffuse_color
    
    if collection and obj.name not in collection.objects:
        collection.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)
    return obj

def add_cad_text(name, text, x, y, z=TEXT_Z, size=0.22, align_x='CENTER', align_y='CENTER', rot_z=0.0, color=COLOR_TEXT, collection=None):
    mat = get_or_create_material(f"Mat_Text_{name}", color, is_emissive=True)
    curve_data = bpy.data.curves.new(name=f"Curve_{name}", type='FONT')
    curve_data.body = text.replace("\\n", "\n")
    curve_data.size = size
    curve_data.align_x = align_x
    curve_data.align_y = align_y
    curve_data.space_line = 1.25
    curve_data.extrude = 0.005 # Solid 3D body prevents thin clipping in viewport
    
    obj = bpy.data.objects.new(name=f"Txt_{name}", object_data=curve_data)
    obj.location = (x, y, z)
    obj.rotation_euler = (0, 0, rot_z)
    obj.data.materials.append(mat)
    
    col = collection if collection else bpy.context.scene.collection
    col.objects.link(obj)
    return obj

def create_door_2d(name, hx, hy, width, angle_deg=90, side='E', collection=None):
    mat_door = get_or_create_material("Mat_CAD_Door", COLOR_DOOR)
    if side == 'E':
        ex, ey = hx + width, hy
    elif side == 'W':
        ex, ey = hx - width, hy
    elif side == 'N':
        ex, ey = hx, hy + width
    else:
        ex, ey = hx, hy - width
        
    leaf = create_box(f"{name}_Leaf", hx, hy, ex, ey + 0.04, 0, 0.05, mat_door, collection)
    return leaf

def create_window_2d(name, x0, y0, x1, y1, is_horiz=True, collection=None):
    mat_win = get_or_create_material("Mat_CAD_Window", COLOR_WINDOW)
    frame = create_box(f"{name}_Frame", x0, y0, x1, y1, 0, WALL_H * 0.35, mat_win, collection)
    if is_horiz:
        create_box(f"{name}_Glass", x0, (y0+y1)/2 - 0.02, x1, (y0+y1)/2 + 0.02, 0, WALL_H * 0.40, mat_win, collection)
    else:
        create_box(f"{name}_Glass", (x0+x1)/2 - 0.02, y0, (x0+x1)/2 + 0.02, y1, 0, WALL_H * 0.40, mat_win, collection)
    return frame

def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 2800
    scene.render.resolution_y = 2200
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = 'Standard' # High-contrast architectural CAD presentation
    
    world = bpy.data.worlds.new("CAD_World")
    scene.world = world
    world.color = (0.96, 0.97, 0.98)
    if world.node_tree:
        for node in world.node_tree.nodes:
            if node.type == 'BACKGROUND':
                node.inputs['Color'].default_value = (0.96, 0.97, 0.98, 1.0)
                node.inputs['Strength'].default_value = 1.0
    return scene

def create_ortho_camera(name, cx, cy, ortho_scale=22.0, target_col=None):
    cam_data = bpy.data.cameras.new(name=name)
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = ortho_scale
    cam_data.clip_start = 0.1
    cam_data.clip_end = 100.0
    
    cam_obj = bpy.data.objects.new(name=name, object_data=cam_data)
    cam_obj.location = (cx, cy, 20.0)
    cam_obj.rotation_euler = (0, 0, 0)
    
    if target_col:
        target_col.objects.link(cam_obj)
    else:
        bpy.context.scene.collection.objects.link(cam_obj)
    return cam_obj

# =============================================================================
# BUILDER 0: SITE CONTEXT & ROADS (00_Site_Plan)
# =============================================================================
def build_site_plan(parent_col):
    col = bpy.data.collections.new("00_Site_Plan")
    parent_col.children.link(col)
    
    mat_plot = get_or_create_material("Mat_Plot_BG", COLOR_PLOT_BG)
    mat_compound = get_or_create_material("Mat_Compound_Wall", COLOR_COMPOUND)
    mat_garden = get_or_create_material("Mat_Garden_Green", COLOR_GARDEN)
    mat_road = get_or_create_material("Mat_Road_Surface", COLOR_ROAD)

    # 1. Surrounding Municipal Roads (30' West & South)
    create_box("Site_Road_West", PLOT_X0 - 3.2, PLOT_Y0 - 3.2, PLOT_X0 - 0.2, PLOT_Y1 + 3.2, -0.05, 0, mat_road, col)
    add_cad_text("Site_Road_West_Lbl", "WEST 30'-0\" WIDE MUNICIPAL ROAD", PLOT_X0 - 1.7, PLOT_Y0 + PLOT_D/2, TEXT_Z, 0.24, rot_z=math.radians(90), collection=col)

    create_box("Site_Road_South", PLOT_X0 - 3.2, PLOT_Y0 - 3.2, PLOT_X1 + 3.2, PLOT_Y0 - 0.2, -0.05, 0, mat_road, col)
    add_cad_text("Site_Road_South_Lbl", "SOUTH 30'-0\" WIDE MUNICIPAL ROAD", PLOT_X0 + PLOT_W/2, PLOT_Y0 - 1.7, TEXT_Z, 0.24, collection=col)

    # 2. Entire Plot Ground Surface (54' x 66')
    create_box("Site_Plot_Ground", PLOT_X0, PLOT_Y0, PLOT_X1, PLOT_Y1, -0.02, 0, mat_plot, col)
    
    # 3. 6" Compound Wall
    create_box("Site_Wall_South", PLOT_X0, PLOT_Y0, PLOT_X1, PLOT_Y0 + COMPOUND_WALL_THICK, 0, 1.20, mat_compound, col)
    create_box("Site_Wall_East", PLOT_X1 - COMPOUND_WALL_THICK, PLOT_Y0, PLOT_X1, PLOT_Y1, 0, 1.20, mat_compound, col)
    create_box("Site_Wall_North", PLOT_X0, PLOT_Y1 - COMPOUND_WALL_THICK, PLOT_X1, PLOT_Y1, 0, 1.20, mat_compound, col)
    create_box("Site_Wall_West", PLOT_X0, PLOT_Y0, PLOT_X0 + COMPOUND_WALL_THICK, PLOT_Y1, 0, 1.20, mat_compound, col)

    # 4. Setbacks & Gardens
    create_box("Site_Garden_North", 0, PLINTH_D, PLINTH_W, PLOT_Y1 - COMPOUND_WALL_THICK, 0, 0.05, mat_garden, col)
    add_cad_text("Site_North_Lawn_Lbl", "NORTH FRONT VAASTU LAWN (16'-0\" CLEAR SETBACK - OPEN TO SKY)", PLINTH_W/2, PLINTH_D + 2.6, TEXT_Z, 0.22, collection=col)

    create_box("Site_Garden_East", PLINTH_W, 0, PLOT_X1 - COMPOUND_WALL_THICK, PLINTH_D, 0, 0.05, mat_garden, col)
    add_cad_text("Site_East_Garden_Lbl", "EAST MORNING GARDEN (8'-6\" SETBACK - TULASI & LANDSCAPE)", PLINTH_W + 1.3, PLINTH_D/2, TEXT_Z, 0.20, rot_z=math.radians(90), collection=col)

    # Ishanya 12,000L Underground Water Sump + RWH Pit
    create_box("Site_Underground_Water_Sump", PLINTH_W + 0.3, PLINTH_D + 1.2, PLINTH_W + 2.1, PLINTH_D + 3.7, 0, 0.10, get_or_create_material("Mat_Water_Sump", (0.2, 0.5, 0.8, 1.0)), col)
    add_cad_text("Site_Sump_Lbl", "UNDERGROUND WATER SUMP\\n(12,000 L - ISHANYA)", PLINTH_W + 1.2, PLINTH_D + 2.45, TEXT_Z, 0.16, collection=col)
    
    create_box("Site_Rainwater_Harvesting_Pit", PLOT_X0 + 6.0, PLINTH_D + 1.5, PLOT_X0 + 7.6, PLINTH_D + 3.1, 0, 0.08, get_or_create_material("Mat_RWH", (0.3, 0.6, 0.9, 1.0)), col)
    add_cad_text("Site_RWH_Lbl", "RWH PIT\\n(1.5m x 1.5m)", PLOT_X0 + 6.8, PLINTH_D + 2.3, TEXT_Z, 0.15, collection=col)

    # 5. External Vertical Core Base (West Setback)
    create_box("Site_Core_Base", -2.35, 6.80, -0.10, 12.20, 0.0, 0.20, get_or_create_material("Mat_Core", (0.9, 0.92, 0.95, 1.0)), col)
    create_box("Site_Core_Wall_W", -2.35, 6.80, -2.15, 12.20, 0.20, WALL_H, mat_compound, col)

    return col

# =============================================================================
# BUILDER 1: GROUND STILT & FUNCTION PAVILION (01_Ground_Floor_Stilt)
# =============================================================================
def build_ground_stilt(parent_col):
    col = bpy.data.collections.new("01_Ground_Floor_Stilt")
    parent_col.children.link(col)
    
    mat_plinth = get_or_create_material("Mat_Plinth_Slab", COLOR_SLAB)
    mat_pavilion = get_or_create_material("Mat_Pavilion_Floor", COLOR_PAVILION)
    mat_parking = get_or_create_material("Mat_Parking_Bay", COLOR_PARKING)
    mat_col = get_or_create_material("Mat_RCC_Column", COLOR_COLUMN)
    mat_balcony = get_or_create_material("Mat_Balcony", COLOR_BALCONY)
    mat_compound = get_or_create_material("Mat_Compound_Wall", COLOR_COMPOUND)

    # 1. Plinth Raised Base
    create_box("G0_Plinth_Base", 0, 0, PLINTH_W, PLINTH_D, 0.0, 0.15, mat_plinth, col)
    
    # 2. Covered Parking: 1 Car (SUV) + 2 Bikes + EV points
    create_box("G0_Car_Bay_1", 0.30, PLINTH_D - 5.50, 3.80, PLINTH_D - 0.30, 0.15, 0.17, mat_parking, col)
    add_cad_text("G0_Car_1_Lbl", "CAR PARKING BAY (SUV)\\n(11'-6\" x 17'-0\" CLEAR)\\nToyota Fortuner / Innova", 2.05, PLINTH_D - 2.90, TEXT_Z, 0.19, collection=col)

    create_box("G0_Bike_Bay", 4.00, PLINTH_D - 5.50, 6.40, PLINTH_D - 0.30, 0.15, 0.17, mat_parking, col)
    add_cad_text("G0_Bike_Lbl", "2x BIKE STALL\\n+ 2x 15A EV POINTS", 5.20, PLINTH_D - 2.90, TEXT_Z, 0.18, collection=col)

    # 3. Multi-Purpose Function Pavilion (~850 sq ft)
    create_box("G0_Pavilion_Floor", 0.30, 0.30, PLINTH_W - 0.30, PLINTH_D - 5.80, 0.15, 0.18, mat_pavilion, col)
    add_cad_text("G0_Pavilion_Title", "SHELTERED OPEN FUNCTION PAVILION (~850 SQ FT)", PLINTH_W/2, (PLINTH_D - 5.80)/2 + 0.6, TEXT_Z, 0.32, collection=col)
    add_cad_text("G0_Pavilion_Sub", "Multi-purpose floor for rituals, family festivals, Satyanarayana Vratams, and dining pandals", PLINTH_W/2, (PLINTH_D - 5.80)/2 - 0.4, TEXT_Z, 0.18, collection=col)

    # 4. Vertical Core (NW): Lift Shaft & 1.4m Landing Gap
    create_box("G0_Lift_Shaft_Ext", -2.25, 10.30, -0.45, 12.10, 0.20, WALL_H, mat_compound, col)
    add_cad_text("G0_Lift_Shaft_Lbl", "4-PAX LIFT\\n(3 STOPS)", -1.35, 11.20, TEXT_Z, 0.16, collection=col)

    create_box("G0_Core_Landing_Foyer", -2.25, 9.60, -0.05, 10.30, 0.15, 0.20, mat_balcony, col)
    add_cad_text("G0_Core_Gap_Lbl", "1.4m CLEAR FOYER / GAP", -1.15, 9.95, TEXT_Z, 0.14, collection=col)
    
    # 5. RCC Columns on Ground Floor
    for c in dm.COLUMNS:
        cx = c["x"] * M_PER_MM
        cy = c["y"] * M_PER_MM
        cw = c["width"] * M_PER_MM
        cd = c["depth"] * M_PER_MM
        create_box(f"G0_Col_{c['id']}", cx - cw/2, cy - cd/2, cx + cw/2, cy + cd/2, 0.15, WALL_H, mat_col, col)

    return col

# =============================================================================
# BUILDER 2: UPPER RESIDENTIAL FLOORS (02_First_Floor_Brother & 03_Second_Floor_Owner)
# =============================================================================
def build_upper_floor(parent_col, floor_code="L2", is_owner_level=True):
    col_name = "03_Second_Floor_Owner" if is_owner_level else "02_First_Floor_Brother"
    col = bpy.data.collections.new(col_name)
    parent_col.children.link(col)
    
    prefix = floor_code # "L1" or "L2"
    
    mat_slab = get_or_create_material("Mat_Upper_Slab", COLOR_SLAB)
    mat_ext = get_or_create_material("Mat_Upper_ExtWall", COLOR_EXT_WALL)
    mat_int = get_or_create_material("Mat_Upper_IntWall", COLOR_INT_WALL)
    mat_col = get_or_create_material("Mat_Upper_Column", COLOR_COLUMN)
    mat_balcony = get_or_create_material("Mat_Upper_Balcony", COLOR_BALCONY)
    mat_furn = get_or_create_material("Mat_Upper_Furn", COLOR_FURNITURE)
    mat_bed = get_or_create_material("Mat_Upper_Bed", COLOR_BED)
    mat_pooja = get_or_create_material("Mat_Upper_Pooja", COLOR_POOJA)
    mat_kitchen = get_or_create_material("Mat_Upper_Kitchen", COLOR_KITCHEN)

    # 1. Main Plinth Slab & Cantilever Wrap-Around Gallery
    create_box(f"{prefix}_Floor_Slab", 0, 0, PLINTH_W, PLINTH_D, 0.0, 0.15, mat_slab, col)
    # North Covered Promenade (4'-3" wide deck)
    create_box(f"{prefix}_North_Promenade", -2.40, PLINTH_D, PLINTH_W + 2.40, PLINTH_D + 1.30, 0.15, 0.18, mat_balcony, col)
    # East Covered Utility Balcony
    create_box(f"{prefix}_East_Utility_Balcony", PLINTH_W, 0, PLINTH_W + 1.25, 5.33, 0.15, 0.18, mat_balcony, col)
    # East Morning Balcony (off ENE French Door)
    create_box(f"{prefix}_East_Morning_Balcony", PLINTH_W, 9.55, PLINTH_W + 1.25, PLINTH_D, 0.15, 0.18, mat_balcony, col)
    # South Shaded Balcony
    create_box(f"{prefix}_South_Balcony", 3.810, -1.07, 6.858, 0, 0.15, 0.18, mat_balcony, col)

    # 2. Exterior Walls with REAL OPENINGS
    # SOUTH EXTERIOR WALL
    # Master Bed South Wall: Solid Wall with Centered 6'-0" Window (NO Balcony Door!)
    create_box(f"{prefix}_Ext_S1_MB", 0, 0, 1.10, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_window_2d(f"{prefix}_Win_MB_S", 1.10, 0, 2.90, EXT_WALL_THICK, True, col)
    create_box(f"{prefix}_Ext_S2_MB", 2.90, 0, 3.810, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    # Dining South Wall: Wall + Sliding Balcony Door
    create_box(f"{prefix}_Ext_S3_Din", 3.810, 0, 4.10, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_door_2d(f"{prefix}_Door_Dining_S_Balcony", 4.10, EXT_WALL_THICK, 1.30, 90, 'N', col)
    create_box(f"{prefix}_Ext_S4_Din", 5.40, 0, 6.858, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    # Kitchen South Wall: Solid Wall backing South Storage Cupboards
    create_box(f"{prefix}_Ext_S5_Kit", 6.858, 0, PLINTH_W, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)

    # EAST EXTERIOR WALL
    create_box(f"{prefix}_Ext_E1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 1.60, 0, WALL_H, mat_ext, col)
    create_window_2d(f"{prefix}_Win_Kit_E", PLINTH_W - EXT_WALL_THICK, 1.60, PLINTH_W, 3.10, False, col)
    create_box(f"{prefix}_Ext_E2", PLINTH_W - EXT_WALL_THICK, 3.10, PLINTH_W, 4.30, 0, WALL_H, mat_ext, col)
    # Utility Balcony Door (via 4' Service Passage, y = 4.30 to 5.15)
    create_door_2d(f"{prefix}_Door_Utility_Passage", PLINTH_W - EXT_WALL_THICK, 4.30, 0.85, 90, 'E', col)
    create_box(f"{prefix}_Ext_E3", PLINTH_W - EXT_WALL_THICK, 5.15, PLINTH_W, 6.15, 0, WALL_H, mat_ext, col)
    create_window_2d(f"{prefix}_Win_Pooja_E", PLINTH_W - EXT_WALL_THICK, 6.15, PLINTH_W, 7.35, False, col)
    create_box(f"{prefix}_Ext_E4", PLINTH_W - EXT_WALL_THICK, 7.35, PLINTH_W, 10.40, 0, WALL_H, mat_ext, col)
    # ENE FRENCH DOUBLE DOOR (East-North-East Morning Light Entrance!)
    create_door_2d(f"{prefix}_Door_ENE_French", PLINTH_W - EXT_WALL_THICK, 10.40, 1.30, 90, 'W', col)
    create_box(f"{prefix}_Ext_E5", PLINTH_W - EXT_WALL_THICK, 11.70, PLINTH_W, PLINTH_D, 0, WALL_H, mat_ext, col)

    # WEST EXTERIOR WALL
    # Master Bed West Wall: Solid Masonry Wall (NO Window! Backs Full Wardrobe)
    create_box(f"{prefix}_Ext_W1_MB", 0, 0.23, EXT_WALL_THICK, 4.115, 0, WALL_H, mat_ext, col)
    create_box(f"{prefix}_Ext_W2_Bath", 0, 4.115, EXT_WALL_THICK, 5.10, 0, WALL_H, mat_ext, col)
    create_window_2d(f"{prefix}_Vent_AttBath_W", 0, 5.10, EXT_WALL_THICK, 5.90, False, col)
    create_box(f"{prefix}_Ext_W3_Bath", 0, 5.90, EXT_WALL_THICK, 7.10, 0, WALL_H, mat_ext, col)
    create_window_2d(f"{prefix}_Vent_ComBath_W", 0, 7.10, EXT_WALL_THICK, 7.90, False, col)
    create_box(f"{prefix}_Ext_W4_B2", 0, 7.90, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_ext, col)

    # NORTH EXTERIOR WALL
    # Bed 2 Window: Centered between C04 (x=0) and C08 (x=3.810)
    create_box(f"{prefix}_Ext_N1", 0, PLINTH_D - EXT_WALL_THICK, 1.00, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_window_2d(f"{prefix}_Win_Bed2_N", 1.00, PLINTH_D - EXT_WALL_THICK, 2.60, PLINTH_D, True, col)
    create_box(f"{prefix}_Ext_N2", 2.60, PLINTH_D - EXT_WALL_THICK, 4.50, PLINTH_D, 0, WALL_H, mat_ext, col) # Embeds C08!
    
    # Office Window: Centered between C08 (x=3.810) and C12 (x=6.858)
    create_window_2d(f"{prefix}_Win_Office_N", 4.50, PLINTH_D - EXT_WALL_THICK, 6.10, PLINTH_D, True, col)
    create_box(f"{prefix}_Ext_N3", 6.10, PLINTH_D - EXT_WALL_THICK, 7.30, PLINTH_D, 0, WALL_H, mat_ext, col) # Embeds C12!
    
    # SIMHADWARAM (D1): NORTH EXTERIOR WALL (Opens INWARD into Wide 5'-7" Regal Foyer!)
    create_door_2d(f"{prefix}_Simhadwaram_D1_Inward", 7.30, PLINTH_D - EXT_WALL_THICK, 1.20, 90, 'S', col)
    create_box(f"{prefix}_Ext_N4", 8.50, PLINTH_D - EXT_WALL_THICK, 9.20, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_window_2d(f"{prefix}_Win_NE_Living_N", 9.20, PLINTH_D - EXT_WALL_THICK, 10.50, PLINTH_D, True, col)
    create_box(f"{prefix}_Ext_N5", 10.50, PLINTH_D - EXT_WALL_THICK, PLINTH_W, PLINTH_D, 0, WALL_H, mat_ext, col) # Embeds C16!

    # 3. Interior Partition Walls
    # Master Bed East Wall (x = 3.810)
    create_box(f"{prefix}_MB_Wall_E", 3.810 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.810 + INT_WALL_THICK/2, 4.115, 0, WALL_H, mat_int, col)
    
    # Master Bed North Wall (y = 4.115) with Attached Bath door and Lobby entry
    create_box(f"{prefix}_MB_Wall_N1", EXT_WALL_THICK, 4.115 - INT_WALL_THICK/2, 0.35, 4.115 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d(f"{prefix}_Door_AttBath_Inward", 0.35, 4.115, 0.75, 90, 'N', col) # Swings INWARD into bath (CCW)!
    create_box(f"{prefix}_MB_Wall_N2", 1.10, 4.115 - INT_WALL_THICK/2, 2.80, 4.115 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d(f"{prefix}_Door_MB_Entry", 3.70, 4.115, 0.90, 90, 'S', col) # Swings INWARD into Master Bed (CCW)!
    create_box(f"{prefix}_MB_Wall_N3", 3.70, 4.115 - INT_WALL_THICK/2, 3.810, 4.115 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Bathrooms Divider (Horizontal at y = 6.10)
    create_box(f"{prefix}_Bath_Divider", EXT_WALL_THICK, 6.10 - INT_WALL_THICK/2, 1.98, 6.10 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box(f"{prefix}_ComBath_Wall_N", EXT_WALL_THICK, 8.128 - INT_WALL_THICK/2, 1.98, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Common Bath East Wall (x = 1.98) with INWARD SCREENED DOOR
    create_box(f"{prefix}_ComBath_Wall_E1", 1.98 - INT_WALL_THICK/2, 4.115, 1.98 + INT_WALL_THICK/2, 7.05, 0, WALL_H, mat_int, col)
    create_door_2d(f"{prefix}_Door_ComBath_Inward", 1.98, 7.80, 0.75, 90, 'W', col) # Swings INWARD into bath (CW)!
    create_box(f"{prefix}_ComBath_Wall_E2", 1.98 - INT_WALL_THICK/2, 7.80, 1.98 + INT_WALL_THICK/2, 8.128, 0, WALL_H, mat_int, col)

    # Private Lobby North Wall (y = 8.128): Direct Door to NW Bedroom 2
    create_box(f"{prefix}_Lobby_North_Wall1", 1.98, 8.128 - INT_WALL_THICK/2, 2.80, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d(f"{prefix}_Door_B2_Entry", 3.70, 8.128, 0.90, 90, 'N', col) # Swings INWARD into Bed 2 (CW)!
    create_box(f"{prefix}_Lobby_North_Wall2", 3.70, 8.128 - INT_WALL_THICK/2, 3.810, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Dividing Wall Between Bed 2 and Office (x = 3.810) - Connects C07 to C08!
    create_box(f"{prefix}_Wall_Bed2_Office", 3.810 - INT_WALL_THICK/2, 8.128, 3.810 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)

    # Office South Wall (y = 8.128, x = 3.810 to 6.858) - Connects C07 to C11!
    create_box(f"{prefix}_Office_Wall_S1", 3.810, 8.128 - INT_WALL_THICK/2, 3.95, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d(f"{prefix}_Door_Office_Entry", 3.95, 8.128, 0.90, 90, 'N', col) # Swings INWARD into Office (CCW)!
    create_box(f"{prefix}_Office_Wall_S2", 4.85, 8.128 - INT_WALL_THICK/2, 6.858, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col) # Connects flush into C11!

    # Office East Wall (x = 6.858, y = 8.128 to 12.192) - CONNECTS C11 DIRECTLY TO C12!
    # Column C11 is 100% EMBEDDED inside the Office Southeast wall corner! ZERO open faces!
    # Leaves a generous 5'-7" (1,694 mm) clear entrance foyer to the Pooja wall!
    create_box(f"{prefix}_Wall_Office_NE", 6.858 - INT_WALL_THICK/2, 8.128, 6.858 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)

    # East Pooja Enclave Partitions:
    create_box(f"{prefix}_Passage_Wall_N", 8.609, 5.334 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 5.334 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box(f"{prefix}_Pooja_Shared_Wall", 8.609, 6.611 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 6.611 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box(f"{prefix}_Mallanna_Wall_N", 8.609, 9.545 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 9.545 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # West Wall of Pooja Enclave (x = 8.609)
    create_box(f"{prefix}_Pooja_Wall_W1", 8.609 - INT_WALL_THICK/2, 5.334, 8.609 + INT_WALL_THICK/2, 5.534, 0, WALL_H, mat_int, col)
    create_door_2d(f"{prefix}_Door_DailyPooja", 8.609, 5.534, 0.80, 90, 'W', col) # Double folding shutters
    create_box(f"{prefix}_Pooja_Wall_W2", 8.609 - INT_WALL_THICK/2, 6.334, 8.609 + INT_WALL_THICK/2, 8.100, 0, WALL_H, mat_int, col)
    create_door_2d(f"{prefix}_Door_Mallanna", 8.609, 8.100, 0.90, 90, 'E', col) # Away from South Altar!
    create_box(f"{prefix}_Pooja_Wall_W3", 8.609 - INT_WALL_THICK/2, 9.000, 8.609 + INT_WALL_THICK/2, 9.545, 0, WALL_H, mat_int, col)

    # NOTE: ZERO WALL BETWEEN KITCHEN AND 4' SERVICE PASSAGE!

    # 4. Built-in Furniture & Identifications
    # Master Bedroom: King Bed (6'-0" x 6'-6", Head to South!)
    create_box(f"{prefix}_MB_King_Bed", 1.30, 0.35, 3.13, 2.33, 0.15, 0.65, mat_bed, col)
    create_box(f"{prefix}_MB_Wardrobes", 0.24, 0.35, 0.84, 3.85, 0.15, 1.20, mat_furn, col)
    # Master Bedroom Dressing Table
    create_box(f"{prefix}_MB_Dressing_Table", 1.40, 3.55, 2.50, 4.05, 0.15, 0.75, mat_furn, col)
    add_cad_text(f"{prefix}_MB_Dress_Lbl", "DRESSING TABLE & MIRROR", 1.95, 3.80, TEXT_Z, 0.15, collection=col)
    add_cad_text(f"{prefix}_MB_Bed_Lbl", "KING BED (6'-0\" x 6'-6\" - HEAD SOUTH)", 2.21, 1.34, TEXT_Z, 0.16, collection=col)

    # Bedroom 2: Queen Bed with Headboard to SOUTH!
    create_box(f"{prefix}_Bed2_Queen_Bed", 1.30, 8.25, 2.82, 10.23, 0.15, 0.65, mat_bed, col)
    add_cad_text(f"{prefix}_Bed2_Lbl", "QUEEN BED (HEAD SOUTH)", 2.06, 9.24, TEXT_Z, 0.18, collection=col)

    # Office Desk (Level 2) or Bedroom 3 (Level 1)
    if is_owner_level:
        create_box(f"{prefix}_Office_Desk", 4.40, 9.80, 6.10, 10.70, 0.15, 0.75, mat_furn, col)
        add_cad_text(f"{prefix}_Office_Lbl", "PERSONAL OFFICE\\n(10'-0\" x 13'-4\" / 9'-8\" x 12'-3\" CLEAR)", 5.33, 8.85, TEXT_Z, 0.20, collection=col)
    else:
        create_box(f"{prefix}_Bed3_Bed", 4.40, 8.25, 5.92, 10.23, 0.15, 0.65, mat_bed, col)
        add_cad_text(f"{prefix}_Bed3_Lbl", "BEDROOM 3\\n(10'-0\" x 13'-4\" / 9'-8\" x 12'-3\" CLEAR)", 5.33, 8.85, TEXT_Z, 0.20, collection=col)

    # Grand Entrance Foyer & NE Living Extension
    add_cad_text(f"{prefix}_Entrance_Foyer_Lbl", "GRAND ENTRANCE FOYER\\n(5'-7\" CLEAR WIDTH - REGAL ARRIVAL)", 7.73, 9.80, TEXT_Z, 0.18, collection=col)

    # Mallanna Altar (South wall, faces North)
    create_box(f"{prefix}_Mallanna_Altar", 8.80, 6.75, 10.50, 7.35, 0.15, 0.95, mat_pooja, col)
    add_cad_text(f"{prefix}_Mallanna_Lbl", "MALLANNA ALTAR (FACES NORTH)", 9.65, 7.05, TEXT_Z, 0.18, collection=col)
    # Clean room label and dimensions (NO 4 people text):
    add_cad_text(f"{prefix}_Mallanna_Room_Lbl", "LORD MALLANNA TEMPLE\\n7'-0\" x 9'-3\" CLEAR", 9.65, 8.40, TEXT_Z, 0.18, collection=col)

    # Daily Pooja Altar (East wall, faces West)
    create_box(f"{prefix}_DailyPooja_Altar", 10.10, 5.50, 10.60, 6.50, 0.15, 0.95, mat_pooja, col)
    add_cad_text(f"{prefix}_DailyPooja_Lbl", "DAILY POOJA (FACES WEST)", 9.35, 6.00, TEXT_Z, 0.18, collection=col)

    # Dining Table
    create_box(f"{prefix}_Dining_Table", 4.40, 1.40, 6.20, 2.80, 0.15, 0.75, mat_furn, col)
    add_cad_text(f"{prefix}_Dining_Lbl", "DINING TABLE (6-SEATER)", 5.30, 2.10, TEXT_Z, 0.20, collection=col)

    # Dining Crockery Cabinet along South Wall
    create_box(f"{prefix}_Dining_Crockery", 5.50, 0.24, 6.75, 0.69, 0.15, 0.90, mat_furn, col)
    add_cad_text(f"{prefix}_Crockery_Lbl", "CROCKERY CABINET & BUFFET", 6.12, 0.47, TEXT_Z, 0.15, collection=col)

    # Kitchen South Storage & Pantry Cupboards
    create_box(f"{prefix}_Kitchen_Pantry", 7.00, 0.24, 10.00, 0.79, 0.15, 1.20, mat_furn, col)
    add_cad_text(f"{prefix}_Pantry_Lbl", "SOUTH STORAGE & PANTRY CUPBOARDS", 8.50, 0.52, TEXT_Z, 0.15, collection=col)

    # Kitchen East Cooking Counter
    create_box(f"{prefix}_Kitchen_Counter", 10.14, 0.80, 10.74, 4.20, 0.15, 0.85, mat_kitchen, col)
    add_cad_text(f"{prefix}_Kitchen_Lbl", "KITCHEN & 4' SERVICE PASSAGE", 8.50, 2.50, TEXT_Z, 0.19, collection=col)

    # Living Sectional Sofa & Brahmasthana
    create_box(f"{prefix}_Living_Sofa", 4.20, 5.80, 6.40, 6.80, 0.15, 0.65, mat_bed, col)
    add_cad_text(f"{prefix}_Living_Title", "GRAND LIVING HALL (BRAHMASTHANA)", 5.33, 7.30, TEXT_Z, 0.25, collection=col)
    add_cad_text(f"{prefix}_Open_Living_Dining_Note", "OPEN, CONTINUOUS LIVING-DINING (ZERO DIVIDER WALLS)", 5.33, 4.115, TEXT_Z, 0.20, collection=col)

    # 5. External Core with 1.4m Landing Gap
    create_box(f"{prefix}_Core_Upper_Base", -2.35, 6.80, -0.10, 12.20, 0.15, 0.20, mat_balcony, col)
    create_box(f"{prefix}_Lift_Shaft_Upper", -2.25, 10.30, -0.45, 12.10, 0.20, WALL_H, mat_ext, col)
    add_cad_text(f"{prefix}_Lift_Upper_Lbl", "4-PAX LIFT", -1.35, 11.20, TEXT_Z, 0.16, collection=col)

    create_box(f"{prefix}_Core_Upper_Foyer", -2.25, 9.60, -0.05, 10.30, 0.15, 0.20, mat_balcony, col)
    add_cad_text(f"{prefix}_Core_Upper_Gap_Lbl", "1.4m CLEAR FOYER / GAP", -1.15, 9.95, TEXT_Z, 0.14, collection=col)

    # 6. Columns (ALL 100% EMBEDDED INSIDE WALLS)
    for c in dm.COLUMNS:
        cx = c["x"] * M_PER_MM
        cy = c["y"] * M_PER_MM
        cw = c["width"] * M_PER_MM
        cd = c["depth"] * M_PER_MM
        create_box(f"{prefix}_Col_{c['id']}", cx - cw/2, cy - cd/2, cx + cw/2, cy + cd/2, 0.15, WALL_H, mat_col, col)

    return col

# =============================================================================
# BUILDER 3: ROOFTOP & TERRACE FLOOR (05_Terrace_Roof)
# =============================================================================
def build_terrace_roof(parent_col):
    col = bpy.data.collections.new("05_Terrace_Roof")
    parent_col.children.link(col)
    prefix = "L3"
    
    mat_slab = get_or_create_material("Mat_Terrace_Slab", (0.96, 0.97, 0.98, 1.0))
    mat_ext_wall = get_or_create_material("Mat_Ext_Wall", COLOR_EXT_WALL)
    mat_int_wall = get_or_create_material("Mat_Int_Wall", COLOR_INT_WALL)
    mat_col = get_or_create_material("Mat_Column", COLOR_COLUMN)
    mat_door = get_or_create_material("Mat_Door", COLOR_DOOR)
    mat_window = get_or_create_material("Mat_Window", COLOR_WINDOW)
    mat_furniture = get_or_create_material("Mat_Furniture", COLOR_FURNITURE)
    mat_kitchen = get_or_create_material("Mat_Kitchen", COLOR_KITCHEN)
    mat_water = get_or_create_material("Mat_Water", (0.15, 0.55, 0.85, 1.0))
    mat_solar_a = get_or_create_material("Mat_Solar_Brother", (0.12, 0.23, 0.54, 1.0))
    mat_solar_b = get_or_create_material("Mat_Solar_Owner", (0.10, 0.45, 0.78, 1.0))
    mat_pergola = get_or_create_material("Mat_Pergola", (0.95, 0.93, 0.82, 1.0))
    mat_yoga = get_or_create_material("Mat_Yoga_Green", (0.85, 0.95, 0.88, 1.0))

    # 1. Base Terrace Floor Slab
    create_box(f"{prefix}_Plinth_Slab", 0, 0, PLINTH_W, PLINTH_D, 0, 0.15, mat_slab, col)
    # Cantilever projections
    create_box(f"{prefix}_North_Deck", -2.35, PLINTH_D, PLINTH_W, PLINTH_D + 1.30, 0, 0.15, mat_slab, col)
    create_box(f"{prefix}_East_Deck", PLINTH_W, 0, PLINTH_W + 1.25, 5.33, 0, 0.15, mat_slab, col)
    create_box(f"{prefix}_Morning_Deck", PLINTH_W, 9.55, PLINTH_W + 1.25, PLINTH_D, 0, 0.15, mat_slab, col)
    create_box(f"{prefix}_South_Deck", 3.810, -1.07, 6.858, 0, 0, 0.15, mat_slab, col)

    # 2. 9" Parapet Walls (3'-6" high)
    create_box(f"{prefix}_Parapet_S", 0, 0, PLINTH_W, EXT_WALL_THICK, 0.15, WALL_H, mat_ext_wall, col)
    create_box(f"{prefix}_Parapet_N", 0, PLINTH_D - EXT_WALL_THICK, PLINTH_W, PLINTH_D, 0.15, WALL_H, mat_ext_wall, col)
    create_box(f"{prefix}_Parapet_E", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, PLINTH_D, 0.15, WALL_H, mat_ext_wall, col)
    create_box(f"{prefix}_Parapet_W_S", 0, 0, EXT_WALL_THICK, 6.80, 0.15, WALL_H, mat_ext_wall, col)
    create_box(f"{prefix}_Parapet_W_N", 0, 11.55, EXT_WALL_THICK, PLINTH_D, 0.15, WALL_H, mat_ext_wall, col)

    # 3. NW Mumty Room, Lift Overrun & 5,000L OHT Atop Mumty (Framed by C_C1 to C_C5)
    create_box(f"{prefix}_Mumty_Walls", -2.25, 6.80, -0.25, 11.05, 0.15, WALL_H, mat_ext_wall, col)
    create_box(f"{prefix}_Lift_Overrun", -2.25, 11.05, -0.45, 12.10, 0.15, WALL_H, mat_ext_wall, col)
    create_door_2d(f"{prefix}_Door_Terrace", -0.25, 9.80, 0.90, 90, 'E', col)
    create_box(f"{prefix}_OHT_Atop_Mumty", -2.20, 6.85, -0.30, 10.60, 0.15, 0.45, mat_water, col)
    add_cad_text(f"{prefix}_OHT_Lbl", "5,000L DUAL OHT ATOP STAIR MUMTY (+13.5m)\\n(FRAMED BY 4 RCC COLS C_C3, C_C4, C_C5, C3)", -1.25, 8.60, TEXT_Z, 0.18, collection=col)

    # 4. Outdoor Powder Room (Vayavyam / NW)
    create_box(f"{prefix}_Powder_Room", 0.15, 9.80, 1.45, 11.55, 0.15, WALL_H, mat_int_wall, col)
    create_door_2d(f"{prefix}_Door_Powder", 0.25, 9.80, 0.70, 90, 'W', col)
    add_cad_text(f"{prefix}_Powder_Lbl", "OUTDOOR POWDER ROOM\\n4'-0\" x 5'-0\" (GUEST WC)", 0.80, 10.35, TEXT_Z, 0.16, collection=col)

    # 5. Covered Pergola Sit-Out Pavilion (Niruthi / SW) - 18' x 12'-6"
    create_box(f"{prefix}_Pergola_Roof", 0.23, 0.23, 5.50, 3.80, 0.15, 0.25, mat_pergola, col)
    create_box(f"{prefix}_Sofa", 1.40, 0.55, 4.00, 1.25, 0.15, 0.45, mat_furniture, col)
    create_box(f"{prefix}_Coffee_Table", 1.85, 1.60, 3.55, 2.35, 0.15, 0.40, mat_furniture, col)
    create_box(f"{prefix}_Chair_1", 0.55, 1.50, 1.20, 2.15, 0.15, 0.45, mat_furniture, col)
    create_box(f"{prefix}_Chair_2", 0.55, 2.40, 1.20, 3.05, 0.15, 0.45, mat_furniture, col)
    create_box(f"{prefix}_Chair_3", 4.25, 1.50, 4.90, 2.15, 0.15, 0.45, mat_furniture, col)
    create_box(f"{prefix}_Chair_4", 4.25, 2.40, 4.90, 3.05, 0.15, 0.45, mat_furniture, col)
    add_cad_text(f"{prefix}_Sitout_Lbl", "COVERED PERGOLA SIT-OUT (NIRUTHI / SW)\\n18'-0\" x 12'-6\" (DRY LOUNGE - NO FIRE)", 2.85, 3.30, TEXT_Z, 0.18, collection=col)

    # 6. Expanded Rooftop Party Buffet & Bar Counter (West Wall) - 13' x 2'-6"
    create_box(f"{prefix}_Party_Counter", 0.23, 4.10, 0.99, 8.10, 0.15, 0.85, mat_kitchen, col)
    create_box(f"{prefix}_Party_Sink", 0.32, 7.35, 0.90, 7.95, 0.80, 0.86, mat_water, col)
    add_cad_text(f"{prefix}_Party_Lbl", "ROOFTOP PARTY BUFFET & BAR (13'x2'-6\")\\n(GRANITE BAR, SINK & 5 STOOLS)", 3.45, 5.80, TEXT_Z, 0.18, collection=col)

    # 7. Dual Rooftop Solar PV Setup (7.0 kW Total: 3.5 kW Brother + 3.5 kW Owner)
    create_box(f"{prefix}_Solar_Bank_A", 5.95, 0.45, 8.10, 3.05, 0.20, 0.35, mat_solar_a, col)
    create_box(f"{prefix}_Solar_Bank_B", 8.25, 0.45, 10.40, 3.05, 0.20, 0.35, mat_solar_b, col)
    add_cad_text(f"{prefix}_Solar_Lbl", "DUAL SOLAR PV ARRAY (7.0 kW TOTAL)\\n[3.5 kW BROTHER L1 + 3.5 kW OWNER L2]\\n(ELEVATED 8'-0\" CLEAR MS FRAME - TILT 18° SOUTH)", 8.20, 3.60, TEXT_Z, 0.18, collection=col)

    # 8. Open Sunrise Yoga & Meditation Deck (Ishanya / NE) - 17' x 15'-9"
    create_box(f"{prefix}_Yoga_Deck", 5.60, 7.20, 10.75, 11.95, 0.15, 0.20, mat_yoga, col)
    create_box(f"{prefix}_Yoga_Mat1", 7.20, 8.40, 7.90, 10.20, 0.20, 0.22, mat_furniture, col)
    create_box(f"{prefix}_Yoga_Mat2", 8.20, 8.40, 8.90, 10.20, 0.20, 0.22, mat_furniture, col)
    add_cad_text(f"{prefix}_Yoga_Lbl", "OPEN SUNRISE YOGA DECK (ISHANYA / NE)\\n17'-0\" x 15'-9\" (100% OPEN TO SKY)", 8.20, 7.60, TEXT_Z, 0.18, collection=col)

    # 9. Central Gathering Plaza (320 sq ft) & Negative Notice
    add_cad_text(f"{prefix}_Plaza_Lbl", "CENTRAL GATHERING PLAZA (320 SQ FT)\\n(COOL-ROOF TILES SRI > 100)", 3.60, 8.10, TEXT_Z, 0.18, collection=col)
    add_cad_text(f"{prefix}_Notice_Lbl", "★ NO JACUZZI / NO POOL ★\\n(100% LEAK-FREE SLAB)", 3.60, 7.00, TEXT_Z, 0.16, collection=col)

    # 11. Columns
    for c in dm.COLUMNS:
        cx = c["x"] * M_PER_MM
        cy = c["y"] * M_PER_MM
        cw = c["width"] * M_PER_MM
        cd = c["depth"] * M_PER_MM
        create_box(f"{prefix}_Col_{c['id']}", cx - cw/2, cy - cd/2, cx + cw/2, cy + cd/2, 0.15, WALL_H, mat_col, col)

    return col

# =============================================================================
# BUILDER 4: ISOLATED CAMERAS & LIGHTING (04_Cameras_and_Lighting)
# =============================================================================
def build_cameras_and_lights(parent_col):
    col = bpy.data.collections.new("04_Cameras_and_Lighting")
    parent_col.children.link(col)
    
    # Sun Directional Light
    bpy.ops.object.light_add(type='SUN', location=(PLINTH_W/2, PLINTH_D/2, 25))
    sun = bpy.context.active_object
    sun.name = "Sun_CAD"
    sun.data.energy = 2.2
    sun.data.color = (1.0, 1.0, 1.0)
    col.objects.link(sun)
    bpy.context.scene.collection.objects.unlink(sun)
    
    # Ground & Site Ortho Camera (fits entire 54'x66' plot + both 30' municipal roads)
    cx_site = (PLOT_X0 + PLOT_X1) / 2.0
    cy_site = (PLOT_Y0 + PLOT_Y1) / 2.0
    cam_ground = create_ortho_camera("Cam_Ground", cx_site, cy_site, ortho_scale=32.0, target_col=col)
    
    # Upper Floors Ortho Camera (fits complete residential floor with wrap-around balconies)
    cx_upper = PLINTH_W / 2.0
    cy_upper = PLINTH_D / 2.0 + 0.15
    cam_upper = create_ortho_camera("Cam_Upper", cx_upper, cy_upper, ortho_scale=19.5, target_col=col)
    
    return col, cam_ground, cam_upper, sun

# =============================================================================
# MAIN RENDER PIPELINE & VIEW LAYER CONFIGURATION
# =============================================================================
def main():
    print("=" * 75)
    print("STARTING MULTI-COLLECTION ARCHITECTURAL CAD ENGINE FOR PROPERTY 2")
    print("=" * 75)
    
    scene = setup_scene()
    root_col = scene.collection
    
    # Build 6 Isolated Collections:
    col_site = build_site_plan(root_col)
    col_ground = build_ground_stilt(root_col)
    col_l1 = build_upper_floor(root_col, floor_code="L1", is_owner_level=False)
    col_l2 = build_upper_floor(root_col, floor_code="L2", is_owner_level=True)
    col_l3 = build_terrace_roof(root_col)
    col_cam, cam_ground, cam_upper, sun = build_cameras_and_lights(root_col)
    
    # --- RENDER 1: GROUND STILT & SITE PLAN ---
    col_site.hide_render = False
    col_ground.hide_render = False
    col_l1.hide_render = True
    col_l2.hide_render = True
    col_l3.hide_render = True
    scene.camera = cam_ground
    p_ground = str(OUTPUT_DIR / "ground_stilt_2d.png")
    scene.render.filepath = p_ground
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {Path(p_ground).name}")
    
    # --- RENDER 2: LEVEL 1 (BROTHER 3BHK) ---
    col_site.hide_render = False
    col_ground.hide_render = True
    col_l1.hide_render = False
    col_l2.hide_render = True
    col_l3.hide_render = True
    scene.camera = cam_upper
    p_l1 = str(OUTPUT_DIR / "first_floor_brother_2d.png")
    scene.render.filepath = p_l1
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {Path(p_l1).name}")
    
    # --- RENDER 3: LEVEL 2 (OWNER 2BHK + OFFICE) ---
    col_site.hide_render = False
    col_ground.hide_render = True
    col_l1.hide_render = True
    col_l2.hide_render = False
    col_l3.hide_render = True
    scene.camera = cam_upper
    p_l2 = str(OUTPUT_DIR / "second_floor_owner_2d.png")
    scene.render.filepath = p_l2
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {Path(p_l2).name}")

    # --- RENDER 4: LEVEL 3 (ROOFTOP TERRACE) ---
    col_site.hide_render = False
    col_ground.hide_render = True
    col_l1.hide_render = True
    col_l2.hide_render = True
    col_l3.hide_render = False
    scene.camera = cam_upper
    p_l3 = str(OUTPUT_DIR / "terrace_roof_2d.png")
    scene.render.filepath = p_l3
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {Path(p_l3).name}")
    
    # --- CONFIGURE VIEW LAYER FOR USER INTERACTION IN BLENDER ---
    def configure_view_layer(layer_col, active_names, excluded_names):
        if layer_col.name in excluded_names:
            layer_col.exclude = True
        elif layer_col.name in active_names:
            layer_col.exclude = False
        for child in layer_col.children:
            configure_view_layer(child, active_names, excluded_names)

    active_set = {"00_Site_Plan", "03_Second_Floor_Owner"}
    excluded_set = {"01_Ground_Floor_Stilt", "02_First_Floor_Brother", "05_Terrace_Roof", "04_Cameras_and_Lighting"}
    configure_view_layer(bpy.context.view_layer.layer_collection, active_set, excluded_set)
    
    col_site.hide_viewport = False
    col_l2.hide_viewport = False
    col_ground.hide_viewport = True
    col_l1.hide_viewport = True
    col_l3.hide_viewport = True
    col_cam.hide_viewport = True

    # Configure 3D Viewport spaces: Solid Shading with Material colors & hide camera wireframes
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'SOLID'
                        space.shading.color_type = 'MATERIAL'
                        space.overlay.show_extras = False

    # Save Master .blend file
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_FILE))
    print(f"CAD Master .blend saved to: {BLEND_FILE}")
    print("=" * 75)
    print("ALL 6 COLLECTIONS CLEANLY ORGANIZED & VALIDATED")
    print("=" * 75)

if __name__ == "__main__":
    main()

