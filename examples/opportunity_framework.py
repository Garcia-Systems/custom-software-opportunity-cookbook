"""Chapter 0 demonstration. Every scenario value is a fictional educational assumption."""

from decimal import Decimal
from pathlib import Path
import sys

# Keep the documented checkout command runnable before an editable install.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import *
from opportunity_cookbook.models import *


scenario = OpportunityScenario(
    business_name="Fictional NeatPath Home Services",
    meaningful_problem=True,
    customer=CustomerEconomics(Decimal("30000"), Decimal("21000"), Decimal("9000"), Decimal("2400")),
    delivery=DeliveryEconomics(Decimal("45"), Decimal("35"), Decimal("65"),
                               qa_hours=Decimal("8"), deployment_hours=Decimal("4"),
                               rework_reserve_hours=Decimal("8"), other_direct_costs=Decimal("300"),
                               annual_support_hours=Decimal("20"), support_hourly_cost=Decimal("65")),
    solutions=SolutionsEconomics(Decimal("6"), Decimal("8"), Decimal("6"), Decimal("5"), Decimal("60")),
    sales=SalesCharacteristics(Level.MODERATE, Decimal("2"), Level.HIGH, Level.LOW),
    technical=TechnicalCharacteristics(2, Level.MODERATE, Level.HIGH, Feasibility.FEASIBLE,
                                       Level.LOW, Level.LOW, Level.MODERATE),
    build_vs_buy=BuildVsBuy(AlternativeFinding.CUSTOM_JUSTIFIED,
                            (AlternativeType.EXISTING_SAAS, AlternativeType.AUTOMATION_TOOLING,
                             AlternativeType.CUSTOM_INTEGRATION),
                            "Fictional review: SaaS cannot join both systems."),
)


def money(value: Decimal) -> str:
    return f"${value:,.2f}"


def main() -> None:
    c, d, s = scenario.customer, scenario.delivery, scenario.solutions
    result = analyze(scenario)
    print("CUSTOM SOFTWARE OPPORTUNITY ANALYSIS\n====================================")
    print("All amounts and operational values below are FICTIONAL EDUCATIONAL ASSUMPTIONS.\n")
    print(f"Business: {scenario.business_name}\n\nCUSTOMER ECONOMICS")
    print(f"Current-state annual burden:  {money(c.current_state_annual_burden)}")
    print(f"Recoverable annual value:     {money(c.recoverable_value)}")
    print(f"Implementation price:         {money(c.implementation_price)}")
    print(f"Annual recurring fee:         {money(c.recurring_annual_fee)}")
    print(f"Customer retained benefit:    {money(customer_net_annual_benefit(c))}")
    print(f"First-year ROI:                {first_year_roi(c):.1%}")
    print(f"Payback:                       {payback_period_months(c):.1f} months")
    print("\nDELIVERY ECONOMICS")
    print(f"Engineering/QA/deploy hours:   {d.reusable_engineering_hours + d.customer_specific_engineering_hours + d.qa_hours + d.deployment_hours + d.rework_reserve_hours}")
    print(f"Direct implementation cost:   {money(implementation_delivery_cost(d))}")
    print(f"Annual support cost:           {money(annual_support_cost(d))}")
    print("\nSOLUTIONS ECONOMICS")
    print(f"Solutions hours:               {solutions_hours(s)}")
    print(f"Implementation contribution:  {money(solutions_contribution(c, d, s))}")
    print(f"Contribution / solutions hour:{money(effective_contribution_per_solutions_hour(c, d, s))}")
    print("\nTECHNICAL / MARKET")
    print(f"Technical feasibility:         {scenario.technical.feasibility.value}")
    print(f"Build-vs-buy:                  {scenario.build_vs_buy.finding.value}")
    print(f"Sales friction:                {scenario.sales.close_friction.value}")
    print(f"Core engineering reuse:        {reuse_percentage(d):.0%}")
    print(f"\nVERDICT\n-------\n{result.verdict.value}\n\nWHY")
    for reason in result.reasons:
        print(f"- {reason}")


if __name__ == "__main__":
    main()
