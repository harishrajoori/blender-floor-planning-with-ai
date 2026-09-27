"""
Civil Engineering & Vaastu-Compliant 2D Floor Plan Generator for Property 2 (54' x 66' Plot)
Runs inside Blender (headless or GUI) to produce:
  1. Ground Stilt Floor (Level 0, +0.00m) - Parking + Sheltered Pavilion + Core
  2. First Floor - Brother's 2BHK Residence (Level 1, +3.00m)
  3. Second Floor - Owner's 2BHK + Office + Dual Pooja Suite (Level 2, +6.00m)
Exports high-resolution 2D orthographic plan renders with full CAD annotations,
dimension strings, column grid bubbles, room tags, and master .blend project.
"""

import bpy
import math
import os
from pathlib import Path

# Paths
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BLEND_FILE = OUTPUT_DIR / "property2_engineering_cad.blend"

# Constants (in meters)
# Plinth: 37'-0" (11.2776m) EW x 40'-0" (12.192m) NS
PLINTH_W = 11.2776
PLINTH_D = 12.192
WALL_H = 0.90           # Cut-plane height for 2D architectural section
EXT_WALL_THICK = 0.230  # 9" exterior brick wall
INT_WALL_THICK = 0.115  # 4.5" interior partition wall
CORE_WALL_THICK = 0.200 # 8" RCC core shaft wall
COL_W = 0.230           # 9" column width
COL_D = 0.450           # 18" column depth

# Column Grid Intersections (4x4 = 16 columns)
GRID_X = [0.115, 3.810, 7.315, PLINTH_W - 0.115]
GRID_Y = [0.115, 4.064, 8.128, PLINTH_D - 0.115]

# Professional CAD Color Palette (RGBA)
COLOR_SLAB = (0.97, 0.97, 0.98, 1.0)
COLOR_EXT_WALL = (0.16, 0.20, 0.27, 1.0)       # Charcoal slate #293345
COLOR_INT_WALL = (0.28, 0.33, 0.42, 1.0)       # Medium slate #47546B
COLOR_COLUMN = (0.05, 0.07, 0.10, 1.0)         # Deep black RCC column
COLOR_DOOR = (0.05, 0.58, 0.40, 1.0)           # Emerald green #0D9488
COLOR_WINDOW = (0.12, 0.45, 0.88, 1.0)         # Glazing blue #1E40AF
COLOR_FURNITURE = (0.68, 0.58, 0.48, 1.0)      # Muted teak / millwork
COLOR_BED = (0.25, 0.45, 0.75, 1.0)            # Navy upholstery
COLOR_KITCHEN = (0.15, 0.16, 0.18, 1.0)        # Black galaxy granite
COLOR_POOJA = (0.88, 0.62, 0.12, 1.0)          # Sacred brass / gold
COLOR_TEXT = (0.08, 0.10, 0.14, 1.0)           # Dark charcoal text
COLOR_DIM = (0.35, 0.40, 0.48, 1.0)            # Dimension string grey
COLOR_GRID = (0.60, 0.65, 0.72, 1.0)           # Column grid line grey
COLOR_BUBBLE = (0.92, 0.94, 0.97, 1.0)         # Grid bubble background
COLOR_PAVILION = (0.94, 0.92, 0.86, 1.0)       # Pavilion slab
COLOR_PARKING = (0.88, 0.92, 0.96, 1.0)        # Stilt parking bay

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
        
    leaf = create_box(f"{name}_Leaf", lx - dx/2, ly - dy/2, lx + dx/2, ly + dy/2, 0, WALL_H, mat, collection)
    
    # Swing arc curve
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

def add_dog_legged_stairs(x0, y0, w, d, collection):
    mat_stair = get_or_create_material("Mat_Stair", (0.42, 0.38, 0.50, 1.0))
    mat_tread = get_or_create_material("Mat_Tread", (0.75, 0.77, 0.82, 1.0))
    
    create_box("Stair_Shaft", x0, y0, x0 + w, y0 + d, -0.05, 0, mat_stair, collection)
    mid_landing_d = 1.10
    create_box("Stair_Landing", x0, y0, x0 + w, y0 + mid_landing_d, 0, 0.06, mat_tread, collection)
    
    mid_x = x0 + w / 2.0
    create_box("Stair_Divider", mid_x - 0.05, y0 + mid_landing_d, mid_x + 0.05, y0 + d, 0, WALL_H * 0.85, mat_stair, collection)
    
    tread_run = (d - mid_landing_d) / 8.0
    for i in range(1, 8):
        ty = y0 + mid_landing_d + i * tread_run
        create_box(f"Tread_L_{i}", x0, ty - 0.015, mid_x - 0.06, ty + 0.015, 0, 0.04, mat_tread, collection)
        create_box(f"Tread_R_{i}", mid_x + 0.06, ty - 0.015, x0 + w, ty + 0.015, 0, 0.04, mat_tread, collection)

def add_lift_shaft(x0, y0, w, d, collection):
    mat_core = get_or_create_material("Mat_Core", (0.35, 0.30, 0.45, 1.0))
    mat_cab = get_or_create_material("Mat_LiftCab", (0.88, 0.88, 0.92, 1.0))
    
    create_box("Lift_Wall_S", x0, y0, x0 + w, y0 + 0.20, 0, WALL_H, mat_core, collection)
    create_box("Lift_Wall_N", x0, y0 + d - 0.20, x0 + w, y0 + d, 0, WALL_H, mat_core, collection)
    create_box("Lift_Wall_W", x0, y0 + 0.20, x0 + 0.20, y0 + d - 0.20, 0, WALL_H, mat_core, collection)
    create_box("Lift_Wall_E", x0 + w - 0.20, y0 + 0.20, x0 + w, y0 + d - 0.20, 0, WALL_H, mat_core, collection)
    create_box("Lift_Cab", x0 + 0.35, y0 + 0.35, x0 + w - 0.35, y0 + d - 0.35, 0, 0.05, mat_cab, collection)

def add_column_grids_and_dimensions(collection):
    """Draws professional structural grid lines, bubbles 1-4/A-D, and bay dimensions."""
    mat_grid = get_or_create_material("Mat_GridLine", COLOR_GRID)
    mat_bubble = get_or_create_material("Mat_GridBubble", COLOR_BUBBLE)
    mat_dim = get_or_create_material("Mat_DimLine", COLOR_DIM)
    
    # 1. Vertical Grid Lines (X1, X2, X3, X4)
    for ix, cx in enumerate(GRID_X):
        create_box(f"GridLine_X_{ix+1}", cx - 0.01, -1.8, cx + 0.01, PLINTH_D + 1.8, 0, 0.02, mat_grid, collection)
        create_box(f"Bubble_Top_{ix+1}", cx - 0.35, PLINTH_D + 1.8, cx + 0.35, PLINTH_D + 2.5, 0, 0.04, mat_bubble, collection)
        add_cad_text(f"GridText_Top_{ix+1}", str(ix+1), cx, PLINTH_D + 2.15, size=0.35, color=COLOR_TEXT, collection=collection)
        create_box(f"Bubble_Bot_{ix+1}", cx - 0.35, -2.5, cx + 0.35, -1.8, 0, 0.04, mat_bubble, collection)
        add_cad_text(f"GridText_Bot_{ix+1}", str(ix+1), cx, -2.15, size=0.35, color=COLOR_TEXT, collection=collection)

    # 2. Horizontal Grid Lines (YA, YB, YC, YD)
    labels_y = ['A', 'B', 'C', 'D']
    for iy, cy in enumerate(GRID_Y):
        create_box(f"GridLine_Y_{labels_y[iy]}", -1.8, cy - 0.01, PLINTH_W + 1.8, cy + 0.01, 0, 0.02, mat_grid, collection)
        create_box(f"Bubble_Left_{labels_y[iy]}", -2.5, cy - 0.35, -1.8, cy + 0.35, 0, 0.04, mat_bubble, collection)
        add_cad_text(f"GridText_Left_{labels_y[iy]}", labels_y[iy], -2.15, cy, size=0.35, color=COLOR_TEXT, collection=collection)
        create_box(f"Bubble_Right_{labels_y[iy]}", PLINTH_W + 1.8, cy - 0.35, PLINTH_W + 2.5, cy + 0.35, 0, 0.04, mat_bubble, collection)
        add_cad_text(f"GridText_Right_{labels_y[iy]}", labels_y[iy], PLINTH_W + 2.15, cy, size=0.35, color=COLOR_TEXT, collection=collection)

    # 3. Overall Outer Dimension Strings
    # South Dimension: 37'-0" (11.28m)
    create_box("Dim_Line_S", 0, -1.1, PLINTH_W, -1.08, 0, 0.02, mat_dim, collection)
    create_box("Dim_Tick_S0", -0.15, -1.25, 0.15, -0.95, 0, 0.03, mat_dim, collection)
    create_box("Dim_Tick_S1", PLINTH_W - 0.15, -1.25, PLINTH_W + 0.15, -0.95, 0, 0.03, mat_dim, collection)
    add_cad_text("Dim_Text_S", "37'-0\" [11.28m] OVERALL PLINTH WIDTH", PLINTH_W / 2.0, -1.45, size=0.26, color=COLOR_TEXT, collection=collection)

    # West Dimension: 40'-0" (12.19m)
    create_box("Dim_Line_W", -1.1, 0, -1.08, PLINTH_D, 0, 0.02, mat_dim, collection)
    create_box("Dim_Tick_W0", -1.25, -0.15, -0.95, 0.15, 0, 0.03, mat_dim, collection)
    create_box("Dim_Tick_W1", -1.25, PLINTH_D - 0.15, -0.95, PLINTH_D + 0.15, 0, 0.03, mat_dim, collection)
    add_cad_text("Dim_Text_W", "40'-0\" [12.19m] PLINTH DEPTH", -1.45, PLINTH_D / 2.0, size=0.26, rot_z=math.radians(90), color=COLOR_TEXT, collection=collection)

    # 4. Road Indicators (West & South Roads)
    add_cad_text("Road_West_Text", "WEST ROAD 30'-0\" WIDE (MAIN ACCESS)", -3.4, PLINTH_D / 2.0, size=0.30, rot_z=math.radians(90), color=(0.15, 0.25, 0.45, 1.0), collection=collection)
    add_cad_text("Road_South_Text", "SOUTH ROAD 30'-0\" WIDE (CORNER ACCESS)", PLINTH_W / 2.0, -2.9, size=0.30, color=(0.15, 0.25, 0.45, 1.0), collection=collection)

    # 5. North Arrow Compass
    add_cad_text("North_Symbol", "NORTH [N]\n▲", PLINTH_W + 3.8, PLINTH_D - 0.5, size=0.30, color=(0.85, 0.15, 0.15, 1.0), collection=collection)

def add_title_block(sheet_title, collection):
    """Engineering Title Block and Legend in bottom-right margin."""
    mat_tb = get_or_create_material("Mat_TitleBlock", (0.95, 0.96, 0.98, 1.0))
    mat_border = get_or_create_material("Mat_TBBorder", (0.20, 0.25, 0.35, 1.0))
    
    bx0, by0 = PLINTH_W + 1.2, -3.8
    bx1, by1 = PLINTH_W + 6.6, 2.2
    create_box("TB_BG", bx0, by0, bx1, by1, 0, 0.02, mat_tb, collection)
    create_box("TB_Border_Top", bx0, by1 - 0.03, bx1, by1, 0, 0.03, mat_border, collection)
    create_box("TB_Border_Bot", bx0, by0, bx1, by0 + 0.03, 0, 0.03, mat_border, collection)
    create_box("TB_Border_L", bx0, by0, bx0 + 0.03, by1, 0, 0.03, mat_border, collection)
    create_box("TB_Border_R", bx1 - 0.03, by0, bx1, by1, 0, 0.03, mat_border, collection)
    
    cx = (bx0 + bx1) / 2.0
    add_cad_text("TB_H1", "PROPERTY 2 RESIDENCE", cx, 1.7, size=0.28, color=(0.1, 0.15, 0.25, 1.0), collection=collection)
    add_cad_text("TB_H2", sheet_title.upper(), cx, 1.25, size=0.24, color=(0.05, 0.45, 0.35, 1.0), collection=collection)
    add_cad_text("TB_P1", "PLOT: 54'-0\" x 66'-0\" (SW CORNER)", cx, 0.8, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P2", "PLINTH: 37'-0\" x 40'-0\" (1480 SQ.FT)", cx, 0.45, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P3", "GRID: 16 RCC COLUMNS (9\" x 18\")", cx, 0.1, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P4", "SETBACKS: S:9' W:8' N:6' E:5'", cx, -0.25, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P5", "VAASTU: TELUGU / TELANGANA", cx, -0.6, size=0.18, color=(0.75, 0.40, 0.05, 1.0), collection=collection)
    add_cad_text("TB_P6", "SCALE: 1:100 @ A3 | CAD PLAN", cx, -0.95, size=0.17, color=COLOR_DIM, collection=collection)
    
    add_cad_text("TB_Leg1", "DOORS: D1: 3'6\"x7' | D2: 3'0\"x7' | D3: 2'6\"x7'", cx, -1.6, size=0.15, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_Leg2", "WINDOWS: W1: 5'0\"x4'6\" | W2: 4'0\"x4'6\" | V1: 2'0\"x2'0\"", cx, -1.95, size=0.15, color=COLOR_TEXT, collection=collection)

def setup_scene(scene_name):
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
    cam_data.ortho_scale = 22.0  # Captures 22m wide frame with generous margins
    
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)
        
    cam_obj.location = (PLINTH_W / 2.0 + 1.2, PLINTH_D / 2.0 - 0.2, 25.0)
    cam_obj.rotation_euler = (0, 0, 0)
    scene.camera = cam_obj
    return scene

# =============================================================================
# SCENE 1: GROUND STILT FLOOR (LEVEL 0, +0.00m)
# =============================================================================
def build_ground_stilt():
    scene = setup_scene("Ground_Stilt")
    bpy.context.window.scene = scene
    col = scene.collection
    
    mat_slab = get_or_create_material("Mat_Slab", COLOR_SLAB)
    mat_pavilion = get_or_create_material("Mat_Pavilion", COLOR_PAVILION)
    mat_parking = get_or_create_material("Mat_Parking", COLOR_PARKING)
    
    # 1. Concrete Plinth Slab
    create_box("Ground_Plinth", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_slab, col)
    
    # 2. Sheltered Function Pavilion (South & East Zone, ~740 sq ft)
    create_box("Pavilion_Area", 0, 0, PLINTH_W, 6.0, 0, 0.05, mat_pavilion, col)
    
    # 3. Stilt Parking Bay (NE Driveway Zone)
    create_box("Car_Stall", PLINTH_W - 3.2, PLINTH_D - 5.5, PLINTH_W - 0.4, PLINTH_D - 0.3, 0, 0.04, mat_parking, col)
    create_box("Bike_Stall_1", PLINTH_W - 4.6, PLINTH_D - 2.8, PLINTH_W - 3.4, PLINTH_D - 0.4, 0, 0.04, mat_parking, col)
    create_box("Bike_Stall_2", PLINTH_W - 4.6, PLINTH_D - 5.4, PLINTH_W - 3.4, PLINTH_D - 3.0, 0, 0.04, mat_parking, col)
    
    # 4. Vertical Core (NW Zone)
    add_dog_legged_stairs(0.23, 6.0, 2.2, 4.4, col)
    add_lift_shaft(2.5, 7.5, 2.05, 2.05, col)
    
    # 5. 16 Structural Columns
    add_columns(col)
    
    # 6. Grid Lines, Dimensions, Roads, Title Block
    add_column_grids_and_dimensions(col)
    add_title_block("Ground Stilt & Parking Plan", col)
    
    # 7. Room Annotations
    add_cad_text("Lbl_Pavilion_1", "SHELTERED OPEN FUNCTION PAVILION", 5.6, 3.2, size=0.34, color=(0.1, 0.2, 0.3, 1.0), collection=col)
    add_cad_text("Lbl_Pavilion_2", "37'-0\" x 20'-0\" [11.28m x 6.10m] | 740 SQ.FT", 5.6, 2.6, size=0.24, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Pavilion_3", "(Family Gatherings, Traditional Events, Verandah)", 5.6, 2.1, size=0.20, color=COLOR_DIM, collection=col)

    add_cad_text("Lbl_Car", "COVERED CAR STALL\n8'-6\" x 17'-0\"", PLINTH_W - 1.8, PLINTH_D - 2.9, size=0.22, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Bikes", "2-WHEELERS\n(4 BIKES)", PLINTH_W - 4.0, PLINTH_D - 2.9, size=0.20, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Stairs", "DOG-LEGGED STAIRCASE\n7'-3\" x 14'-6\" [NW VAYU]", 1.33, 8.2, z=0.95, size=0.22, rot_z=math.radians(90), color=(0.10, 0.12, 0.16, 1.0), collection=col)
    add_cad_text("Lbl_Lift", "PASSENGER LIFT\n6-PAX (1.6m x 1.6m)", 3.52, 8.5, size=0.20, rot_z=math.radians(90), color=(0.1, 0.15, 0.25, 1.0), collection=col)

    # Render
    scene.render.filepath = str(OUTPUT_DIR / "ground_stilt_2d.png")
    bpy.ops.render.render(write_still=True)
    print("Rendered: ground_stilt_2d.png")

# =============================================================================
# SCENE 2: FIRST FLOOR — BROTHER'S 2BHK RESIDENCE (+3.00m)
# =============================================================================
def build_first_floor_brother():
    scene = setup_scene("First_Floor_Brother")
    bpy.context.window.scene = scene
    col = scene.collection
    
    mat_slab = get_or_create_material("Mat_Slab", COLOR_SLAB)
    mat_ext = get_or_create_material("Mat_ExtWall", COLOR_EXT_WALL)
    mat_int = get_or_create_material("Mat_IntWall", COLOR_INT_WALL)
    mat_bed = get_or_create_material("Mat_Bed", COLOR_BED)
    mat_kit = get_or_create_material("Mat_Kitchen", COLOR_KITCHEN)
    mat_furn = get_or_create_material("Mat_Furniture", COLOR_FURNITURE)
    mat_pooja = get_or_create_material("Mat_Pooja", COLOR_POOJA)
    
    # 1. Floor Slab & Columns
    create_box("Floor1_Slab", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_slab, col)
    add_columns(col)
    
    # 2. Exterior 9" (230mm) Walls with Window Openings
    create_box("Ext_S_1", 0, 0, 1.2, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_MB_S", 1.2, 0, 2.7, EXT_WALL_THICK, None, col)
    create_box("Ext_S_2", 2.7, 0, PLINTH_W, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    create_box("Ext_E_1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 1.0, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Kit_E", PLINTH_W - EXT_WALL_THICK, 1.0, PLINTH_W, 2.2, None, col)
    create_box("Ext_E_2", PLINTH_W - EXT_WALL_THICK, 2.2, PLINTH_W, 5.0, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Liv_E", PLINTH_W - EXT_WALL_THICK, 5.0, PLINTH_W, 7.4, None, col)
    create_box("Ext_E_3", PLINTH_W - EXT_WALL_THICK, 7.4, PLINTH_W, PLINTH_D, 0, WALL_H, mat_ext, col)
    
    create_box("Ext_N_1", 0, PLINTH_D - EXT_WALL_THICK, 5.0, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_B2_N", 5.0, PLINTH_D - EXT_WALL_THICK, 6.5, PLINTH_D, None, col)
    create_box("Ext_N_2", 6.5, PLINTH_D - EXT_WALL_THICK, PLINTH_W, PLINTH_D, 0, WALL_H, mat_ext, col)
    
    create_box("Ext_W_1", 0, EXT_WALL_THICK, EXT_WALL_THICK, 4.2, 0, WALL_H, mat_ext, col)
    create_window_2d("Vent_V1", 0, 4.2, EXT_WALL_THICK, 4.8, None, col)
    create_box("Ext_W_2", 0, 4.8, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    # 3. Interior Partitions (4.5" / 115mm)
    create_box("MB_Wall_E", 3.81 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.81 + INT_WALL_THICK/2, 4.06, 0, WALL_H, mat_int, col)
    create_box("MB_Wall_N_1", EXT_WALL_THICK, 4.06 - INT_WALL_THICK/2, 1.8, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_MB", 2.7, 4.06, 0.90, 90, 'S', None, col)
    create_box("MB_Wall_N_2", 2.7, 4.06 - INT_WALL_THICK/2, 3.81, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    create_box("Bath_Div_Wall", 1.8 - INT_WALL_THICK/2, 4.06, 1.8 + INT_WALL_THICK/2, 6.0, 0, WALL_H, mat_int, col)
    create_box("Bath_North_Wall", EXT_WALL_THICK, 6.0 - INT_WALL_THICK/2, 3.81, 6.0 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Bath_East_Wall", 3.81 - INT_WALL_THICK/2, 4.06, 3.81 + INT_WALL_THICK/2, 5.0, 0, WALL_H, mat_int, col)
    create_door_2d("Door_CB", 3.81, 5.0, 0.75, 90, 'W', None, col)
    create_box("Bath_East_Wall_2", 3.81 - INT_WALL_THICK/2, 5.75, 3.81 + INT_WALL_THICK/2, 6.0, 0, WALL_H, mat_int, col)
    
    create_box("Kit_Wall_W", 7.31 - INT_WALL_THICK/2, EXT_WALL_THICK, 7.31 + INT_WALL_THICK/2, 2.5, 0, WALL_H, mat_int, col)
    create_box("Kit_Wall_N", 7.31, 3.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 3.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    create_box("B2_Wall_W", 4.6 - INT_WALL_THICK/2, 8.13, 4.6 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("B2_Wall_E", 7.5 - INT_WALL_THICK/2, 8.13, 7.5 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("B2_Wall_S_1", 4.6, 8.13 - INT_WALL_THICK/2, 5.5, 8.13 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_B2", 5.5, 8.13, 0.90, 90, 'N', None, col)
    create_box("B2_Wall_S_2", 6.4, 8.13 - INT_WALL_THICK/2, 7.5, 8.13 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    create_box("Pooja_Wall_W", 7.5 - INT_WALL_THICK/2, 8.13, 7.5 + INT_WALL_THICK/2, 10.5, 0, WALL_H, mat_int, col)
    create_box("Pooja_Wall_N", 7.5, 10.5 - INT_WALL_THICK/2, 9.5, 10.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Pooja", 8.0, 8.13, 0.80, 90, 'N', None, col)
    
    # 4. Vertical Core (NW)
    add_dog_legged_stairs(EXT_WALL_THICK, 6.0, 2.2, 4.4, col)
    add_lift_shaft(2.5, 7.5, 2.05, 2.05, col)
    create_door_2d("Simhadwaram_D1", 4.6, 6.2, 1.05, 90, 'E', None, col)
    
    # 5. Furniture & Civil Fixtures
    create_box("MB_King_Bed", 1.0, EXT_WALL_THICK + 0.1, 2.8, EXT_WALL_THICK + 2.1, 0, 0.45, mat_bed, col)
    create_box("MB_Headboard", 0.9, EXT_WALL_THICK, 2.9, EXT_WALL_THICK + 0.1, 0, 0.75, mat_bed, col)
    create_box("MB_Wardrobe", EXT_WALL_THICK, 1.5, EXT_WALL_THICK + 0.6, 3.8, 0, 0.90, mat_furn, col)
    
    create_box("B2_Queen_Bed", 5.2, PLINTH_D - EXT_WALL_THICK - 2.1, 6.7, PLINTH_D - EXT_WALL_THICK - 0.1, 0, 0.45, mat_bed, col)
    create_box("B2_Wardrobe", 4.6 + INT_WALL_THICK/2, 9.0, 4.6 + 0.6, 11.2, 0, 0.90, mat_furn, col)
    
    create_box("Kit_Counter_E", PLINTH_W - EXT_WALL_THICK - 0.6, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK, 3.4, 0, 0.85, mat_kit, col)
    create_box("Kit_Counter_S", 7.4, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK - 0.6, EXT_WALL_THICK + 0.6, 0, 0.85, mat_kit, col)
    create_box("Kit_Sink", PLINTH_W - EXT_WALL_THICK - 0.55, 1.3, PLINTH_W - EXT_WALL_THICK - 0.05, 1.9, 0.86, 0.87, mat_slab, col)
    create_box("Kit_Stove", PLINTH_W - EXT_WALL_THICK - 0.55, 2.3, PLINTH_W - EXT_WALL_THICK - 0.10, 3.0, 0.86, 0.88, mat_pooja, col)
    
    create_box("Dining_Table", 4.8, 1.5, 6.3, 2.4, 0, 0.75, mat_furn, col)
    create_box("Living_Sofa_3P", PLINTH_W - EXT_WALL_THICK - 0.9, 4.5, PLINTH_W - EXT_WALL_THICK, 6.5, 0, 0.65, mat_bed, col)
    create_box("Coffee_Table", PLINTH_W - EXT_WALL_THICK - 2.0, 5.0, PLINTH_W - EXT_WALL_THICK - 1.2, 6.0, 0, 0.40, mat_furn, col)
    create_box("Pooja_Altar", 7.6, 8.2, 9.4, 8.8, 0, 0.60, mat_pooja, col)
    
    # 6. Structural Grids, Dimensions, Road Labels, Title Block
    add_column_grids_and_dimensions(col)
    add_title_block("First Floor - Brother's 2BHK", col)
    
    # 7. Professional CAD Room Labels with Clear Dimensions & Vaastu Tags
    add_cad_text("Lbl_MB_1", "MASTER BEDROOM", 2.0, 3.1, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_MB_2", "12'-6\" x 13'-4\" [3.81m x 4.06m]", 2.0, 2.7, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_MB_3", "[NIRUTHI / SW ZONE - HEAVY]", 2.0, 2.35, size=0.17, color=(0.6, 0.3, 0.1, 1.0), collection=col)

    add_cad_text("Lbl_AttBath", "ATT. TOILET\n5'0\" x 6'6\"", 1.0, 5.0, size=0.18, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_ComBath", "COMMON TOILET\n5'0\" x 6'6\" [VARUNA]", 2.8, 5.0, size=0.18, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Kit_1", "MODULAR KITCHEN", 9.2, 2.0, size=0.26, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kit_2", "12'-6\" x 11'-0\" [3.81m x 3.35m]", 9.2, 1.65, size=0.19, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kit_3", "[AGNEYA / SE ZONE - FIRE]", 9.2, 1.35, size=0.16, color=(0.8, 0.3, 0.05, 1.0), collection=col)

    add_cad_text("Lbl_Din", "DINING AREA\n10'-0\" x 11'-6\"", 5.55, 2.8, size=0.22, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Liv_1", "FORMAL LIVING ROOM", 9.2, 5.8, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Liv_2", "14'-0\" x 13'-6\" [4.27m x 4.11m]", 9.2, 5.4, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Liv_3", "[CENTRAL BRAHMASTHANA - OPEN]", 9.2, 5.05, size=0.17, color=(0.1, 0.4, 0.3, 1.0), collection=col)

    add_cad_text("Lbl_B2_1", "BEDROOM 2", 6.0, 10.5, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_B2_2", "9'-6\" x 12'-6\" [2.90m x 3.81m]", 6.0, 10.1, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_B2_3", "[VAYU / NORTH ZONE]", 6.0, 9.75, size=0.17, color=COLOR_DIM, collection=col)

    # Clean non-overlapping Pooja & Balcony tags
    add_cad_text("Lbl_Pooja_1", "POOJA MANDIR", 8.3, 9.2, size=0.22, color=(0.85, 0.50, 0.05, 1.0), collection=col)
    add_cad_text("Lbl_Pooja_2", "6'0\" x 7'9\" [ISHANYA]", 8.3, 8.85, size=0.17, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Balcony_1", "EAST SITOUT BALCONY", 10.0, 11.2, size=0.22, color=(0.1, 0.35, 0.7, 1.0), collection=col)
    add_cad_text("Lbl_Balcony_2", "7'0\" x 12'6\" (OPEN TO SKY)", 10.0, 10.85, size=0.18, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Simha", "MAIN ENTRANCE (SIMHADWARAM)\nNORTH-FACING [D1]", 5.8, 6.7, size=0.20, color=(0.05, 0.55, 0.35, 1.0), collection=col)

    # Render
    scene.render.filepath = str(OUTPUT_DIR / "first_floor_brother_2d.png")
    bpy.ops.render.render(write_still=True)
    print("Rendered: first_floor_brother_2d.png")

# =============================================================================
# SCENE 3: SECOND FLOOR — OWNER'S RESIDENCE (2BHK + OFFICE + DUAL POOJA)
# =============================================================================
def build_second_floor_owner():
    scene = setup_scene("Second_Floor_Owner")
    bpy.context.window.scene = scene
    col = scene.collection
    
    mat_slab = get_or_create_material("Mat_Slab", COLOR_SLAB)
    mat_ext = get_or_create_material("Mat_ExtWall", COLOR_EXT_WALL)
    mat_int = get_or_create_material("Mat_IntWall", COLOR_INT_WALL)
    mat_bed = get_or_create_material("Mat_Bed", COLOR_BED)
    mat_kit = get_or_create_material("Mat_Kitchen", COLOR_KITCHEN)
    mat_furn = get_or_create_material("Mat_Furniture", COLOR_FURNITURE)
    mat_pooja = get_or_create_material("Mat_Pooja", COLOR_POOJA)
    
    # 1. Floor Slab & Columns
    create_box("Floor2_Slab", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_slab, col)
    add_columns(col)
    
    # 2. Exterior Walls (Identical stack to Floor 1)
    create_box("Ext_S_1", 0, 0, 1.2, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_MB_S", 1.2, 0, 2.7, EXT_WALL_THICK, None, col)
    create_box("Ext_S_2", 2.7, 0, PLINTH_W, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    create_box("Ext_E_1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 1.0, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Kit_E", PLINTH_W - EXT_WALL_THICK, 1.0, PLINTH_W, 2.2, None, col)
    create_box("Ext_E_2", PLINTH_W - EXT_WALL_THICK, 2.2, PLINTH_W, 5.0, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Liv_E", PLINTH_W - EXT_WALL_THICK, 5.0, PLINTH_W, 7.4, None, col)
    create_box("Ext_E_3", PLINTH_W - EXT_WALL_THICK, 7.4, PLINTH_W, PLINTH_D, 0, WALL_H, mat_ext, col)
    
    create_box("Ext_N_1", 0, PLINTH_D - EXT_WALL_THICK, 5.0, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_B2_N", 5.0, PLINTH_D - EXT_WALL_THICK, 6.5, PLINTH_D, None, col)
    create_box("Ext_N_2", 6.5, PLINTH_D - EXT_WALL_THICK, PLINTH_W, PLINTH_D, 0, WALL_H, mat_ext, col)
    
    create_box("Ext_W_1", 0, EXT_WALL_THICK, EXT_WALL_THICK, 4.2, 0, WALL_H, mat_ext, col)
    create_window_2d("Vent_V1", 0, 4.2, EXT_WALL_THICK, 4.8, None, col)
    create_box("Ext_W_2", 0, 4.8, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    # 3. Partitions: Master Bed (SW) & Baths (Stacked 1:1)
    create_box("MB_Wall_E", 3.81 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.81 + INT_WALL_THICK/2, 4.06, 0, WALL_H, mat_int, col)
    create_box("MB_Wall_N_1", EXT_WALL_THICK, 4.06 - INT_WALL_THICK/2, 1.8, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_MB", 2.7, 4.06, 0.90, 90, 'S', None, col)
    create_box("MB_Wall_N_2", 2.7, 4.06 - INT_WALL_THICK/2, 3.81, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    create_box("Bath_Div_Wall", 1.8 - INT_WALL_THICK/2, 4.06, 1.8 + INT_WALL_THICK/2, 6.0, 0, WALL_H, mat_int, col)
    create_box("Bath_North_Wall", EXT_WALL_THICK, 6.0 - INT_WALL_THICK/2, 3.81, 6.0 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Bath_East_Wall", 3.81 - INT_WALL_THICK/2, 4.06, 3.81 + INT_WALL_THICK/2, 5.0, 0, WALL_H, mat_int, col)
    create_door_2d("Door_CB", 3.81, 5.0, 0.75, 90, 'W', None, col)
    create_box("Bath_East_Wall_2", 3.81 - INT_WALL_THICK/2, 5.75, 3.81 + INT_WALL_THICK/2, 6.0, 0, WALL_H, mat_int, col)
    
    # Kitchen (SE, stacked 1:1)
    create_box("Kit_Wall_W", 7.31 - INT_WALL_THICK/2, EXT_WALL_THICK, 7.31 + INT_WALL_THICK/2, 2.5, 0, WALL_H, mat_int, col)
    create_box("Kit_Wall_N", 7.31, 3.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 3.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    # Home Office / Study Suite (Center Bay): X in [3.81, 7.31], Y in [2.8, 5.2]
    create_box("Office_Wall_S", 3.81, 2.8 - INT_WALL_THICK/2, 7.31, 2.8 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Office_Wall_N_1", 3.81, 5.2 - INT_WALL_THICK/2, 5.0, 5.2 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Office", 5.0, 5.2, 0.90, 90, 'S', None, col)
    create_box("Office_Wall_N_2", 5.9, 5.2 - INT_WALL_THICK/2, 7.31, 5.2 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    # Bedroom 2 (North): X in [4.6, 7.5], Y in [8.13, 11.96]
    create_box("B2_Wall_W", 4.6 - INT_WALL_THICK/2, 8.13, 4.6 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("B2_Wall_E", 7.5 - INT_WALL_THICK/2, 8.13, 7.5 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("B2_Wall_S_1", 4.6, 8.13 - INT_WALL_THICK/2, 5.5, 8.13 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_B2", 5.5, 8.13, 0.90, 90, 'N', None, col)
    create_box("B2_Wall_S_2", 6.4, 8.13 - INT_WALL_THICK/2, 7.5, 8.13 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    # NE DUAL POOJA SUITE:
    create_box("Pooja_Div_Wall", 7.5, 10.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 10.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Mallanna_Wall_W", 8.8 - INT_WALL_THICK/2, 10.5, 8.8 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Daily_Pooja", 8.0, 10.5, 0.80, 90, 'S', None, col)
    create_door_2d("Door_Mallanna_Pooja", 9.5, 10.5, 0.90, 90, 'N', None, col)
    
    # Vertical Core (NW)
    add_dog_legged_stairs(EXT_WALL_THICK, 6.0, 2.2, 4.4, col)
    add_lift_shaft(2.5, 7.5, 2.05, 2.05, col)
    create_door_2d("Simhadwaram_D1", 4.6, 6.2, 1.05, 90, 'E', None, col)
    
    # 4. Built-in Civil Fixtures & Millwork
    create_box("MB_King_Bed", 1.0, EXT_WALL_THICK + 0.1, 2.8, EXT_WALL_THICK + 2.1, 0, 0.45, mat_bed, col)
    create_box("MB_Headboard", 0.9, EXT_WALL_THICK, 2.9, EXT_WALL_THICK + 0.1, 0, 0.75, mat_bed, col)
    create_box("MB_Wardrobe", EXT_WALL_THICK, 1.5, EXT_WALL_THICK + 0.6, 3.8, 0, 0.90, mat_furn, col)
    
    create_box("B2_Queen_Bed", 5.2, PLINTH_D - EXT_WALL_THICK - 2.1, 6.7, PLINTH_D - EXT_WALL_THICK - 0.1, 0, 0.45, mat_bed, col)
    create_box("B2_Wardrobe", 4.6 + INT_WALL_THICK/2, 9.0, 4.6 + 0.6, 11.2, 0, 0.90, mat_furn, col)
    
    create_box("Office_Desk", 4.5, 3.4, 6.0, 4.2, 0, 0.75, mat_furn, col)
    create_box("Office_Bookcase", 3.81 + INT_WALL_THICK/2, 3.2, 4.15, 4.8, 0, 1.20, mat_furn, col)
    
    create_box("Kit_Counter_E", PLINTH_W - EXT_WALL_THICK - 0.6, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK, 3.4, 0, 0.85, mat_kit, col)
    create_box("Kit_Counter_S", 7.4, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK - 0.6, EXT_WALL_THICK + 0.6, 0, 0.85, mat_kit, col)
    create_box("Kit_Sink", PLINTH_W - EXT_WALL_THICK - 0.55, 1.3, PLINTH_W - EXT_WALL_THICK - 0.05, 1.9, 0.86, 0.87, mat_slab, col)
    create_box("Kit_Stove", PLINTH_W - EXT_WALL_THICK - 0.55, 2.3, PLINTH_W - EXT_WALL_THICK - 0.10, 3.0, 0.86, 0.88, mat_pooja, col)
    
    create_box("Dining_Table", 4.8, 1.5, 6.3, 2.4, 0, 0.75, mat_furn, col)
    create_box("Living_Sofa_3P", PLINTH_W - EXT_WALL_THICK - 0.9, 4.5, PLINTH_W - EXT_WALL_THICK, 6.5, 0, 0.65, mat_bed, col)
    create_box("Coffee_Table", PLINTH_W - EXT_WALL_THICK - 2.0, 5.0, PLINTH_W - EXT_WALL_THICK - 1.2, 6.0, 0, 0.40, mat_furn, col)
    
    # Mallanna Sacred Shrine Altar & Prayer Carpet
    create_box("Mallanna_Altar", 8.9, 10.6, PLINTH_W - EXT_WALL_THICK - 0.1, 11.3, 0, 0.65, mat_pooja, col)
    create_box("Mallanna_Prayer_Carpet", 9.0, 11.4, PLINTH_W - EXT_WALL_THICK - 0.2, PLINTH_D - EXT_WALL_THICK - 0.2, 0, 0.02, mat_pooja, col)
    
    # 5. Structural Grids, Dimensions, Road Labels, Title Block
    add_column_grids_and_dimensions(col)
    add_title_block("Second Floor - Owner's Residence", col)
    
    # 6. Room Annotations
    add_cad_text("Lbl_MB_1", "MASTER BEDROOM", 2.0, 3.1, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_MB_2", "12'-6\" x 13'-4\" [3.81m x 4.06m]", 2.0, 2.7, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_MB_3", "[NIRUTHI / SW ZONE - HEAVY]", 2.0, 2.35, size=0.17, color=(0.6, 0.3, 0.1, 1.0), collection=col)

    add_cad_text("Lbl_AttBath", "ATT. TOILET\n5'0\" x 6'6\"", 1.0, 5.0, size=0.18, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_ComBath", "COMMON TOILET\n5'0\" x 6'6\" [VARUNA]", 2.8, 5.0, size=0.18, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Kit_1", "MODULAR KITCHEN", 9.2, 2.0, size=0.26, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kit_2", "12'-6\" x 11'-0\" [3.81m x 3.35m]", 9.2, 1.65, size=0.19, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kit_3", "[AGNEYA / SE ZONE - FIRE]", 9.2, 1.35, size=0.16, color=(0.8, 0.3, 0.05, 1.0), collection=col)

    add_cad_text("Lbl_Office_1", "HOME OFFICE / STUDY", 5.55, 4.3, size=0.25, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Office_2", "11'-6\" x 8'-0\" [3.50m x 2.44m]", 5.55, 3.9, size=0.18, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Office_3", "[HIGH-FOCUS WORK SUITE]", 5.55, 3.55, size=0.16, color=(0.15, 0.35, 0.65, 1.0), collection=col)

    add_cad_text("Lbl_Din", "DINING AREA\n10'-0\" x 9'-0\"", 5.55, 2.1, size=0.20, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Liv_1", "FAMILY LIVING AREA", 9.2, 5.8, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Liv_2", "14'-0\" x 13'-6\" [4.27m x 4.11m]", 9.2, 5.4, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Liv_3", "[CENTRAL BRAHMASTHANA - OPEN]", 9.2, 5.05, size=0.17, color=(0.1, 0.4, 0.3, 1.0), collection=col)

    add_cad_text("Lbl_B2_1", "BEDROOM 2", 6.0, 10.5, size=0.28, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_B2_2", "9'-6\" x 12'-6\" [2.90m x 3.81m]", 6.0, 10.1, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_B2_3", "[VAYU / NORTH ZONE]", 6.0, 9.75, size=0.17, color=COLOR_DIM, collection=col)

    # NE DUAL POOJA SUITE
    add_cad_text("Lbl_DailyPooja_1", "DAILY POOJA", 8.15, 9.4, size=0.22, color=(0.85, 0.50, 0.05, 1.0), collection=col)
    add_cad_text("Lbl_DailyPooja_2", "4'0\" x 4'0\"", 8.15, 9.05, size=0.17, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Mallanna_1", "MALLANNA TEMPLE SHRINE", 10.0, 11.4, size=0.24, color=(0.85, 0.50, 0.05, 1.0), collection=col)
    add_cad_text("Lbl_Mallanna_2", "9'0\" x 9'0\" [81 SQ.FT]", 10.0, 11.0, size=0.19, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Mallanna_3", "[SACRED ISHANYA / NE CORNER]", 10.0, 10.65, size=0.16, color=(0.8, 0.2, 0.0, 1.0), collection=col)

    add_cad_text("Lbl_Simha", "MAIN ENTRANCE (SIMHADWARAM)\nNORTH-FACING [D1]", 5.8, 6.7, size=0.20, color=(0.05, 0.55, 0.35, 1.0), collection=col)

    # Render
    scene.render.filepath = str(OUTPUT_DIR / "second_floor_owner_2d.png")
    bpy.ops.render.render(write_still=True)
    print("Rendered: second_floor_owner_2d.png")

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    print("Starting Blender 2D Architectural CAD Generation...")
    build_ground_stilt()
    build_first_floor_brother()
    build_second_floor_owner()
    
    # Save the master .blend file so user can open it directly in Blender GUI
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_FILE))
    print(f"Master Project Saved: {BLEND_FILE}")
