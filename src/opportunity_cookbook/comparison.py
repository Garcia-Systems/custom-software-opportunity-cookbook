"""Deterministic, descriptive comparison of the fourteen fictional baselines.

This module deliberately has no composite score.  It adapts each case's reusable
builder to a common set of observable economics and keeps editorial synthesis
separate from the decision rules.
"""

from dataclasses import dataclass
from decimal import Decimal as D
from typing import Callable

from .analysis import OpportunityAnalysis, analyze
from .economics import (annual_support_cost, effective_contribution_per_solutions_hour,
    first_year_roi, implementation_contribution, implementation_delivery_cost,
    payback_period_months, recurring_support_contribution, reuse_percentage,
    solutions_hours)
from .models import OpportunityScenario
from .verdicts import Verdict
from . import (bad_delivery_economics, bad_sales_motion, buy_dont_build,
    construction_trades, healthcare, hotel_group, independent_hotel,
    independent_restaurant, local_government, multi_location_retail,
    professional_services, restaurant_group, tourism_attraction, university)


@dataclass(frozen=True)
class CaseDefinition:
    case_id: int
    title: str
    builder: Callable[[], object]
    archetypes: tuple[str, ...]


# The one canonical, ordered baseline registry.  Entries point to case factories
# rather than materializing mutable presentation data or copying assumptions.
BASELINE_CASES = (
    CaseDefinition(1, "Independent restaurant", independent_restaurant.baseline_case, ("single-site reporting",)),
    CaseDefinition(2, "Restaurant group", restaurant_group.baseline_case, ("multi-unit integration",)),
    CaseDefinition(3, "Independent hotel", independent_hotel.baseline_case, ("single-site reporting",)),
    CaseDefinition(4, "Hotel group", hotel_group.baseline_case, ("multi-unit integration",)),
    CaseDefinition(5, "Tourism attraction", tourism_attraction.baseline_case, ("seasonal reporting",)),
    CaseDefinition(6, "Multi-location retailer", multi_location_retail.baseline_case, ("mature SaaS category",)),
    CaseDefinition(7, "Construction / trades", construction_trades.baseline_case, ("operational handoff integration",)),
    CaseDefinition(8, "Professional services", professional_services.baseline_case, ("mature SaaS category",)),
    CaseDefinition(9, "Local government", local_government.baseline_case, ("institutional friction",)),
    CaseDefinition(10, "University department", university.baseline_case, ("institutional friction", "distributed authority")),
    CaseDefinition(11, "Healthcare organization", healthcare.baseline_case, ("high-value/high-complexity integration",)),
    CaseDefinition(12, "Perfect-looking deal", buy_dont_build.baseline_case, ("mature SaaS category",)),
    CaseDefinition(13, "Bad delivery economics", bad_delivery_economics.baseline_case, ("high-value/bespoke delivery",)),
    CaseDefinition(14, "Bad sales motion", bad_sales_motion.baseline_case, ("product-like engineering/weak acquisition",)),
)

PATTERN_CASES = {
    "single_vs_multi": ((1, 2), (3, 4)),
    "mature_saas": (6, 8, 12, 14),
    "delivery_risk": (7, 11, 13),
    "sales_failure": (14,),
    "institutional_friction": (9, 10),
}


@dataclass(frozen=True)
class ComparisonRow:
    case_id: int
    title: str
    scenario: OpportunityScenario
    analysis: OpportunityAnalysis
    current_burden: D | None
    recoverable_value: D | None
    implementation_price: D
    annual_fee: D
    retained_benefit: D | None
    payback_months: D | None
    first_year_roi: D | None
    engineering_hours: D
    delivery_cost: D
    implementation_contribution: D
    reusable_hours: D
    customer_specific_hours: D
    reuse_rate: D | None
    solutions_hours: D
    contribution_per_solutions_hour: D | None
    expected_acquisition_cost: D | None
    support_cost: D
    recurring_contribution: D
    archetypes: tuple[str, ...]

    @property
    def reason(self) -> str:
        return self.analysis.reasons[0]


def _scenario_and_analysis(case) -> tuple[OpportunityScenario, OpportunityAnalysis]:
    # Case 12's baseline is intentionally its post-alternative discovery state.
    if isinstance(case, buy_dont_build.BuyDontBuildCase):
        scenario = case.final_scenario
        return scenario, analyze(scenario)
    scenario = case.scenario
    if isinstance(case, bad_sales_motion.BadSalesMotionCase):
        return scenario, case.result
    return scenario, analyze(scenario)


def comparison_rows() -> tuple[ComparisonRow, ...]:
    rows = []
    for definition in BASELINE_CASES:
        case = definition.builder()
        scenario, result = _scenario_and_analysis(case)
        c, d, sol = scenario.customer, scenario.delivery, scenario.solutions
        engineering = sum((d.reusable_engineering_hours,
            d.customer_specific_engineering_hours, d.qa_hours, d.deployment_hours,
            d.rework_reserve_hours, d.uncertainty_reserve_hours), D("0"))
        net = None if c.recoverable_value is None else c.recoverable_value - c.recurring_annual_fee
        acquisition = case.acquisition_cost if isinstance(case, bad_sales_motion.BadSalesMotionCase) else None
        rows.append(ComparisonRow(definition.case_id, definition.title, scenario, result,
            c.current_state_annual_burden, c.recoverable_value, c.implementation_price,
            c.recurring_annual_fee, net, payback_period_months(c), first_year_roi(c),
            engineering, implementation_delivery_cost(d),
            implementation_contribution(c.implementation_price, implementation_delivery_cost(d)),
            d.reusable_engineering_hours, d.customer_specific_engineering_hours,
            reuse_percentage(d), solutions_hours(sol),
            effective_contribution_per_solutions_hour(c, d, sol), acquisition,
            annual_support_cost(d), recurring_support_contribution(c, d), definition.archetypes))
    return tuple(rows)


def group_by_verdict(rows=None) -> tuple[tuple[Verdict, tuple[ComparisonRow, ...]], ...]:
    rows = comparison_rows() if rows is None else tuple(rows)
    return tuple((verdict, tuple(row for row in rows if row.analysis.verdict is verdict))
                 for verdict in Verdict if any(r.analysis.verdict is verdict for r in rows))


def money_fields() -> tuple[str, ...]:
    """Fields whose populated values must remain Decimal (useful to consumers/tests)."""
    return ("current_burden", "recoverable_value", "implementation_price", "annual_fee",
            "retained_benefit", "delivery_cost", "implementation_contribution",
            "expected_acquisition_cost", "support_cost", "recurring_contribution")


DISCOVERY_HYPOTHESES = (
    "Multi-unit operators with common ownership and standardized systems may let value scale faster than shared delivery and selling effort.",
    "Operational handoffs with measurable duplicate entry, delay, and rework may support stronger discovery than reporting convenience alone.",
    "Narrow, authorized integrations that preserve manual exception paths may outperform broad replacement projects.",
    "Reachable buyers and repeatable sales motions may matter as much as repeatable engineering.",
)

COMMON_FAILURE_MODES = (
    "The measurable burden or recoverable share cannot support a sustainable price.",
    "A mature buy/configure alternative resolves enough of the problem at lower cost or risk.",
    "Bespoke delivery, validation, support, or acquisition effort destroys an otherwise attractive deal.",
    "The problem owner lacks budget, system, or integration authority.",
)


def _money(value): return "—" if value is None else f"${value:,.0f}"
def _number(value): return "—" if value is None else f"{value:.1f}"


def render_comparison(rows=None) -> str:
    rows = comparison_rows() if rows is None else tuple(rows)
    out = ["CUSTOM SOFTWARE OPPORTUNITY COMPARISON", "=" * 112,
           f"{'Case':<5} {'Opportunity':<27} {'Value':>11} {'Delivery':>11} {'Reuse':>8} {'Sales':>10}  Verdict",
           "-" * 112]
    for r in rows:
        sales = r.scenario.sales.procurement_difficulty.value
        out.append(f"{r.case_id:<5} {r.title:<27} {_money(r.recoverable_value):>11} {_money(r.delivery_cost):>11} {_number(None if r.reuse_rate is None else r.reuse_rate*100)+'%':>8} {sales:>10}  {r.analysis.verdict.value}")
    out += ["", "DETAILED CUSTOMER AND DELIVERY ECONOMICS", "=" * 112,
            f"{'Case':<5} {'Burden':>11} {'Recoverable':>12} {'Price':>10} {'Fee':>9} {'Cost':>10} {'Eng h':>7} {'Sol h':>7} {'Payback':>9}",
            "-" * 112]
    for r in rows:
        pb = "—" if r.payback_months is None else f"{r.payback_months:.1f} mo"
        out.append(f"{r.case_id:<5} {_money(r.current_burden):>11} {_money(r.recoverable_value):>12} {_money(r.implementation_price):>10} {_money(r.annual_fee):>9} {_money(r.delivery_cost):>10} {r.engineering_hours:>7.1f} {r.solutions_hours:>7.1f} {pb:>9}")
    out += ["", "RECURRING, SALES, AND CUSTOMER OUTCOMES", "=" * 112,
            f"{'Case':<5} {'Retained':>11} {'ROI':>8} {'Support':>10} {'Recurring':>11} {'Acquisition':>12} {'$/sol h':>10} {'Cycle':>8}", "-" * 112]
    for r in rows:
        roi = "—" if r.first_year_roi is None else f"{r.first_year_roi*100:.1f}%"
        cycle = f"{r.scenario.sales.sales_cycle_months:g} mo"
        out.append(f"{r.case_id:<5} {_money(r.retained_benefit):>11} {roi:>8} {_money(r.support_cost):>10} {_money(r.recurring_contribution):>11} {_money(r.expected_acquisition_cost):>12} {_money(r.contribution_per_solutions_hour):>10} {cycle:>8}")
    out += ["", "VERDICTS AND DOMINANT REASONS", "=" * 112]
    for verdict, grouped in group_by_verdict(rows):
        out.append(f"\n{verdict.value}")
        for r in grouped: out.append(f"- Case {r.case_id}, {r.title}: {r.reason}")
    out += ["", "DISCOVERY HYPOTHESES", "-" * 20]
    out += [f"{i}. {x}" for i, x in enumerate(DISCOVERY_HYPOTHESES, 1)]
    out += ["", "COMMON FAILURE MODES", "-" * 20]
    out += [f"- {x}" for x in COMMON_FAILURE_MODES]
    out += ["", "NEXT STEP", "-" * 9,
            "Use these results to choose real discovery targets.",
            "Replace fictional assumptions with actual customer evidence before proposing a build."]
    return "\n".join(out)
