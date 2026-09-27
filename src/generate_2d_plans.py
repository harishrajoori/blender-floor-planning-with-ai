"""
Civil Engineering & Vaastu-Compliant 2D Floor Plan Generator for Property 2 (54' x 66' Plot)
Redesigned according to Owner Requirements & Canonical Telangana Vaastu Principles:
  1. North-East (Ishanya) kept completely open as a light sitout terrace.
  2. External Vertical Core (Dog-legged Stairs + 6-PAX Lift) outside the home envelope.
  3. North-facing Home Office with clear garden view (unblocked by lift/stairs).
  4. Sequence along East: Kitchen (SE) -> Dining/Living -> Mallanna Shrine -> Daily Pooja -> Open NE Sitout.
  5. Dual light doors (NNE Simhadwaram & East/NE Glazed Door) for continuous cross-ventilation.
  6. External Utility / Wash balcony cantilevered outside the kitchen.
  7. Spacious luxury bathrooms (6'0" x 8'6") with distinct dry/wet zones.
  8. Three balconies: North, East (Ishanya), and South.
  9. Complete built-in millwork: cupboards/wardrobes, executive desk, TV console, L-sofa, gardens & parking.
"""

import bpy
import math
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BLEND_FILE = OUTPUT_DIR / "property2_engineering_cad.blend"

# Geometry Constants (Meters)
# Plinth Envelope: 37'-0" (11.28m) EW x 40'-0" (12.19m) NS
PLINTH_W = 11.2776
PLINTH_D = 12.192
WALL_H = 0.90           # Cut-plane section height
EXT_WALL_THICK = 0.230  # 9" exterior brick wall
INT_WALL_THICK = 0.115  # 4.5" interior partition wall
CORE_WALL_THICK = 0.200 # 8" RCC lift shaft wall
COL_W = 0.230           # 9" column width
COL_D = 0.450           # 18" column depth

# 16 RCC Column Grid Intersections (4x4)
GRID_X = [0.115, 3.810, 7.315, PLINTH_W - 0.115]
GRID_Y = [0.115, 4.064, 8.128, PLINTH_D - 0.115]

# Professional CAD Color Palette (RGBA)
COLOR_SLAB = (0.97, 0.97, 0.98, 1.0)
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
COLOR_GARDEN = (0.82, 0.92, 0.82, 1.0)         # Landscaped garden green
COLOR_BALCONY = (0.91, 0.94, 0.98, 1.0)        # Open balcony slab

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
    
    # 90 deg swing arc
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
    """
    Stairs and Lift OUTSIDE the home envelope in NW (Vayu) Zone.
    Positioned in West Setback / External Zone: X in [-2.4, 0.0], Y in [6.5, 12.0].
    Provides completely external, independent access to L0, L1, L2.
    """
    mat_core = get_or_create_material("Mat_Core", (0.35, 0.30, 0.45, 1.0))
    mat_tread = get_or_create_material("Mat_Tread", (0.75, 0.77, 0.82, 1.0))
    mat_lift_cab = get_or_create_material("Mat_LiftCab", (0.88, 0.88, 0.92, 1.0))
    mat_ext = get_or_create_material("Mat_ExtWall", COLOR_EXT_WALL)

    # 1. External Landing / Verandah Slab
    create_box("Core_Landing_Slab", -2.5, 6.0, 0.0, 12.2, -0.05, 0, mat_core, collection)
    
    # 2. Dog-Legged Staircase (-2.4 to -0.2, Y: 6.2 to 9.5)
    create_box("Ext_Stair_Base", -2.4, 6.2, -0.3, 9.5, 0, 0.05, mat_tread, collection)
    # Mid landing
    create_box("Stair_Mid_Landing", -2.4, 6.2, -0.3, 7.3, 0, 0.08, mat_tread, collection)
    # Divider
    create_box("Stair_Divider", -1.4, 7.3, -1.3, 9.5, 0, WALL_H * 0.8, mat_core, collection)
    # Treads
    for i in range(1, 7):
        ty = 7.3 + i * (2.2 / 7.0)
        create_box(f"Tread_Up_{i}", -2.4, ty - 0.015, -1.45, ty + 0.015, 0, 0.06, mat_tread, collection)
        create_box(f"Tread_Dn_{i}", -1.25, ty - 0.015, -0.3, ty + 0.015, 0, 0.06, mat_tread, collection)

    # 3. Passenger Lift Shaft 6-PAX (X: -2.3 to -0.4, Y: 9.8 to 11.9)
    create_box("Lift_Wall_S", -2.3, 9.8, -0.4, 10.0, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Wall_N", -2.3, 11.7, -0.4, 11.9, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Wall_W", -2.3, 10.0, -2.1, 11.7, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Wall_E", -0.6, 10.0, -0.4, 11.7, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Cab", -1.95, 10.15, -0.75, 11.55, 0, 0.05, mat_lift_cab, collection)

    # 4. External Core Guardrail
    create_box("Core_Rail_W", -2.5, 6.0, -2.45, 12.2, 0, WALL_H * 0.9, mat_core, collection)

def add_column_grids_and_dimensions(collection):
    """Draws professional structural grid lines, bubbles 1-4/A-D, and bay dimensions."""
    mat_grid = get_or_create_material("Mat_GridLine", COLOR_GRID)
    mat_bubble = get_or_create_material("Mat_GridBubble", COLOR_BUBBLE)
    mat_dim = get_or_create_material("Mat_DimLine", COLOR_DIM)
    
    # Vertical Grid Lines (X1-X4)
    for ix, cx in enumerate(GRID_X):
        create_box(f"GridLine_X_{ix+1}", cx - 0.01, -2.2, cx + 0.01, PLINTH_D + 2.2, 0, 0.02, mat_grid, collection)
        create_box(f"Bubble_Top_{ix+1}", cx - 0.35, PLINTH_D + 2.2, cx + 0.35, PLINTH_D + 2.9, 0, 0.04, mat_bubble, collection)
        add_cad_text(f"GridText_Top_{ix+1}", str(ix+1), cx, PLINTH_D + 2.55, size=0.35, color=COLOR_TEXT, collection=collection)
        create_box(f"Bubble_Bot_{ix+1}", cx - 0.35, -2.9, cx + 0.35, -2.2, 0, 0.04, mat_bubble, collection)
        add_cad_text(f"GridText_Bot_{ix+1}", str(ix+1), cx, -2.55, size=0.35, color=COLOR_TEXT, collection=collection)

    # Horizontal Grid Lines (YA-YD)
    labels_y = ['A', 'B', 'C', 'D']
    for iy, cy in enumerate(GRID_Y):
        create_box(f"GridLine_Y_{labels_y[iy]}", -3.2, cy - 0.01, PLINTH_W + 2.2, cy + 0.01, 0, 0.02, mat_grid, collection)
        create_box(f"Bubble_Left_{labels_y[iy]}", -3.9, cy - 0.35, -3.2, cy + 0.35, 0, 0.04, mat_bubble, collection)
        add_cad_text(f"GridText_Left_{labels_y[iy]}", labels_y[iy], -3.55, cy, size=0.35, color=COLOR_TEXT, collection=collection)
        create_box(f"Bubble_Right_{labels_y[iy]}", PLINTH_W + 2.2, cy - 0.35, PLINTH_W + 2.9, cy + 0.35, 0, 0.04, mat_bubble, collection)
        add_cad_text(f"GridText_Right_{labels_y[iy]}", labels_y[iy], PLINTH_W + 2.55, cy, size=0.35, color=COLOR_TEXT, collection=collection)

    # South Dimension: 37'-0" (11.28m)
    create_box("Dim_Line_S", 0, -1.3, PLINTH_W, -1.28, 0, 0.02, mat_dim, collection)
    create_box("Dim_Tick_S0", -0.15, -1.45, 0.15, -1.15, 0, 0.03, mat_dim, collection)
    create_box("Dim_Tick_S1", PLINTH_W - 0.15, -1.45, PLINTH_W + 0.15, -1.15, 0, 0.03, mat_dim, collection)
    add_cad_text("Dim_Text_S", "37'-0\" [11.28m] OVERALL PLINTH WIDTH", PLINTH_W / 2.0, -1.65, size=0.26, color=COLOR_TEXT, collection=collection)

    # West Dimension: 40'-0" (12.19m)
    create_box("Dim_Line_W", -2.8, 0, -2.78, PLINTH_D, 0, 0.02, mat_dim, collection)
    create_box("Dim_Tick_W0", -2.95, -0.15, -2.65, 0.15, 0, 0.03, mat_dim, collection)
    create_box("Dim_Tick_W1", -2.95, PLINTH_D - 0.15, -2.65, PLINTH_D + 0.15, 0, 0.03, mat_dim, collection)
    add_cad_text("Dim_Text_W", "40'-0\" [12.19m] PLINTH DEPTH", -3.05, PLINTH_D / 2.0, size=0.26, rot_z=math.radians(90), color=COLOR_TEXT, collection=collection)

    # Road Indicators
    add_cad_text("Road_West_Text", "WEST ROAD 30'-0\" WIDE (MAIN VEHICLE & PEDESTRIAN ACCESS)", -4.8, PLINTH_D / 2.0, size=0.30, rot_z=math.radians(90), color=(0.15, 0.25, 0.45, 1.0), collection=collection)
    add_cad_text("Road_South_Text", "SOUTH ROAD 30'-0\" WIDE (SECONDARY CORNER ACCESS)", PLINTH_W / 2.0, -3.4, size=0.30, color=(0.15, 0.25, 0.45, 1.0), collection=collection)

    # North Arrow
    add_cad_text("North_Symbol", "NORTH [N]\n▲", PLINTH_W + 3.8, PLINTH_D - 0.5, size=0.30, color=(0.85, 0.15, 0.15, 1.0), collection=collection)

def add_title_block(sheet_title, collection):
    """Engineering Title Block and Legend in bottom-right margin."""
    mat_tb = get_or_create_material("Mat_TitleBlock", (0.95, 0.96, 0.98, 1.0))
    mat_border = get_or_create_material("Mat_TBBorder", (0.20, 0.25, 0.35, 1.0))
    
    bx0, by0 = PLINTH_W + 1.2, -4.2
    bx1, by1 = PLINTH_W + 6.8, 2.6
    create_box("TB_BG", bx0, by0, bx1, by1, 0, 0.02, mat_tb, collection)
    create_box("TB_Border_Top", bx0, by1 - 0.03, bx1, by1, 0, 0.03, mat_border, collection)
    create_box("TB_Border_Bot", bx0, by0, bx1, by0 + 0.03, 0, 0.03, mat_border, collection)
    create_box("TB_Border_L", bx0, by0, bx0 + 0.03, by1, 0, 0.03, mat_border, collection)
    create_box("TB_Border_R", bx1 - 0.03, by0, bx1, by1, 0, 0.03, mat_border, collection)
    
    cx = (bx0 + bx1) / 2.0
    add_cad_text("TB_H1", "PROPERTY 2 RESIDENCE", cx, 2.1, size=0.28, color=(0.1, 0.15, 0.25, 1.0), collection=collection)
    add_cad_text("TB_H2", sheet_title.upper(), cx, 1.65, size=0.24, color=(0.05, 0.45, 0.35, 1.0), collection=collection)
    add_cad_text("TB_P1", "PLOT: 54'-0\" x 66'-0\" (SW CORNER)", cx, 1.2, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P2", "PLINTH: 37'-0\" x 40'-0\" (1,480 SQ.FT)", cx, 0.85, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P3", "CORE: EXTERNAL NW STAIRS & 6-PAX LIFT", cx, 0.50, size=0.18, color=(0.15, 0.35, 0.65, 1.0), collection=collection)
    add_cad_text("TB_P4", "VAASTU: TELUGU / TELANGANA (OPEN NE)", cx, 0.15, size=0.18, color=(0.75, 0.40, 0.05, 1.0), collection=collection)
    add_cad_text("TB_P5", "BALCONIES: NORTH, EAST (NE), & SOUTH", cx, -0.20, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P6", "UTILITY: EXTERNAL OUT-OF-HOUSE BALCONY", cx, -0.55, size=0.18, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_P7", "BATHS: SPACIOUS 6'0\"x8'6\" WET/DRY", cx, -0.90, size=0.18, color=COLOR_TEXT, collection=collection)
    
    add_cad_text("TB_Leg1", "DOORS: D1: 3'6\"x7' | D2: 3'0\"x7' | D3: 2'6\"x7'", cx, -1.5, size=0.15, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_Leg2", "WINDOWS: W1: 5'0\"x4'6\" | W2: 4'0\"x4'6\" | V1: 2'0\"x2'0\"", cx, -1.85, size=0.15, color=COLOR_TEXT, collection=collection)
    add_cad_text("TB_Leg3", "MILLWORK: WARDROBES, OFFICE DESK, TV CONSOLE, SOFA", cx, -2.2, size=0.14, color=COLOR_DIM, collection=collection)

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
    cam_data.ortho_scale = 23.5  # Captures external core, setbacks, and title block
    
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)
        
    cam_obj.location = (PLINTH_W / 2.0 + 0.8, PLINTH_D / 2.0 - 0.2, 25.0)
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
    mat_garden = get_or_create_material("Mat_Garden", COLOR_GARDEN)
    
    # 1. Main Plinth Slab
    create_box("Ground_Plinth", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_slab, col)
    
    # 2. Sheltered Function Pavilion (South & Central, ~750 sq ft)
    create_box("Pavilion_Area", 0, 0, PLINTH_W, 6.2, 0, 0.05, mat_pavilion, col)
    
    # 3. Covered Car Parking Stall (North Zone Driveway, 9' x 18')
    create_box("Car_Stall", 3.8, PLINTH_D - 5.8, 6.6, PLINTH_D - 0.3, 0, 0.04, mat_parking, col)
    # Car Graphic / Boundary
    create_box("Car_Body", 4.1, PLINTH_D - 5.5, 6.3, PLINTH_D - 0.7, 0.05, 0.40, mat_parking, col)
    
    # 4. Two-Wheeler Parking (4 Bikes, East Driveway)
    create_box("Bike_Stall_1", 7.0, PLINTH_D - 3.0, 9.5, PLINTH_D - 0.5, 0, 0.04, mat_parking, col)
    create_box("Bike_Stall_2", 7.0, PLINTH_D - 5.6, 9.5, PLINTH_D - 3.1, 0, 0.04, mat_parking, col)
    
    # 5. Landscaped Green Gardens (North & East Setbacks)
    # North Garden Court (front setback)
    create_box("Garden_North", 0, PLINTH_D + 0.1, PLINTH_W, PLINTH_D + 2.5, 0, 0.02, mat_garden, col)
    # East Garden Lawn (morning sun setback)
    create_box("Garden_East", PLINTH_W + 0.1, 0, PLINTH_W + 2.2, PLINTH_D, 0, 0.02, mat_garden, col)
    
    # 6. External Vertical Core (NW Vayu Zone)
    add_external_vertical_core(col)
    
    # 7. 16 Structural Columns
    add_columns(col)
    
    # 8. Grids, Dimensions, Roads, Title Block
    add_column_grids_and_dimensions(col)
    add_title_block("Ground Stilt, Parking & Garden Plan", col)
    
    # 9. Annotations
    add_cad_text("Lbl_Pavilion_1", "SHELTERED OPEN FUNCTION PAVILION", 5.6, 3.2, size=0.34, color=(0.1, 0.2, 0.3, 1.0), collection=col)
    add_cad_text("Lbl_Pavilion_2", "37'-0\" x 20'-4\" [11.28m x 6.20m] | 750 SQ.FT", 5.6, 2.6, size=0.24, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Pavilion_3", "(Family Celebrations, Festival Pandal, Open Gathering)", 5.6, 2.1, size=0.20, color=COLOR_DIM, collection=col)

    add_cad_text("Lbl_Car", "COVERED CAR PARKING\n9'-0\" x 18'-0\" [SEDAN/SUV]", 5.2, PLINTH_D - 3.0, size=0.22, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Bikes", "2-WHEELER PARKING BAYS\n(4 MOTORCYCLES)", 8.25, PLINTH_D - 3.0, size=0.20, color=COLOR_TEXT, collection=col)

    add_cad_text("Lbl_Garden_N", "NORTH FRONT GARDEN & LAWN (15' DEEP CLEAR SETBACK)", 5.6, PLINTH_D + 1.2, size=0.24, color=(0.1, 0.5, 0.2, 1.0), collection=col)
    add_cad_text("Lbl_Garden_E", "EAST MORNING GARDEN", PLINTH_W + 1.1, 6.0, size=0.22, rot_z=math.radians(-90), color=(0.1, 0.5, 0.2, 1.0), collection=col)

    add_cad_text("Lbl_Stairs", "EXTERNAL DOG-LEGGED STAIRS\n7'-3\" x 11'-0\" [NW VAYU]", -1.35, 7.8, z=0.95, size=0.20, rot_z=math.radians(90), color=(0.10, 0.12, 0.16, 1.0), collection=col)
    add_cad_text("Lbl_Lift", "6-PAX PASSENGER LIFT\n(1.6m x 1.6m CLEAR CORE)", -1.35, 10.8, size=0.19, rot_z=math.radians(90), color=(0.1, 0.15, 0.25, 1.0), collection=col)

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
    mat_cupboard = get_or_create_material("Mat_Cupboard", COLOR_CUPBOARD)
    mat_pooja = get_or_create_material("Mat_Pooja", COLOR_POOJA)
    mat_balcony = get_or_create_material("Mat_Balcony", COLOR_BALCONY)
    
    # 1. Base Slab & Columns
    create_box("Floor1_Slab", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_slab, col)
    add_columns(col)
    
    # 2. External Vertical Core (NW Vayu Zone)
    add_external_vertical_core(col)
    
    # 3. BALCONIES (North, East/Ishanya, South) & External Utility
    # North Balcony (off Bed 2): X: 3.81 to 7.31, Y: 12.19 to 13.49 (11'6" x 4'3")
    create_box("Balcony_North_Slab", 3.81, PLINTH_D, 7.31, PLINTH_D + 1.30, 0, 0.05, mat_balcony, col)
    create_box("Balcony_North_Rail", 3.81, PLINTH_D + 1.25, 7.31, PLINTH_D + 1.30, 0, WALL_H * 0.9, mat_int, col)
    
    # East / North-East Sitout Balcony (LEFT OPEN FOR ISHANYA LIGHT): X: 7.31 to PLINTH_W, Y: 8.5 to PLINTH_D (13'0" x 12'0")
    create_box("Balcony_East_Slab", 7.31, 8.5, PLINTH_W, PLINTH_D, 0, 0.05, mat_balcony, col)
    create_box("Balcony_East_Rail_N", 7.31, PLINTH_D - 0.1, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    create_box("Balcony_East_Rail_E", PLINTH_W - 0.1, 8.5, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    
    # South Shaded Balcony (off Master Bed): X: 0 to 3.81, Y: -1.2 to 0 (12'6" x 4'0")
    create_box("Balcony_South_Slab", 0, -1.2, 3.81, 0, 0, 0.05, mat_balcony, col)
    create_box("Balcony_South_Rail", 0, -1.2, 3.81, -1.15, 0, WALL_H * 0.9, mat_int, col)
    
    # External Out-of-House Utility Balcony (off Kitchen SE): X: PLINTH_W, Y: 0 to 3.5, width 1.4m
    create_box("Utility_East_Slab", PLINTH_W, 0, PLINTH_W + 1.4, 3.5, 0, 0.05, mat_balcony, col)
    create_box("Utility_East_Rail", PLINTH_W + 1.35, 0, PLINTH_W + 1.4, 3.5, 0, WALL_H * 0.9, mat_int, col)

    # 4. EXTERIOR WALLS WITH GLAZED OPENINGS
    # South Wall (Master Bed & Living)
    create_box("Ext_S_1", 0, 0, 1.2, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_MB_South_Balcony", 1.2, EXT_WALL_THICK, 0.90, 90, 'S', None, col) # Door to South Balcony
    create_box("Ext_S_2", 2.1, 0, 3.81, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_box("Ext_S_3", 3.81, 0, 7.31, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_box("Ext_S_4", 7.31, 0, PLINTH_W, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    # East Wall (Kitchen SE & Living)
    create_box("Ext_E_1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 1.2, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_Kit_Utility", PLINTH_W - EXT_WALL_THICK, 1.2, 0.85, 90, 'E', None, col) # Door to External Utility
    create_box("Ext_E_2", PLINTH_W - EXT_WALL_THICK, 2.05, PLINTH_W, 3.8, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Kit_E", PLINTH_W - EXT_WALL_THICK, 2.2, PLINTH_W, 3.4, None, col)
    create_box("Ext_E_3", PLINTH_W - EXT_WALL_THICK, 3.8, PLINTH_W, 5.0, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Liv_E", PLINTH_W - EXT_WALL_THICK, 5.0, PLINTH_W, 7.2, None, col)
    create_box("Ext_E_4", PLINTH_W - EXT_WALL_THICK, 7.2, PLINTH_W, 8.5, 0, WALL_H, mat_ext, col)

    # North Wall (Bed 2 & Simhadwaram Entrance Wall)
    create_box("Ext_N_W1", 0, PLINTH_D - EXT_WALL_THICK, 1.5, PLINTH_D, 0, WALL_H, mat_ext, col)
    # SIMHADWARAM ENTRANCE (NNE Facing D1 Door entered from external landing):
    create_door_2d("Simhadwaram_D1", 1.5, PLINTH_D - EXT_WALL_THICK, 1.05, 90, 'S', None, col)
    create_box("Ext_N_W2", 2.55, PLINTH_D - EXT_WALL_THICK, 3.81, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_box("Ext_N_W3", 3.81, PLINTH_D - EXT_WALL_THICK, 4.8, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_B2_North_Balcony", 4.8, PLINTH_D - EXT_WALL_THICK, 0.90, 90, 'N', None, col) # Door to North Balcony
    create_window_2d("Win_B2_N", 5.8, PLINTH_D - EXT_WALL_THICK, 7.2, PLINTH_D, None, col)
    create_box("Ext_N_W4", 7.2, PLINTH_D - EXT_WALL_THICK, 7.31, PLINTH_D, 0, WALL_H, mat_ext, col)

    # West Wall (Master Bed & Bathrooms)
    create_box("Ext_W_1", 0, EXT_WALL_THICK, EXT_WALL_THICK, 4.06, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_MB_W", 0, 1.5, EXT_WALL_THICK, 3.0, None, col)
    create_box("Ext_W_2", 0, 4.06, EXT_WALL_THICK, 6.7, 0, WALL_H, mat_ext, col)
    create_window_2d("Vent_Baths", 0, 5.0, EXT_WALL_THICK, 5.8, None, col)
    create_box("Ext_W_3", 0, 6.7, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_ext, col)

    # 5. INTERIOR PARTITION WALLS (4.5" / 115mm)
    # Master Bedroom (SW Niruthi): 12'6" x 13'4" (3.81m x 4.06m)
    create_box("MB_Wall_E", 3.81 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.81 + INT_WALL_THICK/2, 4.06, 0, WALL_H, mat_int, col)
    create_box("MB_Wall_N_1", EXT_WALL_THICK, 4.06 - INT_WALL_THICK/2, 0.5, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    # ATTACHED BATH DOOR (RESOLVED!):
    create_door_2d("Door_AttBath", 0.5, 4.06, 0.75, 90, 'N', None, col)
    create_box("MB_Wall_N_2", 1.25, 4.06 - INT_WALL_THICK/2, 2.7, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    # Master Bedroom Main Door:
    create_door_2d("Door_MB", 2.7, 4.06, 0.90, 90, 'S', None, col)
    create_box("MB_Wall_N_3", 3.6, 4.06 - INT_WALL_THICK/2, 3.81, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Spacious Bathrooms (West Varuna): 6'0" x 8'6" (1.83m x 2.60m)
    create_box("Bath_Div_Wall", 1.83 - INT_WALL_THICK/2, 4.06, 1.83 + INT_WALL_THICK/2, 6.66, 0, WALL_H, mat_int, col)
    create_box("Bath_North_Wall", EXT_WALL_THICK, 6.66 - INT_WALL_THICK/2, 3.81, 6.66 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Bath_East_Wall_1", 3.81 - INT_WALL_THICK/2, 4.06, 3.81 + INT_WALL_THICK/2, 5.2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_CommonBath", 3.81, 5.2, 0.75, 90, 'W', None, col)
    create_box("Bath_East_Wall_2", 3.81 - INT_WALL_THICK/2, 5.95, 3.81 + INT_WALL_THICK/2, 6.66, 0, WALL_H, mat_int, col)

    # Kitchen (SE Agneya): 12'6" x 11'6" (3.81m x 3.50m)
    create_box("Kit_Wall_W", 7.31 - INT_WALL_THICK/2, EXT_WALL_THICK, 7.31 + INT_WALL_THICK/2, 2.2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Kit", 7.31, 2.2, 0.90, 90, 'W', None, col)
    create_box("Kit_Wall_W2", 7.31 - INT_WALL_THICK/2, 3.1, 7.31 + INT_WALL_THICK/2, 3.5, 0, WALL_H, mat_int, col)
    create_box("Kit_Wall_N", 7.31, 3.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 3.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Bedroom 2 (North): 11'6" x 11'6" (3.50m x 3.50m)
    create_box("B2_Wall_W", 3.81 - INT_WALL_THICK/2, 8.5, 3.81 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("B2_Wall_E", 7.31 - INT_WALL_THICK/2, 8.5, 7.31 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("B2_Wall_S_1", 3.81, 8.5 - INT_WALL_THICK/2, 5.0, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_B2", 5.0, 8.5, 0.90, 90, 'N', None, col)
    create_box("B2_Wall_S_2", 5.9, 8.5 - INT_WALL_THICK/2, 7.31, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # POOJA MANDIR & GLAZED LIGHT DOOR TO OPEN ISHANYA SITOUT:
    # Wall separating living from Ishanya open sitout: Y = 8.5, X from 7.31 to PLINTH_W
    create_box("Ishanya_Wall_1", 7.31, 8.5 - INT_WALL_THICK/2, 8.2, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    # Glazed Double Door for Morning Ishanya Light:
    create_door_2d("Door_Ishanya_Light", 8.2, 8.5, 1.20, 90, 'E', None, col)
    create_box("Ishanya_Wall_2", 9.4, 8.5 - INT_WALL_THICK/2, 10.0, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Pooja", 10.0, 8.5, 0.80, 90, 'N', None, col)
    create_box("Ishanya_Wall_3", 10.8, 8.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    # Pooja Mandir East enclosure:
    create_box("Pooja_Wall_W", 10.0 - INT_WALL_THICK/2, 8.5, 10.0 + INT_WALL_THICK/2, 10.5, 0, WALL_H, mat_int, col)
    create_box("Pooja_Wall_N", 10.0, 10.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 10.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # 6. COMPLETE BUILT-IN CUPBOARDS & INTERIOR MILLWORK
    # Master Bedroom Wardrobe (Full width west wall, 2'0" deep)
    create_box("MB_Wardrobe", EXT_WALL_THICK, 0.35, EXT_WALL_THICK + 0.60, 3.8, 0, 1.10, mat_cupboard, col)
    # Master King Bed (Headboard to South Wall)
    create_box("MB_Bed", 1.4, EXT_WALL_THICK + 0.1, 3.4, EXT_WALL_THICK + 2.1, 0, 0.45, mat_bed, col)
    create_box("MB_Headboard", 1.3, EXT_WALL_THICK, 3.5, EXT_WALL_THICK + 0.1, 0, 0.75, mat_bed, col)
    create_box("MB_TV_Console", 3.81 - INT_WALL_THICK/2 - 0.35, 1.5, 3.81 - INT_WALL_THICK/2, 3.2, 0, 0.60, mat_furn, col)

    # Bedroom 2 Wardrobe & Queen Bed
    create_box("B2_Wardrobe", 3.81 + INT_WALL_THICK/2, 9.2, 3.81 + 0.60, 11.8, 0, 1.10, mat_cupboard, col)
    create_box("B2_Bed", 4.8, PLINTH_D - EXT_WALL_THICK - 2.1, 6.6, PLINTH_D - EXT_WALL_THICK - 0.1, 0, 0.45, mat_bed, col)
    create_box("B2_Study_Desk", 6.2, 8.6, 7.2, 9.4, 0, 0.75, mat_furn, col)

    # Kitchen Modular Cabinets & L-Counter (Granite)
    create_box("Kit_Counter_E", PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK, 3.4, 0, 0.85, mat_kit, col)
    create_box("Kit_Counter_S", 7.4, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK + 0.65, 0, 0.85, mat_kit, col)
    create_box("Kit_Pantry_Cupboard", 7.4, 2.5, 7.9, 3.4, 0, 1.20, mat_cupboard, col) # Tall pantry unit
    create_box("Kit_Stove", PLINTH_W - EXT_WALL_THICK - 0.60, 2.1, PLINTH_W - EXT_WALL_THICK - 0.10, 2.9, 0.86, 0.88, mat_pooja, col)
    create_box("Kit_Sink", PLINTH_W - EXT_WALL_THICK - 0.60, 1.0, PLINTH_W - EXT_WALL_THICK - 0.10, 1.6, 0.86, 0.87, mat_slab, col)

    # Living & Dining Millwork (Grand Brahmasthana)
    # L-Shaped Sectional Sofa
    create_box("Sofa_Main", 4.2, 5.0, 7.0, 5.9, 0, 0.65, mat_bed, col)
    create_box("Sofa_L_Ext", 4.2, 5.9, 5.1, 7.5, 0, 0.65, mat_bed, col)
    create_box("Coffee_Table", 5.5, 6.2, 6.7, 7.2, 0, 0.40, mat_furn, col)
    # Entertainment Wall TV Unit (along West Bath Wall)
    create_box("Living_TV_Unit", 3.81 + INT_WALL_THICK/2, 4.5, 3.81 + 0.45, 6.5, 0, 1.10, mat_cupboard, col)
    # Dining Table (6-Seater)
    create_box("Dining_Table", 5.0, 2.2, 6.6, 3.6, 0, 0.75, mat_furn, col)

    # External Utility Washing Machine & Laundry Sink
    create_box("Utility_Wash_Machine", PLINTH_W + 0.2, 0.4, PLINTH_W + 0.9, 1.1, 0, 0.85, mat_furn, col)
    create_box("Utility_Sink", PLINTH_W + 0.2, 1.6, PLINTH_W + 0.8, 2.4, 0, 0.75, mat_kit, col)

    # Grids, Dimensions, Title Block
    add_column_grids_and_dimensions(col)
    add_title_block("First Floor - Brother's 2BHK Residence", col)

    # Room Annotations
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
    scene = setup_scene("Second_Floor_Owner")
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
    
    # 1. Base Slab & Columns
    create_box("Floor2_Slab", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_slab, col)
    add_columns(col)
    
    # 2. External Vertical Core (NW Vayu Zone)
    add_external_vertical_core(col)
    
    # 3. BALCONIES (North, East/Ishanya, South) & External Utility
    # North Balcony (off Home Office & Bed 2): X: 3.81 to 7.31, Y: 12.19 to 13.49
    create_box("Balcony_North_Slab", 3.81, PLINTH_D, 7.31, PLINTH_D + 1.30, 0, 0.05, mat_balcony, col)
    create_box("Balcony_North_Rail", 3.81, PLINTH_D + 1.25, 7.31, PLINTH_D + 1.30, 0, WALL_H * 0.9, mat_int, col)
    
    # East / North-East Sitout Balcony (LEFT OPEN FOR ISHANYA LIGHT): X: 7.31 to PLINTH_W, Y: 8.5 to PLINTH_D
    create_box("Balcony_East_Slab", 7.31, 8.5, PLINTH_W, PLINTH_D, 0, 0.05, mat_balcony, col)
    create_box("Balcony_East_Rail_N", 7.31, PLINTH_D - 0.1, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    create_box("Balcony_East_Rail_E", PLINTH_W - 0.1, 8.5, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    
    # South Shaded Balcony (off Master Bed): X: 0 to 3.81, Y: -1.2 to 0
    create_box("Balcony_South_Slab", 0, -1.2, 3.81, 0, 0, 0.05, mat_balcony, col)
    create_box("Balcony_South_Rail", 0, -1.2, 3.81, -1.15, 0, WALL_H * 0.9, mat_int, col)
    
    # External Out-of-House Utility Balcony (off Kitchen SE): X: PLINTH_W, Y: 0 to 3.5, width 1.4m
    create_box("Utility_East_Slab", PLINTH_W, 0, PLINTH_W + 1.4, 3.5, 0, 0.05, mat_balcony, col)
    create_box("Utility_East_Rail", PLINTH_W + 1.35, 0, PLINTH_W + 1.4, 3.5, 0, WALL_H * 0.9, mat_int, col)

    # 4. EXTERIOR WALLS
    # South Wall
    create_box("Ext_S_1", 0, 0, 1.2, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_MB_South_Balcony", 1.2, EXT_WALL_THICK, 0.90, 90, 'S', None, col)
    create_box("Ext_S_2", 2.1, 0, 3.81, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_box("Ext_S_3", 3.81, 0, 7.31, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_box("Ext_S_4", 7.31, 0, PLINTH_W, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    # East Wall
    create_box("Ext_E_1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 1.2, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_Kit_Utility", PLINTH_W - EXT_WALL_THICK, 1.2, 0.85, 90, 'E', None, col)
    create_box("Ext_E_2", PLINTH_W - EXT_WALL_THICK, 2.05, PLINTH_W, 3.8, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Kit_E", PLINTH_W - EXT_WALL_THICK, 2.2, PLINTH_W, 3.4, None, col)
    create_box("Ext_E_3", PLINTH_W - EXT_WALL_THICK, 3.8, PLINTH_W, 5.0, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Liv_E", PLINTH_W - EXT_WALL_THICK, 5.0, PLINTH_W, 7.2, None, col)
    create_box("Ext_E_4", PLINTH_W - EXT_WALL_THICK, 7.2, PLINTH_W, 8.5, 0, WALL_H, mat_ext, col)

    # North Wall (NORTH-FACING HOME OFFICE WINDOW & SIMHADWARAM ENTRANCE)
    create_box("Ext_N_W1", 0, PLINTH_D - EXT_WALL_THICK, 1.5, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_door_2d("Simhadwaram_D1", 1.5, PLINTH_D - EXT_WALL_THICK, 1.05, 90, 'S', None, col)
    create_box("Ext_N_W2", 2.55, PLINTH_D - EXT_WALL_THICK, 3.81, PLINTH_D, 0, WALL_H, mat_ext, col)
    # NORTH-FACING HOME OFFICE WINDOW (Clear garden view!):
    create_box("Ext_N_W3", 3.81, PLINTH_D - EXT_WALL_THICK, 4.3, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Office_North", 4.3, PLINTH_D - EXT_WALL_THICK, 6.2, PLINTH_D, None, col)
    create_box("Ext_N_W4", 6.2, PLINTH_D - EXT_WALL_THICK, 7.31, PLINTH_D, 0, WALL_H, mat_ext, col)

    # West Wall
    create_box("Ext_W_1", 0, EXT_WALL_THICK, EXT_WALL_THICK, 4.06, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_MB_W", 0, 1.5, EXT_WALL_THICK, 3.0, None, col)
    create_box("Ext_W_2", 0, 4.06, EXT_WALL_THICK, 6.7, 0, WALL_H, mat_ext, col)
    create_window_2d("Vent_Baths", 0, 5.0, EXT_WALL_THICK, 5.8, None, col)
    create_box("Ext_W_3", 0, 6.7, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_ext, col)

    # 5. INTERIOR PARTITIONS (4.5" / 115mm)
    # Master Bedroom (SW Niruthi)
    create_box("MB_Wall_E", 3.81 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.81 + INT_WALL_THICK/2, 4.06, 0, WALL_H, mat_int, col)
    create_box("MB_Wall_N_1", EXT_WALL_THICK, 4.06 - INT_WALL_THICK/2, 0.5, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_AttBath", 0.5, 4.06, 0.75, 90, 'N', None, col)
    create_box("MB_Wall_N_2", 1.25, 4.06 - INT_WALL_THICK/2, 2.7, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_MB", 2.7, 4.06, 0.90, 90, 'S', None, col)
    create_box("MB_Wall_N_3", 3.6, 4.06 - INT_WALL_THICK/2, 3.81, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Spacious Bathrooms (West Varuna)
    create_box("Bath_Div_Wall", 1.83 - INT_WALL_THICK/2, 4.06, 1.83 + INT_WALL_THICK/2, 6.66, 0, WALL_H, mat_int, col)
    create_box("Bath_North_Wall", EXT_WALL_THICK, 6.66 - INT_WALL_THICK/2, 3.81, 6.66 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Bath_East_Wall_1", 3.81 - INT_WALL_THICK/2, 4.06, 3.81 + INT_WALL_THICK/2, 5.2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_CommonBath", 3.81, 5.2, 0.75, 90, 'W', None, col)
    create_box("Bath_East_Wall_2", 3.81 - INT_WALL_THICK/2, 5.95, 3.81 + INT_WALL_THICK/2, 6.66, 0, WALL_H, mat_int, col)

    # Kitchen (SE Agneya)
    create_box("Kit_Wall_W", 7.31 - INT_WALL_THICK/2, EXT_WALL_THICK, 7.31 + INT_WALL_THICK/2, 2.2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Kit", 7.31, 2.2, 0.90, 90, 'W', None, col)
    create_box("Kit_Wall_W2", 7.31 - INT_WALL_THICK/2, 3.1, 7.31 + INT_WALL_THICK/2, 3.5, 0, WALL_H, mat_int, col)
    create_box("Kit_Wall_N", 7.31, 3.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 3.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # NORTH-FACING HOME OFFICE (Executive Study): X in [3.81, 7.31], Y in [8.8, 12.19]
    create_box("Office_Wall_W", 3.81 - INT_WALL_THICK/2, 8.8, 3.81 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("Office_Wall_E", 7.31 - INT_WALL_THICK/2, 8.8, 7.31 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)
    create_box("Office_Wall_S_1", 3.81, 8.8 - INT_WALL_THICK/2, 4.8, 8.8 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Office", 4.8, 8.8, 0.90, 90, 'N', None, col)
    create_box("Office_Wall_S_2", 5.7, 8.8 - INT_WALL_THICK/2, 7.31, 8.8 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # DUAL POOJA SUITE (EAST ZONE PROGRESSION WITHOUT ATTACHING TO KITCHEN):
    # Wall dividing East Living from Pooja/Sitout zone:
    create_box("Pooja_Div_Wall_1", 7.31, 8.5 - INT_WALL_THICK/2, 8.2, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Ishanya_Light", 8.2, 8.5, 1.20, 90, 'E', None, col) # Glazed Light Door
    create_box("Pooja_Div_Wall_2", 9.4, 8.5 - INT_WALL_THICK/2, 10.0, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Mallanna_Pooja", 10.0, 8.5, 0.90, 90, 'N', None, col)
    create_box("Pooja_Div_Wall_3", 10.9, 8.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 8.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Mallanna Shrine & Daily Pooja Partitions (Detached from Kitchen!):
    # Mallanna Shrine: X in [8.8, 11.05], Y in [5.5, 8.5]
    create_box("Mallanna_Wall_W", 8.8 - INT_WALL_THICK/2, 5.5, 8.8 + INT_WALL_THICK/2, 8.5, 0, WALL_H, mat_int, col)
    create_box("Mallanna_Wall_S_1", 8.8, 5.5 - INT_WALL_THICK/2, 9.6, 5.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Mallanna_Entry", 9.6, 5.5, 0.90, 90, 'N', None, col)
    create_box("Mallanna_Wall_S_2", 10.5, 5.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 5.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    # Daily Pooja Room: X in [9.4, 11.05], Y in [8.5, 10.5]
    create_box("Daily_Pooja_Wall_W", 9.4 - INT_WALL_THICK/2, 8.5, 9.4 + INT_WALL_THICK/2, 10.5, 0, WALL_H, mat_int, col)
    create_box("Daily_Pooja_Wall_N", 9.4, 10.5 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 10.5 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Daily_Pooja", 9.5, 8.5, 0.80, 90, 'N', None, col)

    # 6. COMPLETE MILLWORK & BUILT-IN CUPBOARDS
    # Master Bedroom
    create_box("MB_Wardrobe", EXT_WALL_THICK, 0.35, EXT_WALL_THICK + 0.60, 3.8, 0, 1.10, mat_cupboard, col)
    create_box("MB_Bed", 1.4, EXT_WALL_THICK + 0.1, 3.4, EXT_WALL_THICK + 2.1, 0, 0.45, mat_bed, col)
    create_box("MB_Headboard", 1.3, EXT_WALL_THICK, 3.5, EXT_WALL_THICK + 0.1, 0, 0.75, mat_bed, col)
    create_box("MB_TV_Console", 3.81 - INT_WALL_THICK/2 - 0.35, 1.5, 3.81 - INT_WALL_THICK/2, 3.2, 0, 0.60, mat_furn, col)

    # Executive Home Office (Executive Desk facing North/East, Bookcase Cupboards)
    create_box("Office_Desk", 4.6, 10.0, 6.4, 10.8, 0, 0.75, mat_furn, col)
    create_box("Office_Cupboard_Wall", 3.81 + INT_WALL_THICK/2, 9.2, 3.81 + 0.55, 11.8, 0, 1.10, mat_cupboard, col)
    create_box("Office_Lounge_Chair", 6.2, 9.2, 7.0, 10.0, 0, 0.60, mat_bed, col)

    # Mallanna Sacred Shrine Altar & Carpet
    create_box("Mallanna_Altar", 9.0, 7.5, PLINTH_W - EXT_WALL_THICK - 0.1, 8.4, 0, 0.65, mat_pooja, col)
    create_box("Mallanna_Prayer_Carpet", 9.0, 5.8, PLINTH_W - EXT_WALL_THICK - 0.2, 7.4, 0, 0.02, mat_pooja, col)

    # Living & Dining
    create_box("Sofa_Main", 4.2, 5.0, 7.0, 5.9, 0, 0.65, mat_bed, col)
    create_box("Sofa_L_Ext", 4.2, 5.9, 5.1, 7.5, 0, 0.65, mat_bed, col)
    create_box("Coffee_Table", 5.5, 6.2, 6.7, 7.2, 0, 0.40, mat_furn, col)
    create_box("Living_TV_Unit", 3.81 + INT_WALL_THICK/2, 4.5, 3.81 + 0.45, 6.5, 0, 1.10, mat_cupboard, col)
    create_box("Dining_Table", 5.0, 2.2, 6.6, 3.6, 0, 0.75, mat_furn, col)

    # Modular Kitchen & External Utility
    create_box("Kit_Counter_E", PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK, 3.4, 0, 0.85, mat_kit, col)
    create_box("Kit_Counter_S", 7.4, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK + 0.65, 0, 0.85, mat_kit, col)
    create_box("Kit_Pantry_Cupboard", 7.4, 2.5, 7.9, 3.4, 0, 1.20, mat_cupboard, col)
    create_box("Kit_Stove", PLINTH_W - EXT_WALL_THICK - 0.60, 2.1, PLINTH_W - EXT_WALL_THICK - 0.10, 2.9, 0.86, 0.88, mat_pooja, col)
    create_box("Kit_Sink", PLINTH_W - EXT_WALL_THICK - 0.60, 1.0, PLINTH_W - EXT_WALL_THICK - 0.10, 1.6, 0.86, 0.87, mat_slab, col)
    create_box("Utility_Wash_Machine", PLINTH_W + 0.2, 0.4, PLINTH_W + 0.9, 1.1, 0, 0.85, mat_furn, col)
    create_box("Utility_Sink", PLINTH_W + 0.2, 1.6, PLINTH_W + 0.8, 2.4, 0, 0.75, mat_kit, col)

    # Grids, Dimensions, Title Block
    add_column_grids_and_dimensions(col)
    add_title_block("Second Floor - Owner's Residence", col)

    # Room Annotations
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
    print("Starting Blender 2D Architectural CAD Generation (Redesigned Plan)...")
    build_ground_stilt()
    build_first_floor_brother()
    build_second_floor_owner()
    
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_FILE))
    print(f"Master Project Saved: {BLEND_FILE}")
