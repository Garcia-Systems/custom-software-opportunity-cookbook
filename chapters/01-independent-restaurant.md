# Case 1 — The Independent Restaurant

[Repository home](../README.md) · [Previous: Chapter 0](00-opportunity-framework.md)

> **Fiction notice:** James River Kitchen and every operational, effort, and financial value below are fictional educational assumptions. They are neither Williamsburg restaurant data nor industry benchmarks.

## 1. Business

James River Kitchen is a fictional, independently owned restaurant: one approximately 120-seat location, dine-in and takeout, a seasonal/local menu, and a small management team. The question is not whether integrated data could be useful. It is whether one location can recover enough value to justify a responsible custom engagement.

## 2. Problem

Managers repeatedly combine sales, reservations, labor, inventory exports, and feedback in spreadsheets. Identifiers and export formats differ. Reconciliation and analysis consume time, and the useful view can arrive after a busy service period. Some waste and scheduling inefficiency might be preventable—but software cannot eliminate all of it.

## 3. Current systems

```text
POS ──────────────────┐
Reservations ─────────┤
Scheduling ───────────┤
Inventory / CSV ──────┼──→ Management manually reconciles information
Customer feedback ────┘
```

These tools function and do not need replacement. Their boundary is the cross-system management view.

## 4. Current-state economic burden

The baseline constructs burden from visible components:

| Fictional annual assumption | Burden |
|---|---:|
| Management reconciliation labor | $10,400 |
| Operational analysis labor | $6,240 |
| Avoidable waste / purchasing inefficiency | $9,000 |
| Avoidable labor-planning inefficiency | $7,200 |
| Other measurable administration | $2,400 |
| **Total** | **$35,240** |

These are case inputs, not claims about a real business or typical restaurant.

## 5. Potential recoverable value

The model multiplies each applicable burden by an editable improvement assumption; it does not enter a target total.

| Component | Improvement | Recoverable |
|---|---:|---:|
| Management reconciliation | 45% | $4,680 |
| Operational analysis | 30% | $1,872 |
| Waste / purchasing | 20% | $1,800 |
| Labor planning | 20% | $1,440 |
| Other administration | 25% | $600 |
| **Total** |  | **$10,392** |

Thus **total current-state burden ≠ recoverable value**. Causes outside the proposed software remain, and even a useful briefing will not guarantee that managers act on every signal.

## 6. Solution

The smallest intervention is adapters/imports for selected existing exports or permitted APIs, normalized identifiers and fields, a common reporting model, deterministic business calculations, a simple repeatable management briefing, and validation/logging.

```text
Existing operational tools → NARROW CUSTOM INTEGRATION → normalized data
                                                        → management briefing
```

It is not a POS, reservation or scheduling replacement; inventory system; CRM; ERP; AI adviser; complex dashboard; or mobile application. This case builds only an economic analysis, not that operational solution.

## 7. Build vs. buy

| Alternative | What discovery must test |
|---|---|
| Continue manually / do nothing | Cheapest, but retains delay and burden. |
| Improve the spreadsheet/process | May remove enough reconciliation at very low risk. |
| Configure current SaaS reports | Existing tools may already expose sufficient exports or reports. |
| Low-code automation | May connect selected flows with less initial engineering, but still has maintenance and mapping risk. |
| Another reporting/integration product | Could solve most of the need at materially lower cost. |
| Narrow custom integration | Fits the exact cross-system briefing, but carries discovery, adapter, and support cost. |

The baseline assumes—for analysis, not as a market fact—that alternatives were reviewed and do not cover the selected briefing well enough. That claim needs real discovery. A separate scenario makes an existing product adequate and therefore returns **BUY / CONFIGURE**. The case does not claim restaurant software is absent.

## 8. Delivery

| Work | Hours | Treatment |
|---|---:|---|
| Discovery-supported technical validation | 8 | Customer-specific |
| POS adapter/import | 14 | Potentially reusable |
| Reservation adapter/import | 10 | Customer-specific |
| Scheduling adapter/import | 10 | Customer-specific |
| Inventory CSV import | 12 | Potentially reusable |
| Feedback import | 8 | Customer-specific |
| Normalization | 18 | Potentially reusable |
| Business calculations | 10 | Customer-specific |
| Management briefing | 12 | Potentially reusable |
| Validation/error handling | 14 | Potentially reusable |
| Testing | 12 | Delivery overhead |
| Deployment | 6 | Delivery overhead |
| Documentation | 6 | Customer-specific |
| Rework reserve | 10 | Delivery overhead |

There are 150 modeled delivery hours: 70 reusable core, 52 customer-specific core, and 28 testing/deployment/reserve hours. At $70 per delivery hour plus $400 other direct cost, implementation delivery cost is **$10,900**.

## 9. Reuse

The 70 / 122 core-hour split produces **57.4% potential reuse**. Import interfaces, CSV utilities, normalization, validation/logging, reporting shell, and deployment patterns may travel. Vendor mappings, business rules, unusual formats, report configuration, and credentials may not. For customer one, potential portability is a hypothesis—not booked future value. Similar paid deployments must demonstrate similarity.

## 10. Deal economics

### Customer

Implementation price is $15,000 and annual recurring fee is $3,000. First-year cost is $18,000. Recoverable value of $10,392 leaves $7,392 after the recurring fee, producing a negative first-year ROI and **24.4-month** implementation payback under Chapter 0's definitions.

### Engineering partner

The partner supplies 150 delivery hours at the fictional $70 modeled cost, plus $400 direct expense: **$10,900**. Annual support requires 30 engineering hours plus non-labor obligations.

### Solutions organization

Prospecting/sales uses 5 hours, discovery 8, design/scoping 7, and coordination/acceptance 8: **28 hours**. At a fictional $60 internal hourly cost, implementation contribution is **$2,420**, or **$86.43 per solutions hour**. Positive contribution does not repair weak customer payback.

## 11. Market / sales

The owner/operator may be reachable directly, procurement simple, decision-makers few, and the fictional cycle only 1.5 months. Yet:

```text
EASY CUSTOMER TO REACH
+ SMALL CONTRACT
+ NONTRIVIAL DISCOVERY / IMPLEMENTATION
= STILL NOT AN ATTRACTIVE OPPORTUNITY
```

Access and economics are separate gates.

## 12. Support

Hosting, monitoring, failed imports, changing CSV formats, API changes, bugs, customer support, and maintenance remain after launch. Thirty hours at $70 plus $600 of hosting/monitoring makes annual direct support cost **$2,700**. The $3,000 fee leaves only **$300 recurring contribution**. Recurring revenue is not pure contribution, and this thin cushion is sensitive to failures.

## 13. Scenario test

Each factory constructs a new frozen scenario; the baseline is never mutated.

| Scenario | Changed assumption | Result |
|---|---|---|
| Baseline | Primary fictional inputs | **NO DEAL** |
| Higher recoverable value | Improvement rates rise; recovery becomes $20,034 | **PROMISING — VALIDATE IN DISCOVERY** |
| Lower delivery cost | Reusable/simpler imports lower delivery cost to $8,800 | **NO DEAL**; customer payback still fails |
| Strong SaaS alternative | Existing product adequately solves most of the need at lower cost/risk | **BUY / CONFIGURE** |

The executable derives all results through the Chapter 0 economics and verdict functions.

## 14. Verdict

The baseline framework verdict is **NO DEAL**, for the exact reason:

> The customer does not recover implementation price within one year.

Delivery contribution and support coverage are positive, but the customer gate fails. This is intentionally not a forced positive outcome.

```text
TECHNICALLY USEFUL
does not necessarily mean
ECONOMICALLY ATTRACTIVE
```

The earlier restaurant technology hypothesis can be technically correct while a one-location engagement remains economically marginal. That is not a contradiction; it is why opportunity analysis precedes a build.

## Run it

From the [repository setup](../README.md#start-here):

```bash
python examples/independent_restaurant.py
```

[Repository home](../README.md) · [Previous: Chapter 0](00-opportunity-framework.md)
