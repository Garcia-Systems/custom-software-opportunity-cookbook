"""Run Case 7. Every value is a fictional educational assumption."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.construction_trades import (baseline_case,
    clean_integrations_case, difficult_integrations_case, existing_saas_case,
    high_burden_case, highly_customer_specific_case, low_burden_case,
    unsustainable_support_case)
from opportunity_cookbook.economics import (annual_support_cost, first_year_roi,
    implementation_delivery_cost, payback_period_months,
    recurring_support_contribution, reuse_percentage, solutions_contribution,
    solutions_hours)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison


def money(value): return f"${value:,.2f}"


case = baseline_case(); s = case.scenario; e = case.engineering
print("CASE 7 — THE CONSTRUCTION / TRADES COMPANY")
print("=" * 44)
print("Fictional educational scenario: James River Mechanical")
print("\nWORKFLOW\nLead → Estimate → Job → Schedule → Crew → Materials → Completion → Invoice → Payment")
print("\nCURRENT SYSTEMS\nCRM/leads; estimating; scheduling/dispatch; field communication; purchasing/materials; accounting; spreadsheets")
print("\nCURRENT-STATE BURDEN")
for item in case.burdens:
    print(f"{item.name:42} {money(item.annual_burden):>14}")
print(f"{'Invoice-delay financing cost':42} {money(case.billing_timing.annual_burden):>14}")
print(f"{'Total annual burden':42} {money(case.total_burden):>14}")
print("\nRECOVERABLE VALUE")
for item in case.burdens:
    print(f"{item.name + ' × ' + str(item.improvement_rate * 100) + '%':42} {money(item.recoverable):>14}")
print(f"{'Timing financing cost × 40%':42} {money(case.billing_timing.recoverable):>14}")
print(f"{'Total recoverable value':42} {money(case.recoverable_value):>14}")
print("Invoice principal is not value: only administration and financing cost are modeled.")
print("\nCUSTOMER ECONOMICS")
print("Implementation price:", money(s.customer.implementation_price))
print("Annual recurring fee:", money(s.customer.recurring_annual_fee))
print("First-year customer cost:", money(s.customer.implementation_price + s.customer.recurring_annual_fee))
print("Retained annual benefit:", money(case.recoverable_value - s.customer.recurring_annual_fee))
print("ROI / payback:", f"{first_year_roi(s.customer):.1%}", "/", f"{payback_period_months(s.customer):.1f} months")
print("\nDELIVERY")
print("Engineering / reusable / customer-specific hours:", e.total_hours,
      s.delivery.reusable_engineering_hours, s.delivery.customer_specific_engineering_hours)
print("Reliability/error handling + QA/testing hours:", e.reliability_error_handling + e.qa_testing)
print("Deployment / rework reserve hours:", e.deployment, "/", e.rework_reserve)
print("Direct delivery cost:", money(implementation_delivery_cost(s.delivery)))
print("Core reuse:", f"{reuse_percentage(s.delivery):.1%}")
print("\nSOLUTIONS ECONOMICS")
print("Solutions hours:", solutions_hours(s.solutions))
print("Contribution:", money(solutions_contribution(s.customer, s.delivery, s.solutions)))
print("Contribution / solutions hour:", money(solutions_contribution(s.customer, s.delivery, s.solutions) / solutions_hours(s.solutions)))
print("\nBUILD VS. BUY\n" + s.build_vs_buy.note)
print("\nSUPPORT")
print("Hosting, monitoring, API/schema/mapping changes, failed handoffs, credentials, workflow changes, customer support, bugs, and maintenance engineering.")
print("Annual recurring revenue / direct support cost / contribution:",
      money(s.customer.recurring_annual_fee), "/", money(annual_support_cost(s.delivery)),
      "/", money(recurring_support_contribution(s.customer, s.delivery)))
result = analyze(s)
print("\nVERDICT\n-------\n" + result.verdict.value + "\nWHY")
for reason in result.reasons: print("-", reason)
print("\nSCENARIOS")
for name, factory in (("Baseline", baseline_case), ("Existing SaaS", existing_saas_case),
        ("Clean integrations", clean_integrations_case), ("Closed integrations", difficult_integrations_case),
        ("High burden", high_burden_case), ("Low burden", low_burden_case),
        ("Highly customer-specific", highly_customer_specific_case),
        ("Unsustainable support", unsustainable_support_case)):
    print(f"{name:30} {analyze(factory().scenario).verdict.value}")
print("\nIMPLEMENTED-CASE COMPARISON")
for row in implemented_case_comparison():
    print(f"{row.name:28} recoverable {money(row.recoverable_value):>13} | {row.verdict}")
