---
name: new-asset
description: Run the full 3D agency pipeline for a new asset or concept, from brief to concept, mesh, retopo/UV, textures, rig and optimized export, by delegating to the specialist agents. Use when the user asks to make/model/create a 3D asset, character, prop or scene.
---
# New asset pipeline

Argument: a free-text description of what to make (and optionally the target project/engine).

Run the stages in order. Each stage's output is the next stage's input, so don't parallelise across stages. Separate assets from one concept *can* run in parallel.

1. **art-director**: create `briefs/<name>.md`. Show the user the budgets and assumptions, and get a quick OK if anything is ambiguous (engine, style, rigged?).
2. **concept-artist**: write turnaround prompts and images to `assets/<name>/concept/`. Show them to the user; this is the cheapest point to change direction.
3. **modeler**: produce the base mesh in `assets/<name>/source/<name>.blend`.
4. **topology-uv**: make the low-poly mesh to budget, UVs and baked maps.
5. **texture-artist**: make the PBR set.
6. **rigger**: only if the brief says rigged.
7. **optimizer-qa**: run QA, export, optimize, and write REPORT.md.
8. **art-director**: review against the brief and loop back to the owning stage on FAIL (at most 2 loops, then report to the user).

Tool availability: check the Blender MCP connection (`get_scene_info`) and ComfyUI (`curl -s http://127.0.0.1:8188/system_stats`) up front. If one is missing, use the fallback (headless `blender -b --python`, or give the user the prompts) and say so. Don't stall.

Finish with: the paths of the deliverables, the tri and texture stats, screenshots, and any open issues.
