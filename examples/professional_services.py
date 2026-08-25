"""Run Case 8. Every value is a fictional educational assumption."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (alternative_first_year_effect,
    annual_support_cost, custom_first_year_effect, effective_contribution_per_solutions_hour,
    first_year_roi, implementation_delivery_cost, payback_period_months,
    recurring_support_contribution, reuse_percentage, solutions_contribution,
    solutions_hours)
from opportunity_cookbook.professional_services import (baseline_case,
    case_seven_vs_eight, genuine_cross_system_gap_case,
    high_administrative_burden_case, low_administrative_burden_case,
    poorly_configured_tools_case, speculative_utilization_upside_case,
    strong_repeatability_strong_saas_case, unique_billing_workflow_case)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison


def money(value): return f"${value:,.2f}"


case = baseline_case(); s = case.scenario; e = case.engineering
print("CASE 8 — THE PROFESSIONAL SERVICES FIRM")
print("=" * 41)
print("Fictional educational scenario:\nJames River Advisory")
print("\nWORKFLOW\nLead → Opportunity → Proposal → Project → Staff → Time → Billing → Payment")
print("\nCURRENT-STATE BURDEN")
for item in case.burdens:
    print(f"{item.name:40} {money(item.annual_burden):>14}")
print(f"{'Total annual burden':40} {money(case.total_burden):>14}")
print("\nRECOVERABLE VALUE")
for item in case.burdens:
    print(f"{item.name + ' × ' + str(item.improvement_rate * 100) + '%':40} {money(item.recoverable):>14}")
print(f"{'Total recoverable value':40} {money(case.recoverable_value):>14}")
print("Utilization visibility does not create billable work; no utilization upside is in baseline.")
print("\nCUSTOM OPTION")
print("Implementation / recurring / risk:", money(s.customer.implementation_price), "/",
      money(s.customer.recurring_annual_fee), "/", money(case.custom_risk_allowance))
print("Total first-year economic effect:", money(custom_first_year_effect(s.customer, case.custom_risk_allowance)))
print("\nBUY / CONFIGURE OPTION")
print("Process change + SaaS configuration + low-code automation")
print("Setup / subscription / internal administration / residual burden / risk:",
      *(money(value) for value in vars(case.alternative).values()))
print("Total first-year economic effect:", money(alternative_first_year_effect(case.alternative)))
print("\nCUSTOMER ECONOMICS")
print("First-year cost / retained benefit:", money(s.customer.implementation_price + s.customer.recurring_annual_fee),
      "/", money(case.recoverable_value - s.customer.recurring_annual_fee))
print("ROI / payback:", f"{first_year_roi(s.customer):.1%}", "/", f"{payback_period_months(s.customer):.1f} months")
print("\nDELIVERY")
print("Engineering / reusable / customer-specific hours:", e.total_hours,
      s.delivery.reusable_engineering_hours, s.delivery.customer_specific_engineering_hours)
print("Testing / deployment / rework reserve:", e.testing, e.deployment, e.rework_reserve)
print("Direct delivery cost / core reuse:", money(implementation_delivery_cost(s.delivery)),
      f"{reuse_percentage(s.delivery):.1%}")
print("\nSOLUTIONS ECONOMICS")
print("Solutions hours / contribution / contribution per hour:", solutions_hours(s.solutions),
      money(solutions_contribution(s.customer, s.delivery, s.solutions)),
      money(effective_contribution_per_solutions_hour(s.customer, s.delivery, s.solutions)))
print("Good solutions engineering can recommend less engineering.")
print("\nSUPPORT")
print("Hosting, monitoring, SaaS API/auth changes, mappings, billing rules, support, bugs, and maintenance engineering.")
print("Recurring revenue / cost / contribution:", money(s.customer.recurring_annual_fee), "/",
      money(annual_support_cost(s.delivery)), "/", money(recurring_support_contribution(s.customer, s.delivery)))
print("\nBUILD VS. BUY\n" + s.build_vs_buy.note)
result = analyze(s)
print("\nVERDICT\n-------\n" + result.verdict.value + "\nWHY")
for reason in result.reasons: print("-", reason)
print("\nSCENARIOS")
for name, factory in (("Baseline", baseline_case), ("Poor configuration", poorly_configured_tools_case),
        ("Genuine integration gap", genuine_cross_system_gap_case),
        ("High burden", high_administrative_burden_case),
        ("Low burden", low_administrative_burden_case),
        ("Unique billing workflow", unique_billing_workflow_case),
        ("Strong reuse + strong SaaS", strong_repeatability_strong_saas_case),
        ("Speculative utilization upside", speculative_utilization_upside_case)):
    print(f"{name:34} {analyze(factory().scenario).verdict.value}")
comparison = case_seven_vs_eight()
print("\nCASE 7 VS. CASE 8")
print("Construction: recoverable", money(comparison.construction_recoverable), "alternative effect",
      money(comparison.construction_alternative_effect), "→", comparison.construction_verdict)
print("Professional services: recoverable", money(comparison.professional_services_recoverable), "alternative effect",
      money(comparison.professional_services_alternative_effect), "→", comparison.professional_services_verdict)
print("Similar integration architecture is not equivalent opportunity economics: SaaS adequacy changes the answer.")
print("\nIMPLEMENTED-CASE COMPARISON")
for row in implemented_case_comparison():
    print(f"{row.name:28} recoverable {money(row.recoverable_value):>13} | {row.verdict}")
