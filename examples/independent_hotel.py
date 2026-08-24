"""Run Case 3. Every number is a fictional educational assumption."""

from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    customer_net_annual_benefit, effective_contribution_per_solutions_hour,
    first_year_roi, implementation_delivery_cost, payback_period_months,
    recurring_support_contribution, reuse_percentage, solutions_contribution,
    solutions_hours)
from opportunity_cookbook.independent_hotel import (baseline_case,
    difficult_integration_case, easy_integration_case, higher_burden_case,
    strong_saas_case)
from opportunity_cookbook.restaurant_group import case_comparison


def money(value: Decimal) -> str:
    return f"${value:,.2f}"


def main() -> None:
    case = baseline_case()
    s = case.scenario
    c, d = s.customer, s.delivery
    result = analyze(s)
    print("CASE 3 — THE INDEPENDENT HOTEL\n================================")
    print("Fictional educational scenario (not real hotel data or an industry benchmark):")
    print("James River Inn — one 138-room independent property serving fictional leisure")
    print("and business guests, with seasonal demand, front desk, housekeeping, and a small management team.\n")
    print("CURRENT SYSTEMS")
    print("PMS / reservations; direct and third-party booking channels; housekeeping;")
    print("staff scheduling; guest feedback; spreadsheets / exports. Management manually reconciles them.\n")
    print("CURRENT-STATE BURDEN")
    for item in case.burdens:
        formula = (f"{item.hours_per_week}h × {money(item.loaded_hourly_cost)} × {item.operating_weeks}w"
                   if item.hours_per_week else f"fictional loss pool {money(item.annual_nonlabor_loss)}")
        print(f"{item.name:<36}{money(item.annual_burden):>12}  ({formula})")
    print("-" * 50)
    print(f"{'Total annual burden':<36}{money(case.total_burden):>12}\n")
    print("RECOVERABLE VALUE (measurable burden × credible fictional improvement)")
    for item in case.burdens:
        print(f"{item.name + f' × {item.improvement_rate:.0%}':<44}{money(item.recoverable_value):>12}")
    print(f"{'Total recoverable value':<44}{money(case.recoverable_value):>12}")
    print("The operational-loss pool is separate from labor. No unsold room-night revenue is claimed.\n")
    print("CUSTOMER ECONOMICS")
    print(f"Implementation price                 {money(c.implementation_price)}")
    print(f"Annual recurring fee                 {money(c.recurring_annual_fee)}")
    print(f"First-year cost                      {money(c.implementation_price + c.recurring_annual_fee)}")
    print(f"Retained first-year benefit          {money(c.recoverable_value - c.implementation_price - c.recurring_annual_fee)}")
    print(f"Steady-state retained benefit        {money(customer_net_annual_benefit(c))}")
    print(f"First-year ROI                       {first_year_roi(c):.1%}")
    print(f"Payback                              {payback_period_months(c):.1f} months\n")
    total_hours = sum((d.reusable_engineering_hours, d.customer_specific_engineering_hours,
                       d.qa_hours, d.deployment_hours, d.rework_reserve_hours), Decimal("0"))
    print("DELIVERY")
    print(f"Engineering hours                    {total_hours}")
    print(f"Potentially reusable core hours      {d.reusable_engineering_hours}")
    print(f"Property-specific core hours         {d.customer_specific_engineering_hours}")
    print(f"QA / testing                         {d.qa_hours}")
    print(f"Deployment                           {d.deployment_hours}")
    print(f"Rework reserve                       {d.rework_reserve_hours}")
    print(f"Derived core reuse                   {reuse_percentage(d):.1%}")
    print(f"Direct delivery cost                 {money(implementation_delivery_cost(d))}\n")
    print("SOLUTIONS ECONOMICS")
    for name, hours in vars(case.solutions_work).items():
        print(f"{name.replace('_', ' ').title():<39}{hours}")
    print(f"Total solutions hours                {solutions_hours(s.solutions)}")
    print(f"Contribution                         {money(solutions_contribution(c, d, s.solutions))}")
    print(f"Contribution / solutions hour        {money(effective_contribution_per_solutions_hour(c, d, s.solutions))}\n")
    print("INTEGRATION ACCESS\n" + case.integration_access_note + "\n")
    print("BUILD VS. BUY")
    print(s.build_vs_buy.note)
    print("The mature hotel-software ecosystem is a real competitive constraint; discovery must")
    print("exclude an adequate PMS module, reporting SaaS, BI/configuration, or simpler process first.\n")
    print("SUPPORT")
    print(f"Recurring revenue                    {money(c.recurring_annual_fee)}")
    print(f"Support engineering                  {d.annual_support_hours}h")
    print(f"Hosting/monitoring/other costs       {money(d.annual_support_other_direct_costs)}")
    print(f"Direct recurring cost                {money(annual_support_cost(d))}")
    print(f"Recurring contribution               {money(recurring_support_contribution(c, d))}\n")
    print(f"VERDICT\n-------\n{result.verdict.value}\n\nWHY")
    for reason in result.reasons:
        print("- " + reason)
    print("\nSCENARIOS")
    variants = (("Baseline", baseline_case()), ("Strong SaaS alternative", strong_saas_case()),
                ("Easy integration", easy_integration_case()),
                ("Difficult PMS integration", difficult_integration_case()),
                ("Higher operational burden", higher_burden_case()))
    for label, candidate in variants:
        cost = implementation_delivery_cost(candidate.scenario.delivery)
        print(f"{label:<31}{analyze(candidate.scenario).verdict.value:<38} delivery {money(cost)}")
    print("\nIMPLEMENTED-CASE COMPARISON")
    one, group = case_comparison()
    hotel_hours = total_hours
    print(f"{'Opportunity':<25}{'Value':>13}{'Delivery h':>13}{'Reuse':>10}{'Sales':>12}  Verdict")
    print(f"{'Independent restaurant':<25}{money(one.recoverable_value):>13}{one.engineering_hours:>13}{one.reuse:>10.1%}{'moderate':>12}  {one.verdict}")
    print(f"{'Restaurant group':<25}{money(group.recoverable_value):>13}{group.engineering_hours:>13}{group.reuse:>10.1%}{'moderate':>12}  {group.verdict}")
    print(f"{'Independent hotel':<25}{money(case.recoverable_value):>13}{hotel_hours:>13}{reuse_percentage(d):>10.1%}{'moderate':>12}  {result.verdict.value}")
    print("\nDoes the independent hotel behave economically more like the single restaurant or")
    print("the restaurant group? Here the calculated baseline resembles the single restaurant's")
    print("NO DEAL outcome despite greater activity: first-year value does not clear price.")
    print("This property result is not evidence of a repeatable independent-hotel market.")


if __name__ == "__main__":
    main()
