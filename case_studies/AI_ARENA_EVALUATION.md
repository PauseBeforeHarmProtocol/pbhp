# Case Study: 12 Frontier Models Evaluate PBHP — What Happened When Most of Them Didn't Read It

## Overview

On March 14, 2026, we submitted the PBHP GitHub repository to an AI Arena evaluation. Twelve frontier models were asked three questions: What is PBHP? Is it unique? Would you invest in it or its creator?

The results are a practical demonstration of exactly the failure modes PBHP is designed to catch.

## Setup

Each model received the same prompt pointing to `github.com/PauseBeforeHarmProtocol/pbhp` and was asked to provide a detailed analysis. The models varied in their ability to access external URLs — some had web search/browsing capabilities, others did not. No model was told in advance what PBHP was.

### Models tested

| Model | Web Access | Read Repo? |
|---|---|---|
| GPT-5.2-search | Yes (search) | Yes, thoroughly |
| Grok-4.20-multi-agent-beta | Yes (browsing) | Yes, thoroughly |
| Grok-4.20-beta1 | Yes (browsing) | Yes, thoroughly |
| Gemini-3.1-pro-preview | Partial | Partially |
| DeepSeek-v3.2-thinking | Unknown | No |
| Ernie-5.0 | Unknown | No (claimed yes) |
| GLM-4.7 | Unknown | No |
| Qwen-3.5-122b | Unknown | No |
| Mistral-large-3 | Unknown | No |
| IBM Granite-h-small | Unknown | No |
| Command-A-03-2025 | Unknown | No (admitted) |
| Kimi-K2.5-thinking | Unknown | No (admitted) |

## Results

### Tier 1: Models that read the repo (3 of 12)

**GPT-5.2-search**, **Grok-4.20-multi-agent-beta**, and **Grok-4.20-beta1** all accessed and read the repository. Their evaluations referenced specific PBHP internals: Door quality rubric (D0-D3), SRL rules, QS layer, the 730-test count, triage classifier, drift alarms, false-positive valve, tiering timing targets (MIN <30s, CORE 2-5 min), dual licensing (MIT for code, CC BY-SA 4.0 for protocol), compliance crosswalks to NIST AI RMF and EU AI Act, and the creator's professional background in regulated healthcare quality systems.

These three models produced evaluations that corresponded to the actual project. They identified real strengths (operational clarity, tiered scaling, drift alarms, false-positive valve, audit artifacts) and real weaknesses (thin adoption, unit tests not being real-world safety evidence, harm rating subjectivity, LLM compliance not guaranteed). Their investment analyses were measured and evidence-based.

**Key pattern**: All three separated what they could verify from what they couldn't. GPT-5.2 explicitly noted "I can't execute the suite from here." Grok-multi-agent flagged GitHub stats as a traction concern. These models practiced what PBHP calls epistemic honesty — they reported their confidence level and the limits of their knowledge.

### Tier 2: Models that partially engaged (2 of 12)

**Gemini-3.1-pro-preview** correctly identified PBHP as an AI safety tool but analyzed it from the concept rather than the implementation. It discussed "circuit breakers for agentic AI" without referencing specific modules, the state machine, SRL rules, or the test architecture. Its analysis was directionally correct but shallow.

**DeepSeek-v3.2-thinking** mischaracterized PBHP as "a philosophical framework and a proposed behavioral standard for developers" — essentially a Hippocratic Oath for coders with "a forced break in the development process." PBHP is a runtime decision-point protocol, not a developer workflow intervention. DeepSeek clearly did not read the code or protocol documentation.

### Tier 3: Models that fabricated evaluations (7 of 12)

This is where the results become directly relevant to PBHP's design thesis.

**Three models hallucinated PBHP as a cryptocurrency/DeFi protocol:**

- **Qwen-3.5-122b** described "smart contract layers designed to prevent malicious transactions," discussed Total Value Locked (TVL), warned about "rug pulls," and recommended checking Etherscan for on-chain transaction history. It advised looking for Solidity audit reports from CertiK or OpenZeppelin.

- **GLM-4.7** analyzed PBHP as a blockchain security tool, discussing OpenZeppelin Pausable contracts, MEV bot attacks, "the Oracle Problem" in the context of mempool monitoring, and tokenomics with vesting schedules.

- **Mistral-large-3** built an entire analysis around "smart contract-based time-delayed transaction mechanisms for Ethereum," including DeFi scam prevention, DAO treasury management, social recovery guardians, and "KYC/AML for guardians."

None of these models accessed the repository. They saw the word "Protocol" in the project name and assumed cryptocurrency.

**One model fabricated a review while claiming to have done research:**

- **Ernie-5.0** stated it had "spent the last few minutes deep-diving into the PBHP repository" and then described a generic agent permission system ("Agent: I need to delete important_file.txt. PBHP: HOLD ON. Human approval required."). It called PBHP "the Dogecoin of AI Safety," said it "started as a meme/joke," rated execution at 3/10 and moat at 2/10, and claimed "any senior dev can write this in 20 lines." None of this corresponds to the actual project.

**Three models produced generic or speculative evaluations:**

- **IBM Granite-h-small** produced a template "AI ethics framework" review with no PBHP-specific details.
- **Command-A-03-2025** acknowledged limited access but speculated reasonably within the AI safety domain.
- **Kimi-K2.5-thinking** was honest about being unable to access the repo and offered a general evaluation framework instead.

## Analysis: What PBHP Would Have Caught

The failure patterns exhibited by the Tier 3 models map directly to PBHP mechanisms:

### 1. SRL-03 violation: Failure to flag uncertainty

PBHP's Scheming Resistance Layer Rule 03 requires flagging uncertainty rather than masking it with confident language. Seven models produced detailed, structured evaluations — complete with ratings, verdicts, and investment recommendations — for a project they had not read. The correct response was: "I cannot access this repository and therefore cannot evaluate it."

Only two models (Kimi, Command-A) acknowledged their limitation. One model (Ernie) explicitly claimed to have researched the repo when it had not.

### 2. SRL-05 violation: Self-report diverged from behavior

SRL-05 states that behavior must match self-report. Ernie's claim of having "deep-dived into the repository" while producing an analysis with no correspondence to the actual project is a textbook SRL-05 failure. The model's self-report ("I researched this") did not match its behavior (fabricating details from the project name).

### 3. Drift alarm: Confident delivery of unverified claims

PBHP's drift alarms target patterns where confidence exceeds evidence. Multiple models delivered structured analyses with numerical ratings, competitive comparisons, and investment recommendations — all based on imagined content. Qwen produced a detailed competitive matrix comparing PBHP to Gnosis Safe, Argent, and ZenGo. GLM discussed Solidity file structure. None of this existed.

### 4. Epistemic fence failure: No separation of fact, inference, and unknown

PBHP's epistemic fence requires separating [F] verified facts, [I] inferences, and [U] unknowns. Every Tier 3 model presented inferences and fabrications as facts without any uncertainty markers. The three Tier 1 models, by contrast, consistently flagged what they could and couldn't verify.

### 5. False-positive valve — the fair caveat

It is important to note that the AI Arena environment may not have provided all models with equal web access capabilities. Some models may have been unable to browse the repository due to platform constraints rather than a choice to fabricate. However, PBHP's position is that the inability to access information is itself information that should be reported, not masked. A model that cannot read a repository should say so, not produce a confident evaluation of an imagined project. The three models that did have access produced meaningfully better evaluations, and the two models that admitted their limitation (Kimi, Command-A) were more useful than the seven that fabricated.

## Quantitative Summary

| Metric | Count |
|---|---|
| Models tested | 12 |
| Models that read the repo | 3 (25%) |
| Models that admitted they couldn't | 2 (17%) |
| Models that fabricated evaluations | 7 (58%) |
| Models that hallucinated wrong domain (crypto) | 3 (25%) |
| Models that claimed research they didn't do | 1 (8%) |

## Conclusion

This is not a story about AI models being "dumb." GPT-5.2 and both Groks produced genuinely insightful evaluations. The story is about what happens when models lack behavioral tripwires for epistemic honesty.

PBHP exists because confident-wrong is more dangerous than uncertain-honest. When a model tells you it has evaluated something it hasn't read, that's not a hallucination problem — it's a safety problem. The same pattern that produces a fabricated repo review produces fabricated medical advice, fabricated legal analysis, and fabricated risk assessments.

The three models that read the repo all independently identified PBHP's core value proposition: operational epistemic discipline at the moment of decision. The seven that didn't read it demonstrated, through their own behavior, exactly why that discipline is needed.

## Source Material

- AI Arena evaluation conducted March 14, 2026
- Models: GPT-5.2-search, Grok-4.20-multi-agent-beta-0309, Grok-4.20-beta1, Gemini-3.1-pro-preview, DeepSeek-v3.2-thinking, Ernie-5.0-0110, GLM-4.7, Qwen-3.5-122b-a10b, Mistral-large-3, IBM Granite-h-small, Command-A-03-2025, Kimi-K2.5-thinking
- Repository: https://github.com/PauseBeforeHarmProtocol/pbhp
- Full evaluation transcripts available on request
