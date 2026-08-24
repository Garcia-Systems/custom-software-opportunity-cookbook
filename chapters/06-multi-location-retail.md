# Case 6 — The Multi-Location Retailer

> Every name and operational or financial value below is a fictional educational assumption, not a retailer benchmark.

## 1. Business

**James River Outfitters** is a fictional, centrally owned regional retailer with six physical stores, one e-commerce channel, a mostly common merchandise catalog with store variation, and a small central operations team.

## 2. Problem

The team repeatedly exports and reconciles sales, stock, purchasing, transfers, online orders, returns, and store comparisons. Exceptions arrive late. This is a real, measurable problem—but it does not follow that custom code is the right purchase. The key question is **why custom?**

## 3. Current systems

```text
Store POS ───────────────┐
Inventory ──────────────┤
Purchasing ─────────────┤
E-commerce ─────────────┼──> central manual reconciliation
Returns ────────────────┤
Scheduling ─────────────┤
Spreadsheets / exports ─┘
```

These systems function, but their identifiers, timing, and reports are fragmented.

## 4. Current-state economic burden

Each labor burden is `hours/week × fictional loaded hourly cost × 52 weeks`.

| Component | Formula | Annual burden |
|---|---:|---:|
| Cross-store reporting | 10 × $48 × 52 | $24,960 |
| Inventory reconciliation | 12 × $42 × 52 | $26,208 |
| E-commerce/store reconciliation | 7 × $45 × 52 | $16,380 |
| Purchasing and transfer analysis | 6 × $50 × 52 | $15,600 |
| Returns reconciliation | 5 × $40 × 52 | $10,400 |
| Cleanup and exception investigation | 8 × $42 × 52 | $17,472 |
| **Total** | | **$111,020** |

No speculative lost-sales amount is included; an inventory mismatch is not assumed to be a lost sale.

## 5. Potential recoverable value

The model applies a credible improvement rate to each component: reporting 60%, inventory 45%, online/store reconciliation 55%, purchasing 35%, returns 40%, and cleanup/exceptions 35%. `Burden × improvement` produces **$51,513.80** of annual recoverable value. This is not a manually entered benefit total.

## 6. Solution

The smallest custom hypothesis is an adapter/import layer with normalized product and store identifiers, sales and inventory snapshots, purchase-order and return imports, e-commerce reconciliation, validation/logging, exceptions, and a management briefing. It replaces none of the POS, inventory, purchasing, e-commerce, ERP/WMS, scheduling, forecasting, or recommendation systems.

## 7. Build vs. buy

Discovery must compare nine choices: existing suite configuration; native multi-location reporting; native e-commerce/POS integration; retail inventory or ERP SaaS; BI/configuration; automation/low-code; better spreadsheets/process; a narrow custom integration; and doing nothing.

The generic comparison counts cash cost, internal administration, residual burden, and an explicit risk allowance—not subscription alone.

| First-year effect | Custom | Buy/configure |
|---|---:|---:|
| Setup / implementation | $62,000 | $14,000 |
| Recurring fee / subscription | $15,000 | $18,000 |
| Internal administration | — | $8,000 |
| Residual burden | $59,506.20 | $26,000 |
| Risk allowance | $10,000 | $3,000 |
| **Total economic effect** | **$146,506.20** | **$69,000** |

Thus the baseline finding is **BUY / CONFIGURE**. Custom is technically feasible, but the modeled alternative captures much of the same value at materially lower cost and risk.

## 8. Delivery

Engineering is not multiplied wholesale by six: 170 shared hours + 9 hours per store (54) + 42 e-commerce hours + 30 exception hours + 38 QA + 14 deployment + 30 rework = **378 hours**. At $80/hour plus $2,200 direct cost, modeled delivery cost is **$32,440**.

## 9. Reuse

Within the customer, common adapters, identifiers, validation, and reporting provide strong reuse. Across customers, reuse is only plausible until workflows and permissions repeat in discovery. Standard APIs cut custom effort—but the same standards make SaaS integrations better. **High reuse does not imply a good custom-software market.**

## 10. Deal economics

The customer pays $62,000 implementation and $15,000 annually. Against $51,513.80 recoverable value, custom has a negative first-year ROI and about 20.4 months payback. Delivery plus 78 solutions hours at $70 leaves **$24,100 implementation contribution**. Positive vendor contribution does not rescue inferior customer economics relative to SaaS.

## 11. Market / sales

Ownership is accessible and there is one contract, yet incumbent relationships and buyer expectations create a demanding justification burden. Solutions work includes prospecting (8h), discovery (8h), central interviews (8h), store sampling (10h), technical validation (12h), design/scoping (12h), proposal (6h), coordination (8h), and acceptance (6h): **78 hours**. The hardest sales question is not procurement—it is “why custom?”

## 12. Support

Modeled recurring work is 38 fixed hours + 4 × 6 store hours + 18 exception hours = 80 hours. At $80/hour plus $3,480 hosting/other direct costs, annual support costs **$9,880**, leaving **$5,120** contribution on the $15,000 fee. Obligations include hosting, monitoring, POS/e-commerce API changes, mapping and identifier drift, onboarding, returns logic, defects, and customer support.

## 13. Scenario test

All variants create new frozen records; the baseline is unchanged.

| Scenario | Framework result | Lesson |
|---|---|---|
| Baseline | BUY / CONFIGURE | Mature SaaS wins on total effect. |
| Weak SaaS alternative | PROMISING — VALIDATE IN DISCOVERY | High residual burden can justify custom. |
| Strong SaaS alternative | BUY / CONFIGURE | Lower cost and risk strongly favor buying. |
| Highly standardized systems | BUY / CONFIGURE | Delivery improves, but the already-strong SaaS option still wins. |
| Messy acquired stores | BUY / CONFIGURE | Exceptions raise custom delivery and support. |
| Higher measurable burden | PROMISING — VALIDATE IN DISCOVERY | Explicitly higher labor can cross the economic threshold. |
| One-off niche requirement | ONE-OFF CUSTOM PROJECT | Valuable unique work can support a project without a repeatable market. |

## 14. Verdict

**BUY / CONFIGURE.** Exact framework reason: “An existing buy/configure alternative adequately meets the need at materially lower cost or risk.”

Mature SaaS changes the opportunity. Custom competes with the best available alternative, not with manual work alone. Six locations increase burden but do not guarantee a custom opportunity. A unique workflow can be a good project while remaining a weak market.

Real discovery must establish which problems remain after modern SaaS, which integrations truly are unavailable, what configuration can do before code, whether buyers pay for edge cases, and how often the same edge cases repeat.

---

[← Previous: Case 5 — Tourism / Attraction Operator](05-tourism-attraction.md) · [Book home](../README.md) · [Next: Case 7 — The Construction / Trades Company](07-construction-trades.md)
