"""Street-tree density data for Manhattan: neighborhoods and named corridors.

METRIC
------
Everything here is expressed as **street trees per linear street-mile**, i.e.
both sidewalks of one mile of street counted together. That is the metric that
matches the question "how dense is the tree line along the sidewalk", and it is
the only one that lets a 60-foot Village lane be compared with Park Avenue.

Reference points used to anchor the scale:

  ~99 trees / street-mile   Manhattan borough average on the 2005-06 census.
                            NYC Parks reported Manhattan at 49.4 trees per mile
                            of *sidewalk*, the highest of the five boroughs
                            (Queens 49.1, Staten Island 48.6, Brooklyn 44.6,
                            Bronx 37.4); two sidewalks per street => ~99.
  ~110 trees / street-mile  the same figure carried forward to the 2015-16
                            census, which counted 12.5% more street trees
                            citywide. This is the number the model targets.
  ~350 trees / street-mile  theoretical maximum for a fully stocked block:
                            both sides planted on the 30 ft spacing NYC Parks
                            uses for large-canopy species.
  62k-66k street trees      Manhattan's share of the 666,134 street trees in
                            the 2015-16 TreesCount! census (~10% of the city).

STATUS OF THE NUMBERS
---------------------
`trees_per_mile` values below are **modelled estimates**, not measured counts:
this environment's egress policy blocks data.cityofnewyork.us, so the tree
census could not be queried (see scripts/fetch_tree_census.py, which computes
the measured values wherever the host is reachable). Each estimate comes from
built-form reasoning - street width, block length, curb-cut and loading-dock
density, share of frontage under landmark/historic-district streetscape rules,
park and mall frontage - then rescaled as a set so that the area-weighted
borough mean lands on the published ~110 (build_trees.py prints that check on
every run). Treat them as bands, not decimals: the ordering is the finding,
the digits are a scale. The `confidence` field flags where the reasoning
behind an individual estimate is weakest.

The named corridors in STREETS are a qualitative inventory: those are verified
by streetscape character (historic-district plantings, allees, planted malls),
not by a tree count, and `at` is an approximate anchor point for the block
range named in `extent`, not a surveyed centerline.
"""

# Density bands, keyed by band id used on the map.
BANDS = {
    1: {"label": "Continuous canopy", "range": "145+ trees / street-mile",
        "color": "#14532D"},
    2: {"label": "Dense",             "range": "115-144",
        "color": "#2F7A4F"},
    3: {"label": "Above average",     "range": "90-114",
        "color": "#74B06E"},
    4: {"label": "Average",           "range": "65-89",
        "color": "#B9CE9B"},
    5: {"label": "Sparse",            "range": "under 65",
        "color": "#D9D3C3"},
    0: {"label": "Park / open space", "range": "canopy, but not street trees",
        "color": "#8FAE7E"},
}

BOROUGH_AVG_TPM = 110

# rank is assigned at build time from trees_per_mile (descending).
NEIGHBORHOODS = [
    # ---------- band 1: continuous canopy ----------
    {"name": "West Village", "trees_per_mile": 162, "band": 1, "confidence": "high",
     "centroid": (40.735, -74.005),
     "note": "Manhattan's densest street canopy: 60-ft lanes, low rowhouses, "
             "mature London planes, and a historic district that protects the "
             "streetscape. Charles, Perry, Bank, W 11th and St. Luke's Place "
             "close over the roadway in summer.",
     "source": {"base": "West Village"}},

    {"name": "Hamilton Heights / Sugar Hill", "trees_per_mile": 153, "band": 1,
     "confidence": "high", "centroid": (40.825, -73.948),
     "note": "Convent Avenue and Hamilton Terrace are the most completely "
             "vaulted streets north of 96th; the 1880s-1900s rowhouse blocks "
             "off them were laid out with continuous tree pits.",
     "source": {"clip_from": "Harlem", "bbox": [-73.962, 40.820, -73.945, 40.835]}},

    {"name": "Upper West Side (70s-90s)", "trees_per_mile": 150, "band": 1,
     "confidence": "high", "centroid": (40.787, -73.975),
     "note": "The single largest area of dense canopy in Manhattan. Uniform "
             "brownstone side streets, West End Avenue's double row, the "
             "Broadway malls, and Riverside Park along the whole west edge.",
     "source": {"base": "Upper West Side", "remainder_of": True}},

    {"name": "Greenwich Village / NoHo", "trees_per_mile": 146, "band": 1,
     "confidence": "medium",
     "centroid": (40.731, -73.996),
     "note": "Same low-rise fabric as the West Village with more commercial "
             "frontage; Washington Square North, Waverly Place and the W 10th-"
             "W 12th blocks carry full canopy.",
     "source": {"merge": ["Greenwich Village", "NoHo"]}},

    # ---------- band 2: dense ----------
    {"name": "Morningside Heights", "trees_per_mile": 141, "band": 2,
     "confidence": "medium", "centroid": (40.808, -73.961),
     "note": "Riverside Drive, Claremont Avenue and the Columbia blocks of "
             "W 116th; institutional owners maintain the plantings.",
     "source": {"base": "Morningside Heights", "remainder_of": True}},

    {"name": "Carnegie Hill", "trees_per_mile": 138, "band": 2, "confidence": "high",
     "centroid": (40.784, -73.953),
     "note": "E 91st-E 95th between Fifth and Lexington: townhouse blocks with "
             "near-continuous pits, plus Central Park frontage on the west.",
     "source": {"clip_from": "Upper East Side", "bbox": [-73.962, 40.778, -73.953, 40.790]}},

    {"name": "Central Harlem", "trees_per_mile": 134, "band": 2, "confidence": "medium",
     "centroid": (40.808, -73.945),
     "note": "Strivers' Row (W 138th-139th), Astor Row and the Mount Morris "
             "Park historic district are as leafy as anything downtown; the "
             "avenues in between pull the neighborhood average down.",
     "source": {"base": "Harlem", "remainder_of": True}},

    {"name": "Hudson Heights", "trees_per_mile": 132, "band": 2, "confidence": "medium",
     "centroid": (40.852, -73.938),
     "note": "Cabrini Boulevard, Pinehurst and Fort Washington Avenues on the "
             "ridge, with Fort Tryon and Bennett Parks at either end.",
     "source": {"clip_from": "Washington Heights", "bbox": [-73.948, 40.845, -73.930, 40.862]}},

    {"name": "Inwood", "trees_per_mile": 128, "band": 2, "confidence": "medium",
     "centroid": (40.867, -73.921),
     "note": "Seaman and Payson Avenues run against Inwood Hill Park; the "
             "Park Terrace blocks are fully planted.",
     "source": {"base": "Inwood"}},

    {"name": "Upper East Side (60s-80s)", "trees_per_mile": 126, "band": 2,
     "confidence": "high", "centroid": (40.773, -73.960),
     "note": "Side streets between Fifth and Lexington are consistently "
             "planted; the Park Avenue malls add a third row of trees down "
             "the middle. Avenue retail frontage keeps it below the UWS.",
     "source": {"base": "Upper East Side", "remainder_of": True}},

    {"name": "Gramercy / Stuyvesant Square", "trees_per_mile": 124, "band": 2,
     "confidence": "high", "centroid": (40.737, -73.984),
     "note": "Gramercy Park's ring, Irving Place, and E 19th Street - the "
             "'Block Beautiful' - between Irving and Third.",
     "source": {"base": "Gramercy"}},

    {"name": "Stuyvesant Town / Peter Cooper", "trees_per_mile": 117, "band": 2,
     "confidence": "low", "centroid": (40.732, -73.977),
     "note": "Very high canopy, but most of it is interior parkland rather "
             "than sidewalk: the tree line is inside the superblock, not "
             "along a street wall.",
     "source": {"base": "Stuyvesant Town"}},

    {"name": "Tribeca", "trees_per_mile": 116, "band": 2, "confidence": "low",
     "centroid": (40.719, -74.009),
     "note": "Loft blocks were built without tree pits; two decades of "
             "retrofitted plantings on Hudson, Greenwich and Harrison have "
             "brought it up, but the canopy is young and interrupted.",
     "source": {"base": "Tribeca"}},

    # ---------- band 3: above average ----------
    {"name": "East Village", "trees_per_mile": 112, "band": 3, "confidence": "medium",
     "centroid": (40.726, -73.984),
     "note": "E 10th Street and Stuyvesant Street are exceptional; the "
             "avenues and the blocks east of Avenue A are much thinner.",
     "source": {"base": "East Village"}},

    {"name": "Battery Park City", "trees_per_mile": 110, "band": 3, "confidence": "medium",
     "centroid": (40.711, -74.016),
     "note": "Planted as a landscape project, so the trees are continuous - "
             "but along esplanades and internal parks more than street walls.",
     "source": {"base": "Battery Park City"}},

    {"name": "Chelsea", "trees_per_mile": 109, "band": 3, "confidence": "medium",
     "centroid": (40.747, -74.001),
     "note": "The Chelsea historic district (W 20th-W 22nd, Eighth to Tenth) "
             "is densely lined; the wide avenues and former industrial "
             "frontage west of Tenth are not.",
     "source": {"base": "Chelsea", "remainder_of": True}},

    {"name": "Yorkville", "trees_per_mile": 107, "band": 3, "confidence": "medium",
     "centroid": (40.776, -73.948),
     "note": "Steadily planted side streets, but post-war apartment slabs with "
             "curb cuts and service bays break the line more often than in "
             "the 60s-80s blocks to the south.",
     "source": {"clip_from": "Upper East Side", "bbox": [-73.953, 40.770, -73.940, 40.790]}},

    {"name": "Roosevelt Island", "trees_per_mile": 106, "band": 3, "confidence": "low",
     "centroid": (40.762, -73.950),
     "note": "Main Street is planted end to end and the island is ringed by "
             "park; very little of it is conventional sidewalk.",
     "source": {"base": "Roosevelt Island"}},

    {"name": "Murray Hill", "trees_per_mile": 104, "band": 3, "confidence": "medium",
     "centroid": (40.748, -73.978),
     "note": "The brownstone blocks east of Park (E 35th-E 38th) and Sniffen "
             "Court are well planted; Third and Lexington are not.",
     "source": {"base": "Murray Hill"}},

    {"name": "Washington Heights", "trees_per_mile": 102, "band": 3, "confidence": "medium",
     "centroid": (40.840, -73.939),
     "note": "Excluding Hudson Heights. The Jumel Terrace / Sylvan Terrace "
             "pocket and the streets facing Highbridge Park are leafy; the "
             "Broadway and St. Nicholas corridors are hard-surfaced.",
     "source": {"base": "Washington Heights", "remainder_of": True}},

    {"name": "Lincoln Square", "trees_per_mile": 99, "band": 3, "confidence": "medium",
     "centroid": (40.774, -73.984),
     "note": "Broadway and Columbus malls plus tower plazas; the street wall "
             "itself is broken by garages and institutional frontage.",
     "source": {"clip_from": "Upper West Side", "bbox": [-73.996, 40.767, -73.978, 40.776]}},

    {"name": "Manhattanville", "trees_per_mile": 97, "band": 3, "confidence": "low",
     "centroid": (40.819, -73.957),
     "note": "New Columbia campus plantings on the west side; the viaduct and "
             "industrial frontage along 125th carry almost no trees.",
     "source": {"clip_from": "Morningside Heights", "bbox": [-73.965, 40.814, -73.954, 40.819]}},

    {"name": "Kips Bay", "trees_per_mile": 95, "band": 3, "confidence": "medium",
     "centroid": (40.741, -73.978),
     "note": "Hospital superblocks and wide one-way avenues; the residential "
             "cross streets east of Second are the planted ones.",
     "source": {"base": "Kips Bay"}},

    {"name": "East Harlem", "trees_per_mile": 94, "band": 3, "confidence": "medium",
     "centroid": (40.795, -73.938),
     "note": "Tower-in-the-park housing holds a lot of canopy off the street; "
             "sidewalk stocking along the numbered streets is patchy and "
             "younger, and this is a documented heat-island priority area.",
     "source": {"base": "East Harlem"}},

    {"name": "Flatiron / NoMad", "trees_per_mile": 92, "band": 3, "confidence": "medium",
     "centroid": (40.741, -73.989),
     "note": "Loft and office frontage with wide sidewalks; plantings are "
             "recent and concentrated around Madison Square and Broadway.",
     "source": {"base": "Flatiron District"}},

    {"name": "Turtle Bay", "trees_per_mile": 90, "band": 3, "confidence": "medium",
     "centroid": (40.753, -73.968),
     "note": "The E 48th-E 51st townhouse blocks behind the UN are planted; "
             "Second and Third Avenues are not.",
     "source": {"clip_from": "Midtown", "bbox": [-73.975, 40.748, -73.958, 40.757]}},

    # ---------- band 4: average ----------
    {"name": "Sutton Place / Beekman", "trees_per_mile": 88, "band": 4,
     "confidence": "medium", "centroid": (40.756, -73.961),
     "note": "Beekman Place and the Sutton cul-de-sacs are leafy but very "
             "short; First Avenue dominates the linear footage.",
     "source": {"clip_from": "Midtown", "bbox": [-73.965, 40.751, -73.958, 40.762]}},

    {"name": "Marble Hill", "trees_per_mile": 85, "band": 4, "confidence": "low",
     "centroid": (40.876, -73.911),
     "note": "Hillside streets with front yards; small sample and little "
             "consistent street planting.",
     "source": {"base": "Marble Hill"}},

    {"name": "Lower East Side", "trees_per_mile": 83, "band": 4, "confidence": "medium",
     "centroid": (40.717, -73.987),
     "note": "Tenement blocks were built out to the lot line with no pits; "
             "most trees here are retrofits or belong to housing projects.",
     "source": {"base": "Lower East Side"}},

    {"name": "Hell's Kitchen", "trees_per_mile": 82, "band": 4, "confidence": "medium",
     "centroid": (40.764, -73.991),
     "note": "W 45th-W 51st between Eighth and Tenth have real canopy; the "
             "avenues, tunnel approaches and parking frontage do not.",
     "source": {"base": "Hell's Kitchen", "remainder_of": True}},

    {"name": "SoHo", "trees_per_mile": 80, "band": 4, "confidence": "medium",
     "centroid": (40.724, -74.001),
     "note": "Cast-iron loft district: continuous street wall, heavy loading "
             "and vault frontage, very few tree pits by design.",
     "source": {"base": "SoHo"}},

    {"name": "Two Bridges", "trees_per_mile": 76, "band": 4, "confidence": "low",
     "centroid": (40.711, -73.993),
     "note": "Bridge approaches and towers-in-the-park; sidewalk trees are "
             "sporadic.",
     "source": {"base": "Two Bridges"}},

    {"name": "Nolita / Little Italy", "trees_per_mile": 75, "band": 4, "confidence": "medium",
     "centroid": (40.722, -73.995),
     "note": "Narrow streets that would suit trees, but tenement-era frontage "
             "and dense retail leave little room.",
     "source": {"merge": ["Nolita", "Little Italy"]}},

    {"name": "Midtown East", "trees_per_mile": 73, "band": 4, "confidence": "medium",
     "centroid": (40.754, -73.975),
     "note": "The Park Avenue malls are the exception; office frontage on Lex, "
             "Third and the numbered streets is largely treeless.",
     "source": {"clip_from": "Midtown", "bbox": [-73.985, 40.741, -73.958, 40.770],
                "subtract": [[-73.975, 40.748, -73.958, 40.757],
                             [-73.965, 40.751, -73.958, 40.762]]}},

    {"name": "Financial District", "trees_per_mile": 68, "band": 4, "confidence": "low",
     "centroid": (40.708, -74.011),
     "note": "Colonial street plan with no planting strip; the trees are in "
             "plazas and at the Trade Center rather than along sidewalks.",
     "source": {"base": "Financial District"}},

    # ---------- band 5: sparse ----------
    {"name": "Hudson Yards", "trees_per_mile": 61, "band": 5, "confidence": "low",
     "centroid": (40.754, -74.001),
     "note": "Deck construction, rail cuts and superblocks; the greenery is "
             "on podiums and the High Line, not the sidewalk.",
     "source": {"clip_from": "Chelsea", "bbox": [-74.012, 40.748, -73.997, 40.760],
                "and_clip_from": "Hell's Kitchen", "bbox2": [-74.012, 40.752, -73.997, 40.760]}},

    {"name": "Civic Center", "trees_per_mile": 56, "band": 5, "confidence": "low",
     "centroid": (40.713, -74.005),
     "note": "Government superblocks and plazas; almost no residential street "
             "wall to plant against.",
     "source": {"base": "Civic Center"}},

    {"name": "Midtown (core)", "trees_per_mile": 53, "band": 5, "confidence": "medium",
     "centroid": (40.757, -73.988),
     "note": "The least tree-lined large area in Manhattan: continuous office "
             "frontage, loading docks, subway vaults and sidewalk sheds.",
     "source": {"base": "Midtown", "remainder_of": True}},

    {"name": "Chinatown", "trees_per_mile": 49, "band": 5, "confidence": "medium",
     "centroid": (40.715, -73.997),
     "note": "Narrow irregular streets with the heaviest sidewalk vending and "
             "delivery use in the borough; very few surviving pits.",
     "source": {"base": "Chinatown"}},

    {"name": "Theater District", "trees_per_mile": 46, "band": 5, "confidence": "medium",
     "centroid": (40.759, -73.984),
     "note": "Bottom of the ranking. Marquees, bus staging and pedestrian "
             "plazas leave essentially no planted frontage.",
     "source": {"base": "Theater District"}},

    # ---------- band 0: parks, shown for context ----------
    {"name": "Central Park", "trees_per_mile": None, "band": 0, "confidence": "n/a",
     "centroid": (40.782, -73.965),
     "note": "~18,000 trees, but park trees, not street trees. Shown because "
             "the neighborhoods that border it inherit its shade line.",
     "source": {"base": "Central Park"}},
]

# Named corridors. `at` is an approximate anchor for the block range in
# `extent` - close enough to place a marker, not a surveyed centerline.
# stars: 3 = closed canopy over the roadway, 2 = continuous line one or both
# sides, 1 = notable but interrupted.
STREETS = [
    {"name": "Convent Avenue", "extent": "W 141st - W 145th St",
     "area": "Hamilton Heights", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.8237, -73.9483),
     "note": "The most completely vaulted street in Manhattan: mature planes "
             "on both sides of a landmarked rowhouse block, meeting overhead."},

    {"name": "St. Luke's Place (Leroy St)", "extent": "Hudson St - Seventh Ave S",
     "area": "West Village", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.7297, -74.0053),
     "note": "Fifteen 1850s houses facing James J. Walker Park behind a "
             "double row of gingkos and planes; canopy closes completely."},

    {"name": "Hamilton Terrace", "extent": "W 141st - W 144th St",
     "area": "Hamilton Heights", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.8228, -73.9464),
     "note": "One block long, fully stocked on both sides, no curb cuts."},

    {"name": "W 138th & W 139th St (Strivers' Row)",
     "extent": "Adam Clayton Powell Blvd - Frederick Douglass Blvd",
     "area": "Central Harlem", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.8185, -73.9425),
     "note": "The King Model Houses were built with rear service alleys, so "
             "the street frontage is unbroken and continuously planted."},

    {"name": "Charles / Perry / Bank Streets", "extent": "Greenwich Ave - West St",
     "area": "West Village", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.7352, -74.0038),
     "note": "Three parallel 60-ft lanes of 3-4 story rowhouses; the tree line "
             "is effectively continuous for a half mile."},

    {"name": "E 19th Street ('Block Beautiful')", "extent": "Irving Pl - Third Ave",
     "area": "Gramercy", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.7365, -73.9860),
     "note": "Deliberately planted as a unified streetscape in the 1910s and "
             "maintained as one ever since."},

    {"name": "West End Avenue", "extent": "W 70th - W 106th St",
     "area": "Upper West Side", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.7900, -73.9770),
     "note": "The longest continuously tree-lined avenue in Manhattan: pure "
             "residential frontage, no retail curb cuts, ~1.8 miles."},

    {"name": "Riverside Drive", "extent": "W 72nd - W 120th St",
     "area": "UWS / Morningside", "kind": "park frontage", "stars": 3,
     "at": (40.7960, -73.9720),
     "note": "Planted sidewalk on the east side, Riverside Park's canopy on "
             "the west; the shadiest continuous walk in the borough."},

    {"name": "Cabrini Blvd & Pinehurst Ave", "extent": "W 181st - W 187th St",
     "area": "Hudson Heights", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.8517, -73.9380),
     "note": "Ridge-top streets running between Bennett Park and Fort Tryon; "
             "mature canopy over both."},

    {"name": "W 121st - W 123rd St", "extent": "Mount Morris Park W - Lenox Ave",
     "area": "Central Harlem", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.8055, -73.9450),
     "note": "Mount Morris Park historic district: intact brownstone rows "
             "facing the park, planted end to end."},

    {"name": "Seaman & Payson Avenues", "extent": "Dyckman St - W 218th St",
     "area": "Inwood", "kind": "park frontage", "stars": 3,
     "at": (40.8680, -73.9250),
     "note": "Street trees on one side, Inwood Hill Park's forest on the "
             "other - the only place in Manhattan with old-growth alongside."},

    {"name": "W 88th & W 89th St", "extent": "West End Ave - Riverside Dr",
     "area": "Upper West Side", "kind": "sidewalk canopy", "stars": 3,
     "at": (40.7900, -73.9785),
     "note": "Representative of the whole 70s-90s side-street grid, which is "
             "the largest contiguous dense-canopy area in Manhattan."},

    {"name": "E 92nd & E 93rd St", "extent": "Fifth Ave - Lexington Ave",
     "area": "Carnegie Hill", "kind": "sidewalk canopy", "stars": 2,
     "at": (40.7835, -73.9545),
     "note": "Townhouse blocks including the wood-frame houses at 120 and 122 "
             "E 92nd; near-continuous pits."},

    {"name": "Waverly Place & Washington Square North", "extent": "Bank St - Broadway",
     "area": "Greenwich Village", "kind": "sidewalk canopy", "stars": 2,
     "at": (40.7325, -73.9985),
     "note": "The Greek Revival row on Washington Square North sits under one "
             "of the oldest planted lines in the city."},

    {"name": "E 10th Street & Stuyvesant Street", "extent": "Second Ave - Avenue A",
     "area": "East Village", "kind": "sidewalk canopy", "stars": 2,
     "at": (40.7292, -73.9845),
     "note": "St. Mark's Historic District; the E 10th blocks facing Tompkins "
             "Square get park canopy on top of their own."},

    {"name": "Claremont Ave & W 116th St", "extent": "W 116th - LaSalle St",
     "area": "Morningside Heights", "kind": "sidewalk canopy", "stars": 2,
     "at": (40.8105, -73.9640),
     "note": "Columbia's institutional blocks, planted and maintained as a "
             "single landscape."},

    {"name": "W 20th - W 22nd St", "extent": "Eighth Ave - Tenth Ave",
     "area": "Chelsea", "kind": "sidewalk canopy", "stars": 2,
     "at": (40.7460, -74.0000),
     "note": "Chelsea historic district, including Cushman Row; the General "
             "Theological Seminary block adds a full interior canopy."},

    {"name": "Jones, Commerce, Barrow & Grove Streets", "extent": "Bleecker St - Hudson St",
     "area": "West Village", "kind": "sidewalk canopy", "stars": 2,
     "at": (40.7310, -74.0035),
     "note": "Short crooked lanes off the grid; small trees but very short "
             "spacing, so the line reads as continuous."},

    {"name": "W 76th & W 78th St", "extent": "Central Park W - Columbus Ave",
     "area": "Upper West Side", "kind": "sidewalk canopy", "stars": 2,
     "at": (40.7795, -73.9760),
     "note": "Landmarked rowhouse blocks running into Central Park's edge."},

    {"name": "Astor Row (W 130th St)", "extent": "Fifth Ave - Lenox Ave",
     "area": "Central Harlem", "kind": "sidewalk canopy", "stars": 2,
     "at": (40.8115, -73.9420),
     "note": "Semi-detached houses set back behind wooden porches and front "
             "gardens - a planted setback that no other Manhattan block has."},

    {"name": "Jumel Terrace & Sylvan Terrace", "extent": "W 160th - W 162nd St",
     "area": "Washington Heights", "kind": "sidewalk canopy", "stars": 2,
     "at": (40.8352, -73.9385),
     "note": "Cobbled mews around the Morris-Jumel Mansion's grounds; canopy "
             "from the mansion lot spills over the whole enclave."},

    {"name": "Park Avenue malls", "extent": "E 46th - E 96th St",
     "area": "Midtown East / UES", "kind": "planted mall", "stars": 2,
     "at": (40.7710, -73.9640),
     "note": "A planted median rather than a sidewalk line - it reads as a "
             "tree-lined street from a distance, but the trees are in the "
             "middle of the roadway, over the rail tunnel."},

    {"name": "Broadway malls", "extent": "W 70th - W 168th St",
     "area": "UWS / Harlem Heights", "kind": "planted mall", "stars": 2,
     "at": (40.7940, -73.9720),
     "note": "Nearly five miles of planted median; same caveat as Park Ave - "
             "median trees, though here the flanking sidewalks are planted too."},

    {"name": "Gramercy Park North & South / Irving Place", "extent": "E 18th - E 21st St",
     "area": "Gramercy", "kind": "park frontage", "stars": 2,
     "at": (40.7375, -73.9860),
     "note": "The private park's own canopy plus a planted ring of frontage."},

    {"name": "Pomander Walk & W 95th St", "extent": "Broadway - West End Ave",
     "area": "Upper West Side", "kind": "sidewalk canopy", "stars": 1,
     "at": (40.7945, -73.9740),
     "note": "A hidden garden mews mid-block; short, but the densest planting "
             "per foot on the Upper West Side."},

    {"name": "Beekman Place", "extent": "E 49th - E 51st St",
     "area": "Midtown East", "kind": "sidewalk canopy", "stars": 1,
     "at": (40.7545, -73.9645),
     "note": "Two quiet blocks over the FDR; fully planted but tiny."},

    {"name": "Tudor City Place", "extent": "E 41st - E 43rd St",
     "area": "Midtown East", "kind": "park frontage", "stars": 1,
     "at": (40.7495, -73.9715),
     "note": "Private gardens either side of the street - the only real canopy "
             "in the Midtown core."},

    {"name": "Sniffen Court & E 36th St", "extent": "Lexington Ave - Third Ave",
     "area": "Murray Hill", "kind": "sidewalk canopy", "stars": 1,
     "at": (40.7470, -73.9780),
     "note": "A ten-house carriage mews behind a planted block front."},
]
