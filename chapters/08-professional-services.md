# Case 8 — The Professional Services Firm

> James River Advisory and every workflow, operational assumption, and financial value below are fictional educational assumptions—not consulting-industry benchmarks, forecasts, or advice.

## 1. Business

**James River Advisory** is a fictional 36-person, centrally owned advisory firm with one primary office and hybrid/remote work. Several practice areas sell project engagements through a shared pipeline. Management oversees proposals, active projects, staffing, time, utilization, invoices, and operating reports.

Its lead-to-cash workflow is **Lead → Opportunity → Proposal → Signed engagement → Project → Staff assignment → Time → Billing → Payment**.

## 2. Problem

Signed engagements are entered into project tools; metadata is copied; assignments live separately; time, project status, and billing do not align; utilization and weekly management reports are assembled in spreadsheets; invoice readiness requires reconciliation; and pipeline-to-capacity visibility is fragmented. This is a legitimate problem. The question is whether code is its smallest economically sensible remedy.

## 3. Current systems

```text
CRM / leads ───────────────┐
Proposal / documents ─────┤
Project management ───────┤
Time / resource planning ─┼──→ manual reconciliation and reporting
Accounting / billing ─────┤
Spreadsheets ──────────────┘
```

The software ecosystem is mature: CRM, proposal, project, PSA, time/billing, accounting, BI, automation, and spreadsheet/process options must be evaluated before custom code.

## 4. Current-state economic burden

Each formula is `annual units × cost per unit`; weekly labor uses `hours × 52 × loaded hourly cost`. No unbilled-time pool or invoice principal is called software value.

| Fictional component | Formula | Annual burden |
|---|---:|---:|
| Sales-to-project handoff | 5 × 52 × $42 | $10,920 |
| Project setup administration | 6 × 52 × $38 | $11,856 |
| Time/billing reconciliation | 12 × 52 × $42 | $26,208 |
| Utilization reporting | 6 × 52 × $48 | $14,976 |
| Management reporting | 7 × 52 × $58 | $21,112 |
| Resource-planning reconciliation | 5 × 52 × $50 | $13,000 |
| Invoice preparation | 8 × 52 × $40 | $16,640 |
| Error/rework | 40 incidents × $180 | $7,200 |
| **Total** | calculated | **$121,912** |

## 5. Potential recoverable value

The model applies explicit improvement assumptions of 60%, 50%, 55%, 60%, 45%, 35%, 50%, and 30% respectively. This produces **$60,410.40** annual baseline recovery from administration, reporting, reconciliation, and credible rework reduction.

**Utilization visibility is not utilization creation.** A report can clarify staffing choices but does not create demand or billable work. Baseline value therefore includes zero utilization/revenue upside. Scenario H separately labels an uncertain $18,000 hypothesis; it changes neither baseline nor its measured burden recovery.

## 6. Solution

The smallest plausible custom edge would synchronize CRM/project records and engagement IDs, hand off accepted proposals, map employees/projects, normalize time/billing data, calculate utilization deterministically, report invoice readiness, prepare a management briefing, validate inputs, log activity, and route exceptions. It would **not** build CRM, proposal, PM, PSA, time tracking, resource planning, accounting, billing, ERP, or AI staffing.

## 7. Build vs. buy

The explicit alternatives are: existing CRM configuration; project-management configuration; PSA; time/billing; accounting integrations; BI/reporting; automation tooling; better spreadsheets/process; narrow custom integration; and doing nothing.

The central question is: **is this unique workflow, or software the firm already owns but under-configures?** Baseline buy/configure economics are:

| First-year component | Amount |
|---|---:|
| Configuration/setup | $14,000 |
| Subscription/automation | $18,000 |
| Internal administration | $7,000 |
| Residual burden | $32,000 |
| Risk allowance | $3,000 |
| **Total economic effect** | **$74,000** |

Custom's comparable effect is implementation $52,000 + recurring $14,000 + unrecovered burden $61,501.60 + risk $12,000 = **$139,501.60**. Thus **process change + SaaS configuration + low-code automation** wins. Total economics—not subscription alone—drive the finding.

## 8. Delivery

If custom were selected, technical discovery, five system handoffs, identity normalization, utilization/report rules, validation/error handling, testing, deployment, documentation, and reserve total **478 engineering hours**. Of 378 core hours, 155 are reusable and 223 customer-specific; testing is 52, deployment 14, and reserve 34. At fictional cost plus direct expenses, delivery costs **$42,630**.

Engineering must ask whether those hours produce differentiation or recreate configurable integration.

## 9. Reuse

Potentially reusable work includes adapters, client/project identity, handoff patterns, logging/validation, reporting shell, deployment, and generic time/project normalization. Project classifications, billing and utilization definitions, practice areas, employee roles, proposal steps, and reports remain customer-specific.

The strategic tension matters: **if workflows are standardized enough for high reuse, they may also be standardized enough for mature SaaS.** Repeatability alone does not establish a market.

## 10. Deal economics

Custom customer economics are $52,000 implementation, $14,000 annual fee, $66,000 first-year cash cost, $46,410.40 retained annual benefit, -8.5% first-year ROI, and 13.4-month payback. Delivery contribution after $42,630 delivery and $6,160 solutions labor is **$3,210**. These custom economics do not override the better alternative.

## 11. Market / sales

Owner/managing partner, operations, finance, practice/project managers, sales, and the existing IT provider are stakeholders. Procurement may be manageable, but a custom seller bears the burden of answering, “Why can’t we configure our existing tools?”

Prospecting/sales, discovery, workflow mapping, inventory, configuration-vs-code analysis, technical validation, design, proposal/scoping, coordination, and acceptance total **88 solutions hours**. Contribution is $3,210, or **$36.48 per solutions hour**. Good solutions engineering succeeds when it recommends less engineering.

## 12. Support

Custom support includes 72 maintenance engineering hours, hosting/monitoring, SaaS API and authentication changes, mapping changes, billing-rule changes, customer support, and bugs. Annual direct cost is **$10,720**, leaving **$3,280** on the $14,000 fee. Configuration/automation has lower modeled support and delivery risk, reflected in its alternative economics.

## 13. Scenario test

All scenario factories create fresh frozen records; baseline assumptions remain unchanged.

| Immutable scenario | Result | What it demonstrates |
|---|---|---|
| A — Baseline | BUY / CONFIGURE | Adequate SaaS/configuration is materially cheaper or safer. |
| B — Poor configuration | BUY / CONFIGURE | Low-cost setup and automation strongly win. |
| C — Genuine cross-system gap | PROMISING — VALIDATE IN DISCOVERY | High burden remaining after configuration can make narrow custom competitive. |
| D — High administrative burden | PROMISING — VALIDATE IN DISCOVERY | More measured reconciliation/reporting strengthens custom. |
| E — Low administrative burden | BUY / CONFIGURE | Efficient operations weaken custom. |
| F — Unique billing workflow | ONE-OFF CUSTOM PROJECT | Individual economics work, but reusable core falls below 40%. |
| G — Strong repeatability + strong SaaS | BUY / CONFIGURE | 60%+ theoretical reuse cannot defeat an adequate alternative. |
| H — Speculative utilization upside | BUY / CONFIGURE | The uncertain $18,000 upside remains separate; the result does not depend on it. |

### Case 7 vs. Case 8

Both cases suggest integration around authoritative systems. Case 7 baseline recoverable value is **$64,619.29**, its modeled alternative effect is **$164,000**, and its framework verdict is **PROMISING**. Case 8 recovery is **$60,410.40**, but its credible configuration alternative effect is only **$74,000**, producing **BUY / CONFIGURE**. The distinction comes from measured alternatives and economics—not stereotypes about either industry.

Physical field/office handoffs may leave unusual gaps in Case 7; highly digitized Case 8 processes have stronger configurable coverage. Nearly identical architecture is therefore not nearly identical opportunity.

**CUSTOM OPPORTUNITY ≠ WORKFLOW COMPLEXITY ALONE.** A stronger hypothesis is: valuable workflow gap + poorly served by existing software + measurable burden + feasible integration + sustainable delivery = potential custom opportunity.

## 14. Verdict

**BUY / CONFIGURE.** Exact framework reason:

- “An existing buy/configure alternative adequately meets the need at materially lower cost or risk.”

Configuration is a legitimate solution, and recommending it is successful analysis. Custom should target only an unresolved, valuable edge. Scenario F can be a good one-off project without proving professional services is a good broad market.

Real discovery must establish what the firm owns, what remains manual after reasonable configuration, why automation fails, measurable residual burden, recurrence across firms, buying authority, willingness to pay, and support expectations.

---

[← Previous: Case 7 — The Construction / Trades Company](07-construction-trades.md) · [Book home](../README.md) · Next: Case 9 — planned (not implemented)
