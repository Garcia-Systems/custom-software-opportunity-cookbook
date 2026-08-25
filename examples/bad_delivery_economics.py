"""Run Case 13's fictional opportunity analysis."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.bad_delivery_economics import (baseline_case,
    case_12_vs_13, case_7_vs_13, scenario_results)
from opportunity_cookbook.economics import (annual_support_cost, first_year_roi,
    payback_period_months, recurring_support_contribution, reuse_percentage)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison


def money(value): return f"${value:,.2f}"


case = baseline_case(); scenario = case.scenario; delivery = scenario.delivery
print("CASE 13 — GREAT CUSTOMER VALUE, BAD DELIVERY ECONOMICS")
print("=" * 56)
print("Fictional educational scenario:\nJames River Specialty Distribution")
print("Regional specialty distributor; approximately 50 employees; all assumptions are invented, not benchmarks.")
print("\nCUSTOMER PROBLEM")
print("Orders move through validation, inventory, special ordering, fulfillment, shipping, invoicing, and reconciliation.")
print("Disconnected portal, warehouse, supplier, carrier, accounting, email, and spreadsheet workflows require manual orchestration.")
print("\nCURRENT-STATE BURDEN / RECOVERABLE VALUE")
for burden in case.burdens:
    print(f"{burden.name:47} {burden.hours_per_week:>4} h/w × {money(burden.hourly_cost):>9} × 52 = {money(burden.annual_burden):>11}; recover {burden.improvement_rate:>4.0%} = {money(burden.recoverable_value):>10}")
print(f"{'Total annual burden':47} {money(case.total_burden):>47}")
print(f"{'Total recoverable value':47} {money(case.recoverable_value):>47}")
print("\nCUSTOMER ECONOMICS AT PROPOSED PRICE")
for label, value in (("Implementation price", scenario.customer.implementation_price),
                     ("Recurring fee", scenario.customer.recurring_annual_fee),
                     ("First-year retained benefit", case.recoverable_value - scenario.customer.implementation_price - scenario.customer.recurring_annual_fee)):
    print(f"{label:38} {money(value):>14}")
print(f"{'First-year ROI':38} {first_year_roi(scenario.customer):>13.1%}")
print(f"{'Payback':38} {payback_period_months(scenario.customer):>12.1f} months")
print("\nTECHNICAL DISCOVERY / BASE ENGINEERING")
for work in case.base_work:
    print(f"{work.name:47} {work.hours:>6} h  {'reusable' if work.reusable else 'customer-specific'}")
print("Poorly documented interfaces, inconsistent identifiers, special-order paths, accounting mappings, weak test access, and exception rules drive the estimate.")
print("\nDELIVERY ECONOMICS")
for label, value in (("Base engineering hours", case.base_engineering_hours),
                     ("Testing / validation", delivery.qa_hours),
                     ("Deployment", delivery.deployment_hours),
                     ("Rework reserve", delivery.rework_reserve_hours),
                     ("Integration uncertainty reserve", delivery.uncertainty_reserve_hours),
                     ("Total engineering hours", case.total_engineering_hours)):
    print(f"{label:38} {value:>14} h")
print(f"{'Other direct cost':38} {money(delivery.other_direct_costs):>14}")
print(f"{'Direct delivery cost':38} {money(case.direct_delivery_cost):>14}")
print("\nIMPLEMENTATION CONTRIBUTION")
print(f"{'Revenue':38} {money(scenario.customer.implementation_price):>14}")
print(f"{'Direct delivery cost':38} {money(case.direct_delivery_cost):>14}")
print(f"{'Contribution':38} {money(case.implementation_contribution):>14}")
print("\nPRICE CORRIDOR")
print(f"{'Delivery break-even price':38} {money(case.break_even_price):>14}")
print(f"{'Target-contribution price':38} {money(case.target_price):>14}")
print(f"{'Customer maximum economic price':38} {money(case.customer_maximum_price):>14}")
print(f"{'Feasible corridor?':38} {'YES' if case.feasible_price_corridor else 'NO':>14}")
print("\nREUSE")
print(f"Reusable core hours: {delivery.reusable_engineering_hours}; customer-specific core hours: {delivery.customer_specific_engineering_hours}; reuse: {reuse_percentage(delivery):.1%}")
print("Future hypothetical reuse is excluded from this engagement's contribution.")
print("\nSUPPORT")
print("Annual support cost / recurring contribution:", money(annual_support_cost(delivery)), "/", money(recurring_support_contribution(scenario.customer, delivery)))
result = analyze(scenario)
print("\nVERDICT\n-------\n" + result.verdict.value + "\nWHY")
print("- Customer value is real and the proposed price produces attractive customer ROI.")
for reason in result.reasons: print("-", reason)
print("- The target-contribution price exceeds the customer's modeled economic maximum; no feasible baseline corridor exists.")
print("- Speculative reuse cannot turn the actual loss-making engagement into a promising deal.")
print("\nREDESIGN")
print("Build less: omit a supplier adapter, use approved CSV, retain a manual exception path, make one system read-only, defer accounting write-back, and support the highest-volume path first.")
print("\nSCENARIOS")
for name, verdict in scenario_results(): print(f"{name:32} {verdict}")
print("\nCASE 12 VS. CASE 13")
for name, verdict, alternative in case_12_vs_13(): print(f"{name:10} {verdict:34} | alternative: {alternative}")
print("\nCASE 7 VS. CASE 13")
for name, verdict, difficulty in case_7_vs_13(): print(f"{name:10} {verdict:34} | integration difficulty: {difficulty}")
print("\nIMPLEMENTED-CASE COMPARISON")
for row in implemented_case_comparison():
    reuse = "n/a" if row.reuse is None else f"{row.reuse:.0%}"
    print(f"{row.name:28} value {money(row.recoverable_value):>12} | delivery {row.delivery_difficulty:8} | reuse {reuse:>4} | {row.verdict}")
print("\nPAID DISCOVERY QUESTIONS")
for question in ("Which interfaces are supported, documented, permissioned, and testable?",
                 "Who owns identifier normalization and supplier-format changes?",
                 "Which special-order and exception paths are truly required for launch?",
                 "What idempotency, reconciliation, rollback, and acceptance evidence is required?",
                 "Can CSV, read-only access, or a retained manual path replace a costly write integration?",
                 "Who owns monitoring, incident response, vendor changes, and ongoing support?"):
    print("-", question)
