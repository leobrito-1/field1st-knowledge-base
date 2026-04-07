#!/usr/bin/env python3
"""Post-process graphify-out/graph.html for better readability.

Fixes:
1. All node labels visible (Graphify hides low-degree nodes)
2. Balanced physics for spacing without excessive repulsion

Run after any /graphify rebuild:
    python3 ~/.claude/wiki/patch-graph.py
"""
import json
import re
from pathlib import Path

HTML_PATH = Path(__file__).parent / "graphify-out" / "graph.html"


def patch():
    if not HTML_PATH.exists():
        print("No graph.html found — run /graphify first")
        return

    html = HTML_PATH.read_text()
    changes = []

    # Fix 1: Ensure all nodes show labels
    # Graphify sets font.size=0 on low-degree nodes. Parse the JSON array
    # and set a minimum font size on every node.
    nodes_match = re.search(r"const RAW_NODES = (\[.*?\]);", html, re.DOTALL)
    if nodes_match:
        nodes = json.loads(nodes_match.group(1))
        patched = 0
        for node in nodes:
            font = node.get("font", {})
            if font.get("size", 0) < 11:
                font["size"] = 11
                node["font"] = font
                patched += 1
        if patched:
            html = (
                html[: nodes_match.start(1)]
                + json.dumps(nodes)
                + html[nodes_match.end(1) :]
            )
            changes.append(f"labels: restored {patched} hidden labels")

    # Fix 2: Tune physics for balanced spacing
    # Match the JS object literal (not JSON) for the forceAtlas2Based block
    physics_re = re.compile(
        r"(forceAtlas2Based:\s*\{)"
        r"(.*?)"
        r"(\},)",
        re.DOTALL,
    )
    m = physics_re.search(html)
    if m:
        new_physics = """
      gravitationalConstant: -120,
      centralGravity: 0.005,
      springLength: 200,
      springConstant: 0.04,
      damping: 0.7,
      avoidOverlap: 0.9,
    """
        html = html[: m.start(2)] + new_physics + html[m.end(2) :]
        changes.append("physics: balanced repulsion/spring/overlap")

    HTML_PATH.write_text(html)

    if changes:
        print(f"Patched graph.html: {', '.join(changes)}")
    else:
        print("No patches needed")


if __name__ == "__main__":
    patch()
