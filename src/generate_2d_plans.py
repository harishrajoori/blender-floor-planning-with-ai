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
    mat_furn = get_or_create_material("Mat_Furniture", COLOR_FURNITURE)
    
    core_x0 = -2.40
    core_x1 = 0.0
    core_y0 = 6.50
    core_y1 = 12.19
    
    # Plinth Base for Core
    create_box("Core_Slab", core_x0, core_y0, core_x1, core_y1, 0, 0.08, mat_slab, collection)
    
    # Staircase Walls
    create_box("Core_Wall_W", core_x0, core_y0, core_x0 + 0.15, core_y1, 0, WALL_H, mat_ext, collection)
    create_box("Core_Wall_N", core_x0, core_y1 - 0.15, core_x1, core_y1, 0, WALL_H, mat_ext, collection)
    create_box("Core_Wall_S", core_x0, core_y0, core_x1, core_y0 + 0.15, 0, WALL_H, mat_ext, collection)
    create_box("Core_Mid_Wall", core_x0, 9.80 - 0.08, core_x1, 9.80 + 0.08, 0, WALL_H, mat_int, collection)
    
    # Dog-legged Stairs (Treads from y=6.65 to 9.70)
    stair_w = (core_x1 - core_x0 - 0.15 - 0.10) / 2.0
    num_treads = 10
    tread_d = (9.70 - 7.50) / num_treads
    for t in range(num_treads):
        ty0 = 7.50 + t * tread_d
        ty1 = ty0 + tread_d
        create_box(f"Stair_Up_Tr_{t}", core_x0 + 0.15, ty0, core_x0 + 0.15 + stair_w, ty1, 0, 0.08 + (t+1)*0.02, mat_furn, collection)
        create_box(f"Stair_Dn_Tr_{t}", core_x1 - stair_w, ty0, core_x1, ty1, 0, 0.35 + (t+1)*0.02, mat_furn, collection)
        
    create_box("Stair_Mid_Landing", core_x0 + 0.15, 6.65, core_x1, 7.50, 0, 0.30, mat_slab, collection)
    
    # 6-PAX Lift Enclosure (from y=9.88 to 12.04)
    create_box("Lift_Shaft_Box", core_x0 + 0.15, 9.90, core_x1, 12.04, 0, WALL_H, mat_ext, collection)
    create_box("Lift_Cabin", core_x0 + 0.35, 10.15, core_x1 - 0.20, 11.85, 0.05, WALL_H * 0.95, mat_slab, collection)
    create_door_2d("Lift_Telescopic_Door", core_x1 - 0.02, 10.55, 0.90, 90, 'W', None, collection)

def add_title_block(sheet_title, collection, is_ground=False):
    mat_paper = get_or_create_material("Mat_TitlePaper", (0.98, 0.98, 0.99, 1.0))
    mat_border = get_or_create_material("Mat_TitleBorder", COLOR_EXT_WALL)
    
    bx = PLOT_X1 + 1.2 if is_ground else PLINTH_W + 1.2
    by = 2.6
    bw = 4.8
    bh = 6.5
    
    create_box("Title_Block_Bg", bx, by, bx + bw, by + bh, 0.01, 0.03, mat_paper, collection)
    create_box("Title_Border_Out", bx, by, bx + bw, by + bh, 0.03, 0.05, mat_border, collection)
    create_box("Title_Border_In", bx + 0.06, by + 0.06, bx + bw - 0.06, by + bh - 0.06, 0.04, 0.05, mat_paper, collection)
    
    cx = bx + bw / 2.0
    add_cad_text("TB_Title1", "PROPERTY 2 RESIDENCE", cx, by + 5.9, size=0.28, color=(0.05, 0.1, 0.2, 1.0), collection=collection)
    add_cad_text("TB_Title2", sheet_title.upper(), cx, by + 5.4, size=0.20, color=(0.05, 0.55, 0.45, 1.0), collection=collection)
    
    specs = [
        "PLOT: 54'-0\" x 66'-0\" (SW Corner, 3,564 sf)",
        "PLINTH: 37'-0\" x 40'-0\" (1,480 sf Footprint)",
        "SETBACKS: N:17' E:9' S:9' W:8' (Vaastu Compliant)",
        "CORE: External NW Stairs & 6-PAX Lift",
        "VAASTU: Telugu / Telangana (Open Ishanya NE)",
        "ENTRANCE: North-North-East (NNE) Simhadwaram",
        "POOJA: Both Doors West-Facing (Detached)",
        "BATHS: 6'0\" x 8'6\" Spacious Wet/Dry Stacks",
        "BALCONIES: North (from Office), East & South",
        "MILLWORK: Complete Built-in Cupboards & Desks"
    ]
    
    for i, sp in enumerate(specs):
        add_cad_text(f"TB_Spec_{i}", sp, bx + 0.25, by + 4.8 - i * 0.42, size=0.14, align_x='LEFT', color=(0.15, 0.2, 0.3, 1.0), collection=collection)

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
    scene.render.resolution_y = 2000 if is_ground else 1800
    scene.render.resolution_percentage = 100
    
    cam_name = f"Camera_{name}"
    cam_data = bpy.data.cameras.new(name=cam_name)
    cam_data.type = 'ORTHO'
    
    if is_ground:
        cam_data.ortho_scale = 32.0
        cam_x = (PLOT_X0 + PLOT_X1) / 2.0 + 1.2
        cam_y = (PLOT_Y0 + PLOT_Y1) / 2.0
    else:
        cam_data.ortho_scale = 22.0
        cam_x = PLINTH_W / 2.0 + 1.2
        cam_y = PLINTH_D / 2.0
        
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
# SCENE 2 & 3 BUILDER: UPPER FLOORS (L1 BROTHER 2BHK & L2 OWNER RESIDENCE)
# =============================================================================
def build_upper_floor(scene_name, is_owner_level=False):
    scene = setup_scene(scene_name, is_ground=False)
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
    
    # 1. Base Slab, External Core & Columns
    create_box(f"{scene_name}_Slab", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_slab, col)
    add_columns(col)
    add_external_vertical_core(col)
    
    # 2. Covered North Verandah / Walkway Deck
    # Runs from NW core landing (x=0) to NNE Simhadwaram (x=7.315), width y=12.19 to 13.50 (4'-3" wide)
    create_box("North_Verandah_Slab", 0.0, PLINTH_D, 7.315, PLINTH_D + 1.31, 0, 0.06, mat_balcony, col)
    create_box("North_Verandah_Railing", 0.0, PLINTH_D + 1.25, 7.315, PLINTH_D + 1.31, 0, WALL_H * 0.9, mat_int, col)
    
    # 3. East Open Sitout (Ishanya NE Corner Terrace - Open to Sky)
    # x=7.315 to 11.277, y=9.72 to 12.19 (13' x 8')
    create_box("Ishanya_Terrace_Slab", 7.315, 9.72, PLINTH_W, PLINTH_D, 0, 0.05, mat_balcony, col)
    create_box("Ishanya_Rail_North", 7.315, PLINTH_D - 0.10, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    create_box("Ishanya_Rail_East", PLINTH_W - 0.10, 9.72, PLINTH_W, PLINTH_D, 0, WALL_H * 0.9, mat_int, col)
    
    # 4. South Shaded Balcony
    create_box("Balcony_South_Slab", 0, -1.2, 7.315, 0, 0, 0.05, mat_balcony, col)
    create_box("Balcony_South_Rail", 0, -1.2, 7.315, -1.15, 0, WALL_H * 0.9, mat_int, col)
    
    # 5. Out-of-House Utility Balcony (SE Agneya, attached to kitchen)
    create_box("Utility_East_Slab", PLINTH_W, 0, PLINTH_W + 1.40, 3.80, 0, 0.05, mat_balcony, col)
    create_box("Utility_East_Rail", PLINTH_W + 1.35, 0, PLINTH_W + 1.40, 3.80, 0, WALL_H * 0.9, mat_int, col)

    # 6. Exterior Walls (9" / 0.23m)
    # South Wall (y = 0 to 0.23)
    create_box("Ext_S_1", 0, 0, 1.2, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_MB_South_Balcony", 1.2, EXT_WALL_THICK, 0.90, 90, 'S', None, col)
    create_box("Ext_S_2", 2.1, 0, 3.81, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_box("Ext_S_3", 3.81, 0, 5.0, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_Dining_South_Balcony", 5.0, EXT_WALL_THICK, 1.20, 90, 'S', None, col)
    create_box("Ext_S_4", 6.2, 0, PLINTH_W, EXT_WALL_THICK, 0, WALL_H, mat_ext, col)
    
    # East Wall (x = PLINTH_W - 0.23 to PLINTH_W)
    create_box("Ext_E_1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 1.2, 0, WALL_H, mat_ext, col)
    create_door_2d("Door_Kit_Utility", PLINTH_W - EXT_WALL_THICK, 1.2, 0.85, 90, 'E', None, col)
    create_box("Ext_E_2", PLINTH_W - EXT_WALL_THICK, 2.05, PLINTH_W, 3.8, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Kit_E", PLINTH_W - EXT_WALL_THICK, 2.2, PLINTH_W, 3.4, None, col)
    create_box("Ext_E_Pooja", PLINTH_W - EXT_WALL_THICK, 4.60, PLINTH_W, 9.60, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_Pooja_E", PLINTH_W - EXT_WALL_THICK, 5.5, PLINTH_W, 6.5, None, col)
    create_window_2d("Win_DailyPooja_E", PLINTH_W - EXT_WALL_THICK, 8.0, PLINTH_W, 8.8, None, col)
    
    # North Wall (y = PLINTH_D - 0.23 to PLINTH_D)
    # NW Office / Bedroom 2 North Wall
    create_box("Ext_N_NW1", 0, PLINTH_D - EXT_WALL_THICK, 1.2, PLINTH_D, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_NW_North", 1.2, PLINTH_D - EXT_WALL_THICK, 2.7, PLINTH_D, None, col)
    create_box("Ext_N_NW2", 2.7, PLINTH_D - EXT_WALL_THICK, 2.9, PLINTH_D, 0, WALL_H, mat_ext, col)
    # Direct Balcony Entrance from Office / Bedroom 2!
    create_door_2d("Door_Office_North_Balcony", 2.9, PLINTH_D - EXT_WALL_THICK, 0.90, 90, 'N', None, col)
    create_box("Ext_N_NW3", 3.8, PLINTH_D - EXT_WALL_THICK, 6.0, PLINTH_D, 0, WALL_H, mat_ext, col)
    
    # NNE Simhadwaram Main Entrance (x=6.0 to 7.10) - Pure North-North-East, entering Grand Living Hall!
    create_door_2d("Simhadwaram_D1_NNE", 6.0, PLINTH_D - EXT_WALL_THICK, 1.10, 90, 'S', None, col)
    create_box("Ext_N_NNE_Post", 7.10, PLINTH_D - EXT_WALL_THICK, 7.315, PLINTH_D, 0, WALL_H, mat_ext, col)

    # West Wall (x = 0 to 0.23)
    create_box("Ext_W_1", 0, EXT_WALL_THICK, EXT_WALL_THICK, 4.06, 0, WALL_H, mat_ext, col)
    create_window_2d("Win_MB_W", 0, 1.5, EXT_WALL_THICK, 3.0, None, col)
    create_box("Ext_W_2", 0, 4.06, EXT_WALL_THICK, 7.60, 0, WALL_H, mat_ext, col)
    create_window_2d("Vent_Baths_W", 0, 5.2, EXT_WALL_THICK, 6.2, None, col)
    create_box("Ext_W_3", 0, 7.60, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_ext, col)

    # 7. Interior Partitions (4.5" / 0.115m)
    # Master Bedroom (SW Niruthi: x=0.23 to 3.81, y=0.23 to 4.06)
    create_box("MB_Wall_E", 3.81 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.81 + INT_WALL_THICK/2, 3.2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_MB_Entry", 3.81, 3.2, 0.86, 90, 'W', None, col)
    
    # Master Bedroom North Wall (y=4.06) - connects to Attached Bath privately
    create_box("MB_Wall_N_1", EXT_WALL_THICK, 4.06 - INT_WALL_THICK/2, 0.8, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_door_2d("Door_MB_AttBath", 0.8, 4.06, 0.76, 90, 'N', None, col)
    create_box("MB_Wall_N_2", 1.56, 4.06 - INT_WALL_THICK/2, 3.81, 4.06 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # Bathrooms Complex (West Varuna: x=0.23 to 3.81, y=4.18 to 7.60)
    # Dividing wall between Attached Bath (West) and Common Bath (East)
    create_box("Bath_Dividing_Wall", 1.95 - INT_WALL_THICK/2, 4.18, 1.95 + INT_WALL_THICK/2, 7.60, 0, WALL_H, mat_int, col)
    create_box("Bath_North_Wall", EXT_WALL_THICK, 7.60 - INT_WALL_THICK/2, 3.81, 7.60 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    
    # Common Bathroom East Wall (x=3.81) - WITH DIRECT UNBLOCKED DOOR FROM LIVING HALL!
    create_box("CommonBath_East_Wall_1", 3.81 - INT_WALL_THICK/2, 4.18, 3.81 + INT_WALL_THICK/2, 5.20, 0, WALL_H, mat_int, col)
    create_door_2d("Door_CommonBath_East", 3.81, 5.20, 0.80, 90, 'W', None, col)
    create_box("CommonBath_East_Wall_2", 3.81 - INT_WALL_THICK/2, 6.00, 3.81 + INT_WALL_THICK/2, 7.60, 0, WALL_H, mat_int, col)

    # Kitchen (SE Agneya: x=7.315 to PLINTH_W-0.23, y=0.23 to 3.80)
    create_box("Kit_Wall_W1", 7.315 - INT_WALL_THICK/2, EXT_WALL_THICK, 7.315 + INT_WALL_THICK/2, 2.0, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Kit_Entry", 7.315, 2.0, 0.90, 90, 'W', None, col)
    create_box("Kit_Wall_W2", 7.315 - INT_WALL_THICK/2, 2.9, 7.315 + INT_WALL_THICK/2, 3.80, 0, WALL_H, mat_int, col)
    create_box("Kit_Wall_N", 7.315, 3.80 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 3.80 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)

    # NW Room (Home Office on L2 / Bedroom 2 on L1: x=0.23 to 4.00, y=7.72 to 11.96)
    create_box("NW_Room_Wall_S", EXT_WALL_THICK, 7.72 - INT_WALL_THICK/2, 4.00, 7.72 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("NW_Room_Wall_E1", 4.00 - INT_WALL_THICK/2, 7.72, 4.00 + INT_WALL_THICK/2, 8.30, 0, WALL_H, mat_int, col)
    create_door_2d("Door_NW_Room_Entry", 4.00, 8.30, 0.90, 90, 'W', None, col)
    create_box("NW_Room_Wall_E2", 4.00 - INT_WALL_THICK/2, 9.20, 4.00 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)

    # Pooja Rooms Complex (East Zone, buffered from kitchen by dining passage)
    # Mallanna Temple Room (x=8.50 to 11.05 [8'-4" width], y=4.60 to 7.04 [8'-0" depth])
    create_box("Mallanna_Wall_S", 8.50, 4.60 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 4.60 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Mallanna_Wall_N", 8.50, 7.04 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 7.04 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("Mallanna_Wall_W1", 8.50 - INT_WALL_THICK/2, 4.60, 8.50 + INT_WALL_THICK/2, 5.20, 0, WALL_H, mat_int, col)
    # Mallanna Door ON WEST WALL entering from Living/Dining!
    create_door_2d("Door_Mallanna_West", 8.50, 5.20, 0.90, 90, 'E', None, col)
    create_box("Mallanna_Wall_W2", 8.50 - INT_WALL_THICK/2, 6.10, 8.50 + INT_WALL_THICK/2, 7.04, 0, WALL_H, mat_int, col)

    # Daily Pooja Room (x=8.50 to 11.05, y=7.16 to 9.60 [8'-4" length matching Mallanna width])
    create_box("DailyPooja_Wall_N", 8.50, 9.60 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 9.60 + INT_WALL_THICK/2, 0, WALL_H, mat_int, col)
    create_box("DailyPooja_Wall_W1", 8.50 - INT_WALL_THICK/2, 7.16, 8.50 + INT_WALL_THICK/2, 7.80, 0, WALL_H, mat_int, col)
    # Daily Pooja Door ON WEST WALL entering from Living Hall!
    create_door_2d("Door_DailyPooja_West", 8.50, 7.80, 0.80, 90, 'E', None, col)
    create_box("DailyPooja_Wall_W2", 8.50 - INT_WALL_THICK/2, 8.60, 8.50 + INT_WALL_THICK/2, 9.60, 0, WALL_H, mat_int, col)

    # Ishanya Glazed Light Door on West wall of Ishanya Open Sitout (x=7.315, y=9.72 to 12.19)
    create_box("Ishanya_Inner_Wall_S", 7.315 - INT_WALL_THICK/2, 9.60, 8.50, 9.72, 0, WALL_H, mat_int, col)
    create_box("Ishanya_Inner_Wall_W1", 7.315 - INT_WALL_THICK/2, 9.72, 7.315 + INT_WALL_THICK/2, 10.30, 0, WALL_H, mat_int, col)
    create_door_2d("Door_Ishanya_Glazed_Light", 7.315, 10.30, 1.20, 90, 'W', None, col)
    create_box("Ishanya_Inner_Wall_W2", 7.315 - INT_WALL_THICK/2, 11.50, 7.315 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, WALL_H, mat_int, col)

    # 8. Millwork, Furniture & Fixtures
    # Master Bedroom (SW Niruthi)
    create_box("MB_Wardrobe", EXT_WALL_THICK + 0.1, 0.35, EXT_WALL_THICK + 0.70, 3.80, 0, 1.10, mat_cupboard, col)
    create_box("MB_Bed", 1.4, EXT_WALL_THICK + 0.15, 3.4, EXT_WALL_THICK + 2.15, 0, 0.45, mat_bed, col)
    create_box("MB_Headboard", 1.3, EXT_WALL_THICK + 0.05, 3.5, EXT_WALL_THICK + 0.15, 0, 0.75, mat_bed, col)

    # Attached Bath & Common Bath Fixtures
    create_box("AttBath_Shower", EXT_WALL_THICK + 0.1, 6.2, 1.95 - 0.1, 7.5, 0, 0.15, mat_balcony, col)
    create_box("AttBath_Vanity", EXT_WALL_THICK + 0.1, 4.3, EXT_WALL_THICK + 0.6, 5.3, 0, 0.85, mat_furn, col)
    create_box("CommonBath_Shower", 2.05 + 0.1, 6.2, 3.81 - 0.1, 7.5, 0, 0.15, mat_balcony, col)
    create_box("CommonBath_Vanity", 3.81 - 0.6, 6.3, 3.81 - 0.1, 7.3, 0, 0.85, mat_furn, col)

    # Kitchen Counter & Appliances (SE Agneya)
    create_box("Kit_Counter_E", PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK, 3.70, 0, 0.85, mat_kit, col)
    create_box("Kit_Counter_S", 7.40, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK + 0.65, 0, 0.85, mat_kit, col)
    create_box("Kit_Stove_EastHob", PLINTH_W - EXT_WALL_THICK - 0.60, 2.2, PLINTH_W - EXT_WALL_THICK - 0.10, 3.0, 0.86, 0.88, mat_pooja, col)
    create_box("Kit_Sink", PLINTH_W - EXT_WALL_THICK - 0.60, 1.0, PLINTH_W - EXT_WALL_THICK - 0.10, 1.6, 0.86, 0.87, mat_slab, col)

    # Out-of-House Utility
    create_box("Utility_Wash_Machine", PLINTH_W + 0.2, 0.4, PLINTH_W + 0.9, 1.1, 0, 0.85, mat_furn, col)
    create_box("Utility_Gas_Cage", PLINTH_W + 0.2, 1.5, PLINTH_W + 0.8, 2.3, 0, 0.90, mat_int, col)

    # Dining Table (South-Central, adjacent to kitchen)
    create_box("Dining_Table", 5.0, 1.8, 6.6, 3.2, 0, 0.75, mat_furn, col)

    # Grand Living Room Entertainment Wall & Sofas (TV Unit placed on Dining partition facing North!)
    create_box("Living_TV_Entertainment_Unit", 4.8, 3.80 + INT_WALL_THICK/2, 6.8, 4.25, 0, 1.10, mat_cupboard, col)
    create_box("Sofa_Living_L", 4.8, 6.2, 7.6, 7.1, 0, 0.65, mat_bed, col)
    create_box("Sofa_Living_Seat", 4.8, 7.1, 5.7, 8.6, 0, 0.65, mat_bed, col)
    create_box("Living_Coffee_Table", 6.0, 7.3, 7.2, 8.2, 0, 0.40, mat_furn, col)

    # Mallanna Altar (faces North along South wall of Mallanna room)
    create_box("Mallanna_Altar", 8.8, 4.60 + INT_WALL_THICK/2 + 0.1, 10.7, 5.3, 0, 0.95, mat_pooja, col)
    create_box("Mallanna_Carpet", 8.8, 5.5, 10.7, 6.7, 0, 0.05, mat_bed, col)

    # Daily Pooja Altar (faces East along West wall of Daily Pooja room)
    create_box("DailyPooja_Altar", 8.50 + INT_WALL_THICK/2 + 0.1, 8.0, 9.15, 9.4, 0, 0.90, mat_pooja, col)

    # NW Room Distinction (Home Office vs Bedroom 2)
    if is_owner_level:
        # Level 2: Home Office / Executive Study
        create_box("Office_Exec_Desk", 1.8, 9.2, 3.4, 10.2, 0, 0.75, mat_furn, col)
        create_box("Office_Exec_Chair", 2.3, 8.6, 2.9, 9.1, 0, 0.60, mat_bed, col)
        create_box("Office_Bookshelf", 0.4, 8.0, 3.8, 8.5, 0, 1.20, mat_cupboard, col)
    else:
        # Level 1: Bedroom 2
        create_box("B2_Bed", 1.5, 8.8, 3.3, 10.8, 0, 0.45, mat_bed, col)
        create_box("B2_Wardrobe", 0.4, 8.0, 3.8, 8.6, 0, 1.10, mat_cupboard, col)
        create_box("B2_Study_Desk", 1.5, 11.0, 2.7, 11.7, 0, 0.75, mat_furn, col)

    title_txt = "Second Floor - Owner's Residence & Office" if is_owner_level else "First Floor - Brother's 2BHK Residence"
    add_title_block(title_txt, col, is_ground=False)

    # Comprehensive Architectural & Vaastu Text Callouts
    add_cad_text("Lbl_MB", "MASTER BEDROOM\n12'-6\" x 13'-4\" [NIRUTHI / SW]", 2.0, 2.8, size=0.22, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_AttBath", "ATT. BATH\n6'0\"x8'6\" [PRIVATE]", 1.1, 5.6, size=0.18, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_ComBath", "COMMON BATH\n6'0\"x8'6\" [EAST DOOR]", 2.9, 5.6, size=0.18, color=(0.1, 0.4, 0.2, 1.0), collection=col)
    
    if is_owner_level:
        add_cad_text("Lbl_Office", "HOME OFFICE / STUDY\n12'-4\" x 13'-11\" [GARDEN VIEW]\n(Direct Door to North Balcony)", 2.1, 10.5, size=0.20, color=(0.1, 0.25, 0.6, 1.0), collection=col)
    else:
        add_cad_text("Lbl_B2", "BEDROOM 2\n12'-4\" x 13'-11\" [VAYU]\n(Direct Door to North Balcony)", 2.1, 10.5, size=0.20, color=COLOR_TEXT, collection=col)
        
    add_cad_text("Lbl_Living", "GRAND LIVING HALL (BRAHMASTHANA)\n18'-0\" x 14'-0\" [OPEN ILLUMINATED CORE]", 6.3, 8.8, size=0.24, color=(0.05, 0.4, 0.3, 1.0), collection=col)
    add_cad_text("Lbl_Dining", "DINING AREA\n10'-6\" x 11'-8\"", 5.8, 2.5, size=0.20, color=COLOR_TEXT, collection=col)
    add_cad_text("Lbl_Kitchen", "MODULAR KITCHEN\n12'-3\" x 11'-8\" [AGNEYA / SE]\n(East-Facing Cooking Hob)", 9.2, 2.2, size=0.20, color=(0.7, 0.25, 0.1, 1.0), collection=col)
    add_cad_text("Lbl_Utility", "UTILITY BALCONY\n(Out-of-House)", PLINTH_W + 0.7, 1.8, size=0.18, rot_z=math.radians(-90), color=COLOR_TEXT, collection=col)
    
    add_cad_text("Lbl_Mallanna", "MALLANNA TEMPLE ROOM\n8'-4\" x 8'-0\" [WEST DOOR]\n(Faces North | Detached from Kitchen)", 9.8, 6.2, size=0.18, color=(0.8, 0.45, 0.1, 1.0), collection=col)
    add_cad_text("Lbl_DailyPooja", "DAILY POOJA MANDIR\n8'-4\" x 8'-0\" [WEST DOOR]\n(Faces East | Sacred Devotion)", 9.8, 8.6, size=0.18, color=(0.8, 0.45, 0.1, 1.0), collection=col)
    
    add_cad_text("Lbl_Ishanya", "OPEN ISHANYA (NE) SITOUT\n13'-0\" x 8'-0\" [OPEN TO SKY]\n(Sacred Morning Sunlight Corridor)", 9.2, 11.0, size=0.20, color=(0.05, 0.45, 0.7, 1.0), collection=col)
    add_cad_text("Lbl_Simhadwaram", "SIMHADWARAM (MAIN ENTRANCE)\nNORTH-NORTH-EAST (NNE) PADA\n(Direct Arrival from Covered Verandah)", 6.5, PLINTH_D + 0.5, size=0.18, color=(0.05, 0.5, 0.2, 1.0), collection=col)
    add_cad_text("Lbl_Verandah", "COVERED NORTH VERANDAH / WALKWAY (CONNECTS NW CORE TO FRONT DOOR)", 3.6, PLINTH_D + 0.8, size=0.18, color=(0.1, 0.3, 0.5, 1.0), collection=col)

    png_name = "second_floor_owner_2d.png" if is_owner_level else "first_floor_brother_2d.png"
    scene.render.filepath = str(OUTPUT_DIR / png_name)
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {png_name}")

if __name__ == "__main__":
    print("Starting Blender Architectural CAD Generation (Full Plot + Plinth)...")
    build_ground_floor_entire_plot()
    build_upper_floor("First_Floor_Brother", is_owner_level=False)
    build_upper_floor("Second_Floor_Owner", is_owner_level=True)
    
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_FILE))
    print(f"Master Project Saved: {BLEND_FILE}")
