#!/usr/bin/env bash
# Optimize a GLB for a target.
#   bash scripts/optimize.sh in.glb engine [lods]   -> Godot/Unity/Unreal (no runtime-specific compression)
#   bash scripts/optimize.sh in.glb web    [lods]   -> Three.js/Babylon/R3F (meshopt + KTX2/WebP)
# Requires: npx (Node). Uses @gltf-transform/cli and gltfpack via npx if not installed globally.
# Env: TEX_SIZE (default 2048)
set -euo pipefail
IN="$1"; PROFILE="${2:-engine}"; LODS="${3:-}"
TEX_SIZE="${TEX_SIZE:-2048}"
BASE="${IN%.glb}"
GT="npx -y @gltf-transform/cli"
GP="npx -y gltfpack"
TMP="${BASE}.tmp.glb"

$GT dedup  "$IN"  "$TMP"
$GT prune  "$TMP" "$TMP"
$GT weld   "$TMP" "$TMP"
$GT resize "$TMP" "$TMP" --width "$TEX_SIZE" --height "$TEX_SIZE"

case "$PROFILE" in
  engine)
    OUT="${BASE}.engine.glb"
    mv "$TMP" "$OUT"
    ;;
  web)
    OUT="${BASE}.web.glb"
    if command -v toktx >/dev/null 2>&1; then TC=ktx2; else TC=webp; echo "toktx not found -> WebP textures"; fi
    $GT optimize "$TMP" "$OUT" --compress meshopt --texture-compress "$TC" --simplify false
    rm -f "$TMP"
    ;;
  *) echo "profile must be engine|web"; exit 2 ;;
esac

if [[ "$LODS" == "lods" ]]; then
  for R in 0.5 0.25 0.1; do
    if [[ "$PROFILE" == "web" ]]; then FLAGS="-cc"; else FLAGS="-noq"; fi
    $GP -i "$OUT" -o "${BASE}.lod_${R}.${PROFILE}.glb" -si "$R" $FLAGS
  done
fi

$GT inspect "$OUT" | head -n 60
ls -l "$IN" "${BASE}".*.glb
