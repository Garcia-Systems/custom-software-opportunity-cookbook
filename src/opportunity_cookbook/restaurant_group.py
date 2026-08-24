"""Fictional educational assumptions for Case 2; no industry data is used."""

from dataclasses import dataclass, replace
from decimal import Decimal as D
from enum import Enum

from .independent_restaurant import baseline_case as case_one_baseline
from .models import (
    AlternativeFinding, AlternativeType, BuildVsBuy, CustomerEconomics,
    DeliveryEconomics, Feasibility, Level, OpportunityScenario,
    SalesCharacteristics, SolutionsEconomics, TechnicalCharacteristics,
)
from .scaling import EngineeringScaling, SupportScaling


class BurdenScope(Enum):
    PER_LOCATION = "per-location"
    GROUP = "group-level"


@dataclass(frozen=True)
class GroupBurdenAssumption:
    name: str
    scope: BurdenScope
    annual_amount: D
    improvement_rate: D

    def __post_init__(self) -> None:
        if self.annual_amount < 0:
            raise ValueError("annual_amount cannot be negative")
        if not D("0") <= self.improvement_rate <= D("1"):
            raise ValueError("improvement_rate must be between 0 and 1")

    def burden(self, location_count: int) -> D:
        _validate_locations(location_count)
        multiplier = location_count if self.scope is BurdenScope.PER_LOCATION else 1
        return self.annual_amount * multiplier

    def recoverable(self, location_count: int) -> D:
        return self.burden(location_count) * self.improvement_rate


@dataclass(frozen=True)
class SolutionsWork:
    prospecting_sales_hours: D
    discovery_hours: D
    multi_location_discovery_hours: D
    solution_design_hours: D
    commercial_proposal_hours: D
    coordination_hours: D
    acceptance_hours: D

    def __post_init__(self) -> None:
        if any(value < 0 for value in vars(self).values()):
            raise ValueError("solutions hours cannot be negative")

    @property
    def total_hours(self) -> D:
        return sum(vars(self).values(), D("0"))


@dataclass(frozen=True)
class RestaurantGroupCase:
    location_count: int
    burdens: tuple[GroupBurdenAssumption, ...]
    engineering: EngineeringScaling
    support: SupportScaling
    solutions_work: SolutionsWork
    scenario: OpportunityScenario
    within_customer_reuse: str
    potential_cross_customer_reuse: str

    @property
    def location_level_burden(self) -> D:
        return sum((b.burden(self.location_count) for b in self.burdens
                    if b.scope is BurdenScope.PER_LOCATION), D("0"))

    @property
    def group_level_burden(self) -> D:
        return sum((b.burden(self.location_count) for b in self.burdens
                    if b.scope is BurdenScope.GROUP), D("0"))

    @property
    def total_burden(self) -> D:
        return self.location_level_burden + self.group_level_burden

    @property
    def recoverable_value(self) -> D:
        return sum((b.recoverable(self.location_count) for b in self.burdens), D("0"))


def _validate_locations(location_count: int) -> None:
    if not isinstance(location_count, int) or isinstance(location_count, bool) or location_count < 1:
        raise ValueError("location_count must be a positive integer")


BASELINE_BURDENS = (
    GroupBurdenAssumption("Location reconciliation labor", BurdenScope.PER_LOCATION, D("7000"), D("0.60")),
    GroupBurdenAssumption("Repeated location reporting", BurdenScope.PER_LOCATION, D("3500"), D("0.50")),
    GroupBurdenAssumption("Waste / purchasing inefficiency", BurdenScope.PER_LOCATION, D("9000"), D("0.20")),
    GroupBurdenAssumption("Labor-planning inefficiency", BurdenScope.PER_LOCATION, D("7200"), D("0.22")),
    GroupBurdenAssumption("Central management consolidation", BurdenScope.GROUP, D("26000"), D("0.65")),
    GroupBurdenAssumption("Delayed group anomaly detection", BurdenScope.GROUP, D("14000"), D("0.25")),
)

BASELINE_ENGINEERING = EngineeringScaling(
    shared_hours=D("100"), per_unit_hours=D("10"), unit_count=5,
    exception_hours=D("30"), qa_hours=D("24"), deployment_hours=D("10"),
    rework_reserve_hours=D("20"),
)

BASELINE_SUPPORT = SupportScaling(
    fixed_hours=D("18"), per_unit_hours=D("8"), unit_count=5,
    exception_hours=D("10"), fixed_other_costs=D("1300"),
    per_unit_other_costs=D("100"),
)

BASELINE_SOLUTIONS = SolutionsWork(
    D("7"), D("8"), D("7"), D("10"), D("5"), D("9"), D("6"),
)


def _build(location_count: int = 5, *, per_unit_engineering: D = D("10"),
           exception_engineering: D = D("30"),
           finding: AlternativeFinding = AlternativeFinding.CUSTOM_JUSTIFIED,
           implementation_price: D = D("42000"),
           recurring_fee: D = D("9000")) -> RestaurantGroupCase:
    _validate_locations(location_count)
    # Consolidation grows with relationships among locations, but not as a simple
    # per-location multiple. This editable case assumption is deliberately explicit.
    group_growth = D(max(location_count - 5, 0)) * D("3500")
    burdens = tuple(
        replace(b, annual_amount=b.annual_amount + group_growth)
        if b.name == "Central management consolidation" else b
        for b in BASELINE_BURDENS
    )
    engineering = replace(BASELINE_ENGINEERING, unit_count=location_count,
                          per_unit_hours=per_unit_engineering,
                          exception_hours=exception_engineering)
    support = replace(BASELINE_SUPPORT, unit_count=location_count)
    total = sum((b.burden(location_count) for b in burdens), D("0"))
    recoverable = sum((b.recoverable(location_count) for b in burdens), D("0"))
    delivery = DeliveryEconomics(
        reusable_engineering_hours=engineering.shared_hours,
        customer_specific_engineering_hours=(engineering.incremental_hours
                                             + engineering.exception_hours),
        engineering_hourly_cost=D("75"), qa_hours=engineering.qa_hours,
        deployment_hours=engineering.deployment_hours,
        rework_reserve_hours=engineering.rework_reserve_hours,
        other_direct_costs=D("1450"), annual_support_hours=support.total_hours,
        support_hourly_cost=D("75"),
        annual_support_other_direct_costs=support.total_other_costs,
    )
    sw = BASELINE_SOLUTIONS
    solutions = SolutionsEconomics(
        sw.prospecting_sales_hours,
        sw.discovery_hours + sw.multi_location_discovery_hours,
        sw.solution_design_hours + sw.commercial_proposal_hours,
        sw.coordination_hours + sw.acceptance_hours, D("65"),
    )
    scenario = OpportunityScenario(
        "James River Hospitality Group", True,
        CustomerEconomics(total, recoverable, implementation_price, recurring_fee), delivery,
        solutions, SalesCharacteristics(Level.MODERATE, D("3"), Level.HIGH, Level.MODERATE),
        TechnicalCharacteristics(5, Level.MODERATE, Level.MODERATE, Feasibility.FEASIBLE,
                                 Level.LOW, Level.LOW, Level.MODERATE),
        BuildVsBuy(finding, tuple(AlternativeType),
                   "Multi-location SaaS, vendor-native reporting, configuration, automation, manual work, and custom integration were modeled; baseline assumes discovery found a remaining cross-system gap."),
    )
    return RestaurantGroupCase(
        location_count, burdens, engineering, support, sw, scenario,
        "High within this engagement: shared ingestion, normalization, validation, and reporting serve five locations.",
        "Unproven: another customer may use different vendors, mappings, identifiers, and business rules.",
    )


def baseline_case() -> RestaurantGroupCase:
    return _build()


def high_standardization_case() -> RestaurantGroupCase:
    return _build(per_unit_engineering=D("5"), exception_engineering=D("12"))


def low_standardization_case() -> RestaurantGroupCase:
    return _build(per_unit_engineering=D("20"), exception_engineering=D("90"))


def saas_alternative_case() -> RestaurantGroupCase:
    return _build(finding=AlternativeFinding.ADEQUATE_BUY)


def ten_location_case() -> RestaurantGroupCase:
    return _build(location_count=10, per_unit_engineering=D("8"), exception_engineering=D("45"),
                  implementation_price=D("55000"), recurring_fee=D("15000"))


@dataclass(frozen=True)
class CaseComparisonRow:
    locations: int
    burden: D
    recoverable_value: D
    engineering_hours: D
    implementation_price: D
    solutions_hours: D
    annual_support_cost: D
    reuse: D | None
    payback_months: D | None
    verdict: str


def case_comparison() -> tuple[CaseComparisonRow, CaseComparisonRow]:
    """Calculate, rather than copy, the immutable Case 1 and Case 2 baselines."""
    from .analysis import analyze
    from .economics import annual_support_cost, payback_period_months, reuse_percentage, solutions_hours

    one = case_one_baseline()
    group = baseline_case()

    def row(locations: int, case) -> CaseComparisonRow:
        scenario = case.scenario
        delivery = scenario.delivery
        engineering_hours = (delivery.reusable_engineering_hours
                             + delivery.customer_specific_engineering_hours
                             + delivery.qa_hours + delivery.deployment_hours
                             + delivery.rework_reserve_hours)
        return CaseComparisonRow(
            locations, case.total_burden, case.recoverable_value, engineering_hours,
            scenario.customer.implementation_price, solutions_hours(scenario.solutions),
            annual_support_cost(delivery), reuse_percentage(delivery),
            payback_period_months(scenario.customer), analyze(scenario).verdict.value,
        )

    return row(1, one), row(5, group)
