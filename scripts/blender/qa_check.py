"""Headless mesh QA for game/web assets.

Usage:
  blender -b file.blend --python scripts/blender/qa_check.py -- [--max-tris N] [--max-materials N] [--strict]
Exits 1 if any FAIL (or any WARN with --strict).
"""
import sys
import argparse
import bpy
import bmesh

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--max-tris", type=int, default=0)
ap.add_argument("--max-materials", type=int, default=0)
ap.add_argument("--strict", action="store_true")
args = ap.parse_args(argv)

fails, warns = [], []
total_tris = 0
materials = set()
depsgraph = bpy.context.evaluated_depsgraph_get()

for obj in bpy.context.scene.objects:
    if obj.type != "MESH":
        continue
    n = obj.name
    me = obj.evaluated_get(depsgraph).to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)

    tris = sum(len(f.verts) - 2 for f in bm.faces)
    total_tris += tris
    ngons = sum(1 for f in bm.faces if len(f.verts) > 4)
    nonmanifold = sum(1 for e in bm.edges if not e.is_manifold and not e.is_boundary)
    loose_v = sum(1 for v in bm.verts if not v.link_edges)
    loose_e = sum(1 for e in bm.edges if not e.link_faces)
    zero_faces = sum(1 for f in bm.faces if f.calc_area() < 1e-10)

    if not me.uv_layers:
        fails.append(f"{n}: no UV map")
    if any(abs(s - 1.0) > 1e-4 for s in obj.scale) or any(abs(r) > 1e-4 for r in obj.rotation_euler):
        warns.append(f"{n}: unapplied rotation/scale {tuple(round(s, 3) for s in obj.scale)}")
    if obj.scale.x * obj.scale.y * obj.scale.z < 0:
        fails.append(f"{n}: negative scale (flipped normals on export)")
    if nonmanifold:
        warns.append(f"{n}: {nonmanifold} non-manifold edges")
    if loose_v or loose_e:
        fails.append(f"{n}: loose geometry ({loose_v} verts, {loose_e} edges)")
    if zero_faces:
        fails.append(f"{n}: {zero_faces} zero-area faces")
    if ngons:
        warns.append(f"{n}: {ngons} n-gons (triangulate before export for predictable shading)")
    if not any(s.material for s in obj.material_slots):
        warns.append(f"{n}: no material assigned")
    if obj.name.startswith(("Cube", "Sphere", "Cylinder", "Plane")) or "." in obj.name:
        warns.append(f"{n}: default/duplicate-style name")
    for slot in obj.material_slots:
        if slot.material:
            materials.add(slot.material.name)
    # skin weights: max 4 influences
    if obj.vertex_groups and any(m.type == "ARMATURE" for m in obj.modifiers):
        over = sum(1 for v in obj.data.vertices if sum(1 for g in v.groups if g.weight > 1e-4) > 4)
        if over:
            fails.append(f"{n}: {over} verts with >4 bone influences")

    bm.free()
    obj.evaluated_get(depsgraph).to_mesh_clear()

if args.max_tris and total_tris > args.max_tris:
    fails.append(f"scene: {total_tris} tris > budget {args.max_tris}")
if args.max_materials and len(materials) > args.max_materials:
    fails.append(f"scene: {len(materials)} materials > budget {args.max_materials}")

print("\n=== QA REPORT ===")
print(f"triangles: {total_tris} | materials: {len(materials)}")
for f in fails:
    print("FAIL", f)
for w in warns:
    print("WARN", w)
ok = not fails and not (args.strict and warns)
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
