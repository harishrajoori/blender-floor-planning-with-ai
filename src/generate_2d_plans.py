"""
Civil Engineering & Vaastu-Compliant 2D Architectural CAD Engine for Property 2 (54' x 66' Plot)
Automates Ground Floor (Entire Plot 54'x66' + Plinth 37'x40' + Setbacks + Gardens + Parking)
and Upper Floors:
  - Level 1: Brother's Full 3 BHK (Master SW, Bed 2 NW, Bed 3 North, Daily Pooja, Family Lounge, 360° Walk-Around Slab)
  - Level 2: Owner's 2 BHK + North Home Office + Mallanna Shrine (Faces North) + Daily Pooja (4' max width, faces East)
Continuous 360° Cantilever Walk-Around Slab Gallery on Upper Floors.
All 16 RCC Columns (9"x18") 100% Embedded in Walls (Zero Free-Standing Columns in Living Room).
Utility Balcony entered from Dining Lobby, NEVER from Kitchen.
Independent Private Lobby for Master Bed, Common Bath, and NW Office/Bedroom (Zero Walking through Bedrooms).
"""

import bpy
import math
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BLEND_FILE = OUTPUT_DIR / "property2_engineering_cad.blend"

# =============================================================================
# GEOMETRY CONSTANTS (METRIC CONVERSION: 1 FT = 0.3048 M)
# =============================================================================
# Total Plot: 54'-0" (16.4592m) EW x 66'-0" (20.1168m) NS = 3,564 sq ft
PLOT_W = 54.0 * 0.3048   # 16.4592m
PLOT_D = 66.0 * 0.3048   # 20.1168m

# Plinth Built-up Footprint: 37'-0" (11.2776m) EW x 40'-0" (12.1920m) NS = 1,480 sq ft
PLINTH_W = 37.0 * 0.3048 # 11.2776m
PLINTH_D = 40.0 * 0.3048 # 12.1920m

# Setbacks (Vaastu: North & East larger than South & West):
# West = 8'-0" (2.4384m), South = 9'-0" (2.7432m)
# East = 54' - (8' + 37') = 9'-0" (2.7432m) -> East >= West (PASS)
# North = 66' - (9' + 40') = 17'-0" (5.1816m) -> North > South (PASS)
SETBACK_W = 8.0 * 0.3048  # 2.4384m
SETBACK_S = 9.0 * 0.3048  # 2.7432m
SETBACK_E = 9.0 * 0.3048  # 2.7432m
SETBACK_N = 17.0 * 0.3048 # 5.1816m

# Plot Boundaries in Plinth Coordinate Frame (Plinth at 0,0 to PLINTH_W, PLINTH_D):
PLOT_X0 = -SETBACK_W               # -2.4384m
PLOT_X1 = PLINTH_W + SETBACK_E     # 14.0208m
PLOT_Y0 = -SETBACK_S               # -2.7432m
PLOT_Y1 = PLINTH_D + SETBACK_N     # 17.3736m

WALL_H = 0.90           # Cut-plane section height
EXT_WALL_THICK = 0.230  # 9" exterior brick wall
INT_WALL_THICK = 0.115  # 4.5" interior partition wall
COMPOUND_WALL_THICK = 0.150 # 6" compound boundary wall
COL_W = 0.230           # 9" column width
COL_D = 0.450           # 18" column depth

# 16 RCC Column Grid Intersections (4x4 Grid)
GRID_X = [0.115, 3.810, 7.315, PLINTH_W - 0.115]
GRID_Y = [0.115, 4.064, 8.128, PLINTH_D - 0.115]

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

def get_or_create_material(name, color_rgba):
    if name in bpy.data.materials:
        mat = bpy.data.materials[name]
    else:
        mat = bpy.data.materials.new(name=name)
        mat.diffuse_color = color_rgba
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

def add_cad_text(name, text, x, y, z=2.50, size=0.22, align_x='CENTER', align_y='CENTER', rot_z=0.0, color=COLOR_TEXT, collection=None):
    """Adds high-elevation 2D CAD text so it is NEVER clipped or hidden by 3D geometry in orthographic view."""
    mat = get_or_create_material(f"Mat_Text_{name}", color)
    curve_data = bpy.data.curves.new(name=f"Curve_{name}", type='FONT')
    curve_data.body = text
    curve_data.size = size
    curve_data.align_x = align_x
    curve_data.align_y = align_y
    
    obj = bpy.data.objects.new(name, curve_data)
    obj.location = (x, y, z)
    obj.rotation_euler = (0, 0, rot_z)
    obj.color = color
    obj.data.materials.append(mat)
    if collection:
        collection.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)
    return obj

def create_door_2d(name, hinge_x, hinge_y, width, open_angle_deg, open_side='E', mat=None, collection=None):
    mat = mat or get_or_create_material("Mat_Door", COLOR_DOOR)
    leaf_thick = 0.035
    if open_side == 'E':
        dx, dy = width, leaf_thick
        lx, ly = hinge_x + width/2.0, hinge_y
    elif open_side == 'W':
        dx, dy = width, leaf_thick
        lx, ly = hinge_x - width/2.0, hinge_y
    elif open_side == 'N':
        dx, dy = leaf_thick, width
        lx, ly = hinge_x, hinge_y + width/2.0
    else: # 'S'
        dx, dy = leaf_thick, width
        lx, ly = hinge_x, hinge_y - width/2.0
        
    create_box(f"{name}_Leaf", lx - dx/2, ly - dy/2, lx + dx/2, ly + dy/2, 0, WALL_H, mat, collection)
    
    curve_data = bpy.data.curves.new(name=f"{name}_Arc", type='CURVE')
    curve_data.dimensions = '2D'
    polyline = curve_data.splines.new('POLY')
    
    pts = []
    num_pts = 12
    for i in range(num_pts + 1):
        rad = math.radians((open_angle_deg / num_pts) * i)
        if open_side == 'E':
            px = hinge_x + width * math.cos(rad)
            py = hinge_y + width * math.sin(rad)
        elif open_side == 'N':
            px = hinge_x + width * math.sin(rad)
            py = hinge_y + width * math.cos(rad)
        elif open_side == 'W':
            px = hinge_x - width * math.cos(rad)
            py = hinge_y + width * math.sin(rad)
        else: # 'S'
            px = hinge_x + width * math.sin(rad)
            py = hinge_y - width * math.cos(rad)
        pts.append((px, py, 0.02))
        
    polyline.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        polyline.points[i].co = (p[0], p[1], p[2], 1.0)
        
    arc_obj = bpy.data.objects.new(f"{name}_ArcObj", curve_data)
    arc_obj.color = COLOR_DOOR
    arc_obj.data.materials.append(mat)
    if collection:
        collection.objects.link(arc_obj)
    else:
        bpy.context.scene.collection.objects.link(arc_obj)
    return arc_obj

def create_window_2d(name, x0, y0, x1, y1, mat=None, collection=None):
    mat = mat or get_or_create_material("Mat_Window", COLOR_WINDOW)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    create_box(f"{name}_Sill", x0, y0, x1, y1, 0, 0.25, mat, collection)
    if dx > dy:
        create_box(f"{name}_Glass", x0, (y0+y1)/2.0 - 0.015, x1, (y0+y1)/2.0 + 0.015, 0.25, WALL_H, mat, collection)
    else:
        create_box(f"{name}_Glass", (x0+x1)/2.0 - 0.015, y0, (x0+x1)/2.0 + 0.015, y1, 0.25, WALL_H, mat, collection)

def add_columns(collection):
    mat_col = get_or_create_material("Mat_Column", COLOR_COLUMN)
    for i, cx in enumerate(GRID_X):
        for j, cy in enumerate(GRID_Y):
            name = f"RCC_Col_X{i+1}_Y{j+1}"
            create_box(name, cx - COL_W/2.0, cy - COL_D/2.0, cx + COL_W/2.0, cy + COL_D/2.0, 0, WALL_H + 0.1, mat_col, collection)

def add_external_vertical_core(collection):
    mat_int = get_or_create_material("Mat_IntWall", COLOR_INT_WALL)
    mat_ext = get_or_create_material("Mat_ExtWall", COLOR_EXT_WALL)
    mat_slab = get_or_create_material("Mat_Slab", COLOR_SLAB)
    mat_tread = get_or_create_material("Mat_StairTread", (0.82, 0.85, 0.90, 1.0))
    mat_lift = get_or_create_material("Mat_LiftCabin", (0.75, 0.82, 0.90, 1.0))
    
    core_x0 = -2.40
    core_x1 = 0.0
    core_y0 = 6.50
    core_y1 = 12.19
    
    # Outer core enclosing walls
    create_box("Core_Slab", core_x0, core_y0, core_x1, core_y1, 0, 0.08, mat_slab, collection)
    create_box("Core_Wall_W", core_x0, core_y0, core_x0 + 0.15, core_y1, 0, WALL_H, mat_ext, collection)
    create_box("Core_Wall_N", core_x0, core_y1 - 0.15, core_x1, core_y1, 0, WALL_H, mat_ext, collection)
    create_box("Core_Wall_S", core_x0, core_y0, core_x1, core_y0 + 0.15, 0, WALL_H, mat_ext, collection)
    create_box("Core_Mid_Wall", core_x0, 9.80 - 0.08, core_x1, 9.80 + 0.08, 0, WALL_H, mat_int, collection)
    
    # Detailed 10-Tread Staircase
    stair_w = (core_x1 - core_x0 - 0.15 - 0.10) / 2.0
    num_treads = 10
    tread_d = (9.70 - 7.50) / num_treads
    for t in range(num_treads):
        ty0 = 7.50 + t * tread_d
        ty1 = ty0 + tread_d
        create_box(f"Stair_Up_Tr_{t}", core_x0 + 0.15, ty0, core_x0 + 0.15 + stair_w, ty1, 0, 0.08 + (t+1)*0.02, mat_tread, collection)
        create_box(f"Stair_Up_Nose_{t}", core_x0 + 0.15, ty1 - 0.025, core_x0 + 0.15 + stair_w, ty1, 0.08 + (t+1)*0.02, 0.09 + (t+1)*0.02, mat_int, collection)
        create_box(f"Stair_Dn_Tr_{t}", core_x1 - stair_w, ty0, core_x1, ty1, 0, 0.35 + (t+1)*0.02, mat_tread, collection)
        create_box(f"Stair_Dn_Nose_{t}", core_x1 - stair_w, ty0, core_x1, ty0 + 0.025, 0.35 + (t+1)*0.02, 0.36 + (t+1)*0.02, mat_int, collection)
        
    create_box("Stair_Mid_Landing", core_x0 + 0.15, 6.65, core_x1, 7.50, 0, 0.30, mat_slab, collection)
    
    # Directional Text on Stairs
    add_cad_text("Lbl_Stair_UP", "UP ->", core_x0 + 0.15 + stair_w/2.0, 8.60, z=2.50, size=0.16, color=(0.1, 0.3, 0.6, 1.0), collection=collection)
    add_cad_text("Lbl_Stair_DN", "<- DN", core_x1 - stair_w/2.0, 8.60, z=2.50, size=0.16, color=(0.5, 0.2, 0.1, 1.0), collection=collection)
    add_cad_text("Lbl_MidLanding", "MID LANDING (4'x8')", core_x0 + 1.1, 7.05, z=2.50, size=0.14, color=COLOR_DIM, collection=collection)
    
    # 6-PAX Lift
    create_box("Lift_Shaft_Box", core_x0 + 0.15, 9.90, core_x1, 12.04, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Cabin", core_x0 + 0.35, 10.15, core_x1 - 0.20, 11.85, 0.05, WALL_H * 0.95, mat_lift, collection)
    create_door_2d("Lift_Telescopic_Door", core_x1 - 0.02, 10.55, 0.90, 90, 'W', None, collection)
    add_cad_text("Lbl_Lift", "6-PAX LIFT\n(AUTOMATIC)", (core_x0 + core_x1)/2.0, 11.0, z=2.50, size=0.15, color=(0.05, 0.2, 0.4, 1.0), collection=collection)

def add_title_block(sheet_title, collection, is_ground=False):
    mat_paper = get_or_create_material("Mat_TitlePaper", (0.98, 0.98, 0.99, 1.0))
    mat_border = get_or_create_material("Mat_TitleBorder", (0.15, 0.20, 0.28, 1.0))
    
    bx = PLOT_X1 + 1.2 if is_ground else PLINTH_W + 1.2
    by = 2.6
    bw = 4.8
    bh = 6.5
    
    # White background card
    create_box("Title_Block_Bg", bx, by, bx + bw, by + bh, 0.01, 0.03, mat_paper, collection)
    # Border edges (top, bottom, left, right)
    th = 0.04
    create_box("TB_Border_L", bx, by, bx + th, by + bh, 0.04, 0.06, mat_border, collection)
    create_box("TB_Border_R", bx + bw - th, by, bx + bw, by + bh, 0.04, 0.06, mat_border, collection)
    create_box("TB_Border_B", bx, by, bx + bw, by + th, 0.04, 0.06, mat_border, collection)
    create_box("TB_Border_T", bx, by + bh - th, bx + bw, by + bh, 0.04, 0.06, mat_border, collection)
    
    cx = bx + bw / 2.0
    add_cad_text("TB_Title1", "PROPERTY 2 RESIDENCE", cx, by + 5.9, z=2.50, size=0.26, color=(0.05, 0.10, 0.20, 1.0), collection=collection)
    add_cad_text("TB_Title2", sheet_title.upper(), cx, by + 5.4, z=2.50, size=0.19, color=(0.05, 0.45, 0.35, 1.0), collection=collection)
    
    specs = [
        "PLOT: 54'-0\" x 66'-0\" (SW Corner, 3,564 sf)",
        "PLINTH: 37'-0\" x 40'-0\" (1,480 sf Footprint)",
        "SETBACKS: N:17' E:9' S:9' W:8' (Vaastu Compliant)",
        "CORE: External NW Stairs & 6-PAX Lift",
        "SLAB: Continuous 360° Walk-Around Cantilever",
        "COLUMNS: 16 RCC (9\"x18\") 100% Enclosed in Walls",
        "UTILITY: External Balcony via Dining Lobby",
        "DAILY POOJA: Compact 4' Width (Faces East)",
        "MALLANNA: 8'x8' Shrine (Faces North, L2 Only)",
        "VAASTU: Telugu / Telangana (Open Ishanya NE)",
        "SIMHADWARAM: North-North-East (NNE) Entrance"
    ]
    
    for i, sp in enumerate(specs):
        add_cad_text(f"TB_Spec_{i}", sp, bx + 0.25, by + 4.8 - i * 0.40, z=2.50, size=0.13, align_x='LEFT', color=(0.10, 0.15, 0.22, 1.0), collection=collection)

def setup_scene(name, is_ground=False):
    if name in bpy.data.scenes:
        scene = bpy.data.scenes[name]
        for obj in list(scene.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    else:
        scene = bpy.data.scenes.new(name)
        
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.light = 'FLAT'
    scene.display.shading.color_type = 'OBJECT'
    scene.render.resolution_x = 2400
    scene.render.resolution_y = 2000 if is_ground else 1850
    scene.render.resolution_percentage = 100
    
    cam_name = f"Camera_{name}"
    cam_data = bpy.data.cameras.new(name=cam_name)
    cam_data.type = 'ORTHO'
    
    if is_ground:
        cam_data.ortho_scale = 32.0
        cam_x = 7.5
        cam_y = 7.5
    else:
        cam_data.ortho_scale = 22.0
        cam_x = 7.2
        cam_y = 6.2
        
    cam_obj = bpy.data.objects.new(cam_name, cam_data)
    cam_obj.location = (cam_x, cam_y, 35.0)
    cam_obj.rotation_euler = (0, 0, 0)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    bpy.context.window.scene = scene
    return scene

# =============================================================================
# LEVEL 0: GROUND FLOOR (STILT, PARKING, PLOT & GARDENS)
# =============================================================================
def build_ground_stilt():
    scene = setup_scene("Ground_Stilt", is_ground=True)
    col = scene.collection

    mat_plot = get_or_create_material("Mat_Plot_Bg", COLOR_PLOT_BG)
    mat_road = get_or_create_material("Mat_Road", COLOR_ROAD)
    mat_compound = get_or_create_material("Mat_Compound", COLOR_COMPOUND)
    mat_garden = get_or_create_material("Mat_Garden", COLOR_GARDEN)
    mat_drive = get_or_create_material("Mat_Driveway", COLOR_DRIVEWAY)
    mat_parking = get_or_create_material("Mat_Parking", COLOR_PARKING)
    mat_pavil = get_or_create_material("Mat_Pavilion", COLOR_PAVILION)

    # 1. West Road (30' wide) & South Road (24' wide)
    create_box("West_Road", PLOT_X0 - 9.144, PLOT_Y0 - 7.315, PLOT_X0, PLOT_Y1 + 1.0, -0.05, 0.0, mat_road, col)
    create_box("South_Road", PLOT_X0 - 9.144, PLOT_Y0 - 7.315, PLOT_X1 + 1.0, PLOT_Y0, -0.05, 0.0, mat_road, col)
    add_cad_text("Lbl_WestRoad", "30'-0\" WIDE WEST ROAD (PRIMARY ACCESS & MAIN GATES)", PLOT_X0 - 4.5, (PLOT_Y0 + PLOT_Y1)/2.0, z=2.50, size=0.28, rot_z=math.radians(90), color=(0.1, 0.2, 0.4, 1.0), collection=col)
    add_cad_text("Lbl_SouthRoad", "24'-0\" WIDE SOUTH ROAD (SECONDARY ACCESS)", (PLOT_X0 + PLOT_X1)/2.0, PLOT_Y0 - 3.6, z=2.50, size=0.28, color=(0.1, 0.2, 0.4, 1.0), collection=col)

    # 2. Total Plot Ground Base (54' x 66')
    create_box("Plot_Base", PLOT_X0, PLOT_Y0, PLOT_X1, PLOT_Y1, -0.02, 0.0, mat_plot, col)

    # 3. 6" Compound Wall with Gates
    cw = COMPOUND_WALL_THICK
    # North Boundary Wall
    create_box("CW_North", PLOT_X0, PLOT_Y1 - cw, PLOT_X1, PLOT_Y1, 0, WALL_H * 0.7, mat_compound, col)
    # East Boundary Wall
    create_box("CW_East", PLOT_X1 - cw, PLOT_Y0, PLOT_X1, PLOT_Y1, 0, WALL_H * 0.7, mat_compound, col)
    # South Boundary Wall with Secondary Gate
    create_box("CW_South_1", PLOT_X0, PLOT_Y0, 6.0, PLOT_Y0 + cw, 0, WALL_H * 0.7, mat_compound, col)
    add_cad_text("Lbl_Gate_South", "SECONDARY GATE (10' WIDE)", 7.5, PLOT_Y0, z=2.50, size=0.20, color=COLOR_DOOR, collection=col)
    create_box("CW_South_2", 9.0, PLOT_Y0, PLOT_X1, PLOT_Y0 + cw, 0, WALL_H * 0.7, mat_compound, col)
    # West Boundary Wall with Main Sliding Gate & Wicket Gate
    create_box("CW_West_1", PLOT_X0, PLOT_Y0, PLOT_X0 + cw, 10.0, 0, WALL_H * 0.7, mat_compound, col)
    add_cad_text("Lbl_Gate_Main", "MAIN SLIDING GATE (14' WIDE)", PLOT_X0, 12.5, z=2.50, size=0.20, rot_z=math.radians(90), color=COLOR_DOOR, collection=col)
    create_box("CW_West_2", PLOT_X0, 14.5, PLOT_X0 + cw, 15.2, 0, WALL_H * 0.7, mat_compound, col)
    add_cad_text("Lbl_Gate_Wicket", "WICKET GATE (3.5' WIDE)", PLOT_X0, 15.8, z=2.50, size=0.18, rot_z=math.radians(90), color=COLOR_DOOR, collection=col)
    create_box("CW_West_3", PLOT_X0, 16.3, PLOT_X0 + cw, PLOT_Y1, 0, WALL_H * 0.7, mat_compound, col)

    # 4. Setback Zones & Gardens
    # North Garden (17' Setback = 5.18m)
    create_box("North_Garden_Lawn", 0, PLINTH_D, PLOT_X1 - cw, PLOT_Y1 - cw, 0, 0.04, mat_garden, col)
    add_cad_text("Lbl_NorthGarden", "NORTH FRONT LAWN & VAASTU GARDEN\n(17'-0\" SETBACK - OPEN TO SKY)\nMAXIMUM MORNING SUNLIGHT & BREEZE", 6.0, PLINTH_D + 2.6, z=2.50, size=0.26, color=(0.05, 0.40, 0.15, 1.0), collection=col)

    # East Morning Garden (9' Setback = 2.74m)
    create_box("East_Garden", PLINTH_W, 0, PLOT_X1 - cw, PLINTH_D, 0, 0.04, mat_garden, col)
    add_cad_text("Lbl_EastGarden", "EAST MORNING GARDEN (9'-0\" SETBACK)", PLINTH_W + 1.3, PLINTH_D/2.0, z=2.50, size=0.20, rot_z=math.radians(-90), color=(0.05, 0.40, 0.15, 1.0), collection=col)

    # South Setback (9' = 2.74m) & West Setback (8' = 2.44m)
    create_box("South_Setback_Paving", 0, PLOT_Y0 + cw, PLOT_X1 - cw, 0, 0, 0.02, mat_drive, col)
    add_cad_text("Lbl_SouthSetback", "SOUTH SETBACK (9'-0\" DRIVEWAY)", 6.0, -1.3, z=2.50, size=0.20, color=COLOR_DIM, collection=col)

    create_box("West_Driveway_Paving", PLOT_X0 + cw, PLOT_Y0 + cw, 0, PLOT_Y1 - cw, 0, 0.02, mat_drive, col)
    add_cad_text("Lbl_WestSetback", "WEST SETBACK (8'-0\" DRIVEWAY)", -1.2, 3.0, z=2.50, size=0.20, rot_z=math.radians(90), color=COLOR_DIM, collection=col)

    # 5. Stilt Built-Up Footprint (37' x 40')
    # North-East Stilt Pavilion (approx 750 sq ft clear gathering area)
    create_box("Stilt_Pavilion_Floor", 3.810, 4.064, PLINTH_W, PLINTH_D, 0, 0.06, mat_pavil, col)
    add_cad_text("Lbl_Pavilion", "STILT MULTIPURPOSE PAVILION\n(~750 SQ FT GATHERING SPACE)\nFESTIVALS, RITUALS, CELEBRATIONS", (3.810 + PLINTH_W)/2.0, (4.064 + PLINTH_D)/2.0, z=2.50, size=0.26, color=(0.4, 0.3, 0.1, 1.0), collection=col)

    # South & West Parking Bays
    create_box("Car_Parking_1", 3.810, 0, 7.315, 4.064, 0, 0.05, mat_parking, col)
    add_cad_text("Lbl_Car1", "CAR PARKING 1\n(COVERED)", 5.5, 2.0, z=2.50, size=0.22, color=COLOR_TEXT, collection=col)

    create_box("Car_Parking_2", 7.315, 0, PLINTH_W, 4.064, 0, 0.05, mat_parking, col)
    add_cad_text("Lbl_Car2", "CAR PARKING 2\n(COVERED)", 9.3, 2.0, z=2.50, size=0.22, color=COLOR_TEXT, collection=col)

    create_box("Bike_Parking", 0, 0, 3.810, 4.064, 0, 0.05, mat_parking, col)
    add_cad_text("Lbl_Bikes", "4x BIKE PARKING\n+ EV CHARGING", 1.9, 2.0, z=2.50, size=0.22, color=COLOR_TEXT, collection=col)

    # 6. External NW Vertical Core
    add_external_vertical_core(col)

    # 7. 16 Structural RCC Columns
    add_columns(col)

    # 8. Vaastu Water Infrastructure
    mat_water = get_or_create_material("Mat_Water", (0.2, 0.6, 0.9, 1.0))
    create_box("NE_Water_Sump", 10.5, 13.5, 12.5, 15.5, 0, 0.20, mat_water, col)
    add_cad_text("Lbl_Sump", "UNDERGROUND WATER SUMP\n(ISHANYA / NE CORNER)", 11.5, 14.5, z=2.50, size=0.16, color=(0.05, 0.2, 0.5, 1.0), collection=col)

    create_box("NE_Rainwater_Harvest", 12.8, 14.0, 13.6, 15.5, 0, 0.15, mat_water, col)
    add_cad_text("Lbl_RWH", "RWH PIT", 13.2, 14.7, z=2.50, size=0.14, rot_z=math.radians(-90), color=(0.05, 0.2, 0.5, 1.0), collection=col)

    # 9. Title Block & Dimensions
    add_title_block("Ground Stilt, Parking, Plot & Gardens", col, is_ground=True)

    add_cad_text("Dim_PlotW", "54'-0\" [16.46m] TOTAL PLOT WIDTH (EAST-WEST)", (PLOT_X0 + PLOT_X1)/2.0, PLOT_Y0 - 1.8, z=2.50, size=0.24, color=COLOR_DIM, collection=col)
    add_cad_text("Dim_PlotD", "66'-0\" [20.12m] TOTAL PLOT DEPTH (NORTH-SOUTH)", PLOT_X0 - 2.0, (PLOT_Y0 + PLOT_Y1)/2.0, z=2.50, size=0.24, rot_z=math.radians(90), color=COLOR_DIM, collection=col)
    add_cad_text("Dim_PlinthW", "37'-0\" [11.28m] BUILT-UP PLINTH WIDTH", PLINTH_W/2.0, -0.6, z=2.50, size=0.20, color=(0.1, 0.4, 0.3, 1.0), collection=col)
    add_cad_text("Dim_PlinthD", "40'-0\" [12.19m] BUILT-UP PLINTH DEPTH", -0.6, PLINTH_D/2.0, z=2.50, size=0.20, rot_z=math.radians(90), color=(0.1, 0.4, 0.3, 1.0), collection=col)

    scene.render.filepath = str(OUTPUT_DIR / "ground_stilt_2d.png")
    bpy.ops.render.render(write_still=True)
    print("Rendered: ground_stilt_2d.png")

# =============================================================================
# UPPER FLOORS: LEVEL 1 (BROTHER 3BHK) & LEVEL 2 (OWNER 2BHK + OFFICE)
# =============================================================================
def build_upper_floor(is_owner_level=False):
    scene_name = "Second_Floor_Owner" if is_owner_level else "First_Floor_Brother"
    scene = setup_scene(scene_name, is_ground=False)
    col = scene.collection

    mat_slab = get_or_create_material("Mat_Slab", COLOR_SLAB)
    mat_balcony = get_or_create_material("Mat_Balcony", COLOR_BALCONY)
    mat_ext = get_or_create_material("Mat_ExtWall", COLOR_EXT_WALL)
    mat_int = get_or_create_material("Mat_IntWall", COLOR_INT_WALL)
    mat_bed = get_or_create_material("Mat_Bed", COLOR_BED)
    mat_cupboard = get_or_create_material("Mat_Cupboard", COLOR_CUPBOARD)
    mat_furn = get_or_create_material("Mat_Furniture", COLOR_FURNITURE)
    mat_kit = get_or_create_material("Mat_Kitchen", COLOR_KITCHEN)
    mat_pooja = get_or_create_material("Mat_Pooja", COLOR_POOJA)

    # 1. Main Plinth Base Floor Slab (37' x 40')
    create_box("Floor_Slab_Base", 0, 0, PLINTH_W, PLINTH_D, -0.02, 0, mat_slab, col)

    # 2. CONTINUOUS 360° CANTILEVER WALK-AROUND SLAB GALLERY
    # North Cantilever Promenade (4'-3" wide = 1.30m)
    create_box("Slab_North_Promenade", 0, PLINTH_D, PLINTH_W, PLINTH_D + 1.30, -0.02, 0, mat_balcony, col)
    create_box("Railing_North", 0, PLINTH_D + 1.25, PLINTH_W, PLINTH_D + 1.30, 0, 0.45, mat_ext, col)

    # East Cantilever Balcony & Utility (3'-6" to 4'-8" wide)
    create_box("Slab_East_Gallery", PLINTH_W, 0, PLINTH_W + 1.07, PLINTH_D, -0.02, 0, mat_balcony, col)
    create_box("Slab_Utility_Balcony", PLINTH_W, 0, PLINTH_W + 1.42, 4.80, -0.02, 0, mat_balcony, col)
    create_box("Railing_Utility", PLINTH_W + 1.37, 0, PLINTH_W + 1.42, 4.80, 0, 0.45, mat_ext, col)

    # South Shaded Cantilever Balcony (3'-6" wide across full South facade)
    create_box("Slab_South_Balcony", 0, -1.07, PLINTH_W, 0, -0.02, 0, mat_balcony, col)
    create_box("Railing_South", 0, -1.07, PLINTH_W, -1.02, 0, 0.45, mat_ext, col)

    # West Continuous Walkway (3'-0" wide connecting South Balcony to NW Core)
    create_box("Slab_West_Walkway", -0.91, -1.07, 0, 6.50, -0.02, 0, mat_balcony, col)
    create_box("Railing_West", -0.91, -1.07, -0.86, 6.50, 0, 0.45, mat_ext, col)

    # 3. External NW Vertical Core (Stairs & Lift)
    add_external_vertical_core(col)

    # 4. 16 Structural RCC Columns (All embedded in walls)
    add_columns(col)

    # 5. Exterior 9" Load-Bearing Masonry Walls
    # South Exterior Wall
    create_box("Ext_S_1", 0, 0, 1.2, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_MB_S_Balcony", 1.2, EXT_WALL_THICK, 0.90, 90, 'S', None, col)
    create_box("Ext_S_2", 2.1, 0, 4.8, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_Dining_S_Balcony", 4.8, EXT_WALL_THICK, 1.50, 90, 'S', None, col)
    create_box("Ext_S_3", 6.3, 0, PLINTH_W, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)

    # East Exterior Wall
    create_box("Ext_E_1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 2.0, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Kit_East", PLINTH_W - EXT_WALL_THICK, 2.0, PLINTH_W, 3.4, None, col)
    create_box("Ext_E_2", PLINTH_W - EXT_WALL_THICK, 3.4, PLINTH_W, 4.40, 0, WALL_H, mat_ext, col)
    # UTILITY DOOR FROM DINING LOBBY (y=4.40 to 5.25) - NEVER FROM KITCHEN!
    create_door_2d("Door_Utility_from_Lobby", PLINTH_W - EXT_WALL_THICK, 4.40, 0.85, 90, 'E', None, col)
    create_box("Ext_E_3", PLINTH_W - EXT_WALL_THICK, 5.25, PLINTH_W, 5.80, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_EastRoom", PLINTH_W - EXT_WALL_THICK, 5.80, PLINTH_W, 7.20, None, col)
    create_box("Ext_E_4", PLINTH_W - EXT_WALL_THICK, 7.20, PLINTH_W, PLINTH_D, 0, WALL_H, mat_ext, col)

    # North Exterior Wall
    # NW Room (Office on L2 / Bed 2 on L1: x=0 to 3.81)
    create_box("Ext_N_NW1", 0, PLINTH_D - EXT_WALL_THICK, 1.0, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_NW_Garden", 1.0, PLINTH_D - EXT_WALL_THICK, 2.5, PLINTH_D, None, col)
    create_box("Ext_N_NW2", 2.5, PLINTH_D - EXT_WALL_THICK, 2.6, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_NW_Balcony", 2.6, PLINTH_D - EXT_WALL_THICK, 0.90, 90, 'N', None, col)
    create_box("Ext_N_NW3", 3.5, PLINTH_D - EXT_WALL_THICK, 3.810, PLINTH_D, 0, WALL_H, mat_ext, col)

    # North-Central Room (Bed 2 on L2 / Bed 3 on L1: x=3.810 to 7.315)
    create_box("Ext_N_NC1", 3.810, PLINTH_D - EXT_WALL_THICK, 4.2, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_NC_Garden", 4.2, PLINTH_D - EXT_WALL_THICK, 5.6, PLINTH_D, None, col)
    create_box("Ext_N_NC2", 5.6, PLINTH_D - EXT_WALL_THICK, 5.8, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_NC_Balcony", 5.8, PLINTH_D - EXT_WALL_THICK, 0.90, 90, 'N', None, col)
    create_box("Ext_N_NC3", 6.7, PLINTH_D - EXT_WALL_THICK, 7.315, PLINTH_D, 0, WALL_H, mat_ext, col)

    # West Exterior Wall
    create_box("Ext_W_1", 0, EXT_WALL_THICK, EXT_WALL_THICK, 4.064, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_MB_West", 0, 1.5, EXT_WALL_THICK, 3.0, None, col)
    create_box("Ext_W_2", 0, 4.064, EXT_WALL_THICK, 8.128, 0, WALL_H, mat_ext, col)
    create_window_2d("Vent_Baths_West", 0, 5.2, EXT_WALL_THICK, 7.2, None, col)
    create_box("Ext_W_3", 0, 8.128, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_NW_West", 0, 9.2, EXT_WALL_THICK, 10.6, None, col)

    # =========================================================================
    # 6. ARCHITECTURAL INTERIOR PARTITIONS & CIRCULATION SYSTEM
    # =========================================================================
    
    # A. WEST BATHROOMS & PRIVATE RESIDENTIAL LOBBY (y = 4.064 to 8.128)
    # Master Attached Bath (Private to SW Master Bed: x=0.23 to 2.10, y=4.064 to 6.10)
    create_box("Bath_Divider_Horiz", EXT_WALL_THICK, 6.10 - INT_WALL_THICK/2, 2.10, 6.10 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Bath_East_Wall_Att", 2.10 - INT_WALL_THICK/2, 4.064, 2.10 + INT_WALL_THICK/2, 6.10, 0, WALL_H, mat_int, col)
    
    # Door into Attached Bath (Directly from Master Bedroom at y=4.064)
    create_box("MB_Wall_N_1", EXT_WALL_THICK, 4.064 - INT_WALL_THICK/2, 0.80, 4.064 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_AttBath_Private", 0.80, 4.064, 0.80, 90, 'N', None, col)
    create_box("MB_Wall_N_2", 1.60, 4.064 - INT_WALL_THICK/2, 2.10, 4.064 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Common Bath (x=0.23 to 2.10, y=6.10 to 8.128)
    create_box("ComBath_North_Wall", EXT_WALL_THICK, 8.128 - INT_WALL_THICK/2, 2.10, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("ComBath_East_Wall_1", 2.10 - INT_WALL_THICK/2, 6.10, 2.10 + INT_WALL_THICK/2, 6.90, 0, WALL_H, mat_int, col)
    # Door to Common Bath (Opens from Private Lobby at x=2.10, completely shielded from Living room)
    create_door_2d("Door_ComBath_East", 2.10, 6.90, 0.80, 90, 'W', None, col)
    create_box("ComBath_East_Wall_2", 2.10 - INT_WALL_THICK/2, 7.70, 2.10 + INT_WALL_THICK/2, 8.128, 0, WALL_H, mat_int, col)

    # Private Bedroom & Office Lobby (x=2.10 to 3.810, y=4.064 to 8.128 = 5'-7" x 13'-4" gallery)
    # South Wall of Lobby: Door into Master Bedroom
    create_box("Lobby_Wall_S1", 2.10, 4.064 - INT_WALL_THICK/2, 2.60, 4.064 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_MB_Entry", 2.60, 4.064, 0.86, 90, 'S', None, col)
    create_box("Lobby_Wall_S2", 3.46, 4.064 - INT_WALL_THICK/2, 3.810, 4.064 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # North Wall of Lobby: DIRECT INDEPENDENT DOOR INTO NW ROOM (OFFICE / BED 2)!
    # ZERO walking through any other bedroom!
    create_box("Lobby_Wall_N1", 2.10, 8.128 - INT_WALL_THICK/2, 2.40, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_NWRoom_Entry", 2.40, 8.128, 0.90, 90, 'N', None, col)
    create_box("Lobby_Wall_N2", 3.30, 8.128 - INT_WALL_THICK/2, 3.810, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # East Boundary of Lobby (x=3.810): Handwash niche at south, 6'-4" wide archway into Living Hall at north!
    create_box("Lobby_East_Wall", 3.810 - INT_WALL_THICK/2, 4.064, 3.810 + INT_WALL_THICK/2, 6.10, 0, WALL_H, mat_int, col)
    # Hand-wash vanity counter for Living & Dining in Lobby
    create_box("Lobby_Handwash_Vanity", 3.25, 4.25, 3.75, 5.30, 0, 0.85, mat_furn, col)

    # Master Bedroom East Partition Wall (x=3.810, y=0.23 to 4.064)
    create_box("MB_Wall_E", 3.810 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.810 + INT_WALL_THICK/2, 4.064, 0, WALL_H, mat_int, col)

    # B. SOLID SOUNDPROOF PARTITION BETWEEN NW ROOM AND NC BEDROOM (x=3.810, y=8.128 to PLINTH_D)
    create_box("Wall_Between_North_Rooms", 3.810 - INT_WALL_THICK/2, 8.128, 3.810 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)

    # C. NORTH-CENTRAL BEDROOM ENTRANCE (y=8.128, x=3.810 to 7.315)
    # Opens DIRECTLY from Grand Living Hall!
    create_box("NC_Room_Wall_S1", 3.810, 8.128 - INT_WALL_THICK/2, 4.50, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_NC_Room_Entry", 4.50, 8.128, 0.90, 90, 'N', None, col)
    create_box("NC_Room_Wall_S2", 5.40, 8.128 - INT_WALL_THICK/2, 7.315, 8.128 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # D. LIVING / DINING PARTITION & TV WALL (y=4.064, x=3.810 to 7.315)
    create_box("Dining_Living_Partition", 3.810, 4.064 - INT_WALL_THICK/2, 7.315, 4.064 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Living_TV_Unit", 4.60, 4.064 + INT_WALL_THICK/2, 6.60, 4.50, 0, 1.10, mat_cupboard, col)

    # E. MODULAR KITCHEN WALLS (SE Agneya: x=7.315 to PLINTH_W, y=0.23 to 4.064)
    create_box("Kit_Wall_North", 7.315, 4.064 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 4.064 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Kit_Wall_West_1", 7.315 - INT_WALL_THICK/2, EXT_WALL_THICK, 7.315 + INT_WALL_THICK/2, 2.20, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Kit_Entry", 7.315, 2.20, 0.90, 90, 'W', None, col)
    create_box("Kit_Wall_West_2", 7.315 - INT_WALL_THICK/2, 3.10, 7.315 + INT_WALL_THICK/2, 4.064, 0, WALL_H, mat_int, col)

    # F. STRUCTURAL GRID WALL x=7.315 ENCASING COLUMN C11 (7.315, 8.128) - ZERO EXPOSED COLUMNS!
    create_box("Grid_Wall_X3_Enclosing_C11", 7.315 - INT_WALL_THICK/2, 7.20, 7.315 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    
    # NNE Simhadwaram Entrance Portal (x=7.315, y=10.60 to 11.70)
    create_door_2d("Simhadwaram_D1_NNE", 7.315, 10.60, 1.10, 90, 'W', None, col)

    # G. COMPACT DAILY POOJA ROOM (Width 4'-0" Max: x=7.315 to 8.535, y=8.128 to 10.45)
    create_box("DailyPooja_Wall_N", 7.315, 10.45 - INT_WALL_THICK/2, 8.535, 10.45 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("DailyPooja_Wall_E", 8.535 - INT_WALL_THICK/2, 8.128, 8.535 + INT_WALL_THICK/2, 10.45, 0, WALL_H, mat_int, col)
    create_door_2d("Door_DailyPooja_West", 7.315, 8.50, 0.80, 90, 'E', None, col)

    # H. EAST WING: MALLANNA TEMPLE ROOM (ON L2 ONLY) vs FAMILY LOUNGE (ON L1)
    if is_owner_level:
        # Level 2 Owner: Mallanna Shrine (8'-4" x 8'-0", detached from kitchen, faces North)
        create_box("Mallanna_Wall_S", 7.315, 4.80 - INT_WALL_THICK/2, 9.855, 4.80 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
        create_box("Mallanna_Wall_E", 9.855 - INT_WALL_THICK/2, 4.80, 9.855 + INT_WALL_THICK/2, 7.24, 0, WALL_H, mat_int, col)
        create_box("Mallanna_Wall_N", 7.315, 7.24 - INT_WALL_THICK/2, 9.855, 7.24 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
        
        create_box("Mallanna_Wall_W1", 7.315 - INT_WALL_THICK/2, 4.80, 7.315 + INT_WALL_THICK/2, 5.60, 0, WALL_H, mat_int, col)
        create_door_2d("Door_Mallanna_West", 7.315, 5.60, 0.90, 90, 'E', None, col)
        create_box("Mallanna_Wall_W2", 7.315 - INT_WALL_THICK/2, 6.50, 7.315 + INT_WALL_THICK/2, 7.24, 0, WALL_H, mat_int, col)
        
        # Altar on South wall facing North
        create_box("Mallanna_Altar", 7.80, 4.95, 9.40, 5.55, 0, 0.95, mat_pooja, col)
        create_box("Mallanna_Carpet", 7.80, 5.75, 9.40, 7.00, 0, 0.05, mat_bed, col)
    else:
        # Level 1 Brother: Open Family Lounge & Study (12'-4" x 12'-8")
        create_box("Lounge_Wall_S", 7.315, 4.80 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 4.80 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
        create_box("Lounge_Wall_W1", 7.315 - INT_WALL_THICK/2, 4.80, 7.315 + INT_WALL_THICK/2, 5.40, 0, WALL_H, mat_int, col)
        create_box("Lounge_Wall_W2", 7.315 - INT_WALL_THICK/2, 7.00, 7.315 + INT_WALL_THICK/2, 8.128, 0, WALL_H, mat_int, col)
        
        create_box("FamilyLounge_Sofa", 7.8, 5.2, 10.5, 6.2, 0, 0.65, mat_bed, col)
        create_box("FamilyLounge_Desk", 7.8, 6.8, 10.5, 7.6, 0, 0.75, mat_furn, col)

    # =========================================================================
    # 7. BUILT-IN MILLWORK & FURNITURE LAYOUT
    # =========================================================================
    # Master Bedroom (SW Niruthi)
    create_box("MB_Wardrobe", EXT_WALL_THICK + 0.1, 0.35, EXT_WALL_THICK + 0.70, 3.80, 0, 1.10, mat_cupboard, col)
    create_box("MB_Bed", 1.4, EXT_WALL_THICK + 0.15, 3.4, EXT_WALL_THICK + 2.15, 0, 0.45, mat_bed, col)

    # Bathroom Fixtures
    create_box("AttBath_Shower", EXT_WALL_THICK + 0.1, 5.2, 1.1, 6.0, 0, 0.15, mat_balcony, col)
    create_box("AttBath_Vanity", 1.3, 4.2, 1.95, 4.9, 0, 0.85, mat_furn, col)
    
    create_box("ComBath_Shower", EXT_WALL_THICK + 0.1, 7.2, 1.1, 8.0, 0, 0.15, mat_balcony, col)
    create_box("ComBath_Vanity", 1.3, 6.2, 1.95, 6.9, 0, 0.85, mat_furn, col)

    # Kitchen Counter & Appliances (SE Agneya)
    create_box("Kit_Counter_E", PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK, 3.70, 0, 0.85, mat_kit, col)
    create_box("Kit_Counter_S", 7.40, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK + 0.65, 0, 0.85, mat_kit, col)
    create_box("Kit_Stove_EastHob", PLINTH_W - EXT_WALL_THICK - 0.60, 2.2, PLINTH_W - EXT_WALL_THICK - 0.10, 3.0, 0.86, 0.88, mat_pooja, col)

    # Out-of-House Utility Fixtures
    create_box("Utility_Wash_Machine", PLINTH_W + 0.2, 0.4, PLINTH_W + 0.9, 1.1, 0, 0.85, mat_furn, col)
    create_box("Utility_Sink", PLINTH_W + 0.2, 1.6, PLINTH_W + 0.8, 2.4, 0, 0.75, mat_kit, col)
    create_box("Utility_Gas_Cage", PLINTH_W + 0.2, 3.0, PLINTH_W + 0.8, 3.8, 0, 0.90, mat_int, col)

    # Dining Table
    create_box("Dining_Table", 4.8, 1.6, 6.4, 3.2, 0, 0.75, mat_furn, col)

    # Living Room Sofas & Coffee Table
    create_box("Sofa_Living_L", 4.6, 5.5, 7.0, 6.4, 0, 0.65, mat_bed, col)
    create_box("Living_Coffee_Table", 5.2, 6.6, 6.4, 7.4, 0, 0.40, mat_furn, col)

    # North-Central Bedroom Furniture (Bed 2 on L2 / Bed 3 on L1)
    create_box("NC_Bed", 4.8, 8.4, 6.6, 10.4, 0, 0.45, mat_bed, col)
    create_box("NC_Wardrobe", 3.810 + INT_WALL_THICK/2 + 0.1, 10.0, 3.810 + 0.65, 11.8, 0, 1.10, mat_cupboard, col)

    # Daily Pooja Altar (Compact 4' width, faces East)
    create_box("DailyPooja_Altar", 7.45, 8.6, 7.95, 9.8, 0, 0.90, mat_pooja, col)

    if is_owner_level:
        # Level 2: Home Office in NW
        create_box("Office_Exec_Desk", 1.2, 9.6, 2.8, 10.6, 0, 0.75, mat_furn, col)
        create_box("Office_Bookshelf", 0.35, 8.4, 0.75, 11.4, 0, 1.20, mat_cupboard, col)
    else:
        # Level 1: Bedroom 2 in NW
        create_box("B2_Bed", 1.4, 9.2, 3.2, 11.2, 0, 0.45, mat_bed, col)
        create_box("B2_Wardrobe", 0.35, 8.4, 0.75, 11.4, 0, 1.10, mat_cupboard, col)

    title_txt = "Second Floor - Owner's 2BHK & Office" if is_owner_level else "First Floor - Brother's 3BHK Residence"
    add_title_block(title_txt, col, is_ground=False)

    # =========================================================================
    # 8. ARCHITECTURAL TEXT CALLOUTS (Elevated at z=2.50 to avoid clipping)
    # =========================================================================
    add_cad_text("Lbl_MB", "MASTER BEDROOM\n13'-3\" x 13'-3\" [NIRUTHI / SW]", 2.2, 2.8, z=2.50, size=0.22, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_AttBath", "ATT. BATH\n6'-3\" x 6'-8\"\n[PRIVATE]", 1.15, 5.1, z=2.50, size=0.17, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_ComBath", "COMMON BATH\n6'-3\" x 6'-8\"\n[SHIELDED DOOR]", 1.15, 7.1, z=2.50, size=0.17, color=(0.1, 0.4, 0.2, 1.0), collection=col)
    add_cad_text("Lbl_Lobby", "PRIVATE LOBBY\n5'-7\" WIDE GALLERY\n(DIRECT ROOM ACCESS)", 2.95, 5.0, z=2.50, size=0.15, color=(0.15, 0.25, 0.45, 1.0), collection=col)
    
    if is_owner_level:
        add_cad_text("Lbl_Office", "HOME OFFICE / STUDY\n12'-6\" x 12'-7\" [NORTH VIEW]\n(Direct Interior + Balcony Doors)", 2.0, 11.2, z=2.50, size=0.18, color=(0.08, 0.25, 0.60, 1.0), collection=col)
        add_cad_text("Lbl_Bed2", "BEDROOM 2 (GUEST/KIDS)\n11'-6\" x 12'-7\" [NORTH VIEW]\n(Direct Living + Balcony Doors)", 5.5, 11.2, z=2.50, size=0.18, color=COLOR_TEXT, collection=col)
        add_cad_text("Lbl_Mallanna", "MALLANNA TEMPLE ROOM\n8'-4\" x 8'-0\" [WEST DOOR]\n(Faces North | Detached)", 8.6, 6.1, z=2.50, size=0.17, color=(0.85, 0.45, 0.05, 1.0), collection=col)
    else:
        add_cad_text("Lbl_B2", "BEDROOM 2 (VAYU / NW)\n12'-6\" x 12'-7\" [GARDEN VIEW]\n(Direct Interior + Balcony Doors)", 2.0, 11.2, z=2.50, size=0.18, color=COLOR_TEXT, collection=col)
        add_cad_text("Lbl_B3", "BEDROOM 3 (NORTH)\n11'-6\" x 12'-7\" [GARDEN VIEW]\n(Direct Living + Balcony Doors)", 5.5, 11.2, z=2.50, size=0.18, color=COLOR_TEXT, collection=col)
        add_cad_text("Lbl_Lounge", "FAMILY LOUNGE / STUDY\n12'-4\" x 12'-8\" [EAST MORNING VIEW]", 9.3, 6.4, z=2.50, size=0.19, color=(0.15, 0.35, 0.60, 1.0), collection=col)
        
    add_cad_text("Lbl_Living", "GRAND LIVING HALL\n18'-0\" x 14'-0\" (BRAHMASTHANA)\n[NO EXPOSED COLUMNS]", 5.6, 6.7, z=2.50, size=0.20, color=(0.05, 0.40, 0.28, 1.0), collection=col)
    add_cad_text("Lbl_Dining", "DINING AREA\n11'-6\" x 13'-3\"", 5.6, 2.5, z=2.50, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kitchen", "MODULAR KITCHEN\n12'-4\" x 13'-3\" [AGNEYA / SE]\n(East Hob | Independent Utility via Lobby)", 9.3, 2.2, z=2.50, size=0.19, color=(0.70, 0.25, 0.08, 1.0), collection=col)
    add_cad_text("Lbl_Utility", "UTILITY BALCONY\n(Out-of-House)", PLINTH_W + 0.7, 2.4, z=2.50, size=0.18, rot_z=math.radians(-90), color=COLOR_TEXT, collection=col)
    
    add_cad_text("Lbl_DailyPooja", "DAILY POOJA\n4'x7'6\" [WEST DOOR]\n(Faces East)", 7.9, 9.5, z=2.50, size=0.16, color=(0.85, 0.45, 0.05, 1.0), collection=col)
    add_cad_text("Lbl_Ishanya", "OPEN ISHANYA (NE) SITOUT\n12'-6\" x 8'-0\" [OPEN TO SKY]\n(Morning Sunlight Corridor)", 9.8, 10.2, z=2.50, size=0.18, color=(0.05, 0.40, 0.65, 1.0), collection=col)
    add_cad_text("Lbl_Simhadwaram", "SIMHADWARAM (MAIN ENTRANCE)\nNORTH-NORTH-EAST (NNE)\n(Arrive from Covered Promenade)", 7.3, PLINTH_D + 0.38, z=2.50, size=0.16, color=(0.04, 0.48, 0.20, 1.0), collection=col)
    add_cad_text("Lbl_Perimeter", "CONTINUOUS 360° CANTILEVER WALK-AROUND SLAB GALLERY", 5.6, PLINTH_D + 0.82, z=2.50, size=0.16, color=(0.10, 0.28, 0.48, 1.0), collection=col)

    png_name = "second_floor_owner_2d.png" if is_owner_level else "first_floor_brother_2d.png"
    scene.render.filepath = str(OUTPUT_DIR / png_name)
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {png_name}")

def main():
    print("="*70)
    print("STARTING CIVIL ARCHITECTURAL 2D CAD ENGINE FOR PROPERTY 2")
    print("="*70)
    
    # 1. Level 0 Ground Floor Stilt & Site Plan
    build_ground_stilt()
    
    # 2. Level 1 First Floor: Brother's Full 3 BHK Residence
    build_upper_floor(is_owner_level=False)
    
    # 3. Level 2 Second Floor: Owner's 2 BHK + Office + Mallanna Shrine
    build_upper_floor(is_owner_level=True)
    
    # Save Master 3D Blend file
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_FILE))
    print(f"CAD Master .blend saved to: {BLEND_FILE}")
    print("="*70)
    print("ALL 3 FLOORS SUCCESSFULLY COMPILED & RENDERED TO HIGH-RES 2D PNG")
    print("="*70)

if __name__ == "__main__":
    main()
