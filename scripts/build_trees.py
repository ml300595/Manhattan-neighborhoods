"""Build the Manhattan street-tree density map.

Inputs:
  data/manhattan_base.geojson   base neighborhood polygons (blackmad/Pediacities)
  scripts/tree_data.py          density bands, neighborhood estimates, corridors

Outputs:
  output/manhattan_trees.geojson   neighborhood polygons + corridor points
  output/manhattan_trees.svg       static vector map
  output/manhattan_trees.png       static raster map
  output/manhattan_trees.html      self-contained Leaflet interactive map

Also prints the area-weighted mean density, which should land near the
published borough average (~110 trees per street-mile) - that is the sanity
check on the estimates in tree_data.py.
"""
import json
import math
import sys
from pathlib import Path

from shapely.geometry import mapping
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from geo import build_polygons, load_base  # noqa: E402
from tree_data import BANDS, BOROUGH_AVG_TPM, NEIGHBORHOODS, STREETS  # noqa: E402

BASE_PATH = ROOT / "data" / "manhattan_base.geojson"
OUT_DIR = ROOT / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TITLE = "Manhattan Street-Tree Density"
SUBTITLE = ("Where the sidewalk tree line is densest \u00b7 estimated street "
            "trees per linear street-mile")


def ranked(rows):
    """Attach a 1..N rank by density, densest first. Parks are unranked."""
    scored = [r for r in rows if r[0]["trees_per_mile"] is not None]
    scored.sort(key=lambda r: -r[0]["trees_per_mile"])
    for i, (entry, _) in enumerate(scored, start=1):
        entry["rank"] = i
    for entry, _ in rows:
        entry.setdefault("rank", None)
    return rows


def calibration(rows):
    """Area-weighted mean density across non-park neighborhoods."""
    num = den = 0.0
    for entry, geom in rows:
        tpm = entry["trees_per_mile"]
        if tpm is None or geom.is_empty:
            continue
        num += tpm * geom.area
        den += geom.area
    return num / den if den else float("nan")


def write_geojson(rows, path):
    features = []
    for entry, geom in rows:
        band = BANDS[entry["band"]]
        features.append({
            "type": "Feature",
            "geometry": mapping(geom),
            "properties": {
                "kind": "neighborhood",
                "rank": entry["rank"],
                "name": entry["name"],
                "band": entry["band"],
                "band_label": band["label"],
                "band_range": band["range"],
                "color": band["color"],
                "trees_per_mile": entry["trees_per_mile"],
                "confidence": entry["confidence"],
                "estimated": entry["trees_per_mile"] is not None,
                "note": entry["note"],
                "centroid_lat": entry["centroid"][0],
                "centroid_lng": entry["centroid"][1],
            },
        })
    for s in STREETS:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [s["at"][1], s["at"][0]]},
            "properties": {
                "kind": "corridor",
                "name": s["name"],
                "extent": s["extent"],
                "area": s["area"],
                "corridor_kind": s["kind"],
                "stars": s["stars"],
                "note": s["note"],
                "approximate_location": True,
            },
        })
    fc = {"type": "FeatureCollection", "features": features}
    path.write_text(json.dumps(fc))
    print(f"wrote {path} ({len(features)} features)")
    return fc


# ---------- static rendering ----------

LABEL_OFFSETS = {
    "Hamilton Heights / Sugar Hill":  (-0.0015, 0.0005),
    "Central Harlem":                 (0.0015, -0.0015),
    "Manhattanville":                 (-0.001, 0.001),
    "Carnegie Hill":                  (-0.001, 0.000),
    "Yorkville":                      (0.001, 0.001),
    "Lincoln Square":                 (-0.0005, -0.0005),
    "Roosevelt Island":               (0.001, 0.000),
    "Hell's Kitchen":                 (-0.002, 0.002),
    "Hudson Yards":                   (-0.0035, 0.000),
    "Theater District":               (-0.001, 0.0022),
    "Midtown (core)":                 (0.005, -0.001),
    "Midtown East":                   (-0.002, 0.003),
    "Turtle Bay":                     (-0.001, -0.0008),
    "Sutton Place / Beekman":         (0.0035, 0.0018),
    "Murray Hill":                    (0.002, 0.0005),
    "Kips Bay":                       (0.002, 0.000),
    "Flatiron / NoMad":               (0.000, -0.0015),
    "Stuyvesant Town / Peter Cooper": (0.0012, 0.0026),
    "West Village":                   (-0.003, -0.0005),
    "Greenwich Village / NoHo":       (-0.001, 0.0018),
    "SoHo":                           (-0.0015, 0.0008),
    "Nolita / Little Italy":          (0.0025, -0.0005),
    "Lower East Side":                (0.0025, 0.0008),
    "Chinatown":                      (-0.0025, -0.0008),
    "Two Bridges":                    (0.0022, -0.0012),
    "Civic Center":                   (-0.001, -0.0015),
    "Battery Park City":              (-0.001, 0.0015),
}


def label_anchor(entry, geom):
    if geom.is_empty:
        return entry["centroid"]
    pt = geom.representative_point()
    dlng, dlat = LABEL_OFFSETS.get(entry["name"], (0.0, 0.0))
    return (pt.y + dlat, pt.x + dlng)


def render_static(rows, svg_path, png_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.patheffects import withStroke

    mean_lat = 40.78
    x_scale = math.cos(math.radians(mean_lat))

    def project(geom):
        from shapely.affinity import scale as shp_scale
        return shp_scale(geom, xfact=x_scale, yfact=1.0, origin=(0, 0))

    fig, ax = plt.subplots(figsize=(11, 17), dpi=150)
    fig.subplots_adjust(top=0.93, bottom=0.02, left=0.02, right=0.98)
    ax.set_facecolor("#F7F4EC")
    fig.patch.set_facecolor("#F7F4EC")

    for entry, geom in rows:
        pgeom = project(geom)
        polys = pgeom.geoms if pgeom.geom_type == "MultiPolygon" else [pgeom]
        for p in polys:
            if p.is_empty:
                continue
            xs, ys = p.exterior.xy
            ax.fill(xs, ys, color=BANDS[entry["band"]]["color"],
                    edgecolor="#FFFFFF", linewidth=0.6, zorder=2)
            for hole in p.interiors:
                hx, hy = hole.xy
                ax.fill(hx, hy, color="#F7F4EC", zorder=2.5)

    # Corridor markers, sized by how complete the canopy is.
    for s in STREETS:
        lat, lng = s["at"]
        ax.plot(lng * x_scale, lat, marker="o", markersize=2.4 + 1.5 * s["stars"],
                color="#FFD166", markeredgecolor="#4A3B10", markeredgewidth=0.6,
                zorder=5)

    for entry, geom in rows:
        lat, lng = label_anchor(entry, geom)
        area = max(geom.area, 1e-6)
        fs = max(5.5, min(9.5, 5.0 + 1.6 * math.log10(area * 1e6)))
        tpm = entry["trees_per_mile"]
        text = entry["name"] if tpm is None else f"{entry['name']}\n{tpm}"
        ax.text(lng * x_scale, lat, text, ha="center", va="center", fontsize=fs,
                color="#1A1A1A", weight="semibold", zorder=6, linespacing=1.1,
                path_effects=[withStroke(linewidth=2.2, foreground="white")])

    handles = [Patch(facecolor=BANDS[b]["color"], edgecolor="white",
                     label=f"{BANDS[b]['label']} \u2014 {BANDS[b]['range']}")
               for b in (1, 2, 3, 4, 5, 0)]
    handles.append(plt.Line2D([], [], marker="o", linestyle="none", markersize=7,
                              color="#FFD166", markeredgecolor="#4A3B10",
                              label="Named tree-lined corridor"))
    # Upper left is the only empty quadrant: the island runs bottom-left to
    # top-right, so it clears both Inwood and the Financial District.
    leg = fig.legend(handles=handles, loc="upper left",
                     bbox_to_anchor=(0.03, 0.90), frameon=True,
                     facecolor="#FFFFFF", edgecolor="#888", fontsize=9,
                     title="Street trees per street-mile", borderpad=0.8)
    leg.get_title().set_fontweight("bold")

    fig.text(0.5, 0.972, TITLE, ha="center", va="top", fontsize=20,
             weight="bold", color="#1A1A1A")
    fig.text(0.5, 0.949, SUBTITLE, ha="center", va="top", fontsize=10.5, color="#444")
    fig.text(0.5, 0.933,
             "Modelled estimates calibrated to the NYC street tree census "
             f"borough average (~{BOROUGH_AVG_TPM} / street-mile) "
             "\u2014 not measured counts",
             ha="center", va="top", fontsize=8.5, color="#777", style="italic")

    ax.set_aspect("equal")
    ax.set_axis_off()
    pall = project(unary_union([g for _, g in rows]))
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
<title>__TITLE__</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
      integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
      crossorigin=""/>
<style>
  html, body { margin:0; height:100%; font-family: -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  #map { position:absolute; inset:0; background:#F7F4EC; }
  .header {
    position:absolute; top:12px; left:50%; transform:translateX(-50%);
    z-index:1000; background:rgba(255,255,255,0.94);
    padding:10px 18px; border-radius:8px;
    box-shadow:0 2px 10px rgba(0,0,0,0.12);
    text-align:center; max-width:90vw;
  }
  .header h1 { margin:0; font-size:18px; color:#1A1A1A; }
  .header p  { margin:4px 0 0; font-size:12px; color:#555; }
  .header .caveat { font-size:11px; color:#888; font-style:italic; }
  .legend {
    position:absolute; bottom:24px; left:16px; z-index:1000;
    background:rgba(255,255,255,0.96); padding:12px 14px;
    border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.15);
    font-size:12.5px; color:#222; max-width:270px;
  }
  .legend h4 { margin:0 0 8px; font-size:13px; }
  .legend .row { display:flex; align-items:center; margin:3px 0; }
  .legend .swatch {
    width:16px; height:16px; border-radius:3px; margin-right:8px; flex:0 0 auto;
    border:1px solid rgba(0,0,0,0.15);
  }
  .legend .dot {
    width:12px; height:12px; border-radius:50%; margin:0 10px 0 2px; flex:0 0 auto;
    background:#FFD166; border:1.5px solid #4A3B10;
  }
  .legend .foot { margin-top:8px; font-size:11px; color:#777; line-height:1.35; }
  .nbh-label {
    background:transparent; border:none; box-shadow:none;
    color:#1A1A1A; font-weight:600; font-size:11px;
    text-shadow: 0 0 3px #fff, 0 0 3px #fff, 0 0 3px #fff, 0 0 3px #fff;
    text-align:center; white-space:nowrap; pointer-events:none;
  }
  .nbh-label .tpm { font-weight:700; }
  .leaflet-tooltip.nbh-tooltip {
    background:#fff; border:1px solid #888; border-radius:6px;
    padding:8px 10px; font-size:12.5px; max-width:280px; white-space:normal;
    box-shadow:0 2px 10px rgba(0,0,0,0.18);
  }
  .nbh-tooltip .rank { color:#666; font-size:11px; letter-spacing:.04em;
    text-transform:uppercase; }
  .nbh-tooltip .name { font-weight:700; font-size:14px; margin:2px 0 4px; }
  .nbh-tooltip .band { font-weight:600; margin-bottom:4px; }
  .nbh-tooltip .desc { color:#333; }
  .nbh-tooltip .meta { color:#888; font-size:11px; margin-top:5px; }
</style>
</head>
<body>
<div class="header">
  <h1>__TITLE__</h1>
  <p>__SUBTITLE__</p>
  <p class="caveat">Modelled estimates calibrated to the NYC street tree census
     borough average (~99 / street-mile) &mdash; not measured counts</p>
</div>
<div id="map"></div>
<div class="legend" id="legend"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>
<script>
const BANDS = __BANDS_JSON__;
const DATA  = __DATA_JSON__;

const map = L.map('map', { zoomControl: true }).setView([40.785, -73.965], 12);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap, &copy; CARTO &mdash; density: modelled estimate'
}).addTo(map);

const nbhs = { type:'FeatureCollection',
  features: DATA.features.filter(f => f.properties.kind === 'neighborhood') };
const corridors = DATA.features.filter(f => f.properties.kind === 'corridor');

const layer = L.geoJSON(nbhs, {
  style: f => ({ color:'#FFFFFF', weight:1,
                 fillColor:f.properties.color, fillOpacity:0.82 }),
  onEachFeature: (feature, lyr) => {
    const p = feature.properties;
    const head = p.rank ? `Rank ${p.rank} of ${nbhs.features.length - 1}` : 'Parkland';
    const tpm = p.trees_per_mile
      ? `~${p.trees_per_mile} trees / street-mile <span style="color:#999">(est.)</span>`
      : 'park trees, not street trees';
    lyr.bindTooltip(`
      <div class="rank">${head}</div>
      <div class="name">${p.name}</div>
      <div class="band" style="color:${p.color}">${p.band_label} &mdash; ${tpm}</div>
      <div class="desc">${p.note}</div>
      ${p.confidence === 'n/a' ? '' :
        `<div class="meta">estimate confidence: ${p.confidence}</div>`}`,
      { sticky:true, direction:'top', className:'nbh-tooltip', opacity:1 });
    lyr.on('mouseover', () => lyr.setStyle({ weight:3, color:'#222', fillOpacity:0.95 }));
    lyr.on('mouseout',  () => layer.resetStyle(lyr));
    L.marker([p.centroid_lat, p.centroid_lng], {
      icon: L.divIcon({ className:'nbh-label',
        html: p.trees_per_mile
          ? `${p.name}<br><span class="tpm">${p.trees_per_mile}</span>`
          : p.name,
        iconSize:[130,26], iconAnchor:[65,13] }),
      interactive:false, keyboard:false
    }).addTo(map);
  }
}).addTo(map);

corridors.forEach(f => {
  const p = f.properties;
  const [lng, lat] = f.geometry.coordinates;
  L.circleMarker([lat, lng], {
    radius: 3 + 2 * p.stars, color:'#4A3B10', weight:1.2,
    fillColor:'#FFD166', fillOpacity:0.95
  }).bindTooltip(`
      <div class="rank">${p.corridor_kind} &middot; ${'\\u2605'.repeat(p.stars)}</div>
      <div class="name">${p.name}</div>
      <div class="band" style="color:#8A6D1B">${p.extent} &middot; ${p.area}</div>
      <div class="desc">${p.note}</div>
      <div class="meta">marker is an approximate anchor for the block range</div>`,
    { sticky:true, direction:'top', className:'nbh-tooltip', opacity:1 })
   .addTo(map);
});

map.fitBounds(layer.getBounds(), { padding:[40,40] });

document.getElementById('legend').innerHTML =
  '<h4>Street trees per street-mile</h4>' +
  [1,2,3,4,5,0].map(b => `
    <div class="row">
      <span class="swatch" style="background:${BANDS[b].color}"></span>
      <span><strong>${BANDS[b].label}</strong> &mdash; ${BANDS[b].range}</span>
    </div>`).join('') +
  '<div class="row"><span class="dot"></span>' +
  '<span><strong>Named corridor</strong> &mdash; size = canopy completeness</span></div>' +
  '<div class="foot">One street-mile = both sidewalks of one mile of street. ' +
  'Borough average ~__BOROUGH_AVG__.</div>';
</script>
</body>
</html>
"""


def render_html(fc, path):
    bands_json = json.dumps({str(k): v for k, v in BANDS.items()})
    html = (HTML_TEMPLATE
            .replace("__TITLE__", TITLE)
            .replace("__SUBTITLE__", SUBTITLE)
            .replace("__BOROUGH_AVG__", str(BOROUGH_AVG_TPM))
            .replace("__BANDS_JSON__", bands_json)
            .replace("__DATA_JSON__", json.dumps(fc, separators=(",", ":"))))
    path.write_text(html)
    print(f"wrote {path}")


def main():
    base = load_base(BASE_PATH)
    rows = ranked(build_polygons(base, NEIGHBORHOODS))
    fc = write_geojson(rows, OUT_DIR / "manhattan_trees.geojson")
    render_static(rows, OUT_DIR / "manhattan_trees.svg", OUT_DIR / "manhattan_trees.png")
    render_html(fc, OUT_DIR / "manhattan_trees.html")
    mean = calibration(rows)
    print(f"area-weighted mean: {mean:.1f} trees/street-mile "
          f"(published borough average ~{BOROUGH_AVG_TPM})")


if __name__ == "__main__":
    main()
