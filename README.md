# AegisGuard


**AI-powered fraud detection and merchant risk investigation system**

AegisGuard detects abnormal fraud patterns across merchant transactions, investigates the underlying signals, estimates financial exposure, and recommends bounded defensive actions.

The system combines **machine learning, anomaly detection, agentic AI, and deterministic risk controls** to simulate how a payment platform could identify and respond to emerging fraud in real time.

> **Detect → Investigate → Explain → Decide → Act Safely → Audit**

---

## Problem

Fraud is rarely a single suspicious transaction.

A merchant may experience a sudden increase in fraudulent transactions caused by:

* unusual transaction velocity
* new device or IP clusters
* geographic anomalies
* repeated transaction patterns
* abnormal payment amounts
* coordinated activity across customers
* sudden deviation from the merchant's historical baseline

A simple fraud classifier can identify individual risky transactions, but it may miss the larger picture:

> **"Is this merchant experiencing an active fraud event right now?"**

AegisGuard focuses on detecting and investigating these **merchant-level fraud spikes**.

---

## What the System Does

Given a stream or batch of payment transactions, the system:

1. Establishes merchant-specific behavioral baselines.
2. Extracts transaction and behavioral risk features.
3. Classifies transactions using supervised ML.
4. Detects abnormal changes in merchant-level fraud patterns.
5. Groups related suspicious activity into risk signals/clusters.
6. Estimates potential financial exposure.
7. Invokes an AI investigation agent to investigate the event.
8. Produces an evidence-backed explanation.
9. Recommends a bounded defensive action.
10. Applies deterministic policy and safety constraints.
11. Executes approved actions only in the simulated/test environment.
12. Records the complete decision and action trail.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │  Transaction Data   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Data Validation &   │
                    │ Feature Engineering │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
           ┌────────────────┐    ┌─────────────────┐
           │ Fraud Classifier│    │ Anomaly / Spike │
           │                │    │    Detector     │
           └───────┬────────┘    └────────┬────────┘
                   │                      │
                   └──────────┬───────────┘
                              ▼
                    ┌─────────────────────┐
                    │   Risk Aggregator   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Investigation Agent │
                    │                     │
                    │ • Query transactions│
                    │ • Analyze clusters  │
                    │ • Calculate exposure│
                    │ • Gather evidence   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Policy / Safety   │
                    │      Engine         │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │ Test-Mode    │      │ Human Review │
             │ Defensive    │      │ / Escalation │
             │ Action       │      └──────────────┘
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ Audit Trail  │
             └──────────────┘
```

---

## Machine Learning

The ML layer is deliberately separated from the LLM layer.

The LLM is **not responsible for deciding whether a transaction is fraudulent**.

### Supervised Fraud Detection

Candidate models:

* Logistic Regression
* Random Forest
* XGBoost / LightGBM

Features may include:

* transaction amount
* transaction velocity
* payment method
* device history
* IP behavior
* customer history
* geographic distance
* time-of-day patterns
* failed transaction frequency
* refund/chargeback history
* merchant-level behavioral statistics

Models will be evaluated on a **held-out test set** using:

* Precision
* Recall
* F1
* PR-AUC
* ROC-AUC
* Confusion Matrix

Because fraud is highly imbalanced, **PR-AUC and precision/recall are prioritized over accuracy**.

---

## Fraud-Spike Detection

The system also operates at the merchant level.

For each merchant, it maintains rolling behavioral statistics such as:

```text
Fraud Rate
Transaction Volume
Average Transaction Value
Failure Rate
Chargeback Rate
Unique Devices
Unique IPs
Geographic Distribution
Transaction Velocity
```

A spike is detected when current behavior significantly deviates from the merchant's historical baseline.

Example:

```text
Merchant: M102

30-day baseline fraud rate: 0.40%

Current fraud rate:         8.10%

Increase:                   20.25×

Anomaly Score:              5.4σ

Estimated Exposure:         ₹4.2 lakh
```

The system then creates a **Risk Event** for investigation.

---

## AI Investigation Agent

Once a significant risk event is detected, an AI agent investigates it using structured tools.

Example tools:

```text
get_merchant_metrics()
get_recent_transactions()
get_customer_history()
get_device_clusters()
get_ip_clusters()
get_geographic_distribution()
calculate_exposure()
create_risk_alert()
recommend_action()
```

The agent does not directly manipulate transaction state.

Instead, it gathers structured evidence and produces an investigation such as:

```text
HIGH RISK

Fraud activity increased 20.2× above the merchant's
30-day baseline.

Evidence:
• 62% of suspicious transactions originate from 3 IP ranges.
• 71% involve previously unseen devices.
• Transaction velocity increased 8.4×.
• Suspicious activity is concentrated in a 35-minute window.

Estimated financial exposure:
₹4.2 lakh

Recommended action:
Temporarily increase verification requirements for
transactions matching the identified risk pattern.
```

---

## Guardrails & Bounded Actions

AI-generated decisions are never executed directly.

Every recommendation passes through a deterministic policy layer.

Example:

```text
AI Recommendation
       ↓
Policy Validation
       ↓
Is action allowed?
       │
    ┌──┴──┐
    │     │
   YES    NO
    │     │
    ▼     ▼
Execute  Escalate
```

The policy engine can enforce:

* maximum transaction/action limits
* allowed action types
* confidence thresholds
* exposure thresholds
* human-review requirements
* cooldown periods
* test-mode restrictions

**No unrestricted money movement is permitted.**

---

## Failure Handling

The system explicitly handles failures rather than silently producing a decision.

Example:

```text
Agent requests customer history
            ↓
        API timeout
            ↓
         Retry once
            ↓
       Still unavailable
            ↓
    Investigation incomplete
            ↓
   Automated action blocked
            ↓
      Human review required
```

The failure is recorded in the audit trail.

Example:

```text
10:42:17  Risk event detected
10:42:18  Customer history requested
10:42:20  Tool timeout
10:42:21  Retry attempted
10:42:23  Retry failed
10:42:23  Automated action blocked
10:42:24  Escalated for review
```

---

## Evaluation

The project will be evaluated using a held-out dataset rather than cherry-picked examples.

### Model Metrics

| Metric              | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| Precision           | How many flagged transactions are actually risky |
| Recall              | How much fraud the system catches                |
| F1                  | Balance between precision and recall             |
| PR-AUC              | Performance under class imbalance                |
| False Positive Rate | Legitimate activity incorrectly flagged          |
| ROC-AUC             | Overall classification performance               |

### Business Metrics

The system will additionally measure:

* estimated financial exposure detected
* false-positive cost
* expected loss
* detection latency
* percentage of risk events successfully investigated
* percentage of cases requiring human escalation
* action success/failure rate

The objective is **not maximum recall at any cost**.

A useful fraud system must balance:

> **fraud prevented vs. legitimate customers disrupted.**

---

## Dataset

The initial version uses a synthetic Razorpay-like transaction dataset.

The dataset will contain realistic patterns including:

* normal merchant behavior
* isolated fraudulent transactions
* coordinated fraud
* velocity attacks
* device-based clusters
* IP-based clusters
* geographic anomalies
* sudden merchant-level fraud spikes
* highly imbalanced fraud labels

Synthetic data generation will deliberately introduce known fraud scenarios so that the detection system can be evaluated against controlled ground truth.

---

## Tech Stack

### Machine Learning

* Python
* NumPy
* Pandas
* scikit-learn
* XGBoost / LightGBM
* MLflow

### AI

* LLM
* Tool calling
* Structured outputs
* Agent orchestration

### Backend

* FastAPI
* PostgreSQL
* REST APIs

### Frontend

* React
* TypeScript

### Infrastructure

* Docker
* GitHub Actions
* Cloud deployment

---

## Project Structure

```text
fraud-spike-sentinel/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
│
├── notebooks/
│   ├── eda.ipynb
│   ├── feature_engineering.ipynb
│   └── model_comparison.ipynb
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── anomaly/
│   ├── agent/
│   ├── policy/
│   ├── api/
│   └── evaluation/
│
├── tests/
│
├── frontend/
│
├── configs/
│
├── reports/
│   └── model_evaluation.md
│
├── docker/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Key Design Principles

### 1. ML decides risk; LLM explains and investigates

The LLM is not treated as a black-box fraud classifier.

### 2. Every automated action is bounded

The agent operates within explicit policies and test-mode constraints.

### 3. Metrics over demos

Performance is measured on a held-out dataset.

### 4. False positives matter

Blocking legitimate transactions has a measurable business cost.

### 5. Failures are first-class events

Tool failures, unavailable data, and uncertain investigations result in safe escalation rather than fabricated decisions.

### 6. Every decision is auditable

The system records what happened, why it happened, what evidence was used, and what action followed.

---

## Current Status

🚧 **Under development**

Planned milestones:

* [ ] Synthetic transaction generator
* [ ] Exploratory data analysis
* [ ] Feature engineering pipeline
* [ ] Baseline fraud classifier
* [ ] Model comparison
* [ ] Held-out evaluation
* [ ] Merchant-level spike detector
* [ ] Financial exposure estimation
* [ ] AI investigation agent
* [ ] Tool-calling layer
* [ ] Policy/guardrail engine
* [ ] Failure handling
* [ ] Audit trail
* [ ] Razorpay test-mode integration
* [ ] Dashboard
* [ ] Docker deployment
* [ ] End-to-end evaluation

---

## Disclaimer

AegisGuard is an educational and defensive security project intended for experimentation using synthetic data and test-mode payment APIs.

It is designed exclusively for **fraud detection, investigation, prevention, and risk management** and does not provide functionality for committing fraud, bypassing payment controls, or evading detection.
