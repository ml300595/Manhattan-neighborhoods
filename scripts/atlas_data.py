"""Tier definitions and per-neighborhood data from Manhattan Residential Atlas.

Each entry maps a report neighborhood to a polygon source: either a base
Manhattan polygon by name, or a clip rule that carves a region out of one
or more base polygons. Centroids come from the report's coordinate table
and are used as label anchors.
"""

TIERS = {
    1: {"label": "Gold Standard",       "color": "#1F4E3D"},
    2: {"label": "Beautiful & Livable", "color": "#5A8A5E"},
    3: {"label": "Solid Character",     "color": "#C9A961"},
    4: {"label": "Mixed Character",     "color": "#C97A4A"},
    5: {"label": "Weaker Fit",          "color": "#8B3A3A"},
}

# Each neighborhood:
#   rank, name (display), tier, one_liner, centroid (lat, lng)
#   source: dict describing how to derive the polygon
#     - {"base": "<name>"}                       full base polygon
#     - {"base": "<name>", "remainder_of": True} parent minus all carved children
#     - {"clip_from": "<name>", "bbox": [minlng,minlat,maxlng,maxlat]}
#                                                rectangular clip out of parent
#     - {"clip_from": "<name>", "bbox": [...], "and_clip_from": "<name2>", "bbox2": [...]}
#                                                clip from two parents and union
NEIGHBORHOODS = [
    # ---------- Tier 1 ----------
    {"rank": 1, "name": "Upper East Side (60s–70s)", "tier": 1, "centroid": (40.773, -73.960),
     "one_liner": "Manhattan's safest large neighborhood; classic prewar elegance.",
     "source": {"base": "Upper East Side", "remainder_of": True}},

    {"rank": 2, "name": "West Village", "tier": 1, "centroid": (40.735, -74.005),
     "one_liner": "Most beautiful streets in NYC; cobblestones and townhouses.",
     "source": {"base": "West Village", "remainder_of": True}},

    {"rank": 3, "name": "Sutton Place / Beekman", "tier": 1, "centroid": (40.756, -73.961),
     "one_liner": "Hidden village inside Midtown East; eerily quiet, very safe.",
     "source": {"clip_from": "Midtown",
                "bbox": [-73.965, 40.751, -73.958, 40.762]}},

    {"rank": 4, "name": "Upper West Side (70s–80s)", "tier": 1, "centroid": (40.787, -73.975),
     "one_liner": "Grand prewar; Central + Riverside Parks; family residential.",
     "source": {"base": "Upper West Side", "remainder_of": True}},

    {"rank": 5, "name": "Gramercy", "tier": 1, "centroid": (40.737, -73.984),
     "one_liner": "Anchored by private park; deeply residential below 59th.",
     "source": {"base": "Gramercy"}},

    # ---------- Tier 2 ----------
    {"rank": 6, "name": "Tribeca", "tier": 2, "centroid": (40.719, -74.009),
     "one_liner": "Cast-iron architecture; very safe; quiet at night; skews luxury.",
     "source": {"base": "Tribeca"}},

    {"rank": 7, "name": "Greenwich Village / NoHo", "tier": 2, "centroid": (40.731, -73.996),
     "one_liner": "West Village adjacent in charm; some NYU energy.",
     "source": {"merge": ["Greenwich Village", "NoHo"]}},

    {"rank": 8, "name": "Carnegie Hill", "tier": 2, "centroid": (40.784, -73.953),
     "one_liner": "Quieter than core UES; gorgeous brownstones; museum-adjacent.",
     "source": {"clip_from": "Upper East Side",
                "bbox": [-73.962, 40.778, -73.953, 40.790]}},

    {"rank": 9, "name": "Battery Park City", "tier": 2, "centroid": (40.711, -74.016),
     "one_liner": "Modern but waterfront; parks everywhere; residential by design.",
     "source": {"base": "Battery Park City"}},

    {"rank": 10, "name": "Murray Hill", "tier": 2, "centroid": (40.748, -73.978),
     "one_liner": "Genuine residential feel; brownstone blocks east of Park Ave.",
     "source": {"base": "Murray Hill"}},

    {"rank": 11, "name": "Lenox Hill", "tier": 2, "centroid": (40.768, -73.962),
     "one_liner": "UES south slice; safe, classic, slightly busier.",
     "source": {"clip_from": "Upper East Side",
                "bbox": [-73.974, 40.758, -73.953, 40.770]}},

    # ---------- Tier 3 ----------
    {"rank": 12, "name": "Yorkville", "tier": 3, "centroid": (40.776, -73.948),
     "one_liner": "Quiet residential; less architecturally distinguished.",
     "source": {"clip_from": "Upper East Side",
                "bbox": [-73.953, 40.770, -73.940, 40.790]}},

    {"rank": 13, "name": "Flatiron", "tier": 3, "centroid": (40.741, -73.989),
     "one_liner": "Beautiful architecture; more commercial than residential.",
     "source": {"base": "Flatiron District", "remainder_of": True}},

    {"rank": 14, "name": "NoMad", "tier": 3, "centroid": (40.745, -73.987),
     "one_liner": "Newer luxury towers north of Flatiron; more residential feel.",
     "source": {"clip_from": "Flatiron District",
                "bbox": [-73.995, 40.742, -73.983, 40.747]}},

    {"rank": 15, "name": "Roosevelt Island", "tier": 3, "centroid": (40.762, -73.950),
     "one_liner": "Quiet and safe; architecturally bland; isolating.",
     "source": {"base": "Roosevelt Island"}},

    {"rank": 16, "name": "Lincoln Square", "tier": 3, "centroid": (40.774, -73.984),
     "one_liner": "Safe, beautiful; more cultural/commercial than residential.",
     "source": {"clip_from": "Upper West Side",
                "bbox": [-73.996, 40.767, -73.978, 40.776]}},

    {"rank": 17, "name": "Chelsea", "tier": 3, "centroid": (40.747, -74.001),
     "one_liner": "Pretty blocks; safe; busier and less classically residential.",
     "source": {"base": "Chelsea", "remainder_of": True}},

    {"rank": 18, "name": "Kips Bay", "tier": 3, "centroid": (40.741, -73.978),
     "one_liner": "Practical, safe; less character than Murray Hill.",
     "source": {"base": "Kips Bay"}},

    {"rank": 19, "name": "Stuyvesant Town / Peter Cooper", "tier": 3, "centroid": (40.732, -73.977),
     "one_liner": "Park-like superblock; very safe; residential but uniform.",
     "source": {"base": "Stuyvesant Town"}},

    {"rank": 20, "name": "Meatpacking District", "tier": 3, "centroid": (40.740, -74.008),
     "one_liner": "Beautiful cobblestone; nightlife-driven; weak on quiet.",
     "source": {"clip_from": "West Village",
                "bbox": [-74.012, 40.7390, -74.0030, 40.7430]}},

    # ---------- Tier 4 ----------
    {"rank": 21, "name": "SoHo", "tier": 4, "centroid": (40.724, -74.001),
     "one_liner": "Beautiful but tourist-saturated; weak on quiet.",
     "source": {"base": "SoHo", "remainder_of": True}},

    {"rank": 22, "name": "Hell's Kitchen", "tier": 4, "centroid": (40.764, -73.991),
     "one_liner": "Improving, charming pockets; uneven on quiet/beauty.",
     "source": {"base": "Hell's Kitchen", "remainder_of": True}},

    {"rank": 23, "name": "Morningside Heights", "tier": 4, "centroid": (40.808, -73.961),
     "one_liner": "Columbia-anchored, leafy, generally safe.",
     "source": {"base": "Morningside Heights", "remainder_of": True}},

    {"rank": 24, "name": "Financial District", "tier": 4, "centroid": (40.708, -74.011),
     "one_liner": "Safe, striking architecture; dead on weekends.",
     "source": {"base": "Financial District"}},

    {"rank": 25, "name": "East Village", "tier": 4, "centroid": (40.726, -73.984),
     "one_liner": "Charming but loud; uneven safety.",
     "source": {"base": "East Village"}},

    {"rank": 26, "name": "Lower East Side", "tier": 4, "centroid": (40.717, -73.987),
     "one_liner": "Vibrant, noisy, uneven block-by-block.",
     "source": {"base": "Lower East Side"}},

    {"rank": 27, "name": "Midtown (core)", "tier": 4, "centroid": (40.755, -73.984),
     "one_liner": "Office-heavy; not residential in feel.",
     "source": {"base": "Midtown", "remainder_of": True}},

    {"rank": 28, "name": "Theater District", "tier": 4, "centroid": (40.759, -73.984),
     "one_liner": "Tourist energy; transit hub; weak on residential.",
     "source": {"base": "Theater District"}},

    {"rank": 29, "name": "Hudson Square", "tier": 4, "centroid": (40.726, -74.008),
     "one_liner": "Transitional; mostly commercial.",
     "source": {"clip_from": "SoHo",
                "bbox": [-74.016, 40.718, -74.0040, 40.730]}},

    {"rank": 30, "name": "Nolita", "tier": 4, "centroid": (40.722, -73.995),
     "one_liner": "Charming but tiny and busy.",
     "source": {"merge": ["Nolita", "Little Italy"]}},

    {"rank": 31, "name": "Civic Center", "tier": 4, "centroid": (40.713, -74.005),
     "one_liner": "Government buildings; not residential.",
     "source": {"base": "Civic Center"}},

    # ---------- Tier 5 ----------
    {"rank": 32, "name": "Hudson Yards", "tier": 5, "centroid": (40.754, -74.001),
     "one_liner": "Modern, sterile; not residential in any traditional sense.",
     "source": {"clip_from": "Chelsea",
                "bbox": [-74.012, 40.748, -73.997, 40.760],
                "and_clip_from": "Hell's Kitchen",
                "bbox2": [-74.012, 40.752, -73.997, 40.760]}},

    {"rank": 33, "name": "Inwood", "tier": 5, "centroid": (40.867, -73.921),
     "one_liner": "Quiet; has Fort Tryon Park; isolated, architecturally modest.",
     "source": {"base": "Inwood"}},

    {"rank": 34, "name": "Washington Heights", "tier": 5, "centroid": (40.840, -73.939),
     "one_liner": "Some beautiful blocks (Hudson Heights); uneven safety.",
     "source": {"base": "Washington Heights"}},

    {"rank": 35, "name": "Hamilton Heights", "tier": 5, "centroid": (40.825, -73.948),
     "one_liner": "Beautiful brownstones, improving; safety still variable.",
     "source": {"clip_from": "Harlem",
                "bbox": [-73.962, 40.820, -73.945, 40.835]}},

    {"rank": 36, "name": "Manhattanville", "tier": 5, "centroid": (40.819, -73.957),
     "one_liner": "Industrial-residential mix, still transitional.",
     "source": {"clip_from": "Morningside Heights",
                "bbox": [-73.965, 40.814, -73.954, 40.819]}},

    {"rank": 37, "name": "Central Harlem", "tier": 5, "centroid": (40.808, -73.945),
     "one_liner": "Cultural depth, gorgeous brownstones; safety varies.",
     "source": {"base": "Harlem", "remainder_of": True}},

    {"rank": 38, "name": "East Harlem", "tier": 5, "centroid": (40.795, -73.938),
     "one_liner": "Improving but the weakest on safety among Manhattan options.",
     "source": {"base": "East Harlem"}},

    {"rank": 39, "name": "Chinatown", "tier": 5, "centroid": (40.715, -73.997),
     "one_liner": "Vibrant but neither quiet nor classically residential.",
     "source": {"base": "Chinatown"}},

    {"rank": 40, "name": "Two Bridges", "tier": 5, "centroid": (40.711, -73.993),
     "one_liner": "Mixed, transitional, limited residential character.",
     "source": {"base": "Two Bridges"}},

    {"rank": 41, "name": "Marble Hill", "tier": 5, "centroid": (40.876, -73.911),
     "one_liner": "Technically Manhattan but isolated on the Bronx mainland.",
     "source": {"base": "Marble Hill"}},
]
