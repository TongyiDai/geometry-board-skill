#!/usr/bin/env bash
set -u

root="$(cd "$(dirname "$0")/.." && pwd)"
python_ok=0
lark_ok=0
sample_ok=0

if command -v python3 >/dev/null 2>&1; then
  python_ok=1
  sample="$(find "$root/examples" -name '*.scene.json' -print -quit 2>/dev/null)"
  if [ -n "$sample" ] && python3 "$root/scripts/validate_scene.py" "$sample" >/dev/null 2>&1; then
    sample_ok=1
  fi
fi
if command -v lark-cli >/dev/null 2>&1 && lark-cli auth status --json --verify >/dev/null 2>&1; then
  lark_ok=1
fi

if [ "${1:-}" = "--json" ]; then
  printf '{"ok":%s,"skill_root":"%s","required":{"python3":%s,"sample_validation":%s},"optional":{"feishu_write":%s,"renderer":"host-provided"},"next":"%s"}\n' \
    "$([ "$python_ok" = 1 ] && [ "$sample_ok" = 1 ] && echo true || echo false)" \
    "$root" "$([ "$python_ok" = 1 ] && echo true || echo false)" \
    "$([ "$sample_ok" = 1 ] && echo true || echo false)" \
    "$([ "$lark_ok" = 1 ] && echo true || echo false)" \
    "$([ "$python_ok" = 1 ] && [ "$sample_ok" = 1 ] && echo 'generate or validate a Scene JSON' || echo 'run python3 scripts/validate_scene.py on an example')"
  exit 0
fi

echo "skill_root=$root"
echo "python3=$([ "$python_ok" = 1 ] && echo ready || echo missing)"
echo "sample_validation=$([ "$sample_ok" = 1 ] && echo passed || echo failed)"
echo "feishu_write=$([ "$lark_ok" = 1 ] && echo ready || echo unavailable)"
echo "renderer=host-provided"
