"""Shared polygon plumbing for the Manhattan map builds.

Both the residential atlas and the tree-canopy map describe their
neighborhoods with the same little source grammar:

    {"base": "<name>"}                          full base polygon
    {"base": "<name>", "remainder_of": True}    parent minus all carved children
    {"merge": ["<name>", ...]}                  union of base polygons
    {"clip_from": "<name>", "bbox": [...]}      rectangular clip out of parent
      + optional "subtract": [bbox, ...]        punch holes for prior clips
      + optional "and_clip_from"/"bbox2"        clip from a second parent, unioned
"""
import json
import sys

from shapely.geometry import shape, box
from shapely.ops import unary_union


def load_base(path):
    """name -> shapely geometry for a neighborhood base FeatureCollection."""
    raw = json.loads(path.read_text())
    return {f["properties"]["name"]: shape(f["geometry"]) for f in raw["features"]}


def build_polygons(base, entries):
    """Return list of (entry, polygon) for each entry in `entries`.

    Two-pass:
      1. Resolve all `clip_from` rectangles and `merge` operations.
      2. For `remainder_of` entries, subtract every clip taken from that parent.
    """
    # parent name -> list of clip polygons taken from it
    clips_by_parent: dict[str, list] = {}

    resolved = []
    for entry in entries:
        src = entry["source"]
        if "clip_from" in src:
            parent = base[src["clip_from"]]
            rect = box(*src["bbox"])
            geom = parent.intersection(rect)
            if "subtract" in src:
                geom = geom.difference(unary_union([box(*b) for b in src["subtract"]]))
            clips_by_parent.setdefault(src["clip_from"], []).append(rect)
            if "and_clip_from" in src:
                parent2 = base[src["and_clip_from"]]
                rect2 = box(*src["bbox2"])
                geom = unary_union([geom, parent2.intersection(rect2)])
                clips_by_parent.setdefault(src["and_clip_from"], []).append(rect2)
            resolved.append((entry, geom))
        elif "merge" in src:
            resolved.append((entry, unary_union([base[n] for n in src["merge"]])))
        elif src.get("remainder_of"):
            resolved.append((entry, None))  # filled in pass 2
        else:
            resolved.append((entry, base[src["base"]]))

    out = []
    for entry, geom in resolved:
        src = entry["source"]
        if src.get("remainder_of"):
            parent = base[src["base"]]
            cuts = clips_by_parent.get(src["base"], [])
            if cuts:
                parent = parent.difference(unary_union(cuts))
            geom = parent
        if geom.is_empty:
            print(f"WARN: empty geometry for {entry['name']}", file=sys.stderr)
        out.append((entry, geom))
    return out
