# AegisGuard Use Cases

> **Canonical description of how users and system components interact with AegisGuard V1.**

---

## 1. Document Status

**Status:** Living
**Version:** 1.0
**Scope:** AegisGuard V1
**Document Type:** Use-Case Specification

### Purpose

This document defines the primary use cases supported by AegisGuard V1.

Each use case describes:

* The actor initiating or participating in the interaction
* The goal
* Preconditions
* Main flow
* Alternative flows
* Postconditions
* Important business rules

This document describes **system behaviour**, not implementation instructions.

---

# 2. Actors

AegisGuard contains several types of actors.

## 2.1 Fraud/Risk Analyst

The primary human user of AegisGuard.

The analyst can:

* Review Risk Events
* Inspect evidence
* Review investigations
* Review exposure
* Review recommendations
* Approve or reject actions
* Escalate cases
* Record decisions

---

## 2.2 Payment Environment

Represents the synthetic payment environment generating payment activity.

It provides:

* Customers
* Merchants
* Transactions
* Devices
* Network identities
* Transaction outcomes

---

## 2.3 ML Risk Model

The machine-learning component responsible for transaction-level risk scoring.

It produces:

* Risk scores
* Model predictions

It does not directly execute defensive actions.

---

## 2.4 Rule Engine

The deterministic component responsible for evaluating explicit risk rules.

It produces:

* Rule evaluations
* Risk signals

---

## 2.5 Anomaly Detection System

The component responsible for detecting unusual behavioural patterns.

V1 primarily focuses on merchant-level behaviour.

It produces:

* Behavioural anomalies
* Supporting anomaly information

---

## 2.6 AI Investigation Agent

The AI component responsible for investigating Risk Events.

It can:

* Retrieve evidence
* Correlate information
* Analyze available context
* Summarize incidents
* Explain suspicious patterns
* Recommend defensive responses

It does not bypass policy controls.

---

## 2.7 Policy Engine

The deterministic control layer responsible for evaluating recommendations.

It produces:

```text
ALLOW
APPROVAL_REQUIRED
DENY
```

---

## 2.8 Fraud Outcome Source

Represents sources from which later fraud outcomes become known.

Examples:

* Customer report
* Chargeback
* Manual investigation
* External confirmation
* Legitimate transaction determination

---

# 3. Use-Case Map

The primary AegisGuard V1 use cases are:

```text id="v4o8tr"
UC-01  Assess a Transaction for Risk
UC-02  Detect Unusual Merchant Behaviour
UC-03  Create a Risk Event
UC-04  Investigate a Risk Event
UC-05  Check Shared Fraud Intelligence
UC-06  Estimate Potential Financial Exposure
UC-07  Generate Defensive Recommendation
UC-08  Evaluate Recommendation Against Policy
UC-09  Review and Approve High-Impact Action
UC-10  Execute Defensive Action
UC-11  Record Complete Risk Audit Trail
UC-12  Receive a Later Fraud Outcome
UC-13  Build Historical Training/Evaluation Data
UC-14  Handle Component Failure Safely
UC-15  End-to-End Investigation and Response
```

---

# 4. UC-01 — Assess a Transaction for Risk

## Goal

Determine the risk associated with an individual payment transaction.

## Primary Actor

Payment Environment

## Supporting Actors

* ML Risk Model
* Rule Engine
* Risk Signal sources

## Preconditions

* A valid transaction exists.
* Required transaction information is available.

## Main Flow

```text id="g6n7u4"
1. Payment Environment provides a transaction.
2. AegisGuard validates the transaction.
3. AegisGuard retrieves relevant historical information.
4. Available risk signals are identified.
5. Deterministic risk rules are evaluated.
6. ML risk scoring is performed.
7. The resulting risk information is stored.
8. The transaction becomes available for downstream risk-event processing.
```

## Risk information may include

* Transaction attributes
* Customer history
* Merchant history
* Device information
* Network information
* Risk signals
* Rule results
* ML score

## Alternative Flow — ML unavailable

```text id="5r9k7y"
1. ML scoring fails or is unavailable.
2. Deterministic rules and available risk signals remain usable.
3. The transaction is not silently treated as safe.
4. The system may escalate or continue using the available signals.
5. The failure is recorded.
```

## Postconditions

* Transaction is persisted.
* Available risk information is persisted.
* ML score is stored if generated.
* Model version is recorded when ML scoring occurs.
* Relevant audit history exists.

## Important Rule

Only information available at the transaction decision point may be used for transaction-time risk assessment.

---

# 5. UC-02 — Detect Unusual Merchant Behaviour

## Goal

Identify merchant behaviour that significantly deviates from its historical baseline.

## Primary Actor

Anomaly Detection System

## Preconditions

* Merchant has sufficient historical activity for meaningful comparison.
* Current merchant activity is available.

## Main Flow

```text id="eqk7g6"
1. Retrieve merchant activity.
2. Calculate relevant behavioural metrics.
3. Retrieve historical baselines.
4. Compare current behaviour with expected behaviour.
5. Identify significant deviations.
6. Create a BehaviouralAnomaly when appropriate.
7. Store the baseline, observed value, deviation, and detection method.
```

## Example

```text id="jz3kbi"
Historical transaction volume:
10,000/day

Observed volume:
27,000/day

→ Significant behavioural anomaly
```

## Postconditions

A BehaviouralAnomaly exists if unusual behaviour is detected.

## Important Rule

```text id="r8epc5"
Behavioural anomaly ≠ confirmed fraud
```

An anomaly is a reason for investigation, not proof of fraud.

---

# 6. UC-03 — Create a Risk Event

## Goal

Create a higher-level Risk Event from correlated suspicious activity.

## Primary Actor

AegisGuard Detection System

## Supporting Actors

* ML Risk Model
* Rule Engine
* Anomaly Detection System

## Preconditions

Relevant risk information exists.

## Main Flow

```text id="6kt7kh"
1. AegisGuard identifies suspicious signals.
2. Related transactions are identified.
3. Related entities are identified.
4. Merchant behavioural anomalies are considered.
5. Previous relevant risk activity is considered.
6. Signals are correlated.
7. A Risk Event is created.
8. Relevant transactions are associated with the event.
9. Severity and status are assigned.
10. The event is made available for investigation.
```

## Postconditions

A Risk Event exists with:

* Severity
* Status
* Triggering context
* Related transactions
* Relevant signals

---

# 7. UC-04 — Investigate a Risk Event

## Goal

Understand why a Risk Event is suspicious and determine the relevant evidence.

## Primary Actor

AI Investigation Agent

## Supporting Actors

* Fraud/Risk Analyst
* Database
* Shared Fraud Intelligence
* Detection components

## Preconditions

* A Risk Event exists.
* Relevant data is available.

## Main Flow

```text id="6t1k7n"
1. Investigation is initiated.
2. Relevant transactions are retrieved.
3. Risk scores are retrieved.
4. Rule evaluations are retrieved.
5. Risk signals are retrieved.
6. Merchant behavioural information is retrieved.
7. Related devices are examined.
8. Related network identities are examined.
9. Previous relevant risk activity is examined.
10. Shared fraud intelligence is queried where appropriate.
11. Evidence is correlated.
12. Investigation findings are generated.
13. Findings are stored.
14. The Risk Event becomes ready for exposure assessment and recommendation.
```

## Investigation Output

The investigation should distinguish:

```text id="sm8o2s"
Observed Facts
Model Predictions
Rule Results
Behavioural Observations
External/Simulated Signals
AI Interpretation
```

## Alternative Flow — AI unavailable

```text id="c6qyr9"
1. AI investigation cannot execute.
2. Risk Event remains open.
3. Relevant evidence remains accessible.
4. Analyst can investigate manually.
5. Failure is recorded.
```

## Postconditions

An Investigation exists containing structured evidence and findings.

---

# 8. UC-05 — Check Shared Fraud Intelligence

## Goal

Determine whether relevant entities or activity appear in the shared fraud-intelligence environment.

## Primary Actor

AI Investigation Agent

## Supporting Actor

Simulated Network Intelligence

## Preconditions

* An investigation is active.
* An entity suitable for lookup exists.

## Main Flow

```text id="p2h4cq"
1. Investigation identifies an entity of interest.
2. Agent requests a network-intelligence lookup.
3. Simulated intelligence source is queried.
4. Matching intelligence is returned.
5. Results are recorded as NetworkSignals.
6. Relevant results are incorporated into investigation evidence.
```

## Postconditions

Network intelligence is available as investigation evidence where applicable.

## Important Rule

All V1 network intelligence must be clearly identified as simulated.

---

# 9. UC-06 — Estimate Potential Financial Exposure

## Goal

Estimate the potential financial exposure associated with a Risk Event.

## Primary Actor

AegisGuard Investigation System

## Preconditions

* A Risk Event exists.
* Relevant transactions are available.

## Main Flow

```text id="w2l0gj"
1. Retrieve transactions associated with the Risk Event.
2. Identify transactions relevant to the exposure calculation.
3. Calculate the estimated amount.
4. Record the currency.
5. Record the calculation method.
6. Store the ExposureAssessment.
```

## Example

```text id="7zzlme"
Transaction A = ₹10,000
Transaction B = ₹15,000
Transaction C = ₹7,000

Estimated Exposure = ₹32,000
```

## Important Rule

Potential exposure is an estimate.

It does not represent confirmed financial loss.

## Postconditions

An ExposureAssessment exists for the Risk Event.

---

# 10. UC-07 — Generate Defensive Recommendation

## Goal

Determine an appropriate defensive response based on the investigation.

## Primary Actor

AI Investigation Agent / AegisGuard Decision System

## Preconditions

* Investigation has produced sufficient evidence.
* Risk Event exists.
* Relevant exposure information is available where applicable.

## Main Flow

```text id="t2q4hj"
1. Investigation findings are considered.
2. Relevant risk severity is considered.
3. Exposure is considered.
4. Supporting evidence is considered.
5. A defensive action is proposed.
6. Reasoning is recorded.
7. Confidence is recorded.
8. Human-approval requirements are identified.
9. Recommendation is persisted.
10. Recommendation is sent to the Policy Engine.
```

## Possible Recommendations

```text id="6vv0rc"
CONTINUE_MONITORING
ESCALATE
REQUIRE_VERIFICATION
MERCHANT_REVIEW
RESTRICT_SELECTED_ACTIVITY
```

## Important Rule

A Recommendation does not execute an Action.

---

# 11. UC-08 — Evaluate Recommendation Against Policy

## Goal

Determine whether a recommendation is authorized, requires human approval, or must be rejected.

## Primary Actor

Policy Engine

## Preconditions

* Recommendation exists.
* Relevant policies are available.

## Main Flow

```text id="dzl95c"
1. Policy Engine receives the Recommendation.
2. Applicable policies are identified.
3. Risk severity is evaluated.
4. Confidence is evaluated where relevant.
5. Exposure is evaluated where relevant.
6. Action type is evaluated.
7. Merchant status and automation limits are considered.
8. Policy decision is generated.
9. PolicyDecision is stored.
```

## Possible Results

```text id="n3e6j0"
ALLOW
APPROVAL_REQUIRED
DENY
```

## Postconditions

A PolicyDecision exists.

## Important Rule

The AI agent cannot bypass the Policy Engine.

---

# 12. UC-09 — Review and Approve High-Impact Action

## Goal

Allow an analyst to make a human decision when policy requires approval.

## Primary Actor

Fraud/Risk Analyst

## Preconditions

* Recommendation exists.
* PolicyDecision = `APPROVAL_REQUIRED`.

## Main Flow

```text id="xqtx3q"
1. Analyst opens the Risk Event.
2. Analyst reviews triggering signals.
3. Analyst reviews related transactions.
4. Analyst reviews investigation findings.
5. Analyst reviews evidence.
6. Analyst reviews exposure.
7. Analyst reviews AI recommendation.
8. Analyst reviews policy decision.
9. Analyst approves, rejects, or escalates.
10. HumanDecision is recorded.
```

## Alternative Flow — Reject

```text id="l0s8m3"
1. Analyst rejects the recommendation.
2. No consequential Action is executed.
3. Rejection reason is recorded.
4. Audit history is updated.
```

## Alternative Flow — Escalate

```text id="r4qklc"
1. Analyst escalates the event.
2. Event remains open.
3. Additional investigation may occur.
```

## Postconditions

A HumanDecision exists.

An Action may proceed only if authorization requirements have been satisfied.

---

# 13. UC-10 — Execute Defensive Action

## Goal

Execute an authorized defensive response in the simulated payment environment.

## Primary Actor

AegisGuard Response System

## Supporting Actors

* Policy Engine
* Fraud/Risk Analyst
* Simulated Payment Environment

## Preconditions

One of the following must be true:

```text id="odq4bc"
PolicyDecision = ALLOW

OR

PolicyDecision = APPROVAL_REQUIRED
AND
valid HumanDecision authorizes the action
```

## Main Flow

```text id="j8ozzv"
1. System verifies authorization.
2. System verifies the intended action.
3. Defensive action is executed against the simulated environment.
4. Action result is recorded.
5. Action status is updated.
6. Audit event is created.
```

## Alternative Flow — Unauthorized

```text id="zh78un"
1. Authorization check fails.
2. Action is not executed.
3. Failure is recorded.
4. Audit history is updated.
```

## Postconditions

If successful:

* Action exists.
* Action result is recorded.
* Relevant state in the simulated environment changes.
* Audit trail contains the execution.

---

# 14. UC-11 — Record Complete Risk Audit Trail

## Goal

Maintain a reconstructable history of significant risk decisions.

## Primary Actor

AegisGuard

## Main Flow

AegisGuard records significant events such as:

```text id="k7c8b4"
Transaction received
Risk score generated
Rule evaluated
Rule triggered
Anomaly detected
Risk Event created
Investigation started
Evidence collected
Recommendation generated
Policy evaluated
Human decision recorded
Action executed
Fraud outcome received
```

## Postconditions

Important decisions and state transitions can be reconstructed from persistent history.

## Important Rule

Auditability is a system requirement, not merely debugging output.

---

# 15. UC-12 — Receive a Later Fraud Outcome

## Goal

Record information learned after the original transaction.

## Primary Actor

Fraud Outcome Source

## Preconditions

A transaction or relevant Risk Event exists.

## Main Flow

```text id="jz6g2e"
1. A later outcome becomes available.
2. AegisGuard identifies the related transaction.
3. The outcome source is recorded.
4. The outcome timestamp is recorded.
5. The outcome is associated with the relevant transaction.
6. Where applicable, it is associated with the Risk Event.
7. A FraudOutcome is persisted.
8. Audit history is updated.
```

## Possible Outcomes

```text id="eq5vaz"
CONFIRMED_FRAUD
LEGITIMATE
FALSE_POSITIVE
CUSTOMER_REPORTED_FRAUD
CHARGEBACK
MANUAL_CONFIRMATION
```

The exact V1 enumeration may be refined during implementation.

## Important Rule

The outcome may become available long after the original transaction decision.

It must not be retroactively treated as transaction-time information.

---

# 16. UC-13 — Build Historical Training/Evaluation Data

## Goal

Use reliable historical outcomes to evaluate and improve fraud-risk models.

## Primary Actor

ML System

## Preconditions

* Historical transactions exist.
* Later outcomes are available for a meaningful subset of transactions.
* Decision-time information can be reconstructed.

## Main Flow

```text id="2p7jbl"
1. Retrieve historical transactions.
2. Retrieve information available at the original decision point.
3. Retrieve later fraud outcomes.
4. Construct features using only decision-time information.
5. Associate appropriate later outcomes as labels.
6. Exclude or appropriately handle uncertain/noisy outcomes.
7. Produce historical training/evaluation data.
8. Evaluate model performance.
```

## Important Rule

The feature dataset and outcome labels have different temporal meanings.

```text id="g5k7f2"
Features
= Information available at decision time

Labels
= Information learned later
```

---

# 17. UC-14 — Handle Component Failure Safely

## Goal

Ensure system failures do not produce uncontrolled consequential actions.

## Primary Actor

AegisGuard

## Scenario A — ML Failure

```text id="u8h6bs"
1. ML scoring becomes unavailable.
2. Transaction processing continues where safe.
3. Deterministic risk rules/signals remain available.
4. System may escalate when necessary.
5. Failure is recorded.
```

## Scenario B — AI Failure

```text id="x9k3qv"
1. AI investigation becomes unavailable.
2. Risk Event remains open.
3. Evidence remains accessible.
4. Analyst can investigate manually.
5. No unsafe automated action occurs solely because AI failed.
6. Failure is recorded.
```

## Scenario C — Policy Engine Failure

```text id="3m17xn"
1. Policy evaluation becomes unavailable.
2. Consequential action is not allowed to bypass policy.
3. Action remains pending or is escalated.
4. Failure is recorded.
```

## Postconditions

System failure does not result in uncontrolled high-impact behaviour.

---

# 18. UC-15 — End-to-End Investigation and Response

## Goal

Complete the full AegisGuard fraud-risk lifecycle for a suspicious activity pattern.

## Primary Actor

Fraud/Risk Analyst

## Supporting Actors

* Payment Environment
* ML Risk Model
* Rule Engine
* Anomaly Detection System
* AI Investigation Agent
* Policy Engine

## Preconditions

* Synthetic payment activity exists.
* Required system components are available.

## Main Flow

```text id="h7c4f8"
1. A suspicious transaction enters the system.
2. Transaction data is validated.
3. Risk signals are collected.
4. Deterministic rules are evaluated.
5. ML risk scoring occurs.
6. Merchant behaviour is evaluated.
7. Behavioural anomalies are detected where applicable.
8. Related activity is correlated.
9. A Risk Event is created.
10. Investigation begins.
11. Relevant transactions are retrieved.
12. Related devices and network identities are examined.
13. Simulated network intelligence is queried.
14. Evidence is assembled.
15. AI investigation produces structured findings.
16. Potential exposure is estimated.
17. A defensive recommendation is generated.
18. Recommendation is evaluated by the Policy Engine.
19. If human approval is required, the analyst reviews the event.
20. Analyst approves, rejects, or escalates.
21. If authorized, a simulated defensive Action is executed.
22. The entire lifecycle is recorded in the audit trail.
23. A later FraudOutcome may eventually arrive.
24. The outcome becomes available for model evaluation.
```

## Postconditions

The system has demonstrated the complete lifecycle:

```text id="c9n3q0"
Detect
  ↓
Correlate
  ↓
Investigate
  ↓
Assess
  ↓
Recommend
  ↓
Constrain
  ↓
Decide
  ↓
Act
  ↓
Audit
  ↓
Learn
```

---

# 19. Cross-Cutting Business Rules

The following rules apply across multiple use cases.

## BR-01 — Prediction Is Not Confirmation

A model prediction must not be represented as a confirmed fraud outcome.

---

## BR-02 — Anomaly Is Not Confirmation

A behavioural anomaly must not automatically be classified as fraud.

---

## BR-03 — Recommendation Is Not Action

A recommendation must not be treated as an executed defensive action.

---

## BR-04 — AI Must Respect Policy

The AI agent must not bypass the Policy Engine.

---

## BR-05 — Human Approval Must Be Enforceable

If policy requires human approval, the action cannot execute without a valid HumanDecision.

---

## BR-06 — Later Outcomes Are Not Historical Features

Information learned after the original transaction cannot be silently used as a feature for the original risk decision.

---

## BR-07 — Simulated Intelligence Must Be Identified

Synthetic shared fraud intelligence must be clearly identified as simulated.

---

## BR-08 — Exposure Is an Estimate

Potential financial exposure is an estimate and must not be presented as confirmed loss.

---

## BR-09 — Actions Are Simulated

V1 defensive actions operate only against the synthetic payment environment.

---

## BR-10 — Significant Decisions Must Be Auditable

Important system decisions and actions must produce persistent audit history.

---

## BR-11 — Failure Must Be Safe

Component failure must not allow consequential actions to bypass safety or policy controls.

---

# 20. Use-Case Dependency Map

The use cases form a dependency chain.

```text id="l4w6s5"
UC-01 Assess Transaction
       │
       ├──────────────→ UC-03 Create Risk Event
       │                       │
UC-02 Merchant Anomaly ────────┤
                               ↓
                       UC-04 Investigate
                               │
                    ┌──────────┴──────────┐
                    ↓                     ↓
              UC-05 Network          UC-06 Exposure
              Intelligence           Assessment
                    │                     │
                    └──────────┬──────────┘
                               ↓
                       UC-07 Recommendation
                               ↓
                       UC-08 Policy Decision
                               ↓
                       ┌───────┴────────┐
                       ↓                ↓
                UC-09 Human       UC-10 Action
                   Decision             │
                       │                │
                       └───────┬────────┘
                               ↓
                       UC-11 Audit Trail
                               ↓
                       UC-12 Later Outcome
                               ↓
                    UC-13 Historical Data
```

Failure handling through UC-14 applies across the lifecycle.

UC-15 combines the major use cases into one complete scenario.

---

# 21. Use-Case to Domain Mapping

| Use Case                        | Primary Domain Entities                                          |
| ------------------------------- | ---------------------------------------------------------------- |
| UC-01 Assess Transaction        | Transaction, RiskScore, RiskSignal, RuleEvaluation, ModelVersion |
| UC-02 Detect Merchant Behaviour | Merchant, BehaviouralAnomaly                                     |
| UC-03 Create Risk Event         | RiskEvent, RiskEventTransaction, RiskSignal                      |
| UC-04 Investigate Event         | Investigation, Evidence, RiskEvent                               |
| UC-05 Shared Intelligence       | NetworkSignal, Evidence                                          |
| UC-06 Exposure                  | ExposureAssessment, Transaction, RiskEvent                       |
| UC-07 Recommendation            | Recommendation, Investigation, RiskEvent                         |
| UC-08 Policy Evaluation         | Policy, PolicyDecision, Recommendation                           |
| UC-09 Human Review              | HumanDecision, Recommendation                                    |
| UC-10 Defensive Action          | Action, Recommendation, HumanDecision                            |
| UC-11 Audit                     | AuditEvent                                                       |
| UC-12 Later Outcome             | FraudOutcome, Transaction, RiskEvent                             |
| UC-13 Historical Learning       | FraudOutcome, Transaction, RiskScore, ModelVersion               |
| UC-14 Failure Handling          | All relevant system components                                   |
| UC-15 End-to-End                | All major V1 entities                                            |

---

# 22. Use-Case to Requirement Traceability

| Use Case | Primary Requirements                     |
| -------- | ---------------------------------------- |
| UC-01    | FR-01, FR-02, FR-03, FR-04, FR-05, FR-06 |
| UC-02    | FR-07, FR-08                             |
| UC-03    | FR-09, FR-10                             |
| UC-04    | FR-12, FR-13                             |
| UC-05    | FR-11                                    |
| UC-06    | FR-14                                    |
| UC-07    | FR-15                                    |
| UC-08    | FR-16                                    |
| UC-09    | FR-17                                    |
| UC-10    | FR-18                                    |
| UC-11    | FR-23                                    |
| UC-12    | FR-19, FR-20                             |
| UC-13    | FR-21, FR-22                             |
| UC-14    | FR-25                                    |
| UC-15    | FR-01 through FR-25 as applicable        |

---

# 23. V1 Use-Case Boundary

The use cases intentionally do not cover:

* Commercial SaaS onboarding
* Billing
* Multi-tenancy
* Enterprise account administration
* Real payment processing
* Real external consortium integrations
* Production compliance workflows
* Enterprise case-management systems
* Large-scale distributed infrastructure

These may be introduced in future versions if the product scope expands.

---

# 24. Relationship to Other Documents

This document is derived from:

```text id="0d8e5h"
product-definition.md
requirements.md
```

It provides behavioural context for:

```text id="6jcn6k"
domain-model.md
data-model.md
architecture.md
system-flows.md
```

The relationship is:

```text id="4xbrp6"
Product Definition
        ↓
Requirements
        ↓
Use Cases
        ↓
Domain Model
        ↓
Data Model
        ↓
Architecture
        ↓
System Flows
```

Changes to requirements or product scope may require changes to these use cases.

---

# 25. Change Management

This is a living document.

When a requirement changes:

1. Identify affected use cases.
2. Update the affected use cases.
3. Review domain entities.
4. Review persistence requirements.
5. Review system flows.
6. Review tests and implementation.

When a new use case is proposed, determine whether it represents:

* A genuinely new user/system goal
* An extension of an existing use case
* An implementation detail that does not belong as a separate use case

Avoid creating use cases solely to represent internal function calls.

---

# 26. Canonical V1 Use Cases

The canonical AegisGuard V1 use cases are:

```text id="ph0r9g"
UC-01  Assess a Transaction for Risk
UC-02  Detect Unusual Merchant Behaviour
UC-03  Create a Risk Event
UC-04  Investigate a Risk Event
UC-05  Check Shared Fraud Intelligence
UC-06  Estimate Potential Financial Exposure
UC-07  Generate Defensive Recommendation
UC-08  Evaluate Recommendation Against Policy
UC-09  Review and Approve High-Impact Action
UC-10  Execute Defensive Action
UC-11  Record Complete Risk Audit Trail
UC-12  Receive a Later Fraud Outcome
UC-13  Build Historical Training/Evaluation Data
UC-14  Handle Component Failure Safely
UC-15  End-to-End Investigation and Response
```

These represent the canonical behavioural scope of **AegisGuard V1**.
