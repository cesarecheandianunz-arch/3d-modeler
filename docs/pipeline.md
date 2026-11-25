# Optimized pipeline — why each choice

Principle: **generate fast, then make it production-correct.** AI generators give you form and colour in minutes;
classical deterministic tools (retopo, UV, bake, meshoptimizer) make it game/web ready. Never ship a raw AI mesh.

## 1. Brief (art-director)
Lock before generating anything: target platform, poly budget, texture budget, style, scale (metres), pivot,
rigged or static, LOD count, file format. Budgets drive every later stage.

| Target | Tris (hero / prop) | Textures | Format |
|---|---|---|---|
| Mobile / web | 5–15k / 0.5–3k | 1k–2k, KTX2 | GLB (meshopt + KTX2) |
| PC/console game | 30–80k / 2–15k | 2k–4k | GLB/FBX, engine compresses |
| Render / film | unlimited | 4k+ UDIM | .blend / USD |
| 3D print | watertight, no limit | none | STL/3MF |

## 2. Concept (concept-artist)
Image-to-3D quality is decided here. Produce a **clean turnaround**: neutral pose (A-pose for characters),
orthographic-ish, plain background, even lighting, no heavy shadows, front + side + back (+ 3/4).
Multi-view input (Hunyuan3D-2mv, Pixal3D 4-view sheets) beats single image for back-side accuracy.

## 3. Base mesh (modeler) — pick the route
- **Organic / characters / props with complex form** → image-to-3D: TRELLIS.2 (MIT, high-res), Pixal3D (pixel-aligned, PBR, low-VRAM mode), Hunyuan3D 2.1/3.0 (shape + PBR paint). All run natively in ComfyUI.
- **Hard-surface, architecture, modular kits, precise dimensions** → Blender via MCP with Python (bmesh, modifiers, Geometry Nodes). Deterministic, exact, already clean topology.
- **Hybrid** (best quality): AI mesh as a sculpt/reference, re-model key hard parts in Blender.

## 4. Retopology & UVs (topology-uv)
- Static props: Decimate (planar + collapse) to budget is usually enough.
- Deforming meshes / hero assets: quad remesh (AutoRemesher, Instant Meshes, QuadWild-BiMDF), then fix edge loops at joints.
- UVs: Blender Smart UV for props, seams-by-hand for characters, **xatlas** for automatic lightmap/bake atlases. Target ≥ 1 px padding per mip level.
- Bake high → low: normal, AO, curvature (Blender Cycles bake, GPU).

## 5. Texturing (texture-artist)
- AI paint on the low-poly: Hunyuan3D-Paint / Pixal3D PBR output → re-bake onto your clean UVs.
- Material from image: Ubisoft CHORD (ComfyUI) estimates basecolor/normal/roughness/metal from a texture image.
- Procedural/tileable: Material Maker or Blender shader nodes → bake.
- Always glTF metallic-roughness: BaseColor (sRGB), ORM packed (R=AO, G=Rough, B=Metal, linear), Normal (OpenGL +Y).

## 6. Rig (rigger)
- Humanoid: Rigify or Mixamo for speed; UniRig for arbitrary topology / creatures.
- Check weights with stress poses; keep ≤ 4 influences per vertex for real-time; bone names engine-friendly.

## 7. Optimize, QA, export (optimizer-qa)
`scripts/blender/qa_check.py` → `scripts/blender/export_glb.py` → `scripts/optimize.sh <engine|web>`.

**About OpenGL / D3D:** you do *not* need a custom renderer to be optimal. The GPU-level wins
(vertex-cache order, overdraw, vertex-fetch, quantization, LOD simplification) are exactly what
**meshoptimizer** does, and it is what engines use internally. Use a custom GL/D3D/Vulkan viewer only for
a bespoke runtime; for review, Blender EEVEE, Godot (Godot MCP already installed) or a three.js viewer is enough.

- **Engine profile** (Godot/Unity/Unreal): dedup, weld, prune, resize textures, *no* meshopt/KTX2 compression — engines re-import and compress themselves (Godot doesn't read EXT_meshopt_compression).
- **Web profile** (Three.js/Babylon/R3F): meshopt geometry compression + KTX2 (or WebP) textures; client needs MeshoptDecoder + KTX2Loader.
- LODs: `gltfpack -si 0.5` / gltf-transform `simplify` per LOD level.

## Definition of done
QA script passes · within tri & texture budget · scale correct (1 unit = 1 m), +Y up in glTF · pivot at base/origin ·
transforms applied · named meshes/materials · opens cleanly in the target engine · turntable screenshot in `assets/<name>/`.
