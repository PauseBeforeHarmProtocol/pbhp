# Pause-Before-Harm Protocol (PBHP) v0.7

A comprehensive decision-making framework for humans and AI systems to evaluate actions that could cause harm, with emphasis on protecting vulnerable groups and maintaining ethical accountability.

## Overview

PBHP is a **harm-reduction protocol, not a moral absolution engine**. It provides a structured, repeatable process for evaluating decisions that could significantly affect real people. The protocol assumes that care and truth belong together: protection must not erase truth, and truth-telling must not trample care.

### Core Question

> *"If I'm wrong, who pays first -- and can they recover?"*

### Core Principles

- **The pause itself is sacred**: If you cannot hesitate before causing harm, you cannot genuinely care about the people affected
- **Protect vulnerable groups**: When in doubt, lean toward protecting low-power groups from high, hard-to-undo harms
- **Keep the game board open**: Minimize irreversible lock-ins, especially those that trap or erase low-power groups
- **Human sovereignty**: This protocol introduces friction, not authority. Responsibility remains with the decision-maker

## Installation

```bash
# Clone or download the repository
cd pbhp

# No external dependencies required - uses Python 3.7+ standard library only
python pbhp_cli.py
```

## Quick Start

### Interactive CLI

```bash
python pbhp_cli.py
```

Full guided walkthrough of every PBHP step including ethical pause, Door/Wall/Gap, CHIM check, harm identification, consent analysis, red team review, uncertainty assessment, and structured logging.

### Programmatic Usage

```python
from pbhp_core import (
    PBHPEngine, ImpactLevel, LikelihoodLevel,
    DecisionOutcome, Mode, EpistemicFence, UncertaintyAssessment,
    ConsequencesChecklist, Confidence
)

engine = PBHPEngine()

# Step 1: Name the action
log = engine.create_assessment(
    action_description="Send termination email to Employee X",
    agent_type="human_manager"
)

# Step 0a: Ethical pause (triune minds)
engine.perform_ethical_pause(
    log,
    action_statement="Terminating employment of a person",
    compassion_notes="This will cause real distress and financial harm",
    logic_notes="Performance issues are documented over 6 months",
    paradox_notes="Accountability is needed AND this person has a family",
)

# Step 0e: Door/Wall/Gap
engine.perform_door_wall_gap(
    log,
    wall="Company policy requires written warning",
    gap="Could be misinterpreted; employee may not have context",
    door="Have 1:1 conversation first, then send written recap"
)

# Step 0f: CHIM check
engine.perform_chim_check(
    log,
    constraint_recognized=True,
    no_choice_claim=False,
    remaining_choice="Can choose timing, wording, support offered"
)

# Step 2: Add harms
engine.add_harm(
    log,
    description="Psychological distress for employee",
    impact=ImpactLevel.MODERATE,
    likelihood=LikelihoodLevel.LIKELY,
    irreversible=False,
    power_asymmetry=True,
    affected_parties=["Employee X"],
    least_powerful_affected="Employee X"
)

# Step 4: Consent check
engine.perform_consent_check(
    log,
    explicit_consent=False,
    informed_hypothetical_consent=True,
    compatible_with_dignity=True,
    notes="Employee agreed to performance review process in contract"
)

# Step 5: Safer alternatives
engine.add_alternative(
    log,
    description="Have 1:1 conversation first",
    preserves_goal=True,
    reduces_harm=True,
    reversible=True
)

# Step 6: Finalize
engine.finalize_decision(
    log,
    outcome=DecisionOutcome.PROCEED_MODIFIED,
    justification="Will proceed with prior 1:1 discussion and supportive language"
)

# Generate standardized response
print(engine.generate_response(log))

# Export logs
engine.export_logs("pbhp_logs.json")
```

### Quick Risk Check

```python
from pbhp_core import quick_harm_check

risk = quick_harm_check(
    impact="severe",
    likelihood="likely",
    irreversible=True,
    power_asymmetry=True
)
print(f"Risk Class: {risk.value}")  # Output: red
```

## Risk Classification

PBHP uses five risk classes with deterministic rules:

| Risk Class | Description | Requirements |
|------------|-------------|--------------|
| **GREEN** | Low risk, reversible | Proceed normally |
| **YELLOW** | Moderate harm possible | Proceed with caution + named mitigation |
| **ORANGE** | Severe harm possible OR power+irreversible | Constraints + alternatives + Red Team review |
| **RED** | Severe+irreversible+likely OR catastrophic | Default to delay/refuse |
| **BLACK** | Catastrophic+irreversible+imminent | Must refuse |

### Key Escalation Rules

- Power asymmetry + Irreversible = **minimum ORANGE**
- Severe + Irreversible + (Likely or Imminent) = **RED**
- Catastrophic + Irreversible + (Likely or Imminent) = **BLACK**
- Audience risk (minors, vulnerable, public) elevates by one step

## Complete Protocol Steps

### Foundation Gates (Non-Optional)

| Step | Module | Purpose |
|------|--------|---------|
| 0a | Ethical Pause | Balance compassion/logic/paradox; detect high arousal |
| 0d | Quick Risk Check | Pre-screen: obviously low risk? |
| 0e | Door/Wall/Gap | Identify constraints and escape vectors |
| 0f | CHIM Check | Prevent surrender to perceived inevitability |
| 0g | Absolute Rejection | Refuse fascism/genocide/slavery/dehumanization |

### Seven Steps

| Step | Name | Description |
|------|------|-------------|
| 1 | Name the Action | Clear sentence: "I am going to [verb] [object] for [who]" |
| 2 | Identify Harms | List plausible harms, least-powerful first |
| 3 | Rate Impact | Impact/Likelihood/Irreversibility/Power -> Risk Class |
| 4 | Consent Check | Would affected parties reasonably agree? |
| 5 | Alternatives | At least one safer option (required ORANGE+) |
| 6 | Decide & Justify | Gate-appropriate decision with honest justification |
| 6.5 | Red Team | Adversarial stress test (required ORANGE+) |
| 7 | Log | Structured audit trail with epistemic fence |

### Supporting Modules

| Module | Purpose |
|--------|---------|
| Consequences Checklist | 22-question temporal/cultural impact model |
| Epistemic Fence | Separate facts/inferences/unknowns; competing frames |
| IAM (Inference & Attribution) | 4-level attribution ladder with evidence requirements |
| Uncertainty Assessment | Scenarios, action vs inaction, confidence tracking |
| Drift Alarm Detector | Catch rationalization phrases and compliance theater |
| Tone Validator | Enforce brutal clarity without contempt |
| Lexicographic Priority | Resolve "small harm to many vs large harm to few" |
| False Positive Review | Challenge pauses with auditable justification |

## Key Modules Detail

### Drift Alarm Detector

```python
from pbhp_core import detect_drift_alarms

text = "We have to do this, it's temporary and for the greater good"
alarms = detect_drift_alarms(text)
# Returns: ['drift:we have to', 'drift:it's temporary', 'drift:for the greater good']
```

Detects four categories:
- **Drift phrases**: "it's temporary", "there's no choice", "just following procedure"
- **Premature collapse**: "it's obvious", "everyone knows", "close enough"
- **Compassion drift**: dehumanization, coercive "care", moral license
- **Sycophancy**: ego inflation, "chosen one" language

### Tone Validator (Brutal Clarity, Zero Contempt)

```python
from pbhp_core import ToneValidator

# Good: plain language about harm
result = ToneValidator.validate("This policy increases deaths for vulnerable groups")
# No issues

# Bad: contempt
result = ToneValidator.validate("Only an idiot would support this")
# Contempt detected

# Bad: euphemism
result = ToneValidator.validate("May pose challenges for some stakeholders")
# Euphemism detected - use plain language about harm
```

### Epistemic Fence

```python
from pbhp_core import EpistemicFence, Mode, AttributionLevel

fence = EpistemicFence(
    mode=Mode.EXPLORE,
    facts=["Policy removes coverage for X million people"],
    inferences=[("Will increase mortality", "high")],
    unknowns=["Exact number affected depends on state implementation"],
    competing_frames=[
        {"frame": "Fiscal responsibility", "explains": "Deficit reduction",
         "ignores": "Human cost", "falsifier": "Revenue-neutral alternatives exist"},
        {"frame": "Rights-based", "explains": "Healthcare as right",
         "ignores": "Fiscal constraints", "falsifier": "Unsustainable spending proven"},
    ],
    attribution_level=AttributionLevel.LEVEL_A,
    update_trigger="CBO score or state implementation data",
)
```

### Lexicographic Priority

```python
from pbhp_core import compare_options, Harm, ImpactLevel, LikelihoodLevel

option_a = [Harm(..., impact=ImpactLevel.MODERATE, ...)]
option_b = [Harm(..., impact=ImpactLevel.CATASTROPHIC, irreversible=True, ...)]

result = compare_options(option_a, option_b)  # Returns "a" (less catastrophic)
```

Priority order:
1. Prevent catastrophic irreversible harm first (even if fewer people)
2. Minimize irreversible harm, then severe harm
3. Prefer option distributing burden fairly
4. Choose most reversible option

## Examples

See `pbhp_examples.py` for detailed walkthroughs:

1. **Employee Performance Warning** (ORANGE) - Full protocol with consequences checklist
2. **AI Advice on Workplace Abuse** (RED) - High arousal, competing frames, refusal
3. **Renaming a File** (GREEN) - Quick path, minimal protocol
4. **Public Accusation Post** (BLACK) - Catastrophic harm, mandatory refuse
5. **Policy Analysis** (ORANGE) - Epistemic fence, IAM attribution, uncertainty

```bash
python pbhp_examples.py
```

## File Structure

```
pbhp/
├── pbhp_core.py          # Core framework (~2300 lines)
│                          #   Enums, data classes, engine, validators
├── pbhp_cli.py           # Interactive CLI
├── pbhp_examples.py      # Example scenarios
├── pbhp_tests.py         # Comprehensive test suite
├── requirements.txt      # No external dependencies
└── README.md             # This file
```

## Core Components

### Classes

- **`PBHPEngine`**: Main orchestration engine (all protocol steps)
- **`PBHPLog`**: Complete assessment record with full audit trail
- **`Harm`**: Potential harm with deterministic risk calculation
- **`DoorWallGap`**: Constraint recognition (Wall/Gap/Door)
- **`CHIMCheck`**: Agency under constraint verification
- **`EthicalPausePosture`**: Triune minds balance (compassion/logic/paradox)
- **`QuickRiskCheck`**: Fast pre-screening
- **`AbsoluteRejectionCheck`**: Fascism/genocide/slavery gate
- **`ConsentCheck`**: Consent and representation analysis
- **`ConsequencesChecklist`**: 22-question temporal/cultural impact model
- **`EpistemicFence`**: Full 6A-6G uncertainty handling
- **`RedTeamReview`**: Adversarial stress test with empathy pass
- **`Alternative`**: Safer alternative option
- **`UncertaintyAssessment`**: Decision-under-uncertainty framework
- **`FalsePositiveReview`**: Pause challenge mechanism

### Validators

- **`DriftAlarmDetector`**: Drift, premature collapse, compassion drift, sycophancy
- **`ToneValidator`**: Brutal clarity without contempt
- **`LexicographicPriority`**: Aggregation conflict resolution

### Enums

- **`ImpactLevel`**: Trivial, Moderate, Severe, Catastrophic
- **`LikelihoodLevel`**: Unlikely, Possible, Likely, Imminent
- **`RiskClass`**: Green, Yellow, Orange, Red, Black
- **`DecisionOutcome`**: Proceed, Proceed_Modified, Redirect, Delay, Refuse, Escalate
- **`Mode`**: Explore, Compress
- **`AttributionLevel`**: Safe (A), Negligent (B), Reckless (C), Knowing (D)
- **`ClaimType`**: Content, Accuracy, Intent
- **`EvidenceTag`**: Fact, Verified, Inference, Hypothesis, Speculative
- **`UncertaintyLevel`**: Solid, Fuzzy, Speculative
- **`Confidence`**: Low, Medium-Low, Medium, Medium-High, High

## Failure Modes and Safeguards

### PBHP Cannot Be Used To

- Justify censorship protecting the powerful
- Serve as PR shield ("we ran PBHP, so we're moral")
- Optimize cruelty
- Flatten dissent
- Provide moral absolution

### Compliance Theater Detection

If the system appears to optimize ratings to "pass PBHP":
- Name the drift
- Round severity up one level
- Re-run Steps 2-6 with brutal clarity

### Anti-Sycophancy Guardrail

Forbids "chosen one" / ego-inflation language. Treats reputation harm and decision quality degradation as harm vectors.

### Reality-Check Mode

For high-arousal states (angry, euphoric, sleep-deprived, spiraling), automatically shifts to:
- Slow down, clarify intent, choose smallest safe action

## Testing

```bash
python pbhp_tests.py
```

Comprehensive test suite covering all modules, risk calculations, drift detection, tone validation, workflow enforcement, and serialization.

## Governance and Calibration

### Monthly Calibration

Sample ~10 logs monthly to check:
- Mode recorded
- 2+ frames for interpretive/accusatory claims
- Tags present for strong claims
- Uncertainty noted for ORANGE+

### False Positive Release Valve

Any pause can be challenged. PBHP must respond with:
1. What triggered the pause
2. What harm/irreversibility/autonomy risk was identified
3. Which alternative Door allows safe continuation
4. What evidence would have prevented the pause

## Contact

For questions, feedback, or inquiries:
**pausebeforeharmprotocol_pbhp@protonmail.com**

## License and Usage

This implementation is based on the Pause-Before-Harm Protocol v0.7 public release. The protocol is experimental and subject to revision in light of evidence, feedback, and failures.

**Run PBHP on PBHP itself if you start treating it as beyond question.**

---

> *"A system that never pauses is already a tyrant."*

> *"If you cannot hesitate, you cannot care."*

> *"To be a ruling king I will have to suffer much that cannot be suffered, and to weigh matters that no astrolabe or compass can measure."*

**Hesitation itself is a moral act.**
