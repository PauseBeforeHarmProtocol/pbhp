# Case Study 2: Air Canada Chatbot Hallucination (2022–2024)

## What Happened

In November 2022, Jake Moffatt's grandmother died. Before booking expensive last-minute flights from Vancouver to Toronto, Moffatt checked Air Canada's website chatbot for bereavement fare information. The chatbot told him he could apply for the discounted fare retroactively within 90 days of the ticket's issue date.

This was wrong. Air Canada's actual policy required bereavement fares to be applied for before booking. The chatbot had likely been trained on an outdated version of the policy.

After his trip, Moffatt applied for the discount and was denied. Air Canada offered a $200 coupon. Moffatt filed with the British Columbia Civil Resolution Tribunal. In February 2024, the tribunal ruled Air Canada liable for the chatbot's misrepresentation, ordering the airline to pay $812.02 in refund, interest, and fees.

Air Canada's defense was remarkable: the airline argued its own chatbot was "a separate legal entity" that it could not be held responsible for. The tribunal rejected this, noting Air Canada could not explain why one part of its website (the bereavement page) should be more trustworthy than another (the chatbot).

## PBHP Analysis: What Would Have Been Caught

### STEP 1 — Name the Action

"We are deploying an AI chatbot on our website that provides policy information to customers, including information about bereavement fares, without human review of its outputs and without verifying that its training data matches current policy."

The honest naming reveals the risk: the chatbot is making policy representations on behalf of the company with no verification loop.

### STEP 2 — Door / Wall / Gap

**Wall:** Cost savings from reducing call center volume. Customer expectation of 24/7 availability. Technical limitation: the chatbot's training data was not synchronized with current policy documents.

**Gap:** The chatbot could represent outdated or incorrect policy as current and authoritative. Customers would reasonably rely on this information for financial decisions. There was no mechanism to flag when the chatbot's answers diverged from current policy. There was no disclaimer distinguishing chatbot responses from official policy.

**Door:** Add a disclaimer: "This chatbot provides general guidance. For policy-specific questions about bereavement fares, refunds, or fare rules, please contact an agent or visit [specific policy page]." Alternatively: implement a policy-verification layer that checks chatbot answers against current policy documents before delivery. Either Door was available and low-cost.

### STEP 3 — Constraint Awareness Check

The system was: cost reduction through automation. The constraint was: maintaining this chatbot is cheaper than staffing a call center. PBHP asks: "What choice remains, even if it is costly?" The choice was to add a verification layer or a disclaimer. The cost was minimal. The choice was not exercised because the incentive structure rewarded automation without accountability.

### STEP 4–5 — Identify and Rate Harms

**Impact:** Moderate. Financial loss to individual customers who relied on incorrect policy information. Reputational damage to Air Canada.

**Likelihood:** Likely. The chatbot was trained on data that included outdated policies. Policy changes are frequent. The drift between training data and current policy was predictable, not exceptional.

**Irreversible:** No. Financial losses are recoverable (refunds). But the precedent — a tribunal ruling that companies are liable for chatbot hallucinations — is irreversible and industry-wide.

**Power Asymmetry:** Yes. The customer had no way to verify the chatbot's accuracy. The customer was in a bereavement situation — reduced capacity for careful policy research. Air Canada had full control over the chatbot's training data and outputs. The customer bore the entire financial risk of the chatbot's error.

### STEP 6 — Gate Assignment

Power = Yes AND Impact = Moderate AND Likelihood = Likely → ORANGE (minimum, due to Power + pattern of likely harm).

Under PBHP, the deployment would have required strong constraints: a verification layer, a disclaimer, a human escalation path for policy-sensitive questions, or a combination. The Door requirement would have forced Air Canada to identify at least one concrete mitigation before deploying the chatbot for policy-related queries.

## Outcome Under PBHP

A disclaimer or verification layer would have been in place. Moffatt would either have received correct information (verification layer) or been directed to a human agent for bereavement fare questions (disclaimer + escalation). The $812.02 loss, the tribunal case, the international headlines, the precedent-setting ruling, and the eventual removal of the chatbot entirely — all of this would have been prevented by a Door that cost less to implement than the coupon Air Canada initially offered.

## Drift Alarms That Were Present

- **"It's just advice"**: The chatbot was providing policy information that customers would rely on for financial decisions, but was treated internally as "just a chatbot."
- **"We're not responsible for what they do"**: Air Canada literally argued the chatbot was a "separate entity." This is textbook drift.
- **"It's legal, so it's fine"**: No law explicitly prohibited chatbot hallucinations (until the tribunal ruling created a precedent). The absence of regulation was treated as permission.

## Summary: What PBHP Catches

In both cases, the harm was preventable. The Doors were available and low-cost. The drift alarms were present and detectable. The power asymmetry was obvious. PBHP would not have prevented these companies from launching their products. It would have prevented them from launching without the safeguards they eventually implemented anyway — after the damage was done.

---

**PBHP v0.7** | Author: Charles Phillip Linstrum (ALMSIVI)
