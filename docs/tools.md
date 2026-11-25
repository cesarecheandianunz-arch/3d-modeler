# Tool catalog (researched 2026-11-25 — verify licenses before commercial use)

## Agent control / MCP
- Blender MCP (community, `uvx mcp-for-blender`) — https://github.com/ahujasid/blender-mcp
- Blender Lab official MCP server (Blender 5.1+, GPL-3.0, port 9876 — don't run both) — https://www.blender.org/lab/mcp-server
- Godot MCP — already configured in this machine's Claude Code.
- Meshy MCP (commercial text/image→3D, texture, rig) — https://www.meshy.ai/tutorials/blender-mcp-guide

## Claude Code skills worth studying / importing
- htdt/godogen — full Godot 4 project generation incl. 3D assets — https://github.com/htdt/godogen
- blender-skills (blender-core, blender-asset-qa, engine export) — https://aiindigo.com/tool/blender-skills
- Blender web pipeline skill — https://claudemarketplaces.com/skills/freshtechbro/claudedesignskills/blender-web-pipeline
- asset-pipeline-3d — https://www.skills.sh/anthemflynn/ccmp/asset-pipeline-3d
- three.js model optimizer — https://skills.sh/openaec-foundation/three.js-claude-skill-package/threejs-agents-model-optimizer
- Godot asset generator — https://claudemarketplaces.com/skills/jwynia/agent-skills/godot-asset-generator
- Overview article — https://snyk.io/articles/top-claude-skills-3d-modeling-game-dev-shader-programming

## Image / multiview → 3D (open weights)
- TRELLIS.2 (Microsoft, MIT, 4B params) — https://sourceforge.net/mirror/trellis-2/
- Pixal3D (TencentARC, SIGGRAPH 2026, PBR, low-VRAM) — https://github.com/TencentARC/Pixal3D
- Hunyuan3D 2.0 / 2.1 / 3.0 (shape DiT + Paint PBR) — https://arxiv.org/html/2506.15442v1
- ComfyUI native TRELLIS.2 & Pixal3D — https://blog.comfy.org/p/trellis2-and-pixal3d-are-now-native
- ComfyUI Hunyuan3D multiview — https://docs.comfy.org/tutorials/3d/hunyuan3D-2
- ComfyUI-3D-Pack — https://github.com/MrForExample/ComfyUI-3D-Pack

## Texturing / materials
- Ubisoft CHORD (PBR estimation, ComfyUI nodes) — https://blog.comfy.org/p/ubisoft-open-sources-the-chord-model
- Material Maker (procedural, MIT, Godot-based) · ArmorLab · Dream Textures (Blender SD add-on)

## Retopology / UV
- AutoRemesher (quad remesh; now MIT) — https://digitalproduction.com/2026/07/28/autoremesher-final-goes-mit/
- Instant Meshes, QuadWild-BiMDF (quad remeshers)
- xatlas (C++ UV atlas, WASM ports) — https://github.com/jpcy/xatlas · Blender add-on https://github.com/fire/blender-xatlas

## Rigging
- UniRig (VAST-AI) — https://docsearch.algolia.com/mcp/docs/repo/vast-ai-research/unirig
- Blender Rigify (built-in), Mixamo (humanoids)

## Optimization / delivery (the "GPU-level" layer)
- meshoptimizer + gltfpack — https://github.com/zeux/meshoptimizer
- glTF-Transform CLI — https://www.npmjs.com/package/@gltf-transform/cli
- KTX-Software (toktx) for KTX2/Basis Universal textures
