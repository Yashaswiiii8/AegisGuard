# AegisGuard Product Definition

> **AI-Assisted Fraud Risk Monitoring, Investigation & Response System**

---

## 1. Document Status

**Status:** Living
**Version:** 1.0
**Current Product Version:** V1
**Document Type:** Product Definition

### Purpose

This document defines what AegisGuard is, the problem it addresses, its intended capabilities, its boundaries, and the direction in which the system may evolve.

This document describes the **product concept and scope**.

It does not define implementation details such as database schemas, API contracts, ML algorithms, or frontend architecture.

---

# 2. Product Overview

AegisGuard is an intelligent fraud-risk monitoring and investigation system designed to help a payment platform identify suspicious activity, understand the broader context surrounding that activity, estimate potential financial exposure, and recommend appropriate defensive responses.

The system combines:

* Machine learning
* Deterministic risk rules
* Behavioural anomaly detection
* Risk-event correlation
* AI-assisted investigation
* Evidence aggregation
* Financial exposure assessment
* Policy-controlled recommendations
* Human-in-the-loop decision making
* Simulated defensive actions
* Delayed fraud outcomes
* Model evaluation
* Complete auditability

The core idea is that fraud-risk management is not a single prediction problem.

It is a lifecycle:

```text id="8f0f6g"
Payment Activity
      ↓
Risk Assessment
      ↓
Risk Event
      ↓
Investigation
      ↓
Exposure Assessment
      ↓
Recommendation
      ↓
Policy / Human Decision
      ↓
Defensive Action
      ↓
Audit Trail
      ↓
Later Fraud Outcome
      ↓
Future Evaluation / Learning
```

---

# 3. Problem Statement

Traditional simplified fraud-detection systems are often represented as:

```text id="0z8zcc"
Transaction
    ↓
Fraud Model
    ↓
Fraud / Not Fraud
```

This representation does not capture the broader operational problem.

In a realistic payment environment:

* Individual transactions may contain ambiguous signals.
* Fraud patterns may only become visible across multiple transactions.
* Merchants may change behaviour over time.
* Device and network identities may connect otherwise unrelated activity.
* ML predictions are probabilistic.
* Rules may produce false positives.
* Behavioural anomalies may be legitimate.
* Fraud may only be confirmed hours or days later.
* Investigation requires combining multiple sources of evidence.
* Defensive actions may have financial or operational consequences.
* AI-generated recommendations require safety controls.
* Analysts need to understand why the system reached a decision.
* Historical outcomes are necessary to evaluate and improve the detection system.

AegisGuard addresses this broader problem by modelling fraud risk as a continuous decision and investigation lifecycle rather than as a single classification task.

---

# 4. Product Objective

The primary objective of AegisGuard V1 is to demonstrate a complete fraud-risk lifecycle in a controlled synthetic payment environment.

The system should be able to:

1. Receive synthetic payment activity.
2. Assess transaction-level risk.
3. Apply deterministic risk rules.
4. Detect unusual merchant behaviour.
5. Correlate suspicious activity into Risk Events.
6. Investigate Risk Events using structured evidence.
7. Use an AI agent to assist with investigation.
8. Estimate potential financial exposure.
9. Generate defensive recommendations.
10. Evaluate recommendations against deterministic policies.
11. Escalate high-impact decisions to human analysts where required.
12. Execute simulated defensive actions.
13. Record a complete audit trail.
14. Receive later fraud outcomes.
15. Use those outcomes for future evaluation and learning.

---

# 5. Core Product Principle

AegisGuard must maintain clear boundaries between different types of information and decisions.

```text id="m0e6wp"
Observed Activity
       ↓
Risk Signal
       ↓
Model Prediction / Rule Result / Anomaly
       ↓
Risk Event
       ↓
Investigation
       ↓
AI Interpretation
       ↓
Recommendation
       ↓
Policy Decision
       ↓
Human Decision if Required
       ↓
Action
       ↓
Later Outcome
```

The following distinctions are fundamental:

```text id="g9n4ob"
Prediction       ≠ Confirmation

Anomaly          ≠ Fraud

Evidence         ≠ Interpretation

Recommendation   ≠ Action

Transaction Time ≠ Outcome Time
```

These distinctions must remain explicit throughout the system.

---

# 6. Target Users

The primary V1 user is a **fraud/risk analyst**.

The analyst uses AegisGuard to:

* Monitor suspicious activity
* Review Risk Events
* Understand why an event was flagged
* Inspect supporting evidence
* Examine related transactions
* Examine merchant behaviour
* Review network intelligence
* Review AI-generated investigation results
* Understand potential exposure
* Review recommendations
* Approve or reject actions where required
* Record investigation decisions
* Review historical outcomes

V1 focuses on the analyst workflow rather than providing a complete commercial customer-facing product.

---

# 7. Core Product Capabilities

## 7.1 Transaction Risk Assessment

AegisGuard evaluates individual payment transactions.

The assessment may consider:

* Transaction characteristics
* Customer history
* Merchant history
* Device information
* Network information
* Transaction velocity
* Deterministic rules
* Other risk intelligence available at decision time

The output is a transaction-level risk score.

---

## 7.2 Deterministic Risk Rules

AegisGuard uses explicit rules to identify known risk conditions.

Examples include:

* Excessive transaction velocity
* Blocklisted entities
* Suspicious geographic patterns
* Unusual transaction behaviour
* Repeated failures
* Other configurable risk conditions

Rules provide explainable signals.

They do not constitute definitive proof of fraud.

---

## 7.3 Behavioural Anomaly Detection

AegisGuard monitors merchant behaviour over time.

Potential behavioural metrics include:

* Transaction volume
* Transaction value
* Average transaction amount
* Failure rate
* Suspicious transaction rate
* Refund/dispute rate
* Device diversity
* Geographic distribution
* Transaction velocity

The system compares current behaviour with historical baselines.

An anomaly indicates unusual behaviour, not confirmed fraud.

---

## 7.4 Risk Event Generation

AegisGuard combines related signals and suspicious activity into higher-level Risk Events.

A Risk Event may contain:

* Multiple suspicious transactions
* High ML risk scores
* Triggered rules
* Behavioural anomalies
* Related devices
* Related network identities
* Merchant history
* Previous risk events
* Network intelligence

This allows the system to investigate patterns rather than isolated transactions.

---

## 7.5 AI-Assisted Investigation

The AI agent assists analysts in investigating Risk Events.

The agent can:

* Retrieve relevant evidence
* Correlate related activity
* Examine transaction history
* Examine merchant behaviour
* Examine device relationships
* Examine network information
* Query simulated network intelligence
* Summarize the incident
* Explain why the activity appears suspicious
* Identify relevant patterns
* Estimate/contextualize exposure
* Recommend a defensive response

The AI agent is **not the primary fraud detector**.

Detection is performed through the combination of ML, rules, and anomaly detection.

The agent primarily performs investigation and reasoning over available evidence.

---

## 7.6 Exposure Assessment

AegisGuard estimates the potential financial exposure associated with a Risk Event.

For example:

```text id="7d9yyo"
Suspicious Transaction A = ₹10,000
Suspicious Transaction B = ₹15,000
Suspicious Transaction C = ₹7,000

Potential Exposure = ₹32,000
```

The value is an estimate.

It must not be presented as confirmed financial loss.

---

## 7.7 Defensive Recommendations

AegisGuard may recommend responses such as:

* Continue monitoring
* Escalate for review
* Require additional verification
* Place a merchant under review
* Temporarily restrict selected activity

Recommendations contain supporting reasoning and evidence.

The system distinguishes:

```text id="qf1jsf"
What AegisGuard recommends
```

from:

```text id="e8b6ko"
What the system actually executes
```

---

## 7.8 Policy-Controlled Decisions

AI recommendations are subject to deterministic policy controls.

The decision flow is:

```text id="2z4y2w"
AI Recommendation
       ↓
Policy Engine
       ↓
ALLOW / APPROVAL REQUIRED / DENY
```

Policies may consider:

* Risk severity
* Model confidence
* Estimated exposure
* Action type
* Merchant status
* Automation limits
* Required human approval

The AI agent must not bypass these controls.

---

## 7.9 Human-in-the-Loop

Where policy requires human approval, the analyst reviews the recommendation before execution.

The analyst may:

* Approve
* Reject
* Escalate
* Add notes
* Resolve the Risk Event

High-impact actions should not occur merely because an AI agent recommended them.

---

## 7.10 Defensive Actions

V1 operates against a simulated payment environment.

Potential simulated actions include:

* Merchant under review
* Additional verification
* Selected activity restriction
* Increased monitoring

No real payment or financial action is performed.

---

## 7.11 Fraud Outcomes

Fraud may be confirmed only after the original transaction.

Possible later outcomes include:

* Customer-reported fraud
* Chargeback
* Manual investigation
* External confirmation
* Legitimate transaction
* False positive

These outcomes provide historical information for model evaluation and future learning.

---

# 8. Synthetic Payment Environment

AegisGuard V1 uses synthetic data.

The environment models:

* Customers
* Merchants
* Transactions
* Devices
* Network identities
* Normal behaviour
* Fraudulent behaviour
* Risk signals
* Suspicious activity
* Merchant behavioural changes
* Delayed outcomes
* Noisy labels
* Simulated shared fraud intelligence

The purpose of the synthetic environment is to reproduce the technical and ML challenges of a fraud-risk system.

It is not intended to represent a real payment network or provide evidence of production fraud-detection performance.

---

# 9. Shared Fraud Intelligence

Real payment ecosystems may use shared intelligence from:

* Banks
* Payment processors
* Card networks
* Merchants
* Fraud-prevention providers
* Other financial institutions

Such information is generally proprietary or subject to controlled access.

AegisGuard V1 therefore uses a **simulated shared fraud-intelligence registry**.

The system must clearly identify this intelligence as simulated.

It must never imply that synthetic intelligence represents real external fraud data.

---

# 10. Point-in-Time Correctness

AegisGuard must respect what was known at the time of a decision.

For example:

```text id="7ynb8u"
10:00
Transaction occurs

Available at 10:00:
✓ Device information
✓ IP information
✓ Customer history
✓ Merchant history
✓ Existing risk signals

14:00
Chargeback received

Known only after 14:00:
✗ Chargeback outcome
```

The chargeback cannot be used as a transaction-time feature for the 10:00 risk decision.

This prevents temporal/data leakage.

The system therefore distinguishes between:

```text id="ph2jcn"
When something occurred
When AegisGuard recorded it
When information became available
```

---

# 11. Feedback Loop

AegisGuard is designed around a continuous feedback loop.

```text id="x24e6c"
Detect
  ↓
Investigate
  ↓
Act
  ↓
Observe Outcome
  ↓
Evaluate Detection
  ↓
Improve Models / Rules
  ↓
Detect Again
```

Later fraud outcomes become valuable historical labels.

This enables analysis of:

* True positives
* False positives
* False negatives
* Model performance
* Rule performance
* Behavioural detection performance
* Model drift
* Changing fraud patterns

---

# 12. AI Safety Model

AI is treated as a bounded system component rather than an unrestricted decision maker.

The intended responsibility separation is:

```text id="4h7t0n"
ML / Rules / Anomaly Detection
        ↓
      Detect
        ↓
AI Agent
        ↓
    Investigate
        ↓
AI Recommendation
        ↓
 Policy Engine
        ↓
Human Approval if required
        ↓
      Action
```

The AI agent should not:

* Directly modify arbitrary database records
* Bypass policy controls
* Execute unrestricted consequential actions
* Treat its own interpretation as confirmed truth
* Invent evidence
* Represent simulated intelligence as real intelligence

---

# 13. Auditability

AegisGuard should provide enough historical information to reconstruct significant risk decisions.

The system should be able to answer:

* What happened?
* When did it happen?
* Which signals were present?
* Which rules triggered?
* What did the ML model predict?
* Which model version produced the prediction?
* What anomaly was detected?
* What evidence was considered?
* What did the investigation conclude?
* What exposure was estimated?
* What did the AI recommend?
* Which policy was evaluated?
* Was human approval required?
* What decision was made?
* What action was taken?
* What happened later?

Auditability is a core product capability.

---

# 14. Reliability and Failure Behaviour

AegisGuard should fail safely.

### ML unavailable

The system should fall back to available deterministic signals/rules or escalate appropriately.

### AI investigation unavailable

The Risk Event should remain available for human investigation.

### Policy engine unavailable

The system must not bypass policy controls to execute consequential actions.

The guiding principle is:

> **A component failure must not create uncontrolled high-impact behaviour.**

---

# 15. V1 Scope

AegisGuard V1 is intentionally bounded.

### Included

* Synthetic payment environment
* Transaction risk scoring
* Deterministic rules
* Merchant behavioural monitoring
* Anomaly detection
* Risk-event generation
* Evidence correlation
* AI-assisted investigation
* Simulated network intelligence
* Exposure assessment
* Defensive recommendations
* Policy enforcement
* Human approval
* Simulated defensive actions
* Delayed/noisy fraud outcomes
* Model versioning
* Auditability
* ML evaluation

### Not included in V1

* Real payment processing
* Real financial transactions
* Real consortium integrations
* Production fraud-prevention guarantees
* Internet-scale infrastructure
* Commercial SaaS functionality
* Multi-tenant enterprise architecture
* Billing
* Enterprise identity infrastructure
* Production compliance systems
* Large-scale distributed streaming
* Microservice decomposition
* Kubernetes infrastructure
* Graph databases
* Vector databases
* Redis-based infrastructure unless a measured V1 requirement emerges

---

# 16. V1 Engineering Philosophy

V1 follows the principle:

> **Production-minded, not production-scale.**

The project should demonstrate serious engineering practices without prematurely reproducing the infrastructure of a global payment platform.

Priority is given to:

1. Correct domain modelling
2. Point-in-time correctness
3. Explainable risk decisions
4. Safe AI integration
5. Strong data integrity
6. Auditability
7. Testability
8. Reproducibility
9. Measured ML performance
10. Maintainable architecture

Infrastructure complexity should only be introduced when justified by an actual requirement.

---

# 17. High-Level Technology Direction

The current V1 technology direction is:

```text id="lq4h4m"
Frontend
React

Backend
FastAPI / Python

Persistence
PostgreSQL

ORM
SQLAlchemy 2.x

Migrations
Alembic

ML
Python ML ecosystem

AI Investigation
Bounded AI agent with controlled tools
```

The exact implementation details are defined in downstream technical documentation.

---

# 18. Future Product Evolution

V1 is the current implementation target.

AegisGuard is intentionally designed so that future versions can evolve beyond the current prototype.

## V2 — Scalable Platform

A future V2 could introduce capabilities such as:

* High-volume event ingestion
* Real-time processing
* Distributed workloads
* Advanced feature computation
* Dedicated model serving
* Expanded observability
* More sophisticated agent orchestration
* Larger-scale relationship analysis
* Advanced model monitoring
* External integrations

Technologies such as event streaming, caching, distributed processing, or specialized data stores may become appropriate if justified by future requirements.

## V3 — Full-Scale Product

A future V3 could potentially evolve AegisGuard into a full scalable fraud-risk product with capabilities such as:

* Multi-tenancy
* Production payment integrations
* Real external fraud-intelligence integrations
* Enterprise access control
* Advanced case management
* Enterprise security and compliance
* Production deployment infrastructure
* Large-scale distributed architecture
* Customer-facing workflows
* Commercial SaaS functionality
* Extensive integration APIs

These versions are **future possibilities, not current requirements**.

The immediate objective is to build V1 correctly and establish a strong technical foundation.

---

# 19. Product Success Criteria for V1

AegisGuard V1 should successfully demonstrate that the system can:

```text id="j5xq0a"
Receive payment activity
        ↓
Assess risk
        ↓
Detect suspicious behaviour
        ↓
Correlate evidence
        ↓
Create a Risk Event
        ↓
Investigate it
        ↓
Estimate exposure
        ↓
Generate a recommendation
        ↓
Apply policy controls
        ↓
Obtain human approval when required
        ↓
Execute a simulated action
        ↓
Record the complete history
        ↓
Receive a later outcome
        ↓
Evaluate the original decision
```

A successful V1 is therefore not defined simply by the accuracy of a fraud classifier.

It is defined by demonstrating a coherent, explainable, auditable, and safe fraud-risk lifecycle.

---

# 20. Relationship to Other Documents

This document is the highest-level product definition for AegisGuard V1.

Downstream design documents derive their scope and assumptions from this document.

The current documentation hierarchy is:

```text id="5jz5px"
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

Changes to product scope should begin here and then propagate to affected downstream documents.

---

# 21. Change Management

This is a living document.

If a major feature, boundary, user, or product objective changes:

1. Update this document.
2. Review `requirements.md`.
3. Review affected use cases.
4. Review the domain model.
5. Review the data model.
6. Review architecture and system flows.
7. Review implementation plans and tests.

New infrastructure should not be introduced solely because it is technically interesting.

It should be introduced because a documented requirement justifies it.

---

# 22. Canonical Product Definition

For V1:

> **AegisGuard is an AI-assisted fraud-risk monitoring, investigation, and response system that combines ML risk scoring, deterministic rules, behavioural anomaly detection, evidence correlation, bounded AI investigation, exposure assessment, policy-controlled recommendations, human decision making, simulated defensive actions, delayed fraud outcomes, and complete auditability within a synthetic payment environment.**

**V1 is the current implementation target.**

**V2 and V3 are future evolution paths toward a scalable platform and full product, respectively, and are not part of the current implementation scope.**
