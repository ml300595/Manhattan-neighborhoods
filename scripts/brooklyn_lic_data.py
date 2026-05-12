"""Tier definitions and per-neighborhood data for Brooklyn & Long Island City.

Applies the identical 4-criterion rubric used in the Manhattan Residential Atlas:
  Safety (S) · Beauty (B) · Quiet (Q) · Residential Feel (R)
Each scored 1–5; tier assigned from weighted composite (see methodology.md).

Polygon source hints follow the same convention as atlas_data.py:
  {"base": "<name>"}                full base polygon from borough GeoJSON
  {"clip_from": "<name>", "bbox": [minlng,minlat,maxlng,maxlat]}
  {"merge": ["<A>", "<B>"]}         union of two base polygons

Scores are included as metadata for documentation and AI-consumption purposes;
only tier is used by the rendering pipeline.
"""

# ── Tier definitions (shared with Manhattan atlas) ────────────────────────────
TIERS = {
    1: {"label": "Gold Standard",       "color": "#1F4E3D"},
    2: {"label": "Beautiful & Livable", "color": "#5A8A5E"},
    3: {"label": "Solid Character",     "color": "#C9A961"},
    4: {"label": "Mixed Character",     "color": "#C97A4A"},
    5: {"label": "Weaker Fit",          "color": "#8B3A3A"},
}

# ── Scoring reference ─────────────────────────────────────────────────────────
# scores: [Safety, Beauty, Quiet, Residential] each 1.0–5.0
# composite = (S*1.3 + B*1.0 + Q*1.2 + R*1.0) / 4.5   (Safety & Quiet weighted)
# Tier 1: composite ≥ 4.5, no dimension < 4.0
# Tier 2: composite ≥ 4.0, at most ONE dimension below 4.0, that dimension must be ≥ 3.5
# Tier 3: composite ≥ 3.5, no dimension < 3.0
# Tier 4: composite ≥ 3.0 or one structural weakness
# Tier 5: composite < 3.0 or fails safety / accessibility floor

# ── Brooklyn neighborhoods ────────────────────────────────────────────────────
BROOKLYN = [

    # ──── Tier 1 ─────────────────────────────────────────────────────────────
    {
        "rank": 1, "name": "Brooklyn Heights", "tier": 1,
        "borough": "Brooklyn",
        "centroid": (40.6960, -73.9937),
        "scores": {"safety": 5.0, "beauty": 5.0, "quiet": 5.0, "residential": 5.0},
        "composite": 5.0,
        "one_liner": "Manhattan Tier-1 equivalent; safest in Brooklyn, finest brownstone fabric, silent streets.",
        "commute_midtown_min": 30,
        "commute_fidi_min": 18,
        "price_range_1br": "$3,200–$5,200",
        "transit": ["A/C (High St)", "2/3/4/5/R (Borough Hall-Court St)", "F (York St–DUMBO)", "NYC Ferry"],
        "key_streets": ["Remsen St", "Pierrepont St", "Columbia Heights", "Willow St", "Cranberry/Orange/Pineapple Sts"],
        "why_tier_1": (
            "Lowest reported crime rate of any large Brooklyn neighborhood. "
            "Architectural stock is predominantly 19th-century Italianate and Greek Revival brownstones "
            "in an intact historic district. "
            "Virtually no nightlife venues; BQE noise is below-grade and inaudible on most blocks. "
            "Promenade provides extraordinary waterfront amenity. "
            "Street character is purely residential—no tourist cluster, no office corridor."
        ),
        "watch_outs": "Price premium; furnished supply is limited; some blocks adjacent to BQE hear some highway noise.",
        "source": {"base": "Brooklyn Heights"},
    },

    {
        "rank": 2, "name": "Cobble Hill", "tier": 1,
        "borough": "Brooklyn",
        "centroid": (40.6869, -73.9951),
        "scores": {"safety": 5.0, "beauty": 4.5, "quiet": 5.0, "residential": 4.5},
        "composite": 4.75,
        "one_liner": "Quietest large neighborhood in North Brooklyn; immaculate brownstone blocks.",
        "commute_midtown_min": 38,
        "commute_fidi_min": 22,
        "price_range_1br": "$2,800–$4,200",
        "transit": ["F/G (Bergen St)", "R (Court St)", "B/D/N/Q/R (Atlantic-Barclays)"],
        "key_streets": ["Kane St", "Degraw St", "Tompkins Pl", "Warren St", "Baltic St"],
        "why_tier_1": (
            "Safety and quiet match Brooklyn Heights. "
            "Brownstone blocks between Court and Henry Streets are as architecturally distinguished "
            "as anything outside Manhattan T1. "
            "Almost no nightlife; no tourist attraction. "
            "Very residential—mostly families and professionals."
        ),
        "watch_outs": "Slightly longer Midtown commute than Brooklyn Heights; Court St has some commercial noise.",
        "source": {"base": "Cobble Hill"},
    },

    # ──── Tier 2 ─────────────────────────────────────────────────────────────
    {
        "rank": 3, "name": "Carroll Gardens", "tier": 2,
        "borough": "Brooklyn",
        "centroid": (40.6804, -73.9994),
        "scores": {"safety": 4.5, "beauty": 4.5, "quiet": 4.0, "residential": 4.5},
        "composite": 4.33,
        "one_liner": "Beautiful garden-front brownstones; Smith St nightlife corridor is contained.",
        "commute_midtown_min": 40,
        "commute_fidi_min": 25,
        "price_range_1br": "$2,600–$4,000",
        "transit": ["F/G (Carroll St)", "F/G (Smith-9th Sts)"],
        "key_streets": ["President St", "Carroll St", "First Pl", "Second Pl", "Third Pl"],
        "why_tier_2": (
            "Residential blocks west of Smith St are near-Tier-1 quiet and beautiful. "
            "Italian-American heritage gives strong community character. "
            "Smith St bar scene exists but affects only one corridor; side streets are silent. "
            "Safety excellent throughout."
        ),
        "watch_outs": "Smith St noise if unit is on or very near it; F/G service gaps at night.",
        "source": {"base": "Carroll Gardens"},
    },

    {
        "rank": 4, "name": "Park Slope (North)", "tier": 1,
        "borough": "Brooklyn",
        "centroid": (40.6757, -73.9800),
        "scores": {"safety": 5.0, "beauty": 5.0, "quiet": 4.0, "residential": 5.0},
        "composite": 4.73,
        "one_liner": "Safest large neighborhood in Brooklyn; grand brownstones; Prospect Park at the door.",
        "commute_midtown_min": 35,
        "commute_fidi_min": 28,
        "price_range_1br": "$2,900–$4,800",
        "transit": ["2/3 (Grand Army Plaza)", "B/Q (7th Ave)", "F (4th Ave-9th St)", "R (Union St)"],
        "key_streets": ["Prospect Park West", "8th Ave", "7th Ave (commercial)", "2nd St", "5th St"],
        "why_tier_1": (
            "Consistently one of Brooklyn's lowest-crime precincts—rival to the 19th Precinct (UES). "
            "Grand Victorian and Romanesque Revival brownstones along Prospect Park West rival "
            "anything in the borough. "
            "7th Ave restaurant strip provides amenity without nightlife noise. "
            "Q=4.0 (not lower) reflects that 5th Ave activity is a corridor, not a pervading presence. "
            "No dimension below 4.0; composite 4.73 clearly in Tier 1 range. "
            "Proximity to Prospect Park is a major lifestyle plus."
        ),
        "watch_outs": "5th Ave bar strip on the eastern edge; 7th Ave busy during peak hours.",
        "source": {"clip_from": "Park Slope", "bbox": [-73.992, 40.668, -73.973, 40.684]},
    },

    {
        "rank": 5, "name": "DUMBO", "tier": 3,
        "borough": "Brooklyn",
        "centroid": (40.7034, -73.9888),
        "scores": {"safety": 5.0, "beauty": 5.0, "quiet": 3.5, "residential": 3.0},
        "composite": 4.16,
        "one_liner": "Most spectacular aesthetics in Brooklyn; cobblestones and bridge views; less residential feel.",
        "commute_midtown_min": 28,
        "commute_fidi_min": 15,
        "price_range_1br": "$3,400–$6,000",
        "transit": ["A/C (High St)", "F (York St)", "NYC Ferry (DUMBO/Main St)"],
        "key_streets": ["Water St", "Front St", "Jay St", "Washington St", "Plymouth St"],
        "why_tier_3": (
            "Safety is exceptional—new money residential district. "
            "Beauty is top-tier: iconic Manhattan Bridge framing, cobblestone streets, "
            "converted 19th-century warehouse loft stock. "
            "Rated Tier 3 because TWO dimensions fall below 4.0: Q=3.5 (Brooklyn Bridge Park "
            "weekend tourist flow) and R=3.0 (loft-heavy stock, limited everyday services). "
            "This is the highest-composite Tier 3 in the Brooklyn analysis (4.16); "
            "the trade-offs are real but aesthetic quality is extraordinary."
        ),
        "watch_outs": "Tourist flow on weekends at Brooklyn Bridge Park; loft buildings can be drafty/noisy; very expensive.",
        "source": {"base": "DUMBO"},
    },

    {
        "rank": 6, "name": "Boerum Hill", "tier": 2,
        "borough": "Brooklyn",
        "centroid": (40.6891, -73.9917),
        "scores": {"safety": 4.5, "beauty": 4.0, "quiet": 4.0, "residential": 4.0},
        "composite": 4.11,
        "one_liner": "Quiet, safe, brownstone charm; excellent transit at Atlantic Terminal.",
        "commute_midtown_min": 35,
        "commute_fidi_min": 22,
        "price_range_1br": "$2,500–$3,800",
        "transit": ["A/C/G (Hoyt-Schermerhorn)", "B/D/N/Q/R/2/3/4/5 (Atlantic-Barclays)"],
        "key_streets": ["State St", "Pacific St", "Dean St", "Bergen St", "Bond St"],
        "why_tier_2": (
            "Solid brownstone residential fabric with no major commercial strip creating noise. "
            "Smith St corridor is at the western edge—easy to find quiet blocks. "
            "Atlantic Terminal is one of Brooklyn's best transit hubs: 10 lines within a few blocks. "
            "Strong safety record."
        ),
        "watch_outs": "Atlantic Ave itself is a busy commercial street; blocks immediately adjacent can be noisy.",
        "source": {"base": "Boerum Hill"},
    },

    # ──── Tier 3 ─────────────────────────────────────────────────────────────
    {
        "rank": 7, "name": "Fort Greene", "tier": 3,
        "borough": "Brooklyn",
        "centroid": (40.6896, -73.9739),
        "scores": {"safety": 4.0, "beauty": 4.5, "quiet": 3.5, "residential": 4.0},
        "composite": 3.93,
        "one_liner": "Beautiful brownstones around Fort Greene Park; Myrtle Ave nightlife corridor a partial drawback.",
        "commute_midtown_min": 40,
        "commute_fidi_min": 25,
        "price_range_1br": "$2,400–$3,600",
        "transit": ["C (Lafayette Ave)", "G (Fulton St)", "B/D/N/Q/R/2/3/4/5 (Atlantic-Barclays nearby)"],
        "key_streets": ["DeKalb Ave", "Lafayette Ave", "Willoughby Ave", "Cumberland St", "Fort Greene Pl"],
        "why_tier_3": (
            "Fort Greene Park is a genuine neighborhood asset. "
            "Brownstone architecture is first-rate on the park-adjacent blocks. "
            "Myrtle Ave bar and restaurant strip generates evening noise on that corridor. "
            "Safety is generally good but a few blocks south of Myrtle toward the Navy Yard require "
            "block-by-block judgment. "
            "Scores 3.5 on quiet due to the Myrtle Ave effect."
        ),
        "watch_outs": "Myrtle Ave blocks loud on weekends; some variability south of DeKalb.",
        "source": {"base": "Fort Greene"},
    },

    {
        "rank": 8, "name": "Clinton Hill", "tier": 3,
        "borough": "Brooklyn",
        "centroid": (40.6876, -73.9601),
        "scores": {"safety": 3.5, "beauty": 4.5, "quiet": 3.5, "residential": 4.0},
        "composite": 3.76,
        "one_liner": "Some of Brooklyn's finest Romanesque Revival architecture; safety slightly variable south of Fulton.",
        "commute_midtown_min": 42,
        "commute_fidi_min": 28,
        "price_range_1br": "$2,200–$3,400",
        "transit": ["C (Clinton-Washington Aves)", "G (Classon Ave)"],
        "key_streets": ["Clinton Ave", "Washington Ave", "Waverly Ave", "Grand Ave", "Willoughby Ave"],
        "why_tier_3": (
            "Clinton Ave north of Fulton has extraordinary 19th-century residential architecture—"
            "some blocks are genuinely beautiful. "
            "Pratt Institute brings some campus energy but also anchors the neighborhood culturally. "
            "Safety is solid north of Fulton; south toward Myrtle Ave is more variable. "
            "Quiet is good on residential blocks; Fulton St itself is busy."
        ),
        "watch_outs": "Safety variance south of Fulton; Myrtle Ave noise; C/G trains are infrequent at night.",
        "source": {"base": "Clinton Hill"},
    },

    {
        "rank": 9, "name": "Greenpoint", "tier": 2,
        "borough": "Brooklyn",
        "centroid": (40.7243, -73.9516),
        "scores": {"safety": 4.0, "beauty": 3.5, "quiet": 4.0, "residential": 4.5},
        "composite": 4.00,
        "one_liner": "Quiet, very residential Polish neighborhood; good ferry access; moderate architectural character.",
        "commute_midtown_min": 40,
        "commute_fidi_min": 35,
        "price_range_1br": "$2,200–$3,500",
        "transit": ["G (Greenpoint Ave, Nassau Ave)", "NYC Ferry (Greenpoint Landing)"],
        "key_streets": ["Manhattan Ave", "Franklin St", "Calyer St", "Huron St", "Java St"],
        "why_tier_2": (
            "Greenpoint is one of the most residential-feeling neighborhoods in North Brooklyn—"
            "very low nightlife density, strong Polish-American community. "
            "Safety is good throughout. "
            "Composite 4.00 satisfies the T2 floor; only one dimension below 4.0 (B=3.5). "
            "G train is the only subway—frequent service gaps hurt commute reliability. "
            "Ferry to Midtown East supplements the G train well. "
            "Architecture is attractive low-rise but not the prewar grandeur of the Heights."
        ),
        "watch_outs": "G train unreliability; farthest North Brooklyn neighborhood from Manhattan; industrial waterfront blocks.",
        "source": {"base": "Greenpoint"},
    },

    {
        "rank": 10, "name": "Prospect Heights", "tier": 3,
        "borough": "Brooklyn",
        "centroid": (40.6762, -73.9671),
        "scores": {"safety": 4.0, "beauty": 3.5, "quiet": 3.0, "residential": 3.5},
        "composite": 3.56,
        "one_liner": "Good transit, Brooklyn Museum adjacency; Vanderbilt Ave nightlife brings noise.",
        "commute_midtown_min": 35,
        "commute_fidi_min": 28,
        "price_range_1br": "$2,300–$3,500",
        "transit": ["2/3 (Grand Army Plaza)", "B/Q (Prospect Park, 7th Ave)", "4 (Franklin Ave)"],
        "key_streets": ["Vanderbilt Ave", "Washington Ave", "St Marks Ave", "Prospect Pl", "Park Pl"],
        "why_tier_3": (
            "Vanderbilt Ave has become one of Brooklyn's best restaurant/bar streets—a pro for lifestyle, "
            "a con for quiet. "
            "Safety has improved significantly over the past decade. "
            "Architecture is a mix of brownstones and newer infill. "
            "Brooklyn Museum, Brooklyn Botanic Garden, and Grand Army Plaza are all walkable. "
            "Quietest blocks are on Washington Ave east of Grand Army Plaza."
        ),
        "watch_outs": "Vanderbilt Ave loud on Friday/Saturday nights; some blocks near the 4 train are noisy.",
        "source": {"base": "Prospect Heights"},
    },

    {
        "rank": 11, "name": "South Slope", "tier": 2,
        "borough": "Brooklyn",
        "centroid": (40.6633, -73.9836),
        "scores": {"safety": 4.5, "beauty": 3.5, "quiet": 4.0, "residential": 4.0},
        "composite": 4.03,
        "one_liner": "Quieter, more affordable Park Slope south of 9th St; less architectural grandeur.",
        "commute_midtown_min": 40,
        "commute_fidi_min": 32,
        "price_range_1br": "$2,200–$3,400",
        "transit": ["F/G (Smith-9th Sts)", "F/G/R (4th Ave-9th St)", "D/N/R (36th St)"],
        "key_streets": ["7th Ave", "6th Ave", "5th Ave", "15th St", "20th St"],
        "why_tier_2": (
            "Very safe—part of the 78th precinct, consistently low crime. "
            "Composite 4.03 satisfies T2 floor; only one dimension below 4.0 (B=3.5). "
            "Architecture transitions from grand Park Slope brownstones to smaller, more modest row houses. "
            "7th Ave is quieter in this stretch than the North Slope commercial district. "
            "Good value relative to North Slope."
        ),
        "watch_outs": "5th Ave bar strip; more modest architecture than North Slope.",
        "source": {"base": "South Slope"},
    },

    {
        "rank": 12, "name": "Vinegar Hill", "tier": 3,
        "borough": "Brooklyn",
        "centroid": (40.7011, -73.9822),
        "scores": {"safety": 4.5, "beauty": 4.0, "quiet": 5.0, "residential": 3.0},
        "composite": 4.11,
        "one_liner": "Tiny, extremely quiet historic enclave between DUMBO and the Navy Yard.",
        "commute_midtown_min": 30,
        "commute_fidi_min": 18,
        "price_range_1br": "$2,500–$3,800",
        "transit": ["F (York St)", "A/C (High St)"],
        "key_streets": ["Hudson Ave", "Gold St", "Front St"],
        "why_tier_3": (
            "Among the quietest micro-neighborhoods in all of NYC—tiny footprint, almost no through-traffic. "
            "19th-century Federal and Greek Revival houses are charming. "
            "Very safe. "
            "Ranked T3 rather than T2 only because supply is extremely limited (tiny neighborhood) "
            "and everyday amenities require walking to DUMBO or Farragut."
        ),
        "watch_outs": "Very limited housing supply; minimal neighborhood amenities; isolated feel.",
        "source": {"base": "Vinegar Hill"},
    },

    {
        "rank": 13, "name": "Windsor Terrace", "tier": 2,
        "borough": "Brooklyn",
        "centroid": (40.6531, -73.9795),
        "scores": {"safety": 4.5, "beauty": 3.5, "quiet": 4.5, "residential": 5.0},
        "composite": 4.39,
        "one_liner": "Quietest, most residential neighborhood in the Slope ecosystem; Prospect Park on two sides.",
        "commute_midtown_min": 42,
        "commute_fidi_min": 35,
        "price_range_1br": "$2,200–$3,400",
        "transit": ["F/G (Fort Hamilton Pkwy)", "F/G (15th St-Prospect Park)"],
        "key_streets": ["Prospect Ave", "Greenwood Ave", "Seeley St", "Vanderbilt St"],
        "why_tier_2": (
            "Windsor Terrace is among the safest and quietest neighborhoods in all of Brooklyn. "
            "No nightlife venues; no tourist infrastructure; a genuinely insular residential community "
            "with Irish-American heritage and strong long-term-resident fabric. "
            "Prospect Park forms the eastern and northern boundary—park access is extraordinary. "
            "Composite 4.39 with only B=3.5 below 4.0 (architecture is modest row houses, not grand brownstones). "
            "The commute to Midtown (~42 min via F/G) is the primary trade-off."
        ),
        "watch_outs": "Longer Midtown commute (42 min); modest architectural character; very limited furnished supply.",
        "source": {"base": "Windsor Terrace"},
    },

    {
        "rank": 14, "name": "Ditmas Park (Victorian Flatbush)", "tier": 2,
        "borough": "Brooklyn",
        "centroid": (40.6382, -73.9659),
        "scores": {"safety": 4.0, "beauty": 4.5, "quiet": 4.5, "residential": 4.5},
        "composite": 4.36,
        "one_liner": "NYC's only intact Victorian mansion streetscape; landmarked; extremely quiet; long commute.",
        "commute_midtown_min": 45,
        "commute_fidi_min": 38,
        "price_range_1br": "$2,200–$3,600",
        "transit": ["B/Q (Cortelyou Rd, Ditmas Ave, Beverly Rd)"],
        "key_streets": ["Ditmas Ave", "Westminster Rd", "Marlborough Rd", "Buckingham Rd", "Rugby Rd"],
        "why_tier_2": (
            "The Victorian Flatbush historic districts (Ditmas Park, Prospect Park South, "
            "Matthews-Stratford) contain the only blocks of detached Victorian mansions in Brooklyn—"
            "Shingle Style, Queen Anne, and Colonial Revival houses on leafy 80ft streets. "
            "Architecturally unique in all of NYC; B=4.5 is conservative. "
            "Very safe (70th Precinct residential core), extremely quiet. "
            "No nightlife; very residential; strong neighborhood identity. "
            "The commute to Midtown (45 min via B/Q) is the primary reason it is overlooked. "
            "Composite 4.36 with no dimension below 4.0 satisfies T2; just misses T1 on composite."
        ),
        "watch_outs": "Longest Brooklyn commute in the analysis (45 min to Midtown); very limited furnished supply; may require car for some errands.",
        "source": {"clip_from": "Flatbush", "bbox": [-73.972, 40.626, -73.950, 40.648]},
    },

    # ──── Tier 4 ─────────────────────────────────────────────────────────────
    {
        "rank": 15, "name": "Williamsburg (North)", "tier": 5,
        "tier_note": "Auto-T5: Q=2.0 < 2.5 triggers automatic Tier 5 regardless of composite.",
        "borough": "Brooklyn",
        "centroid": (40.7149, -73.9557),
        "scores": {"safety": 4.0, "beauty": 3.5, "quiet": 2.0, "residential": 3.0},
        "composite": 3.11,
        "one_liner": "Vibrant, well-served by L train; persistent nightlife noise is the critical weakness.",
        "commute_midtown_min": 25,
        "commute_fidi_min": 30,
        "price_range_1br": "$2,800–$4,500",
        "transit": ["L (Bedford Ave, Lorimer St)"],
        "key_streets": ["Bedford Ave", "N 7th St", "Metropolitan Ave", "Berry St"],
        "why_tier_4": (
            "North Williamsburg is safe, transit-connected (L to Union Square in ~10 min), "
            "and has excellent dining/culture. "
            "The fatal weakness for this searcher's profile is noise: "
            "Bedford Ave and Metropolitan Ave are active bar corridors Thursday–Sunday until 4am. "
            "Scores 2.0 on quiet, which drags the composite below T3 threshold. "
            "Architecture is mixed warehouse/converted building stock—some charm, not classical."
        ),
        "watch_outs": "Friday–Sunday noise is severe on primary corridors; L train disruptions affect reliability.",
        "source": {"clip_from": "Williamsburg", "bbox": [-73.965, 40.710, -73.945, 40.722]},
    },

    {
        "rank": 16, "name": "Red Hook", "tier": 4,
        "borough": "Brooklyn",
        "centroid": (40.6749, -74.0081),
        "scores": {"safety": 4.0, "beauty": 4.0, "quiet": 4.5, "residential": 3.0},
        "composite": 3.87,
        "one_liner": "Beautiful, quiet, very safe; no subway and flood-zone exposure make it logistically challenging.",
        "commute_midtown_min": 55,
        "commute_fidi_min": 35,
        "price_range_1br": "$2,200–$3,500",
        "transit": ["B61/B57 bus", "NYC Ferry (South Brooklyn Ferry)"],
        "key_streets": ["Van Brunt St", "Columbia St", "Pioneer St", "Coffey St"],
        "why_tier_4": (
            "Scores exceptionally on quiet, beauty, and safety. "
            "However: no subway access is a structural challenge for a car-free NYC lifestyle. "
            "FEMA flood zone exposure (as demonstrated in Sandy 2012) is a practical risk. "
            "Ferry to Lower Manhattan is pleasant but limited schedule; bus commutes are slow. "
            "Ranked T4 because the transit isolation would significantly impact daily life."
        ),
        "watch_outs": "No subway; serious flood risk; bus commute to Midtown is 45–60 min; limited daily amenities.",
        "source": {"base": "Red Hook"},
    },

    {
        "rank": 17, "name": "Crown Heights (North)", "tier": 4,
        "borough": "Brooklyn",
        "centroid": (40.6710, -73.9490),
        "scores": {"safety": 3.0, "beauty": 3.5, "quiet": 3.5, "residential": 3.5},
        "composite": 3.36,
        "one_liner": "Improving rapidly; beautiful brownstones on specific blocks; safety still variable.",
        "commute_midtown_min": 42,
        "commute_fidi_min": 32,
        "price_range_1br": "$2,000–$3,000",
        "transit": ["2/3 (Eastern Pkwy-Brooklyn Museum, Nostrand Ave)", "4 (Franklin Ave)"],
        "key_streets": ["Eastern Pkwy", "Franklin Ave", "Nostrand Ave", "Sterling Pl", "Park Pl"],
        "why_tier_4": (
            "North Crown Heights (north of Eastern Pkwy) has seen significant gentrification "
            "and has beautiful brownstone blocks. "
            "Safety has improved but remains uneven—some blocks on the 2/3 corridor are fine, "
            "others to the east are still mixed. "
            "Franklin Ave has a growing bar/restaurant scene. "
            "Block-by-block research is critical before selecting a unit here."
        ),
        "watch_outs": "Safety variance requires block-level verification; Franklin Ave nightlife; south of Eastern Pkwy is weaker.",
        "source": {"base": "Crown Heights"},
    },

    # ──── Tier 5 ─────────────────────────────────────────────────────────────
    {
        "rank": 18, "name": "Williamsburg (South / Southside)", "tier": 5,
        "borough": "Brooklyn",
        "centroid": (40.7081, -73.9563),
        "scores": {"safety": 3.0, "beauty": 2.5, "quiet": 2.0, "residential": 3.0},
        "composite": 2.62,
        "one_liner": "More mixed safety and less character than North Williamsburg, with similar noise.",
        "commute_midtown_min": 28,
        "commute_fidi_min": 30,
        "price_range_1br": "$2,200–$3,400",
        "transit": ["L (Bedford Ave, Lorimer, Graham, Grand, Montrose)"],
        "key_streets": ["Grand St", "Metropolitan Ave", "Maujer St"],
        "why_tier_5": "Combines noise from the L corridor, lower safety scores, and weaker architecture—below threshold on 3 of 4 criteria.",
        "watch_outs": "Nightlife noise, less gentrified pockets, variable safety.",
        "source": {"clip_from": "Williamsburg", "bbox": [-73.965, 40.700, -73.945, 40.712]},
    },

    {
        "rank": 19, "name": "Bushwick", "tier": 5,
        "borough": "Brooklyn",
        "centroid": (40.6944, -73.9213),
        "scores": {"safety": 2.5, "beauty": 2.5, "quiet": 2.0, "residential": 3.0},
        "composite": 2.49,
        "one_liner": "Artsy, cheap; safety uneven and loud on weekends; does not meet minimum thresholds.",
        "commute_midtown_min": 35,
        "commute_fidi_min": 38,
        "price_range_1br": "$1,800–$2,800",
        "transit": ["L (Jefferson, DeKalb, Myrtle-Wyckoff)", "M/J/Z (Myrtle-Wyckoff)"],
        "key_streets": ["Wyckoff Ave", "Wilson Ave", "Knickerbocker Ave"],
        "why_tier_5": "Fails minimum safety and quiet thresholds for this search profile.",
        "watch_outs": "Safety varies significantly block by block; weekend warehouse party noise.",
        "source": {"base": "Bushwick"},
    },

    {
        "rank": 20, "name": "East New York / Cypress Hills", "tier": 5,
        "borough": "Brooklyn",
        "centroid": (40.6676, -73.8797),
        "scores": {"safety": 1.5, "beauty": 2.0, "quiet": 3.0, "residential": 3.5},
        "composite": 2.13,
        "one_liner": "Outside the viable range for this search profile; included for completeness.",
        "commute_midtown_min": 50,
        "commute_fidi_min": 45,
        "price_range_1br": "$1,400–$2,200",
        "transit": ["J/Z/L (multiple stops)"],
        "key_streets": [],
        "why_tier_5": "Safety scores fail the minimum threshold; distance from Manhattan compounds the issue.",
        "watch_outs": "Excluded from active consideration.",
        "source": {"base": "East New York"},
    },
]

# ── Long Island City & Western Queens neighborhoods ───────────────────────────
LIC_QUEENS = [

    # ──── Tier 1 ─────────────────────────────────────────────────────────────
    {
        "rank": 1, "name": "Hunters Point (LIC Core)", "tier": 2,
        "borough": "Queens",
        "centroid": (40.7442, -73.9545),
        "scores": {"safety": 5.0, "beauty": 4.0, "quiet": 4.0, "residential": 4.0},
        "composite": 4.29,
        "tier_note": "BEST COMMUTE: 15 min to Midtown; composite 4.29 places this firmly in T2; no dimension below 4.0.",
        "one_liner": "Best commute in the analysis (15 min to Midtown); modern high-rises, East River views.",
        "commute_midtown_min": 15,
        "commute_fidi_min": 22,
        "price_range_1br": "$2,800–$4,500",
        "transit": ["7 (Vernon Blvd-Jackson Ave)", "LIRR (Hunters Point Ave)", "NYC Ferry (LIC)"],
        "key_streets": ["Vernon Blvd", "Jackson Ave", "47th Ave", "21st St"],
        "why_tier_2": (
            "The fastest non-Manhattan commute in the analysis—7 train in 15 minutes to Midtown. "
            "Safety is excellent (new residential development, minimal street crime). "
            "East River Waterfront Esplanade provides extraordinary views and park space. "
            "Modern high-rise towers are architecturally neutral but livable and well-amenitized. "
            "Composite 4.29 with no dimension below 4.0 places this squarely in Tier 2. "
            "The T2 composite is 0.21 below the T1 threshold (4.50) — a real gap. "
            "Flagged as BEST COMMUTE: for a commute-first searcher this is the strongest option."
        ),
        "watch_outs": (
            "Architecture is modern/generic—no brownstone or prewar character. "
            "Neighborhood still maturing; some blocks feel underdeveloped. "
            "7 train is crowded during peak hours."
        ),
        "source": {"base": "Long Island City", "remainder_of": True},
    },

    {
        "rank": 2, "name": "Astoria (Ditmars-Steinway North)", "tier": 1,
        "borough": "Queens",
        "centroid": (40.7729, -73.9301),
        "scores": {"safety": 5.0, "beauty": 4.0, "quiet": 4.5, "residential": 5.0},
        "composite": 4.60,
        "one_liner": "Queens' most livable neighborhood; Greek heritage, quiet low-rise streets, excellent value.",
        "commute_midtown_min": 28,
        "commute_fidi_min": 38,
        "price_range_1br": "$2,300–$3,800",
        "transit": ["N/W (Ditmars Blvd, Astoria Blvd)"],
        "key_streets": ["31st Ave", "Ditmars Blvd", "34th Ave", "Crescent St", "33rd St"],
        "why_tier_1": (
            "Upper Astoria (north of 30th Ave) is one of NYC's quietest non-Manhattan residential areas. "
            "Very safe—consistently low crime, strong community cohesion. "
            "Low-rise residential streetscape is attractive and consistent without being as grand as brownstones. "
            "Greek heritage means exceptional food within walking distance. "
            "Astoria Park (East River waterfront) provides excellent park access. "
            "Scores 5.0 on residential feel—extremely neighborhood-y, strong local businesses, low tourist footprint. "
            "Price point is the best value in the Tier 1 analysis."
        ),
        "watch_outs": (
            "N/W trains run local in this section—slower than advertised. "
            "Architecture lacks the grandeur of Manhattan/Brooklyn T1. "
            "Limited direct transit to downtown Brooklyn."
        ),
        "source": {"clip_from": "Astoria", "bbox": [-73.940, 40.768, -73.920, 40.780]},
    },

    # ──── Tier 2 ─────────────────────────────────────────────────────────────
    {
        "rank": 3, "name": "Hunters Point South (HPS)", "tier": 2,
        "borough": "Queens",
        "centroid": (40.7390, -73.9575),
        "scores": {"safety": 5.0, "beauty": 3.5, "quiet": 4.5, "residential": 4.0},
        "composite": 4.22,
        "one_liner": "Newer development south of LIC core; very quiet, excellent park waterfront, still maturing.",
        "commute_midtown_min": 18,
        "commute_fidi_min": 25,
        "price_range_1br": "$2,600–$4,000",
        "transit": ["7 (Vernon Blvd-Jackson Ave)", "NYC Ferry (LIC)"],
        "key_streets": ["Center Blvd", "48th Ave", "Newtown Creek"],
        "why_tier_2": (
            "Very safe new-construction residential towers with excellent park frontage on the East River. "
            "Quieter than the LIC core—fewer commercial streets. "
            "Architecture is modern glass towers—lacks historic character but buildings are high-quality. "
            "Neighborhood amenities are still limited (fewer restaurants/shops than core LIC). "
            "Ranked T2 rather than T1 primarily because beauty and neighborhood maturity lag LIC core."
        ),
        "watch_outs": "Neighborhood still developing; limited dining/shopping without walking to core LIC; some wind from open waterfront.",
        "source": {"clip_from": "Long Island City", "bbox": [-73.962, 40.734, -73.950, 40.743]},
    },

    {
        "rank": 4, "name": "Sunnyside", "tier": 2,
        "borough": "Queens",
        "centroid": (40.7432, -73.9241),
        "scores": {"safety": 4.5, "beauty": 3.5, "quiet": 4.5, "residential": 5.0},
        "composite": 4.39,
        "one_liner": "Supremely residential, quiet, and underrated; excellent 7-train commute; modest architecture.",
        "commute_midtown_min": 22,
        "commute_fidi_min": 32,
        "price_range_1br": "$2,200–$3,200",
        "transit": ["7 (46th St, 40th St)", "No. 7 express (peak hours)"],
        "key_streets": ["Skillman Ave", "Barnett Ave", "43rd Ave", "Greenpoint Ave", "Queens Blvd (commercial)"],
        "why_tier_2": (
            "Sunnyside is one of NYC's most genuinely residential neighborhoods—"
            "very low nightlife presence, strong Irish/Hispanic/Asian community character, "
            "Sunnyside Gardens (a 1924 planned residential community) is a designated landmark. "
            "Safety is very good. 7-train commute to Midtown is ~22 minutes—excellent. "
            "Architecture is pleasant but modest—2–6 story brick buildings rather than prewar brownstones. "
            "Ranked T2 because beauty/character lag behind T1 neighborhoods."
        ),
        "watch_outs": "Queens Blvd is a wide, noisy commercial corridor—units facing it should be avoided; architecture lacks distinction.",
        "source": {"base": "Sunnyside"},
    },

    {
        "rank": 5, "name": "Astoria (30th Ave / Main)", "tier": 3,
        "borough": "Queens",
        "centroid": (40.7634, -73.9302),
        "scores": {"safety": 4.5, "beauty": 3.5, "quiet": 3.5, "residential": 4.5},
        "composite": 4.01,
        "one_liner": "Vibrant, very livable; busier commercial energy than upper Astoria but still strong.",
        "commute_midtown_min": 30,
        "commute_fidi_min": 40,
        "price_range_1br": "$2,200–$3,600",
        "transit": ["N/W (30th Ave, Broadway, Queensboro Plaza)", "M60 bus to LaGuardia"],
        "key_streets": ["30th Ave", "Steinway St", "Broadway", "31st St"],
        "why_tier_3": (
            "The main Astoria commercial core is vibrant without the nightclub energy of Williamsburg. "
            "Steinway St and 30th Ave have excellent restaurants and everyday retail. "
            "Safety is very good. Residential blocks one street off the commercial strip are quiet. "
            "Ranked T3 because TWO dimensions are at 3.5 (B and Q), violating the T2 rule "
            "of at most one dimension below 4.0. Composite 4.01 would otherwise qualify for T2."
        ),
        "watch_outs": "Steinway St can be noisy evenings; proximity to construction around Queens Plaza.",
        "source": {"clip_from": "Astoria", "bbox": [-73.940, 40.756, -73.920, 40.770]},
    },

    # ──── Tier 3 ─────────────────────────────────────────────────────────────
    {
        "rank": 6, "name": "Jackson Heights", "tier": 3,
        "borough": "Queens",
        "centroid": (40.7557, -73.8835),
        "scores": {"safety": 3.5, "beauty": 3.5, "quiet": 3.0, "residential": 4.0},
        "composite": 3.47,
        "one_liner": "Extraordinarily diverse; vibrant food scene; longer commute; moderate noise and safety.",
        "commute_midtown_min": 35,
        "commute_fidi_min": 45,
        "price_range_1br": "$2,200–$3,000",
        "transit": ["7/E/F/M/R (Jackson Heights-Roosevelt Ave)"],
        "key_streets": ["Roosevelt Ave", "74th St", "Northern Blvd", "34th Ave"],
        "why_tier_3": (
            "Some of NYC's most exceptional food diversity and cultural richness. "
            "Safety is generally good on residential streets, variable near Roosevelt Ave. "
            "Historic Jackson Heights Gardens District has beautiful 1920s–30s cooperative apartment buildings. "
            "Roosevelt Ave elevated train is extremely noisy—units near it should be excluded. "
            "Ranked T3 because safety and quiet scores land below T2 floor."
        ),
        "watch_outs": "Roosevelt Ave elevated-train noise is severe; safety varies; long commute to FiDi.",
        "source": {"base": "Jackson Heights"},
    },

    {
        "rank": 7, "name": "LIC (Court Square area)", "tier": 3,
        "borough": "Queens",
        "centroid": (40.7473, -73.9456),
        "scores": {"safety": 4.0, "beauty": 3.0, "quiet": 3.5, "residential": 3.0},
        "composite": 3.44,
        "one_liner": "Most urban/dense part of LIC; strong transit hub; transitional blocks mix industrial and residential.",
        "commute_midtown_min": 12,
        "commute_fidi_min": 20,
        "price_range_1br": "$2,500–$4,000",
        "transit": ["7/E/M (Court Sq-23rd St)", "G (Court Sq)", "E/M (Queens Plaza)"],
        "key_streets": ["Jackson Ave", "Thomson Ave", "Queens Blvd", "44th Dr"],
        "why_tier_3": (
            "Exceptional transit—best commute in the entire outer-borough analysis. "
            "However, the blocks around Court Square still have industrial adjacency and construction noise. "
            "Residential feel is lower than Hunters Point to the south. "
            "Architecture is largely modern towers without character. "
            "Ranked T3 for the best-commute seekers who accept less neighborhood warmth."
        ),
        "watch_outs": "Construction activity; industrial-adjacent blocks; commuter-heavy feel rather than neighborhood.",
        "source": {"clip_from": "Long Island City", "bbox": [-73.952, 40.743, -73.939, 40.752]},
    },

    # ──── Tier 4 ─────────────────────────────────────────────────────────────
    {
        "rank": 8, "name": "Woodside", "tier": 4,
        "borough": "Queens",
        "centroid": (40.7454, -73.9053),
        "scores": {"safety": 4.0, "beauty": 2.5, "quiet": 3.5, "residential": 4.0},
        "composite": 3.53,
        "one_liner": "Residential, affordable, safe; architecturally minimal; good 7-train access.",
        "commute_midtown_min": 28,
        "commute_fidi_min": 38,
        "price_range_1br": "$1,700–$2,600",
        "transit": ["7 (61st St-Woodside, 52nd St)", "LIRR (Woodside)"],
        "key_streets": ["Roosevelt Ave", "Queens Blvd", "61st St"],
        "why_tier_4": "Safe and residential but offers no architectural distinction; limited evening/weekend amenity.",
        "watch_outs": "Roosevelt Ave elevated-train noise; limited dining/culture.",
        "source": {"base": "Woodside"},
    },
]

# ── Combined export ────────────────────────────────────────────────────────────
ALL_OUTER_BOROUGH = BROOKLYN + LIC_QUEENS
