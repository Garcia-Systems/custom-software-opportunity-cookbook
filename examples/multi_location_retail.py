"""Run Case 6. Every value is a fictional educational assumption."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (alternative_first_year_effect,
    annual_support_cost, custom_first_year_effect, first_year_roi,
    implementation_delivery_cost, payback_period_months, reuse_percentage,
    solutions_contribution, solutions_hours)
from opportunity_cookbook.multi_location_retail import (baseline_case,
    higher_burden_case, highly_standardized_case, messy_acquired_stores_case,
    one_off_niche_case, strong_saas_alternative_case,
    weak_saas_alternative_case)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison


def money(value):
    return f"${value:,.2f}"


case = baseline_case()
s = case.scenario
print("CASE 6 — THE MULTI-LOCATION RETAILER")
print("=" * 38)
print("Fictional educational scenario: James River Outfitters")
print("\nBUSINESS\n6 physical stores + one e-commerce channel; centralized regional operations")
print("\nCURRENT SYSTEMS\nPOS; inventory; purchasing; e-commerce; returns; scheduling; spreadsheets/exports")
print("\nCURRENT-STATE BURDEN")
for item in case.burdens:
    print(f"{item.name:42} {money(item.annual_burden):>14}")
print(f"{'Total annual burden':42} {money(case.total_burden):>14}")
print("\nRECOVERABLE VALUE")
for item in case.burdens:
    print(f"{item.name + ' × ' + str(item.improvement_rate * 100) + '%':42} {money(item.recoverable):>14}")
print(f"{'Total recoverable value':42} {money(case.recoverable_value):>14}")
print("\nCUSTOM OPTION")
print("Implementation price", money(s.customer.implementation_price))
print("Recurring fee", money(s.customer.recurring_annual_fee))
print("Delivery cost", money(implementation_delivery_cost(s.delivery)))
print("Support cost", money(annual_support_cost(s.delivery)))
print("First-year total economic effect", money(custom_first_year_effect(s.customer, case.custom_risk_allowance)))
print("\nBUY / CONFIGURE OPTION")
for label, value in (("Setup/configuration", case.alternative.setup_cost),
        ("Recurring subscription", case.alternative.recurring_annual_cost),
        ("Internal administration", case.alternative.internal_administration_cost),
        ("Residual unresolved burden", case.alternative.residual_annual_burden),
        ("Risk allowance", case.alternative.risk_allowance)):
    print(label, money(value))
print("First-year total economic effect", money(alternative_first_year_effect(case.alternative)))
print("\nCUSTOMER ECONOMICS")
print("First-year ROI", f"{first_year_roi(s.customer):.1%}")
print("Payback", f"{payback_period_months(s.customer):.1f} months")
e = case.engineering
print("\nDELIVERY")
print("Shared / per-store total / e-commerce / exception hours:",
      e.shared_hours, e.per_store_total_hours, e.ecommerce_hours, e.exception_hours)
print("QA / deployment / rework hours:", e.qa_hours, e.deployment_hours, e.rework_reserve_hours)
print("Total engineering hours:", e.total_hours)
print("\nREUSE\n", case.within_customer_reuse, "\n", case.future_customer_reuse)
print("Core reuse percentage:", f"{reuse_percentage(s.delivery):.1%}")
print("\nSOLUTIONS ECONOMICS")
print("Solutions hours:", solutions_hours(s.solutions))
print("Implementation contribution after delivery and solutions labor:", money(solutions_contribution(s.customer, s.delivery, s.solutions)))
print("\nSUPPORT\nRecurring obligations include hosting, monitoring, API and mapping drift, store onboarding, returns changes, bug fixes, and customer support.")
print("Recurring fee / direct support cost:", money(s.customer.recurring_annual_fee), "/", money(annual_support_cost(s.delivery)))
result = analyze(s)
print("\nBUILD VS. BUY\n", s.build_vs_buy.note)
print("\nVERDICT\n-------\n", result.verdict.value)
print("WHY")
for reason in result.reasons:
    print("-", reason)
print("\nSCENARIOS")
for name, factory in (("Baseline", baseline_case), ("Weak SaaS alternative", weak_saas_alternative_case),
        ("Strong SaaS alternative", strong_saas_alternative_case),
        ("Highly standardized systems", highly_standardized_case),
        ("Messy acquired stores", messy_acquired_stores_case),
        ("Higher measurable burden", higher_burden_case),
        ("One-off niche requirement", one_off_niche_case)):
    print(f"{name:30} {analyze(factory().scenario).verdict.value}")
print("\nIMPLEMENTED-CASE COMPARISON")
for row in implemented_case_comparison():
    print(f"{row.name:28} recoverable {money(row.recoverable_value):>13} | {row.verdict}")
