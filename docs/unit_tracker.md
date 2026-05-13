# NYC Unit Tracker — Evaluated Listings

Applies the §7 Unit-Level Evaluation Framework from `nyc_residential_atlas_complete.md`.

**Formula:**
```
Score = (Neighborhood_Composite × 2.0) + (Block_Quality × 1.5)
      + (Building_Quality × 1.0) + (Unit_Specifics × 1.0)
      + (Price_Value × 0.8) + (Availability_Fit × 0.5) + (Roommate_Fit × 0.7)

Max = 34.5  →  Normalized to 100
```

**Interpretation:** 80–100 Exceptional · 65–79 Strong · 50–64 Acceptable · <50 Weak

**Automatic exclusions (deal-breakers):** female roommate · not available by Jun 4 · rent > $4,100 ·
not furnished · Neighborhood T5 · faces bar/club directly · active DOB structural/fire violations ·
3+ total occupants

---

## Summary Table

| # | Address | Neighborhood | Tier | Adj.Comp | BQ | BuQ | US | PV | AF | RF | Raw | /100 | Deal-Breakers | Verdict |
|---|---------|--------------|------|----------|----|-----|----|----|----|----|-----|------|---------------|---------|
| 1 | 210 N 10th St, Brooklyn (Triplex ~7F+, courtyard, terrace) | Williamsburg North | **T5** | 3.40¹ | 4.0 | 3.5 | +2.0 | 5.0² | 4.0 | 5.0² | 27.8 | **80.6** | ⚠️ #6 T5 · ⚠️ #9 risk³ | EXCLUDED⁴ |

---

## Listing Detail

### #1 — 210 N 10th St, Brooklyn, NY 11211

**Property:** Triplex, 3–4BR, terrace, floor 7+, courtyard/rear-facing  
**Rent:** $3,500–$4,100/mo (exact unknown; scored at midpoint $3,800)  
**Listed:** Available now · Standard furnishing  
**Occupancy:** Not confirmed (solo assumed for scoring; see Flag ③)

#### Score Breakdown

| Component | Value | Weight | Points | Notes |
|-----------|-------|--------|--------|-------|
| Neighborhood Composite | 3.40¹ | ×2.0 | **6.80** | Williamsburg North base 3.11; +1.0 Q noise override (high floor + courtyard) |
| Block Quality (BQ) | 4.0 | ×1.5 | **6.00** | N 10th St: quiet side street, no nightlife on block, McCarren Park 2 blocks N |
| Building Quality (BuQ) | 3.5 | ×1.0 | **3.50** | Newer high-rise construction assumed; no doorman confirmed → default 3.5 ⚑ |
| Unit Specifics (US) | +2.0 | ×1.0 | **2.00** | +1 high floor (7+); +1 courtyard/rear facing |
| Price Value (PV) | 5.0 | ×0.8 | **4.00** | Full triplex at ~$3,800 is exceptional value; per-room if shared would score 2.0 |
| Availability Fit (AF) | 4.0 | ×0.5 | **2.00** | Available now ✓; end date not confirmed (assumed ≥ 30 days) ⚑ |
| Roommate Fit (RF) | 5.0 | ×0.7 | **3.50** | Assumes sole occupancy of full triplex ⚑ |
| **Total** | | | **27.80 / 34.5** | |
| **Normalized** | | | **80.6 / 100** | "Exceptional" band — if deal-breakers waived |

#### Deal-Breaker Flags

| Flag | Rule | Status | Detail |
|------|------|--------|--------|
| ⚠️ | #6 — Neighborhood T5 | **TRIGGERED** | Williamsburg North is auto-T5 (Q=2.0 < 2.5 floor). Structural nightlife noise Thu–Sun. |
| ⚠️ | #9 — 3+ occupants | **RISK** | 3–4BR triplex may imply 3+ occupants. Confirm solo or 2-person occupancy. If 3+: second exclusion triggered. |

#### Pending Clarifications (⚑ = affects score)

| Item | Impact |
|------|--------|
| Exact monthly rent (all-in, including fees) | PV score ± 1 point |
| Occupancy: solo vs. shared (and roommate gender if shared) | RF score; possible Deal-Breaker #9 |
| Building name / construction year | BuQ ± 0.5 |
| Availability end date | AF ± 1 point |
| Doorman / elevator / laundry in-unit | BuQ ± 0.5 |

#### Practical Assessment

Despite the T5 exclusion flag, this unit has meaningful mitigating factors that bring it closer to T4 in practice:

- **High floor + courtyard** triggers the noise override: effective Q rises from 2.0 → 3.0, lifting the working composite from 3.11 to 3.40
- **McCarren Park** (2 blocks north) acts as a physical noise buffer from the southern nightlife district; the blocks north of N 9th St are noticeably quieter than the Bedford Ave corridor
- **Triplex with terrace** is an unusual configuration that trades away some neighbourhood quietude for a private outdoor space — a meaningful quality-of-life asset

The score of 80.6 would rank "Exceptional" if the T5 rule were waived. Whether to waive it is a judgment call: if the searcher is willing to accept louder-than-ideal weekends in exchange for the park proximity, terrace, floor level, and value, this listing competes with T3/T4 options in far less interesting locations.

**If occupancy is confirmed as solo or 1 male roommate (separate bathroom), Deal-Breaker #9 is cleared and only #6 remains.**

---

¹ Adjusted composite: Williamsburg North base composite 3.11 raised by noise override (+1.0 effective Q for high floor + courtyard). Base scores: S=4.0, B=3.5, Q=2.0→3.0 (effective), R=3.0.  
² PV=5.0 and RF=5.0 assume full-triplex solo occupancy at ~$3,800/mo. If shared with 3+ people, PV drops to 2.0 and Deal-Breaker #9 is triggered.  
³ 3–4BR listing flags possible 3+ total occupants; Deal-Breaker #9 triggered if confirmed.  
⁴ Formal status is EXCLUDED pending occupancy confirmation and the searcher's decision on whether to waive the T5 neighborhood rule given the unit-specific mitigations.
