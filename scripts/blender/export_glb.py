"""Export the open .blend to GLB with game/web-friendly settings.

Usage:
  blender -b file.blend --python scripts/blender/export_glb.py -- out.glb [--no-anim]
"""
import os
import sys
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if not argv:
    sys.exit("usage: ... -- out.glb [--no-anim]")
out = os.path.abspath(argv[0])
anim = "--no-anim" not in argv
os.makedirs(os.path.dirname(out), exist_ok=True)

# Apply transforms on meshes that aren't skinned (skinned meshes keep their bind pose)
bpy.ops.object.select_all(action="DESELECT")
for obj in bpy.context.scene.objects:
    if obj.type == "MESH" and not any(m.type == "ARMATURE" for m in obj.modifiers):
        obj.select_set(True)
if bpy.context.selected_objects:
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

bpy.ops.export_scene.gltf(
    filepath=out,
    export_format="GLB",
    export_yup=True,
    export_apply=True,          # apply modifiers (except armature)
    export_texcoords=True,
    export_normals=True,
    export_tangents=False,      # engines regenerate MikkTSpace tangents
    export_materials="EXPORT",
    export_image_format="AUTO",
    export_animations=anim,
    export_skins=anim,
    use_visible=True,
)
print("exported", out, os.path.getsize(out), "bytes")
