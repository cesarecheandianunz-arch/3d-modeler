# 3D Modeler — AI-assisted 3D agency

A Claude Code workspace that takes an idea from **brief → concept → mesh → retopo/UV → PBR textures → rig → optimized export**
for any project (games in Godot/Unity/Unreal, web/Three.js, AR, renders, 3D print).

Open this folder in Claude Code and say e.g. *"/new-asset a stylized wooden treasure chest for a Godot mobile game"*.
The `new-asset` skill drives the specialist agents in `.claude/agents/` stage by stage.

## Pipeline at a glance

| Stage | Agent | Primary tools (local / open first) |
|---|---|---|
| 1. Brief & art direction | `art-director` | `briefs/_template.md`, reference boards |
| 2. Concept art & turnarounds | `concept-artist` | ComfyUI (FLUX/SDXL) → front/side/back sheet |
| 3. Base mesh | `modeler` | **TRELLIS.2 / Pixal3D / Hunyuan3D** (image→3D) or Blender via MCP for hard-surface/procedural |
| 4. Retopology & UVs | `topology-uv` | AutoRemesher / Instant Meshes / QuadWild, Blender Decimate, **xatlas** |
| 5. Texturing (PBR) | `texture-artist` | Hunyuan3D-Paint, Ubisoft **CHORD** (ComfyUI), Blender bake, Material Maker |
| 6. Rigging & anim | `rigger` | **UniRig**, Blender Rigify, Mixamo (humanoids) |
| 7. Optimize, QA & export | `optimizer-qa` | Blender QA script, **gltf-transform**, **meshoptimizer/gltfpack**, KTX2 |

Full rationale: [`docs/pipeline.md`](docs/pipeline.md). Tool catalog with links: [`docs/tools.md`](docs/tools.md).

## Setup

1. **Blender 5.1+** (needed for the official Blender Lab MCP; the community server works on 4.x).
2. MCP: `.mcp.json` registers the community Blender MCP (`uvx mcp-for-blender`). Install its add-on in Blender, click *Connect*.
3. **ComfyUI** (local GPU, ≥12 GB VRAM recommended) – TRELLIS.2, Pixal3D and Hunyuan3D run natively.
4. Node.js → `npm i -g @gltf-transform/cli gltfpack` ; optional KTX-Software (`toktx`) for KTX2.
5. Optional: UniRig (Python 3.11 + PyTorch ≥ 2.3.1), AutoRemesher binary.

## Layout

```
briefs/            one markdown brief per asset (copy _template.md)
assets/<name>/     concept/, source/ (.blend), export/ (.glb) – large files git-ignored
scripts/blender/   headless Blender scripts (QA, export)
scripts/optimize.sh  engine/web glTF optimization profiles
.claude/agents/    the agency's specialists
.claude/skills/    new-asset orchestration skill
```
