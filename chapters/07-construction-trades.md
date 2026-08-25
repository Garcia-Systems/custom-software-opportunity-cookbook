# Case 7 — The Construction / Trades Company

> Every company, workflow, and number below is a fictional educational assumption—not an industry benchmark, forecast, or recommendation.

## 1. Business

**James River Mechanical** is a fictional regional residential and light-commercial contractor with 44 employees, seven field crews, one office/operations team, and dozens of active jobs. The owner, general manager, operations manager, office manager, estimator, field supervisor, and accounting lead are reachable stakeholders; procurement is assumed to be moderate rather than institutional.

Its lead-to-cash workflow is **Lead → Estimate → Job → Schedule → Crew → Materials → Completion → Invoice → Payment**.

## 2. Problem

Lead information is re-entered for estimates; accepted estimates are manually made into jobs; job and crew details are copied into scheduling; material requirements move separately; completion signals reach billing late; status reports require spreadsheet reconciliation; errors require correction; and office staff chase field status. The hypothesis is not that every handoff should disappear. It is that repeated administration, rework, correction, and delay may create measurable recoverable value.

## 3. Current systems

CRM/leads, estimating, scheduling/dispatch, field communication, purchasing/material workflows, accounting, and spreadsheets remain authoritative. The proposed pattern is:

```text
SYSTEM OF RECORD A
        ↓ validated event / data
CUSTOM INTEGRATION LAYER
        ↓ normalized customer/job identity
SYSTEM OF RECORD B
        ↓
logged handoff or human exception
```

This orchestrates transitions; it does not replace the systems of record.

## 4. Current-state economic burden

Each labor row is `fictional hours/week × 52 × loaded cost`; error correction is `incidents × average correction cost`. There is no handoff score.

| Burden | Calculation | Annual burden |
|---|---:|---:|
| Duplicate entry | 12 × 52 × $38 | $23,712.00 |
| Estimate-to-job reconciliation | 8 × 52 × $45 | $18,720.00 |
| Scheduling coordination | 7 × 52 × $42 | $15,288.00 |
| Materials/purchasing coordination | 5 × 52 × $40 | $10,400.00 |
| Field-to-office reconciliation | 9 × 52 × $40 | $18,720.00 |
| Completion-to-invoice administration | 6 × 52 × $38 | $11,856.00 |
| Error correction/rework | 72 × $240 | $17,280.00 |
| Management status reporting | 4 × 52 × $50 | $10,400.00 |
| Invoice-delay financing cost | $2,400,000 × 8/365 × 8% | $4,208.22 |
| **Total** | | **$130,584.22** |

Invoice delay is treated carefully. The fictional invoice flow is not lost revenue. Faster invoice creation can reduce administration, improve visibility, and reduce a financing/cash-conversion cost. Only the modeled financing cost is included; **none of the $2.4 million invoice principal is claimed as newly created value**, and actual lost revenue is assumed to be zero.

## 5. Potential recoverable value

Human judgment remains. The model applies 65% to duplicate entry, 55% to estimate/job and field/office reconciliation, 40% to scheduling, 35% to materials and errors, 50% to billing administration and reporting, and 40% to the timing financing cost. `Burden × improvement` yields **$64,619.29 annual recoverable value**, not 100% automation.

## 6. Solution

The smallest useful intervention synchronizes lead/customer identifiers, hands an accepted estimate into a normalized job identity, passes validated job/status/scheduling and material-requirement data, receives field completion, emits an invoice-ready signal, and provides logging, idempotency, retry/error handling, validation, an exception queue, and a management workflow briefing.

It is explicitly **connect systems, not replace everything**. It is not a CRM, estimator, dispatcher, field-service app, accounting package, ERP, payroll, purchasing system, or mobile workforce app.

## 7. Build vs. buy

Discovery must compare: (1) field-service/construction-management SaaS, (2) CRM/estimating suite expansion, (3) accounting integrations, (4) native vendor integrations, (5) automation/low-code, (6) process redesign, (7) better spreadsheets, (8) narrow custom integration, (9) full replacement, and (10) doing nothing. Mature vertical SaaS may solve the workflow adequately; the SaaS scenario therefore returns **BUY / CONFIGURE**. Full replacement is substantially more expensive and risky than the narrow hypothesis.

In the baseline, the fictional alternative's first-year effect is $164,000 (setup, subscription, internal administration, unresolved burden, and risk) versus a $139,964.93 custom effect (custom spend, residual burden, and risk). That comparison—not a claim that SaaS is incapable—sets the framework's baseline custom finding.

## 8. Delivery

Delivery is 24h technical discovery + 36h API validation + 104h adapters + 34h identity normalization + 58h orchestration + **48h reliability/error handling** + 34h exceptions + 22h documentation + **54h QA/testing** + 16h deployment + 36h rework reserve = **466 hours**. At $85/hour plus $2,500 other direct cost, delivery costs **$42,110**. Reliability is material because a broken job or invoice-ready handoff has greater operational consequences than a broken read-only report—without inventing a distributed workflow platform.

## 9. Reuse

Of 360 core hours (before QA, deployment, and reserve), 190 are reusable (**52.8%**) and 170 customer-specific. Candidate reuse includes adapter structure, identity/event patterns, validation, idempotency, retries, logging/monitoring, exceptions, and deployment tooling. Customer-specific mappings, estimate rules, job states, scheduling, materials, accounting, and exceptions remain substantial. The customer-specific scenario falls below 40% reuse and becomes a viable **ONE-OFF CUSTOM PROJECT**, not evidence of a repeatable market.

## 10. Deal economics

Implementation is **$50,000** and the annual recurring fee **$12,000**. First-year spend is $62,000; retained annual benefit after the recurring fee is **$52,619.29**; first-year ROI is approximately **4.2%**; payback is approximately **11.4 months**. After delivery and 88 solutions hours at $70, implementation contribution is **$1,730**, or **$19.66 per solutions hour**. Those thin margins make validation important.

## 11. Market / sales

The modeled 88 solutions hours include prospecting/sales (8), discovery (10), workflow mapping (14), stakeholder interviews (12), feasibility (12), requirements/scoping (10), design (10), proposal (5), coordination (4), and acceptance (3). Meaningful burden plus an accessible owner and moderate contracting may be interesting, but workflow discovery is demanding and “why not configure the incumbent?” must be answered.

## 12. Support

Annual support is 92 engineering hours × $85 plus $1,800 hosting/monitoring and $1,200 vendor/incident costs = **$10,820**, leaving **$1,180 recurring contribution**. Obligations include API and schema changes, failed handoffs, expired credentials, mapping/workflow changes, monitoring, customer support, defects, and maintenance engineering. The unsustainable-support scenario raises cost above the unchanged fee and returns NO DEAL.

## 13. Scenario test

All factories return new frozen records and leave the baseline unchanged.

| Scenario | Framework result | Observation |
|---|---|---|
| Baseline contractor | PROMISING — VALIDATE IN DISCOVERY | Value, contribution, support, and reuse clear the ordered gates, narrowly. |
| Existing SaaS solves workflow | BUY / CONFIGURE | Adequate lower-cost/risk vertical SaaS wins. |
| Clean APIs / standardized systems | PROMISING — VALIDATE IN DISCOVERY | Delivery and support costs fall. |
| Closed / difficult integrations | NO DEAL | Validation, adapters, reliability, QA, reserve, and support rise materially. |
| High administrative burden | PROMISING — VALIDATE IN DISCOVERY | Explicit labor burden strengthens value. |
| Low administrative burden | NO DEAL | Efficient current processes cannot repay implementation within a year. |
| Highly customer-specific | ONE-OFF CUSTOM PROJECT | Engagement works, but derived core reuse is below 40%. |
| Unsustainable support | NO DEAL | The unchanged recurring fee does not cover support. |

## 14. Verdict

**PROMISING — VALIDATE IN DISCOVERY.** Exact framework reasons:

- “Customer value, delivery contribution, and recurring support economics work under the assumptions.”
- “At least 40% of core engineering work is modeled as demonstrably reusable.”
- “Promising is an economic hypothesis; market validation still requires discovery.”

Handoffs can be expensive; integration can automate transitions without replacing authoritative systems; and operational writes require stronger reliability. But mature SaaS is the principal competitor, customer rules can destroy repeatability, and an accessible buyer does not rescue weak economics.

### Emerging pattern and discovery questions

Cases 1–6 primarily examine reporting/analytics integration across restaurants, hotels, tourism, and retail. Case 7 examines workflow/handoff integration that removes repeated operational work rather than only improving visibility. That **may** support stronger recoverable value, but one fictional case cannot establish a market. Real discovery must determine which handoffs recur, which system combinations recur, actual API/export/write permissions, measured administration, what vertical SaaS already solves, willingness to pay, workflow similarity, and the remaining customer-specific logic. This distinguishes a good project from a good market without claiming either conclusion.

---

[← Previous: Case 6 — The Multi-Location Retailer](06-multi-location-retail.md) · [Book home](../README.md) · [Next: Case 8 — The Professional Services Firm →](08-professional-services.md)
