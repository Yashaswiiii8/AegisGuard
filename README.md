# AegisGuard

> **AI-Assisted Fraud Risk Monitoring, Investigation & Response System**

AegisGuard is a production-minded fraud-risk monitoring and investigation system designed to model how a modern payment platform can detect suspicious activity, investigate correlated risk, estimate potential financial exposure, and recommend defensive actions.

The system combines:

* Machine-learning-based transaction risk scoring
* Deterministic fraud rules
* Behavioural anomaly detection
* Risk-event correlation
* Evidence-based AI investigation
* Financial exposure assessment
* Policy-controlled defensive recommendations
* Human-in-the-loop decision making
* Simulated defensive actions
* Delayed and noisy fraud outcomes
* Model evaluation and feedback
* Complete auditability

AegisGuard is currently being developed as **Version 1 (V1)** using a synthetic payment environment.

---

## 1. Project Objective

Fraud detection is not simply:

```text
Transaction → ML Model → Fraud / Not Fraud
```

Real fraud-risk systems operate as a continuous lifecycle:

```text
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

AegisGuard is designed to reproduce this broader lifecycle in a controlled engineering environment.

The central design principle is:

> **AegisGuard must distinguish between what is known, what is predicted, what is anomalous, what is later confirmed, what is recommended, and what is actually executed.**

---

## 2. Current Version — V1

**Current status: V1 — Design and Development**

V1 is intentionally scoped as a technically serious prototype rather than a production-scale commercial platform.

The objective is to build a coherent end-to-end system while developing practical understanding of:

* Fraud-risk modelling
* Machine learning decisioning
* Class imbalance
* Delayed and noisy labels
* Temporal data leakage
* Behavioural anomaly detection
* Risk-event correlation
* AI-assisted investigation
* Agent tool design
* Policy enforcement
* Human-in-the-loop systems
* Security boundaries
* Auditability
* Model evaluation
* Failure-safe system design

V1 uses synthetic data and simulated external systems where real-world data or infrastructure would normally be proprietary.

### V1 does not attempt to provide

* Production payment processing
* Real financial transactions
* Real consortium fraud intelligence
* Production fraud-prevention guarantees
* Internet-scale event processing
* Enterprise multi-tenancy
* Commercial billing
* Full SaaS functionality
* Production Kubernetes infrastructure
* Microservice decomposition
* High-volume streaming infrastructure

The goal is:

> **Production-minded engineering, not production-scale infrastructure.**

---

## 3. High-Level Architecture

The current V1 logical architecture is:

```text
┌──────────────────────┐
│      React UI        │
│  Analyst Dashboard   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       FastAPI        │
│    Backend / API     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     PostgreSQL       │
│   Domain & Events    │
└──────────┬───────────┘
           │
           ▼
┌─────────────────────────────────┐
│ ML + Rules + Anomaly Detection  │
└──────────┬──────────────────────┘
           │
           ▼
┌──────────────────────┐
│   AI Investigation   │
│        Agent         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Policy Engine     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Defensive Action     │
│  / Human Approval    │
└──────────────────────┘
```

This represents the **logical architecture**, not necessarily a single synchronous request path.

---

## 4. Core System Components

### 4.1 Transaction Risk Assessment

AegisGuard evaluates individual payment transactions using:

* Transaction attributes
* Customer history
* Merchant history
* Device information
* Network information
* Velocity signals
* Deterministic rules
* Other risk intelligence available at decision time

The result is a transaction-level risk score.

---

### 4.2 Rule Engine

Deterministic rules provide explicit risk signals such as:

* Excessive transaction velocity
* Blocklisted entities
* Suspicious geographic patterns
* Unusual transaction characteristics
* Other configurable risk conditions

Rules provide **evidence**, not absolute proof of fraud.

---

### 4.3 Behavioural Anomaly Detection

AegisGuard monitors merchant behaviour over time.

Examples include:

* Transaction volume
* Transaction value
* Average transaction amount
* Failure rate
* Suspicious transaction rate
* Refund/dispute rate
* Device diversity
* Geographic distribution
* Transaction velocity

The system compares observed behaviour against historical baselines.

> **Anomaly does not mean fraud.**

An anomaly is a deviation that may warrant investigation.

---

### 4.4 Risk Events

Individual risk signals are correlated into higher-level **Risk Events**.

A Risk Event may contain:

* Triggering transactions
* ML risk scores
* Rule evaluations
* Behavioural anomalies
* Related devices
* Related network identities
* Merchant history
* Previous risk events
* Network intelligence

This allows AegisGuard to investigate a situation rather than isolated transactions.

---

### 4.5 AI Investigation

The AI agent is responsible for investigation rather than being the primary fraud detector.

The agent can:

1. Retrieve relevant evidence
2. Correlate related activity
3. Examine transaction history
4. Examine merchant behaviour
5. Examine risk signals
6. Query simulated network intelligence
7. Summarize the incident
8. Explain why the event is suspicious
9. Estimate/contextualize exposure
10. Recommend an appropriate next step

The investigation must distinguish:

```text
Observed Fact
      ≠
Model Prediction
      ≠
External Signal
      ≠
AI Interpretation
```

---

### 4.6 Exposure Assessment

For suspicious activity, AegisGuard estimates potential financial exposure.

For example:

```text
Potential Exposure =
Sum of relevant suspicious transaction amounts
```

Exposure is explicitly treated as an **estimate**, not a guaranteed financial loss.

---

### 4.7 Policy Engine

AI recommendations cannot directly bypass system controls.

The decision flow is:

```text
AI Recommendation
       ↓
Policy Engine
       ↓
┌─────────┬────────────┬─────────┐
│  ALLOW  │  APPROVAL  │  DENY   │
└─────────┴────────────┴─────────┘
```

Policies can consider factors such as:

* Risk severity
* Model confidence
* Estimated exposure
* Recommended action
* Merchant status
* Automation limits
* Whether human approval is required

This creates a deterministic control boundary around AI-generated decisions.

---

### 4.8 Human-in-the-Loop

High-impact actions can require analyst approval.

Analysts can:

* Review risk events
* Inspect evidence
* Review AI investigations
* Examine exposure
* Approve recommendations
* Reject recommendations
* Escalate events
* Add notes
* Resolve investigations

---

### 4.9 Defensive Actions

V1 uses a simulated payment environment.

Example actions include:

* Continue monitoring
* Escalate for review
* Require additional verification
* Place a merchant under review
* Temporarily restrict selected activity

No real financial action is performed.

---

### 4.10 Fraud Outcomes

Fraud may only become known after the original transaction.

Possible later outcomes include:

* Customer-reported fraud
* Chargeback
* Manual investigation result
* External confirmation
* Legitimate transaction
* False positive

These outcomes become historical information for future model evaluation and training.

---

## 5. Point-in-Time Correctness

AegisGuard explicitly models the difference between information available during a transaction and information learned later.

For example:

```text
10:00 — Transaction occurs

Available at 10:00:
✓ Device information
✓ IP information
✓ Customer history
✓ Merchant history
✓ Existing risk signals

14:00 — Chargeback occurs

Known only after 14:00:
✗ Chargeback outcome
```

The 14:00 chargeback cannot be used as a feature for the 10:00 risk decision.

This prevents **temporal/data leakage**.

Risk signals therefore carry temporal semantics such as:

```text
occurred_at
created_at
available_at
```

---

## 6. Synthetic Fraud Environment

Because real payment and fraud datasets are proprietary, V1 uses synthetic data.

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
* Merchant behaviour changes
* Delayed fraud outcomes
* Noisy labels
* Simulated shared fraud intelligence

The purpose is not to claim real-world fraud-detection accuracy.

The purpose is to reproduce the **engineering and ML problems** encountered in real fraud-risk systems.

---

## 7. Technology Stack

### Frontend

* React
* JavaScript / TypeScript
* Analyst dashboard

### Backend

* Python
* FastAPI
* SQLAlchemy 2.x
* Alembic

### Database

* PostgreSQL

PostgreSQL is the primary V1 datastore because the domain contains:

* Strong relationships
* Foreign-key constraints
* Transactional state
* Aggregations
* Historical records
* Audit data
* Flexible risk metadata

Financial values will use integer minor units rather than floating-point monetary values:

```text
amount_minor BIGINT
currency     CHAR(3)
```

---

### Machine Learning

The ML layer will support:

* Transaction risk scoring
* Model evaluation
* Model versioning
* Historical outcome-based learning
* Class-imbalance handling
* Temporal evaluation

Candidate models can evolve during implementation based on the characteristics of the generated dataset.

---

### AI Investigation

The AI investigation layer will operate as a bounded agent.

The agent will interact with AegisGuard through controlled tools rather than having unrestricted access to the system.

---

## 8. Core Domain Entities

The V1 domain is organized into the following areas.

### Payment

* Customer
* Merchant
* Transaction
* Device
* NetworkIdentity
* CustomerDevice

### Detection

* RiskScore
* RiskSignal
* RiskRule
* RuleEvaluation
* BehaviouralAnomaly
* RiskEvent
* RiskEventTransaction

### Investigation

* Investigation
* Evidence
* NetworkSignal
* ExposureAssessment
* Recommendation

### Decision / Response

* Policy
* PolicyDecision
* HumanDecision
* Action

### Learning

* FraudOutcome
* ModelVersion

### Governance

* AuditEvent

The domain model is relationally implemented in PostgreSQL.

Although the domain is naturally graph-shaped — for example:

```text
Customer
   ↓
Device
   ↓
Transaction
   ↓
Merchant
   ↓
Network Identity
```

V1 does **not** require a graph database.

PostgreSQL relationships and junction tables are sufficient for the current scope.

---

## 9. Fraud-Risk Lifecycle

The complete V1 lifecycle is:

```text
                    ┌──────────────────┐
                    │ Payment Activity │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Risk Assessment │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │   Risk Event     │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │  Investigation   │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Exposure         │
                    │ Assessment       │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Recommendation   │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Policy Decision  │
                    └────────┬─────────┘
                             ↓
                  ┌──────────┴──────────┐
                  ↓                     ↓
           Human Approval         Automatic Action
                  │                     │
                  └──────────┬──────────┘
                             ↓
                    ┌──────────────────┐
                    │   Audit Trail    │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Later Outcome    │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Evaluation /     │
                    │ Future Learning  │
                    └──────────────────┘
```

This feedback loop is fundamental to AegisGuard.

---

## 10. Failure-Safe Behaviour

AegisGuard must fail safely.

Examples:

### ML unavailable

```text
ML unavailable
      ↓
Fallback to deterministic signals/rules
      ↓
Escalate if necessary
```

### AI investigation unavailable

```text
AI unavailable
      ↓
Risk Event remains open
      ↓
Human investigation remains possible
```

### Policy engine unavailable

Consequential actions must not bypass policy controls.

The system should prefer:

> **No uncontrolled high-impact action over an unsafe automatic action.**

---

## 11. Auditability

AegisGuard maintains an audit trail covering significant system events.

The system should make it possible to determine:

* What happened
* When it happened
* Which signals were present
* Which rules triggered
* What the ML model predicted
* Which model version was used
* Which anomaly was detected
* Which evidence was considered
* What the AI investigation concluded
* What exposure was estimated
* What recommendation was generated
* Which policy was evaluated
* Whether human approval was required
* What decision was made
* What action was executed
* What happened later

Auditability is a core system property rather than an optional logging feature.

---

## 12. Repository Structure

```text
AegisGuard/
│
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── docs/
│   ├── product-definition.md
│   ├── requirements.md
│   ├── use-cases.md
│   ├── domain-model.md
│   ├── data-model.md
│   ├── data-dictionary.md
│   ├── architecture.md
│   └── system-flows.md
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── db/
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── ml/
│   ├── models/
│   ├── training/
│   ├── inference/
│   └── ...
│
└── scripts/
```

The repository structure may evolve as implementation progresses.

---

## 13. Development Philosophy

AegisGuard is being developed incrementally.

The development process is:

```text
Design Foundation
       ↓
Minimum Project Skeleton
       ↓
Implement One Vertical Slice
       ↓
Understand & Validate
       ↓
Document What Was Learned
       ↓
Implement Next Slice
       ↓
Test & Refine
```

The project should avoid premature infrastructure complexity.

V1 prioritizes:

1. Correct domain modelling
2. Clear system boundaries
3. Explainable decisions
4. Point-in-time correctness
5. Safe AI integration
6. Strong data modelling
7. Testability
8. Auditability
9. Measured ML performance
10. Maintainable implementation

---

## 14. V1 Scope Boundaries

The following technologies and architectural patterns are intentionally **not required for V1**:

* Kafka
* Kubernetes
* Redis
* Graph databases
* Vector databases
* Microservice architecture
* Large-scale distributed processing
* Enterprise multi-tenancy
* Billing infrastructure
* Production payment gateways
* Real consortium integrations

These technologies may become appropriate if a future version introduces requirements that justify them.

The rule is:

> **Introduce infrastructure because the system requires it, not because the technology is available.**

---

## 15. Documentation

The `docs/` directory contains the living design documentation for AegisGuard.

Current design foundation:

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

Each document acts as a source of truth for its specific design concern and should be updated when upstream decisions change.

Implementation-specific documentation will be added as the corresponding development stages are reached.

---

## 16. Project Status

### Current Phase

**V1 — Design Foundation → Development**

### Completed / Defined

* Product concept
* V1 scope
* Core requirements
* Primary use cases
* High-level architecture
* PostgreSQL-based persistence strategy
* Core domain entities
* Fraud-risk lifecycle
* AI investigation concept
* Policy and human-approval model
* Auditability requirements
* Synthetic fraud environment

### Current Next Steps

1. Finalize domain model
2. Finalize relational data model
3. Define data dictionary
4. Finalize system architecture
5. Define system flows
6. Create minimum project skeleton
7. Implement the first vertical slice
8. Build synthetic payment data
9. Implement initial risk scoring
10. Incrementally add investigation and response capabilities

---

# 17. Future Evolution — V2 and V3

AegisGuard is intentionally designed so that **V1 can become the foundation for larger future versions**.

The immediate objective is **not** to build a fully scalable commercial product.

Future versions may evolve AegisGuard toward:

### V2 — Scalable Platform

Potential additions could include:

* High-volume event streaming
* Distributed processing
* Real-time feature computation
* Advanced model serving
* Redis or equivalent low-latency infrastructure
* Kafka or equivalent event streaming
* Stronger observability
* More sophisticated agent orchestration
* Larger-scale relationship analysis
* More advanced model monitoring
* Expanded integrations

### V3 — Full Product

A future V3 could potentially evolve AegisGuard into a complete scalable fraud-risk platform with capabilities such as:

* Multi-tenant architecture
* Production payment integrations
* External fraud-intelligence integrations
* Enterprise access control
* Advanced case management
* Customer/merchant-facing workflows
* Production-grade deployment infrastructure
* Large-scale distributed architecture
* Enterprise security and compliance
* Commercial SaaS capabilities
* Extensive APIs and integration tooling

These are **future possibilities, not current V1 requirements**.

The current objective remains:

> **Build V1 correctly, understand the underlying systems deeply, and establish a strong technical foundation that can support V2 and V3 when the requirements justify them.**

---

## 18. Final V1 Principle

AegisGuard V1 is not trying to simulate an entire global payment network.

It is trying to demonstrate that a modern fraud-risk system can be designed as a complete lifecycle:

```text
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

**That lifecycle is the core of AegisGuard.**
