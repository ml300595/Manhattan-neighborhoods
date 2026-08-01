"""Replace the modelled estimates in tree_data.py with measured counts.

Pulls the NYC street tree census (TreesCount! 2015-16, Socrata dataset
uvpi-gqnh) and writes two CSVs:

  data/tree_counts_by_nta.csv     live street trees per neighborhood tabulation
                                  area, with the NTA's share of the borough
  data/tree_counts_by_street.csv  live street trees per street name, derived
                                  from the census `address` column

Optionally, if you hand it a LION or CSCL street-centerline extract with a
length field, it also computes the metric this project actually ranks on -
trees per linear street-mile - instead of just raw counts:

  python3 scripts/fetch_tree_census.py --centerlines data/lion_manhattan.csv

NETWORK
-------
This does not run in the Claude Code web sandbox: the egress policy blocks
data.cityofnewyork.us (CONNECT returns 403). Run it locally, or from any
environment allowed to reach the open-data portal. An app token is optional
but avoids Socrata's anonymous throttle:

  export NYC_APP_TOKEN=...
"""
import argparse
import csv
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

DATASET = "uvpi-gqnh"          # 2015 Street Tree Census - Tree Data
ENDPOINT = f"https://data.cityofnewyork.us/resource/{DATASET}.json"
PAGE = 50_000                  # Socrata's max page size for this endpoint

# Directional prefixes/suffixes and street types get normalised so that
# "E 10 ST", "EAST 10TH STREET" and "E 10th St" collapse to one key.
SUFFIXES = {
    "ST": "St", "STREET": "St", "AVE": "Ave", "AVENUE": "Ave", "PL": "Pl",
    "PLACE": "Pl", "BLVD": "Blvd", "BOULEVARD": "Blvd", "DR": "Dr",
    "DRIVE": "Dr", "TER": "Ter", "TERRACE": "Ter", "PKWY": "Pkwy", "RD": "Rd",
    "LN": "Ln", "CT": "Ct", "SQ": "Sq", "WALK": "Walk", "BRDG": "Bridge",
}
DIRECTIONS = {"E": "E", "EAST": "E", "W": "W", "WEST": "W",
              "N": "N", "NORTH": "N", "S": "S", "SOUTH": "S"}


def fetch(params):
    """One Socrata request -> parsed JSON."""
    url = f"{ENDPOINT}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    token = os.environ.get("NYC_APP_TOKEN")
    if token:
        req.add_header("X-App-Token", token)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except OSError as exc:
        sys.exit(f"could not reach {ENDPOINT}: {exc}\n"
                 "If this is a sandboxed environment, the open-data host is "
                 "probably blocked by egress policy - run it locally instead.")


def counts_by_nta(borough):
    """Live street trees grouped by neighborhood tabulation area."""
    rows = fetch({
        "$select": "nta,nta_name,count(tree_id) as trees",
        "$where": f"boroname='{borough}' AND status='Alive'",
        "$group": "nta,nta_name",
        "$order": "trees DESC",
        "$limit": 5000,
    })
    return [{"nta": r["nta"], "nta_name": r["nta_name"], "trees": int(r["trees"])}
            for r in rows]


def normalize_street(address):
    """'1139 E 10 STREET' -> 'E 10th St'. Returns None if unparseable."""
    if not address:
        return None
    parts = address.strip().upper().split()
    if not parts:
        return None
    if re.fullmatch(r"\d+[A-Z]?(-\d+[A-Z]?)?", parts[0]):  # drop house number
        rest = parts[1:]
        # ...unless dropping it leaves only a street type: in "5 AVENUE" the
        # number is the street name, not a house number.
        if rest and any(t not in SUFFIXES and t not in DIRECTIONS for t in rest):
            parts = rest
    if not parts:
        return None
    out = []
    for i, tok in enumerate(parts):
        if i == 0 and tok in DIRECTIONS:
            out.append(DIRECTIONS[tok])
        elif i == len(parts) - 1 and tok in SUFFIXES:
            out.append(SUFFIXES[tok])
        elif re.fullmatch(r"\d+(ST|ND|RD|TH)?", tok):
            n = int(re.sub(r"\D", "", tok))
            tens, unit = n % 100, n % 10
            ord_ = "th" if 11 <= tens <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(unit, "th")
            out.append(f"{n}{ord_}")
        else:
            out.append(tok.title())
    return " ".join(out) or None


def counts_by_street(borough):
    """Live street trees grouped by normalised street name.

    The census has no street-name column, so this pages through the rows and
    parses `address`. ~65k rows for Manhattan: two requests.
    """
    tally = defaultdict(int)
    offset = 0
    while True:
        rows = fetch({
            "$select": "address",
            "$where": f"boroname='{borough}' AND status='Alive'",
            "$limit": PAGE,
            "$offset": offset,
            "$order": "tree_id",
        })
        if not rows:
            break
        for r in rows:
            name = normalize_street(r.get("address"))
            if name:
                tally[name] += 1
        print(f"  ...{offset + len(rows)} rows", file=sys.stderr)
        if len(rows) < PAGE:
            break
        offset += PAGE
    return sorted(({"street": k, "trees": v} for k, v in tally.items()),
                  key=lambda r: -r["trees"])


def load_centerline_miles(path):
    """street name -> miles of centerline, from a LION/CSCL CSV extract.

    Expects a `street` (or `Street`/`stname`) column and a length column in
    feet (`shape_leng`, `SHAPE_Length`) or miles (`miles`).
    """
    miles = defaultdict(float)
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            low = {k.lower(): v for k, v in row.items()}
            name = normalize_street(low.get("street") or low.get("stname") or "")
            if not name:
                continue
            if low.get("miles"):
                miles[name] += float(low["miles"])
            else:
                feet = low.get("shape_leng") or low.get("shape_length") or 0
                miles[name] += float(feet or 0) / 5280.0
    return miles


def write_csv(rows, path, fields):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--borough", default="Manhattan")
    ap.add_argument("--centerlines", type=Path,
                    help="CSV of street centerlines, for trees per street-mile")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"fetching {args.borough} counts by NTA...", file=sys.stderr)
    ntas = counts_by_nta(args.borough)
    total = sum(r["trees"] for r in ntas) or 1
    for r in ntas:
        r["share_pct"] = round(100 * r["trees"] / total, 2)
    write_csv(ntas, DATA_DIR / "tree_counts_by_nta.csv",
              ["nta", "nta_name", "trees", "share_pct"])

    print(f"fetching {args.borough} counts by street...", file=sys.stderr)
    streets = counts_by_street(args.borough)
    fields = ["street", "trees"]
    if args.centerlines:
        miles = load_centerline_miles(args.centerlines)
        for r in streets:
            m = miles.get(r["street"], 0.0)
            # Under a tenth of a mile the ratio is noise, so leave it blank.
            r["street_miles"] = round(m, 3)
            r["trees_per_mile"] = round(r["trees"] / m, 1) if m >= 0.1 else ""
        streets.sort(key=lambda r: -(r["trees_per_mile"] or 0))
        fields += ["street_miles", "trees_per_mile"]
    write_csv(streets, DATA_DIR / "tree_counts_by_street.csv", fields)

    print(f"\n{args.borough}: {total:,} living street trees")
    print("top 15 streets by count:")
    for r in sorted(streets, key=lambda r: -r["trees"])[:15]:
        print(f"  {r['trees']:>5}  {r['street']}")


if __name__ == "__main__":
    main()
