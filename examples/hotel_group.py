"""Run Case 4. Every value is a fictional educational assumption."""
from decimal import Decimal
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost, customer_net_annual_benefit,
    effective_contribution_per_solutions_hour, first_year_roi, implementation_delivery_cost,
    payback_period_months, recurring_support_contribution, reuse_percentage,
    solutions_contribution, solutions_hours)
from opportunity_cookbook.hotel_group import (BurdenScope, baseline_case,
    case_three_comparison, fragmented_portfolio_case, high_standardization_case,
    larger_group_case, strong_saas_case)
from opportunity_cookbook.restaurant_group import case_comparison

def money(v: Decimal) -> str: return f"${v:,.2f}"

def main() -> None:
    case = baseline_case(); s = case.scenario; c = s.customer; d = s.delivery
    result = analyze(s)
    print("CASE 4 — THE SMALL HOTEL GROUP\n================================")
    print("Fictional educational scenario (not hotel data or an industry benchmark):")
    print(f"James River Lodging Group — {case.property_count} properties / approximately {case.room_count} rooms\n")
    print("BUSINESS PROBLEM\nProperties ask what is happening locally; central management asks which property")
    print("differs, by how much, and where to investigate. Manual consolidation delays that answer.\n")
    print("CURRENT-STATE BURDEN")
    for b in case.burdens:
        multiplier = f" × {case.property_count} properties" if b.scope is BurdenScope.PROPERTY else ""
        print(f"{b.name:<34}{money(b.annual_burden(case.property_count)):>13}  ({b.hours_per_week}h × {money(b.loaded_hourly_cost)} × {b.operating_weeks}w{multiplier})")
    print(f"{'Property-level burden':<34}{money(case.property_level_burden):>13}")
    print(f"{'Central group burden':<34}{money(case.central_burden):>13}")
    print(f"{'Total annual burden':<34}{money(case.total_burden):>13}\n")
    print("RECOVERABLE VALUE")
    for b in case.burdens:
        print(f"{b.name + f' × {b.improvement_rate:.0%}':<42}{money(b.recoverable(case.property_count)):>13}")
    print(f"{'Total recoverable value':<42}{money(case.recoverable_value):>13}\n")
    print("CUSTOMER ECONOMICS")
    print(f"Implementation price                 {money(c.implementation_price)}")
    print(f"Annual recurring fee                 {money(c.recurring_annual_fee)}")
    print(f"First-year cost                      {money(c.implementation_price + c.recurring_annual_fee)}")
    print(f"Retained first-year benefit          {money(c.recoverable_value-c.implementation_price-c.recurring_annual_fee)}")
    print(f"Steady-state retained benefit        {money(customer_net_annual_benefit(c))}")
    print(f"First-year ROI                       {first_year_roi(c):.1%}")
    print(f"Payback                              {payback_period_months(c):.1f} months\n")
    e = case.engineering
    print("DELIVERY")
    print(f"Shared engineering hours             {e.shared_hours}")
    print(f"Per-property hours                   {e.per_unit_hours} × {e.unit_count} = {e.incremental_hours}")
    print(f"Exception hours                      {e.exception_hours}")
    print(f"QA / deployment / rework             {e.qa_hours} / {e.deployment_hours} / {e.rework_reserve_hours}")
    print(f"Total engineering hours              {e.total_hours}")
    print(f"Direct delivery cost                 {money(implementation_delivery_cost(d))}\n")
    print(f"STANDARDIZATION\n{case.standardization.value}\n")
    print(f"REUSE\nWithin-group: {case.within_group_reuse}\nMarket: {case.market_reuse}")
    print(f"Derived core reuse                   {reuse_percentage(d):.1%}\n")
    print("SOLUTIONS ECONOMICS")
    for name, hours in vars(case.solutions_work).items(): print(f"{name.replace('_',' ').title():<39}{hours}")
    print(f"Total solutions hours                {solutions_hours(s.solutions)}")
    print(f"Contribution                         {money(solutions_contribution(c,d,s.solutions))}")
    print(f"Contribution / solutions hour        {money(effective_contribution_per_solutions_hour(c,d,s.solutions))}\n")
    print("INTEGRATION ACCESS\n" + case.integration_access_note + "\n")
    sup = case.support
    fixed = sup.fixed_hours * d.support_hourly_cost + sup.fixed_other_costs
    scaled = (sup.per_unit_hours*sup.unit_count+sup.exception_hours)*d.support_hourly_cost + sup.per_unit_other_costs*sup.unit_count
    print("SUPPORT")
    print(f"Fixed support                        {money(fixed)}")
    print(f"Property-scaled / exception support  {money(scaled)}")
    print(f"Total recurring cost                 {money(annual_support_cost(d))}")
    print(f"Recurring contribution               {money(recurring_support_contribution(c,d))}\n")
    print("BUILD VS. BUY\n" + s.build_vs_buy.note)
    print("Baseline assumes a residual integration gap; mature multi-property SaaS remains a strong constraint.\n")
    print(f"VERDICT\n-------\n{result.verdict.value}\n\nWHY")
    for reason in result.reasons: print("- " + reason)
    print("\nCASE 3 VS. CASE 4")
    three, four = case_three_comparison()
    print(f"{'Metric':<25}{'Case 3':>40}{'Case 4':>40}")
    for label, a, b in (("Properties",three.properties,four.properties),("Burden",money(three.burden),money(four.burden)),("Recoverable value",money(three.recoverable_value),money(four.recoverable_value)),("Engineering hours",three.engineering_hours,four.engineering_hours),("Implementation price",money(three.implementation_price),money(four.implementation_price)),("Solutions hours",three.solutions_hours,four.solutions_hours),("Annual support",money(three.annual_support_cost),money(four.annual_support_cost)),("Reuse",f"{three.reuse:.1%}",f"{four.reuse:.1%}"),("Payback",f"{three.payback_months:.1f} mo",f"{four.payback_months:.1f} mo"),("Verdict",three.verdict,four.verdict)):
        print(f"{label:<25}{str(a):>40}{str(b):>40}")
    print("\nSCENARIOS")
    variants=(("Baseline",baseline_case()),("Highly standardized",high_standardization_case()),("Fragmented portfolio",fragmented_portfolio_case()),("Strong SaaS alternative",strong_saas_case()),("Larger eight-property group",larger_group_case()))
    for label, candidate in variants:
        print(f"{label:<28}{analyze(candidate.scenario).verdict.value:<38} delivery {money(implementation_delivery_cost(candidate.scenario.delivery))}")
    print("\nIMPLEMENTED-CASE COMPARISON")
    one,two=case_comparison()
    rows=(("Independent restaurant",one),("Restaurant group",two),("Independent hotel",three),("Hotel group",four))
    print(f"{'Opportunity':<25}{'Value':>14}{'Delivery h':>13}{'Reuse':>10}  Verdict")
    for name,row in rows: print(f"{name:<25}{money(row.recoverable_value):>14}{row.engineering_hours:>13}{row.reuse:>10.1%}  {row.verdict}")

if __name__ == "__main__": main()
