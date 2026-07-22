#!/usr/bin/env python3
"""Validate a Geometry Board Scene JSON against V0.1 structural constraints."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
RATIOS = {"16:9", "4:3", "A4"}
ALLOWED_TYPES = {
    "point", "line", "circle", "rect", "plane", "cube", "cylinder",
    "dot-grid", "frame",
}


def validate(scene: dict) -> list[str]:
    errors: list[str] = []
    canvas = scene.get("canvas")
    intent = scene.get("intent")
    style = scene.get("style", {})
    nodes = scene.get("nodes")
    edges = scene.get("edges")

    if not isinstance(canvas, dict):
        errors.append("canvas must be an object")
    else:
        for key in ("width", "height"):
            if not isinstance(canvas.get(key), (int, float)) or canvas[key] <= 0:
                errors.append(f"canvas.{key} must be a positive number")
        if canvas.get("ratio") not in RATIOS:
            errors.append("canvas.ratio must be one of 16:9, 4:3, A4")
        if canvas.get("background", "#FFFFFF").upper() != "#FFFFFF":
            errors.append("canvas.background must default to #FFFFFF")

    if not isinstance(intent, dict):
        errors.append("intent must be an object")
    else:
        if not isinstance(intent.get("core_message"), str) or not intent["core_message"].strip():
            errors.append("intent.core_message must be a non-empty sentence")
        if not isinstance(intent.get("composition"), str) or not intent["composition"].strip():
            errors.append("intent.composition must be provided")

    if not isinstance(nodes, list):
        errors.append("nodes must be an array")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be an array")
        edges = []
    if len(nodes) > 15:
        errors.append(f"nodes has {len(nodes)} items; default maximum is 15")
    if len(edges) > 20:
        errors.append(f"edges has {len(edges)} items; default maximum is 20")

    ids: set[str] = set()
    total_text = 0
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"nodes[{index}] must be an object")
            continue
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id.strip():
            errors.append(f"nodes[{index}].id must be a non-empty string")
        elif node_id in ids:
            errors.append(f"duplicate node id: {node_id}")
        else:
            ids.add(node_id)
        if node.get("type") not in ALLOWED_TYPES:
            errors.append(f"nodes[{index}].type is not a supported semantic type")
        label = node.get("label", "")
        if not isinstance(label, str):
            errors.append(f"nodes[{index}].label must be a string")
        else:
            total_text += len(label)
            if len(label) > 12:
                errors.append(f"nodes[{index}].label exceeds 12 characters")
        importance = node.get("importance")
        if not isinstance(importance, int) or not 1 <= importance <= 5:
            errors.append(f"nodes[{index}].importance must be an integer from 1 to 5")

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edges[{index}] must be an object")
            continue
        if edge.get("from") not in ids or edge.get("to") not in ids:
            errors.append(f"edges[{index}] references an unknown node")

    focus = intent.get("focus_node") if isinstance(intent, dict) else None
    if focus is not None and focus not in ids:
        errors.append("intent.focus_node must reference an existing node")
    if total_text > 100:
        errors.append(f"node labels contain {total_text} characters; default maximum is 100")

    accent = style.get("accent_color") if isinstance(style, dict) else None
    if accent is not None and (not isinstance(accent, str) or not HEX.match(accent)):
        errors.append("style.accent_color must be a six-digit hex color")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene", type=Path, help="Path to a Scene JSON file")
    args = parser.parse_args()
    try:
        scene = json.loads(args.scene.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    errors = validate(scene) if isinstance(scene, dict) else ["Scene JSON root must be an object"]
    result = {"ok": not errors, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
