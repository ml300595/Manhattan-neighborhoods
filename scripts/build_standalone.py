"""Render the tree-density map as a self-contained, zoomable SVG page.

output/manhattan_trees.html is a Leaflet map: it needs a CDN for the library
and a tile server for the basemap, so it is blank without internet and cannot
be published anywhere with a strict content policy. This build inlines
everything - geometry, styling, interaction - into one file that works
offline.

Outputs:
  output/manhattan_trees_zoomable.html   full standalone document
  --fragment PATH                        same page without the html/head/body
                                         wrapper, for hosts that supply one

Usage:
  python3 scripts/build_standalone.py [--fragment out.html]
"""
import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from tree_data import BANDS, BOROUGH_AVG_TPM  # noqa: E402

SRC = ROOT / "output" / "manhattan_trees.geojson"
OUT = ROOT / "output" / "manhattan_trees_zoomable.html"

LAT0 = 40.78          # projection reference latitude
K = 10_000            # degrees -> SVG user units


def project(lng, lat):
    return (lng * math.cos(math.radians(LAT0)) * K, -lat * K)


def rings(geometry):
    """Yield each polygon's list of rings, for Polygon and MultiPolygon."""
    if geometry["type"] == "Polygon":
        yield geometry["coordinates"]
    elif geometry["type"] == "MultiPolygon":
        yield from geometry["coordinates"]


def path_data(geometry, dx, dy):
    parts = []
    for poly in rings(geometry):
        for ring in poly:
            pts = []
            for lng, lat in ring:
                x, y = project(lng, lat)
                pts.append(f"{x - dx:.1f},{y - dy:.1f}")
            parts.append("M" + "L".join(pts) + "Z")
    return "".join(parts)


def ring_area(ring):
    """Shoelace area in projected units - used only to rank label size."""
    total = 0.0
    for i in range(len(ring) - 1):
        (x1, y1), (x2, y2) = project(*ring[i]), project(*ring[i + 1])
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def short_range(text):
    """'145+ trees / street-mile' -> '145+'; keeps the legend on one line."""
    text = text.replace(" trees / street-mile", "")
    return "not street trees" if "canopy" in text else text


def build_scene():
    fc = json.loads(SRC.read_text())

    xs, ys = [], []
    for f in fc["features"]:
        if f["geometry"]["type"] == "Point":
            x, y = project(*f["geometry"]["coordinates"])
            xs.append(x)
            ys.append(y)
            continue
        for poly in rings(f["geometry"]):
            for lng, lat in poly[0]:
                x, y = project(lng, lat)
                xs.append(x)
                ys.append(y)
    pad = 30
    dx, dy = min(xs) - pad, min(ys) - pad
    width = max(xs) - min(xs) + 2 * pad
    height = max(ys) - min(ys) + 2 * pad

    hoods, corridors = [], []
    for f in fc["features"]:
        p = f["properties"]
        if p["kind"] == "neighborhood":
            area = max((ring_area(poly[0]) for poly in rings(f["geometry"])), default=0)
            cx, cy = project(p["centroid_lng"], p["centroid_lat"])
            r, g, b = (int(p["color"][i:i + 2], 16) for i in (1, 3, 5))
            hoods.append({
                # Label contrast comes from the fill, not the page theme: the
                # choropleth colors are the same in light and dark mode.
                "onLight": (0.2126 * r + 0.7152 * g + 0.0722 * b) > 140,
                "name": p["name"], "rank": p["rank"], "tpm": p["trees_per_mile"],
                "band": p["band"], "bandLabel": p["band_label"], "color": p["color"],
                "confidence": p["confidence"], "note": p["note"],
                "d": path_data(f["geometry"], dx, dy),
                "cx": round(cx - dx, 1), "cy": round(cy - dy, 1),
                "area": round(area),
            })
        else:
            x, y = project(*f["geometry"]["coordinates"])
            corridors.append({
                "name": p["name"], "extent": p["extent"], "area": p["area"],
                "type": p["corridor_kind"], "stars": p["stars"], "note": p["note"],
                "x": round(x - dx, 1), "y": round(y - dy, 1),
            })

    hoods.sort(key=lambda h: (h["rank"] is None, h["rank"]))
    corridors.sort(key=lambda c: (-c["stars"], c["name"]))
    # Only the biggest polygons keep a label when zoomed all the way out.
    cutoff = sorted((h["area"] for h in hoods), reverse=True)[:14][-1]
    for h in hoods:
        # Parks carry no density number, so their labels wait for a zoom in.
        h["big"] = h["area"] >= cutoff and h["tpm"] is not None
    return {"w": round(width), "h": round(height),
            "hoods": hoods, "corridors": corridors}


PAGE = """<style>
:root {
  --paper:#EDF0E8; --panel:#FAFBF7; --panel-edge:#D3DACC;
  --ink:#16211A; --ink-soft:#4C5A50; --ink-faint:#78846F;
  --accent:#8A5A12; --accent-soft:#C8961F; --focus:#2F6E4E;
  --shadow:0 1px 2px rgba(20,35,25,.10), 0 8px 24px rgba(20,35,25,.10);
  --stroke-map:#FBFCF9;
  --serif:Georgia,"Iowan Old Style","Times New Roman",serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark) {
  :root {
    --paper:#0F1512; --panel:#161D18; --panel-edge:#2A342C;
    --ink:#E6EDE4; --ink-soft:#A3B0A2; --ink-faint:#7C8A7C;
    --accent:#E3B255; --accent-soft:#F0C877; --focus:#7FCBA0;
    --shadow:0 1px 2px rgba(0,0,0,.5), 0 10px 30px rgba(0,0,0,.45);
    --stroke-map:#0F1512;
  }
}
:root[data-theme="dark"] {
  --paper:#0F1512; --panel:#161D18; --panel-edge:#2A342C;
  --ink:#E6EDE4; --ink-soft:#A3B0A2; --ink-faint:#7C8A7C;
  --accent:#E3B255; --accent-soft:#F0C877; --focus:#7FCBA0;
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 10px 30px rgba(0,0,0,.45);
  --stroke-map:#0F1512;
}
:root[data-theme="light"] {
  --paper:#EDF0E8; --panel:#FAFBF7; --panel-edge:#D3DACC;
  --ink:#16211A; --ink-soft:#4C5A50; --ink-faint:#78846F;
  --accent:#8A5A12; --accent-soft:#C8961F; --focus:#2F6E4E;
  --shadow:0 1px 2px rgba(20,35,25,.10), 0 8px 24px rgba(20,35,25,.10);
  --stroke-map:#FBFCF9;
}

* { box-sizing:border-box; }
body {
  margin:0; background:var(--paper); color:var(--ink);
  font-family:var(--sans); font-size:15px; line-height:1.5;
  -webkit-text-size-adjust:100%;
}
.wrap {
  display:grid; grid-template-columns:minmax(300px,340px) 1fr;
  gap:18px; padding:18px; height:100vh; max-width:1500px; margin:0 auto;
}
@media (max-width:900px) {
  .wrap { grid-template-columns:1fr; height:auto; }
  .rail { max-height:none; }
  .stage { height:72vh; }
}

/* ---------- rail ---------- */
.rail {
  display:flex; flex-direction:column; gap:14px; min-height:0;
  overflow-y:auto; padding-right:4px;
}
.masthead h1 {
  font-family:var(--serif); font-weight:400; font-size:26px; line-height:1.15;
  margin:0 0 6px; text-wrap:balance; letter-spacing:-.01em;
}
.masthead .lede { margin:0; color:var(--ink-soft); font-size:13.5px; }
.masthead .caveat {
  margin:8px 0 0; padding-top:8px; border-top:1px solid var(--panel-edge);
  color:var(--ink-faint); font-size:12px;
}
.eyebrow {
  font-size:11px; letter-spacing:.10em; text-transform:uppercase;
  color:var(--ink-faint); margin:0 0 8px;
}
.card {
  background:var(--panel); border:1px solid var(--panel-edge);
  border-radius:10px; padding:14px;
}
.key { display:flex; flex-direction:column; gap:7px; }
.key .row { display:flex; align-items:center; gap:9px; font-size:13px;
            white-space:nowrap; }
.key .chip {
  width:15px; height:15px; border-radius:3px; flex:0 0 auto;
  border:1px solid rgba(0,0,0,.18);
}
.key .dot {
  width:11px; height:11px; border-radius:50%; margin:0 2px 0 2px; flex:0 0 auto;
  background:var(--accent-soft); border:1.5px solid var(--accent);
}
.key .val { color:var(--ink-soft); font-family:var(--mono); font-size:12px; }
.key .foot {
  margin-top:4px; padding-top:9px; border-top:1px solid var(--panel-edge);
  color:var(--ink-faint); font-size:12px; line-height:1.45;
}
.tabs { display:flex; gap:6px; }
.tabs button {
  flex:1; font:inherit; font-size:13px; padding:7px 10px; cursor:pointer;
  color:var(--ink-soft); background:transparent; border:1px solid var(--panel-edge);
  border-radius:8px;
}
.tabs button[aria-selected="true"] {
  background:var(--panel); color:var(--ink); border-color:var(--accent);
  box-shadow:inset 0 -2px 0 var(--accent);
}
.list { list-style:none; margin:0; padding:0; }
.list li + li { border-top:1px solid var(--panel-edge); }
.list button {
  width:100%; display:flex; align-items:baseline; gap:10px; text-align:left;
  font:inherit; padding:8px 6px; background:none; border:0; cursor:pointer;
  color:inherit; border-radius:6px;
}
.list button:hover { background:color-mix(in srgb, var(--accent) 10%, transparent); }
.list .n {
  font-family:var(--mono); font-size:11.5px; color:var(--ink-faint);
  width:20px; flex:0 0 auto; font-variant-numeric:tabular-nums;
}
.list .swatch {
  width:9px; height:22px; border-radius:2px; flex:0 0 auto; align-self:center;
}
.list .nm { flex:1; font-size:13.5px; line-height:1.25; }
.list .nm small { display:block; color:var(--ink-faint); font-size:11.5px; }
.list .v {
  font-family:var(--mono); font-size:13px; font-variant-numeric:tabular-nums;
  color:var(--ink-soft); flex:0 0 auto;
}
.list .stars { color:var(--accent); font-size:12px; letter-spacing:.06em; flex:0 0 auto; }

/* ---------- map ---------- */
.stage {
  position:relative; min-height:0; background:var(--panel);
  border:1px solid var(--panel-edge); border-radius:12px; overflow:hidden;
  box-shadow:var(--shadow);
}
svg { display:block; width:100%; height:100%; touch-action:none; cursor:grab; }
svg.dragging { cursor:grabbing; }
.hood { stroke:var(--stroke-map); vector-effect:non-scaling-stroke; stroke-width:1.1; }
.hood:hover, .hood.on { stroke:var(--ink); stroke-width:2.2; }
.corridor { fill:var(--accent-soft); stroke:var(--accent); vector-effect:non-scaling-stroke; }
.corridor.on { stroke:var(--ink); stroke-width:3; }
.lbl {
  font-family:var(--sans); font-weight:600; paint-order:stroke;
  stroke-width:3px; stroke-linejoin:round; text-anchor:middle;
  pointer-events:none;
}
.lbl.on-light { fill:#141E16; stroke:rgba(252,253,250,.92); }
.lbl.on-dark  { fill:#F4F8F2; stroke:rgba(10,20,13,.75); }
.lbl tspan.v { font-family:var(--mono); font-weight:700; }

.controls { position:absolute; right:12px; bottom:12px; display:flex; gap:6px; }
.controls button {
  width:34px; height:34px; font:inherit; font-size:15px; cursor:pointer;
  background:var(--panel); color:var(--ink); border:1px solid var(--panel-edge);
  border-radius:8px; box-shadow:var(--shadow); line-height:1;
}
.controls button:hover { border-color:var(--accent); }
.hint {
  position:absolute; left:12px; bottom:12px; color:var(--ink-faint);
  font-size:11.5px; background:color-mix(in srgb, var(--panel) 88%, transparent);
  padding:4px 8px; border-radius:6px;
}
.tip {
  position:absolute; z-index:5; pointer-events:none; opacity:0; max-width:270px;
  background:var(--panel); border:1px solid var(--panel-edge); border-radius:9px;
  padding:9px 11px; box-shadow:var(--shadow); transition:opacity .10s ease;
}
.tip.on { opacity:1; }
.tip .t-rank {
  font-size:10.5px; letter-spacing:.09em; text-transform:uppercase;
  color:var(--ink-faint);
}
.tip .t-name { font-family:var(--serif); font-size:16px; margin:2px 0 3px; }
.tip .t-band { font-size:12.5px; font-weight:600; margin-bottom:5px; }
.tip .t-band .v { font-family:var(--mono); }
.tip .t-note { font-size:12.5px; color:var(--ink-soft); line-height:1.4; }
.tip .t-meta { font-size:11px; color:var(--ink-faint); margin-top:6px; }

button:focus-visible, [tabindex]:focus-visible {
  outline:2px solid var(--focus); outline-offset:2px;
}
@media (prefers-reduced-motion:reduce) { * { transition:none !important; } }
</style>

<div class="wrap">
  <div class="rail">
    <div class="masthead">
      <p class="eyebrow">Manhattan &middot; street trees</p>
      <h1>Where the sidewalk canopy is thickest</h1>
      <p class="lede">Estimated street trees per linear street-mile &mdash; both
        sidewalks of one mile of street, counted together.</p>
      <p class="caveat">Modelled estimates calibrated to the NYC street tree
        census borough average (~__AVG__ per street-mile), not measured counts.
        Trust the ordering; treat the digits as a scale.</p>
    </div>

    <div class="card key" id="key"></div>

    <div class="tabs" role="tablist">
      <button role="tab" id="tab-hoods" aria-selected="true" aria-controls="panel-list">
        Neighborhoods</button>
      <button role="tab" id="tab-streets" aria-selected="false" aria-controls="panel-list">
        Named streets</button>
    </div>
    <div class="card" style="padding:6px 10px">
      <ul class="list" id="panel-list" role="tabpanel"></ul>
    </div>
  </div>

  <div class="stage">
    <svg id="map" viewBox="0 0 __W__ __H__" preserveAspectRatio="xMidYMid meet"
         role="img" aria-label="Map of Manhattan shaded by street-tree density">
      <g id="scene">
        <g id="g-hoods"></g>
        <g id="g-labels"></g>
        <g id="g-corridors"></g>
      </g>
    </svg>
    <div class="controls">
      <button id="zoom-in"  title="Zoom in (+)"  aria-label="Zoom in">+</button>
      <button id="zoom-out" title="Zoom out (-)" aria-label="Zoom out">&minus;</button>
      <button id="zoom-rst" title="Reset view (0)" aria-label="Reset view">&#8634;</button>
    </div>
    <p class="hint">Scroll or pinch to zoom &middot; drag to pan</p>
    <div class="tip" id="tip"></div>
  </div>
</div>

<script>
const SCENE = __SCENE__;
const BANDS = __BANDS__;
const NS = "http://www.w3.org/2000/svg";

const svg = document.getElementById('map');
const scene = document.getElementById('scene');
const tip = document.getElementById('tip');
const stage = svg.parentElement;

/* ---------- draw ---------- */
const el = (tag, attrs) => {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs) n.setAttribute(k, attrs[k]);
  return n;
};

const gH = document.getElementById('g-hoods');
const gC = document.getElementById('g-corridors');
const gL = document.getElementById('g-labels');

SCENE.hoods.forEach((h, i) => {
  const p = el('path', { d:h.d, fill:h.color, class:'hood', 'data-i':i,
                         tabindex:'0', role:'img', 'aria-label':h.name });
  gH.appendChild(p);

  const t = el('text', { class:'lbl ' + (h.onLight ? 'on-light' : 'on-dark'),
                         x:h.cx, y:h.cy, 'data-big':h.big ? 1 : 0 });
  t.appendChild(el('tspan', { x:h.cx, dy:'0' })).textContent = h.name;
  if (h.tpm !== null) {
    const v = el('tspan', { x:h.cx, dy:'1.15em', class:'v' });
    v.textContent = h.tpm;
    t.appendChild(v);
  }
  gL.appendChild(t);
});

SCENE.corridors.forEach((c, i) => {
  gC.appendChild(el('circle', { cx:c.x, cy:c.y, r:6, class:'corridor',
                                'data-i':i, tabindex:'0', role:'img',
                                'aria-label':c.name }));
});

/* ---------- zoom + pan ---------- */
const VB = { w:SCENE.w, h:SCENE.h };
let k = 1, tx = 0, ty = 0;

function clamp() {
  k = Math.min(14, Math.max(1, k));
  const maxX = VB.w * (k - 1), maxY = VB.h * (k - 1);
  tx = Math.min(0, Math.max(-maxX, tx));
  ty = Math.min(0, Math.max(-maxY, ty));
}

function apply() {
  clamp();
  scene.setAttribute('transform', `translate(${tx} ${ty}) scale(${k})`);
  // Keep labels and markers at a constant on-screen size.
  const px = (svg.clientHeight / VB.h) * k || 1;
  gL.querySelectorAll('text').forEach(t => {
    t.setAttribute('font-size', 12 / px);
    t.style.display = (t.dataset.big === '1' || k > 1.7) ? '' : 'none';
  });
  gC.querySelectorAll('circle').forEach((c, i) => {
    c.setAttribute('r', (3 + 1.6 * SCENE.corridors[i].stars) / px);
  });
}

function zoomAt(factor, cx, cy) {   // cx, cy in viewBox units
  const k2 = Math.min(14, Math.max(1, k * factor));
  tx = cx - (cx - tx) * (k2 / k);
  ty = cy - (cy - ty) * (k2 / k);
  k = k2;
  apply();
}

function toScene(evt) {
  const r = svg.getBoundingClientRect();
  // preserveAspectRatio="meet": the viewBox is letterboxed inside the element.
  const s = Math.min(r.width / VB.w, r.height / VB.h);
  return { x:(evt.clientX - r.left - (r.width - VB.w * s) / 2) / s,
           y:(evt.clientY - r.top - (r.height - VB.h * s) / 2) / s };
}

svg.addEventListener('wheel', e => {
  e.preventDefault();
  const p = toScene(e);
  zoomAt(Math.exp(-e.deltaY * 0.0015), p.x, p.y);
}, { passive:false });

let drag = null;
svg.addEventListener('pointerdown', e => {
  drag = { x:e.clientX, y:e.clientY, tx, ty };
  svg.setPointerCapture(e.pointerId);
  svg.classList.add('dragging');
});
svg.addEventListener('pointermove', e => {
  if (!drag) return;
  const r = svg.getBoundingClientRect();
  const s = Math.min(r.width / VB.w, r.height / VB.h);
  tx = drag.tx + (e.clientX - drag.x) / s;
  ty = drag.ty + (e.clientY - drag.y) / s;
  apply();
});
['pointerup', 'pointercancel'].forEach(t => svg.addEventListener(t, e => {
  drag = null;
  svg.classList.remove('dragging');
}));

document.getElementById('zoom-in').onclick  = () => zoomAt(1.5, VB.w / 2, VB.h / 2);
document.getElementById('zoom-out').onclick = () => zoomAt(1 / 1.5, VB.w / 2, VB.h / 2);
document.getElementById('zoom-rst').onclick = () => { k = 1; tx = ty = 0; apply(); };

document.addEventListener('keydown', e => {
  if (e.target.matches('input, textarea')) return;
  const step = 60 / k;
  if (e.key === '+' || e.key === '=') zoomAt(1.5, VB.w / 2, VB.h / 2);
  else if (e.key === '-') zoomAt(1 / 1.5, VB.w / 2, VB.h / 2);
  else if (e.key === '0') { k = 1; tx = ty = 0; apply(); }
  else if (e.key === 'ArrowLeft')  { tx += step; apply(); }
  else if (e.key === 'ArrowRight') { tx -= step; apply(); }
  else if (e.key === 'ArrowUp')    { ty += step; apply(); }
  else if (e.key === 'ArrowDown')  { ty -= step; apply(); }
  else return;
  e.preventDefault();
});

function focusOn(x, y, level) {
  k = level;
  tx = VB.w / 2 - x * k;
  ty = VB.h / 2 - y * k;
  apply();
}

/* ---------- tooltips ---------- */
function showTip(html, evt) {
  tip.innerHTML = html;
  tip.classList.add('on');
  const r = stage.getBoundingClientRect();
  let x = evt.clientX - r.left + 14, y = evt.clientY - r.top + 14;
  x = Math.min(x, r.width - tip.offsetWidth - 8);
  y = Math.min(y, r.height - tip.offsetHeight - 8);
  tip.style.left = Math.max(8, x) + 'px';
  tip.style.top = Math.max(8, y) + 'px';
}
const hideTip = () => tip.classList.remove('on');

const hoodTip = h => `
  <div class="t-rank">${h.rank ? 'Rank ' + h.rank + ' of 40' : 'Parkland'}</div>
  <div class="t-name">${h.name}</div>
  <div class="t-band" style="color:${h.color}">${h.bandLabel}${
    h.tpm !== null ? ' &middot; <span class="v">' + h.tpm + '</span> / street-mile' : ''}</div>
  <div class="t-note">${h.note}</div>
  ${h.confidence === 'n/a' ? '' :
    `<div class="t-meta">estimate confidence: ${h.confidence}</div>`}`;

const corridorTip = c => `
  <div class="t-rank">${c.type} &middot; ${'\\u2605'.repeat(c.stars)}</div>
  <div class="t-name">${c.name}</div>
  <div class="t-band" style="color:var(--accent)">${c.extent} &middot; ${c.area}</div>
  <div class="t-note">${c.note}</div>
  <div class="t-meta">marker is an approximate anchor for that block range</div>`;

gH.addEventListener('pointermove', e => {
  const p = e.target.closest('.hood');
  if (p && !drag) showTip(hoodTip(SCENE.hoods[p.dataset.i]), e); else hideTip();
});
gC.addEventListener('pointermove', e => {
  const c = e.target.closest('.corridor');
  if (c && !drag) showTip(corridorTip(SCENE.corridors[c.dataset.i]), e);
});
svg.addEventListener('pointerleave', hideTip);
svg.addEventListener('pointerdown', hideTip);

/* ---------- legend ---------- */
document.getElementById('key').innerHTML =
  '<p class="eyebrow" style="margin:0 0 2px">Trees per street-mile</p>' +
  [1, 2, 3, 4, 5, 0].map(b => `
    <div class="row">
      <span class="chip" style="background:${BANDS[b].color}"></span>
      <span>${BANDS[b].label}</span>
      <span class="val" style="margin-left:auto">${BANDS[b].short}</span>
    </div>`).join('') +
  `<div class="row"><span class="dot"></span>
     <span>Named tree-lined street</span>
     <span class="val" style="margin-left:auto">size = canopy</span></div>
   <div class="foot">Borough average is about __AVG__ per street-mile:
     roughly one tree every 100 feet of frontage.</div>`;

/* ---------- rail list ---------- */
const list = document.getElementById('panel-list');
const tabH = document.getElementById('tab-hoods');
const tabS = document.getElementById('tab-streets');

function renderHoods() {
  list.innerHTML = SCENE.hoods.map((h, i) => `
    <li><button data-i="${i}">
      <span class="n">${h.rank ?? '&mdash;'}</span>
      <span class="swatch" style="background:${h.color}"></span>
      <span class="nm">${h.name}<small>${h.bandLabel}</small></span>
      <span class="v">${h.tpm ?? '&mdash;'}</span>
    </button></li>`).join('');
  list.querySelectorAll('button').forEach(b => b.onclick = () => {
    const h = SCENE.hoods[b.dataset.i];
    focusOn(h.cx, h.cy, 4);
    gH.querySelectorAll('.hood').forEach(p => p.classList.toggle('on', p.dataset.i === b.dataset.i));
  });
}

function renderStreets() {
  list.innerHTML = SCENE.corridors.map((c, i) => `
    <li><button data-i="${i}">
      <span class="stars">${'\\u2605'.repeat(c.stars)}</span>
      <span class="nm">${c.name}<small>${c.extent} &middot; ${c.area}</small></span>
    </button></li>`).join('');
  list.querySelectorAll('button').forEach(b => b.onclick = () => {
    const c = SCENE.corridors[b.dataset.i];
    focusOn(c.x, c.y, 7);
    gC.querySelectorAll('.corridor').forEach(p => p.classList.toggle('on', p.dataset.i === b.dataset.i));
  });
}

function selectTab(which) {
  const streets = which === 'streets';
  tabS.setAttribute('aria-selected', streets);
  tabH.setAttribute('aria-selected', !streets);
  streets ? renderStreets() : renderHoods();
  list.scrollTop = 0;
}
tabH.onclick = () => selectTab('hoods');
tabS.onclick = () => selectTab('streets');

selectTab('hoods');
apply();
addEventListener('resize', apply);
</script>
"""

WRAPPER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Manhattan Street-Tree Density</title>
</head>
<body>
{body}
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fragment", type=Path,
                    help="also write the page without the document wrapper")
    args = ap.parse_args()

    scene = build_scene()
    body = (PAGE
            .replace("__SCENE__", json.dumps(scene, separators=(",", ":")))
            .replace("__BANDS__", json.dumps({
                str(k): {**v, "short": short_range(v["range"])}
                for k, v in BANDS.items()}))
            .replace("__AVG__", str(BOROUGH_AVG_TPM))
            .replace("__W__", str(scene["w"]))
            .replace("__H__", str(scene["h"])))

    OUT.write_text(WRAPPER.format(body=body))
    print(f"wrote {OUT} ({len(scene['hoods'])} areas, "
          f"{len(scene['corridors'])} corridors)")
    if args.fragment:
        args.fragment.write_text(body)
        print(f"wrote {args.fragment}")


if __name__ == "__main__":
    main()
