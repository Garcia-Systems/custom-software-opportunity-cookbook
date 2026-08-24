"""Run Case 2. All values are fictional educational assumptions, not benchmarks."""

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
from opportunity_cookbook.restaurant_group import (
    baseline_case, case_comparison, high_standardization_case,
    low_standardization_case, saas_alternative_case, ten_location_case,
)


def money(value: Decimal) -> str:
    return f"${value:,.2f}"


def main() -> None:
    case = baseline_case()
    scenario = case.scenario
    customer, delivery, solutions = scenario.customer, scenario.delivery, scenario.solutions
    result = analyze(scenario)
    print("CASE 2 — THE FIVE-LOCATION RESTAURANT GROUP")
    print("============================================")
    print("Fictional educational scenario (not real restaurant data or a benchmark):")
    print("James River Hospitality Group — five commonly owned restaurants.\n")
    print("LOCATIONS\n5\n")
    print("BUSINESS PROBLEM")
    print("Managers normalize functioning POS, labor, inventory, and reservation exports")
    print("to ask not only what happened, but which locations differ and where to investigate.\n")

    print("CURRENT-STATE BURDEN")
    for burden in case.burdens:
        amount = burden.burden(case.location_count)
        label = f"{burden.name} ({burden.scope.value})"
        print(f"{label:<54}{money(amount):>12}")
    print("-" * 66)
    print(f"{'Location-level burden':<54}{money(case.location_level_burden):>12}")
    print(f"{'Group-level burden':<54}{money(case.group_level_burden):>12}")
    print(f"{'Total annual burden':<54}{money(case.total_burden):>12}\n")

    print("RECOVERABLE VALUE (burden × fictional improvement rate)")
    for burden in case.burdens:
        label = f"{burden.name} × {burden.improvement_rate:.0%}"
        print(f"{label:<54}{money(burden.recoverable(case.location_count)):>12}")
    print(f"{'Total recoverable value':<54}{money(case.recoverable_value):>12}")
    print("Current-state burden is not recoverable value.\n")

    print("CUSTOMER ECONOMICS")
    print(f"Implementation price                              {money(customer.implementation_price)}")
    print(f"Annual recurring fee                              {money(customer.recurring_annual_fee)}")
    print(f"First-year cost                                   {money(customer.implementation_price + customer.recurring_annual_fee)}")
    print(f"Retained first-year benefit                       {money(customer.recoverable_value - customer.implementation_price - customer.recurring_annual_fee)}")
    print(f"Steady-state annual benefit                       {money(customer_net_annual_benefit(customer))}")
    print(f"First-year ROI                                    {first_year_roi(customer):.1%}")
    print(f"Payback                                           {payback_period_months(customer):.1f} months\n")

    engineering = case.engineering
    print("DELIVERY ECONOMICS")
    print(f"Shared engineering hours                         {engineering.shared_hours}")
    print(f"Incremental location hours ({engineering.per_unit_hours} × {case.location_count})              {engineering.incremental_hours}")
    print(f"Customer-specific exception hours                {engineering.exception_hours}")
    print(f"QA / testing hours                               {engineering.qa_hours}")
    print(f"Deployment hours                                 {engineering.deployment_hours}")
    print(f"Rework reserve hours                             {engineering.rework_reserve_hours}")
    print(f"Total engineering hours                          {engineering.total_hours}")
    print(f"Modeled hourly delivery cost                     {money(delivery.engineering_hourly_cost)}")
    print(f"Other direct costs                               {money(delivery.other_direct_costs)}")
    print(f"Direct implementation cost                       {money(implementation_delivery_cost(delivery))}\n")

    print("REUSE")
    print(f"Within-customer core reuse ratio                  {reuse_percentage(delivery):.1%}")
    print("Within-customer reuse: " + case.within_customer_reuse)
    print("Potential cross-customer reuse: " + case.potential_cross_customer_reuse + "\n")

    sw = case.solutions_work
    print("SOLUTIONS ECONOMICS")
    print(f"Prospecting / sales hours                        {sw.prospecting_sales_hours}")
    print(f"Discovery + multi-location discovery             {sw.discovery_hours + sw.multi_location_discovery_hours}")
    print(f"Design + commercial / proposal                   {sw.solution_design_hours + sw.commercial_proposal_hours}")
    print(f"Coordination + acceptance                        {sw.coordination_hours + sw.acceptance_hours}")
    print(f"Total solutions hours                            {solutions_hours(solutions)}")
    print(f"Implementation contribution                      {money(solutions_contribution(customer, delivery, solutions))}")
    print(f"Contribution / solutions hour                    {money(effective_contribution_per_solutions_hour(customer, delivery, solutions))}\n")

    print("SALES")
    print("One ownership group; one buyer relationship, discovery process, contract, and")
    print("procurement motion cover five operating locations. More managers, variation,")
    print("coordination, and implementation risk still make this harder than Case 1.\n")

    print("SUPPORT")
    print(f"Fixed support hours                              {case.support.fixed_hours}")
    print(f"Per-location support hours ({case.support.per_unit_hours} × {case.location_count})              {case.support.per_unit_hours * case.location_count}")
    print(f"Exception support hours                          {case.support.exception_hours}")
    print(f"Annual recurring revenue                         {money(customer.recurring_annual_fee)}")
    print(f"Annual direct support cost                       {money(annual_support_cost(delivery))}")
    print(f"Recurring contribution                           {money(recurring_support_contribution(customer, delivery))}\n")

    print("BUILD VS. BUY")
    print("The baseline assumes multi-location SaaS, vendor-native enterprise reporting,")
    print("configuration, automation, manual process, and custom integration were compared")
    print("and left a cross-system gap. This is a discovery assumption, not a market fact;")
    print("the strong-SaaS scenario correctly selects BUY / CONFIGURE.\n")

    print(f"VERDICT\n-------\n{result.verdict.value}\n\nWHY")
    for reason in result.reasons:
        print(f"- {reason}")

    print("\nCASE 1 VS. CASE 2")
    one, five = case_comparison()
    print(f"{'Calculated measure':<32}{'Case 1':>20}  {'Case 2':>34}")
    print(f"{'Locations':<32}{one.locations:>20}  {five.locations:>34}")
    for label, attr, formatter in (
        ("Current-state burden", "burden", money),
        ("Recoverable value", "recoverable_value", money),
        ("Engineering hours", "engineering_hours", str),
        ("Implementation price", "implementation_price", money),
        ("Solutions hours", "solutions_hours", str),
        ("Annual support cost", "annual_support_cost", money),
        ("Core engineering reuse", "reuse", lambda x: f"{x:.1%}"),
        ("Customer payback", "payback_months", lambda x: f"{x:.1f} months"),
        ("Verdict", "verdict", str),
    ):
        print(f"{label:<32}{formatter(getattr(one, attr)):>20}  {formatter(getattr(five, attr)):>34}")
    value_growth = five.recoverable_value / one.recoverable_value
    effort_growth = five.engineering_hours / one.engineering_hours
    print(f"Recoverable-value growth: {value_growth:.2f}×; engineering-hour growth: {effort_growth:.2f}×.")
    print("Here value scales faster than delivery effort; this is a modeled result, not a rule.\n")

    print("SCENARIO TESTS")
    for label, candidate in (
        ("Baseline", baseline_case()),
        ("Single-location comparison", None),
        ("High standardization", high_standardization_case()),
        ("Low standardization", low_standardization_case()),
        ("Strong SaaS alternative", saas_alternative_case()),
        ("Ten-location thought experiment", ten_location_case()),
    ):
        if candidate is None:
            print(f"{label:<36}{one.verdict}")
        else:
            print(f"{label:<36}{analyze(candidate.scenario).verdict.value} ({candidate.engineering.total_hours} engineering hours)")
    print("\nA good project is not proof of a repeatable market. Validate system overlap,")
    print("unresolved needs, reachable buyers, SaaS gaps, and repeated willingness to pay.")


if __name__ == "__main__":
    main()
