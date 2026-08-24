# Case 4 — The Small Hotel Group

> **Fiction notice:** James River Lodging Group and every room count, workflow, hour, cost, price, percentage, and result below are fictional educational assumptions—not hotel-industry benchmarks, market research, or financial advice.

**Core question:** Does hotel-integration economics improve materially when several properties share ownership, management, reporting needs, and some systems? This case is deliberately paired with Case 3, but does not multiply Case 3 by four.

## 1. Business

James River Lodging Group is a fictional common owner of four properties and approximately 528 rooms. A small central team oversees a mix of leisure and business demand. The properties share two common PMS/export patterns and reporting needs, while housekeeping, staffing, channel mix, mappings, and local conditions vary.

## 2. Problem

A property asks, “What is happening here?” The group asks, “Which property differs, by how much, and where should management investigate?” Property teams repeatedly reconcile local data; central management then cleans inconsistent exports, reconciles KPI definitions, and rebuilds comparisons. Delayed group exception visibility is a separate problem from four local briefings.

## 3. Current systems

```text
PROPERTY 1 ── PMS / housekeeping / staffing / channels ──┐
PROPERTY 2 ── PMS / housekeeping / staffing / channels ──┤
PROPERTY 3 ── PMS / housekeeping / staffing / channels ──┼──→ CENTRAL MANAGEMENT
PROPERTY 4 ── PMS / housekeeping / staffing / channels ──┘    manual consolidation
```

API access may vary by property or PMS version. Vendor approval, integration fees, export-only access, rate limits, and credential administration must be validated rather than inferred from ownership.

## 4. Current-state burden

Property work uses `hours/property/week × loaded cost × 52 × 4`; central work is modeled once and is not multiplied by property count.

| Fictional burden | Formula | Annual burden |
|---|---:|---:|
| Property reconciliation | 5 h × $45 × 52 × 4 | $46,800 |
| Housekeeping comparison | 4 h × $32 × 52 × 4 | $26,624 |
| Staffing visibility | 2.5 h × $44 × 52 × 4 | $22,880 |
| Booking-channel analysis | 2.5 h × $46 × 52 × 4 | $23,920 |
| **Property-level subtotal** | | **$120,224** |
| Central consolidation | 12 h × $58 × 52 | $36,192 |
| Central reporting | 7 h × $52 × 52 | $18,928 |
| Data/KPI normalization | 6 h × $48 × 52 | $14,976 |
| Delayed anomaly investigation | 4 h × $60 × 52 | $12,480 |
| **Central subtotal** | | **$82,576** |
| **Total** | calculated | **$202,800** |

The larger-group scenario adds explicit central-consolidation growth; not every central burden scales linearly.

## 5. Recoverable value

No recoverable total is entered by hand. Each result is `burden × fictional improvement`: property reconciliation 55% ($25,740), housekeeping 30% ($7,987.20), staffing 25% ($5,720), channel analysis 35% ($8,372), central consolidation 65% ($23,524.80), reporting 55% ($10,410.40), normalization 60% ($8,985.60), and anomaly investigation 30% ($3,744). **Total recoverable annual value is $94,484.** Changing a burden or improvement changes the result.

## 6. Solution

The smallest useful intervention is a shared ingestion framework with PMS/export adapters, property identifiers, channel/housekeeping/staffing normalization, a shared operating model, deterministic cross-property metrics, validation/logging, scheduled imports, and a central briefing.

```text
PROPERTIES 1–4 → SHARED INTEGRATION LAYER → property normalization
                  → group operating model → cross-property briefing
```

It is not a PMS, booking engine, channel manager, workforce tool, housekeeping app, revenue-management system, CRM, AI recommendation system, or generic hotel dashboard.

## 7. Build vs. buy

Discovery must seriously compare (1) PMS-native group reporting, (2) hotel analytics SaaS, (3) central BI/configuration, (4) channel-management reporting, (5) automation/low-code, (6) spreadsheet/process improvement, (7) narrow custom integration, and (8) doing nothing. Baseline assumes these leave a residual cross-system gap; it does not assume custom is inherently best. When the strong-SaaS scenario says an adequate lower-risk product exists, the same framework returns **BUY / CONFIGURE**. Greater group value and stronger SaaS competition can coexist.

## 8. Delivery

Delivery is executable `shared + per-property + exception + QA + deployment + reserve`, not Case 3 hours × 4.

| Work | Hours |
|---|---:|
| Shared architecture, import framework, model, validation/logging, reporting shell, pipeline, adapter pattern | 130 |
| Configuration, credentials, mappings, status normalization, validation, onboarding | 18 × 4 = 72 |
| Second pattern and property-specific exceptions | 38 |
| QA / testing | 32 |
| Deployment | 14 |
| Rework reserve | 28 |
| **Total** | **314** |

At fictional $75/hour plus $2,200 other costs, direct delivery is **$25,750**. Moderate standardization assumes two common patterns and property-specific mappings. High standardization cuts per-property work to 10 hours and exceptions to 10; fragmentation raises them to 30 and 180. Permissions, risk, support, and integration count change too. Thus standardization matters more than raw count.

## 9. Reuse

Within this customer, the 130 shared hours serve four properties and calculated core reuse is **54.2%**. That materially helps this deal. It is not market validation: another group can have different PMSs, versions, access rights, channels, mappings, identifiers, and reporting rules. Reuse across properties and reuse across future customers are distinct claims.

## 10. Deal economics

Implementation price is **$48,000** and annual fee **$15,000**. First-year cost is $63,000; retained first-year benefit is **$31,484**, first-year ROI **50.0%**, steady-state retained benefit $79,484, and payback **7.2 months**.

The 76 solutions hours include 8 prospecting/sales, 8 discovery, 8 central interviews, 12 selected-property discovery, 10 design, 10 technical validation, 6 proposal/scoping, 8 coordination, and 6 acceptance. One ownership group creates one relationship and contract—not four sales processes—although stakeholder and discovery breadth rise. Delivery and solutions labor leave **$17,310** contribution, or **$227.76/solutions hour**.

## 11. Market / sales

Compared with selling four independent hotels, the group offers one buyer, sponsor, contract, and deployment program, shared discovery, and larger recoverable value. Against that: more stakeholders, possible central IT/vendor approval, operational variance, and higher perceived implementation risk. The model uses one 76-hour commercial effort rather than four Case 3 efforts (232 hours), while acknowledging broader discovery.

A good project is not automatically a good market. Repeatability still requires evidence about common shared PMS environments, unresolved central reporting, SaaS adequacy, access patterns, buying authority, willingness to pay, and similarity between deployments.

## 12. Support

Recurring revenue is not pure contribution. Fixed support is 24 hours plus $2,200 for hosting, monitoring, account management, and the environment: **$4,000**. Property-scaled and exception support is 48 hours plus $1,200: **$4,800**. Total recurring cost is **$8,800**, leaving **$6,200** contribution on the $15,000 fee. Scaled work covers failures, mapping drift, vendor changes, tickets, and data quality.

## 13. Scenario test

Every scenario constructs new frozen records; baseline remains unchanged.

| Scenario | Key change | Delivery | Verdict |
|---|---|---:|---|
| Baseline four-property | moderate standardization | $25,750 | PROMISING — VALIDATE IN DISCOVERY |
| Independent-hotel comparison | one property / Case 3 inputs | $18,750 | NO DEAL |
| Highly standardized | common PMS/exports/definitions/processes | $19,600 | PROMISING — VALIDATE IN DISCOVERY |
| Fragmented acquired portfolio | multiple configurations, identifiers and exceptions | $43,725 | NO DEAL |
| Strong multi-property SaaS | adequate lower-risk product | $25,750 | BUY / CONFIGURE |
| Larger eight-property group | shared infrastructure remains 130 hours | $30,025 | PROMISING — VALIDATE IN DISCOVERY |

### Calculated Case 3 versus Case 4

| Metric | Case 3 | Case 4 |
|---|---:|---:|
| Properties | 1 | 4 |
| Current burden | $94,196 | $202,800 |
| Recoverable value | $35,342.80 | $94,484 |
| Engineering hours | 230 | 314 |
| Implementation price | $30,000 | $48,000 |
| Solutions hours | 58 | 76 |
| Annual support cost | $6,750 | $8,800 |
| Core reuse | 44.3% | 54.2% |
| Payback | 13.7 months | 7.2 months |
| Verdict | NO DEAL | PROMISING — VALIDATE IN DISCOVERY |

Here value rises 2.67× while delivery hours rise 1.37× because central burden is real and shared work is not repeated. That supports the hypothesis only under these fictional moderate-standardization assumptions; fragmentation reverses the result.

## 14. Verdict

Baseline is **PROMISING — VALIDATE IN DISCOVERY**, derived by the common gates because customer value clears price and fee, implementation covers delivery and solutions labor, recurring fees cover support, sales friction is not high, and core reuse exceeds 40%. “Promising” is not a predetermined conclusion or market proof. The fragmented case is **NO DEAL**, and adequate SaaS is **BUY / CONFIGURE**.

Central lessons: scale can improve economics without multiplying delivery; standardization dominates raw count; one commercial relationship helps sales economics; SaaS competition strengthens with size; and within-customer reuse is not evidence of a repeatable market.

### Real discovery questions

- How common are shared PMS versions, exports, identifiers, and reporting definitions across owned properties?
- Which central reporting questions remain unresolved after PMS-native, analytics SaaS, BI, channel, low-code, or process options?
- What API/export permissions, fees, rate limits, vendor approvals, and credential practices apply property by property?
- Which burdens are measured, non-overlapping, and genuinely recoverable; which management decisions change?
- Who owns the budget and can approve one group contract? Which property and central stakeholders accept it?
- What is willingness to pay, expected support response, onboarding cadence, and vendor-change exposure?
- Which adapter and mapping work actually repeats across other hotel groups rather than only inside this one?

## Run it

```bash
python examples/hotel_group.py
```

[Previous: Case 3](03-independent-hotel.md) · [Book home](../README.md) · [Next: Case 5 — The Tourism / Attraction Operator](05-tourism-attraction.md)
