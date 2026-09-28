"""
Blender 3D CAD Multi-Camera Rendering Engine for Property 2.
Directly driven by the parametric geometry in src/design_model.py.
Renders 4 mathematically exact 3D views:
  1. 3D Isometric Cutaway of Second Floor (Owner 2BHK + Office)
  2. 3D Interior Living & Lord Mallanna Temple View
  3. 3D Rooftop Terrace Sky Lounge View
  4. 3D Full-Building G+2 Exterior Perspective (Corner Plot)
"""

import bpy
import math
import sys
from pathlib import Path
from mathutils import Vector

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import design_model as dm

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

M_PER_MM = 0.001
PLOT_W = dm.PLOT_W_MM * M_PER_MM
PLOT_D = dm.PLOT_D_MM * M_PER_MM
PLINTH_W = dm.PLINTH_W_MM * M_PER_MM
PLINTH_D = dm.PLINTH_D_MM * M_PER_MM

SETBACK_W = dm.SETBACK_W_MM * M_PER_MM
SETBACK_S = dm.SETBACK_S_MM * M_PER_MM
SETBACK_E = dm.SETBACK_E_MM * M_PER_MM
SETBACK_N = dm.SETBACK_N_MM * M_PER_MM

PLOT_X0 = -SETBACK_W
PLOT_X1 = PLINTH_W + SETBACK_E
PLOT_Y0 = -SETBACK_S
PLOT_Y1 = PLINTH_D + SETBACK_N

EXT_WALL_THICK = 0.23
INT_WALL_THICK = 0.115
COMPOUND_WALL_THICK = 0.23

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderSettings") and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    
    # World background
    world = bpy.data.worlds.new("CAD_World")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.92, 0.94, 0.96, 1.0)
        bg.inputs["Strength"].default_value = 1.0
    return scene

def get_mat(name, color, roughness=0.4, metallic=0.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = roughness
            bsdf.inputs["Metallic"].default_value = metallic
    return mat

def create_box(name, x0, y0, x1, y1, z0, z1, mat, col):
    w = abs(x1 - x0)
    d = abs(y1 - y0)
    h = abs(z1 - z0)
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    cz = (z0 + z1) / 2.0
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (w, d, h)
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        obj.data.materials.append(mat)
    col.objects.link(obj)
    bpy.context.scene.collection.objects.unlink(obj)
    return obj

def aim_camera(cam, target_pos):
    loc = cam.location
    direction = Vector(target_pos) - loc
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()

def add_sun_and_lights(col, sun_energy=3.0):
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 25))
    sun = bpy.context.active_object
    sun.name = "Sun_3D"
    sun.data.energy = sun_energy
    sun.data.color = (1.0, 0.98, 0.92)
    sun.rotation_euler = (math.radians(45), math.radians(20), math.radians(-35))
    col.objects.link(sun)
    bpy.context.scene.collection.objects.unlink(sun)
    
    bpy.ops.object.light_add(type='POINT', location=(-5, 15, 18))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 800.0
    fill.data.color = (0.85, 0.92, 1.0)
    col.objects.link(fill)
    bpy.context.scene.collection.objects.unlink(fill)

# =============================================================================
# SCENE BUILDER: SECOND FLOOR CUTAWAY (OWNER 2BHK + OFFICE)
# =============================================================================
def build_second_floor_cutaway(col, wall_h=1.35):
    mat_marble = get_mat("Mat_Marble_Living", (0.95, 0.94, 0.91, 1.0), roughness=0.15)
    mat_wood_floor = get_mat("Mat_Wood_Bed", (0.58, 0.40, 0.25, 1.0), roughness=0.35)
    mat_ext_wall = get_mat("Mat_Ext_Wall", (0.88, 0.86, 0.82, 1.0), roughness=0.7)
    mat_int_wall = get_mat("Mat_Int_Wall", (0.94, 0.93, 0.90, 1.0), roughness=0.7)
    mat_teak = get_mat("Mat_Teak_Pooja", (0.45, 0.22, 0.08, 1.0), roughness=0.25)
    mat_brass = get_mat("Mat_Brass_Gold", (0.95, 0.75, 0.25, 1.0), roughness=0.2, metallic=0.9)
    mat_kitchen = get_mat("Mat_Granite_Black", (0.12, 0.12, 0.14, 1.0), roughness=0.2)
    mat_sofa = get_mat("Mat_Sofa_Fabric", (0.35, 0.42, 0.50, 1.0), roughness=0.8)
    mat_col = get_mat("Mat_RCC_Col", (0.18, 0.22, 0.28, 1.0), roughness=0.5)

    # Base Plinth Slab
    create_box("Floor_Slab", 0, 0, PLINTH_W, PLINTH_D, -0.15, 0, mat_marble, col)
    # North & East Balconies
    create_box("Balcony_North", -2.40, PLINTH_D, PLINTH_W + 2.40, PLINTH_D + 1.30, -0.15, 0, mat_marble, col)
    create_box("Balcony_East_Util", PLINTH_W, 0, PLINTH_W + 1.25, 5.33, -0.15, 0, mat_marble, col)
    create_box("Balcony_East_Morn", PLINTH_W, 9.55, PLINTH_W + 1.25, PLINTH_D, -0.15, 0, mat_marble, col)
    create_box("Balcony_South", 3.810, -1.07, 6.858, 0, -0.15, 0, mat_marble, col)

    # Master Bed & Office wood flooring
    create_box("Floor_MasterBed", EXT_WALL_THICK, EXT_WALL_THICK, 3.810 - INT_WALL_THICK/2, 4.115 - INT_WALL_THICK/2, 0, 0.01, mat_wood_floor, col)
    create_box("Floor_Office", 3.810 + INT_WALL_THICK/2, 8.128 + INT_WALL_THICK/2, 6.858 - INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, 0.01, mat_wood_floor, col)

    # South Exterior Wall
    create_box("Ext_S1", 0, 0, 1.10, EXT_WALL_THICK, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_S2", 2.90, 0, 3.810, EXT_WALL_THICK, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_S3", 3.810, 0, 4.10, EXT_WALL_THICK, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_S4", 5.40, 0, 6.858, EXT_WALL_THICK, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_S5", 6.858, 0, PLINTH_W, EXT_WALL_THICK, 0, wall_h, mat_ext_wall, col)

    # East Exterior Wall
    create_box("Ext_E1", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, 1.60, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_E2", PLINTH_W - EXT_WALL_THICK, 3.10, PLINTH_W, 4.30, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_E3", PLINTH_W - EXT_WALL_THICK, 5.15, PLINTH_W, 6.15, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_E4", PLINTH_W - EXT_WALL_THICK, 7.35, PLINTH_W, 10.40, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_E5", PLINTH_W - EXT_WALL_THICK, 11.70, PLINTH_W, PLINTH_D, 0, wall_h, mat_ext_wall, col)

    # West Exterior Wall
    create_box("Ext_W1", 0, 0.23, EXT_WALL_THICK, 4.115, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_W2", 0, 4.115, EXT_WALL_THICK, 5.10, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_W3", 0, 5.90, EXT_WALL_THICK, 7.10, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_W4", 0, 7.90, EXT_WALL_THICK, PLINTH_D - EXT_WALL_THICK, 0, wall_h, mat_ext_wall, col)

    # North Exterior Wall
    create_box("Ext_N1", 0, PLINTH_D - EXT_WALL_THICK, 1.00, PLINTH_D, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_N2", 2.60, PLINTH_D - EXT_WALL_THICK, 4.50, PLINTH_D, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_N3", 6.10, PLINTH_D - EXT_WALL_THICK, 7.30, PLINTH_D, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_N4", 8.50, PLINTH_D - EXT_WALL_THICK, 9.20, PLINTH_D, 0, wall_h, mat_ext_wall, col)
    create_box("Ext_N5", 10.50, PLINTH_D - EXT_WALL_THICK, PLINTH_W, PLINTH_D, 0, wall_h, mat_ext_wall, col)

    # Interior Partitions
    create_box("MB_Wall_E", 3.810 - INT_WALL_THICK/2, EXT_WALL_THICK, 3.810 + INT_WALL_THICK/2, 4.115, 0, wall_h, mat_int_wall, col)
    create_box("MB_Wall_N", EXT_WALL_THICK, 4.115 - INT_WALL_THICK/2, 2.80, 4.115 + INT_WALL_THICK/2, 0, wall_h, mat_int_wall, col)
    create_box("Bath_Divider", EXT_WALL_THICK, 6.10 - INT_WALL_THICK/2, 1.98, 6.10 + INT_WALL_THICK/2, 0, wall_h, mat_int_wall, col)
    create_box("ComBath_Wall_N", EXT_WALL_THICK, 8.128 - INT_WALL_THICK/2, 1.98, 8.128 + INT_WALL_THICK/2, 0, wall_h, mat_int_wall, col)
    create_box("ComBath_Wall_E", 1.98 - INT_WALL_THICK/2, 4.115, 1.98 + INT_WALL_THICK/2, 7.05, 0, wall_h, mat_int_wall, col)
    create_box("Wall_Bed2_Office", 3.810 - INT_WALL_THICK/2, 8.128, 3.810 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, wall_h, mat_int_wall, col)
    create_box("Office_Wall_S", 4.85, 8.128 - INT_WALL_THICK/2, 6.858, 8.128 + INT_WALL_THICK/2, 0, wall_h, mat_int_wall, col)
    create_box("Wall_Office_NE", 6.858 - INT_WALL_THICK/2, 8.128, 6.858 + INT_WALL_THICK/2, PLINTH_D - EXT_WALL_THICK, 0, wall_h, mat_int_wall, col)

    # East Shrines: Lord Mallanna Temple & Daily Pooja
    create_box("Passage_Wall_N", 8.609, 5.334 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 5.334 + INT_WALL_THICK/2, 0, wall_h, mat_int_wall, col)
    create_box("Pooja_Shared_Wall", 8.609, 6.611 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 6.611 + INT_WALL_THICK/2, 0, wall_h, mat_int_wall, col)
    create_box("Mallanna_Wall_N", 8.609, 9.545 - INT_WALL_THICK/2, PLINTH_W - EXT_WALL_THICK, 9.545 + INT_WALL_THICK/2, 0, wall_h, mat_int_wall, col)
    create_box("Pooja_Wall_W", 8.609 - INT_WALL_THICK/2, 6.334, 8.609 + INT_WALL_THICK/2, 8.100, 0, wall_h, mat_int_wall, col)

    # Lord Mallanna Temple Altar & Shrine (Carved Teak Mandapam)
    create_box("Mallanna_Mandapam_Base", 8.90, 6.90, PLINTH_W - 0.40, 9.25, 0, 0.45, mat_teak, col)
    create_box("Mallanna_Backdrop", PLINTH_W - 0.45, 7.00, PLINTH_W - 0.25, 9.15, 0.45, 1.30, mat_teak, col)
    create_box("Mallanna_Deity_Idol", 9.80, 7.85, 10.30, 8.35, 0.45, 0.95, mat_brass, col)

    # Daily Pooja Mandir Altar
    create_box("Daily_Pooja_Base", 8.90, 5.50, PLINTH_W - 0.40, 6.45, 0, 0.40, mat_teak, col)
    create_box("Daily_Pooja_Idol", 9.80, 5.85, 10.20, 6.15, 0.40, 0.80, mat_brass, col)

    # 100% OPEN Living & Dining Hall Furniture
    create_box("Sofa_Main", 2.20, 5.50, 4.80, 6.40, 0, 0.45, mat_sofa, col)
    create_box("Sofa_L_Return", 2.20, 6.40, 3.10, 7.80, 0, 0.45, mat_sofa, col)
    create_box("Coffee_Table", 3.40, 6.70, 4.40, 7.50, 0, 0.35, mat_teak, col)

    create_box("Dining_Table", 4.30, 1.80, 6.10, 3.00, 0, 0.75, mat_teak, col)
    for i in range(3):
        create_box(f"Chair_S_{i}", 4.50 + i*0.60, 1.35, 4.90 + i*0.60, 1.70, 0, 0.48, mat_sofa, col)
        create_box(f"Chair_N_{i}", 4.50 + i*0.60, 3.10, 4.90 + i*0.60, 3.45, 0, 0.48, mat_sofa, col)

    # Open Modular Kitchen L-Counter in Southeast
    create_box("Kitchen_Counter_S", 6.858, EXT_WALL_THICK, PLINTH_W - EXT_WALL_THICK, EXT_WALL_THICK + 0.65, 0, 0.86, mat_kitchen, col)
    create_box("Kitchen_Counter_E", PLINTH_W - EXT_WALL_THICK - 0.65, EXT_WALL_THICK + 0.65, PLINTH_W - EXT_WALL_THICK, 4.00, 0, 0.86, mat_kitchen, col)

    # Master Bedroom: King Bed & Side Tables
    create_box("MB_King_Bed", 1.10, 0.75, 2.90, 2.75, 0, 0.55, mat_wood_floor, col)
    create_box("MB_Mattress", 1.15, 0.80, 2.85, 2.70, 0.50, 0.75, mat_sofa, col)
    create_box("MB_Headboard", 1.05, 0.65, 2.95, 0.75, 0, 1.10, mat_teak, col)
    create_box("MB_Wardrobe", EXT_WALL_THICK, 1.20, EXT_WALL_THICK + 0.60, 3.80, 0, 1.35, mat_teak, col)

    # Personal Office: Executive Desk & Bookshelf
    create_box("Office_Desk", 4.30, 9.60, 5.80, 10.40, 0, 0.75, mat_teak, col)
    create_box("Office_Bookshelf", 6.858 - INT_WALL_THICK/2 - 0.40, 8.50, 6.858 - INT_WALL_THICK/2, 11.20, 0, 1.35, mat_teak, col)

    # Bedroom 2: Queen Bed
    create_box("Bed2_Frame", 1.00, 9.20, 2.60, 11.00, 0, 0.55, mat_wood_floor, col)
    create_box("Bed2_Headboard", 0.95, 9.10, 2.65, 9.20, 0, 1.05, mat_teak, col)

    # NW External Core: Lift & Stairs
    create_box("Lift_Shaft", -2.25, 10.30, -0.45, 12.10, 0, wall_h, mat_ext_wall, col)
    create_box("Stair_Landing", -2.25, 6.80, -0.25, 9.60, 0, 0.30, mat_marble, col)

    # 21 RCC Columns
    for c in dm.COLUMNS:
        cx = c["x"] * M_PER_MM
        cy = c["y"] * M_PER_MM
        cw = c["width"] * M_PER_MM
        cd = c["depth"] * M_PER_MM
        create_box(f"Col_{c['id']}", cx - cw/2, cy - cd/2, cx + cw/2, cy + cd/2, 0, wall_h + 0.05, mat_col, col)

# =============================================================================
# SCENE BUILDER: ROOFTOP TERRACE
# =============================================================================
def build_terrace_scene(col):
    mat_cool_tiles = get_mat("Mat_Cool_Tiles", (0.95, 0.96, 0.98, 1.0), roughness=0.3)
    mat_timber = get_mat("Mat_Timber_Pergola", (0.50, 0.28, 0.12, 1.0), roughness=0.4)
    mat_granite = get_mat("Mat_Granite_Bar", (0.10, 0.10, 0.12, 1.0), roughness=0.15)
    mat_metal_frame = get_mat("Mat_Metal_Frame", (0.20, 0.25, 0.30, 1.0), roughness=0.3, metallic=0.8)
    mat_solar_blue = get_mat("Mat_Solar_Cell", (0.08, 0.18, 0.45, 1.0), roughness=0.1, metallic=0.5)
    mat_parapet = get_mat("Mat_Parapet", (0.88, 0.87, 0.85, 1.0), roughness=0.6)
    mat_sofa = get_mat("Mat_Outdoor_Sofa", (0.82, 0.80, 0.75, 1.0), roughness=0.7)
    mat_water_tank = get_mat("Mat_OHT_Cyan", (0.15, 0.55, 0.85, 1.0), roughness=0.3)

    # Base Terrace Slab
    create_box("Terrace_Floor", 0, 0, PLINTH_W, PLINTH_D, 0, 0.15, mat_cool_tiles, col)
    create_box("Terrace_N_Deck", -2.35, PLINTH_D, PLINTH_W, PLINTH_D + 1.30, 0, 0.15, mat_cool_tiles, col)
    create_box("Terrace_E_Deck", PLINTH_W, 0, PLINTH_W + 1.25, PLINTH_D, 0, 0.15, mat_cool_tiles, col)
    create_box("Terrace_S_Deck", 3.810, -1.07, 6.858, 0, 0, 0.15, mat_cool_tiles, col)

    # Parapet Walls
    create_box("Parapet_S", 0, 0, PLINTH_W, EXT_WALL_THICK, 0.15, 1.05, mat_parapet, col)
    create_box("Parapet_N", 0, PLINTH_D - EXT_WALL_THICK, PLINTH_W, PLINTH_D, 0.15, 1.05, mat_parapet, col)
    create_box("Parapet_E", PLINTH_W - EXT_WALL_THICK, 0, PLINTH_W, PLINTH_D, 0.15, 1.05, mat_parapet, col)
    create_box("Parapet_W_S", 0, 0, EXT_WALL_THICK, 4.10, 0.15, 1.05, mat_parapet, col)
    create_box("Parapet_W_N", 0, 11.55, EXT_WALL_THICK, PLINTH_D, 0.15, 1.05, mat_parapet, col)

    # SW Niruthi Covered Pergola Sit-Out (18' x 12'-6" / 5.5m x 3.8m)
    create_box("Post_SW", 0.35, 0.35, 0.60, 0.60, 0.15, 2.70, mat_timber, col)
    create_box("Post_SE", 5.25, 0.35, 5.50, 0.60, 0.15, 2.70, mat_timber, col)
    create_box("Post_NW", 0.35, 3.55, 0.60, 3.80, 0.15, 2.70, mat_timber, col)
    create_box("Post_NE", 5.25, 3.55, 5.50, 3.80, 0.15, 2.70, mat_timber, col)
    for i in range(9):
        rx = 0.35 + i * 0.62
        create_box(f"Rafter_{i}", rx, 0.30, rx + 0.10, 3.85, 2.70, 2.85, mat_timber, col)

    create_box("Sofa_3Seater", 1.40, 0.65, 4.20, 1.40, 0.15, 0.55, mat_sofa, col)
    create_box("Coffee_Table", 2.00, 1.70, 3.60, 2.45, 0.15, 0.40, mat_timber, col)
    create_box("Armchair_W1", 0.65, 1.55, 1.30, 2.20, 0.15, 0.55, mat_sofa, col)
    create_box("Armchair_W2", 0.65, 2.45, 1.30, 3.10, 0.15, 0.55, mat_sofa, col)
    create_box("Armchair_E1", 4.30, 1.55, 4.95, 2.20, 0.15, 0.55, mat_sofa, col)
    create_box("Armchair_E2", 4.30, 2.45, 4.95, 3.10, 0.15, 0.55, mat_sofa, col)

    # West Linear Party Buffet & Bar Counter (13' x 2'-6")
    create_box("Party_Bar_Counter", 0.23, 4.10, 0.99, 8.10, 0.15, 1.00, mat_granite, col)
    create_box("Party_Prep_Sink", 0.32, 7.35, 0.90, 7.95, 0.95, 1.01, get_mat("Mat_Sink_SS", (0.8, 0.82, 0.85, 1.0), roughness=0.1, metallic=0.9), col)
    for i in range(5):
        sy = 4.50 + i * 0.70
        create_box(f"Bar_Stool_{i}", 1.25, sy - 0.20, 1.60, sy + 0.20, 0.15, 0.75, mat_metal_frame, col)

    # SE Dual Solar PV Space-Frame (7.0 kW Total) - Elevated 8'-0" (2.44m)
    create_box("Solar_Post_1", 5.85, 0.35, 6.05, 0.55, 0.15, 2.50, mat_metal_frame, col)
    create_box("Solar_Post_2", 8.16, 0.35, 8.36, 0.55, 0.15, 2.50, mat_metal_frame, col)
    create_box("Solar_Post_3", 10.45, 0.35, 10.65, 0.55, 0.15, 2.50, mat_metal_frame, col)
    create_box("Solar_Post_4", 5.85, 3.85, 6.05, 4.05, 0.15, 3.20, mat_metal_frame, col)
    create_box("Solar_Post_5", 8.16, 3.85, 8.36, 4.05, 0.15, 3.20, mat_metal_frame, col)
    create_box("Solar_Post_6", 10.45, 3.85, 10.65, 4.05, 0.15, 3.20, mat_metal_frame, col)
    create_box("Solar_Panels_Array", 5.75, 0.25, 10.75, 4.15, 2.70, 2.85, mat_solar_blue, col)

    # NW Mumty Room & 5,000L Overhead Water Tank Atop (+13.5m)
    create_box("Mumty_Walls", -2.25, 6.80, -0.25, 11.05, 0.15, 2.85, mat_parapet, col)
    create_box("Lift_Overrun", -2.25, 11.05, -0.45, 12.10, 0.15, 4.20, mat_parapet, col)
    create_box("OHT_Atop_Mumty", -2.20, 6.85, -0.30, 10.60, 2.85, 3.90, mat_water_tank, col)

# =============================================================================
# SCENE BUILDER: FULL G+2 EXTERIOR
# =============================================================================
def build_exterior_scene(col):
    mat_road = get_mat("Mat_Road_Asphalt", (0.22, 0.24, 0.26, 1.0), roughness=0.85)
    mat_compound = get_mat("Mat_Compound_Wall", (0.85, 0.84, 0.80, 1.0), roughness=0.7)
    mat_plinth_floor = get_mat("Mat_Plinth_Floor", (0.80, 0.80, 0.78, 1.0), roughness=0.5)
    mat_facade_white = get_mat("Mat_Facade_White", (0.92, 0.91, 0.88, 1.0), roughness=0.6)
    mat_wood_cladding = get_mat("Mat_Wood_Louvers", (0.50, 0.32, 0.16, 1.0), roughness=0.4)
    mat_glass_balcony = get_mat("Mat_Balcony_Glass", (0.75, 0.90, 0.98, 0.3), roughness=0.05)
    mat_car = get_mat("Mat_SUV_Silver", (0.65, 0.68, 0.72, 1.0), roughness=0.15, metallic=0.9)
    mat_gate = get_mat("Mat_Iron_Gate", (0.15, 0.16, 0.18, 1.0), roughness=0.3, metallic=0.8)

    # 1. Surrounding Municipal Roads
    create_box("Road_West", PLOT_X0 - 9.144, PLOT_Y0 - 9.144, PLOT_X0, PLOT_Y1 + 3.0, -0.30, -0.15, mat_road, col)
    create_box("Road_South", PLOT_X0 - 9.144, PLOT_Y0 - 9.144, PLOT_X1 + 3.0, PLOT_Y0, -0.30, -0.15, mat_road, col)

    # 2. Boundary Compound Wall with Splay & Gates
    create_box("Comp_South", PLOT_X0 + 1.5, PLOT_Y0, PLOT_X1, PLOT_Y0 + COMPOUND_WALL_THICK, -0.15, 1.50, mat_compound, col)
    create_box("Comp_West", PLOT_X0, PLOT_Y0 + 1.5, PLOT_X0 + COMPOUND_WALL_THICK, PLOT_Y1, -0.15, 1.50, mat_compound, col)
    create_box("Comp_East", PLOT_X1 - COMPOUND_WALL_THICK, PLOT_Y0, PLOT_X1, PLOT_Y1, -0.15, 1.80, mat_compound, col)
    create_box("Comp_North", PLOT_X0, PLOT_Y1 - COMPOUND_WALL_THICK, PLOT_X1, PLOT_Y1, -0.15, 1.80, mat_compound, col)
    create_box("North_Gate", PLOT_X0 + 3.0, PLOT_Y1 - COMPOUND_WALL_THICK, PLOT_X0 + 6.65, PLOT_Y1, -0.15, 1.60, mat_gate, col)

    # 3. Ground Stilt Parking Level (Z: 0 to 3.0m)
    create_box("Plinth_G0", 0, 0, PLINTH_W, PLINTH_D, 0, 0.20, mat_plinth_floor, col)
    for c in dm.COLUMNS:
        cx = c["x"] * M_PER_MM
        cy = c["y"] * M_PER_MM
        cw = c["width"] * M_PER_MM
        cd = c["depth"] * M_PER_MM
        create_box(f"Col_G0_{c['id']}", cx - cw/2, cy - cd/2, cx + cw/2, cy + cd/2, 0.20, 3.00, mat_facade_white, col)
    create_box("SUV_Body", 1.00, PLINTH_D - 4.80, 2.90, PLINTH_D - 0.60, 0.20, 1.65, mat_car, col)

    # 4. First Floor (Brother 3BHK) (Z: 3.0 to 6.0m)
    create_box("Slab_L1", 0, 0, PLINTH_W, PLINTH_D, 3.00, 3.15, mat_plinth_floor, col)
    create_box("Balcony_L1_N", -2.40, PLINTH_D, PLINTH_W, PLINTH_D + 1.30, 3.00, 3.15, mat_plinth_floor, col)
    create_box("Balcony_L1_S", 3.810, -1.07, 6.858, 0, 3.00, 3.15, mat_plinth_floor, col)
    create_box("Facade_L1_S", 0, 0, PLINTH_W, EXT_WALL_THICK, 3.15, 6.00, mat_facade_white, col)
    create_box("Facade_L1_W", 0, 0, EXT_WALL_THICK, PLINTH_D, 3.15, 6.00, mat_facade_white, col)
    create_box("Wood_L1_Louvers", 0.05, 0.50, 0.25, 3.50, 3.15, 5.80, mat_wood_cladding, col)
    create_box("Glass_Rail_L1_S", 3.810, -1.07, 6.858, -1.00, 3.15, 4.15, mat_glass_balcony, col)

    # 5. Second Floor (Owner 2BHK + Office) (Z: 6.0 to 9.0m)
    create_box("Slab_L2", 0, 0, PLINTH_W, PLINTH_D, 6.00, 6.15, mat_plinth_floor, col)
    create_box("Balcony_L2_N", -2.40, PLINTH_D, PLINTH_W, PLINTH_D + 1.30, 6.00, 6.15, mat_plinth_floor, col)
    create_box("Balcony_L2_S", 3.810, -1.07, 6.858, 0, 6.00, 6.15, mat_plinth_floor, col)
    create_box("Facade_L2_S", 0, 0, PLINTH_W, EXT_WALL_THICK, 6.15, 9.00, mat_facade_white, col)
    create_box("Facade_L2_W", 0, 0, EXT_WALL_THICK, PLINTH_D, 6.15, 9.00, mat_facade_white, col)
    create_box("Wood_L2_Louvers", 0.05, 0.50, 0.25, 3.50, 6.15, 8.80, mat_wood_cladding, col)
    create_box("Glass_Rail_L2_S", 3.810, -1.07, 6.858, -1.00, 6.15, 7.15, mat_glass_balcony, col)

    # 6. Rooftop Terrace Level (Z: 9.0 to 13.5m)
    create_box("Slab_L3", 0, 0, PLINTH_W, PLINTH_D, 9.00, 9.15, mat_plinth_floor, col)
    create_box("Parapet_Roof_S", 0, 0, PLINTH_W, EXT_WALL_THICK, 9.15, 10.20, mat_facade_white, col)
    create_box("Parapet_Roof_W", 0, 0, EXT_WALL_THICK, 6.80, 9.15, 10.20, mat_facade_white, col)
    create_box("Pergola_Roof_3D", 0.35, 0.35, 5.50, 3.80, 11.70, 11.90, mat_wood_cladding, col)
    create_box("Solar_Canopy_3D", 5.80, 0.25, 10.75, 4.15, 11.60, 11.80, get_mat("Mat_Solar_Top", (0.1, 0.2, 0.5, 1.0), roughness=0.1), col)
    create_box("Mumty_Ext_3D", -2.25, 6.80, -0.25, 11.05, 9.15, 11.85, mat_facade_white, col)
    create_box("OHT_Ext_3D", -2.20, 6.85, -0.30, 10.60, 11.85, 12.85, get_mat("Mat_Tank_Blue", (0.15, 0.55, 0.85, 1.0)), col)
    create_box("Lift_Tower_3D", -2.25, 11.05, -0.45, 12.10, 9.15, 13.20, mat_facade_white, col)

# =============================================================================
# MAIN RENDERER
# =============================================================================
def main():
    print("=" * 75)
    print("STARTING BLENDER 3D CAD ARCHITECTURAL RENDERING ENGINE")
    print("=" * 75)

    # 1. RENDER: 3D ISOMETRIC CUTAWAY OF SECOND FLOOR (OWNER 2BHK + OFFICE)
    print("Building Scene 1: Second Floor 3D Isometric Cutaway...")
    scene = clean_scene()
    col = bpy.data.collections.new("01_3D_Cutaway")
    scene.collection.children.link(col)
    build_second_floor_cutaway(col, wall_h=1.35)
    add_sun_and_lights(col, sun_energy=2.8)

    cam_data = bpy.data.cameras.new("Cam_Cutaway")
    cam_data.lens = 45
    cam = bpy.data.objects.new("Cam_Cutaway", cam_data)
    cam.location = (17.5, -9.5, 14.5)
    aim_camera(cam, (5.5, 6.1, 0.7))
    col.objects.link(cam)
    scene.camera = cam

    p_cutaway = str(OUTPUT_DIR / "blender_3d_cutaway_owner.png")
    scene.render.filepath = p_cutaway
    bpy.ops.render.render(write_still=True)
    print(f"✅ Rendered: {Path(p_cutaway).name}")

    # 2. RENDER: 3D INTERIOR LIVING & LORD MALLANNA TEMPLE VIEW
    print("Building Scene 2: 3D Interior Living & Temple View...")
    scene = clean_scene()
    col = bpy.data.collections.new("02_3D_Interior")
    scene.collection.children.link(col)
    build_second_floor_cutaway(col, wall_h=2.85)
    mat_ceiling = get_mat("Mat_Ceiling", (0.96, 0.95, 0.93, 1.0))
    create_box("Ceiling_Living", 0, 0, PLINTH_W, PLINTH_D, 2.85, 3.00, mat_ceiling, col)

    bpy.ops.object.light_add(type='POINT', location=(9.5, 7.8, 2.4))
    shrine_light = bpy.context.active_object
    shrine_light.name = "Shrine_Warm_Light"
    shrine_light.data.energy = 450.0
    shrine_light.data.color = (1.0, 0.85, 0.55)
    col.objects.link(shrine_light)
    bpy.context.scene.collection.objects.unlink(shrine_light)

    bpy.ops.object.light_add(type='POINT', location=(4.5, 5.5, 2.5))
    living_light = bpy.context.active_object
    living_light.name = "Living_Center_Light"
    living_light.data.energy = 600.0
    living_light.data.color = (1.0, 0.94, 0.85)
    col.objects.link(living_light)
    bpy.context.scene.collection.objects.unlink(living_light)

    cam_int_data = bpy.data.cameras.new("Cam_Interior")
    cam_int_data.lens = 22
    cam_int = bpy.data.objects.new("Cam_Interior", cam_int_data)
    cam_int.location = (2.2, 4.8, 1.25)
    aim_camera(cam_int, (9.2, 7.4, 1.15))
    col.objects.link(cam_int)
    scene.camera = cam_int

    p_interior = str(OUTPUT_DIR / "blender_3d_interior_living.png")
    scene.render.filepath = p_interior
    bpy.ops.render.render(write_still=True)
    print(f"✅ Rendered: {Path(p_interior).name}")

    # 3. RENDER: 3D ROOFTOP TERRACE SKY LOUNGE VIEW
    print("Building Scene 3: 3D Rooftop Terrace Sky Lounge...")
    scene = clean_scene()
    col = bpy.data.collections.new("03_3D_Terrace")
    scene.collection.children.link(col)
    build_terrace_scene(col)
    add_sun_and_lights(col, sun_energy=2.5)

    cam_ter_data = bpy.data.cameras.new("Cam_Terrace")
    cam_ter_data.lens = 24
    cam_ter = bpy.data.objects.new("Cam_Terrace", cam_ter_data)
    cam_ter.location = (0.5, -3.8, 4.8)
    aim_camera(cam_ter, (5.5, 5.8, 1.1))
    col.objects.link(cam_ter)
    scene.camera = cam_ter

    p_terrace = str(OUTPUT_DIR / "blender_3d_terrace_view.png")
    scene.render.filepath = p_terrace
    bpy.ops.render.render(write_still=True)
    print(f"✅ Rendered: {Path(p_terrace).name}")

    # 4. RENDER: FULL MULTI-STORY G+2 EXTERIOR CORNER PERSPECTIVE
    print("Building Scene 4: Full G+2 Exterior Corner Perspective...")
    scene = clean_scene()
    col = bpy.data.collections.new("04_3D_Exterior")
    scene.collection.children.link(col)
    build_exterior_scene(col)
    add_sun_and_lights(col, sun_energy=3.5)

    cam_ext_data = bpy.data.cameras.new("Cam_Exterior")
    cam_ext_data.lens = 32
    cam_ext = bpy.data.objects.new("Cam_Exterior", cam_ext_data)
    cam_ext.location = (-13.5, -14.5, 9.5)
    aim_camera(cam_ext, (5.5, 6.0, 5.8))
    col.objects.link(cam_ext)
    scene.camera = cam_ext

    p_exterior = str(OUTPUT_DIR / "blender_3d_exterior_corner.png")
    scene.render.filepath = p_exterior
    bpy.ops.render.render(write_still=True)
    print(f"✅ Rendered: {Path(p_exterior).name}")

    print("=" * 75)
    print("ALL 4 3D CAD RENDERS EXECUTED DIRECTLY FROM PARAMETRIC DESIGN MODEL")
    print("=" * 75)

if __name__ == "__main__":
    main()
