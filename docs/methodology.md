# NYC Residential Atlas — Methodology Reference

This document describes the evaluation framework used to tier all neighborhoods
across Manhattan, Brooklyn, and Long Island City / Western Queens.

---

## 1. Purpose

The methodology was designed to answer one question for a specific searcher:

> "For a single male professional who values quiet, beauty, safety, and residential
> feel — where in NYC should he look for a furnished short-term rental?"

The system is reproducible: given the same neighborhood and the same rubric,
two independent evaluators should reach the same tier within ±1 step.

---

## 2. Four Core Dimensions

### 2.1 Safety (S) · Weight: 1.3×

**What it measures:** Street-level personal safety at all hours, based on:
- NYPD CompStat major felony statistics (robbery, assault, burglary) per 10,000 residents
- Precinct-level crime index relative to the five-borough median
- Nighttime pedestrian safety (lighting, street activity after 11pm)
- Community perception and stability of safety trends

**Scoring:**

| Score | Threshold | Examples |
|---|---|---|
| 5.0 | < 50% of citywide felony rate; any solo walk at 2am unremarkable | UES, Brooklyn Heights, LIC Core |
| 4.5 | 50–70% of citywide rate; minor incidents only | UWS, Carroll Gardens, North Astoria |
| 4.0 | 70–90% of citywide rate; aware adult is fine at any hour | Fort Greene, Park Slope |
| 3.5 | ~Citywide average; specific streets require awareness | Morningside Heights, Crown Heights North |
| 3.0 | Above average; block selection matters; avoid certain corridors at night | Clinton Hill, East Village core |
| 2.5 | Elevated; incidents occur on residential blocks; solo night walks not recommended | Washington Heights, Hamilton Heights |
| 2.0 | Significantly elevated; regular occurrence of street crime | East Harlem, outer Bushwick |
| 1.0–1.5 | Fails minimum threshold; excluded from active consideration | East New York |

**Why 1.3× weight:** Safety is the only dimension that cannot be improved through
unit selection. A beautiful apartment on an unsafe block is still on an unsafe block.
The 1.3× premium reflects this irreversibility.

### 2.2 Beauty (B) · Weight: 1.0×

**What it measures:** Aesthetic quality of the street-level environment:
- Architectural character and consistency of the residential fabric
- Historic integrity (landmark districts, prewar buildings)
- Street-level greenery, tree canopy
- Absence of intrusive infrastructure (elevated highways, industrial buildings)

**Scoring:**

| Score | Threshold | Examples |
|---|---|---|
| 5.0 | Intact 19th-century historic district; consistently exceptional streetscape | West Village, Brooklyn Heights, Tribeca |
| 4.5 | Very high architectural quality; minor inconsistencies | Carnegie Hill, Park Slope North, UES |
| 4.0 | Mostly beautiful; some postwar infill; strong overall character | Murray Hill, Fort Greene, LIC Waterfront |
| 3.5 | Attractive in places; mixed with ordinary buildings | Yorkville, Boerum Hill |
| 3.0 | Ordinary to decent; no consistent character | Kips Bay, Sunnyside |
| 2.5 | Mostly ordinary; limited visual interest | Midtown core, Woodside |
| 2.0 | Industrial, utilitarian, or poorly maintained | East Harlem, East New York |

**Note:** Modern luxury towers are capped at 4.0 regardless of amenity quality.
Beauty is about the *street environment*, not the interior of the building.

### 2.3 Quiet (Q) · Weight: 1.2×

**What it measures:** Ambient noise level on residential streets, primarily:
- Nightlife venue density (bars, clubs, live music) within 300 meters
- Operating hours of nearby commercial activity
- Volume of through-traffic on primary streets
- Elevated transit adjacency (6-train, J/M/Z, 7-train elevated sections)
- Seasonal or tourist peak noise events

**Scoring:**

| Score | Threshold | Examples |
|---|---|---|
| 5.0 | Essentially silent residential streets; negligible nightlife within walking distance | Brooklyn Heights, Sutton Pl, Cobble Hill |
| 4.5 | Quiet; minor commercial strip that closes by 11pm; no clubs | Upper Astoria, Sunnyside, Gramercy |
| 4.0 | Generally quiet; one active restaurant row but not a nightlife corridor | Murray Hill, Carroll Gardens, UWS |
| 3.5 | Moderate; a nightlife strip exists but residential blocks are somewhat insulated | Yorkville, NoMad, Fort Greene |
| 3.0 | Noticeable; bar activity on primary streets affects nearby blocks | Chelsea, Flatiron, Prospect Heights |
| 2.5 | Fairly loud; nightlife corridors are multi-block; late-night activity common | SoHo, Meatpacking, North Williamsburg |
| 2.0 | Very loud; active bar corridors until 4am; affects most residential blocks | East Village core, Theater District |
| 1.5 | Extreme noise; clubs, tourist buses, or Times Square adjacency | Times Square, LES weekends |

**Why 1.2× weight:** Noise directly affects sleep quality every single night and
persists regardless of unit floor in most cases. The impact is cumulative and
well-documented in sleep research. A quiet-preferring person who moves to a noisy
street will have daily quality-of-life degradation.

**Exception rule:** A high-floor unit (7+) facing a courtyard or the interior of a
block can functionally upgrade a neighborhood's quiet score by 1.0 point for that
specific unit. This unit-level adjustment is captured in the Block Quality metric
in the unit evaluation framework (§7 of the main document).

### 2.4 Residential Feel (R) · Weight: 1.0×

**What it measures:** The extent to which a neighborhood *functions as a neighborhood*
versus as a commercial, tourist, or office zone:
- Ratio of residential buildings to commercial/hotel/office stock
- Presence of everyday residential services (grocery, pharmacy, laundromat, hardware)
- Absence of tourist infrastructure (branded tour buses, souvenir shops, hotel lobbies)
- Community cohesion indicators (local associations, parks usage, long-term residents)
- Weekday / weekend population consistency (office corridors empty on weekends)

**Scoring:**

| Score | Threshold | Examples |
|---|---|---|
| 5.0 | Purely residential; strong neighborhood identity; no tourist footprint | Cobble Hill, Astoria Ditmars, Sunnyside |
| 4.5 | Predominantly residential; appropriate commercial support | Brooklyn Heights, UES, Carroll Gardens |
| 4.0 | Residential majority; some commercial strip activity | Murray Hill, Park Slope, Boerum Hill |
| 3.5 | Mixed but livable; residents are the primary users | Yorkville, Flatiron residential blocks, Fort Greene |
| 3.0 | Balanced; visible commercial or tourist use | Chelsea, Prospect Heights |
| 2.5 | Commercial-heavy; residents are secondary users; nightlife or tourist flows dominate | SoHo, Meatpacking, DUMBO (weekends) |
| 2.0 | Primarily non-residential in function | FiDi, Midtown East, Theater District |
| 1.0–1.5 | Almost entirely non-residential; nearly no everyday residential services | Civic Center, Hudson Yards |

---

## 3. Composite Score & Tier Assignment

### 3.1 Formula

```
Composite = (S × 1.3 + B × 1.0 + Q × 1.2 + R × 1.0) / 4.5
```

The denominator (4.5) is the sum of the four weights, normalizing the output
back to the 1–5 scale.

### 3.2 Tier Thresholds

| Tier | Label | Composite | Dimension Rule | Notes |
|---|---|---|---|---|
| 1 | Gold Standard | ≥ 4.5 | No dimension < 4.0 | True excellence on all axes |
| 2 | Beautiful & Livable | ≥ 4.0 | At most ONE dimension below 4.0; that dimension must be ≥ 3.5 | High quality with exactly one manageable trade-off |
| 3 | Solid Character | ≥ 3.5 | No dimension < 3.0 | Good neighborhoods with real trade-offs |
| 4 | Mixed Character | ≥ 3.0 | Has ≥ 1 dimension below 3.0 OR ≥ 2 dimensions below 4.0 | Significant trade-offs; block-level care required |
| 5 | Weaker Fit | < 3.0 OR automatic rule triggered | See §3.3 | Not recommended for this searcher |

**Important clarification on Tier 2:** A neighborhood with *two* dimensions below 4.0 does not
qualify for Tier 2 even if composite ≥ 4.0. Examples: DUMBO (Q=3.5, R=3.0) and
Astoria 30th Ave (B=3.5, Q=3.5) both have composite > 4.0 but are rated Tier 3 because
they have two weaknesses. They are noted as "high-composite Tier 3" in the results tables.

### 3.3 Automatic Tier 5 Rules

A neighborhood is automatically placed in Tier 5 if **any** of the following are true,
regardless of composite:
1. Safety score < 3.0 (below acceptable floor)
2. Quiet score < 2.5 (nightlife noise is structurally severe)
3. Residential Feel score < 1.5 (non-residential in function)

These represent conditions that unit-level choices cannot overcome.

### 3.4 Block-Level Exception

A neighborhood may have a **sub-zone exception** if:
- A geographically distinct portion of the neighborhood scores significantly differently
  (≥ 1.0 difference on ≥ 2 dimensions)
- The sub-zone has a clear, navigable boundary (a major avenue, a park, a highway)
- The sub-zone represents a coherent area of at least 4–6 city blocks

Currently the only exception applied is:
- **East Village (north of 10th St / Stuyvesant area):** Rated as effective Tier 3
  within a Tier 5 neighborhood

---

## 4. Data Sources

| Source | Used for |
|---|---|
| NYPD CompStat (precinct and block-level) | Safety scoring |
| NYC Landmarks Preservation Commission maps | Beauty / historic district verification |
| Google Street View (street-level inspection) | Beauty, quiet (nightlife signage), block quality |
| Yelp / Google Maps venue density | Quiet (bar/club count within 300m radius) |
| NYC Open Data neighborhood boundaries | Polygon source for mapping |
| GTFS transit data / MTA website | Commute time estimates |
| NYCHPD HPD Open Data (violations) | Building quality verification |
| NYC DOB Building Information System | Construction date, violations |
| Real estate market data (StreetEasy, Furnished Finder) | Price range benchmarks |

---

## 5. What This Methodology Does NOT Capture

**School quality:** Not relevant for this searcher (no children mentioned).

**Flood risk:** Brooklyn's Red Hook is noted as a flood-zone risk but this is not
a formal scoring dimension. It affects the Red Hook Tier 4 placement via the
Residential/Practical assessment.

**Transit frequency in detail:** Commute times are estimated but transit frequency
variations (e.g., G train gaps, N/W weekend service changes) are noted qualitatively
rather than scored formally.

**Hyper-local temporary events:** Construction projects, temporary closures, or
seasonal events may affect specific blocks. These are not captured in the scoring
but are noted in individual neighborhood profiles where known.

**Building-specific factors:** The methodology covers neighborhoods and blocks.
Individual building quality (doorman, maintenance, management responsiveness)
is covered in the unit evaluation framework in the main document (§7).

---

## 6. Methodology Changelog

| Version | Change |
|---|---|
| v1.0 | Manhattan only; 41 sub-neighborhoods; 4 dimensions; 5 tiers |
| v1.1 | Added 3-zone Midtown split (Turtle Bay, Midtown East, Midtown core) |
| v2.0 | Extended to Brooklyn (18 neighborhoods) and LIC/Queens (8 neighborhoods) |
| v2.0 | Added unit-level evaluation framework (§7 of main doc) |
| v2.0 | Added cross-borough comparison and commute matrix |
| v2.0 | Added East Village northern sub-zone exception |

---

*Methodology version 2.0 · May 2026*
