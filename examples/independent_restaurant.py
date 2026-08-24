"""Run Case 1. All values are fictional educational assumptions, not benchmarks."""

from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (
    annual_support_cost, customer_net_annual_benefit,
    effective_contribution_per_solutions_hour, first_year_roi,
    implementation_delivery_cost, payback_period_months,
    recurring_support_contribution, reuse_percentage, solutions_contribution,
    solutions_hours,
)
from opportunity_cookbook.independent_restaurant import (
    baseline_case, higher_value_case, lower_delivery_cost_case,
    saas_alternative_case,
)


def money(value: Decimal) -> str:
    return f"${value:,.2f}"


def main() -> None:
    case = baseline_case()
    scenario = case.scenario
    c, d, s = scenario.customer, scenario.delivery, scenario.solutions
    result = analyze(scenario)
    print("CASE 1 — THE INDEPENDENT RESTAURANT\n===================================")
    print("Fictional educational scenario (not real restaurant data or a benchmark):")
    print("James River Kitchen — one independently owned, approximately 120-seat location;")
    print("dine-in and takeout, a seasonal/local menu, and a small management team.\n")
    print("BUSINESS PROBLEM")
    print("Management repeatedly reconciles functioning POS, reservation, scheduling,")
    print("inventory/CSV, and feedback tools; mismatched exports delay a pre-service view.\n")
    print("CURRENT-STATE BURDEN")
    for item in case.burdens:
        print(f"{item.name:<43}{money(item.annual_burden):>12}")
    print("-" * 55)
    print(f"{'Total burden':<43}{money(case.total_burden):>12}\n")
    print("RECOVERABLE VALUE (burden × fictional improvement rate)")
    for item in case.burdens:
        print(f"{item.name + ' × ' + format(item.improvement_rate, '.0%'):<43}{money(item.recoverable_value):>12}")
    print(f"{'Total recoverable value':<43}{money(case.recoverable_value):>12}")
    print("Total burden is not recoverable value; most burden remains.\n")
    print("CUSTOMER ECONOMICS")
    print(f"Implementation price                         {money(c.implementation_price)}")
    print(f"Recurring annual fee                         {money(c.recurring_annual_fee)}")
    print(f"First-year cost                              {money(c.implementation_price + c.recurring_annual_fee)}")
    print(f"Retained annual benefit                      {money(customer_net_annual_benefit(c))}")
    print(f"First-year ROI                               {first_year_roi(c):.1%}")
    print(f"Payback                                      {payback_period_months(c):.1f} months\n")
    print("DELIVERY")
    for item in case.delivery_work:
        if item.name in {"Testing", "Deployment", "Rework reserve"}:
            category = "delivery overhead (excluded from reuse ratio)"
        else:
            category = "common/potentially reusable" if item.reusable else "customer-specific"
        print(f"- {item.name}: {item.hours} hours ({category})")
    total_hours = (d.reusable_engineering_hours + d.customer_specific_engineering_hours
                   + d.qa_hours + d.deployment_hours + d.rework_reserve_hours)
    print(f"Engineering hours                            {total_hours}")
    print(f"Reusable core hours                          {d.reusable_engineering_hours}")
    print(f"Customer-specific core hours                 {d.customer_specific_engineering_hours}")
    print(f"Direct delivery cost                         {money(implementation_delivery_cost(d))}\n")
    print("SOLUTIONS ECONOMICS")
    print(f"Prospecting / sales hours                    {s.prospecting_sales_hours}")
    print(f"Discovery hours                              {s.discovery_hours}")
    print(f"Solution-design / scoping hours              {s.solution_design_hours}")
    print(f"Coordination / acceptance hours              {s.coordination_acceptance_hours}")
    print(f"Total solutions hours                        {solutions_hours(s)}")
    print(f"Implementation contribution                  {money(solutions_contribution(c, d, s))}")
    print(f"Contribution / solutions hour                {money(effective_contribution_per_solutions_hour(c, d, s))}\n")
    print("BUILD VS. BUY")
    print("Manual work, a better spreadsheet, SaaS configuration, low-code automation,")
    print("another reporting product, narrow custom integration, and doing nothing were")
    print("modeled as alternatives. Baseline custom superiority is only a fictional")
    print("assumption requiring discovery; the strong-SaaS scenario reverses it.\n")
    print("SUPPORT")
    print("Obligations: " + "; ".join(case.support_obligations) + ".")
    print(f"Annual recurring revenue                     {money(c.recurring_annual_fee)}")
    print(f"Annual direct support cost                   {money(annual_support_cost(d))}")
    print(f"Recurring contribution                       {money(recurring_support_contribution(c, d))}\n")
    print(f"REUSE\nCore engineering reuse                       {reuse_percentage(d):.1%}")
    print("This is potential portability, not guaranteed future economic value.\n")
    print(f"VERDICT\n-------\n{result.verdict.value}\n\nWHY")
    for reason in result.reasons:
        print(f"- {reason}")
    print("\nSCENARIO TESTS")
    scenarios = (
        ("Baseline", baseline_case()),
        ("Higher recoverable value", higher_value_case()),
        ("Lower delivery cost", lower_delivery_cost_case()),
        ("Strong SaaS alternative", saas_alternative_case()),
    )
    for label, candidate in scenarios:
        print(f"{label:<31}{analyze(candidate.scenario).verdict.value}")
    print("\nTECHNICALLY USEFUL does not necessarily mean ECONOMICALLY ATTRACTIVE.")


if __name__ == "__main__":
    main()
