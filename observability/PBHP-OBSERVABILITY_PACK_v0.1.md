# PBHP Observability Pack v0.1

## Purpose

If PBHP scales, people will game it. Observability lets operators detect when PBHP is actually binding vs. when it's become compliance theater.

## Metrics (Computed from Receipts)

### 1. Gate Drift
**What:** Distribution of gates over time. If everything is GREEN, PBHP isn't doing anything.
**Signal:** >90% GREEN over 30 days in a domain that includes irreversible actions.
**Action:** Sample 10 recent GREEN decisions. Re-evaluate with fresh eyes. If any should have been YELLOW+, tighten activation triggers.

### 2. Ritualization
**What:** Repeated boilerplate in Wall/Gap/Door fields. Low variety = copy-paste compliance.
**Signal:** >50% of receipts share identical Wall or Door text (after normalizing whitespace).
**Action:** Flag for manual review. Require context-specific language in receipts for one week. If boilerplate persists, the team may not understand the protocol.

### 3. Asymmetry Load
**What:** How often "who pays first" identifies a low-power party.
**Signal:** Not a problem signal by itself — but if asymmetry is detected frequently AND gates remain GREEN, that's drift.
**Action:** Cross-reference asymmetry detections with gate assignments. Asymmetry + GREEN = review.

### 4. Delay Harm
**What:** Cases where pausing or refusing caused harm (missed deadline, missed opportunity, frustrated user).
**Signal:** Documented cases where PBHP friction produced worse outcomes than proceeding would have.
**Action:** Investigate. If false positives are systematic, adjust activation triggers or False Positive Valve thresholds. Track delay harm rate vs. prevented harm rate.

### 5. Bypass Hints
**What:** Tool calls or irreversible actions occurring without ORANGE+ receipts.
**Signal:** Actions tagged as irreversible in logs but no corresponding Pause Receipt exists.
**Action:** Investigate why the receipt was skipped. Was PBHP not triggered? Was it deliberately bypassed? Was the action misclassified as reversible?

### 6. Confidence Calibration
**What:** Ratio of "Calibrated" vs "Uncalibrated/Overconfident" tags in receipts.
**Signal:** >80% "Calibrated" in a domain with significant uncertainty = possible overconfidence.
**Action:** Sample 10 "Calibrated" receipts. Check if evidence justifies the confidence. If not, retrain on calibration definitions.

## Thresholds and Response

| Metric | Yellow Threshold | Red Threshold | Response |
|--------|-----------------|---------------|----------|
| Gate Drift | >85% GREEN (30d) | >95% GREEN (30d) | Sample + re-evaluate |
| Ritualization | >40% identical | >60% identical | Manual review week |
| Asymmetry + GREEN | >20% of asymmetric cases | >40% | Gate review |
| Delay Harm Rate | >5% of pauses | >15% | Trigger calibration |
| Bypass Hints | Any in ORANGE+ | Repeated pattern | Investigate immediately |
| Confidence Inflation | >75% Calibrated | >90% Calibrated | Evidence audit |

## Implementation

### Minimum Viable Observability
1. Collect receipts in a shared log (file, database, or structured chat log)
2. Run a monthly count of gate distributions
3. Grep for identical Wall/Door/Gap text across receipts
4. Flag any ORANGE+ actions without receipts

### Full Observability
1. Structured receipt storage (JSON) with queryable fields
2. Automated metric computation on receipt ingestion
3. Dashboard with threshold alerts
4. Monthly calibration review (per PBHP-CORE governance section)

## What This Does NOT Do

- Does not measure whether PBHP decisions were "correct" (that requires outcome data)
- Does not replace human judgment about individual cases
- Does not penalize high gate counts (many ORANGE decisions may be appropriate in high-stakes domains)

The goal is to detect **systematic patterns** that suggest PBHP is being gamed, ritualized, or bypassed — not to score individual decisions.

---

PBHP Observability Pack v0.1 | Add-on for PBHP v0.7.1
