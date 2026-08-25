# Case 9 — The Local Government Department

> **Fiction notice:** James River County Permitting Department, its county, systems, staffing, requirements, and every operational and financial assumption below are fictional educational values. It does not represent James City County, Williamsburg, or any real agency. These assumptions are not benchmarks or legal/compliance advice.

## 1. Business

The fictional **James River County Permitting Department** is a county-level department of 32 staff. It accepts public applications, coordinates internal review and corrections, records approvals and status, and prepares reports. Documents, payments, and authoritative records remain in existing systems.

Its workflow is **Application → Intake → Validation → Department review → Corrections/resubmission → Approval → Status/record → Reporting**. Professional judgment, regulatory review, and required approval are legitimate human work, not automation savings.

## 2. Problem

Staff duplicate data, reconcile status, search systems, maintain spreadsheets, check documents, administer corrections, and assemble reports. Fragmented information adds avoidable delay. This is meaningful, but a large problem alone does not make the department an attractive customer.

## 3. Current systems

```text
Public intake / legacy records / documents / finance
Email / spreadsheets / reporting exports
                         ↓
             manual reconciliation

Approved exports / interfaces / status data
                         ↓
              NARROW INTEGRATION LAYER
                         ↓
        normalized status / internal reporting view
```

Existing products remain systems of record. Baseline access means approved exports or vendor-controlled interfaces, security approval, network restrictions, limited test environments, and integration review. Scenario E closes critical access.

## 4. Current-state economic burden

Weekly labor is `hours × 52 × fictional loaded hourly cost`; rework is `incidents × cost per incident`.

| Component | Formula | Annual burden |
|---|---:|---:|
| Duplicate entry | 18 × 52 × $38 | $35,568 |
| Status reconciliation | 22 × 52 × $42 | $48,048 |
| Report preparation | 12 × 52 × $46 | $28,704 |
| Document/status lookup | 16 × 52 × $40 | $33,280 |
| Correction administration | 10 × 52 × $41 | $21,320 |
| Management reporting | 7 × 52 × $58 | $21,112 |
| Avoidable administrative rework | 55 × $240 | $13,200 |
| **Total** | calculated | **$201,232** |

This excludes permit-processing time, revenue, profit, professional review, and mandated approval.

## 5. Potential recoverable value

Recovery is burden multiplied by explicit improvements: 55%, 60%, 65%, 45%, 35%, 50%, and 30%. The results are $19,562.40, $28,828.80, $18,657.60, $14,976, $7,462, $10,556, and $3,960: **$104,002.80 annually**. Visibility can reduce information work; it cannot eliminate judgment or approvals.

## 6. Solution

The smallest useful intervention provides approved import/adapters, a normalized case identifier and status model, validation, exception handling, audit-friendly logging, deterministic reporting, an accessibility-conscious internal view, deployment, and monitoring.

It is **not** a permitting platform, records system, payment system, public portal, document platform, identity system, ERP, or legacy replacement. This repository evaluates the opportunity; it builds none of those products.

## 7. Build vs. buy

The comparison includes incumbent modules and professional services, government case-management SaaS, configuration, approved low-code, improved process/spreadsheet reporting, narrow custom integration, full replacement, and doing nothing.

Baseline alternative effect is **$258,000**: $35,000 setup + $32,000 recurring + $18,000 administration + $155,000 retained burden + $18,000 risk. Baseline custom effect is **$219,229.20**: $78,000 implementation + $24,000 support + $97,229.20 retained burden + $20,000 risk. Custom passes this fictional comparison. Scenario F supplies an adequate incumbent module and returns **BUY / CONFIGURE**.

## 8. Delivery

| Engineering category | Hours |
|---|---:|
| Technical discovery / access validation | 28 / 32 |
| Legacy adapter / document-status integration | 70 / 40 |
| Normalization / workflow-status model | 40 / 46 |
| Audit logging | 38 |
| Security hardening / accessibility | 44 / 24 |
| Documentation / testing / deployment / rework | 18 / 64 / 28 / 50 |
| **Total** | **522** |

At $95 internal hourly cost plus $3,500 direct costs, delivery costs **$53,090**. Non-feature security/accessibility is **68 hours**. Delivery contribution before acquisition is **$24,910**: healthy once won, but incomplete deal economics.

## 9. Reuse

Adapter, status, validation, audit, reporting, security, and deployment patterns contribute 185 of 380 core hours: **48.7% core reuse**. Legacy products, workflows, approval rules, vendor restrictions, environments, and reports remain specific. Scenario G raises reuse above 75%, yet procurement, security review, contracts, permissions, and stakeholder alignment remain bespoke.

## 10. Deal economics

Implementation is **$78,000** and annual support **$24,000**. Recoverable value after the fee is $80,002.80, so implementation payback is just under one year. Delivery plus 192 solutions hours at $80 leaves **$9,550 solutions contribution**, only **$49.74 per solutions hour**.

Thus **delivery contribution can look healthy while contribution per total solutions/sales effort looks poor**. `POOR TARGET CUSTOMER` means a viable project is unattractive under this acquisition motion. `NO DEAL` means an earlier engagement gate fails; Scenario E demonstrates that distinct outcome.

## 11. Market / sales

Baseline work is prospecting 18, discovery 16, stakeholder meetings 20, technical validation 16, security documentation 14, accessibility review 12, proposal/RFP 22, procurement support 28, contract coordination 18, implementation planning 12, acceptance 10, and other coordination 6: **192 hours**.

The modeled nine-month category is not magically converted into dollars. Its meetings, documentation, proposal and contracting work, delayed contribution, and reduced throughput are visible. The fictional motion includes multiple stakeholders, possible solicitation, contracting/legal coordination, vendor/insurance documentation, security and accessibility review, implementation approval, budget timing, and permissions. These are assumptions, not universal government rules.

## 12. Support

Annual support includes 110 engineering hours at $95 plus hosting $1,800, monitoring $1,200, security updates $1,600, vendor/API changes $1,800, audit/log maintenance $800, accessibility fixes $600, incident response $1,200, documentation $600, and change control $1,000. Cost is **$21,050**, leaving **$2,950** contribution. Recurring revenue is not automatically lucrative.

## 13. Scenario test

Factories return fresh frozen records; scenarios never mutate baseline assumptions.

| Scenario | Result | Lesson |
|---|---|---|
| A — Baseline | **POOR TARGET CUSTOMER** | Valuable, feasible project; unattractive acquisition motion. |
| B — Cooperative pilot | **PROMISING — VALIDATE IN DISCOVERY** | 56 solutions hours, clear access, two-month approval improve economics. |
| C — Formal RFP | **POOR TARGET CUSTOMER** | 304 hours leave $590 contribution, or $1.94/hour. |
| D — Higher contract value | **POOR TARGET CUSTOMER** | $80,000 improves contribution; difficult procurement still controls attractiveness. |
| E — Closed legacy integration | **NO DEAL** | Critical access makes the intervention infeasible. |
| F — Existing vendor module | **BUY / CONFIGURE** | Adequate supported module has lower cost/risk. |
| G — Reusable technology, hard sales | **POOR TARGET CUSTOMER** | Reusable code cannot remove per-customer governance. |

### Case 7 vs. Case 9

Calculated Case 7 recoverable value is **$64,619.29**, with 88 solutions hours, a 4-month cycle, and **PROMISING**. Case 9 has greater recovery (**$104,002.80**) but 192 solutions hours, a 9-month cycle, and **POOR TARGET CUSTOMER**. Similar technical opportunity does not imply similar target attractiveness.

The implemented comparison now covers Cases 1–9 and independently reports customer recovery, engineering difficulty/hours, reuse, procurement difficulty, and verdict. It creates no arbitrary composite score.

## 14. Verdict

**POOR TARGET CUSTOMER.** Exact framework reasons:

- Procurement difficulty is high for the modeled contract.
- Stakeholder and close friction is high for the modeled contract.
- Access to a clear buyer is low for the modeled contract.
- The modeled sales cycle exceeds six months and consumes scarce solutions capacity.

The project remains **technically feasible**, customer payback and support gates pass, and the problem remains important. Larger contracts can justify harder motions—but only to a point. A good won project is not automatically a good repeatable market.

Real discovery must investigate purchasing thresholds, procurement pathways and pilots, budget cycles, vendor requirements, security review, accessibility expectations, integration permissions and test environments, typical contract size, actual cycle duration, incumbent options, deployment/retention restrictions, and support/incident/change-control obligations.

---

[← Previous: Case 8 — The Professional Services Firm](08-professional-services.md) · [Book home](../README.md) · [Next: Case 10 — The University Department →](10-university.md)
