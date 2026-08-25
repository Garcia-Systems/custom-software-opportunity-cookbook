# Case 11 — The Healthcare Organization

> **Fiction notice and boundary:** James River Specialty Clinic Group, its several outpatient clinics, approximately 80 employees, systems, operations, and every figure below are invented educational assumptions—not healthcare benchmarks. This case evaluates administrative custom-software economics. It processes no real information, contains no patient records, offers no medical advice, and models no diagnosis, treatment, clinical prioritization, clinical outcome, or clinical revenue benefit. It is not legal or compliance advice.

## 1. Business

James River Specialty Clinic Group has centralized administrative operations across several fictional clinics. Scheduling, a practice-management system, an electronic clinical-record system, billing/revenue-cycle software, patient communications, staff scheduling, reporting exports, and spreadsheets support this administrative sequence:

```text
APPOINTMENT → SCHEDULING / REGISTRATION → ADMINISTRATIVE STATUS
→ SERVICE-COMPLETION SIGNAL → BILLING WORKFLOW
→ PAYMENT / RECONCILIATION → MANAGEMENT REPORTING
```

Clinical systems are mentioned only because approved administrative status events may originate there. Existing systems remain authoritative.

## 2. Problem

Administrative staff reconcile appointment and status information, assemble billing-status and management reports from exports, search multiple systems, repeat administrative entry, prepare exceptions manually, combine location reports, and follow up on integration failures. Clinical work is not recoverable administrative burden.

## 3. Current systems

```text
Scheduling ───────────────┐
Practice management ─────┤
Clinical-record system ──┤
Billing / RCM ────────────┼──→ manual administrative reconciliation
Patient communications ──┤
Staff scheduling ─────────┤
Reporting exports ────────┤
Spreadsheets ─────────────┘
```

Access is not presumed. Fictional constraints include vendor-controlled interfaces, limited test environments, interface fees, export-only access, vendor professional services, difficult authentication, and approvals. Discovery must validate them.

## 4. Current-state economic burden

Every burden is `annual units × cost per unit`; weekly hours use `weekly hours × 52 × fictional loaded hourly cost`.

| Administrative component | Formula | Annual burden |
|---|---:|---:|
| Reconciliation | 30 × 52 × $42 | $65,520 |
| Duplicate entry | 18 × 52 × $38 | $35,568 |
| Billing-status reconciliation | 24 × 52 × $46 | $57,408 |
| Management reporting | 16 × 52 × $55 | $45,760 |
| Exception-list preparation | 14 × 52 × $41 | $29,848 |
| Cross-location reporting | 12 × 52 × $49 | $30,576 |
| Avoidable administrative rework | 180 incidents × $280 | $50,400 |
| **Total** | | **$315,080** |

The rework line is fictional administrative handling cost. It excludes care, medical outcomes, and captured revenue.

## 5. Potential recoverable value

Recovery is burden multiplied by a conservative improvement assumption: reconciliation 55% ($36,036), duplicate entry 45% ($16,005.60), billing-status reconciliation 50% ($28,704), management reporting 60% ($27,456), exceptions 55% ($16,416.40), cross-location reporting 50% ($15,288), and administrative rework 30% ($15,120). **Total recoverable value is $155,026.** Software is not assumed to improve health, treatment, clinical productivity, or clinical revenue.

## 6. Solution

The smallest deep-integration hypothesis accepts only approved administrative imports or APIs, normalizes clinic/location and administrative statuses (including billing status where appropriate), produces deterministic exception and cross-location reports, and adds reconciliation, duplicate detection, idempotency where relevant, failure handling, auditability, recovery considerations, monitoring, and a management briefing.

```text
APPROVED ADMINISTRATIVE DATA / EVENTS
                 ↓
       NARROW CUSTOM INTEGRATION
                 ↓
       normalized operational view
                 ↓
 administrative exceptions / reporting
```

**Data minimization is an architectural and economic control:**

```text
NEED DATA?
├── NO  → DO NOT INGEST IT
└── YES → USE MINIMUM NECESSARY FIELDS
```

No EHR, practice-management product, billing platform, portal, scheduling system, clinical workflow engine, diagnostic system, medical AI, or patient-facing product is proposed. Security features are cost assumptions, not a claim of legal compliance.

## 7. Build vs. buy

The comparison includes existing system reporting, vendor-supported interfaces/modules, practice-management reporting, revenue-cycle/reporting products, approved BI, vendor professional services, narrow custom integration, full replacement, and doing nothing. It compares setup, recurring cost, internal administration, retained burden, and explicit risk allowance. A supported vendor option can be economically superior even with a higher sticker price. Full replacement is outside the plausible intervention.

## 8. Delivery

Baseline effort is transparent:

| Delivery category | Hours |
|---|---:|
| Base engineering (discovery, adapters, minimization, normalization, audit/error handling, documentation, acceptance) | 400 |
| Integration-access validation | 72 |
| Security/privacy implementation | 82 |
| Validation/reconciliation plus testing | 196 |
| Deployment/monitoring | 34 |
| Rework reserve | 72 |
| Integration uncertainty reserve | 90 |
| **Total** | **946** |

At $105/hour plus $6,500 other direct costs, direct delivery cost is **$105,830**. The reserve is not a hidden score: uncertain interface behavior adds 90 explicit hours, separate from 72 expected rework hours. Sensitive-data handling, least privilege, authentication/authorization, audit logging, encryption expectations, secrets, environment separation, access controls, security review, incident expectations, and minimization consume effort without guaranteeing compliance.

Higher consequences of failure require reconciliation, duplicate detection, deterministic behavior, testing, acceptance, auditability, monitoring, and recovery planning. That is why this is materially more expensive than an ordinary read-only SMB report.

## 9. Reuse

The model identifies 190 reusable base hours for adapter framework, normalization, validation/reconciliation, idempotency, audit/logging, monitoring, secure configuration, and deployment tooling. It separately carries **364 customer-specific core hours**, plus QA, deployment, and reserves. Vendor interfaces, mappings, clinic workflows/statuses, billing mappings, security environment, reporting definitions, and acceptance remain specific. High reuse therefore can coexist with expensive validation.

## 10. Deal economics

Implementation price is **$126,000** and annual fee **$38,000**. Direct delivery cost is $105,830. Solutions labor is 196 hours × $85 = $16,660, leaving **$3,510 implementation contribution**, or **$17.91 per solutions hour**. Recoverable value less annual fee is $117,026, below implementation price: the customer misses one-year payback. High customer value does not cancel high delivery cost.

## 11. Market / sales

Solutions work includes prospecting 12, discovery 18, workflow mapping 20, interviews 18, security/privacy discovery 24, vendor validation 32, design 18, proposal/scoping 14, procurement/security coordination 26, and acceptance planning 14: **196 hours**. Baseline assumes an eight-month cycle, high procurement and close friction, but access to a willing buyer. Desire and authority are not the modeled failure: delivery economics are.

One viable clinic engagement would not validate healthcare as a market. Discovery must establish actual administrative burden, interface availability and vendor costs, security requirements, procurement, willingness to pay, support expectations, repeatable integration patterns, repeatable versus customer-specific validation, and whether narrower administrative cases are better.

## 12. Support

Expected support includes 150 engineering hours at $105, plus fictional direct costs for hosting $2,400, monitoring $2,200, failed integrations $1,800, interface changes $2,600, credentials $900, security updates $1,800, incident expectations $1,600, mappings $1,200, data quality $1,500, customer support $1,200, and periodic validation $1,400. Annual cost is **$34,350**; the $38,000 fee leaves **$3,650**. This thin margin matters. The underpriced-support scenario retains positive implementation contribution but raises annual cost above fee, producing NO DEAL.

## 13. Scenario test

Factories return new frozen records; baseline never mutates.

| Scenario | Result | Lesson |
|---|---|---|
| A — Baseline | **NO DEAL** | $155,026 recovery still fails one-year implementation payback. |
| B — Vendor-supported interfaces | **PROMISING — VALIDATE IN DISCOVERY** | Documented approved interfaces and usable tests cut delivery to 661 hours and support cost. |
| C — Difficult proprietary integration | **NO DEAL** | Delivery rises to 1,391 hours; implementation and support economics fail. |
| D — High customer value | **POOR TARGET CUSTOMER** | Recovery rises to $279,046.80 while delivery stays 946 hours; sales/procurement gates remain. Value alone is not permission to ignore the rest. |
| E — Vendor-supported product/module | **BUY / CONFIGURE** | A supported alternative meets most need at lower modeled total cost/risk. |
| F — Underpriced support | **NO DEAL** | Attractive implementation contribution cannot fund $54,800 expected annual support. |
| G — Narrow read-only scope | **PROMISING — VALIDATE IN DISCOVERY** | Recovery falls to $85,264.30, but delivery falls to 344 hours and support to $16,300. |
| H — High reuse / high validation | **NO DEAL** | More reusable core does not remove 310 validation/testing hours or restore contribution. |

An unresolved-access variant also demonstrates **INVESTIGATE**. Thus assumptions can drive INVESTIGATE, POOR TARGET CUSTOMER, NO DEAL, or BUY / CONFIGURE without a healthcare-specific verdict override.

### Scope reduction as an economic tool

Deep integration offers $155,026 recovery, costs 946 hours to deliver, costs $34,350 annually to support, and returns NO DEAL. Stable read-only exports offer only $85,264.30 recovery but require 344 hours, cost $16,300 annually to support, and return PROMISING. Smaller scope reduces value **and** engineering, test exposure, sensitive-data surface, uncertainty, and support. Existing systems remain authoritative in both cases.

### Case 7 vs. Case 11

Case 7 has meaningful handoff burden, operational consequences, moderate integrations, and an accessible buyer. Case 11 has larger recoverable burden, high sensitivity, more constrained integrations, much more validation, and higher support expectations. The comparison deliberately shows value, delivery, integration, support, and verdict separately. There is no composite score. The question is where extra value stops compensating for extra delivery complexity.

### Case 9 → Case 10 → Case 11

- **Case 9:** the project may be good, but procurement makes the customer unattractive.
- **Case 10:** the department may want the project, but authority/governance blocks execution.
- **Case 11:** the customer may want and authorize the project, but delivery/support complexity can still break the economics.

The implemented-case comparison now contains Cases 1–11 with explainable value, delivery difficulty/hours, reuse, procurement, support in each case model, and framework verdict—never an opportunity score.

## 14. Verdict

**NO DEAL.** The exact framework reason is:

- The customer does not recover implementation price within one year.

This is not forced negative because the domain is healthcare; it follows the same ordered gates as every case. High value does not cancel high cost. Sensitive integrations require more than features. Minimization can reduce risk and economics. Supported products may win. Scope reduction can rescue a deal. Reusable code cannot reuse customer validation. Recurring revenue must fund recurring obligations. A good project is not automatically a good market.

---

[← Previous: Case 10 — The University Department](10-university.md) · [Book home](../README.md) · [Next: Case 12 — The Perfect-Looking Deal That Isn't](12-buy-dont-build.md)
