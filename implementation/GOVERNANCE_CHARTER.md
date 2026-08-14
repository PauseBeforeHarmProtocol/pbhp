# PBHP Governance Charter

**Historical Version 1.0 — February 2026**

**Current status annotation — August 14, 2026**

> This charter is retained for PBHP lineage and maintenance. Project Shadow 1.0 / R1 is locked, and this document does not authorize feature expansion, production deployment, certification, or additions to canonical R1. See [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md) for the controlling current status and exact-hash boundary.

## Purpose

This charter establishes the governance structure for the Pause Before Harm Protocol (PBHP). It defines how the protocol is versioned, how changes are proposed and reviewed, who has authority to modify the protocol, and how organizational implementations relate to the canonical specification.

## Canonical Authority

- **Author and Maintainer:** Charles Phillip Linstrum
- **Canonical PBHP Repository:** https://github.com/PauseBeforeHarmProtocol/PauseBeforeHarmProtocolMain
- **License:** Creative Commons BY-SA 4.0 for documentation, MIT for any code implementations
- **Preserved Repository Snapshot:** April 19, 2026 v0.9.5-named source with 17 post-audit fix categories implemented across 103 source/protocol lines explicitly labeled v0.9.6; untagged and not a clean release identity
- **Latest Formal GitHub Release:** v0.9.0

## Versioning Convention

**Major versions (v1.0, v2.0):** Historically, structural changes to the protocol architecture (new tiers, new gates, fundamental logic changes) required a community review period of 30 days.

**Minor versions:** Historically, refinements to existing mechanisms, new drift alarms, clarified terminology, and added case studies were reviewed by the maintainer plus at least one external reviewer.

**Patches:** Historically, typos, formatting, and clarifications that did not change protocol behavior were handled at maintainer discretion.

## Maintenance and Change-Control Process

The locked project is not accepting feature expansion through this charter. The process below applies to reproducible defects, security concerns, rights issues, documentation corrections, and evidence-preserving maintenance. A substantive change requires an explicitly scoped successor identity and must not silently rewrite preserved or admitted bytes.

**Step 1:** Submit a GitHub Issue describing the proposed change, rationale, and which protocol section(s) are affected.

**Step 2:** Apply the review period appropriate to the proposed successor (historically, at least 14 days for minor versions and 30 days for major versions), unless a narrowly scoped security or rights correction requires faster containment and is documented as such.

**Step 3:** Maintainer reviews discussion, may request additional evidence or case studies.

**Step 4:** Maintainer accepts, modifies, or rejects. Decision documented in the Issue with rationale.

**Step 5:** If accepted, change is implemented under a new exact identity, the version/status surfaces are updated, and a changelog entry is mandatory. Preserved releases remain immutable.

## Organizational Implementations

Organizations adopting PBHP may customize the protocol for their context (adjusted harm thresholds, industry-specific drift alarms, modified tier selection criteria). Customized implementations should:

1. Document all deviations from the canonical specification.
2. Maintain the core gate logic and power-asymmetry escalation rules unchanged.
3. Not claim certification, legal compliance, safety, or efficacy merely because PBHP concepts are present. If the false-positive valve or drift-alarm system is removed, describe the result as a derivative rather than canonical PBHP.
4. Propose significant improvements through the change-control process. A proposal does not enter the locked Project Shadow R1 scope without a separate, explicit successor decision.

## Historical Review Cycle

The following was the original active-development policy. In the current locked state, reviews identify corrections and evidence gaps; they do not silently reopen development.

**Annual review:** The canonical specification is reviewed annually for relevance, accuracy, and alignment with current AI safety practices. The review includes:
- Assessment of drift alarm list (add new patterns, retire obsolete ones)
- Evaluation of gate criteria against real-world incidents
- Integration of feedback from organizational implementations

**Incident-triggered review:** If a significant AI safety incident occurs that PBHP should have addressed but didn't, an expedited review is initiated within 30 days.

## Identity-Defining Elements

The following elements historically defined canonical PBHP. This is identity guidance, not certification criteria or an additional license restriction:

1. **The power-asymmetry auto-escalation rules:** Power + Irreversible = minimum ORANGE; Power + Irreversible + Severe/Catastrophic = minimum RED.
2. **The Door requirement:** No proceeding without a concrete escape vector.
3. **The false positive release valve:** Any pause can be challenged; four-part response required.
4. **The drift alarm system:** Specific triggers that force protocol re-run.
5. **The logging requirement:** All YELLOW+ decisions must produce a PBHP Log.

Everything else can be adapted. These five elements are the protocol's immune system. Remove any one and it is no longer PBHP.

## Historical v0.8.0 Operational Extensions

PBHP v0.8.0 introduced five modules that extended the core protocol without modifying it:

- **Decision Triage Classifier** — automated tier routing based on risk signals
- **Domain Metric Packs** — standardized severity thresholds (hiring, healthcare, finance, content moderation, security)
- **Multi-Agent Coordination** — quorum voting and veto rules for multi-agent deployments
- **Compliance Crosswalks** — mappings to NIST AI RMF, ISO/IEC 42001, ISO/IEC 23894, EU AI Act
- **Drift Rate Measurement** — quantitative drift velocity, acceleration, threshold breach projection

These modules were optional add-ons. They did not change the five identity-defining elements above.

---

**PBHP governance lineage** | Author and Maintainer: Charles Phillip Linstrum | Current status: [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
