# Case 12 — The Perfect-Looking Deal That Isn't

> James River Equipment Services, ServiceFlow Pro, every workflow, and every financial value are fictional educational assumptions—not company facts, vendor claims, prices, or industry benchmarks.

## 1. Business

**James River Equipment Services** is a fictional regional equipment-service company with 26 employees: several field technicians, office and operations staff, and recurring service customers. It already uses a CRM, scheduling tool, service records, accounting software, spreadsheets, customer communications, and management reports.

## 2. Problem

```text
CUSTOMER REQUEST → SERVICE JOB → SCHEDULE → TECHNICIAN → COMPLETION
                                                        ↓
                              INVOICE / REPORTING ← FOLLOW-UP
```

Fragmented systems cause duplicate entry, schedule and technician-status reconciliation, service-record administration, invoice preparation, follow-up, reporting, and avoidable rework. The problem is meaningful; that does not yet select an intervention.

## 3. Current systems

```text
CRM ────────────────┐
Scheduling ─────────┤
Service records ────┼──→ proposed custom integration layer
Accounting ─────────┤              ↓
Spreadsheets ───────┘       normalized job workflow
                                   ↓
                           exceptions / reporting
```

The hypothesis leaves authoritative systems in place. It is opportunity analysis, not service-management software.

## 4. Current-state burden

Each item is `fictional hours/week × fictional loaded cost × 52`.

| Burden | Annual burden |
|---|---:|
| Duplicate entry | $8,320 |
| Scheduling reconciliation | $11,232 |
| Technician-status reconciliation | $9,100 |
| Service-record administration | $12,376 |
| Invoice preparation | $7,904 |
| Customer follow-up | $4,992 |
| Management reporting | $9,360 |
| Avoidable rework | $4,368 |
| **Total** | **$67,652** |

## 5. Recoverable value

Applying explicit recovery assumptions of 50–70% produces **$41,826.20/year**. No speculative sales, technician revenue, or customer-retention upside is counted.

## 6. Initial custom hypothesis

The narrow custom layer would synchronize job identifiers and statuses, normalize the workflow, surface exceptions, and produce the unusual management report. It would not replace CRM, scheduling, service records, or accounting.

## 7. Initial economics — before alternative discovery

At Stage 1, the team knows the manual burden but has not found a credible alternative. Implementation is **$12,000**, annual fee **$3,000**, first-year spend **$15,000**, first-year ROI **178.8%**, and payback **3.7 months**. Annual retained benefit after the fee is **$38,826.20**.

Delivery covers discovery, CRM, scheduling, service-record and accounting adapters, normalization, workflow logic, validation, testing, deployment, documentation, and rework reserve: 117 hours plus $500, or **$8,690**. Thirty solutions hours cost $1,950, leaving **$1,360 implementation contribution**. Support costs **$2,000/year**, leaving $1,000. Reusable core is 55 of 90 core hours (**61%**). The standard framework therefore says **PROMISING — VALIDATE IN DISCOVERY**.

That is a defensible *interim* result—and an incomplete discovery result.

## 8. Alternative discovery

Discovery finds **ServiceFlow Pro (fictional)**. It provides CRM/service-job synchronization, scheduling, technician status, standard service workflow, accounting integration, customer notifications, and management reporting. The assumptions are $3,000 setup/configuration, $4,200 annual subscription, $2,400 internal administration, and no hidden vendor claim.

It removes 90% of the burden the custom hypothesis could recover:

```text
ORIGINAL BURDEN                         $67,652.00
− BURDEN REMOVED BY FICTIONAL SaaS      $37,643.58
= RESIDUAL BURDEN                       $30,008.42
```

Residual burden is not zero: much of it was never recoverable by either intervention, and **$4,182.62** is the remaining advantage of full custom over SaaS. Thus:

| Measure | Annual value |
|---|---:|
| Custom value against status quo | $41,826.20 |
| SaaS value against status quo | $37,643.58 |
| **Incremental custom value above SaaS** | **$4,182.62** |

Customer ROI against doing nothing is insufficient. The relevant comparison is the best credible alternative.

## 9. Build vs. buy

The model compares cash, retained burden, and benefits—not $12,000 versus a subscription sticker.

| Option | First-year cash cost | Recurring cost | Burden remaining | Burden removed | First-year net benefit | Payback |
|---|---:|---:|---:|---:|---:|---:|
| A — Do nothing | $0 | $0 | $67,652.00 | $0 | $0 | Not meaningful |
| B — Full custom | $15,000 | $3,000 | $25,825.80 | $41,826.20 | $26,826.20 | 3.7 months |
| C — SaaS / configure | $9,600 | $6,600 | $30,008.42 | $37,643.58 | **$28,043.58** | 1.2 months |
| D — SaaS + narrow edge | $14,900 | $7,400 | $27,408.42 | $40,243.58 | $25,343.58 | 2.7 months |

The proposed edge is one proprietary export and management exception. It recovers $2,600 but costs $4,500 plus $800/year. Ten percent uniqueness is not a reason to rebuild the other ninety percent. Here even the edge should wait.

```text
FICTIONAL SaaS → STANDARD WORKFLOW
                         + optional edge only if separately justified
```

### Opportunity funnel

```text
Meaningful problem? YES
  ↓ Measurable value? YES
  ↓ Technically feasible? YES
  ↓ Customer economics vs doing nothing? ATTRACTIVE
  ↓ Existing SaaS solves adequately? YES
  ↓ BUY / CONFIGURE
```

Build-vs-buy belongs before celebrating custom ROI.

### Break-even residual burden

Custom's first-year total effect is custom cash plus remaining burden: **$40,825.80**. SaaS fixed first-year cash is $9,600. Therefore SaaS residual burden must rise to **$31,225.80** before its first-year total effect ties custom. Baseline residual burden is $30,008.42, below that threshold. This is a deterministic sensitivity, not an optimization engine.

## 10. Delivery and reuse

Full custom models the actual adapters, normalization, workflow, validation, testing, deployment, documentation, and reserve. SaaS + edge models only the export/exception edge; configuration is not disguised as full engineering.

The original architecture has high technical reuse. But **high reuse + common problem** can be evidence that a product category already exists. Reusable code has no strategic magic when a maintained product already captures the common workflow.

## 11. Deal economics

The custom implementation and support have positive provider contribution, and the customer's status-quo ROI is excellent. The deal still loses on intervention selection. A rejected custom project is not classified as commercial success. Avoiding an inferior commitment protects both customer and delivery organization.

## 12. Sales and discovery

Thirty solutions hours cover prospecting (4), workflow and burden discovery (10), alternative/system/gap investigation and design (9), and configuration/acceptance coordination (7). Discovery that kills a deal creates professional value through qualification, but it does not create custom revenue.

**Bad discovery:** “What does the manual problem cost?”

**Better discovery:** “What does the manual problem cost?” **+** “What alternatives already exist?” **+** “What burden remains after using them?”

The most important questions are:

1. Which current burdens are measured, recoverable, and owned by a buyer?
2. Which supported products, native integrations, and configuration paths already address them?
3. What cash, internal administration, retained burden, support, and risk accompany each alternative?
4. Precisely what valuable burden remains after the best alternative?
5. Can configuration solve the gap? If not, can a narrow edge recover enough value to fund delivery and support?
6. Are permissions, identifiers, exceptions, acceptance criteria, and ongoing ownership verified?

## 13. Support

Full custom support is 20 hours × $70 plus $600 of direct obligations: **$2,000/year** against a $3,000 fee. SaaS administration is explicitly $2,400 in addition to subscription. The support-burden scenario increases administration to $15,000 and changes the comparison; “buy” is not presumed free to operate.

## 14. Scenario tests

Factories produce new frozen assumptions; none mutate baseline.

| Scenario | Result | Lesson |
|---|---|---|
| A — Pre-alternative discovery | **PROMISING — VALIDATE IN DISCOVERY** | Status-quo economics look excellent because discovery is incomplete. |
| B — Strong SaaS | **BUY / CONFIGURE** | 90% of custom-recoverable burden is addressed more economically. |
| C — Weak SaaS | **PROMISING — VALIDATE IN DISCOVERY** | $42,000 residual burden makes full custom competitive again. |
| D — Expensive SaaS | **PROMISING — VALIDATE IN DISCOVERY** | Higher setup/subscription changes total outcome. |
| E — Small unique gap | **BUY / CONFIGURE** | The $2,600 edge does not fund its added cost. |
| F — Large unique gap | **SAAS + NARROW CUSTOM EDGE** | A $14,000 gap supports the edge, not a needless full rebuild. |
| G — Cheap custom | **BUY / CONFIGURE** | Lower custom price still loses to the strong alternative's total benefit. |
| H — SaaS support burden | **PROMISING — VALIDATE IN DISCOVERY** | Material administration must be included and can restore custom competitiveness. |

Case 6 shows mature retail software can dominate custom. Case 8 shows configuration can solve a seemingly bespoke workflow. Case 12 adds time: the custom deal looked excellent **until** iterative discovery found the alternative. Common, repeatable workflows attract product vendors; build only the unresolved edge, and only when meaningful.

## 15. Final verdict

**BUY / CONFIGURE.** The exact framework reason is:

- An existing buy/configure alternative adequately meets the need at materially lower cost or risk.

The SaaS option produces the strongest baseline first-year net benefit, has faster payback, and leaves too little incremental value to justify either full custom or the proposed edge. **BUY / CONFIGURE is a successful verdict**: correct intervention selection, not custom-software volume, is the objective.

---

[← Previous: Case 11 — The Healthcare Organization](11-healthcare.md) · [Book home](../README.md) · [Next: Case 13 — Great Customer Value, Bad Delivery Economics →](13-bad-delivery-economics.md)
