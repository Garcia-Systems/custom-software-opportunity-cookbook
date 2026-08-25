"""Run Case 12's fictional two-stage opportunity analysis."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.buy_dont_build import baseline_case, scenario_results
from opportunity_cookbook.economics import (annual_support_cost, first_year_roi,
    implementation_delivery_cost, payback_period_months, recurring_support_contribution,
    reuse_percentage, solutions_contribution)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison


def money(value): return f"${value:,.2f}"
def months(value): return "not meaningful" if value is None else f"{value:.1f} months"


case = baseline_case(); stage = case.stage_one
print("CASE 12 — THE PERFECT-LOOKING DEAL THAT ISN'T\n" + "=" * 48)
print("Fictional educational scenario:\nJames River Equipment Services")
print("Regional equipment-service company; 26 employees; fictional assumptions, not benchmarks.")
print("\nSTAGE 1 — BEFORE ALTERNATIVE DISCOVERY")
for label, value in (("Current-state burden", case.total_burden),
        ("Recoverable value", case.recoverable_value),
        ("Custom implementation", stage.customer.implementation_price),
        ("Recurring fee", stage.customer.recurring_annual_fee),
        ("First-year customer cost", stage.customer.implementation_price + stage.customer.recurring_annual_fee)):
    print(f"{label:38} {money(value):>14}")
print(f"{'Customer ROI':38} {first_year_roi(stage.customer):>13.1%}")
print(f"{'Payback':38} {months(payback_period_months(stage.customer)):>14}")
print("Delivery cost / solutions contribution:", money(implementation_delivery_cost(stage.delivery)), "/", money(solutions_contribution(stage.customer, stage.delivery, stage.solutions)))
print("Support cost / contribution:", money(annual_support_cost(stage.delivery)), "/", money(recurring_support_contribution(stage.customer, stage.delivery)))
print("Core reuse:", f"{reuse_percentage(stage.delivery):.0%}")
print("Initial verdict:\n" + analyze(stage).verdict.value)

print("\nSTAGE 2 — DISCOVERY FINDS AN ALTERNATIVE")
print("Fictional alternative:\n" + case.saas_name)
print("Provides standard synchronization, scheduling, technician status, accounting integration, notifications, and reporting.")
for label, value in (("Setup/configuration", case.saas.setup_cost),
        ("Annual subscription", case.saas.recurring_annual_cost),
        ("Internal setup/admin labor", case.saas.internal_administration_cost),
        ("Original burden", case.total_burden),
        ("Burden removed by SaaS", case.saas_recoverable_value),
        ("Residual burden", case.saas.residual_annual_burden)):
    print(f"{label:38} {money(value):>14}")

print("\nOPTION COMPARISON")
print(f"{'Option':29} {'first-year cost':>15} {'recurring':>12} {'remaining':>12} {'net benefit':>13} {'payback':>14}")
for option in case.options():
    print(f"{option.name:29} {money(option.first_year_cost):>15} {money(option.recurring_cost):>12} {money(option.burden_remaining):>12} {money(option.first_year_net_benefit):>13} {months(option.payback_months):>14}")
print("\nCUSTOM VALUE VS STATUS QUO       ", money(case.recoverable_value))
print("INCREMENTAL CUSTOM VALUE VS SaaS", money(case.incremental_custom_value))
print("\nBREAK-EVEN")
print("Residual burden needed for custom's first-year total effect to beat SaaS:", money(case.break_even_residual_burden))

result = analyze(case.final_scenario)
print("\nFINAL VERDICT\n-------------\n" + result.verdict.value + "\nWHY")
for reason in result.reasons: print("-", reason)
print("- SaaS removes about 90% of the custom-recoverable burden; the unique gap is too small to fund the edge.")
print("- Discovery avoided an inferior full-custom commitment; that is successful qualification, not a custom sale.")
print("\nSCENARIOS")
for name, verdict in scenario_results(): print(f"{name:32} {verdict}")
print("\nIMPLEMENTED-CASE COMPARISON")
for row in implemented_case_comparison():
    print(f"{row.name:28} value {money(row.recoverable_value):>12} | delivery {row.delivery_difficulty:8} | reuse {row.reuse:.0%} | {row.verdict}")
