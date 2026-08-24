# Case 2 — The Five-Location Restaurant Group

[Previous: Case 1](01-independent-restaurant.md) · [Book home](../README.md) · Next: Case 3 — planned

> **Fiction notice:** James River Hospitality Group and every operational, effort, and financial value below are fictional educational assumptions. They are neither Williamsburg restaurant-group data nor industry benchmarks.

## 1. Business

James River Hospitality Group is a fictional common owner of five restaurants. Their volumes, menus, hours, staffing, inventory, and reservation intensity differ, but ownership, management, several systems, and reporting needs overlap. This paired experiment asks whether Case 1's integration problem becomes a substantially better opportunity at five locations—not whether five is automatically five times better.

## 2. Problem

Case 1 asks, “What happened here?” The group asks, “What happened across the group, which locations differ, why, and where should management investigate?” Managers repeatedly manipulate exports, normalize location definitions, reconcile sales and labor, compare waste and purchasing, and look for anomalies. The group-level comparison and central management delay are new burdens, not five copies of a single-location spreadsheet.

The experiment explicitly asks whether burden, recoverable value, implementation, support, sales, reusable work, exceptions, willingness to pay, and management visibility scale at the same rates. They do not in the baseline.

## 3. Current systems

```text
LOCATION 1 ── POS / labor / inventory / reservations ──┐
LOCATION 2 ── POS / labor / inventory / reservations ──┤
LOCATION 3 ── POS / labor / inventory / reservations ──┼──→ MANUAL GROUP REPORTING
LOCATION 4 ── POS / labor / inventory / reservations ──┤
LOCATION 5 ── POS / labor / inventory / reservations ──┘
```

Operational systems already function. Some are common; configurations, exports, identifiers, and data quality can still vary by location. Management currently supplies the missing group model manually.

## 4. Current-state economic burden

The executable keeps per-location and group-level assumptions distinct.

| Editable fictional assumption | Scope | Unit burden | Five-location burden |
|---|---|---:|---:|
| Location reconciliation labor | Per location | $7,000 | $35,000 |
| Repeated location reporting | Per location | $3,500 | $17,500 |
| Waste / purchasing inefficiency | Per location | $9,000 | $45,000 |
| Labor-planning inefficiency | Per location | $7,200 | $36,000 |
| Central management consolidation | Group | $26,000 | $26,000 |
| Delayed group anomaly detection | Group | $14,000 | $14,000 |
| **Total** |  |  | **$173,500** |

Location-level burden is **$133,500** and group-level burden is **$40,000**. Group consolidation is entered once, not multiplied by five. In the ten-location thought experiment it grows by an explicit $3,500 for each location beyond five, illustrating a nonlinear editable assumption rather than hiding a universal formula.

## 5. Potential recoverable value

Recovery is derived component by component.

| Component | Credible improvement | Recoverable |
|---|---:|---:|
| Location reconciliation | 60% | $21,000 |
| Repeated reporting | 50% | $8,750 |
| Waste / purchasing | 20% | $9,000 |
| Labor planning | 22% | $7,920 |
| Central consolidation | 65% | $16,900 |
| Delayed anomaly detection | 25% | $3,500 |
| **Total** |  | **$67,070** |

```text
CURRENT-STATE BURDEN × CREDIBLE IMPROVEMENT = RECOVERABLE VALUE
```

Burden is not value. The proposed layer cannot remove every root cause, guarantee management action, or turn every anomaly into savings.

## 6. Solution

The smallest useful intervention is shared ingestion/imports, adapters for selected existing systems, location-aware normalization and common identifiers, deterministic cross-location metrics, a simple management briefing, scheduled ingestion, validation, logging, and actionable error reporting.

```text
LOCATION 1 ──┐
LOCATION 2 ──┤
LOCATION 3 ──┼──→ SHARED INTEGRATION LAYER → normalized group model
LOCATION 4 ──┤                                  ↓
LOCATION 5 ──┘                         cross-location reporting
                                                   ↓
                                          management briefing
```

It is not a POS, reservations, scheduling, inventory, CRM, ERP, recommendation, forecasting, mobile, or complex dashboard product. This repository evaluates the fictional engagement; it does not build that integration.

## 7. Build vs. buy

| Alternative | Serious discovery question |
|---|---|
| Existing multi-location analytics SaaS | Does a mature product already normalize the relevant systems and comparisons at lower cost and risk? |
| Vendor-native enterprise reporting | Could consolidating on a vendor or enabling enterprise reports close enough of the gap? |
| Configuration | Can current tools and identifiers be configured without custom code? |
| Automation tooling | Can low-code flows reliably move and reconcile exports? |
| Manual process | Is clearer ownership or a better workbook sufficient? |
| Custom integration | Is the unresolved cross-system management briefing valuable enough to own its adapter and support risk? |

SaaS competition may be *stronger* for a group than for Case 1. The baseline assumes a review leaves a material cross-system gap, but this is fictional and requires discovery. When the immutable strong-SaaS scenario marks an existing alternative adequate, the same verdict engine returns **BUY / CONFIGURE**. More customer value does not grant custom software a waiver from alternatives.

## 8. Delivery

Five locations do not cause five copies of all engineering:

| Executable category | Calculation | Hours |
|---|---:|---:|
| Fixed/shared architecture, adapter framework, normalization, reporting shell, logging/validation, pipeline | Once | 100 |
| Location mapping, credentials, configuration, and validation | 10 × 5 | 50 |
| Customer-specific exceptions and unusual rules | Explicit reserve | 30 |
| QA/testing | Once across the engagement | 24 |
| Deployment | Shared deployment | 10 |
| Rework reserve | Engagement reserve | 20 |
| **Total** |  | **234** |

At $75 per hour plus $1,450 other direct costs, direct implementation cost is **$19,000**. Multiplying Case 1's 150 hours by five would produce 750 hours; the model instead exposes shared, incremental, and exceptional work. Standardization scenarios modify the latter two without touching the shared baseline architecture.

## 9. Reuse

**Reuse across locations is not reuse across customers.** Within this engagement, 100 shared hours serve all five locations. Against 180 core hours, the Chapter 0 reuse ratio is **55.6%**. That improves this project's delivery economics.

Potential cross-customer reuse remains unproven. Another group may use different vendors, mappings, identifiers, configuration, exports, and business rules. Common frameworks may travel, but no future sales or portability value is booked. Repeated paid discovery must establish cross-customer reuse.

## 10. Deal economics

### Customer

| Measure | Calculated baseline |
|---|---:|
| Current-state annual burden | $173,500 |
| Recoverable annual value | $67,070 |
| Implementation price | $42,000 |
| Annual recurring fee | $9,000 |
| First-year customer cost | $51,000 |
| Retained first-year benefit | $16,070 |
| Steady-state annual benefit | $58,070 |
| First-year ROI | 31.5% |
| Implementation payback | 8.7 months |

These reuse Chapter 0 exactly: steady-state benefit is recoverable value less recurring fee; ROI is first-year net gain divided by first-year spend; payback is implementation price divided by net annual benefit.

### Engineering partner

Shared 100 + incremental 50 + exceptions 30 + QA 24 + deployment 10 + reserve 20 equals **234 hours**. At the fictional cost and direct expenses, implementation delivery cost is **$19,000**.

### Solutions organization

| Activity | Hours |
|---|---:|
| Prospecting/sales | 7 |
| Discovery | 8 |
| Multi-location process discovery | 7 |
| Solution design/scoping | 10 |
| Commercial/proposal | 5 |
| Coordination | 9 |
| Acceptance | 6 |
| **Total** | **52** |

At $65 internal hourly cost, implementation contribution after delivery and solutions labor is **$19,620**, or **$377.31 per solutions hour**. This is more than Case 1's 28 solutions hours, but nowhere near five times 28.

## 11. Market / sales

```text
SELL FIVE SEPARATE RESTAURANTS       SELL ONE FIVE-LOCATION GROUP
five buyer relationships            one ownership group
five discovery/proposal motions     one coordinated discovery/proposal motion
five contracts/procurements         one contract/procurement motion
fragmented value                    larger combined value
```

The concentration advantage is one commercial relationship covering repeated workflows. It is not simply that a larger customer “has more money.” More stakeholders, managers, operational variation, coordination, and implementation risk partly offset the advantage.

A good **project** is not yet a good **market**. Discovery must learn how many similar reachable groups exist, which systems they use, whether unresolved mappings repeat, whether SaaS already solves enough, and whether willingness to pay repeats. This chapter makes no market-validation claim.

## 12. Support

Fixed monitoring, hosting, and account obligations coexist with per-location failures, data-quality exceptions, onboarding, vendor changes, and support requests.

| Obligation | Calculation | Annual amount |
|---|---:|---:|
| Fixed support labor | 18 hours | 18 hours |
| Per-location labor | 8 × 5 | 40 hours |
| Exception labor | Explicit | 10 hours |
| Fixed non-labor | Hosting/monitoring | $1,300 |
| Per-location non-labor | $100 × 5 | $500 |

Sixty-eight hours at $75 plus $1,800 makes annual direct support cost **$6,900**. Against $9,000 recurring revenue, recurring contribution is **$2,100**. Revenue is not pure profit, and location growth requires pricing to keep pace with real obligations.

## 13. Scenario test

All factories return new frozen records; no scenario mutates the baseline.

| Scenario | Key calculated change | Verdict |
|---|---|---|
| Baseline five-location group | 234 engineering hours; $19,000 delivery cost | **PROMISING — VALIDATE IN DISCOVERY** |
| Single-location comparison | Imports Case 1 factory: 150 hours; weak customer payback | **NO DEAL** |
| High standardization | Per-location 5 hours, exceptions 12; 191 total hours; $15,775 delivery cost | **PROMISING — VALIDATE IN DISCOVERY** |
| Low standardization | Per-location 20 hours, exceptions 90; 344 hours; $27,250 delivery cost; reuse falls below 40% | **ONE-OFF CUSTOM PROJECT** |
| Strong SaaS alternative | Adequate lower-cost/lower-risk alternative | **BUY / CONFIGURE** |
| Ten-location growth thought experiment | Shared work remains 100 hours; 279 total; support rises to $10,400; price/fee assumptions rise explicitly | **PROMISING — VALIDATE IN DISCOVERY** |

The ten-location calculation is only a thought experiment, not Case 2B. Its location burden grows, central consolidation uses the explicit non-linear increment, per-location engineering falls to eight hours under a standardization assumption, and exceptions rise to 45. Operating leverage appears, but so do support and pricing requirements.

### Calculated Case 1 comparison

| Measure | Case 1 | Case 2 |
|---|---:|---:|
| Locations | 1 | 5 |
| Current-state burden | $35,240 | $173,500 |
| Recoverable value | $10,392 | $67,070 |
| Engineering hours | 150 | 234 |
| Implementation price | $15,000 | $42,000 |
| Solutions hours | 28 | 52 |
| Annual support cost | $2,700 | $6,900 |
| Core reuse | 57.4% | 55.6% |
| Customer payback | 24.4 months | 8.7 months |
| Verdict | NO DEAL | PROMISING — VALIDATE IN DISCOVERY |

The executable obtains both rows from the Case 1 and Case 2 factories. Recoverable value grows **6.45×**, while engineering hours grow **1.56×**. In this baseline, **value scales faster than delivery cost**. That conclusion is conditional on standardization, insufficient SaaS, manageable support, willingness to pay, and exceptions not exploding.

## 14. Verdict

The framework-derived baseline verdict is **PROMISING — VALIDATE IN DISCOVERY** because:

- customer value, delivery contribution, and recurring support economics work under the assumptions;
- at least 40% of core engineering is demonstrably reusable within the model; and
- “promising” is only an economic hypothesis; market validation still requires discovery.

The strategic balance is:

```text
MORE RECOVERABLE VALUE + SHARED ENGINEERING + ONE COMMERCIAL RELATIONSHIP
+ REPEATED WORKFLOWS
versus
ADDITIONAL COMPLEXITY + CUSTOMER-SPECIFIC EXCEPTIONS + SUPPORT + SaaS COMPETITION
```

The customer is attractive only if the first side grows faster. Real discovery must test system permissions and overlap, data quality, exact mappings, stakeholder acceptance, implementation risk, SaaS coverage, support frequency, reachable similar groups, and repeated willingness to pay.

## Run it

```bash
python examples/restaurant_group.py
```

[Previous: Case 1](01-independent-restaurant.md) · [Book home](../README.md) · Next: Case 3 — planned
