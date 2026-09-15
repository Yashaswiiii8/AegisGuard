# AegisGuard Data Model

> **Canonical description of the AegisGuard V1 PostgreSQL persistence model.**

---

## 1. Document Status

**Status:** Living
**Version:** 1.0
**Scope:** AegisGuard V1
**Database:** PostgreSQL
**ORM:** SQLAlchemy 2.x
**Migration Tool:** Alembic

### Purpose

This document defines how the conceptual domain model is represented in PostgreSQL.

It specifies:

* Persistent entities
* Tables
* Primary keys
* Foreign keys
* Relationships
* Important constraints
* Temporal fields
* Monetary representation
* JSON/structured metadata
* Indexing principles
* Data-integrity rules

This document is derived from `domain-model.md`.

It does **not** define API endpoints, frontend state, ML algorithms, or agent implementation details.

---

# 2. Persistence Philosophy

AegisGuard V1 uses PostgreSQL as the system of record.

The database should preserve the distinction between:

```text
Payment Activity
      ↓
Detection
      ↓
Investigation
      ↓
Decision
      ↓
Action
      ↓
Outcome
      ↓
Audit History
```

The database should preserve historical information rather than overwriting important decisions.

For example, if a transaction was initially scored using model version `v1.0` and later rescored using `v1.1`, the original score should remain historically traceable.

---

# 3. Primary Database

## PostgreSQL

PostgreSQL is the primary V1 datastore.

Reasons:

* Strong relational modelling
* Foreign-key integrity
* ACID transactions
* Efficient aggregation
* Mature indexing
* JSONB support
* Good Python ecosystem
* Suitable support for historical and audit data

V1 does not require:

* MongoDB
* Neo4j
* Redis
* Kafka
* A separate data warehouse
* A vector database

Those technologies may become appropriate in future versions if actual requirements justify them.

---

# 4. Identifier Strategy

V1 entities should use stable unique identifiers.

The preferred identifier type is:

```text
UUID
```

UUIDs provide:

* Global uniqueness
* Non-sequential public identifiers
* Easy generation across application components
* Compatibility with distributed systems if the architecture later evolves

Database-generated or application-generated UUIDs may be used consistently throughout the system.

The implementation should avoid mixing arbitrary identifier strategies without a clear reason.

---

# 5. Monetary Representation

Financial amounts must **not** use floating-point database types.

Use:

```text
amount_minor BIGINT
currency CHAR(3)
```

Example:

```text
₹1,250.75
```

would conceptually be represented as:

```text
amount_minor = 125075
currency = "INR"
```

The exact minor-unit interpretation depends on the currency.

### Reason

Floating-point representation can introduce precision errors.

Financial calculations must therefore use integer minor units or an appropriate exact numeric representation.

V1 standardizes on integer minor units for transaction amounts.

---

# 6. Timestamp Strategy

AegisGuard must distinguish between different meanings of time.

The primary temporal concepts are:

### `occurred_at`

When the underlying event actually happened.

### `created_at`

When AegisGuard created or persisted the record.

### `available_at`

When information became available to the risk system.

These values must not be casually substituted for one another.

All persisted timestamps should use PostgreSQL timestamp types with timezone awareness:

```text
TIMESTAMPTZ
```

The application should treat timestamps consistently in UTC.

---

# 7. Table Groups

The V1 database contains the following logical table groups.

### Payment

```text
customers
merchants
transactions
devices
network_identities
customer_devices
```

### Detection

```text
risk_scores
risk_signals
risk_rules
rule_evaluations
behavioural_anomalies
risk_events
risk_event_transactions
```

### Investigation

```text
investigations
evidence
network_signals
exposure_assessments
recommendations
```

### Decision / Response

```text
policies
policy_decisions
human_decisions
actions
```

### Learning

```text
fraud_outcomes
model_versions
```

### Governance

```text
audit_events
```

---

# 8. Payment Tables

## 8.1 `customers`

Represents customers participating in the synthetic payment environment.

### Core fields

```text
id
status
created_at
updated_at
```

Optional behavioural/profile metadata may be stored separately or through controlled structured fields where justified.

### Primary key

```text
id
```

### Relationships

```text
customers 1 ───── * transactions
customers * ───── * devices
```

---

# 9. `merchants`

Represents merchants participating in the payment environment.

### Core fields

```text
id
status
created_at
updated_at
```

### Relationships

```text
merchants 1 ───── * transactions
merchants 1 ───── * behavioural_anomalies
```

Merchant status may be relevant to policy evaluation and defensive actions.

---

# 10. `transactions`

Represents payment activity.

This is one of the central tables in the system.

### Core fields

```text
id
customer_id
merchant_id
amount_minor
currency
payment_method
device_id
network_identity_id
country_code
status
occurred_at
created_at
```

### Foreign keys

```text
customer_id → customers.id
merchant_id → merchants.id
device_id → devices.id
network_identity_id → network_identities.id
```

### Important constraints

* `amount_minor` must be non-negative where appropriate
* `currency` must contain a valid three-character currency code
* Required entity relationships should use foreign keys
* `occurred_at` should represent the transaction's actual event time
* `created_at` should represent ingestion/persistence time

### Relationships

```text
transactions 1 ───── * risk_scores
transactions 1 ───── * risk_signals
transactions 1 ───── * rule_evaluations
transactions 1 ───── * fraud_outcomes

transactions * ───── * risk_events
```

---

# 11. `devices`

Represents synthetic device identities.

### Core fields

```text
id
fingerprint
device_type
created_at
```

The exact fingerprint representation may evolve.

### Constraints

Device fingerprints should be uniquely identifiable where the domain requires a one-to-one representation of a synthetic device.

### Relationships

```text
devices 1 ───── * transactions
devices * ───── * customers
```

---

# 12. `network_identities`

Represents network-level identities.

Examples:

* IP address
* Synthetic network identity
* Other network identifier

### Core fields

```text
id
identity_value
identity_type
country_code
created_at
```

Sensitive network values should be handled appropriately in application logs and API responses.

### Relationship

```text
network_identities 1 ───── * transactions
```

---

# 13. `customer_devices`

Association table connecting customers and devices.

### Core fields

```text
customer_id
device_id
first_seen_at
last_seen_at
```

### Primary key

Composite key:

```text
(customer_id, device_id)
```

### Foreign keys

```text
customer_id → customers.id
device_id → devices.id
```

### Relationship

```text
customers * ───── * devices
```

This table allows AegisGuard to represent shared device relationships.

---

# 14. Detection Tables

## 14.1 `risk_scores`

Stores ML-generated transaction risk predictions.

### Core fields

```text
id
transaction_id
model_version_id
score
scored_at
metadata
```

### Foreign keys

```text
transaction_id → transactions.id
model_version_id → model_versions.id
```

### Constraints

`score` should be constrained to the expected model output range.

For probability-based scoring:

```text
0.0 ≤ score ≤ 1.0
```

### Important rule

A risk score is a prediction.

It must never be treated as a confirmed fraud outcome.

### Relationship

```text
transactions 1 ───── * risk_scores
model_versions 1 ─── * risk_scores
```

---

# 15. `risk_signals`

Stores individual pieces of risk-related evidence.

### Core fields

```text
id
transaction_id
signal_type
source
value
occurred_at
available_at
created_at
metadata
```

### Foreign key

```text
transaction_id → transactions.id
```

### Examples

```text
signal_type = "HIGH_VELOCITY"
source = "RULE_ENGINE"
```

or:

```text
signal_type = "SUSPICIOUS_IP"
source = "NETWORK_INTELLIGENCE"
```

### Temporal requirement

`available_at` is particularly important.

A signal cannot be treated as available for transaction-time scoring if it became available after the transaction decision.

---

# 16. `risk_rules`

Stores deterministic risk rules.

### Core fields

```text
id
name
description
rule_type
configuration
enabled
created_at
updated_at
```

`configuration` may use JSONB where rule-specific parameters vary.

Example:

```json
{
  "window_minutes": 10,
  "max_transactions": 20
}
```

### Reason for JSONB

Different rules may require different configuration structures.

This avoids creating a large number of sparse rule-specific columns.

---

# 17. `rule_evaluations`

Stores execution results for risk rules.

### Core fields

```text
id
rule_id
transaction_id
triggered
evaluated_at
details
```

### Foreign keys

```text
rule_id → risk_rules.id
transaction_id → transactions.id
```

### Purpose

Rule definitions and rule execution results are separate.

```text
RiskRule
   ↓
RuleEvaluation
```

This preserves historical information even when a rule's configuration later changes.

---

# 18. `behavioural_anomalies`

Stores detected deviations from expected merchant behaviour.

### Core fields

```text
id
merchant_id
metric
baseline_value
observed_value
deviation
detection_method
detected_at
metadata
```

### Foreign key

```text
merchant_id → merchants.id
```

### Example

```text
metric = "transaction_volume"

baseline_value = 10000
observed_value = 27000
deviation = 2.7
```

### Important rule

The existence of a behavioural anomaly does not imply fraud.

---

# 19. `risk_events`

Represents correlated suspicious situations.

### Core fields

```text
id
merchant_id
severity
status
created_at
updated_at
metadata
```

A Risk Event may be associated primarily with a merchant in V1 while still containing transactions and related evidence.

### Foreign key

```text
merchant_id → merchants.id
```

### Relationships

```text
risk_events 1 ───── 0..1 investigations
risk_events 1 ───── * exposure_assessments
risk_events 1 ───── * recommendations
risk_events 1 ───── * fraud_outcomes
risk_events * ───── * transactions
```

---

# 20. `risk_event_transactions`

Association table connecting Risk Events and Transactions.

### Fields

```text
risk_event_id
transaction_id
relationship_type
created_at
```

### Primary key

Composite:

```text
(risk_event_id, transaction_id)
```

### Foreign keys

```text
risk_event_id → risk_events.id
transaction_id → transactions.id
```

### Purpose

A transaction may participate in multiple risk events.

A risk event may contain many transactions.

---

# 21. Investigation Tables

## 21.1 `investigations`

Represents the structured investigation of a Risk Event.

### Core fields

```text
id
risk_event_id
status
started_at
completed_at
summary
created_at
updated_at
```

### Foreign key

```text
risk_event_id → risk_events.id
```

### Constraint

V1 allows at most one active investigation record per Risk Event.

This can be expanded later if the domain requires multiple investigation sessions.

---

# 22. `evidence`

Represents information considered during an investigation.

### Core fields

```text
id
investigation_id
evidence_type
source_type
source_reference
description
observed_at
created_at
metadata
```

### Foreign key

```text
investigation_id → investigations.id
```

### Important distinction

Evidence may represent:

* Observed facts
* Model outputs
* Rule results
* Behavioural observations
* Network intelligence

The database should preserve the evidence source so that AI interpretation is not confused with observed data.

---

# 23. `network_signals`

Stores simulated shared fraud-intelligence results.

### Core fields

```text
id
investigation_id
signal_type
entity_type
entity_reference
confidence
source
observed_at
created_at
metadata
```

### Foreign key

```text
investigation_id → investigations.id
```

### V1 constraint

The source must clearly identify the signal as simulated.

AegisGuard must not represent synthetic intelligence as real external intelligence.

---

# 24. `exposure_assessments`

Stores potential financial exposure estimates.

### Core fields

```text
id
risk_event_id
amount_minor
currency
calculation_method
assessed_at
metadata
```

### Foreign key

```text
risk_event_id → risk_events.id
```

### Important rule

The amount represents an estimate of potential exposure.

It does not represent confirmed financial loss.

---

# 25. `recommendations`

Stores defensive recommendations.

### Core fields

```text
id
risk_event_id
action_type
reason
confidence
human_approval_required
created_at
metadata
```

### Foreign key

```text
risk_event_id → risk_events.id
```

### Relationships

```text
recommendations 1 ───── 1 policy_decisions
recommendations 1 ───── 0..1 human_decisions
recommendations 1 ───── 0..1 actions
```

A recommendation must remain separate from its eventual action.

---

# 26. Decision / Response Tables

## 26.1 `policies`

Stores deterministic decision policies.

### Core fields

```text
id
name
description
enabled
priority
configuration
created_at
updated_at
```

Policy-specific configuration may use JSONB where appropriate.

---

# 27. `policy_decisions`

Stores the result of evaluating a recommendation against policy.

### Core fields

```text
id
recommendation_id
policy_id
decision
reason
evaluated_at
metadata
```

### Foreign keys

```text
recommendation_id → recommendations.id
policy_id → policies.id
```

### Expected decisions

```text
ALLOW
APPROVAL_REQUIRED
DENY
```

### Purpose

This table creates an explicit authorization boundary between AI recommendation and action.

---

# 28. `human_decisions`

Stores analyst decisions.

### Core fields

```text
id
recommendation_id
decision
reason
analyst_reference
decided_at
metadata
```

### Foreign key

```text
recommendation_id → recommendations.id
```

### Expected decisions

Examples:

```text
APPROVE
REJECT
ESCALATE
```

The exact enumeration may evolve with V1 implementation.

---

# 29. `actions`

Represents actual defensive actions.

### Core fields

```text
id
recommendation_id
human_decision_id
action_type
status
executed_at
completed_at
result
metadata
```

### Foreign keys

```text
recommendation_id → recommendations.id
human_decision_id → human_decisions.id
```

### Important distinction

An Action represents what actually happened.

It must not be created merely because a Recommendation exists.

---

# 30. Learning Tables

## 30.1 `fraud_outcomes`

Stores information learned after the original transaction.

### Core fields

```text
id
transaction_id
risk_event_id
outcome
source
occurred_at
recorded_at
confidence
metadata
```

### Foreign keys

```text
transaction_id → transactions.id
risk_event_id → risk_events.id
```

The Risk Event relationship may be nullable where an outcome exists without an associated event.

### Examples

```text
outcome = CONFIRMED_FRAUD
source = CHARGEBACK
```

or:

```text
outcome = LEGITIMATE
source = MANUAL_REVIEW
```

### Important temporal rule

Fraud outcomes may arrive after the original risk decision.

They must not be retroactively treated as transaction-time features.

---

# 31. `model_versions`

Stores metadata about ML models used by AegisGuard.

### Core fields

```text
id
model_name
version
status
trained_at
created_at
metadata
```

### Relationship

```text
model_versions 1 ───── * risk_scores
```

### Purpose

Every ML risk score must be traceable to a model version.

---

# 32. Governance Tables

## 32.1 `audit_events`

Stores the historical record of significant system events.

### Core fields

```text
id
event_type
entity_type
entity_id
actor_type
actor_id
occurred_at
created_at
metadata
```

### Example event types

```text
TRANSACTION_RECEIVED
RISK_SCORE_CREATED
RULE_TRIGGERED
RISK_EVENT_CREATED
INVESTIGATION_STARTED
RECOMMENDATION_CREATED
POLICY_EVALUATED
HUMAN_DECISION_RECORDED
ACTION_EXECUTED
FRAUD_OUTCOME_RECEIVED
```

### Purpose

Audit events should make it possible to reconstruct important system decisions.

---

# 33. Entity Relationship Summary

The primary database relationships are:

```text
customers
    │
    ├───────────────< transactions
    │
    └───────────────< customer_devices >────────────── devices
                                                        │
                                                        └──< transactions

merchants
    │
    ├───────────────< transactions
    │
    └───────────────< behavioural_anomalies

network_identities
    │
    └───────────────< transactions

transactions
    │
    ├───────────────< risk_scores >──────── model_versions
    │
    ├───────────────< risk_signals
    │
    ├───────────────< rule_evaluations >── risk_rules
    │
    ├───────────────< fraud_outcomes
    │
    └───────────────< risk_event_transactions >──────── risk_events
                                                            │
                                                            ├──< investigations
                                                            │       │
                                                            │       ├──< evidence
                                                            │       │
                                                            │       └──< network_signals
                                                            │
                                                            ├──< exposure_assessments
                                                            │
                                                            ├──< recommendations
                                                            │       │
                                                            │       └── policy_decisions >── policies
                                                            │
                                                            └──< fraud_outcomes

recommendations
    │
    ├───────────────< human_decisions
    │
    └───────────────< actions

All significant domain entities/events
    │
    └───────────────< audit_events
```

---

# 34. Cardinality Summary

| Relationship                    | Cardinality     |
| ------------------------------- | --------------- |
| Customer → Transaction          | 1 : many        |
| Merchant → Transaction          | 1 : many        |
| Customer ↔ Device               | many : many     |
| Device → Transaction            | 1 : many        |
| NetworkIdentity → Transaction   | 1 : many        |
| Transaction → RiskScore         | 1 : many        |
| ModelVersion → RiskScore        | 1 : many        |
| Transaction → RiskSignal        | 1 : many        |
| RiskRule → RuleEvaluation       | 1 : many        |
| Transaction → RuleEvaluation    | 1 : many        |
| Merchant → BehaviouralAnomaly   | 1 : many        |
| RiskEvent ↔ Transaction         | many : many     |
| RiskEvent → Investigation       | 1 : zero-or-one |
| Investigation → Evidence        | 1 : many        |
| Investigation → NetworkSignal   | 1 : many        |
| RiskEvent → ExposureAssessment  | 1 : many        |
| RiskEvent → Recommendation      | 1 : many        |
| Recommendation → PolicyDecision | 1 : one         |
| Policy → PolicyDecision         | 1 : many        |
| Recommendation → HumanDecision  | 1 : zero-or-one |
| Recommendation → Action         | 1 : zero-or-one |
| Transaction → FraudOutcome      | 1 : many        |
| RiskEvent → FraudOutcome        | 1 : many        |
| ModelVersion → RiskScore        | 1 : many        |
| Domain entities → AuditEvent    | many : many     |

---

# 35. Indexing Strategy

Indexes should support actual access patterns rather than being created indiscriminately.

Likely V1 indexes include:

### Transactions

```text
merchant_id
customer_id
device_id
network_identity_id
occurred_at
created_at
```

Composite indexes may be required for common behavioural queries such as:

```text
merchant_id + occurred_at
customer_id + occurred_at
device_id + occurred_at
```

### Risk Scores

```text
transaction_id
model_version_id
scored_at
```

### Risk Events

```text
merchant_id
status
severity
created_at
```

### Fraud Outcomes

```text
transaction_id
risk_event_id
occurred_at
```

### Audit Events

```text
entity_type + entity_id
event_type
occurred_at
```

Indexes should be validated against actual query patterns once the application is implemented.

---

# 36. Constraints and Data Integrity

The database should enforce domain rules wherever practical.

Examples:

### Monetary values

```text
amount_minor >= 0
```

### Risk scores

```text
0 <= score <= 1
```

### Required relationships

Foreign keys should prevent references to nonexistent:

* Customers
* Merchants
* Transactions
* Devices
* Risk Events
* Models
* Policies

### Enumerated states

Important status and decision fields should use controlled values rather than unrestricted strings where practical.

Examples:

```text
Risk Event Status
Recommendation Action Type
Policy Decision
Human Decision
Action Status
Fraud Outcome
```

The exact implementation may use PostgreSQL enums, constrained text values, or application-level enumerations depending on migration and extensibility requirements.

---

# 37. Historical Data Preservation

AegisGuard must preserve important historical decisions.

The following should generally be treated as append-oriented historical records:

* Risk scores
* Rule evaluations
* Investigations
* Evidence
* Exposure assessments
* Recommendations
* Policy decisions
* Human decisions
* Actions
* Fraud outcomes
* Audit events

Updating current status is acceptable where appropriate, but historical decision records should not be silently overwritten.

---

# 38. Soft Deletion

V1 should avoid unnecessary soft-delete complexity.

For core historical entities such as:

* Transactions
* Risk scores
* Risk events
* Investigations
* Recommendations
* Actions
* Fraud outcomes
* Audit events

records should generally remain available for historical analysis.

If an entity requires deactivation, prefer explicit status fields where appropriate.

---

# 39. JSONB Usage

PostgreSQL `JSONB` may be used for genuinely variable metadata.

Good candidates include:

* Risk signal metadata
* Rule configuration
* Policy configuration
* Model metadata
* Investigation metadata
* Evidence metadata
* Network signal metadata
* Action results

JSONB should **not** be used as a substitute for properly modelling stable relationships.

For example:

```text
Bad:
transaction.customer_id stored inside arbitrary JSON

Good:
transaction.customer_id as a foreign-key column
```

Use relational columns for stable domain structure and JSONB for genuinely flexible metadata.

---

# 40. Data Retention and Auditability

V1 should preserve enough historical data to support:

* Investigation
* Debugging
* Model evaluation
* Fraud-outcome analysis
* Audit reconstruction
* Demonstration of the complete fraud lifecycle

Retention policies should not be introduced solely for convenience before the project's actual data requirements are understood.

---

# 41. Point-in-Time Data Integrity

The database must preserve temporal information necessary to determine whether information was available at a given decision point.

For risk-related data, the system should be able to answer:

> "Was this signal available when the transaction was scored?"

This is why fields such as:

```text
occurred_at
available_at
created_at
```

must have clear semantics.

The ML training pipeline must use these timestamps when constructing historical features.

---

# 42. V1 Database Boundary

The PostgreSQL database is the system of record for the AegisGuard V1 application.

The database does not itself perform:

* ML inference
* AI reasoning
* Policy reasoning
* Fraud detection algorithms
* Frontend rendering

Those responsibilities belong to application components.

The database provides the persistent state and historical evidence required by those components.

---

# 43. Future Database Evolution

V1 deliberately uses PostgreSQL without additional infrastructure.

Future requirements may justify introducing:

```text
High-volume event ingestion
        ↓
Kafka / event streaming

Low-latency counters
        ↓
Redis / in-memory systems

Large analytical workloads
        ↓
Data warehouse / analytical store

Large-scale relationship traversal
        ↓
Graph-oriented storage

Semantic investigation knowledge
        ↓
Vector retrieval infrastructure
```

These technologies are **not part of the V1 database architecture**.

They should only be introduced when measurable system requirements justify them.

---

# 44. Relationship to Other Documents

This document depends on:

```text
product-definition.md
requirements.md
use-cases.md
domain-model.md
```

It provides the persistence foundation for:

```text
data-dictionary.md
architecture.md
system-flows.md
```

Later implementation documents will depend on this model as appropriate.

### Downstream impact

Changes to this document may affect:

* SQLAlchemy models
* Alembic migrations
* API schemas
* Services
* ML feature pipelines
* Agent tools
* Policy engine
* Tests
* Audit implementation

---

# 45. Change Management

This is a living document.

When a new persistent concept is introduced:

1. Determine whether it is actually a new domain entity.
2. Update `domain-model.md` if necessary.
3. Update this document.
4. Define its relationships and constraints.
5. Update `data-dictionary.md`.
6. Review affected architecture and system flows.
7. Only then implement the corresponding database changes.

Database schema changes should follow the domain model rather than silently introducing new concepts during implementation.

---

# 46. Canonical V1 Tables

The canonical AegisGuard V1 PostgreSQL table set is:

```text
PAYMENT
├── customers
├── merchants
├── transactions
├── devices
├── network_identities
└── customer_devices

DETECTION
├── risk_scores
├── risk_signals
├── risk_rules
├── rule_evaluations
├── behavioural_anomalies
├── risk_events
└── risk_event_transactions

INVESTIGATION
├── investigations
├── evidence
├── network_signals
├── exposure_assessments
└── recommendations

DECISION / RESPONSE
├── policies
├── policy_decisions
├── human_decisions
└── actions

LEARNING
├── fraud_outcomes
└── model_versions

GOVERNANCE
└── audit_events
```

This represents the **canonical persistence model for AegisGuard V1**.

It may be refined during implementation when concrete query patterns, validation requirements, and integration constraints become known, but changes must remain consistent with the domain model and V1 scope.
