"""Run Case 9. This evaluates an opportunity; it implements no government system."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    effective_contribution_per_solutions_hour, implementation_delivery_cost,
    recurring_support_contribution, reuse_percentage, solutions_contribution,
    solutions_hours)
from opportunity_cookbook.local_government import (baseline_case,
    case_seven_vs_nine, closed_legacy_integration_case, cooperative_pilot_case,
    existing_vendor_module_case, formal_rfp_case, high_contract_value_case,
    reusable_technical_hard_sales_case)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison


def money(value): return f"${value:,.2f}"


case = baseline_case(); s = case.scenario
print("CASE 9 — THE LOCAL GOVERNMENT DEPARTMENT\n" + "=" * 40)
print("Fictional educational scenario:\nJames River County Permitting Department")
print("This name, organization, and every assumption are fictional; they describe no real agency.")
print("\nBUSINESS / PUBLIC SERVICE PROBLEM")
print("Application → intake → validation → review → corrections → approval → record → reporting")
print("A 32-person fictional department reconciles fragmented information; required human review is excluded.")
print("\nCURRENT-STATE BURDEN")
for item in case.burdens: print(f"{item.name:38} {money(item.annual_burden):>14}")
print(f"{'Total annual burden':38} {money(case.total_burden):>14}")
print("\nRECOVERABLE VALUE")
for item in case.burdens:
    print(f"{item.name + ' × ' + str(item.improvement_rate * 100) + '%':38} {money(item.recoverable):>14}")
print(f"{'Total recoverable value':38} {money(case.recoverable_value):>14}")
print("No regulatory review, judgment, approval, profit, or revenue is claimed as recoverable.")
print("\nCUSTOMER ECONOMICS")
print("Implementation / annual fee:", money(s.customer.implementation_price), "/", money(s.customer.recurring_annual_fee))
print("\nDELIVERY ECONOMICS")
print("Engineering hours:", case.engineering.total_hours)
print("Security/accessibility effort:", case.engineering.security_accessibility_hours)
print("Direct delivery cost:", money(implementation_delivery_cost(s.delivery)))
print("Delivery contribution before sales:", money(s.customer.implementation_price - implementation_delivery_cost(s.delivery)))
print("\nSALES / PROCUREMENT")
print("Discovery / proposal-RFP / security-procurement hours:", case.procurement.discovery,
      case.procurement.proposal_rfp, case.procurement.security_procurement_hours)
print("Total solutions hours / sales-cycle category:", solutions_hours(s.solutions), "/", f"{s.sales.sales_cycle_months} months (long)")
print("Solutions contribution / contribution per solutions hour:",
      money(solutions_contribution(s.customer, s.delivery, s.solutions)), "/",
      money(effective_contribution_per_solutions_hour(s.customer, s.delivery, s.solutions)))
print("Duration has no standalone dollar charge; its meetings, reviews, proposals, and coordination consume these hours and capacity.")
print("\nINTEGRATION ACCESS")
print("Baseline assumes approved exports/vendor-controlled interfaces, security approval, network restrictions, limited testing, and integration review.")
print("Existing products remain systems of record; the intervention is only adapters, normalized status, exceptions, audit logs, and reporting view.")
print("\nBUILD VS. BUY\n" + s.build_vs_buy.note)
print("Baseline narrow custom is economically preferred to the modeled alternatives; an incumbent module wins Scenario F.")
print("\nSUPPORT")
print("Hosting, monitoring, security and API changes, audit logs, accessibility fixes, incidents, documentation, and change control.")
print("Annual revenue / cost / contribution:", money(s.customer.recurring_annual_fee), "/",
      money(annual_support_cost(s.delivery)), "/", money(recurring_support_contribution(s.customer, s.delivery)))
result = analyze(s)
print("\nVERDICT\n-------\n" + result.verdict.value + "\nWHY")
for reason in result.reasons: print("-", reason)
print("Technically feasible and economically viable once won does not mean attractive target customer; POOR TARGET CUSTOMER is not NO DEAL.")
print("\nSCENARIOS")
for name, factory in (("Baseline", baseline_case), ("Cooperative pilot", cooperative_pilot_case),
        ("Formal RFP", formal_rfp_case), ("Higher contract value", high_contract_value_case),
        ("Closed legacy integration", closed_legacy_integration_case),
        ("Existing vendor module", existing_vendor_module_case),
        ("High technical reuse / hard sales", reusable_technical_hard_sales_case)):
    print(f"{name:38} {analyze(factory().scenario).verdict.value}")
c = case_seven_vs_nine()
print("\nCASE 7 VS. CASE 9")
print("Construction: recoverable / solutions hours / cycle:", money(c.construction_recoverable), c.construction_solutions_hours, c.construction_sales_cycle_months, "→", c.construction_verdict)
print("Local government: recoverable / solutions hours / cycle:", money(c.government_recoverable), c.government_solutions_hours, c.government_sales_cycle_months, "→", c.government_verdict)
print("\nIMPLEMENTED-CASE COMPARISON")
for row in implemented_case_comparison():
    print(f"{row.name:28} value {money(row.recoverable_value):>13} | delivery {row.delivery_difficulty:8} | procurement {row.sales_procurement_difficulty:8} | reuse {row.reuse:.0%} | {row.verdict}")
