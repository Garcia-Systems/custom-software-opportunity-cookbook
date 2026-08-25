# Case 14 — Great Product, Bad Sales Motion

> **Fictional educational scenario.** James River Professional Association, every organization, figure, price, labor rate, close rate, and cycle below is invented. They are assumptions to validate, not benchmarks.

## 1. Business

The modeled target is **regional membership associations** with roughly 1,500–3,000 members and small administrative teams. James River Professional Association represents a mature-market customer with 2,200 members.

## 2. Problem

Staff reconcile event registrations to members, re-enter data, reconcile accounting, report membership status, assemble board reports, align email lists, and administer spreadsheets. The annual burden is **$17,628**; avoidable work makes the problem meaningful even though each contract is small.

## 3. Current systems

Membership-management SaaS, event registration, email/communications, accounting, website/forms, and spreadsheets each hold part of the truth. No real vendor connection or customer data is used.

## 4. Current-state burden

| Workflow | Annual hours | Cost | Recovery | Recoverable |
|---|---:|---:|---:|---:|
| Event/member reconciliation | 95 | $3,040 | 62% | $1,884.80 |
| Duplicate entry | 80 | $2,400 | 70% | $1,680.00 |
| Accounting reconciliation | 78 | $2,808 | 55% | $1,544.40 |
| Membership-status reporting | 65 | $2,210 | 65% | $1,436.50 |
| Management/board reporting | 70 | $2,800 | 60% | $1,680.00 |
| Email-list reconciliation | 55 | $1,650 | 65% | $1,072.50 |
| Spreadsheet administration/rework | 85 | $2,720 | 60% | $1,632.00 |

## 5. Recoverable value

Modeled annual recoverable value is **$10,930.20**. This excludes speculative revenue and preserves unrecoverable work.

## 6. Solution

```text
Membership SaaS ─┐
Events ──────────┤
Email ───────────┼─> reusable integration layer -> normalized member/event view
Accounting ──────┤                                      |
Forms / website ─┘                              reporting / exceptions
```

The executable evaluates this opportunity; it does not build association software, a CRM, or a pipeline tool.

## 7. Build vs. buy

The fictional comparison considers existing SaaS, configuration, automation, narrow integration, and doing nothing. The baseline assumes none supplies the cross-system normalized view economically. Discovery must challenge that assumption before custom is justified.

## 8. Delivery

The partner already has an account shell, import framework, adapter patterns, CSV normalization, validation, logging, monitoring, reporting shell, pipeline, and membership/event domain model. A first customer would fund more foundation work; this representative **later customer** takes 45 hours and **$3,500** direct cost. At a $7,000 implementation price, implementation contribution is **$3,500**.

## 9. Reuse

| Reusable (80% of core work) | Customer-specific (20%) |
|---|---|
| adapters, normalization, reporting, validation | credentials and field mapping |
| deployment, monitoring, domain model | minor rules, report configuration, acceptance |

Engineering reuse is not sales reuse. Sales reuse requires the same ICP, pain, buyer, demo, scope, proposal, and procurement motion. Product-like delivery does **not** automatically create product-like selling.

## 10. Customer/deal economics

Implementation is **$7,000**, recurring is **$2,000**, and first-year retained benefit is **$1,930.20**. First-year ROI is **21.4%** and implementation payback is **9.4 months**. Annual support costs **$900**, leaving **$1,100** recurring contribution. Contribution before acquisition is therefore **$4,600**.

## 11. Market / sales

Account research, outreach, call, discovery, demo, follow-up, technical validation, stakeholder meeting, proposal, committee review, onboarding, contract coordination, and scheduling consume **28 hours per qualified opportunity**. At a **20%** qualified close rate, the modeled 7-month cycle also occupies follow-up capacity, delays cash, lowers throughput, and increases forecast uncertainty. Months are not arbitrarily converted to dollars.

## 12. Acquisition economics

```text
28 hours/opportunity ÷ 20% close probability = 140 expected hours/win
140 hours × $65 solutions cost              = $9,100 expected acquisition cost
$3,500 implementation + $1,100 recurring    = $4,600 before acquisition
$4,600 - $9,100                             = -$4,500 after acquisition
```

The customer maximum implementation price preserving $3,400 retained first-year benefit is **$5,530.20**. The minimum covering delivery, acquisition, $2,000 required contribution, less $1,100 recurring contribution is **$13,500**. The corridor is not feasible. “Just charge more” transfers inefficient acquisition to a customer whose economics cannot absorb it.

## 13. Support

Ten support hours at $60 plus $300 hosting/monitoring obligations cost **$900** against the $2,000 fee. Support remains visible and sustainable; it is not the failure point.

## 14. Scenario tests

| Immutable scenario | Change | Contribution after acquisition | Verdict / observation |
|---|---|---:|---|
| Baseline outbound | 28 h, 20%, 7 months | -$4,500 | **POOR TARGET CUSTOMER** |
| Warm referral | 7 h, 70%, 2 months | $3,950 | **PROMISING — VALIDATE IN DISCOVERY**; same software/delivery |
| Higher close rate | 50% | $960 | Improves materially but remains **POOR TARGET** under the required contribution/corridor |
| Productized sales | 7 h, 45%, 2.5 months | $3,588.89 | **PROMISING**; standard demo/scope/price/proposal/onboarding |
| Larger customer | doubled burden; $14,500 + $3,500 | $8,028.57 | **PROMISING**; moving upmarket can work here, not universally |
| Higher price only | $12,000, no added value | $500 | Customer one-year gate fails: **NO DEAL** |
| Very high engineering reuse | 18 total hours; sales unchanged | -$2,610 | **POOR TARGET**; code efficiency cannot compensate indefinitely |
| Partner/channel | 4 h, 65%, $700 channel cost | $3,500 | **PROMISING**; channel cost is explicit |

Close-rate denominator sensitivity (28 hours/opportunity, $65/hour) is deterministic:

| Close rate | Expected hours/win | Acquisition cost |
|---:|---:|---:|
| 10% | 280.00 | $18,200.00 |
| 20% | 140.00 | $9,100.00 |
| 30% | 93.33 | $6,066.67 |
| 50% | 56.00 | $3,640.00 |

**Good project vs. good market:** referred customer + same software + same delivery = good project. Cold outbound + same software + same delivery + expensive motion = poor market.

### Case 13 vs. Case 14

| | Customer value | Delivery | Reuse | Sales | Failure |
|---|---|---|---|---|---|
| Case 13 | strong | expensive | weak/moderate | manageable | **BUILD** |
| Case 14 | strong | cheap | high | expensive | **ACQUIRE** |

### Case 9 vs. Case 14

Case 9 is difficult because institutional procurement is itself a barrier. Case 14 has no single catastrophic barrier: ordinary selling and committee/onboarding effort simply cost too much relative to a small contract. Procurement failure and acquisition-unit-economics failure are related but distinct.

## 15. Verdict

**POOR TARGET CUSTOMER** for baseline outbound. Exact framework reasons:

- Expected customer acquisition effort is too high relative to contract value.
- Contribution after expected acquisition cost is below the required contribution.
- The acquisition-adjusted minimum price exceeds the customer's economic maximum.

Customer value, delivery, reuse, and support are good. The target market motion is not. **A great implementation is not necessarily a great business**, and many technically similar customers are insufficient without repeatable acquisition.

---

[← Previous: Case 13 — Great Customer Value, Bad Delivery Economics](13-bad-delivery-economics.md) · [Book home](../README.md) · [Next: Chapter 15 — Where Custom Software Deserves to Exist →](15-cross-case-synthesis.md)
