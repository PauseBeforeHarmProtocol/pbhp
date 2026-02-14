# PBHP vs. Existing Frameworks

How PBHP compares to existing AI safety and quality management approaches. PBHP is complementary to most of these, not competitive.

## PBHP vs. Quality Management Frameworks

### Key Insight

PBHP's unique position is that it operates at the decision point — before the action is taken. Constitutional AI and RLHF operate during training (before deployment). FMEA operates during design. CAPA operates after failure. ISO 9001 provides the systemic framework. PBHP fills the gap between all of these: the moment when a specific decision is being made by a specific system or person, and the question is "should we proceed?"

This is not a replacement for any of these frameworks. It is the missing layer that none of them provide. PBHP + ISO 9001 + CAPA is the full lifecycle:
- **ISO 9001:** Systemic quality management
- **PBHP:** Decision-point safety
- **CAPA:** Post-failure correction

## PBHP vs. AI Safety & Decision-Making Frameworks

| Feature | PBHP v0.7 | Constitutional AI (Anthropic) | RLHF Guardrails | WHO Surgical Checklist |
|---------|-----------|-------------------------------|-----------------|------------------------|
| Tiered Architecture | Yes (4 tiers) | No (single tier) | No (single tier) | No (single checklist) |
| False Positive Management | Yes (formal valve) | No | No | No |
| Drift Monitoring | Yes (quantitative) | No | Partial (reward hacking) | No |
| Power-Asymmetry Analysis | Yes (deterministic escalation) | Partial (principles mention fairness) | No | No |
| Reversibility Assessment | Yes (Door/Wall/Gap) | No | No | Partial (timeout concept) |
| Audit Trail | Yes (PBHP Log) | Partial (training data) | Partial (reward model) | Yes (completion records) |
| Works Without AI | Yes (HUMAN tier) | No (AI-specific) | No (AI-specific) | Yes (human-first) |
| Empirical Validation | Limited (cross-platform testing) | Yes (published research) | Yes (published research) | Yes (extensive clinical trials) |
| Organizational Adoption | Pilot stage | Anthropic internal | Industry-wide | Global (WHO member states) |

## PBHP vs. Quality & Operational Management

| Feature | PBHP v0.7 | ISO 9001:2015 | FMEA | CAPA |
|---------|-----------|----------------|------|------|
| When it acts | Before the decision | Systemic (ongoing) | During design | After the failure |
| False positive handling | Built-in valve | Not addressed | Not addressed | Not addressed |
| Power-asymmetry focus | Central mechanism | Not explicit | Not explicit | Not explicit |
| Real-time drift detection | Yes (alarm phrases + behaviors) | Audit-based (periodic) | No (point-in-time) | No (reactive) |
| Applicable to AI | Yes (built for it) | Partially (adaptable) | Partially (adaptable) | Yes (adaptable) |

## Complementary Use

**PBHP + ISO 9001:** ISO provides the systemic framework; PBHP provides the decision-point gate. Together they ensure both process quality and decision safety.

**PBHP + Constitutional AI:** Constitutional AI shapes training; PBHP gates deployment and operational decisions. Both are necessary for full safety coverage.

**PBHP + FMEA:** FMEA identifies failure modes during design; PBHP assesses them at decision-time with current information. FMEA is prospective; PBHP is operational.

**PBHP + CAPA:** CAPA responds to failures after they occur; PBHP prevents them before decision-makers commit. Running both together creates a full safety lifecycle.

---

**PBHP v0.7** | Author: Charles Phillip Linstrum (ALMSIVI)
