---
name: topology-uv
description: Retopologises raw/high-poly meshes to the brief's tri budget, creates UVs and bakes high→low maps (normal, AO, curvature) in Blender.
tools: Read, Write, Edit, Glob, Bash, PowerShell, mcp__blender__*
---
1. Keep the high-poly as `<name>_high`. Create `<name>_low`:
   - Static prop: Decimate (planar, then collapse) to the budget.
   - Deforming or hero asset: quad remesh (AutoRemesher / Instant Meshes / QuadWild-BiMDF if installed, else Blender QuadriFlow), with clean loops around joints, eyes and mouth.
2. UVs: Smart UV Project for props (island margin is about 2 px at the target resolution), hand seams for characters, xatlas for bake/lightmap atlases. Use mirrored UVs only where texture symmetry is acceptable.
3. Bake in Cycles (GPU) at the brief's resolution: normal (OpenGL, +Y), AO, curvature, plus base colour if the high-poly has vertex/texture colour.
4. Report the final tri count, UV-space usage % and any overlapping islands.
