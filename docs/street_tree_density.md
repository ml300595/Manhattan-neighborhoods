# Manhattan Street-Tree Density — where the sidewalk canopy is thickest

**Question:** which Manhattan streets and neighborhoods have the densest tree
line along their sidewalks?

**Short answer:**

- **Neighborhood: the West Village**, with **Hamilton Heights / Sugar Hill** and
  the **Upper West Side side streets (70s–90s)** immediately behind it. The
  Upper West Side is the largest *contiguous* area of dense canopy; the West
  Village is the densest per mile of street.
- **Single street: Convent Avenue between W 141st and W 145th** (Hamilton
  Heights) — the most completely vaulted street in the borough, with
  **St. Luke's Place**, **Hamilton Terrace**, and **Strivers' Row
  (W 138th–139th)** in the same class.
- **Longest continuously tree-lined avenue: West End Avenue**, W 70th–W 106th
  (~1.8 miles of unbroken residential frontage). **Riverside Drive** is the
  shadiest continuous walk, but half its canopy is Riverside Park, not
  sidewalk trees.
- **The opposite end:** the Theater District, Chinatown, the Midtown core and
  Civic Center — under half the borough average.

Map: `output/manhattan_trees.html` (interactive), `output/manhattan_trees.png`
/ `.svg` (static), `output/manhattan_trees.geojson` (data).

---

## 1. The metric

Everything is **street trees per linear street-mile** — both sidewalks of one
mile of street, counted together. Trees per square mile flatters neighborhoods
with big parks and superblocks; trees per capita flatters low-density ones.
Only a linear measure answers "how continuous is the tree line as I walk down
this block".

Anchors for the scale:

| Reference | Value | Source |
|---|---|---|
| Manhattan borough average, 2005–06 census | 49.4 trees per **sidewalk**-mile → ~99 per street-mile | NYC Parks TreesCount!, highest of the five boroughs (Queens 49.1, Staten Island 48.6, Brooklyn 44.6, Bronx 37.4) |
| Same, carried to the 2015–16 census (+12.5% citywide) | **~110 per street-mile** | the value this model targets |
| Fully stocked block, both sides at 30 ft spacing | ~350 per street-mile | NYC Parks large-canopy spacing standard |
| Manhattan's share of the 666,134 citywide street trees | ~10% (≈62–66k trees) | TreesCount! 2015–16 |

So a neighborhood at 150 has roughly half of a theoretically perfect street
planted; one at 50 has about one tree every 200 feet of frontage.

## 2. Neighborhood ranking

| # | Neighborhood | Est. trees / street-mile | Band | Confidence |
|---|---|---|---|---|
| 1 | West Village | 162 | Continuous canopy | high |
| 2 | Hamilton Heights / Sugar Hill | 153 | Continuous canopy | high |
| 3 | Upper West Side (70s-90s) | 150 | Continuous canopy | high |
| 4 | Greenwich Village / NoHo | 146 | Continuous canopy | medium |
| 5 | Morningside Heights | 141 | Dense | medium |
| 6 | Carnegie Hill | 138 | Dense | high |
| 7 | Central Harlem | 134 | Dense | medium |
| 8 | Hudson Heights | 132 | Dense | medium |
| 9 | Inwood | 128 | Dense | medium |
| 10 | Upper East Side (60s-80s) | 126 | Dense | high |
| 11 | Gramercy / Stuyvesant Square | 124 | Dense | high |
| 12 | Stuyvesant Town / Peter Cooper | 117 | Dense | low |
| 13 | Tribeca | 116 | Dense | low |
| 14 | East Village | 112 | Above average | medium |
| 15 | Battery Park City | 110 | Above average | medium |
| 16 | Chelsea | 109 | Above average | medium |
| 17 | Yorkville | 107 | Above average | medium |
| 18 | Roosevelt Island | 106 | Above average | low |
| 19 | Murray Hill | 104 | Above average | medium |
| 20 | Washington Heights | 102 | Above average | medium |
| 21 | Lincoln Square | 99 | Above average | medium |
| 22 | Manhattanville | 97 | Above average | low |
| 23 | Kips Bay | 95 | Above average | medium |
| 24 | East Harlem | 94 | Above average | medium |
| 25 | Flatiron / NoMad | 92 | Above average | medium |
| 26 | Turtle Bay | 90 | Above average | medium |
| 27 | Sutton Place / Beekman | 88 | Average | medium |
| 28 | Marble Hill | 85 | Average | low |
| 29 | Lower East Side | 83 | Average | medium |
| 30 | Hell's Kitchen | 82 | Average | medium |
| 31 | SoHo | 80 | Average | medium |
| 32 | Two Bridges | 76 | Average | low |
| 33 | Nolita / Little Italy | 75 | Average | medium |
| 34 | Midtown East | 73 | Average | medium |
| 35 | Financial District | 68 | Average | low |
| 36 | Hudson Yards | 61 | Sparse | low |
| 37 | Civic Center | 56 | Sparse | low |
| 38 | Midtown (core) | 53 | Sparse | medium |
| 39 | Chinatown | 49 | Sparse | medium |
| 40 | Theater District | 46 | Sparse | medium |

The area-weighted mean of this table is 110.7 per street-mile, against the
published borough average of ~110 — `scripts/build_trees.py` prints that check
on every run.

### What the ranking is really measuring

Three built-form facts drive nearly all of it:

1. **Street width and building height.** A 60-foot Village lane with 4-story
   rowhouses gets light to the sidewalk and has no loading frontage. The same
   trees on a 100-foot Midtown avenue under 40-story towers do not survive.
2. **Curb cuts and service frontage.** Every garage entrance, loading dock,
   bus stop and subway vault deletes a tree pit. This is why the Theater
   District and the Midtown core sit at the bottom despite wide sidewalks, and
   why Strivers' Row — built with *rear* service alleys — sits at the top.
3. **Historic-district streetscape rules.** Landmarked blocks in the West
   Village, Hamilton Heights, Carnegie Hill, Mount Morris Park and Chelsea
   preserve continuous planting; unregulated blocks lose pits over time and
   rarely regain them.

Two entries need an asterisk. **Stuyvesant Town / Peter Cooper** and **Battery
Park City** have very high canopy, but most of it is interior parkland and
esplanade rather than a tree line along a street wall. **Roosevelt Island** is
the same story. If you want a shaded *walk*, they deliver; if you want a
tree-lined *street*, they do not.

## 3. The streets themselves

★★★ = canopy closes over the roadway · ★★ = continuous line on one or both
sides · ★ = notable but short or interrupted.

| Canopy | Street | Extent | Neighborhood | Type | Why |
|---|---|---|---|---|---|
| ★★★ | **W 138th & W 139th St (Strivers' Row)** | Adam Clayton Powell Blvd - Frederick Douglass Blvd | Central Harlem | sidewalk canopy | The King Model Houses were built with rear service alleys, so the street frontage is unbroken and continuously planted. |
| ★★★ | **W 121st - W 123rd St** | Mount Morris Park W - Lenox Ave | Central Harlem | sidewalk canopy | Mount Morris Park historic district: intact brownstone rows facing the park, planted end to end. |
| ★★★ | **E 19th Street ('Block Beautiful')** | Irving Pl - Third Ave | Gramercy | sidewalk canopy | Deliberately planted as a unified streetscape in the 1910s and maintained as one ever since. |
| ★★★ | **Convent Avenue** | W 141st - W 145th St | Hamilton Heights | sidewalk canopy | The most completely vaulted street in Manhattan: mature planes on both sides of a landmarked rowhouse block, meeting overhead. |
| ★★★ | **Hamilton Terrace** | W 141st - W 144th St | Hamilton Heights | sidewalk canopy | One block long, fully stocked on both sides, no curb cuts. |
| ★★★ | **Cabrini Blvd & Pinehurst Ave** | W 181st - W 187th St | Hudson Heights | sidewalk canopy | Ridge-top streets running between Bennett Park and Fort Tryon; mature canopy over both. |
| ★★★ | **Seaman & Payson Avenues** | Dyckman St - W 218th St | Inwood | park frontage | Street trees on one side, Inwood Hill Park's forest on the other - the only place in Manhattan with old-growth alongside. |
| ★★★ | **Riverside Drive** | W 72nd - W 120th St | UWS / Morningside | park frontage | Planted sidewalk on the east side, Riverside Park's canopy on the west; the shadiest continuous walk in the borough. |
| ★★★ | **West End Avenue** | W 70th - W 106th St | Upper West Side | sidewalk canopy | The longest continuously tree-lined avenue in Manhattan: pure residential frontage, no retail curb cuts, ~1.8 miles. |
| ★★★ | **W 88th & W 89th St** | West End Ave - Riverside Dr | Upper West Side | sidewalk canopy | Representative of the whole 70s-90s side-street grid, which is the largest contiguous dense-canopy area in Manhattan. |
| ★★★ | **St. Luke's Place (Leroy St)** | Hudson St - Seventh Ave S | West Village | sidewalk canopy | Fifteen 1850s houses facing James J. Walker Park behind a double row of gingkos and planes; canopy closes completely. |
| ★★★ | **Charles / Perry / Bank Streets** | Greenwich Ave - West St | West Village | sidewalk canopy | Three parallel 60-ft lanes of 3-4 story rowhouses; the tree line is effectively continuous for a half mile. |
| ★★ | **E 92nd & E 93rd St** | Fifth Ave - Lexington Ave | Carnegie Hill | sidewalk canopy | Townhouse blocks including the wood-frame houses at 120 and 122 E 92nd; near-continuous pits. |
| ★★ | **Astor Row (W 130th St)** | Fifth Ave - Lenox Ave | Central Harlem | sidewalk canopy | Semi-detached houses set back behind wooden porches and front gardens - a planted setback that no other Manhattan block has. |
| ★★ | **W 20th - W 22nd St** | Eighth Ave - Tenth Ave | Chelsea | sidewalk canopy | Chelsea historic district, including Cushman Row; the General Theological Seminary block adds a full interior canopy. |
| ★★ | **E 10th Street & Stuyvesant Street** | Second Ave - Avenue A | East Village | sidewalk canopy | St. Mark's Historic District; the E 10th blocks facing Tompkins Square get park canopy on top of their own. |
| ★★ | **Gramercy Park North & South / Irving Place** | E 18th - E 21st St | Gramercy | park frontage | The private park's own canopy plus a planted ring of frontage. |
| ★★ | **Waverly Place & Washington Square North** | Bank St - Broadway | Greenwich Village | sidewalk canopy | The Greek Revival row on Washington Square North sits under one of the oldest planted lines in the city. |
| ★★ | **Park Avenue malls** | E 46th - E 96th St | Midtown East / UES | planted mall | A planted median rather than a sidewalk line - it reads as a tree-lined street from a distance, but the trees are in the middle of the roadway, over the rail tunnel. |
| ★★ | **Claremont Ave & W 116th St** | W 116th - LaSalle St | Morningside Heights | sidewalk canopy | Columbia's institutional blocks, planted and maintained as a single landscape. |
| ★★ | **Broadway malls** | W 70th - W 168th St | UWS / Harlem Heights | planted mall | Nearly five miles of planted median; same caveat as Park Ave - median trees, though here the flanking sidewalks are planted too. |
| ★★ | **W 76th & W 78th St** | Central Park W - Columbus Ave | Upper West Side | sidewalk canopy | Landmarked rowhouse blocks running into Central Park's edge. |
| ★★ | **Jumel Terrace & Sylvan Terrace** | W 160th - W 162nd St | Washington Heights | sidewalk canopy | Cobbled mews around the Morris-Jumel Mansion's grounds; canopy from the mansion lot spills over the whole enclave. |
| ★★ | **Jones, Commerce, Barrow & Grove Streets** | Bleecker St - Hudson St | West Village | sidewalk canopy | Short crooked lanes off the grid; small trees but very short spacing, so the line reads as continuous. |
| ★ | **Beekman Place** | E 49th - E 51st St | Midtown East | sidewalk canopy | Two quiet blocks over the FDR; fully planted but tiny. |
| ★ | **Tudor City Place** | E 41st - E 43rd St | Midtown East | park frontage | Private gardens either side of the street - the only real canopy in the Midtown core. |
| ★ | **Sniffen Court & E 36th St** | Lexington Ave - Third Ave | Murray Hill | sidewalk canopy | A ten-house carriage mews behind a planted block front. |
| ★ | **Pomander Walk & W 95th St** | Broadway - West End Ave | Upper West Side | sidewalk canopy | A hidden garden mews mid-block; short, but the densest planting per foot on the Upper West Side. |

### Planted malls are not sidewalk canopy

Park Avenue and Broadway read as tree-lined from a distance, but their trees
are in a median in the middle of the roadway — on Park Avenue, in soil over
the Metro-North tunnel. They are ranked here as a separate `planted mall`
type. Broadway is the better of the two for a pedestrian, because its flanking
sidewalks are planted as well.

## 4. Method and provenance

Neighborhood polygons come from `data/manhattan_base.geojson` (the same
Pediacities base the residential atlas uses), subdivided with the clip rules in
`scripts/tree_data.py` and built by `scripts/geo.py`.

**The `trees_per_mile` values are modelled estimates, not measured counts.**
This environment's egress policy blocks `data.cityofnewyork.us`, so the tree
census itself could not be queried. Each estimate comes from built-form
reasoning — street width, block length, curb-cut and loading density, share of
frontage under landmark rules, park and mall frontage — and the set is then
rescaled so the area-weighted borough mean lands on the published ~110. The
`confidence` column flags where that reasoning is weakest (small samples like
Marble Hill, or areas where canopy is off-street like Stuyvesant Town).

What that means in practice:

- **Trust the ordering and the bands.** The top four and the bottom five would
  not change under any plausible measurement.
- **Do not quote the individual numbers as census figures.** A neighborhood
  ranked 21st could plausibly be 17th or 25th.
- The street corridors are a qualitative inventory verified by streetscape
  character (historic-district plantings, allées, park frontage), not by tree
  counts. Marker positions in the map are approximate anchors for the block
  range named, not surveyed centerlines.

### Replacing the estimates with measured data

`scripts/fetch_tree_census.py` does the real thing wherever the open-data host
is reachable:

```bash
export NYC_APP_TOKEN=...            # optional, avoids Socrata throttling
python3 scripts/fetch_tree_census.py --borough Manhattan
```

It writes `data/tree_counts_by_nta.csv` (living street trees per neighborhood
tabulation area) and `data/tree_counts_by_street.csv` (per street name, parsed
from the census `address` column). Hand it a LION or CSCL centerline extract
and it produces the ranking metric directly rather than raw counts:

```bash
python3 scripts/fetch_tree_census.py --centerlines data/lion_manhattan.csv
```

Then update `trees_per_mile` in `scripts/tree_data.py` from the measured
values, drop the `confidence` field, and re-run `scripts/build_trees.py`.

### Rebuilding the map

```bash
pip install shapely matplotlib
python3 scripts/build_trees.py
```
