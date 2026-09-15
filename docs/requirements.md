# AegisGuard Requirements

> **Canonical functional and non-functional requirements for AegisGuard V1.**

---

## 1. Document Status

**Status:** Living
**Version:** 1.0
**Scope:** AegisGuard V1
**Document Type:** System Requirements

### Purpose

This document defines what AegisGuard V1 must do and the properties it must satisfy.

It translates the product definition into explicit, testable requirements.

This document defines **system behaviour and constraints**, not implementation details.

Implementation choices must remain consistent with these requirements.

---

# 2. Requirement ID Convention

Requirements are uniquely identified using:

```text
FR-XX    Functional Requirement
ML-XX    Machine Learning Requirement
SEC-XX   Security Requirement
AUD-XX   Auditability Requirement
REL-XX   Reliability Requirement
NFR-XX   Other Non-Functional Requirement
```

---

# 3. System Scope

AegisGuard V1 shall provide an end-to-end fraud-risk lifecycle:

```text
Payment Activity
      ↓
Risk Assessment
      ↓
Detection
      ↓
Risk Event
      ↓
Investigation
      ↓
Exposure Assessment
      ↓
Recommendation
      ↓
Policy Decision
      ↓
Human Decision if Required
      ↓
Defensive Action
      ↓
Audit Trail
      ↓
Later Fraud Outcome
      ↓
Evaluation / Learning
```

The system shall operate against a synthetic payment environment.

---

# 4. Functional Requirements

## FR-01 — Ingest Payment Events

AegisGuard shall ingest payment transaction events containing sufficient information for risk assessment.

A transaction shall support, where applicable:

* Transaction ID
* Customer ID
* Merchant ID
* Amount
* Currency
* Timestamp
* Payment method
* Device ID
* Network identity
* Geographic information
* Transaction status

The system shall validate incoming transaction data before persistence and risk processing.

---

## FR-02 — Ingest Supporting Risk Signals

AegisGuard shall support risk intelligence associated with payment activity.

Risk signals may originate from:

* Device intelligence
* IP/network intelligence
* Customer history
* Merchant history
* Existing risk rules
* Blocklists
* Related entities
* Simulated shared fraud intelligence

Each relevant signal shall preserve sufficient information to determine:

* What the signal represents
* Its source
* When it was generated
* When it became available
* What entity or transaction it relates to

---

## FR-03 — Preserve Point-in-Time Information

AegisGuard shall ensure that transaction-time risk decisions use only information that was legitimately available at the time of the decision.

The system shall distinguish between:

```text
When an event occurred
When the system recorded it
When information became available
```

Later information, including confirmed fraud outcomes, shall not be silently used as a feature for an earlier transaction-time decision.

---

## FR-04 — Assess Transaction Risk

AegisGuard shall perform transaction-level risk assessment.

The assessment may use:

* Transaction attributes
* Customer history
* Merchant history
* Device information
* Network information
* Risk signals
* Rule results
* ML predictions

The resulting assessment shall be traceable to the information and model version used.

---

## FR-05 — Generate Transaction Risk Scores

AegisGuard shall generate a machine-learning-based risk score for transactions where the ML component is available.

The score shall represent the model's estimated risk.

For probability-based models, the score shall be represented on a normalized range such as:

```text
0.0 → 1.0
```

The system shall store:

* Score
* Transaction
* Model version
* Scoring timestamp
* Relevant scoring metadata

A risk score shall not be treated as confirmed fraud.

---

## FR-06 — Evaluate Deterministic Risk Rules

AegisGuard shall support deterministic risk rules.

Rules may evaluate conditions such as:

* Transaction velocity
* Geographic patterns
* Blocklists
* Repeated failures
* Other configurable risk conditions

The system shall record rule evaluations and whether individual rules triggered.

A rule result shall be treated as a risk signal rather than definitive proof of fraud.

---

## FR-07 — Monitor Merchant Behaviour

AegisGuard shall monitor merchant-level behavioural metrics over time.

Metrics may include:

* Transaction volume
* Transaction value
* Average transaction amount
* Failure rate
* Suspicious transaction rate
* Refund/dispute rate
* Device diversity
* Geographic distribution
* Transaction velocity

The system shall maintain or derive historical baselines against which current behaviour can be evaluated.

---

## FR-08 — Detect Behavioural Anomalies

AegisGuard shall detect significant deviations from expected merchant behaviour.

An anomaly shall preserve:

* Merchant/entity
* Metric
* Historical baseline
* Observed value
* Deviation
* Detection method
* Detection timestamp

An anomaly shall not automatically be classified as fraud.

---

## FR-09 — Generate Risk Events

AegisGuard shall create higher-level Risk Events when related suspicious activity warrants investigation.

A Risk Event shall support:

* Unique event ID
* Related entity/context
* Severity
* Status
* Creation timestamp
* Triggering signals
* Related transactions

A Risk Event shall represent a correlated situation rather than merely duplicating an individual risk signal.

---

## FR-10 — Correlate Related Evidence

AegisGuard shall support correlation of related activity.

Correlation may include:

* Suspicious transactions
* Shared devices
* Shared network identities
* Unusual transaction amounts
* Merchant anomalies
* Previous risk events
* Risk scores
* Rule evaluations
* Other relevant signals

The purpose is to identify patterns that may not be visible from an individual transaction.

---

## FR-11 — Query Shared Fraud Intelligence

AegisGuard shall support querying a simulated shared fraud-intelligence source.

The system may use this source to identify previously observed suspicious entities or activity.

The system shall clearly identify this intelligence as simulated.

AegisGuard shall not represent synthetic intelligence as real external intelligence.

---

## FR-12 — Investigate Risk Events

AegisGuard shall provide structured investigation of Risk Events.

An investigation shall be capable of gathering:

* Related transactions
* Risk scores
* Rule evaluations
* Risk signals
* Behavioural anomalies
* Device relationships
* Network identities
* Merchant history
* Previous risk activity
* Simulated network intelligence

The investigation shall produce a structured result that can be reviewed by an analyst.

---

## FR-13 — Provide Evidence-Based Explanation

AegisGuard shall provide an explanation of why a Risk Event was considered suspicious.

The explanation shall distinguish between:

```text
Observed facts
Model predictions
Rule results
External/simulated signals
AI interpretation
```

AI-generated reasoning shall not be presented as an observed fact.

---

## FR-14 — Estimate Potential Financial Exposure

AegisGuard shall estimate potential financial exposure associated with a Risk Event.

The system shall be able to calculate exposure from relevant suspicious transactions.

Exposure estimates shall include:

* Estimated amount
* Currency
* Calculation method
* Assessment timestamp

The system shall explicitly treat exposure as an estimate rather than confirmed financial loss.

---

## FR-15 — Generate Defensive Recommendations

AegisGuard shall generate defensive recommendations based on investigation results.

Possible recommendations include:

* Continue monitoring
* Escalate
* Require additional verification
* Place merchant under review
* Temporarily restrict selected activity

Each recommendation shall contain, where applicable:

* Proposed action
* Reason
* Supporting evidence
* Confidence
* Human-approval requirement
* Creation timestamp

A recommendation shall not itself execute an action.

---

## FR-16 — Evaluate Recommendations Against Policy

AegisGuard shall evaluate recommendations through a deterministic Policy Engine.

The Policy Engine shall be capable of producing:

```text
ALLOW
APPROVAL_REQUIRED
DENY
```

Policy evaluation may consider:

* Risk severity
* Model confidence
* Estimated exposure
* Action type
* Merchant status
* Automation limits
* Human-approval requirements

AI-generated recommendations shall not bypass the Policy Engine.

---

## FR-17 — Support Human-in-the-Loop Decisions

AegisGuard shall support analyst review for actions requiring human approval.

The analyst shall be able to:

* Review the Risk Event
* Inspect supporting evidence
* Review the investigation
* Review exposure
* Review the recommendation
* Approve a recommendation
* Reject a recommendation
* Escalate the event
* Add investigation notes

A high-impact action requiring approval shall not execute without the required human decision.

---

## FR-18 — Execute Defensive Actions

AegisGuard shall support execution of approved defensive actions against the simulated payment environment.

Possible actions include:

* Place merchant under review
* Require additional verification
* Restrict selected activity
* Increase monitoring

V1 shall not execute real financial actions.

An executed Action shall be distinguishable from a Recommendation.

---

## FR-19 — Record Fraud Outcomes

AegisGuard shall support recording outcomes that become known after the original payment activity.

Possible outcomes include:

* Confirmed fraud
* Customer-reported fraud
* Chargeback
* Manual investigation result
* External confirmation
* Legitimate transaction
* False positive

The system shall preserve the source and timing of the outcome.

---

## FR-20 — Handle Delayed and Noisy Labels

AegisGuard shall support the reality that fraud labels may:

* Arrive later
* Be incomplete
* Be uncertain
* Conflict across sources
* Contain false positives
* Contain false negatives

The system shall not assume that every transaction has an immediate and perfectly accurate fraud label.

---

## FR-21 — Build Historical Training and Evaluation Data

AegisGuard shall support using reliable later fraud outcomes as historical labels for ML evaluation and future training.

The system shall preserve the distinction between:

```text
Features available at decision time
```

and:

```text
Labels learned after the decision
```

Historical dataset construction shall prevent future information from leaking into past features.

---

## FR-22 — Version ML Models

AegisGuard shall version ML models used for transaction risk scoring.

Each risk score shall be traceable to the model version that produced it.

Model metadata should include, where applicable:

* Model name
* Version
* Training timestamp
* Evaluation information
* Status
* Relevant metadata

---

## FR-23 — Maintain Complete Risk Audit Trail

AegisGuard shall record significant events throughout the fraud-risk lifecycle.

Auditable events shall include, where applicable:

* Transaction received
* Risk assessment performed
* Risk score generated
* Rule evaluated
* Rule triggered
* Anomaly detected
* Risk Event created
* Investigation started
* Evidence collected
* Recommendation generated
* Policy evaluated
* Human decision recorded
* Action executed
* Fraud outcome received

The audit trail shall support reconstruction of important decisions.

---

## FR-24 — Provide Analyst Risk Event View

The analyst interface shall allow an analyst to move from a Risk Event to its supporting context.

The conceptual investigation view should contain:

```text
Risk Event
    ↓
Why Flagged
    ↓
Risk Signals
    ↓
Transactions
    ↓
Related Entities
    ↓
Merchant Behaviour
    ↓
Network Intelligence
    ↓
AI Investigation
    ↓
Exposure
    ↓
Recommendation
    ↓
Policy Decision
    ↓
Human Decision
    ↓
Action
    ↓
Audit History
```

---

## FR-25 — Fail Safely

AegisGuard shall fail safely when individual components become unavailable.

### ML unavailable

The system shall use available deterministic risk signals/rules or escalate appropriately.

### AI investigation unavailable

The Risk Event shall remain available for human investigation.

### Policy engine unavailable

The system shall not bypass policy controls to execute consequential actions.

Component failure shall not create uncontrolled high-impact behaviour.

---

# 5. Machine Learning Requirements

## ML-01 — Evaluation on Held-Out Data

ML models shall be evaluated on data not used during model training.

---

## ML-02 — Class Imbalance Awareness

The ML pipeline shall account for fraud-class imbalance where applicable.

Evaluation shall not rely solely on raw accuracy.

---

## ML-03 — Precision and Recall

The system shall evaluate relevant classification metrics, including:

* Precision
* Recall
* F1 score

---

## ML-04 — Ranking / Probability Evaluation

Where appropriate, evaluation shall include:

* PR-AUC
* ROC-AUC

PR-AUC is particularly relevant when the positive class is highly imbalanced.

---

## ML-05 — Confusion Matrix

The system shall support confusion-matrix analysis:

```text
                 Actual
              Fraud   Legitimate

Pred Fraud      TP        FP

Pred Legit      FN        TN
```

---

## ML-06 — Temporal Evaluation

Where appropriate, model evaluation shall respect temporal ordering.

Training on future information and evaluating on earlier information shall be avoided.

---

## ML-07 — Model Traceability

Every production-like risk score generated in V1 shall identify the model version that produced it.

---

## ML-08 — Feature Leakage Prevention

Features used for a historical transaction must only contain information legitimately available at the corresponding decision point.

Later fraud outcomes must not become transaction-time features.

---

## ML-09 — Model Performance Monitoring

V1 should provide enough information to evaluate model performance over time.

Future versions may introduce more advanced model drift monitoring.

---

# 6. Security Requirements

## SEC-01 — Controlled AI Access

The AI investigation component shall interact with the system through controlled interfaces/tools.

It shall not receive unrestricted system access.

---

## SEC-02 — Policy Enforcement

AI-generated recommendations shall not bypass deterministic policy controls.

---

## SEC-03 — Action Authorization

Consequential actions shall require valid authorization according to policy and, where required, human approval.

---

## SEC-04 — Input Validation

External or user-provided inputs shall be validated before being used by application components.

---

## SEC-05 — Sensitive Data Handling

Sensitive information such as network identifiers shall not be unnecessarily exposed through logs, debugging output, or user interfaces.

---

## SEC-06 — Secrets Management

Credentials, API keys, and other secrets shall not be hardcoded into source code.

Development configuration shall use environment-based secrets.

---

## SEC-07 — AI Evidence Integrity

AI-generated content shall not be allowed to silently modify or fabricate underlying evidence.

Observed evidence and AI interpretation must remain distinguishable.

---

# 7. Auditability Requirements

## AUD-01 — Decision Traceability

The system shall allow a significant risk decision to be traced from:

```text
Transaction
    ↓
Risk Signals
    ↓
Risk Score / Rules / Anomalies
    ↓
Risk Event
    ↓
Investigation
    ↓
Recommendation
    ↓
Policy Decision
    ↓
Human Decision
    ↓
Action
    ↓
Outcome
```

---

## AUD-02 — Model Traceability

Risk predictions shall identify the model version responsible for the prediction.

---

## AUD-03 — Recommendation Traceability

Every executed action should be traceable to the recommendation that led to it.

---

## AUD-04 — Policy Traceability

Every policy-controlled recommendation should identify the policy decision that authorized, rejected, or escalated it.

---

## AUD-05 — Human Decision Traceability

Human decisions requiring approval shall identify the relevant decision and timestamp.

---

## AUD-06 — Outcome Traceability

Later fraud outcomes should be traceable to relevant transactions and Risk Events.

---

# 8. Reliability Requirements

## REL-01 — Graceful Component Failure

Failure of a non-critical component should not cause uncontrolled system behaviour.

---

## REL-02 — No Unsafe Fallback

Fallback behaviour must not bypass security or policy controls.

---

## REL-03 — Persistent Decision History

Important decisions and actions should remain recoverable from persistent storage.

---

## REL-04 — Transactional Integrity

Operations that modify related financial-risk state should preserve database consistency.

---

# 9. Explainability Requirements

## NFR-01 — Risk Explanation

The system should provide understandable reasons for significant risk assessments.

---

## NFR-02 — Evidence Attribution

Investigation conclusions should identify the evidence supporting them.

---

## NFR-03 — Prediction vs Fact

The system shall distinguish model predictions from observed facts.

---

## NFR-04 — Uncertainty

Where confidence or uncertainty is relevant, the system should represent it rather than presenting probabilistic conclusions as absolute truth.

---

# 10. Performance Requirements

V1 is a prototype and does not target internet-scale performance.

The system should nevertheless provide reasonable interactive performance for the synthetic workload.

The implementation should avoid unnecessary:

* N+1 database queries
* Repeated expensive calculations
* Unbounded synchronous operations
* Excessive data retrieval

Concrete performance targets should be established after the initial workload and architecture are implemented.

---

# 11. Maintainability Requirements

## NFR-05 — Separation of Concerns

The system should maintain clear boundaries between:

```text
API
Domain Logic
Persistence
ML
Risk Detection
Investigation
Policy
Actions
```

---

## NFR-06 — Modular Components

Components should be structured so that individual mechanisms can be tested and replaced without rewriting the entire system.

---

## NFR-07 — Migration-Based Database Changes

Database schema changes shall be managed through versioned migrations.

---

## NFR-08 — Configuration Separation

Environment-specific configuration shall remain separate from application logic.

---

# 12. Reproducibility Requirements

## NFR-09 — Synthetic Data Reproducibility

Synthetic datasets should support deterministic generation through controlled random seeds where practical.

---

## NFR-10 — Model Reproducibility

Training and evaluation processes should preserve sufficient metadata to understand how a model was produced.

---

## NFR-11 — Versioned Decisions

Risk scores should retain model-version information so historical results can be reproduced or analyzed.

---

# 13. Data Integrity Requirements

## NFR-12 — Referential Integrity

Relationships between domain entities shall use appropriate database constraints.

---

## NFR-13 — Monetary Precision

Financial amounts shall not use floating-point representation.

V1 shall use integer minor units with an associated ISO-style three-character currency code.

Example:

```text
amount_minor = 125075
currency = INR
```

---

## NFR-14 — Temporal Integrity

The system shall preserve the distinction between:

```text
occurred_at
created_at
available_at
```

where these concepts are relevant.

---

## NFR-15 — Historical Preservation

Important historical records such as risk scores, investigations, recommendations, policy decisions, actions, outcomes, and audit events should not be silently overwritten.

---

# 14. Observability Requirements

The application should provide sufficient logging and diagnostics to determine:

* Whether components are running
* Whether requests are succeeding
* Whether database operations are failing
* Whether ML scoring is failing
* Whether AI investigation is failing
* Whether policy evaluation is failing

Logs should avoid unnecessarily exposing sensitive information.

More advanced metrics and tracing may be introduced as the implementation matures.

---

# 15. Prototype Constraints

The following constraints apply to V1:

### Synthetic environment

Payment activity is synthetic.

### Simulated external intelligence

Network/consortium intelligence is simulated.

### Simulated defensive actions

Actions operate against a simulated environment.

### No production financial impact

The system must not perform real financial transactions or real payment restrictions.

### No production-scale claims

V1 performance should not be presented as evidence of production fraud-detection capability.

---

# 16. Explicit V1 Architecture Boundaries

The following are not required by V1:

* Kafka
* Kubernetes
* Redis
* Graph database
* Vector database
* Microservice architecture
* Data warehouse
* Enterprise multi-tenancy
* Billing infrastructure
* Production payment gateways
* Real consortium integrations

These may be introduced in future versions only when requirements justify them.

---

# 17. Requirement Priority

Requirements should generally be implemented in the following priority order.

### Critical

* FR-01 — Payment ingestion
* FR-03 — Point-in-time correctness
* FR-04 — Risk assessment
* FR-05 — Risk scoring
* FR-06 — Rules
* FR-08 — Anomaly detection
* FR-09 — Risk Events
* FR-12 — Investigation
* FR-14 — Exposure assessment
* FR-15 — Recommendations
* FR-16 — Policy controls
* FR-17 — Human-in-the-loop
* FR-18 — Defensive actions
* FR-19 — Fraud outcomes
* FR-23 — Audit trail
* FR-25 — Safe failure

### Important

* FR-02 — Supporting signals
* FR-10 — Evidence correlation
* FR-11 — Shared intelligence
* FR-13 — Evidence-based explanation
* FR-20 — Noisy/delayed labels
* FR-21 — Historical training data
* FR-22 — Model versioning
* FR-24 — Analyst interface

### Supporting

* Advanced observability
* Advanced model monitoring
* Additional metadata
* Additional behavioural metrics
* Future scalability capabilities

---

# 18. Requirements Traceability

The requirements derive from:

```text
product-definition.md
```

and are refined by:

```text
use-cases.md
domain-model.md
data-model.md
```

The relationship is:

```text
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
Implementation
```

A requirement should not be implemented in isolation from the relevant domain and architecture documents.

---

# 19. Change Management

This is a living document.

When requirements change:

1. Update this document.
2. Identify affected use cases.
3. Review the domain model.
4. Review the data model.
5. Review architecture.
6. Review system flows.
7. Review implementation and tests.

New infrastructure should not be introduced simply because it is technically interesting.

It should be justified by an actual requirement.

---

# 20. V1 Requirement Boundary

AegisGuard V1 is complete when it can demonstrate the core lifecycle:

```text
Ingest
  ↓
Assess
  ↓
Detect
  ↓
Correlate
  ↓
Investigate
  ↓
Assess Exposure
  ↓
Recommend
  ↓
Apply Policy
  ↓
Human Decision if Required
  ↓
Act
  ↓
Audit
  ↓
Receive Outcome
  ↓
Evaluate / Learn
```

The objective is a technically coherent, explainable, auditable, and safe fraud-risk system.

It is **not** to build a production-scale global payment platform in V1.
