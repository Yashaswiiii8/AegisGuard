# AegisGuard Domain Model

> **Canonical description of the AegisGuard V1 domain and its conceptual entities, relationships, responsibilities, and boundaries.**

---

## 1. Document Status

**Status:** Living
**Version:** 1.0
**Scope:** AegisGuard V1
**Document Type:** Domain Specification

### Purpose

This document defines the conceptual domain model of AegisGuard.

It describes:

* What entities exist in the system
* What each entity represents
* Why each entity exists
* How entities relate to one another
* The distinction between related but different concepts
* Important cardinalities
* Domain boundaries
* Temporal semantics
* Core invariants

This document defines the **domain**, not the implementation details of the database or API.

Database tables, columns, indexes, constraints, API schemas, and ORM implementations should be derived from this model rather than redefining the domain independently.

---

# 2. Domain Overview

AegisGuard models a fraud-risk lifecycle around payment activity.

The system must distinguish between:

```text
Transaction
     ↓
Risk Signal
     ↓
Risk Score / Rule Evaluation / Anomaly
     ↓
Risk Event
     ↓
Investigation
     ↓
Evidence
     ↓
Exposure Assessment
     ↓
Recommendation
     ↓
Policy Decision
     ↓
Human Decision (if required)
     ↓
Action
     ↓
Audit Event
     ↓
Later Fraud Outcome
```

These concepts are intentionally separate.

For example:

> A high ML risk score is not a fraud outcome.

Similarly:

> An anomaly is not proof of fraud.

And:

> An AI recommendation is not an executed action.

The domain model preserves these distinctions so that the system remains explainable, auditable, and suitable for future ML evaluation.

---

# 3. Domain Areas

The AegisGuard V1 domain is divided into six logical areas.

```text
┌─────────────────────────────────────────┐
│ Payment Domain                           │
│ Customer, Merchant, Transaction, Device │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ Detection Domain                         │
│ Scores, Signals, Rules, Anomalies,       │
│ Risk Events                              │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ Investigation Domain                    │
│ Investigation, Evidence, Network        │
│ Intelligence, Exposure, Recommendation  │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ Decision / Response Domain               │
│ Policy, Policy Decision, Human Decision │
│ Action                                   │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ Learning Domain                          │
│ Fraud Outcomes, Model Versions           │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ Governance Domain                        │
│ Audit Events                             │
└─────────────────────────────────────────┘
```

---

# 4. Payment Domain

The Payment Domain represents the entities involved in payment activity and the identities associated with that activity.

---

## 4.1 Customer

### Definition

A **Customer** represents an individual or account performing payment activity.

### Responsibilities

A Customer provides the identity context for transactions and historical behavioural analysis.

Relevant information may include:

* Customer identifier
* Account status
* Account creation information
* Historical transaction behaviour
* Historical risk activity

### Relationships

```text
Customer 1 ─────── * Transaction
Customer * ─────── * Device
```

A customer may perform many transactions.

A customer may use multiple devices over time.

A device may also be associated with multiple customers.

---

## 4.2 Merchant

### Definition

A **Merchant** represents a business or payment recipient participating in the payment environment.

### Responsibilities

A Merchant provides the entity context for:

* Transactions
* Historical behaviour
* Merchant-level anomaly detection
* Risk events
* Investigations
* Defensive actions

Relevant behavioural metrics may include:

* Transaction volume
* Transaction value
* Average transaction amount
* Failure rate
* Suspicious activity rate
* Refund/dispute rate
* Device diversity
* Geographic distribution
* Transaction velocity

### Relationships

```text
Merchant 1 ─────── * Transaction
Merchant 1 ─────── * BehaviouralAnomaly
```

A merchant may have many transactions and many historical behavioural anomalies.

---

## 4.3 Transaction

### Definition

A **Transaction** represents a payment event that occurred in the synthetic payment environment.

It is the central payment-domain entity around which risk assessment begins.

### Conceptual attributes

A transaction may contain:

* Transaction identifier
* Customer
* Merchant
* Amount
* Currency
* Timestamp
* Payment method
* Device
* Network identity
* Geographic information
* Transaction status

### Temporal attributes

A transaction must distinguish between:

* `occurred_at` — when the payment actually occurred
* `created_at` — when AegisGuard received/persisted the transaction

These timestamps must not be treated as interchangeable.

### Relationships

```text
Customer 1 ─────── * Transaction
Merchant 1 ─────── * Transaction
Device 1 ───────── * Transaction
NetworkIdentity 1 ─ * Transaction

Transaction 1 ──── * RiskScore
Transaction 1 ──── * RiskSignal
Transaction 1 ──── * RuleEvaluation
Transaction 1 ──── * FraudOutcome

Transaction * ───── * RiskEvent
```

A transaction can participate in multiple risk events if different investigations identify different suspicious contexts.

---

## 4.4 Device

### Definition

A **Device** represents a device identity associated with payment activity.

Examples may include:

* Browser/device fingerprint
* Mobile device identifier
* Synthetic device identity

### Purpose

Device relationships help identify behavioural connections between customers and transactions.

Example:

```text
Customer A
    ↓
Device X
    ↓
Transactions
    ↓
Merchant B
```

### Relationships

```text
Device * ─────── * Customer
Device 1 ─────── * Transaction
```

The many-to-many customer-device relationship is represented through the `CustomerDevice` association.

---

## 4.5 NetworkIdentity

### Definition

A **NetworkIdentity** represents a network-level identity associated with payment activity.

Examples:

* IP address
* Synthetic network identity
* Other network identifier

### Purpose

Network identities provide supporting risk context and allow related activity to be identified.

### Relationship

```text
NetworkIdentity 1 ───── * Transaction
```

A network identity can appear across many transactions.

---

## 4.6 CustomerDevice

### Definition

`CustomerDevice` is an association entity representing the relationship between customers and devices.

### Purpose

The relationship is many-to-many:

```text
Customer A ──┐
             ├── Device X
Customer B ──┘
```

This relationship can provide useful evidence during investigations.

For example, a device associated with many unrelated customers may become a relevant risk signal.

---

# 5. Detection Domain

The Detection Domain represents the mechanisms that identify potentially suspicious behaviour.

It contains multiple forms of evidence because no single detection mechanism should be treated as absolute truth.

---

## 5.1 RiskScore

### Definition

A **RiskScore** represents the output of a machine-learning risk model for a transaction.

It answers:

> "According to the model, how likely is this transaction to represent risky behaviour?"

### Important distinction

A risk score is a **prediction**, not a confirmed fraud outcome.

### Conceptual attributes

A RiskScore includes:

* Transaction
* Score/probability
* Model version
* Scoring timestamp
* Relevant scoring metadata

### Relationship

```text
Transaction 1 ───── * RiskScore
ModelVersion 1 ──── * RiskScore
```

Multiple scores may exist for the same transaction if the transaction is rescored using different model versions or at different stages.

---

## 5.2 RiskSignal

### Definition

A **RiskSignal** represents an individual piece of information that may contribute to a fraud-risk assessment or investigation.

Examples:

* Suspicious IP
* Unusual device
* High transaction velocity
* Geographic inconsistency
* Previous suspicious activity
* Blocklist match
* External intelligence match

### Important properties

A risk signal should identify:

* What the signal represents
* Its source
* When it was generated
* When it became available
* The entity or transaction it relates to

### Temporal semantics

A RiskSignal must support the concept of:

```text
occurred_at
created_at
available_at
```

`available_at` represents the earliest time the signal could legitimately have been used by the risk system.

This is important for preventing temporal leakage.

### Relationship

```text
Transaction 1 ───── * RiskSignal
```

Risk signals may also be associated with other entities in later implementations where appropriate.

---

## 5.3 RiskRule

### Definition

A **RiskRule** represents a deterministic condition used to identify potentially risky behaviour.

Examples:

```text
Transaction velocity > threshold

Entity appears on blocklist

Transaction occurs in restricted geography

Unusual number of failures within time window
```

### Purpose

Rules provide deterministic and explainable risk evidence.

Rules do not establish fraud by themselves.

### Relationship

```text
RiskRule 1 ───── * RuleEvaluation
```

---

## 5.4 RuleEvaluation

### Definition

A **RuleEvaluation** represents the result of evaluating a RiskRule against a transaction or relevant context.

It should capture:

* Rule evaluated
* Transaction/context
* Whether the rule triggered
* Evaluation time
* Relevant evaluation information

### Relationship

```text
RiskRule 1 ───── * RuleEvaluation
Transaction 1 ── * RuleEvaluation
```

A single transaction may trigger multiple rules.

---

## 5.5 BehaviouralAnomaly

### Definition

A **BehaviouralAnomaly** represents a statistically or heuristically unusual deviation from an expected behavioural baseline.

V1 primarily focuses on merchant-level behavioural anomalies.

Examples:

```text
Normal transaction volume:
10,000/day

Observed:
27,000/day

→ Behavioural anomaly
```

Another example:

```text
Historical average transaction amount:
₹1,200

Observed average:
₹4,800

→ Behavioural anomaly
```

### Important distinction

```text
Anomaly
   ≠
Fraud
```

An anomaly means:

> "This behaviour differs significantly from the expected baseline."

It does not mean:

> "This behaviour is definitely fraudulent."

### Conceptual attributes

An anomaly should preserve:

* Entity
* Metric
* Historical baseline
* Observed value
* Deviation
* Detection method
* Detection timestamp

### Relationship

```text
Merchant 1 ───── * BehaviouralAnomaly
```

---

## 5.6 RiskEvent

### Definition

A **RiskEvent** represents a correlated suspicious situation that is significant enough to warrant investigation or response.

It is a higher-level domain concept than an individual signal.

### Example

```text
Transaction A
Transaction B
Transaction C
       +
Same device
       +
Same network identity
       +
Merchant volume anomaly
       +
High ML scores
       ↓
Risk Event
```

### Conceptual attributes

A RiskEvent includes:

* Event identifier
* Entity/context
* Creation timestamp
* Severity
* Status
* Triggering signals
* Related transactions

### Relationships

```text
RiskEvent * ───── * Transaction
RiskEvent 1 ───── 0..1 Investigation
RiskEvent 1 ───── * ExposureAssessment
RiskEvent 1 ───── * Recommendation
RiskEvent 1 ───── * FraudOutcome
```

The many-to-many transaction relationship is represented through `RiskEventTransaction`.

---

## 5.7 RiskEventTransaction

### Definition

`RiskEventTransaction` is an association entity connecting transactions to Risk Events.

### Purpose

A Risk Event can contain multiple transactions, and a transaction can participate in multiple Risk Events.

```text
RiskEvent A ──┐
              ├── Transaction X
RiskEvent B ──┘
```

This allows investigations to represent overlapping suspicious patterns without duplicating transactions.

---

# 6. Investigation Domain

The Investigation Domain represents the process of understanding why a risk event occurred and what evidence supports it.

---

## 6.1 Investigation

### Definition

An **Investigation** represents a structured analysis of a Risk Event.

### Purpose

An investigation gathers and interprets relevant information rather than simply repeating the detection result.

It may examine:

* Transactions
* Risk scores
* Risk signals
* Rule evaluations
* Behavioural anomalies
* Device relationships
* Network identities
* Merchant history
* Network intelligence
* Previous risk events

### Relationship

```text
RiskEvent 1 ───── 0..1 Investigation
```

V1 allows one investigation per Risk Event.

This can evolve in a future version if multiple investigation sessions or case workflows become necessary.

---

## 6.2 Evidence

### Definition

An **Evidence** entity represents a specific piece of information considered relevant during an investigation.

Examples:

```text
Observed fact:
"27 transactions originated from Device X."

Model prediction:
"Transaction risk score = 0.94."

Rule result:
"Velocity rule triggered."

Behavioural observation:
"Merchant volume is 2.7× historical baseline."

External signal:
"Network intelligence reports previous suspicious activity."
```

### Purpose

Evidence allows the investigation to distinguish between raw observations and interpretations.

### Relationship

```text
Investigation 1 ───── * Evidence
```

Evidence should preserve enough context to explain where the information came from.

---

## 6.3 NetworkSignal

### Definition

A **NetworkSignal** represents intelligence obtained from the simulated shared fraud-intelligence environment.

In a real payment ecosystem, similar information might come from shared intelligence among financial institutions, processors, card networks, merchants, or other participants.

V1 uses a synthetic implementation.

### Important constraint

Network intelligence must be explicitly identifiable as **simulated**.

A simulated signal must not be presented as real external intelligence.

### Relationship

Network signals may be referenced as investigation evidence.

```text
Investigation 1 ───── * NetworkSignal
```

---

## 6.4 ExposureAssessment

### Definition

An **ExposureAssessment** represents an estimate of the potential financial exposure associated with a Risk Event.

### Example

If an investigation identifies:

```text
Transaction A = ₹10,000
Transaction B = ₹15,000
Transaction C = ₹7,000
```

Potential exposure:

```text
₹32,000
```

### Important distinction

Potential exposure is an estimate.

It does not necessarily represent:

* Actual loss
* Confirmed fraud
* Recoverable amount
* Final financial liability

### Relationship

```text
RiskEvent 1 ───── * ExposureAssessment
```

Multiple assessments can exist if an event is reassessed as additional evidence becomes available.

---

## 6.5 Recommendation

### Definition

A **Recommendation** represents a defensive action proposed by AegisGuard, potentially using AI-generated investigation results.

Examples:

* Continue monitoring
* Escalate for human review
* Require additional verification
* Place merchant under review
* Temporarily restrict selected activity

### Conceptual attributes

A recommendation should include:

* Recommended action
* Reason
* Supporting evidence
* Confidence
* Human-approval requirement
* Creation timestamp

### Critical distinction

```text
Recommendation
      ≠
Action
```

The AI can recommend an action without being authorized to execute it.

### Relationship

```text
RiskEvent 1 ───── * Recommendation
Recommendation 1 ─ 1 PolicyDecision
Recommendation 1 ─ 0..1 HumanDecision
Recommendation 1 ─ 0..1 Action
```

---

# 7. Decision and Response Domain

This domain controls what happens after an investigation produces a recommendation.

---

## 7.1 Policy

### Definition

A **Policy** represents a deterministic control that determines whether a recommended action can be executed automatically, requires human approval, or must be denied.

### Purpose

Policies create a safety boundary around AI-generated recommendations.

### Example

```text
IF
    severity = HIGH
    AND exposure > threshold
    AND action = RESTRICT_MERCHANT

THEN
    HUMAN_APPROVAL_REQUIRED
```

### Relationship

```text
Policy 1 ───── * PolicyDecision
```

---

## 7.2 PolicyDecision

### Definition

A **PolicyDecision** represents the result of evaluating a Recommendation against the applicable policies.

Possible outcomes include:

```text
ALLOW
APPROVAL_REQUIRED
DENY
```

### Relationship

```text
Recommendation 1 ───── 1 PolicyDecision
Policy 1 ────────────── * PolicyDecision
```

The policy decision provides the deterministic authorization boundary between recommendation and action.

---

## 7.3 HumanDecision

### Definition

A **HumanDecision** represents an analyst's decision regarding a recommendation requiring human review.

Possible decisions include:

* Approve
* Reject
* Escalate
* Modify/override where permitted by V1 policy

### Relationship

```text
Recommendation 1 ───── 0..1 HumanDecision
```

Human approval is required only where the applicable policy determines that it is necessary.

---

## 7.4 Action

### Definition

An **Action** represents an actual defensive response executed by the system.

Examples:

* Merchant placed under review
* Selected activity restricted
* Additional verification required
* Monitoring enabled

### Critical distinction

```text
Recommendation
      ↓
Policy Decision
      ↓
Human Decision if required
      ↓
Action
```

The existence of a recommendation does not imply that an action occurred.

### Relationships

```text
Recommendation 1 ───── 0..1 Action
HumanDecision 1 ─────── 0..1 Action
```

V1 actions operate against the simulated payment environment.

---

# 8. Learning Domain

The Learning Domain captures information needed to evaluate and improve fraud-risk models.

---

## 8.1 FraudOutcome

### Definition

A **FraudOutcome** represents information learned after the original payment or risk decision about whether suspicious activity was actually fraudulent or legitimate.

Possible outcome sources include:

* Customer report
* Chargeback
* Manual investigation
* External confirmation
* Legitimate transaction determination
* False-positive determination

### Important property

Fraud outcomes can arrive significantly later than the transaction.

Example:

```text
10:00
Transaction occurs

10:01
Risk score generated

10:02
Risk event created

14:00
Chargeback received

→ Fraud outcome becomes available
```

### Relationships

```text
Transaction 1 ───── * FraudOutcome
RiskEvent 1 ─────── * FraudOutcome
```

The relationship to RiskEvent provides investigation context, while the transaction relationship provides transaction-level outcome information.

---

## 8.2 ModelVersion

### Definition

A **ModelVersion** identifies a specific version of an ML model used for risk scoring.

### Purpose

Every risk prediction must be traceable to the model that produced it.

### Conceptual attributes

A ModelVersion may contain:

* Model identifier
* Version
* Training information
* Creation timestamp
* Evaluation metadata
* Status

### Relationship

```text
ModelVersion 1 ───── * RiskScore
```

This enables comparison of model performance across versions.

---

# 9. Governance Domain

## 9.1 AuditEvent

### Definition

An **AuditEvent** represents a recorded event in the AegisGuard system's operational and decision history.

Examples:

```text
Transaction received
Risk score generated
Rule triggered
Risk event created
Investigation started
Evidence collected
Recommendation generated
Policy evaluated
Human decision recorded
Action executed
Fraud outcome received
```

### Purpose

Audit events allow the system to reconstruct important decisions and actions.

### Relationship

Audit events can reference relevant domain entities.

Conceptually:

```text
Domain Entity
      ↓
AuditEvent
```

A single entity may generate many audit events.

---

# 10. Complete Domain Relationship Map

The primary relationships are:

```text
Customer
   │
   ├─────────────── * Transaction
   │
   └─────────────── * CustomerDevice * ───── Device
                                            │
                                            └──── * Transaction

Merchant
   │
   ├─────────────── * Transaction
   │
   └─────────────── * BehaviouralAnomaly

NetworkIdentity
   │
   └─────────────── * Transaction

Transaction
   │
   ├─────────────── * RiskScore ───────── ModelVersion
   │
   ├─────────────── * RiskSignal
   │
   ├─────────────── * RuleEvaluation ──── RiskRule
   │
   ├─────────────── * FraudOutcome
   │
   └──── * RiskEventTransaction * ─────── RiskEvent
                                             │
                                             ├── 0..1 Investigation
                                             │       │
                                             │       ├── * Evidence
                                             │       │
                                             │       └── * NetworkSignal
                                             │
                                             ├── * ExposureAssessment
                                             │
                                             ├── * Recommendation
                                             │       │
                                             │       └── 1 PolicyDecision ─── Policy
                                             │
                                             └── * FraudOutcome

Recommendation
   │
   ├────────────── 1 PolicyDecision
   │
   ├────────────── 0..1 HumanDecision
   │
   └────────────── 0..1 Action

All significant domain activity
   │
   └────────────── * AuditEvent
```

---

# 11. Entity Responsibility Summary

| Domain Entity        | Primary Responsibility                                 |
| -------------------- | ------------------------------------------------------ |
| Customer             | Represents payment customer                            |
| Merchant             | Represents payment recipient/business                  |
| Transaction          | Represents payment activity                            |
| Device               | Represents device identity                             |
| NetworkIdentity      | Represents network identity                            |
| CustomerDevice       | Connects customers and devices                         |
| RiskScore            | Stores ML risk prediction                              |
| RiskSignal           | Represents individual risk evidence                    |
| RiskRule             | Defines deterministic risk condition                   |
| RuleEvaluation       | Stores rule execution result                           |
| BehaviouralAnomaly   | Represents unusual behavioural deviation               |
| RiskEvent            | Represents correlated suspicious situation             |
| RiskEventTransaction | Connects transactions to risk events                   |
| Investigation        | Represents structured event investigation              |
| Evidence             | Represents information considered during investigation |
| NetworkSignal        | Represents simulated shared intelligence               |
| ExposureAssessment   | Estimates potential financial exposure                 |
| Recommendation       | Proposes defensive response                            |
| Policy               | Defines deterministic action constraints               |
| PolicyDecision       | Determines whether recommendation is authorized        |
| HumanDecision        | Records analyst decision                               |
| Action               | Represents executed defensive response                 |
| FraudOutcome         | Records later information about actual outcome         |
| ModelVersion         | Identifies ML model version                            |
| AuditEvent           | Records system and decision history                    |

---

# 12. Critical Domain Distinctions

The following distinctions are fundamental to AegisGuard.

## 12.1 Risk Score vs Fraud Outcome

```text
RiskScore
= What the model predicted

FraudOutcome
= What was learned later
```

A high risk score does not prove fraud.

---

## 12.2 Risk Signal vs Risk Event

```text
RiskSignal
= Individual evidence

RiskEvent
= Correlated suspicious situation
```

Multiple signals may contribute to one risk event.

---

## 12.3 Anomaly vs Fraud

```text
BehaviouralAnomaly
= Behaviour differs from expected baseline

FraudOutcome
= Later determination about actual outcome
```

An anomaly can be legitimate.

---

## 12.4 Recommendation vs Action

```text
Recommendation
= What AegisGuard proposes

Action
= What AegisGuard actually executes
```

A recommendation must pass through policy controls.

---

## 12.5 AI Interpretation vs Observed Evidence

```text
Evidence
= Information observed or retrieved

AI Interpretation
= Reasoning based on that evidence
```

The system should avoid presenting AI-generated interpretation as if it were raw fact.

---

## 12.6 Transaction Time vs Outcome Time

```text
Transaction time
= Information available for the original decision

Outcome time
= Information learned later
```

Later outcomes must not leak into historical transaction-time features.

---

# 13. Temporal Model

AegisGuard operates across multiple points in time.

At minimum, the domain should distinguish:

```text
occurred_at
created_at
available_at
```

### `occurred_at`

When the underlying event actually occurred.

### `created_at`

When AegisGuard received or persisted the record.

### `available_at`

When information became available for use by the risk system.

These distinctions are especially important for:

* Risk signals
* Fraud outcomes
* Model features
* Investigations
* Audit events

---

# 14. Core Domain Invariants

The following rules must remain true throughout V1.

### Invariant 1 — Prediction is not outcome

A RiskScore must never be treated as a confirmed FraudOutcome.

### Invariant 2 — Anomaly is not fraud

A BehaviouralAnomaly must represent deviation, not confirmation.

### Invariant 3 — AI does not bypass policy

An AI-generated Recommendation cannot directly execute a consequential Action without the required PolicyDecision.

### Invariant 4 — Human approval must be enforceable

If policy requires human approval, the Action must not execute until a valid HumanDecision is recorded.

### Invariant 5 — Later information cannot become historical evidence

Fraud outcomes discovered after a transaction must not be silently treated as information available at transaction time.

### Invariant 6 — Every risk score is traceable

Every RiskScore must identify the ModelVersion that generated it.

### Invariant 7 — Simulated intelligence must remain identifiable

Synthetic network intelligence must never be represented as real external intelligence.

### Invariant 8 — Actions must be distinguishable from recommendations

The presence of a Recommendation does not imply that an Action occurred.

### Invariant 9 — Significant decisions must be auditable

Risk assessment, investigation, recommendation, policy evaluation, human decision, and action execution should produce auditable history.

### Invariant 10 — Component failure must not create uncontrolled actions

Failure of ML, AI, or other components must not allow consequential actions to bypass safety controls.

---

# 15. Domain Boundary

The V1 domain model intentionally does not include:

* Billing
* SaaS subscriptions
* Tenant management
* Enterprise customer management
* Real payment gateway processing
* Real external consortium systems
* Production identity-management infrastructure
* Production compliance workflows
* Commercial case-management functionality

These may belong to future versions if the product scope expands.

---

# 16. V1 vs Future Evolution

The domain model is designed to be extensible without requiring those extensions in V1.

Future versions may introduce additional concepts such as:

* Multiple investigation sessions
* Advanced case management
* Real external intelligence providers
* Real-time feature stores
* Distributed event processing
* Advanced entity relationship modelling
* Multi-tenant boundaries
* Enterprise roles and permissions
* More sophisticated action orchestration

These are future possibilities.

They should not be introduced into V1 unless an actual V1 requirement requires them.

---

# 17. Relationship to Other Design Documents

This document is the conceptual foundation for the persistence and implementation layers.

```text
product-definition.md
        ↓
requirements.md
        ↓
use-cases.md
        ↓
domain-model.md
        ↓
data-model.md
        ↓
data-dictionary.md
        ↓
architecture.md
        ↓
system-flows.md
```

### Upstream dependencies

This document depends primarily on:

* `product-definition.md`
* `requirements.md`
* `use-cases.md`

### Downstream impact

Changes to this document may require updates to:

* `data-model.md`
* `data-dictionary.md`
* `architecture.md`
* `system-flows.md`
* API specifications
* ML design
* Agent design
* Policy engine design
* Testing strategy

---

# 18. Change Management

This is a **living document**.

If a new requirement introduces a new domain concept, the concept should first be evaluated here before being added directly to the database schema or application code.

If an existing entity changes meaning, its relationships and downstream dependencies must be reviewed.

The domain model should remain implementation-independent wherever possible.

---

# 19. Canonical V1 Entity List

The canonical AegisGuard V1 entities are:

```text
PAYMENT
├── Customer
├── Merchant
├── Transaction
├── Device
├── NetworkIdentity
└── CustomerDevice

DETECTION
├── RiskScore
├── RiskSignal
├── RiskRule
├── RuleEvaluation
├── BehaviouralAnomaly
├── RiskEvent
└── RiskEventTransaction

INVESTIGATION
├── Investigation
├── Evidence
├── NetworkSignal
├── ExposureAssessment
└── Recommendation

DECISION / RESPONSE
├── Policy
├── PolicyDecision
├── HumanDecision
└── Action

LEARNING
├── FraudOutcome
└── ModelVersion

GOVERNANCE
└── AuditEvent
```

This is the canonical conceptual domain model for **AegisGuard V1**.
