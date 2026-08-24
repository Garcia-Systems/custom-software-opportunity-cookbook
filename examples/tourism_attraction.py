"""Run Case 5. Every value and context input is a fictional educational assumption."""
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
from opportunity_cookbook.tourism_attraction import (baseline_case,
    fragmented_integrations_case, high_reconciliation_burden_case,
    high_seasonality_low_burden_case, implemented_case_comparison,
    standardized_integrations_case, strong_vertical_saas_case,
    uncertain_revenue_upside_case)


def money(v: Decimal) -> str: return f"${v:,.2f}"


def main() -> None:
    case = baseline_case(); s = case.scenario; c = s.customer; d = s.delivery
    result = analyze(s)
    print("CASE 5 — THE TOURISM / ATTRACTION OPERATOR\n===========================================")
    print("Fictional educational scenario (not local or tourism-industry data/benchmarks):")
    print("James River Adventure Park — one regional attraction with timed and walk-up admission\n")
    print("BUSINESS\nSeasonal, open much of the year; memberships, concessions/retail, scheduled staff,")
    print("multiple activity areas, and guest feedback accompany admissions.\n")
    print("SEASONAL OPERATING PROFILE")
    print(f"Peak / non-peak weeks                {case.season.peak_weeks} / {case.season.non_peak_weeks}")
    print(f"Total operating weeks                {case.season.operating_weeks}\n")
    print("CURRENT SYSTEMS\nTicketing / attendance | Membership | Staffing | Concessions / retail POS")
    print("Guest feedback | fictional weather/event context | spreadsheets / exports")
    print("These functioning systems feed manual analysis; none is proposed for replacement.\n")
    print("CURRENT-STATE BURDEN")
    for b in case.burdens:
        formula = f"{b.peak_weekly_units}×{case.season.peak_weeks} + {b.non_peak_weekly_units}×{case.season.non_peak_weeks}; {b.basis}"
        print(f"{b.name:<31}{money(b.annual_burden(case.season)):>12}  ({formula})")
    print(f"{'Total annual burden':<31}{money(case.total_burden):>12}\n")
    print("RECOVERABLE VALUE")
    for b in case.burdens:
        print(f"{b.name + f' × {b.improvement_rate:.0%}':<39}{money(b.recoverable(case.season)):>12}")
    print(f"{'Total recoverable value':<39}{money(case.recoverable_value):>12}")
    print("No attendance revenue benefit is included in the baseline.\n")
    print("CUSTOMER ECONOMICS")
    print(f"Implementation price                 {money(c.implementation_price)}")
    print(f"Annual recurring fee                 {money(c.recurring_annual_fee)}")
    print(f"First-year cost                      {money(c.implementation_price+c.recurring_annual_fee)}")
    print(f"Retained first-year benefit          {money(c.recoverable_value-c.implementation_price-c.recurring_annual_fee)}")
    print(f"Steady-state retained benefit        {money(customer_net_annual_benefit(c))}")
    print(f"First-year ROI                       {first_year_roi(c):.1%}")
    print(f"Payback                              {payback_period_months(c):.1f} months\n")
    total_hours = sum((d.reusable_engineering_hours, d.customer_specific_engineering_hours,
        d.qa_hours, d.deployment_hours, d.rework_reserve_hours), Decimal("0"))
    print("DELIVERY")
    print(f"Engineering hours                    {total_hours}")
    print(f"Reusable / attraction-specific       {d.reusable_engineering_hours} / {d.customer_specific_engineering_hours}")
    print(f"Testing / deployment / rework        {d.qa_hours} / {d.deployment_hours} / {d.rework_reserve_hours}")
    print(f"Derived core reuse                   {reuse_percentage(d):.1%}")
    print(f"Direct delivery cost                 {money(implementation_delivery_cost(d))}\n")
    print("SOLUTION\nScheduled imports, adapter validation/logging, normalized date/activity records,")
    print("deterministic daily metrics, and a management briefing—not forecasting or an operations suite.\n")
    print("CONTEXT INPUTS")
    for k,v in vars(case.context).items(): print(f"{k:<35}{v}")
    print("Context annotates evidence; it does not create an opaque prediction score.\n")
    print("SOLUTIONS ECONOMICS")
    for name,hours in vars(case.solutions_work).items(): print(f"{name.replace('_',' ').title():<39}{hours}")
    print(f"Total solutions hours                {solutions_hours(s.solutions)}")
    print(f"Contribution                         {money(solutions_contribution(c,d,s.solutions))}")
    print(f"Contribution / solutions hour        {money(effective_contribution_per_solutions_hour(c,d,s.solutions))}\n")
    print("BUILD VS. BUY\n" + s.build_vs_buy.note)
    print("The baseline assumes a residual gap, but accessible vertical SaaS can override custom economics.\n")
    print("SUPPORT")
    print("Hosting, monitoring, source/export changes, context maintenance, data quality,")
    print("bugs, support, and periodic mapping changes are modeled as recurring direct cost.")
    print(f"Recurring revenue                    {money(c.recurring_annual_fee)}")
    print(f"Recurring direct cost                {money(annual_support_cost(d))}")
    print(f"Recurring contribution               {money(recurring_support_contribution(c,d))}\n")
    print(f"VERDICT\n-------\n{result.verdict.value}\n\nWHY")
    for reason in result.reasons: print("- " + reason)
    print("\nSCENARIOS")
    variants = (("Baseline", baseline_case()),
        ("High seasonality / low burden", high_seasonality_low_burden_case()),
        ("High reconciliation burden", high_reconciliation_burden_case()),
        ("Standardized integrations", standardized_integrations_case()),
        ("Fragmented integrations", fragmented_integrations_case()),
        ("Strong vertical SaaS", strong_vertical_saas_case()),
        ("Uncertain revenue upside", uncertain_revenue_upside_case()))
    for label, candidate in variants:
        print(f"{label:<31}{analyze(candidate.scenario).verdict.value:<38} value {money(candidate.recoverable_value):>11}  delivery {money(implementation_delivery_cost(candidate.scenario.delivery))}")
    print("\nIMPLEMENTED-CASE COMPARISON")
    print(f"{'Opportunity':<25}{'Value':>14}{'Delivery h':>13}{'Reuse':>10}  Verdict")
    for row in implemented_case_comparison():
        print(f"{row.name:<25}{money(row.recoverable_value):>14}{row.engineering_hours:>13}{row.reuse:>10.1%}  {row.verdict}")
    print("\nComplexity is not value. The attraction is attractive only if measured burden,")
    print("credible recovery, manageable delivery, and a real SaaS gap coexist.")


if __name__ == "__main__": main()
