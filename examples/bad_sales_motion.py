"""Run Case 14's fictional market-motion analysis."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.bad_sales_motion import (baseline_case, case_13_vs_14,
    case_9_vs_14, close_rate_sensitivity, scenario_results)
from opportunity_cookbook.economics import (first_year_roi, payback_period_months,
    reuse_percentage)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison


def money(value): return f"${value:,.2f}"

case = baseline_case(); s = case.scenario; d = s.delivery
print("CASE 14 — GREAT PRODUCT, BAD SALES MOTION")
print("=" * 41)
print("Fictional educational scenario:\nJames River Professional Association")
print("Regional membership association; 2,200 members; small staff. Every assumption is invented, not a benchmark.")
print("\nCUSTOMER ECONOMICS")
for label, value in (("Current-state burden", case.total_burden), ("Recoverable value", case.recoverable_value),
                     ("Implementation price", s.customer.implementation_price), ("Recurring fee", s.customer.recurring_annual_fee),
                     ("Customer retained benefit", case.recoverable_value-s.customer.implementation_price-s.customer.recurring_annual_fee)):
    print(f"{label:40} {money(value):>14}")
print(f"{'First-year ROI':40} {first_year_roi(s.customer):>13.1%}")
print(f"{'Payback':40} {payback_period_months(s.customer):>10.1f} months")
print("\nDELIVERY ECONOMICS")
hours=sum((d.reusable_engineering_hours,d.customer_specific_engineering_hours,d.qa_hours,d.deployment_hours,d.rework_reserve_hours,d.uncertainty_reserve_hours))
print(f"{'Mature-customer engineering hours':40} {hours:>14}")
print(f"{'Reusable core work':40} {reuse_percentage(d):>13.1%}")
print(f"{'Customer-specific core work':40} {1-reuse_percentage(d):>13.1%}")
print(f"{'Direct delivery cost':40} {money(case.delivery_cost):>14}")
print(f"{'Implementation contribution':40} {money(case.implementation_contribution):>14}")
print("Reusable: adapters, domain model, normalization, reporting, validation, deployment, monitoring.")
print("Customer-specific: credentials, mappings, minor rules, report configuration, acceptance.")
print("\nSUPPORT")
print(f"{'Recurring direct cost':40} {money(case.support_cost):>14}")
print(f"{'Recurring contribution':40} {money(case.recurring_contribution):>14}")
print("\nSALES MOTION")
print(f"{'Sales hours / qualified opportunity':40} {case.acquisition.hours_per_qualified_opportunity:>14}")
print(f"{'Close probability':40} {case.acquisition.close_probability:>13.0%}")
print(f"{'Expected sales hours / won customer':40} {case.expected_sales_hours:>14}")
print(f"{'Expected acquisition cost':40} {money(case.acquisition_cost):>14}")
print(f"{'Sales cycle':40} {case.acquisition.sales_cycle_months:>10} months")
print("A long cycle delays cash, occupies follow-up capacity, lowers throughput, and adds forecast uncertainty; no arbitrary dollar charge is assigned to months.")
print("\nAFTER ACQUISITION")
print(f"{'Contribution before acquisition':40} {money(case.contribution_before_acquisition):>14}")
print(f"{'Expected acquisition cost':40} {money(case.acquisition_cost):>14}")
print(f"{'Contribution after acquisition':40} {money(case.contribution_after_acquisition):>14}")
print("\nMARKET PRICE CORRIDOR")
print(f"{'Customer maximum economic price':40} {money(case.customer_maximum_price):>14}")
print(f"{'Acquisition-adjusted minimum price':40} {money(case.acquisition_adjusted_minimum_price):>14}")
print(f"{'Feasible?':40} {'YES' if case.feasible_corridor else 'NO':>14}")
print("\nVERDICT\n-------\n" + case.result.verdict.value + "\nWHY")
for reason in case.result.reasons: print("-", reason)
print("- Customer value is meaningful, delivery inexpensive, technical reuse strong, and support manageable.")
print("\nSCENARIOS")
for name, verdict, contribution in scenario_results(): print(f"{name:32} {verdict:36} | after acquisition {money(contribution)}")
print("\nCLOSE-RATE SENSITIVITY")
for rate, hours, cost in close_rate_sensitivity(): print(f"{rate:>4.0%} close | {hours:>7.2f} expected hours/win | {money(cost):>12}")
print("\nENGINEERING REUSE VS. SALES REUSE")
print("Same adapters/domain/deployment do not imply the same ICP, buyer, pain, demo, scope, proposal, or procurement motion.")
print("\nCASE 13 VS. CASE 14")
for row in case_13_vs_14(): print(" | ".join(row))
print("\nCASE 9 VS. CASE 14")
for row in case_9_vs_14(): print(" | ".join(row))
print("\nIMPLEMENTED-CASE COMPARISON")
for row in implemented_case_comparison():
    reuse="n/a" if row.reuse is None else f"{row.reuse:.0%}"
    print(f"{row.name:28} value {money(row.recoverable_value):>12} | delivery {row.delivery_difficulty:8} | reuse {reuse:>4} | sales/procurement {row.sales_procurement_difficulty:8} | {row.verdict}")
print("\nDISCOVERY / GO-TO-MARKET QUESTIONS")
for q in ("Is the burden and willingness to pay repeatable across the ICP?", "Who owns the budget and who joins approval?",
          "Which sales steps can use one demo, scope, price, proposal, and onboarding path?", "What are qualified close rate and solutions hours by channel?",
          "Can referrals or trusted providers supply qualified demand, and at what transparent cost?", "Do larger associations preserve similar delivery and selling effort?",
          "Which interfaces, permissions, support expectations, and vendor changes must be validated?"):
    print("-", q)
