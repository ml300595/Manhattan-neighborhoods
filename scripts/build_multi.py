"""Build multi-borough NYC Residential Atlas map artifacts.

Inputs:
  data/manhattan_base.geojson   Manhattan base neighborhood polygons
  data/brooklyn_base.geojson    Brooklyn base neighborhood polygons (blackmad/Pediacities)
  data/queens_base.geojson      Queens base neighborhood polygons (blackmad/Pediacities)
  scripts/atlas_data.py         Manhattan neighborhood rankings + clip rules
  scripts/brooklyn_lic_data.py  Brooklyn & Queens neighborhood rankings + clip rules

Outputs:
  output/nyc_atlas_multi.geojson   tagged FeatureCollection (71 features)
  output/nyc_atlas_multi.svg       static vector map
  output/nyc_atlas_multi.png       static raster map (200 dpi)
  output/nyc_atlas_multi.html      self-contained Leaflet interactive map
"""
import json
import math
import sys
from pathlib import Path

from shapely.geometry import shape, mapping, box
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from atlas_data import TIERS, NEIGHBORHOODS as MANHATTAN_HOODS  # noqa: E402
from brooklyn_lic_data import ALL_OUTER_BOROUGH                  # noqa: E402

DATA_DIR = ROOT / "data"
OUT_DIR  = ROOT / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Attach borough tag to Manhattan entries (they don't have it)
for _e in MANHATTAN_HOODS:
    _e.setdefault("borough", "Manhattan")

ALL_HOODS = MANHATTAN_HOODS + ALL_OUTER_BOROUGH


# ── Base polygon loading ──────────────────────────────────────────────────────

def load_base():
    """Merge all three borough base GeoJSON files into one name→Shapely dict."""
    base = {}
    files = [
        DATA_DIR / "manhattan_base.geojson",
        DATA_DIR / "brooklyn_base.geojson",
        DATA_DIR / "queens_base.geojson",
    ]
    for fpath in files:
        raw = json.loads(fpath.read_text())
        for f in raw["features"]:
            name = f["properties"]["name"]
            base[name] = shape(f["geometry"])
    return base


# ── Polygon builder ───────────────────────────────────────────────────────────

def build_polygons(base, neighborhoods):
    """Two-pass polygon builder; same logic as build.py, extended for all boroughs."""
    clips_by_parent: dict[str, list] = {}
    resolved = []

    for entry in neighborhoods:
        src = entry["source"]

        if "clip_from" in src:
            pname = src["clip_from"]
            if pname not in base:
                print(f"WARN: missing base '{pname}' for {entry['name']}", file=sys.stderr)
                resolved.append((entry, None))
                continue
            parent = base[pname]
            rect   = box(*src["bbox"])
            geom   = parent.intersection(rect)
            if "subtract" in src:
                geom = geom.difference(unary_union([box(*b) for b in src["subtract"]]))
            clips_by_parent.setdefault(pname, []).append(rect)
            if "and_clip_from" in src:
                p2name = src["and_clip_from"]
                if p2name in base:
                    rect2 = box(*src["bbox2"])
                    geom  = unary_union([geom, base[p2name].intersection(rect2)])
                    clips_by_parent.setdefault(p2name, []).append(rect2)
            resolved.append((entry, geom))

        elif "merge" in src:
            parts = [base[n] for n in src["merge"] if n in base]
            resolved.append((entry, unary_union(parts) if parts else None))

        elif src.get("remainder_of"):
            resolved.append((entry, None))  # computed in pass 2

        else:
            bname = src["base"]
            if bname not in base:
                print(f"WARN: missing base '{bname}' for {entry['name']}", file=sys.stderr)
                resolved.append((entry, None))
            else:
                resolved.append((entry, base[bname]))

    # Pass 2 — remainders
    out = []
    for entry, geom in resolved:
        if entry["source"].get("remainder_of"):
            bname  = entry["source"]["base"]
            parent = base.get(bname)
            if parent is None:
                print(f"WARN: missing base '{bname}' for remainder {entry['name']}", file=sys.stderr)
                out.append((entry, None))
                continue
            cuts = clips_by_parent.get(bname, [])
            geom = parent.difference(unary_union(cuts)) if cuts else parent
        if geom is not None and geom.is_empty:
            print(f"WARN: empty geometry for {entry['name']}", file=sys.stderr)
        out.append((entry, geom))

    return [(e, g) for e, g in out if g is not None and not g.is_empty]


# ── GeoJSON writer ────────────────────────────────────────────────────────────

def write_geojson(rows, path):
    features = []
    for entry, geom in rows:
        tier = TIERS[entry["tier"]]
        features.append({
            "type": "Feature",
            "geometry": mapping(geom),
            "properties": {
                "rank":         entry["rank"],
                "name":         entry["name"],
                "borough":      entry.get("borough", ""),
                "tier":         entry["tier"],
                "tier_label":   tier["label"],
                "color":        tier["color"],
                "one_liner":    entry["one_liner"],
                "centroid_lat": entry["centroid"][0],
                "centroid_lng": entry["centroid"][1],
            },
        })
    fc = {"type": "FeatureCollection", "features": features}
    path.write_text(json.dumps(fc))
    print(f"wrote {path} ({len(features)} features)")
    return fc


# ── Static rendering ──────────────────────────────────────────────────────────

# Hand-tuned label nudges (lng_offset, lat_offset) to reduce collisions.
# Outer-borough names are generally less crowded; add only where needed.
LABEL_OFFSETS = {
    # Manhattan (carried over from build.py, crowded Midtown zone)
    "Hudson Yards":                     (-0.004, 0.000),
    "Theater District":                 ( 0.000, 0.001),
    "Midtown (core)":                   ( 0.005,-0.001),
    "Sutton Place / Beekman":           ( 0.003, 0.001),
    "Hell's Kitchen":                   (-0.002, 0.002),
    "Murray Hill":                      ( 0.001, 0.000),
    "NoMad":                            ( 0.000, 0.001),
    "Flatiron":                         ( 0.000,-0.0015),
    "Kips Bay":                         ( 0.002, 0.000),
    "Stuyvesant Town / Peter Cooper":   ( 0.000, 0.001),
    "Greenwich Village / NoHo":         ( 0.000, 0.001),
    "Nolita":                           ( 0.001, 0.000),
    "Civic Center":                     (-0.0015,-0.001),
    "Hudson Square":                    (-0.001, 0.000),
    "Manhattanville":                   (-0.001, 0.001),
    "Hamilton Heights":                 (-0.001, 0.000),
    "Carnegie Hill":                    (-0.001, 0.000),
    "Lenox Hill":                       ( 0.001,-0.001),
    "Yorkville":                        ( 0.001, 0.001),
    "Lincoln Square":                   (-0.0005,-0.0005),
    "Roosevelt Island":                 ( 0.001, 0.000),
    "Battery Park City":                (-0.001, 0.0015),
    "Meatpacking District":             (-0.0015, 0.000),
    # Brooklyn
    "Vinegar Hill":                     ( 0.002, 0.001),
    "DUMBO":                            ( 0.000,-0.001),
    "Boerum Hill":                      ( 0.001, 0.000),
    "Ditmas Park (Victorian Flatbush)": ( 0.000, 0.000),
    "Williamsburg (South / Southside)": ( 0.002, 0.000),
    "Prospect Heights":                 ( 0.000,-0.001),
    # Queens
    "Hunters Point (LIC Core)":         (-0.002, 0.001),
    "Hunters Point South (HPS)":        (-0.002,-0.001),
    "LIC (Court Square area)":          ( 0.003, 0.001),
    "Astoria (30th Ave / Main)":        ( 0.002, 0.000),
    "Astoria (Ditmars-Steinway North)": ( 0.002, 0.001),
}


def label_anchor(entry, geom):
    if geom.is_empty:
        return entry["centroid"]
    pt = geom.representative_point()
    lat, lng = pt.y, pt.x
    dlng, dlat = LABEL_OFFSETS.get(entry["name"], (0.0, 0.0))
    return (lat + dlat, lng + dlng)


def render_static(rows, svg_path, png_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.patheffects import withStroke

    # Equal-area projection: scale lon by cos(mean_lat)
    # Mean lat across Manhattan + Brooklyn + Queens ≈ 40.74
    mean_lat = 40.74
    x_scale  = math.cos(math.radians(mean_lat))

    def project(geom):
        from shapely.affinity import scale as shp_scale
        return shp_scale(geom, xfact=x_scale, yfact=1.0, origin=(0, 0))

    # Canvas: data aspect is ~2:1 portrait (see module docstring)
    fig, ax = plt.subplots(figsize=(13, 24), dpi=150)
    fig.subplots_adjust(top=0.945, bottom=0.01, left=0.01, right=0.99)
    bg = "#F4EFE6"
    ax.set_facecolor(bg)
    fig.patch.set_facecolor(bg)

    # Draw filled polygons
    for entry, geom in rows:
        tier  = TIERS[entry["tier"]]
        pgeom = project(geom)
        polys = pgeom.geoms if pgeom.geom_type == "MultiPolygon" else [pgeom]
        for p in polys:
            if p.is_empty:
                continue
            xs, ys = p.exterior.xy
            ax.fill(xs, ys, color=tier["color"], edgecolor="#FFFFFF",
                    linewidth=0.5, zorder=2)
            for hole in p.interiors:
                hx, hy = hole.xy
                ax.fill(hx, hy, color=bg, zorder=2.5)

    # Draw labels
    for entry, geom in rows:
        lat, lng = label_anchor(entry, geom)
        x, y     = lng * x_scale, lat
        # Scale font with polygon area (capped smaller than Manhattan-only map)
        area = max(geom.area, 1e-6)
        fs   = max(4.5, min(8.0, 4.5 + 1.4 * math.log10(area * 1e6)))
        ax.text(x, y, entry["name"],
                ha="center", va="center", fontsize=fs,
                color="#1A1A1A", weight="semibold", zorder=4,
                path_effects=[withStroke(linewidth=2.0, foreground="white")])

    # Borough watermark labels (non-intrusive, background layer)
    for bname, blat, blng in [("Manhattan", 40.785, -73.970),
                               ("Brooklyn",  40.660, -73.980),
                               ("Queens",    40.755, -73.915)]:
        ax.text(blng * x_scale, blat, bname,
                ha="center", va="center", fontsize=14,
                color="#B0A090", weight="bold", zorder=1, alpha=0.35,
                style="italic")

    # Legend
    legend_handles = [
        Patch(facecolor=TIERS[t]["color"], edgecolor="white",
              label=f"Tier {t} — {TIERS[t]['label']}")
        for t in sorted(TIERS)
    ]
    leg = fig.legend(handles=legend_handles,
                     loc="upper right",
                     bbox_to_anchor=(0.985, 0.910),
                     frameon=True, facecolor="#FFFFFF", edgecolor="#888",
                     fontsize=9, title="Residential Character",
                     borderpad=0.8)
    leg.get_title().set_fontweight("bold")

    # Title
    fig.text(0.5, 0.974, "NYC Multi-Borough Residential Atlas",
             ha="center", va="top", fontsize=19, weight="bold", color="#1A1A1A")
    fig.text(0.5, 0.952,
             "Manhattan · Brooklyn · Long Island City & Queens  ·  "
             "Ranked by safety · beauty · quiet · residential feel",
             ha="center", va="top", fontsize=9.5, color="#444")

    ax.set_aspect("equal")
    ax.set_axis_off()
    all_geom = unary_union([g for _, g in rows])
    pall     = project(all_geom)
    minx, miny, maxx, maxy = pall.bounds
    pad = 0.005
    ax.set_xlim(minx - pad, maxx + pad)
    ax.set_ylim(miny - pad, maxy + pad)

    fig.savefig(svg_path, facecolor=fig.get_facecolor())
    fig.savefig(png_path, facecolor=fig.get_facecolor(), dpi=200)
    plt.close(fig)
    print(f"wrote {svg_path}")
    print(f"wrote {png_path}")


# ── Interactive (Leaflet) HTML ────────────────────────────────────────────────

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>NYC Multi-Borough Residential Atlas</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
      integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
      crossorigin=""/>
<style>
  html, body { margin:0; height:100%; font-family: -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  #map { position:absolute; inset:0; background:#F4EFE6; }
  .header {
    position:absolute; top:12px; left:50%; transform:translateX(-50%);
    z-index:1000; background:rgba(255,255,255,0.94);
    padding:10px 20px; border-radius:8px;
    box-shadow:0 2px 10px rgba(0,0,0,0.12);
    text-align:center; max-width:92vw; white-space:nowrap;
  }
  .header h1 { margin:0; font-size:17px; color:#1A1A1A; }
  .header p  { margin:4px 0 0; font-size:11.5px; color:#555; }
  .legend {
    position:absolute; bottom:24px; left:16px; z-index:1000;
    background:rgba(255,255,255,0.96); padding:12px 14px;
    border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.15);
    font-size:12.5px; color:#222;
  }
  .legend h4 { margin:0 0 8px; font-size:13px; }
  .legend .row { display:flex; align-items:center; margin:3px 0; }
  .legend .swatch {
    width:16px; height:16px; border-radius:3px; margin-right:8px;
    border:1px solid rgba(0,0,0,0.15); flex-shrink:0;
  }
  .borough-filter {
    position:absolute; bottom:24px; right:16px; z-index:1000;
    background:rgba(255,255,255,0.96); padding:10px 14px;
    border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.15);
    font-size:12.5px; color:#222;
  }
  .borough-filter h4 { margin:0 0 8px; font-size:13px; }
  .borough-filter label { display:flex; align-items:center; margin:4px 0; cursor:pointer; gap:6px; }
  .nbh-label {
    background:transparent; border:none; box-shadow:none;
    color:#1A1A1A; font-weight:600; font-size:10.5px;
    text-shadow: 0 0 3px #fff, 0 0 3px #fff, 0 0 3px #fff, 0 0 3px #fff;
    text-align:center; white-space:nowrap; pointer-events:none;
  }
  .leaflet-tooltip.nbh-tooltip {
    background:#fff; border:1px solid #888; border-radius:6px;
    padding:8px 10px; font-size:12.5px; max-width:280px; white-space:normal;
    box-shadow:0 2px 10px rgba(0,0,0,0.18);
  }
  .leaflet-tooltip.nbh-tooltip .borough { color:#888; font-size:10px;
    letter-spacing:.06em; text-transform:uppercase; }
  .leaflet-tooltip.nbh-tooltip .name { font-weight:700; font-size:14px; margin:2px 0 4px; }
  .leaflet-tooltip.nbh-tooltip .tier { font-weight:600; margin-bottom:4px; }
  .leaflet-tooltip.nbh-tooltip .desc { color:#333; }
</style>
</head>
<body>
<div class="header">
  <h1>NYC Multi-Borough Residential Atlas</h1>
  <p>Manhattan &nbsp;·&nbsp; Brooklyn &nbsp;·&nbsp; Long Island City &amp; Queens
     &nbsp;&mdash;&nbsp; ranked by safety &middot; beauty &middot; quiet &middot; residential feel</p>
</div>
<div id="map"></div>
<div class="legend" id="legend"></div>
<div class="borough-filter" id="borough-filter">
  <h4>Borough</h4>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>
<script>
const TIERS = __TIERS_JSON__;
const ATLAS = __ATLAS_JSON__;

const map = L.map('map', { zoomControl: true, preferCanvas: false })
  .setView([40.72, -73.97], 11);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap, &copy; CARTO &mdash; Atlas data: report'
}).addTo(map);

function styleFor(feature) {
  return {
    color: '#FFFFFF', weight: 1,
    fillColor: feature.properties.color, fillOpacity: 0.75
  };
}

// Borough layer groups
const boroughLayers = {};
const allLabels     = [];

const geoLayer = L.geoJSON(ATLAS, {
  style: styleFor,
  onEachFeature: (feature, lyr) => {
    const p = feature.properties;
    const borough = p.borough || '';
    if (!boroughLayers[borough]) boroughLayers[borough] = L.layerGroup().addTo(map);

    const html = `
      <div class="borough">${borough}</div>
      <div class="name">${p.name}</div>
      <div class="tier" style="color:${p.color}">Tier ${p.tier} &mdash; ${p.tier_label}</div>
      <div class="desc">${p.one_liner}</div>`;
    lyr.bindTooltip(html, {
      sticky: true, direction: 'top', className: 'nbh-tooltip', opacity: 1
    });
    lyr.on('mouseover', () => lyr.setStyle({ weight: 3, color:'#222', fillOpacity:0.92 }));
    lyr.on('mouseout',  () => geoLayer.resetStyle(lyr));
    boroughLayers[borough].addLayer(lyr);

    // Permanent name label
    const labelMarker = L.marker([p.centroid_lat, p.centroid_lng], {
      icon: L.divIcon({
        className: 'nbh-label', html: p.name,
        iconSize: [130, 14], iconAnchor: [65, 7]
      }),
      interactive: false, keyboard: false
    });
    boroughLayers[borough].addLayer(labelMarker);
    allLabels.push({ borough, marker: labelMarker });
  }
}).addTo(map);

map.fitBounds(geoLayer.getBounds(), { padding: [40, 40] });

// Legend
const legendEl = document.getElementById('legend');
legendEl.innerHTML = '<h4>Residential Character</h4>' +
  Object.keys(TIERS).map(t => `
    <div class="row">
      <span class="swatch" style="background:${TIERS[t].color}"></span>
      <span><strong>Tier ${t}</strong> &mdash; ${TIERS[t].label}</span>
    </div>`).join('');

// Borough filter checkboxes
const filterEl = document.getElementById('borough-filter');
const boroughs = Object.keys(boroughLayers).sort();
boroughs.forEach(b => {
  const id = 'chk-' + b.replace(/\\s+/g,'_');
  filterEl.innerHTML += `
    <label>
      <input type="checkbox" id="${id}" checked onchange="toggleBorough('${b}', this.checked)">
      ${b}
    </label>`;
});

function toggleBorough(borough, show) {
  const lg = boroughLayers[borough];
  if (!lg) return;
  if (show) { lg.addTo(map); } else { map.removeLayer(lg); }
}

// Hide labels at low zoom to reduce clutter
map.on('zoomend', () => {
  const z = map.getZoom();
  allLabels.forEach(({marker}) => {
    const el = marker.getElement();
    if (el) el.style.display = (z >= 13) ? '' : 'none';
  });
});
// Initial hide at default zoom
setTimeout(() => map.fire('zoomend'), 100);
</script>
</body>
</html>
"""


def render_html(fc, path):
    tiers_json = json.dumps({str(k): {"label": v["label"], "color": v["color"]}
                             for k, v in TIERS.items()})
    atlas_json = json.dumps(fc, separators=(",", ":"))
    html = (HTML_TEMPLATE
            .replace("__TIERS_JSON__", tiers_json)
            .replace("__ATLAS_JSON__", atlas_json))
    path.write_text(html)
    print(f"wrote {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    base = load_base()
    rows = build_polygons(base, ALL_HOODS)
    fc   = write_geojson(rows, OUT_DIR / "nyc_atlas_multi.geojson")
    render_static(rows, OUT_DIR / "nyc_atlas_multi.svg", OUT_DIR / "nyc_atlas_multi.png")
    render_html(fc, OUT_DIR / "nyc_atlas_multi.html")
    print(f"\nDone — {len(rows)} neighborhoods across all boroughs.")


if __name__ == "__main__":
    main()
