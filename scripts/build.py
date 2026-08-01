"""Build the Manhattan Residential Atlas map artifacts.

Inputs:
  data/manhattan_base.geojson   base neighborhood polygons (blackmad/Pediacities)
  scripts/atlas_data.py         report rankings + clip rules

Outputs:
  output/manhattan_atlas.geojson   tagged FeatureCollection (41 features)
  output/manhattan_atlas.svg       static vector map
  output/manhattan_atlas.png       static raster map
  output/manhattan_atlas.html      self-contained Leaflet interactive map
"""
import json
import math
import sys
from pathlib import Path

from shapely.geometry import mapping
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from atlas_data import TIERS, NEIGHBORHOODS  # noqa: E402
from geo import build_polygons, load_base  # noqa: E402

BASE_PATH = ROOT / "data" / "manhattan_base.geojson"
OUT_DIR = ROOT / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def write_geojson(rows, path):
    features = []
    for entry, geom in rows:
        tier = TIERS[entry["tier"]]
        features.append({
            "type": "Feature",
            "geometry": mapping(geom),
            "properties": {
                "rank": entry["rank"],
                "name": entry["name"],
                "tier": entry["tier"],
                "tier_label": tier["label"],
                "color": tier["color"],
                "one_liner": entry["one_liner"],
                "centroid_lat": entry["centroid"][0],
                "centroid_lng": entry["centroid"][1],
            },
        })
    fc = {"type": "FeatureCollection", "features": features}
    path.write_text(json.dumps(fc))
    print(f"wrote {path} ({len(features)} features)")
    return fc


# ---------- static rendering ----------

# Hand-tuned label nudges (lng_offset, lat_offset) for crowded midtown / tiny polys
LABEL_OFFSETS = {
    "Hudson Yards":               (-0.0035, 0.000),
    "Theater District":           ( 0.000, 0.001),
    "Midtown (core)":             ( 0.005, -0.001),
    "Sutton Place / Beekman":     ( 0.003, 0.001),
    "Hell's Kitchen":             (-0.002, 0.002),
    "Murray Hill":                ( 0.001, 0.000),
    "NoMad":                      ( 0.000, 0.001),
    "Flatiron":                   ( 0.000, -0.0015),
    "Kips Bay":                   ( 0.002, 0.000),
    "Stuyvesant Town / Peter Cooper": (0.000, 0.001),
    "Greenwich Village / NoHo":   ( 0.000, 0.001),
    "Nolita":                     ( 0.001, 0.000),
    "Civic Center":               (-0.0015, -0.001),
    "Hudson Square":              (-0.0010, 0.000),
    "Little Italy":               ( 0.001, 0.000),
    "Manhattanville":             (-0.001, 0.001),
    "Hamilton Heights":           (-0.001, 0.000),
    "Carnegie Hill":              (-0.001, 0.000),
    "Lenox Hill":                 ( 0.001, -0.001),
    "Yorkville":                  ( 0.001, 0.001),
    "Lincoln Square":             (-0.0005, -0.0005),
    "Roosevelt Island":           ( 0.001, 0.000),
    "Battery Park City":          (-0.001, 0.0015),
    "Meatpacking District":       (-0.0015, 0.000),
}


def label_anchor(entry, geom):
    """Return (lat, lng) for label. Prefer polygon-interior point; tiny
    nudges keep dense midtown labels from colliding."""
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

    # Equal-area-ish: scale longitude by cos(mean lat) so Manhattan looks right
    mean_lat = 40.78
    x_scale = math.cos(math.radians(mean_lat))

    def project(geom):
        from shapely.affinity import scale as shp_scale
        return shp_scale(geom, xfact=x_scale, yfact=1.0, origin=(0, 0))

    # Tall canvas; matplotlib's `subplots_adjust` reserves headroom for the
    # title so it never collides with the topmost polygon.
    fig, ax = plt.subplots(figsize=(11, 17), dpi=150)
    fig.subplots_adjust(top=0.93, bottom=0.02, left=0.02, right=0.98)
    ax.set_facecolor("#F4EFE6")
    fig.patch.set_facecolor("#F4EFE6")

    for entry, geom in rows:
        tier = TIERS[entry["tier"]]
        pgeom = project(geom)
        polys = pgeom.geoms if pgeom.geom_type == "MultiPolygon" else [pgeom]
        for p in polys:
            if p.is_empty:
                continue
            xs, ys = p.exterior.xy
            ax.fill(xs, ys, color=tier["color"], edgecolor="#FFFFFF",
                    linewidth=0.6, zorder=2)
            for hole in p.interiors:
                hx, hy = hole.xy
                ax.fill(hx, hy, color="#F4EFE6", zorder=2.5)

    for entry, geom in rows:
        lat, lng = label_anchor(entry, geom)
        x, y = lng * x_scale, lat
        area = max(geom.area, 1e-6)
        fs = max(5.5, min(9.5, 5.0 + 1.6 * math.log10(area * 1e6)))
        ax.text(x, y, entry["name"],
                ha="center", va="center", fontsize=fs,
                color="#1A1A1A", weight="semibold", zorder=4,
                path_effects=[withStroke(linewidth=2.2, foreground="white")])

    legend_handles = [
        Patch(facecolor=TIERS[t]["color"], edgecolor="white",
              label=f"Tier {t} — {TIERS[t]['label']}")
        for t in sorted(TIERS)
    ]
    # Legend in figure coords (top-right) so it never overlaps polygons
    leg = fig.legend(handles=legend_handles,
                     loc="upper right",
                     bbox_to_anchor=(0.985, 0.905),
                     frameon=True, facecolor="#FFFFFF", edgecolor="#888",
                     fontsize=9, title="Residential Character",
                     borderpad=0.8)
    leg.get_title().set_fontweight("bold")

    # Title in figure coords with comfortable headroom
    fig.text(0.5, 0.97, "Manhattan Residential Atlas",
             ha="center", va="top",
             fontsize=20, weight="bold", color="#1A1A1A")
    fig.text(0.5, 0.945,
             "Every neighborhood, ranked by safety · beauty · quiet · residential feel",
             ha="center", va="top", fontsize=11, color="#444")

    ax.set_aspect("equal")
    ax.set_axis_off()
    all_geom = unary_union([g for _, g in rows])
    pall = project(all_geom)
    minx, miny, maxx, maxy = pall.bounds
    pad = 0.004
    ax.set_xlim(minx - pad, maxx + pad)
    ax.set_ylim(miny - pad, maxy + pad)

    fig.savefig(svg_path, facecolor=fig.get_facecolor())
    fig.savefig(png_path, facecolor=fig.get_facecolor(), dpi=200)
    plt.close(fig)
    print(f"wrote {svg_path}")
    print(f"wrote {png_path}")


# ---------- interactive (Leaflet) ----------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Manhattan Residential Atlas</title>
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
    padding:10px 18px; border-radius:8px;
    box-shadow:0 2px 10px rgba(0,0,0,0.12);
    text-align:center; max-width:90vw;
  }
  .header h1 { margin:0; font-size:18px; color:#1A1A1A; }
  .header p  { margin:4px 0 0; font-size:12px; color:#555; }
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
    border:1px solid rgba(0,0,0,0.15);
  }
  .nbh-label {
    background:transparent; border:none; box-shadow:none;
    color:#1A1A1A; font-weight:600; font-size:11px;
    text-shadow: 0 0 3px #fff, 0 0 3px #fff, 0 0 3px #fff, 0 0 3px #fff;
    text-align:center; white-space:nowrap; pointer-events:none;
  }
  .leaflet-tooltip.nbh-tooltip {
    background:#fff; border:1px solid #888; border-radius:6px;
    padding:8px 10px; font-size:12.5px; max-width:260px; white-space:normal;
    box-shadow:0 2px 10px rgba(0,0,0,0.18);
  }
  .leaflet-tooltip.nbh-tooltip .rank {
    color:#666; font-size:11px; letter-spacing:.04em; text-transform:uppercase;
  }
  .leaflet-tooltip.nbh-tooltip .name { font-weight:700; font-size:14px; margin:2px 0 4px; }
  .leaflet-tooltip.nbh-tooltip .tier { font-weight:600; margin-bottom:4px; }
  .leaflet-tooltip.nbh-tooltip .desc { color:#333; }
</style>
</head>
<body>
<div class="header">
  <h1>Manhattan Residential Atlas</h1>
  <p>Every neighborhood, ranked by safety · beauty · quiet · residential feel</p>
</div>
<div id="map"></div>
<div class="legend" id="legend"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>
<script>
const TIERS = __TIERS_JSON__;
const ATLAS = __ATLAS_JSON__;

const map = L.map('map', { zoomControl: true, preferCanvas: false })
  .setView([40.785, -73.965], 12);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap, &copy; CARTO &mdash; Atlas data: report'
}).addTo(map);

function styleFor(feature) {
  return {
    color: '#FFFFFF',
    weight: 1,
    fillColor: feature.properties.color,
    fillOpacity: 0.78
  };
}

const layer = L.geoJSON(ATLAS, {
  style: styleFor,
  onEachFeature: (feature, lyr) => {
    const p = feature.properties;
    const html = `
      <div class="rank">Rank ${p.rank}</div>
      <div class="name">${p.name}</div>
      <div class="tier" style="color:${p.color}">Tier ${p.tier} — ${p.tier_label}</div>
      <div class="desc">${p.one_liner}</div>`;
    lyr.bindTooltip(html, {
      sticky: true, direction: 'top', className: 'nbh-tooltip', opacity: 1
    });
    lyr.on('mouseover', () => lyr.setStyle({ weight: 3, color: '#222', fillOpacity: 0.92 }));
    lyr.on('mouseout',  () => layer.resetStyle(lyr));
    // permanent name label at the report's centroid
    L.marker([p.centroid_lat, p.centroid_lng], {
      icon: L.divIcon({
        className: 'nbh-label',
        html: p.name,
        iconSize: [120, 14],
        iconAnchor: [60, 7]
      }),
      interactive: false,
      keyboard: false
    }).addTo(map);
  }
}).addTo(map);

map.fitBounds(layer.getBounds(), { padding: [40, 40] });

// Build legend
const legendEl = document.getElementById('legend');
legendEl.innerHTML = '<h4>Residential Character</h4>' +
  Object.keys(TIERS).map(t => `
    <div class="row">
      <span class="swatch" style="background:${TIERS[t].color}"></span>
      <span><strong>Tier ${t}</strong> &mdash; ${TIERS[t].label}</span>
    </div>`).join('');
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


def main():
    base = load_base(BASE_PATH)
    rows = build_polygons(base, NEIGHBORHOODS)
    fc = write_geojson(rows, OUT_DIR / "manhattan_atlas.geojson")
    render_static(rows, OUT_DIR / "manhattan_atlas.svg", OUT_DIR / "manhattan_atlas.png")
    render_html(fc, OUT_DIR / "manhattan_atlas.html")


if __name__ == "__main__":
    main()
