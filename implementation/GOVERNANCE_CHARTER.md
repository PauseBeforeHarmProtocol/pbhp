# PBHP Governance Charter

**Version 1.0 — February 2026**

## Purpose

This charter establishes the governance structure for the Pause Before Harm Protocol (PBHP). It defines how the protocol is versioned, how changes are proposed and reviewed, who has authority to modify the protocol, and how organizational implementations relate to the canonical specification.

## Canonical Authority

- **Author and Maintainer:** Charles Phillip Linstrum (ALMSIVI)
- **Canonical Repository:** https://github.com/PauseBeforeHarmProtocol/pbhp
- **License:** Creative Commons BY-SA 4.0 for documentation, MIT for any code implementations
- **Current Version:** PBHP v0.7 (February 2026)

## Versioning Convention

**Major versions (v1.0, v2.0):** Structural changes to the protocol architecture (new tiers, new gates, fundamental logic changes). Require community review period of 30 days.

**Minor versions (v0.7, v0.8):** Refinements to existing mechanisms, new drift alarms, clarified terminology, added case studies. Reviewed by maintainer + at least one external reviewer.

**Patches (v0.7.1, v0.7.2):** Typos, formatting, clarifications that do not change protocol behavior. Maintainer discretion.

## Change Proposal Process

**Step 1:** Submit a GitHub Issue describing the proposed change, rationale, and which protocol section(s) are affected.

**Step 2:** Community discussion period (minimum 14 days for minor versions, 30 days for major versions).

**Step 3:** Maintainer reviews discussion, may request additional evidence or case studies.

**Step 4:** Maintainer accepts, modifies, or rejects. Decision documented in the Issue with rationale.

**Step 5:** If accepted, change is implemented and version number is updated. Changelog entry is mandatory.

## Organizational Implementations

Organizations adopting PBHP may customize the protocol for their context (adjusted harm thresholds, industry-specific drift alarms, modified tier selection criteria). Customized implementations should:

1. Document all deviations from the canonical specification.
2. Maintain the core gate logic and power-asymmetry escalation rules unchanged.
3. Not claim PBHP compliance if the false positive valve or drift alarm system is removed.
4. Contribute significant improvements back to the canonical specification via the change proposal process.

## Review Cycle

**Annual review:** The canonical specification is reviewed annually for relevance, accuracy, and alignment with current AI safety practices. The review includes:
- Assessment of drift alarm list (add new patterns, retire obsolete ones)
- Evaluation of gate criteria against real-world incidents
- Integration of feedback from organizational implementations

**Incident-triggered review:** If a significant AI safety incident occurs that PBHP should have addressed but didn't, an expedited review is initiated within 30 days.

## Minimum Non-Negotiable Elements

Any implementation calling itself "PBHP-compliant" must preserve these elements without modification:

1. **The power-asymmetry auto-escalation rules:** Power + Irreversible = minimum ORANGE; Power + Irreversible + Severe/Catastrophic = minimum RED.
2. **The Door requirement:** No proceeding without a concrete escape vector.
3. **The false positive release valve:** Any pause can be challenged; four-part response required.
4. **The drift alarm system:** Specific triggers that force protocol re-run.
5. **The logging requirement:** All YELLOW+ decisions must produce a PBHP Log.

Everything else can be adapted. These five elements are the protocol's immune system. Remove any one and it is no longer PBHP.

---

**PBHP v0.7** | Author: Charles Phillip Linstrum (ALMSIVI)
