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

    # Fix 1: Derive community labels from node content
    # Graphify uses generic "Community N" labels. We derive meaningful names
    # by looking at which nodes are in each community — package nodes (pkg_*)
    # and concept nodes give the best labels.
    nodes_match = re.search(r"const RAW_NODES = (\[.*?\]);", html, re.DOTALL)
    if nodes_match:
        nodes = json.loads(nodes_match.group(1))

        # Group nodes by community
        communities: dict[int, list[dict]] = {}
        for node in nodes:
            cid = node.get("community", 0)
            communities.setdefault(cid, []).append(node)

        # Derive label for each community
        derived_labels: dict[int, str] = {}
        for cid, members in communities.items():
            labels = [n["label"] for n in members]
            ids = [n["id"] for n in members]

            # Priority 1: if community contains a package node, use its name
            pkg_nodes = [n["label"] for n in members if n["id"].startswith("pkg_")]
            if pkg_nodes:
                derived_labels[cid] = pkg_nodes[0]
                continue

            # Priority 2: if community contains "field1st", it's the project root
            if "field1st" in ids:
                derived_labels[cid] = "Field1st"
                continue

            # Priority 3: use the highest-degree node's label as the community name
            top = max(members, key=lambda n: n.get("degree", 0))
            derived_labels[cid] = top["label"]

        # Apply labels to all nodes
        relabeled = 0
        for node in nodes:
            cid = node.get("community", 0)
            new_name = derived_labels.get(cid, node.get("community_name", ""))
            if new_name and node.get("community_name") != new_name:
                node["community_name"] = new_name
                relabeled += 1

        if relabeled:
            html = (
                html[: nodes_match.start(1)]
                + json.dumps(nodes)
                + html[nodes_match.end(1) :]
            )
            changes.append(
                f"communities: {', '.join(f'C{k}={v}' for k, v in sorted(derived_labels.items()))}"
            )

        # Also patch the legend data
        legend_match = re.search(r"const RAW_LEGEND = (\[.*?\]);", html, re.DOTALL)
        if legend_match:
            legend = json.loads(legend_match.group(1))
            for entry in legend:
                cid = entry.get("cid", -1)
                if cid in derived_labels:
                    entry["label"] = derived_labels[cid]
            html = (
                html[: legend_match.start(1)]
                + json.dumps(legend)
                + html[legend_match.end(1) :]
            )

    # Re-find nodes after potential modification above
    nodes_match = re.search(r"const RAW_NODES = (\[.*?\]);", html, re.DOTALL)

    # Fix 2: Ensure all nodes show labels
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

    # Fix 3: Tune physics for balanced spacing
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
