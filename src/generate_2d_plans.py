"""
Civil Engineering & Vaastu-Compliant 2D Architectural CAD Engine for Property 2 (54' x 66' Plot)
Automates Ground Floor (Entire Plot 54'x66' + Plinth 37'x40' + Setbacks + Gardens + Parking)
and Upper Floors (L1 Brother 2BHK, L2 Owner Residence + Office + Dual Pooja + Open Ishanya NE).
Strictly compliant with Telugu / Telangana Vaastu Shastra and Civil Engineering Standards.
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
# East = 54' - (8' + 37') = 9'-0" (2.7432m) -> East > West (PASS)
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

# 16 RCC Column Grid Intersections (4x4)
GRID_X = [0.115, 3.810, 7.315, PLINTH_W - 0.115]
GRID_Y = [0.115, 4.064, 8.128, PLINTH_D - 0.115]

# Professional CAD Color Palette (RGBA)
COLOR_SLAB = (0.97, 0.97, 0.98, 1.0)
COLOR_PLOT_BG = (0.96, 0.97, 0.98, 1.0)
COLOR_COMPOUND = (0.22, 0.27, 0.35, 1.0)       # Dark slate compound wall
COLOR_EXT_WALL = (0.16, 0.20, 0.27, 1.0)       # Charcoal slate #293345
COLOR_INT_WALL = (0.28, 0.33, 0.42, 1.0)       # Medium slate #47546B
COLOR_COLUMN = (0.05, 0.07, 0.10, 1.0)         # Deep black RCC column
COLOR_DOOR = (0.05, 0.58, 0.40, 1.0)           # Emerald green #0D9488
COLOR_WINDOW = (0.12, 0.45, 0.88, 1.0)         # Glazing blue #1E40AF
COLOR_FURNITURE = (0.68, 0.58, 0.48, 1.0)      # Muted teak millwork
COLOR_CUPBOARD = (0.82, 0.72, 0.60, 1.0)       # Built-in wardrobe / cupboard
COLOR_BED = (0.25, 0.45, 0.75, 1.0)            # Navy upholstery
COLOR_KITCHEN = (0.15, 0.16, 0.18, 1.0)        # Black galaxy granite
COLOR_POOJA = (0.88, 0.62, 0.12, 1.0)          # Sacred brass / gold
COLOR_TEXT = (0.08, 0.10, 0.14, 1.0)           # Dark charcoal text
COLOR_DIM = (0.35, 0.40, 0.48, 1.0)            # Dimension string grey
COLOR_GRID = (0.60, 0.65, 0.72, 1.0)           # Column grid line grey
COLOR_BUBBLE = (0.92, 0.94, 0.97, 1.0)         # Grid bubble background
COLOR_PAVILION = (0.94, 0.92, 0.86, 1.0)       # Pavilion slab
COLOR_PARKING = (0.88, 0.92, 0.96, 1.0)        # Stilt parking bay
COLOR_DRIVEWAY = (0.92, 0.93, 0.95, 1.0)       # Paved driveway
COLOR_GARDEN = (0.82, 0.93, 0.82, 1.0)         # Landscaped lawn green
COLOR_BALCONY = (0.91, 0.94, 0.98, 1.0)        # Open balcony slab
COLOR_ROAD = (0.89, 0.91, 0.94, 1.0)           # Asphalt road tone

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

def add_cad_text(name, text, x, y, z=0.92, size=0.22, align_x='CENTER', align_y='CENTER', rot_z=0.0, color=COLOR_TEXT, collection=None):
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
        else:
            px = hinge_x + width * math.cos(rad)
            py = hinge_y - width * math.sin(rad)
        pts.append((px, py, 0.02))
        
    polyline.points.add(len(pts) - 1)
    for idx, (px, py, pz) in enumerate(pts):
        polyline.points[idx].co = (px, py, pz, 1.0)
        
    curve_obj = bpy.data.objects.new(f"{name}_ArcObj", curve_data)
    curve_obj.data.materials.append(mat)
    curve_obj.color = COLOR_DOOR
    if collection:
        collection.objects.link(curve_obj)
    else:
        bpy.context.scene.collection.objects.link(curve_obj)

def create_window_2d(name, x0, y0, x1, y1, mat=None, collection=None):
    mat = mat or get_or_create_material("Mat_Window", COLOR_WINDOW)
    create_box(f"{name}_Sill", x0, y0, x1, y1, 0, WALL_H * 0.35, mat, collection)
    mid_x = (x0 + x1) / 2.0
    mid_y = (y0 + y1) / 2.0
    if abs(x1 - x0) > abs(y1 - y0):
        create_box(f"{name}_Glass", x0, mid_y - 0.02, x1, mid_y + 0.02, 0, WALL_H, mat, collection)
    else:
        create_box(f"{name}_Glass", mid_x - 0.02, y0, mid_x + 0.02, y1, 0, WALL_H, mat, collection)

def add_columns(collection):
    mat_col = get_or_create_material("Mat_Column", COLOR_COLUMN)
    for ix, cx in enumerate(GRID_X):
        for iy, cy in enumerate(GRID_Y):
            create_box(f"Col_{ix+1}_{chr(65+iy)}", cx - COL_W/2, cy - COL_D/2, cx + COL_W/2, cy + COL_D/2, 0, WALL_H + 0.08, mat_col, collection)

def add_external_vertical_core(collection):
    """External stairs & 6-PAX lift located in NW (Vayu) Zone outside the home envelope."""
    mat_core = get_or_create_material("Mat_Core", (0.35, 0.30, 0.45, 1.0))
    mat_tread = get_or_create_material("Mat_Tread", (0.75, 0.77, 0.82, 1.0))
    mat_lift_cab = get_or_create_material("Mat_LiftCab", (0.88, 0.88, 0.92, 1.0))
    mat_ext = get_or_create_material("Mat_ExtWall", COLOR_EXT_WALL)

    create_box("Core_Landing_Slab", -2.40, 6.0, 0.0, 12.2, -0.05, 0, mat_core, collection)
    create_box("Ext_Stair_Base", -2.35, 6.2, -0.25, 9.5, 0, 0.05, mat_tread, collection)
    create_box("Stair_Mid_Landing", -2.35, 6.2, -0.25, 7.3, 0, 0.08, mat_tread, collection)
    create_box("Stair_Divider", -1.35, 7.3, -1.25, 9.5, 0, WALL_H * 0.8, mat_core, collection)
    for i in range(1, 7):
        ty = 7.3 + i * (2.2 / 7.0)
        create_box(f"Tread_Up_{i}", -2.35, ty - 0.015, -1.40, ty + 0.015, 0, 0.06, mat_tread, collection)
        create_box(f"Tread_Dn_{i}", -1.20, ty - 0.015, -0.25, ty + 0.015, 0, 0.06, mat_tread, collection)

    create_box("Lift_Wall_S", -2.3, 9.8, -0.4, 10.0, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Wall_N", -2.3, 11.7, -0.4, 11.9, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Wall_W", -2.3, 10.0, -2.1, 11.7, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Wall_E", -0.6, 10.0, -0.4, 11.7, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Cab", -1.95, 10.15, -0.75, 11.55, 0, 0.05, mat_lift_cab, collection)
    create_box("Core_Rail_W", -2.40, 6.0, -2.35, 12.2, 0, WALL_H * 0.9, mat_core, collection)

def add_title_block(sheet_title, collection, is_ground=False):
    """Engineering Title Block and Legend in right margin."""
    mat_tb = get_or_create_material("Mat_TitleBlock", (0.95, 0.96, 0.98, 1.0))
    mat_border = get_or_create_material("Mat_TBBorder", (0.20, 0.25, 0.35, 1.0))
    
    bx0 = PLOT_X1 + 1.2 if is_ground else PLINTH_W + 1.2
    bx1 = bx0 + 5.8
    by0 = -4.5
    by1 = 3.5
    
    create_box("TB_BG", bx0, by0, bx1, by1, 0, 0.02, mat_tb, collection)
    create_box("TB_Border_Top", bx0, by1 - 0.03, bx1, by1, 0, 0.03, mat_border, collection)
    create_box("TB_Border_Bot", bx0, by0, bx1, by0 + 0.03, 0, 0.03, mat_border, collection)
    create_box("TB_Border_L", bx0, by0, bx0 + 0.03, by1, 0, 0.03, mat_border, collection)
    create_box("TB_Border_R", bx1 - 0.03, by0, bx1, by1, 0, 0.03, mat_border, collection)
    
    cx = (bx0 + bx1) / 2.0
    add_cad_text("TB_H1", "PROPERTY 2 RESIDENCE", cx, 2.9, size=0.30, color=(0.1, 0.15, 0.25, 1.0), collection=collection)
    add_cad_text("TB_H2", sheet_title.upper(), cx, 2.4, size=0.24, color=(0.05, 0.45, 0.35, 1.0), collection=collection)
    add_cad_text("TB_P1", "PLOT: 54'-0\" x 66'-0\" [3,564 SQ.FT]", cx, 1.9, size=0.19, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P2", "PLINTH: 37'-0\" x 40'-0\" [1,480 SQ.FT]", cx, 1.55, size=0.19, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P3", "SETBACKS: N:17' E:9' S:9' W:8' (VAASTU)", cx, 1.20, size=0.18, color=(0.1, 0.5, 0.2, 1.0), collection=collection)
    add_cad_text("TB_P4", "CORE: EXTERNAL NW STAIRS & 6-PAX LIFT", cx, 0.85, size=0.18, color=(0.15, 0.35, 0.65, 1.0), collection=collection)
    add_cad_text("TB_P5", "VAASTU: TELUGU / TELANGANA COMPLIANT", cx, 0.50, size=0.18, color=(0.75, 0.40, 0.05, 1.0), collection=collection)
    add_cad_text("TB_P6", "ISHANYA: OPEN SITOUT TERRACE (NE)", cx, 0.15, size=0.18, color=(0.05, 0.45, 0.35, 1.0), collection=collection)
    add_cad_text("TB_P7", "OFFICE: NORTH FACING (GARDEN VIEW)", cx, -0.20, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P8", "BATHS: SPACIOUS 6'0\"x8'6\" (WET/DRY)", cx, -0.55, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P9", "UTILITY: OUT-OF-HOUSE WASH BALCONY", cx, -0.90, size=0.18, color=COLOR_TEXT, collection=collection)
    
    add_cad_text("TB_Leg1", "DOORS: D1: 3'6\"x7' | D2: 3'0\"x7' | D3: 2'6\"x7'", cx, -1.6, size=0.15, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_Leg2", "WINDOWS: W1: 5'0\"x4'6\" | W2: 4'0\"x4'6\" | V1: 2'0\"x2'0\"", cx, -1.95, size=0.15, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_Leg3", "MILLWORK: WARDROBES, OFFICE DESK, TV UNIT, SOFAS", cx, -2.3, size=0.14, color=COLOR_DIM, collection=collection)

def setup_scene(scene_name, is_ground=False):
    if scene_name in bpy.data.scenes:
        scene = bpy.data.scenes[scene_name]
    else:
        scene = bpy.data.scenes.new(name=scene_name)
    
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.light = 'FLAT'
    scene.display.shading.color_type = 'OBJECT'
    scene.render.resolution_x = 2800
    scene.render.resolution_y = 2200
    scene.render.resolution_percentage = 100
    
    cam_name = f"Cam_{scene_name}"
    if cam_name in bpy.data.cameras:
        cam_data = bpy.data.cameras[cam_name]
    else:
        cam_data = bpy.data.cameras.new(cam_name)
    
    cam_data.type = 'ORTHO'
    if is_ground:
        cam_data.ortho_scale = 32.0
        cam_x = (PLOT_X0 + PLOT_X1) / 2.0 + 2.5
        cam_y = (PLOT_Y0 + PLOT_Y1) / 2.0
    else:
        cam_data.ortho_scale = 24.0
        cam_x = PLINTH_W / 2.0 + 1.0
        cam_y = PLINTH_D / 2.0 - 0.2
        
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)
        
    cam_obj.location = (cam_x, cam_y, 30.0)
    cam_obj.rotation_euler = (0, 0, 0)
    scene.camera = cam_obj
    return scene

# =============================================================================
# SCENE 1: GROUND FLOOR — ENTIRE PLOT (54'x66') + BUILT-UP PLINTH (37'x40')
# =============================================================================
def build_ground_floor_entire_plot():
    scene = setup_scene("Ground_Stilt_Entire_Plot", is_ground=True)
    bpy.context.window.scene = scene
    col = scene.collection
    
    mat_plot = get_or_create_material("Mat_PlotBG", COLOR_PLOT_BG)
    mat_compound = get_or_create_material("Mat_CompoundWall", COLOR_COMPOUND)
    mat_slab = get_or_create_material("Mat_Slab", COLOR_SLAB)
    mat_pavilion = get_or_create_material("Mat_Pavilion", COLOR_PAVILION)
    mat_parking = get_or_create_material("Mat_Parking", COLOR_PARKING)
    mat_driveway = get_or_create_material("Mat_Driveway", COLOR_DRIVEWAY)
    mat_garden = get_or_create_material("Mat_Garden", COLOR_GARDEN)
    mat_road = get_or_create_material("Mat_Road", COLOR_ROAD)
    mat_dim = get_or_create_material("Mat_DimLine", COLOR_DIM)
    
    # 1. Roads (West 30' and South 30')
    create_box("Road_West", PLOT_X0 - 9.14, PLOT_Y0 - 9.14, PLOT_X0, PLOT_Y1 + 3.0, -0.25, -0.10, mat_road, col)
    create_box("Road_South", PLOT_X0 - 9.14, PLOT_Y0 - 9.14, PLOT_X1 + 3.0, PLOT_Y0, -0.25, -0.10, mat_road, col)
    add_cad_text("Road_West_Lbl", "30'-0\" WIDE WEST ROAD (PRIMARY ACCESS & MAIN GATES)", PLOT_X0 - 4.5, (PLOT_Y0 + PLOT_Y1)/2.0, size=0.45, rot_z=math.radians(90), color=(0.15, 0.25, 0.45, 1.0), collection=col)
    add_cad_text("Road_South_Lbl", "30'-0\" WIDE SOUTH ROAD (SECONDARY CORNER ACCESS)", (PLOT_X0 + PLOT_X1)/2.0, PLOT_Y0 - 4.5, size=0.45, color=(0.15, 0.25, 0.45, 1.0), collection=col)

    # 2. Entire Plot Base (54' x 66')
    create_box("Plot_Base_Slab", PLOT_X0, PLOT_Y0, PLOT_X1, PLOT_Y1, -0.12, 0, mat_plot, col)

    # 3. Gardens & Paved Driveways
    create_box("Garden_North_Lawn", PLOT_X0 + COMPOUND_WALL_THICK, PLINTH_D, PLOT_X1 - COMPOUND_WALL_THICK, PLOT_Y1 - COMPOUND_WALL_THICK, 0, 0.03, mat_garden, col)
    create_box("Garden_East_Lawn", PLINTH_W, PLOT_Y0 + COMPOUND_WALL_THICK, PLOT_X1 - COMPOUND_WALL_THICK, PLINTH_D, 0, 0.03, mat_garden, col)
    create_box("Garden_South_Setback", 0, PLOT_Y0 + COMPOUND_WALL_THICK, PLINTH_W, 0, 0, 0.02, mat_garden, col)
    create_box("Driveway_West", PLOT_X0 + COMPOUND_WALL_THICK, PLOT_Y0 + COMPOUND_WALL_THICK, 0, PLINTH_D, 0, 0.02, mat_driveway, col)

    # 4. Compound Boundary Wall with Gates
    cw = COMPOUND_WALL_THICK
    create_box("CW_North", PLOT_X0, PLOT_Y1 - cw, PLOT_X1, PLOT_Y1, 0, WALL_H, mat_compound, col)
    create_box("CW_East", PLOT_X1 - cw, PLOT_Y0, PLOT_X1, PLOT_Y1, 0, WALL_H, mat_compound, col)
    create_box("CW_South_1", PLOT_X0, PLOT_Y0, 7.5, PLOT_Y0 + cw, 0, WALL_H, mat_compound, col)
    create_door_2d("Gate_South", 7.5, PLOT_Y0 + cw, 3.5, 90, 'E', mat_compound, col)
    create_box("CW_South_2", 11.0, PLOT_Y0, PLOT_X1, PLOT_Y0 + cw, 0, WALL_H, mat_compound, col)
    create_box("CW_West_1", PLOT_X0, PLOT_Y0, PLOT_X0 + cw, 8.5, 0, WALL_H, mat_compound, col)
    create_door_2d("Gate_Pedestrian", PLOT_X0 + cw, 8.5, 1.2, 90, 'N', mat_compound, col)
    create_box("CW_West_2", PLOT_X0, 9.7, PLOT_X0 + cw, 12.0, 0, WALL_H, mat_compound, col)
    create_door_2d("Gate_Vehicle_Main", PLOT_X0 + cw, 12.0, 4.5, 90, 'N', mat_compound, col)
    create_box("CW_West_3", PLOT_X0, 16.5, PLOT_X0 + cw, PLOT_Y1, 0, WALL_H, mat_compound, col)

    # 5. Built-up Plinth (37' x 40' = 1,480 sq ft)
    create_box("Plinth_Slab", 0, 0, PLINTH_W, PLINTH_D, 0, 0.15, mat_slab, col)
    create_box("Plinth_Curb_S", 0, 0, PLINTH_W, 0.15, 0.15, 0.35, mat_compound, col)
    create_box("Plinth_Curb_E", PLINTH_W - 0.15, 0, PLINTH_W, PLINTH_D, 0.15, 0.35, mat_compound, col)
    create_box("Plinth_Curb_N", 0, PLINTH_D - 0.15, PLINTH_W, PLINTH_D, 0.15, 0.35, mat_compound, col)
    create_box("Plinth_Curb_W", 0, 0, 0.15, PLINTH_D, 0.15, 0.35, mat_compound, col)

    # 6. Sheltered Function Pavilion (750 sq ft)
    create_box("Pavilion_Area", 0, 0, PLINTH_W, 6.2, 0.15, 0.20, mat_pavilion, col)

    # 7. Parking (Car + 4 Bikes)
    create_box("Car_Stall", 3.8, PLINTH_D - 5.8, 6.6, PLINTH_D - 0.3, 0.15, 0.18, mat_parking, col)
    create_box("Car_Body_3D", 4.1, PLINTH_D - 5.5, 6.3, PLINTH_D - 0.7, 0.18, 0.65, mat_parking, col)
    create_box("Bike_Stall_1", 7.0, PLINTH_D - 3.0, 9.5, PLINTH_D - 0.5, 0.15, 0.18, mat_parking, col)
    create_box("Bike_Stall_2", 7.0, PLINTH_D - 5.6, 9.5, PLINTH_D - 3.1, 0.15, 0.18, mat_parking, col)

    # 8. External Vertical Core & 16 Columns
    add_external_vertical_core(col)
    add_columns(col)

    # 9. Plot & Plinth Dual Dimensions
    # South Plot Width (54'-0")
    create_box("Dim_Plot_S", PLOT_X0, PLOT_Y0 - 1.8, PLOT_X1, PLOT_Y0 - 1.77, 0, 0.03, mat_dim, col)
    add_cad_text("Dim_Plot_S_Text", "54'-0\" [16.46m] TOTAL PLOT WIDTH (EAST-WEST)", (PLOT_X0 + PLOT_X1)/2.0, PLOT_Y0 - 2.3, size=0.36, color=(0.1, 0.15, 0.25, 1.0), collection=col)

    # West Plot Depth (66'-0")
    create_box("Dim_Plot_W", PLOT_X0 - 1.8, PLOT_Y0, PLOT_X0 - 1.77, PLOT_Y1, 0, 0.03, mat_dim, col)
    add_cad_text("Dim_Plot_W_Text", "66'-0\" [20.12m] TOTAL PLOT DEPTH (NORTH-SOUTH)", PLOT_X0 - 2.4, (PLOT_Y0 + PLOT_Y1)/2.0, size=0.36, rot_z=math.radians(90), color=(0.1, 0.15, 0.25, 1.0), collection=col)

    # Plinth Width & Depth
    create_box("Dim_Plinth_S", 0, -1.0, PLINTH_W, -0.98, 0, 0.03, mat_dim, col)
    add_cad_text("Dim_Plinth_S_Text", "37'-0\" [11.28m] BUILT-UP PLINTH WIDTH", PLINTH_W / 2.0, -1.4, size=0.28, color=(0.05, 0.45, 0.35, 1.0), collection=col)
    create_box("Dim_Plinth_W", -1.0, 0, -0.98, PLINTH_D, 0, 0.03, mat_dim, col)
    add_cad_text("Dim_Plinth_W_Text", "40'-0\" [12.19m] BUILT-UP PLINTH DEPTH", -1.4, PLINTH_D / 2.0, size=0.28, rot_z=math.radians(90), color=(0.05, 0.45, 0.35, 1.0), collection=col)

    # Setback Callouts
    add_cad_text("Setback_W_Lbl", "WEST SETBACK: 8'-0\" [2.44m]", (PLOT_X0 + 0)/2.0, -0.5, size=0.20, color=(0.7, 0.3, 0.1, 1.0), collection=col)
    add_cad_text("Setback_S_Lbl", "SOUTH SETBACK: 9'-0\" [2.74m]", PLINTH_W / 2.0, (PLOT_Y0 + 0)/2.0, size=0.20, color=(0.7, 0.3, 0.1, 1.0), collection=col)
    add_cad_text("Setback_E_Lbl", "EAST SETBACK: 9'-0\" [2.74m] (GARDEN)", (PLINTH_W + PLOT_X1)/2.0, 6.0, size=0.22, rot_z=math.radians(-90), color=(0.1, 0.5, 0.2, 1.0), collection=col)
    add_cad_text("Setback_N_Lbl", "NORTH FRONT GARDEN SETBACK: 17'-0\" [5.18m] (OPEN & LIGHT)", (PLOT_X0 + PLOT_X1)/2.0, (PLINTH_D + PLOT_Y1)/2.0 + 0.5, size=0.30, color=(0.1, 0.5, 0.2, 1.0), collection=col)

    # Labels & Title Block
    add_cad_text("Lbl_Pavilion_1", "SHELTERED OPEN FUNCTION PAVILION", 5.6, 3.4, z=1.1, size=0.36, color=(0.1, 0.2, 0.3, 1.0), collection=col)
    add_cad_text("Lbl_Pavilion_2", "37'-0\" x 20'-4\" [11.28m x 6.20m] | 750 SQ.FT", 5.6, 2.7, z=1.1, size=0.26, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Pavilion_3", "(Family Celebrations, Festival Pandal, Open Gathering)", 5.6, 2.1, z=1.1, size=0.22, color=COLOR_DIM, collection=col)

    add_cad_text("Lbl_Car", "COVERED CAR PARKING\n9'-0\" x 18'-0\" [SEDAN/SUV]", 5.2, PLINTH_D - 3.0, z=1.1, size=0.24, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Bikes", "2-WHEELER PARKING\n(4 MOTORCYCLES)", 8.25, PLINTH_D - 3.0, z=1.1, size=0.22, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Stairs", "EXTERNAL STAIRS\n7'3\"x11'0\" [NW VAYU]", -1.35, 7.8, z=1.1, size=0.20, rot_z=math.radians(90), color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Lift", "6-PAX LIFT\n1.6m x 1.6m", -1.35, 10.8, z=1.1, size=0.20, rot_z=math.radians(90), color=(0.1, 0.15, 0.25, 1.0), collection=col)

    add_title_block("Ground Stilt, Parking, Plot & Gardens", col, is_ground=True)

    scene.render.filepath = str(OUTPUT_DIR / "ground_stilt_2d.png")
    bpy.ops.render.render(write_still=True)
    print("Rendered: ground_stilt_2d.png (Entire Plot 54'x66' + Plinth 37'x40')")

# =============================================================================
# SCENE 2: FIRST FLOOR — BROTHER'S 2BHK RESIDENCE (+3.00m)
# =============================================================================
def build_first_floor_brother():
    scene = setup_scene("First_Floor_Brother", is_ground=False)
    bpy.context.window.scene = scene
    col = scene.collection
    
    mat_slab = get_or_create_material("Mat_Slab", COLOR_SLAB)
    mat_ext = get_or_create_material("Mat_ExtWall", COLOR_EXT_WALL)
    mat_int = get_or_create_material("Mat_IntWall", COLOR_INT_WALL)
    mat_bed = get_or_create_material("Mat_Bed", COLOR_BED)
    mat_kit = get_or_create_material("Mat_Kitchen", COLOR_KITCHEN)
    mat_furn = get_or_create_material("Mat_Furniture", COLOR_FURNITURE)
    mat_cupboard = get_or_create_material("Mat_Cupboard", COLOR_CUPBOARD)
    mat_pooja = get_or_create_material("Mat_Pooja", COLOR_POOJA)
    mat_balcony = get_or_create_material("Mat_Balcony", COLOR_BALCONY)
    
    # Base Slab & Columns
    create_box("Floor1_Slab", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_slab, col)
    add_columns(col)
    add_external_vertical_core(col)
    
    # 3 Balconies & External Utility
    create_box("Balcony_North_Slab", 3.81, PLINTH_D, 7.31, PLINTH_D + 1.30, 0, 0.05, mat_balcony, col)
    create_box("Balcony_North_Rail", 3.81, PLINTH_D + 1.25, 7.31, PLINTH_D + 1.30, 0, WALL_H * 0.9, mat_int, col)
    create_box("Balcony_East_Slab", 7.31, 8.5, PLINTH_W, PLINTH_D, 0, 0.05, mat_balcony, col)
    create_box("Balcony_East_Rail_N", 7.31, PLINTH_D - 0.1, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    create_box("Balcony_East_Rail_E", PLINTH_W - 0.1, 8.5, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    create_box("Balcony_South_Slab", 0, -1.2, 3.81, 0, 0, 0.05, mat_balcony, col)
    create_box("Balcony_South_Rail", 0, -1.2, 3.81, -1.15, 0, WALL_H * 0.9, mat_int, col)
    create_box("Utility_East_Slab", PLINTH_W, 0, PLINTH_W + 1.4, 3.5, 0, 0.05, mat_balcony, col)
    create_box("Utility_East_Rail", PLINTH_W + 1.35, 0, PLINTH_W + 1.4, 3.5, 0, WALL_H * 0.9, mat_int, col)

    # Exterior Walls
    create_box("Ext_S_1", 0, 0, 1.2, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_MB_South_Balcony", 1.2, EXT_WALL_THICK, 0.90, 90, 'S', None, col)
    create_box("Ext_S_2", 2.1, 0, 3.81, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_box("Ext_S_3", 3.81, 0, 7.31, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_box("Ext_S_4", 7.31, 0, PLINTH_W, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    create_box("Ext_E_1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 1.2, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_Kit_Utility", PLINTH_W - EXT_WALL_THICK, 1.2, 0.85, 90, 'E', None, col)
    create_box("Ext_E_2", PLINTH_W - EXT_WALL_THICK, 2.05, PLINTH_W, 3.8, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Kit_E", PLINTH_W - EXT_WALL_THICK, 2.2, PLINTH_W, 3.4, None, col)
    create_box("Ext_E_3", PLINTH_W - EXT_WALL_THICK, 3.8, PLINTH_W, 5.0, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Liv_E", PLINTH_W - EXT_WALL_THICK, 5.0, PLINTH_W, 7.2, None, col)
    create_box("Ext_E_4", PLINTH_W - EXT_WALL_THICK, 7.2, PLINTH_W, 8.5, 0, WALL_H, mat_ext, col)

    create_box("Ext_N_W1", 0, PLINTH_D - EXT_WALL_THICK, 1.5, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_door_2d("Simhadwaram_D1", 1.5, PLINTH_D - EXT_WALL_THICK, 1.05, 90, 'S', None, col)
    create_box("Ext_N_W2", 2.55, PLINTH_D - EXT_WALL_THICK, 3.81, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_box("Ext_N_W3", 3.81, PLINTH_D - EXT_WALL_THICK, 4.8, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_B2_North_Balcony", 4.8, PLINTH_D - EXT_WALL_THICK, 0.90, 90, 'N', None, col)
    create_window_2d("Win_B2_N", 5.8, PLINTH_D - EXT_WALL_THICK, 7.2, PLINTH_D, None, col)
    create_box("Ext_N_W4", 7.2, PLINTH_D - EXT_WALL_THICK, 7.31, PLINTH_D, 0, WALL_H, mat_ext, col)

    create_box("Ext_W_1", 0, EXT_WALL_THICK, EXT_WALL_THICK, 4.06, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_MB_W", 0, 1.5, EXT_WALL_THICK, 3.0, None, col)
    create_box("Ext_W_2", 0, 4.06, EXT_WALL_THICK, 6.7, 0, WALL_H, mat_ext, col)
    create_window_2d("Vent_Baths", 0, 5.0, EXT_WALL_THICK, 5.8, None, col)
    create_box("Ext_W_3", 0, 6.7, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_ext, col)

    # Interior Partitions (4.5")
    create_box("MB_Wall_E", 3.81 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.81 + INT_WALL_THICK/2, 4.06, 0, WALL_H, mat_int, col)
    create_box("MB_Wall_N_1", EXT_WALL_THICK, 4.06 - INT_WALL_THICK/2, 0.5, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_AttBath", 0.5, 4.06, 0.75, 90, 'N', None, col)
    create_box("MB_Wall_N_2", 1.25, 4.06 - INT_WALL_THICK/2, 2.7, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_MB", 2.7, 4.06, 0.90, 90, 'S', None, col)
    create_box("MB_Wall_N_3", 3.6, 4.06 - INT_WALL_THICK/2, 3.81, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    create_box("Bath_Div_Wall", 1.83 - INT_WALL_THICK/2, 4.06, 1.83 + INT_WALL_THICK/2, 6.66, 0, WALL_H, mat_int, col)
    create_box("Bath_North_Wall", EXT_WALL_THICK, 6.66 - INT_WALL_THICK/2, 3.81, 6.66 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Bath_East_Wall_1", 3.81 - INT_WALL_THICK/2, 4.06, 3.81 + INT_WALL_THICK/2, 5.2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_CommonBath", 3.81, 5.2, 0.75, 90, 'W', None, col)
    create_box("Bath_East_Wall_2", 3.81 - INT_WALL_THICK/2, 5.95, 3.81 + INT_WALL_THICK/2, 6.66, 0, WALL_H, mat_int, col)

    create_box("Kit_Wall_W", 7.31 - INT_WALL_THICK/2, EXT_WALL_THICK, 7.31 + INT_WALL_THICK/2, 2.2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Kit", 7.31, 2.2, 0.90, 90, 'W', None, col)
    create_box("Kit_Wall_W2", 7.31 - INT_WALL_THICK/2, 3.1, 7.31 + INT_WALL_THICK/2, 3.5, 0, WALL_H, mat_int, col)
    create_box("Kit_Wall_N", 7.31, 3.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 3.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    create_box("B2_Wall_W", 3.81 - INT_WALL_THICK/2, 8.5, 3.81 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("B2_Wall_E", 7.31 - INT_WALL_THICK/2, 8.5, 7.31 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("B2_Wall_S_1", 3.81, 8.5 - INT_WALL_THICK/2, 5.0, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_B2", 5.0, 8.5, 0.90, 90, 'N', None, col)
    create_box("B2_Wall_S_2", 5.9, 8.5 - INT_WALL_THICK/2, 7.31, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    create_box("Ishanya_Wall_1", 7.31, 8.5 - INT_WALL_THICK/2, 8.2, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Ishanya_Light", 8.2, 8.5, 1.20, 90, 'E', None, col)
    create_box("Ishanya_Wall_2", 9.4, 8.5 - INT_WALL_THICK/2, 10.0, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Pooja", 10.0, 8.5, 0.80, 90, 'N', None, col)
    create_box("Ishanya_Wall_3", 10.8, 8.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Pooja_Wall_W", 10.0 - INT_WALL_THICK/2, 8.5, 10.0 + INT_WALL_THICK/2, 10.5, 0, WALL_H, mat_int, col)
    create_box("Pooja_Wall_N", 10.0, 10.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 10.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Millwork & Furniture
    create_box("MB_Wardrobe", EXT_WALL_THICK, 0.35, EXT_WALL_THICK + 0.60, 3.8, 0, 1.10, mat_cupboard, col)
    create_box("MB_Bed", 1.4, EXT_WALL_THICK + 0.1, 3.4, EXT_WALL_THICK + 2.1, 0, 0.45, mat_bed, col)
    create_box("MB_Headboard", 1.3, EXT_WALL_THICK, 3.5, EXT_WALL_THICK + 0.1, 0, 0.75, mat_bed, col)
    create_box("MB_TV_Console", 3.81 - INT_WALL_THICK/2 - 0.35, 1.5, 3.81 - INT_WALL_THICK/2, 3.2, 0, 0.60, mat_furn, col)

    create_box("B2_Wardrobe", 3.81 + INT_WALL_THICK/2, 9.2, 3.81 + 0.60, 11.8, 0, 1.10, mat_cupboard, col)
    create_box("B2_Bed", 4.8, PLINTH_D - EXT_WALL_THICK - 2.1, 6.6, PLINTH_D - EXT_WALL_THICK - 0.1, 0, 0.45, mat_bed, col)
    create_box("B2_Study_Desk", 6.2, 8.6, 7.2, 9.4, 0, 0.75, mat_furn, col)

    create_box("Kit_Counter_E", PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK, 3.4, 0, 0.85, mat_kit, col)
    create_box("Kit_Counter_S", 7.4, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK + 0.65, 0, 0.85, mat_kit, col)
    create_box("Kit_Pantry_Cupboard", 7.4, 2.5, 7.9, 3.4, 0, 1.20, mat_cupboard, col)
    create_box("Kit_Stove", PLINTH_W - EXT_WALL_THICK - 0.60, 2.1, PLINTH_W - EXT_WALL_THICK - 0.10, 2.9, 0.86, 0.88, mat_pooja, col)
    create_box("Kit_Sink", PLINTH_W - EXT_WALL_THICK - 0.60, 1.0, PLINTH_W - EXT_WALL_THICK - 0.10, 1.6, 0.86, 0.87, mat_slab, col)

    create_box("Sofa_Main", 4.2, 5.0, 7.0, 5.9, 0, 0.65, mat_bed, col)
    create_box("Sofa_L_Ext", 4.2, 5.9, 5.1, 7.5, 0, 0.65, mat_bed, col)
    create_box("Coffee_Table", 5.5, 6.2, 6.7, 7.2, 0, 0.40, mat_furn, col)
    create_box("Living_TV_Unit", 3.81 + INT_WALL_THICK/2, 4.5, 3.81 + 0.45, 6.5, 0, 1.10, mat_cupboard, col)
    create_box("Dining_Table", 5.0, 2.2, 6.6, 3.6, 0, 0.75, mat_furn, col)

    create_box("Utility_Wash_Machine", PLINTH_W + 0.2, 0.4, PLINTH_W + 0.9, 1.1, 0, 0.85, mat_furn, col)
    create_box("Utility_Sink", PLINTH_W + 0.2, 1.6, PLINTH_W + 0.8, 2.4, 0, 0.75, mat_kit, col)

    add_title_block("First Floor - Brother's 2BHK Residence", col, is_ground=False)

    # Room Labels
    add_cad_text("Lbl_MB_1", "MASTER BEDROOM", 2.0, 3.0, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_MB_2", "12'-6\" x 13'-4\" [3.81m x 4.06m]", 2.0, 2.6, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_MB_3", "[NIRUTHI / SW - HEAVY | BUILT-IN WARDROBE]", 2.0, 2.25, size=0.17, color=(0.6, 0.3, 0.1, 1.0), collection=col)
    add_cad_text("Lbl_AttBath", "SPACIOUS ATT. BATH\n6'0\" x 8'6\" [WET/DRY]", 1.0, 5.4, size=0.18, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_ComBath", "SPACIOUS COM. BATH\n6'0\" x 8'6\" [VARUNA]", 2.8, 5.4, size=0.18, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kit_1", "MODULAR KITCHEN", 9.2, 2.1, size=0.26, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kit_2", "12'-6\" x 11'-6\" [SE AGNEYA]", 9.2, 1.75, size=0.19, color=(0.8, 0.3, 0.05, 1.0), collection=col)
    add_cad_text("Lbl_Util", "OUT-OF-HOUSE UTILITY\nBALCONY (WASH/GAS)", PLINTH_W + 0.7, 2.8, size=0.16, rot_z=math.radians(-90), color=(0.1, 0.3, 0.5, 1.0), collection=col)
    add_cad_text("Lbl_Din", "DINING AREA\n10'-6\" x 11'-6\"", 5.8, 1.5, size=0.22, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Liv_1", "GRAND LIVING HALL", 6.0, 4.4, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Liv_2", "18'-0\" x 14'-0\" [OPEN BRAHMASTHANA]", 6.0, 4.0, size=0.20, color=(0.1, 0.4, 0.3, 1.0), collection=col)
    add_cad_text("Lbl_B2_1", "BEDROOM 2", 5.5, 10.5, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_B2_2", "11'-6\" x 11'-6\" [VAYU/NORTH]", 5.5, 10.1, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Pooja", "POOJA MANDIR\n4'6\" x 6'6\"", 10.5, 9.5, size=0.19, color=(0.85, 0.50, 0.05, 1.0), collection=col)
    add_cad_text("Lbl_Ishanya_1", "OPEN ISHANYA (NE) SITOUT", 8.8, 11.2, size=0.24, color=(0.1, 0.35, 0.7, 1.0), collection=col)
    add_cad_text("Lbl_Ishanya_2", "[LIGHT & OPEN - VAASTU ALIGNED]", 8.8, 10.8, size=0.18, color=(0.05, 0.45, 0.35, 1.0), collection=col)
    add_cad_text("Lbl_Simha", "SIMHADWARAM (D1)\nNORTH-FACING", 2.0, PLINTH_D - 0.7, size=0.19, color=(0.05, 0.55, 0.35, 1.0), collection=col)

    scene.render.filepath = str(OUTPUT_DIR / "first_floor_brother_2d.png")
    bpy.ops.render.render(write_still=True)
    print("Rendered: first_floor_brother_2d.png")

# =============================================================================
# SCENE 3: SECOND FLOOR — OWNER'S RESIDENCE (2BHK + OFFICE + DUAL POOJA)
# =============================================================================
def build_second_floor_owner():
    scene = setup_scene("Second_Floor_Owner", is_ground=False)
    bpy.context.window.scene = scene
    col = scene.collection
    
    mat_slab = get_or_create_material("Mat_Slab", COLOR_SLAB)
    mat_ext = get_or_create_material("Mat_ExtWall", COLOR_EXT_WALL)
    mat_int = get_or_create_material("Mat_IntWall", COLOR_INT_WALL)
    mat_bed = get_or_create_material("Mat_Bed", COLOR_BED)
    mat_kit = get_or_create_material("Mat_Kitchen", COLOR_KITCHEN)
    mat_furn = get_or_create_material("Mat_Furniture", COLOR_FURNITURE)
    mat_cupboard = get_or_create_material("Mat_Cupboard", COLOR_CUPBOARD)
    mat_pooja = get_or_create_material("Mat_Pooja", COLOR_POOJA)
    mat_balcony = get_or_create_material("Mat_Balcony", COLOR_BALCONY)
    
    create_box("Floor2_Slab", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_slab, col)
    add_columns(col)
    add_external_vertical_core(col)
    
    # 3 Balconies & External Utility
    create_box("Balcony_North_Slab", 3.81, PLINTH_D, 7.31, PLINTH_D + 1.30, 0, 0.05, mat_balcony, col)
    create_box("Balcony_North_Rail", 3.81, PLINTH_D + 1.25, 7.31, PLINTH_D + 1.30, 0, WALL_H * 0.9, mat_int, col)
    create_box("Balcony_East_Slab", 7.31, 8.5, PLINTH_W, PLINTH_D, 0, 0.05, mat_balcony, col)
    create_box("Balcony_East_Rail_N", 7.31, PLINTH_D - 0.1, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    create_box("Balcony_East_Rail_E", PLINTH_W - 0.1, 8.5, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    create_box("Balcony_South_Slab", 0, -1.2, 3.81, 0, 0, 0.05, mat_balcony, col)
    create_box("Balcony_South_Rail", 0, -1.2, 3.81, -1.15, 0, WALL_H * 0.9, mat_int, col)
    create_box("Utility_East_Slab", PLINTH_W, 0, PLINTH_W + 1.4, 3.5, 0, 0.05, mat_balcony, col)
    create_box("Utility_East_Rail", PLINTH_W + 1.35, 0, PLINTH_W + 1.4, 3.5, 0, WALL_H * 0.9, mat_int, col)

    # Exterior Walls
    create_box("Ext_S_1", 0, 0, 1.2, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_MB_South_Balcony", 1.2, EXT_WALL_THICK, 0.90, 90, 'S', None, col)
    create_box("Ext_S_2", 2.1, 0, 3.81, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_box("Ext_S_3", 3.81, 0, 7.31, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_box("Ext_S_4", 7.31, 0, PLINTH_W, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    create_box("Ext_E_1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 1.2, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_Kit_Utility", PLINTH_W - EXT_WALL_THICK, 1.2, 0.85, 90, 'E', None, col)
    create_box("Ext_E_2", PLINTH_W - EXT_WALL_THICK, 2.05, PLINTH_W, 3.8, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Kit_E", PLINTH_W - EXT_WALL_THICK, 2.2, PLINTH_W, 3.4, None, col)
    create_box("Ext_E_3", PLINTH_W - EXT_WALL_THICK, 3.8, PLINTH_W, 5.0, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Liv_E", PLINTH_W - EXT_WALL_THICK, 5.0, PLINTH_W, 7.2, None, col)
    create_box("Ext_E_4", PLINTH_W - EXT_WALL_THICK, 7.2, PLINTH_W, 8.5, 0, WALL_H, mat_ext, col)

    create_box("Ext_N_W1", 0, PLINTH_D - EXT_WALL_THICK, 1.5, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_door_2d("Simhadwaram_D1", 1.5, PLINTH_D - EXT_WALL_THICK, 1.05, 90, 'S', None, col)
    create_box("Ext_N_W2", 2.55, PLINTH_D - EXT_WALL_THICK, 3.81, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_box("Ext_N_W3", 3.81, PLINTH_D - EXT_WALL_THICK, 4.3, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Office_North", 4.3, PLINTH_D - EXT_WALL_THICK, 6.2, PLINTH_D, None, col)
    create_box("Ext_N_W4", 6.2, PLINTH_D - EXT_WALL_THICK, 7.31, PLINTH_D, 0, WALL_H, mat_ext, col)

    create_box("Ext_W_1", 0, EXT_WALL_THICK, EXT_WALL_THICK, 4.06, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_MB_W", 0, 1.5, EXT_WALL_THICK, 3.0, None, col)
    create_box("Ext_W_2", 0, 4.06, EXT_WALL_THICK, 6.7, 0, WALL_H, mat_ext, col)
    create_window_2d("Vent_Baths", 0, 5.0, EXT_WALL_THICK, 5.8, None, col)
    create_box("Ext_W_3", 0, 6.7, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_ext, col)

    # Partitions (4.5")
    create_box("MB_Wall_E", 3.81 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.81 + INT_WALL_THICK/2, 4.06, 0, WALL_H, mat_int, col)
    create_box("MB_Wall_N_1", EXT_WALL_THICK, 4.06 - INT_WALL_THICK/2, 0.5, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_AttBath", 0.5, 4.06, 0.75, 90, 'N', None, col)
    create_box("MB_Wall_N_2", 1.25, 4.06 - INT_WALL_THICK/2, 2.7, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_MB", 2.7, 4.06, 0.90, 90, 'S', None, col)
    create_box("MB_Wall_N_3", 3.6, 4.06 - INT_WALL_THICK/2, 3.81, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    create_box("Bath_Div_Wall", 1.83 - INT_WALL_THICK/2, 4.06, 1.83 + INT_WALL_THICK/2, 6.66, 0, WALL_H, mat_int, col)
    create_box("Bath_North_Wall", EXT_WALL_THICK, 6.66 - INT_WALL_THICK/2, 3.81, 6.66 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Bath_East_Wall_1", 3.81 - INT_WALL_THICK/2, 4.06, 3.81 + INT_WALL_THICK/2, 5.2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_CommonBath", 3.81, 5.2, 0.75, 90, 'W', None, col)
    create_box("Bath_East_Wall_2", 3.81 - INT_WALL_THICK/2, 5.95, 3.81 + INT_WALL_THICK/2, 6.66, 0, WALL_H, mat_int, col)

    create_box("Kit_Wall_W", 7.31 - INT_WALL_THICK/2, EXT_WALL_THICK, 7.31 + INT_WALL_THICK/2, 2.2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Kit", 7.31, 2.2, 0.90, 90, 'W', None, col)
    create_box("Kit_Wall_W2", 7.31 - INT_WALL_THICK/2, 3.1, 7.31 + INT_WALL_THICK/2, 3.5, 0, WALL_H, mat_int, col)
    create_box("Kit_Wall_N", 7.31, 3.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 3.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    create_box("Office_Wall_W", 3.81 - INT_WALL_THICK/2, 8.8, 3.81 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("Office_Wall_E", 7.31 - INT_WALL_THICK/2, 8.8, 7.31 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("Office_Wall_S_1", 3.81, 8.8 - INT_WALL_THICK/2, 4.8, 8.8 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Office", 4.8, 8.8, 0.90, 90, 'N', None, col)
    create_box("Office_Wall_S_2", 5.7, 8.8 - INT_WALL_THICK/2, 7.31, 8.8 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    create_box("Pooja_Div_Wall_1", 7.31, 8.5 - INT_WALL_THICK/2, 8.2, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Ishanya_Light", 8.2, 8.5, 1.20, 90, 'E', None, col)
    create_box("Pooja_Div_Wall_2", 9.4, 8.5 - INT_WALL_THICK/2, 10.0, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Mallanna_Pooja", 10.0, 8.5, 0.90, 90, 'N', None, col)
    create_box("Pooja_Div_Wall_3", 10.9, 8.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    create_box("Mallanna_Wall_W", 8.8 - INT_WALL_THICK/2, 5.5, 8.8 + INT_WALL_THICK/2, 8.5, 0, WALL_H, mat_int, col)
    create_box("Mallanna_Wall_S_1", 8.8, 5.5 - INT_WALL_THICK/2, 9.6, 5.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Mallanna_Entry", 9.6, 5.5, 0.90, 90, 'N', None, col)
    create_box("Mallanna_Wall_S_2", 10.5, 5.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 5.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    create_box("Daily_Pooja_Wall_W", 9.4 - INT_WALL_THICK/2, 8.5, 9.4 + INT_WALL_THICK/2, 10.5, 0, WALL_H, mat_int, col)
    create_box("Daily_Pooja_Wall_N", 9.4, 10.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 10.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Daily_Pooja", 9.5, 8.5, 0.80, 90, 'N', None, col)

    # Millwork & Furniture
    create_box("MB_Wardrobe", EXT_WALL_THICK, 0.35, EXT_WALL_THICK + 0.60, 3.8, 0, 1.10, mat_cupboard, col)
    create_box("MB_Bed", 1.4, EXT_WALL_THICK + 0.1, 3.4, EXT_WALL_THICK + 2.1, 0, 0.45, mat_bed, col)
    create_box("MB_Headboard", 1.3, EXT_WALL_THICK, 3.5, EXT_WALL_THICK + 0.1, 0, 0.75, mat_bed, col)
    create_box("MB_TV_Console", 3.81 - INT_WALL_THICK/2 - 0.35, 1.5, 3.81 - INT_WALL_THICK/2, 3.2, 0, 0.60, mat_furn, col)

    create_box("Office_Desk", 4.6, 10.0, 6.4, 10.8, 0, 0.75, mat_furn, col)
    create_box("Office_Cupboard_Wall", 3.81 + INT_WALL_THICK/2, 9.2, 3.81 + 0.55, 11.8, 0, 1.10, mat_cupboard, col)
    create_box("Office_Lounge_Chair", 6.2, 9.2, 7.0, 10.0, 0, 0.60, mat_bed, col)

    create_box("Mallanna_Altar", 9.0, 7.5, PLINTH_W - EXT_WALL_THICK - 0.1, 8.4, 0, 0.65, mat_pooja, col)
    create_box("Mallanna_Prayer_Carpet", 9.0, 5.8, PLINTH_W - EXT_WALL_THICK - 0.2, 7.4, 0, 0.02, mat_pooja, col)

    create_box("Sofa_Main", 4.2, 5.0, 7.0, 5.9, 0, 0.65, mat_bed, col)
    create_box("Sofa_L_Ext", 4.2, 5.9, 5.1, 7.5, 0, 0.65, mat_bed, col)
    create_box("Coffee_Table", 5.5, 6.2, 6.7, 7.2, 0, 0.40, mat_furn, col)
    create_box("Living_TV_Unit", 3.81 + INT_WALL_THICK/2, 4.5, 3.81 + 0.45, 6.5, 0, 1.10, mat_cupboard, col)
    create_box("Dining_Table", 5.0, 2.2, 6.6, 3.6, 0, 0.75, mat_furn, col)

    create_box("Kit_Counter_E", PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK, 3.4, 0, 0.85, mat_kit, col)
    create_box("Kit_Counter_S", 7.4, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK + 0.65, 0, 0.85, mat_kit, col)
    create_box("Kit_Pantry_Cupboard", 7.4, 2.5, 7.9, 3.4, 0, 1.20, mat_cupboard, col)
    create_box("Kit_Stove", PLINTH_W - EXT_WALL_THICK - 0.60, 2.1, PLINTH_W - EXT_WALL_THICK - 0.10, 2.9, 0.86, 0.88, mat_pooja, col)
    create_box("Kit_Sink", PLINTH_W - EXT_WALL_THICK - 0.60, 1.0, PLINTH_W - EXT_WALL_THICK - 0.10, 1.6, 0.86, 0.87, mat_slab, col)
    create_box("Utility_Wash_Machine", PLINTH_W + 0.2, 0.4, PLINTH_W + 0.9, 1.1, 0, 0.85, mat_furn, col)
    create_box("Utility_Sink", PLINTH_W + 0.2, 1.6, PLINTH_W + 0.8, 2.4, 0, 0.75, mat_kit, col)

    add_title_block("Second Floor - Owner's Residence", col, is_ground=False)

    # Labels
    add_cad_text("Lbl_MB_1", "MASTER BEDROOM", 2.0, 3.0, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_MB_2", "12'-6\" x 13'-4\" [3.81m x 4.06m]", 2.0, 2.6, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_MB_3", "[NIRUTHI / SW - HEAVY | BUILT-IN WARDROBE]", 2.0, 2.25, size=0.17, color=(0.6, 0.3, 0.1, 1.0), collection=col)
    add_cad_text("Lbl_AttBath", "SPACIOUS ATT. BATH\n6'0\" x 8'6\" [WET/DRY]", 1.0, 5.4, size=0.18, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_ComBath", "SPACIOUS COM. BATH\n6'0\" x 8'6\" [VARUNA]", 2.8, 5.4, size=0.18, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kit_1", "MODULAR KITCHEN", 9.2, 2.1, size=0.26, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kit_2", "12'-6\" x 11'-6\" [SE AGNEYA]", 9.2, 1.75, size=0.19, color=(0.8, 0.3, 0.05, 1.0), collection=col)
    add_cad_text("Lbl_Util", "OUT-OF-HOUSE UTILITY\nBALCONY (WASH/GAS)", PLINTH_W + 0.7, 2.8, size=0.16, rot_z=math.radians(-90), color=(0.1, 0.3, 0.5, 1.0), collection=col)
    add_cad_text("Lbl_Office_1", "HOME OFFICE / EXECUTIVE STUDY", 5.5, 11.2, size=0.26, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Office_2", "11'-6\" x 11'-0\" [NORTH GARDEN VIEW]", 5.5, 10.8, size=0.19, color=(0.15, 0.35, 0.65, 1.0), collection=col)
    add_cad_text("Lbl_Office_3", "(Unblocked by Core | Executive Millwork)", 5.5, 10.45, size=0.16, color=COLOR_DIM, collection=col)
    add_cad_text("Lbl_Liv_1", "GRAND LIVING HALL", 6.0, 4.4, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Liv_2", "18'-0\" x 14'-0\" [OPEN BRAHMASTHANA]", 6.0, 4.0, size=0.20, color=(0.1, 0.4, 0.3, 1.0), collection=col)
    add_cad_text("Lbl_Mallanna_1", "MALLANNA SHRINE", 9.9, 7.0, size=0.22, color=(0.85, 0.50, 0.05, 1.0), collection=col)
    add_cad_text("Lbl_Mallanna_2", "8'-6\" x 10'-0\" [DETACHED]", 9.9, 6.65, size=0.17, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_DailyPooja", "DAILY POOJA\n5'6\" x 6'6\"", 10.2, 9.5, size=0.19, color=(0.85, 0.50, 0.05, 1.0), collection=col)
    add_cad_text("Lbl_Ishanya_1", "OPEN ISHANYA (NE) SITOUT", 8.8, 11.2, size=0.24, color=(0.1, 0.35, 0.7, 1.0), collection=col)
    add_cad_text("Lbl_Ishanya_2", "[LIGHT & OPEN - VAASTU ALIGNED]", 8.8, 10.8, size=0.18, color=(0.05, 0.45, 0.35, 1.0), collection=col)
    add_cad_text("Lbl_Simha", "SIMHADWARAM (D1)\nNORTH-FACING", 2.0, PLINTH_D - 0.7, size=0.19, color=(0.05, 0.55, 0.35, 1.0), collection=col)

    scene.render.filepath = str(OUTPUT_DIR / "second_floor_owner_2d.png")
    bpy.ops.render.render(write_still=True)
    print("Rendered: second_floor_owner_2d.png")

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    print("Starting Blender Architectural CAD Generation (Full Plot + Plinth)...")
    build_ground_floor_entire_plot()
    build_first_floor_brother()
    build_second_floor_owner()
    
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_FILE))
    print(f"Master Project Saved: {BLEND_FILE}")
