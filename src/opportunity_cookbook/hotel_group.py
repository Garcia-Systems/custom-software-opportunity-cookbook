"""Case 4: fictional hotel-group opportunity assumptions, not benchmarks."""

from dataclasses import dataclass, replace
from decimal import Decimal as D
from enum import Enum

from .models import (AlternativeFinding, AlternativeType, BuildVsBuy,
                     CustomerEconomics, DeliveryEconomics, Feasibility, Level,
                     OpportunityScenario, SalesCharacteristics,
                     SolutionsEconomics, TechnicalCharacteristics)
from .scaling import EngineeringScaling, SupportScaling


class BurdenScope(Enum):
    PROPERTY = "property-level"
    CENTRAL = "central group"


class Standardization(Enum):
    HIGH = "high — common systems, exports, definitions, and processes"
    MODERATE = "moderate — common patterns with property-specific mappings"
    LOW = "low — fragmented systems, identifiers, and workflows"


@dataclass(frozen=True)
class GroupHotelBurden:
    name: str
    scope: BurdenScope
    hours_per_week: D
    loaded_hourly_cost: D
    operating_weeks: D
    improvement_rate: D

    def __post_init__(self) -> None:
        if any(v < 0 for v in (self.hours_per_week, self.loaded_hourly_cost,
                               self.operating_weeks)):
            raise ValueError("burden values cannot be negative")
        if not D("0") <= self.improvement_rate <= D("1"):
            raise ValueError("improvement_rate must be between 0 and 1")

    def annual_burden(self, property_count: int) -> D:
        _properties(property_count)
        multiplier = property_count if self.scope is BurdenScope.PROPERTY else 1
        return self.hours_per_week * self.loaded_hourly_cost * self.operating_weeks * multiplier

    def recoverable(self, property_count: int) -> D:
        return self.annual_burden(property_count) * self.improvement_rate


@dataclass(frozen=True)
class HotelGroupSolutionsWork:
    prospecting_sales: D
    discovery: D
    central_interviews: D
    selected_property_discovery: D
    solution_design: D
    technical_validation: D
    proposal_scoping: D
    coordination: D
    acceptance: D

    def __post_init__(self) -> None:
        if any(v < 0 for v in vars(self).values()):
            raise ValueError("solutions hours cannot be negative")

    @property
    def total_hours(self) -> D:
        return sum(vars(self).values(), D("0"))


@dataclass(frozen=True)
class HotelGroupCase:
    property_count: int
    room_count: int
    burdens: tuple[GroupHotelBurden, ...]
    engineering: EngineeringScaling
    support: SupportScaling
    solutions_work: HotelGroupSolutionsWork
    standardization: Standardization
    scenario: OpportunityScenario
    integration_access_note: str
    within_group_reuse: str
    market_reuse: str

    @property
    def property_level_burden(self) -> D:
        return sum((b.annual_burden(self.property_count) for b in self.burdens
                    if b.scope is BurdenScope.PROPERTY), D("0"))

    @property
    def central_burden(self) -> D:
        return sum((b.annual_burden(self.property_count) for b in self.burdens
                    if b.scope is BurdenScope.CENTRAL), D("0"))

    @property
    def total_burden(self) -> D:
        return self.property_level_burden + self.central_burden

    @property
    def recoverable_value(self) -> D:
        return sum((b.recoverable(self.property_count) for b in self.burdens), D("0"))


def _properties(count: int) -> None:
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise ValueError("property_count must be a positive integer")


BASELINE_BURDENS = (
    GroupHotelBurden("Property reconciliation", BurdenScope.PROPERTY, D("5"), D("45"), D("52"), D("0.55")),
    GroupHotelBurden("Housekeeping comparison", BurdenScope.PROPERTY, D("4"), D("32"), D("52"), D("0.30")),
    GroupHotelBurden("Staffing visibility", BurdenScope.PROPERTY, D("2.5"), D("44"), D("52"), D("0.25")),
    GroupHotelBurden("Booking-channel analysis", BurdenScope.PROPERTY, D("2.5"), D("46"), D("52"), D("0.35")),
    GroupHotelBurden("Central consolidation", BurdenScope.CENTRAL, D("12"), D("58"), D("52"), D("0.65")),
    GroupHotelBurden("Central management reporting", BurdenScope.CENTRAL, D("7"), D("52"), D("52"), D("0.55")),
    GroupHotelBurden("Data / KPI normalization", BurdenScope.CENTRAL, D("6"), D("48"), D("52"), D("0.60")),
    GroupHotelBurden("Delayed anomaly investigation", BurdenScope.CENTRAL, D("4"), D("60"), D("52"), D("0.30")),
)

BASELINE_ENGINEERING = EngineeringScaling(D("130"), D("18"), 4, D("38"), D("32"), D("14"), D("28"))
BASELINE_SUPPORT = SupportScaling(D("24"), D("9"), 4, D("12"), D("2200"), D("300"))
BASELINE_SOLUTIONS = HotelGroupSolutionsWork(D("8"), D("8"), D("8"), D("12"), D("10"), D("10"), D("6"), D("8"), D("6"))


def _build(property_count: int = 4, *, standardization=Standardization.MODERATE,
           per_property_hours: D = D("18"), exception_hours: D = D("38"),
           qa_hours: D = D("32"), deployment_hours: D = D("14"),
           rework_hours: D = D("28"), support_per_property: D = D("9"),
           support_exception: D = D("12"), other_direct: D = D("2200"),
           support_fixed_cost: D = D("2200"), support_property_cost: D = D("300"),
           price: D = D("48000"), fee: D = D("15000"),
           finding=AlternativeFinding.CUSTOM_JUSTIFIED,
           permission=Level.MODERATE, integration_count: int = 9,
           access_note: str = "Two common PMS/export patterns are assumed; group credentials and scheduled exports are plausible, while API rights, vendor fees, versions, rate limits, and approvals require validation.") -> HotelGroupCase:
    _properties(property_count)
    # Central coordination is shared, but larger groups add some relationship complexity.
    growth = D(max(property_count - 4, 0)) * D("1.5")
    burdens = tuple(replace(b, hours_per_week=b.hours_per_week + growth)
                    if b.name == "Central consolidation" else b for b in BASELINE_BURDENS)
    eng = EngineeringScaling(D("130"), per_property_hours, property_count,
                             exception_hours, qa_hours, deployment_hours, rework_hours)
    support = SupportScaling(D("24"), support_per_property, property_count,
                             support_exception, support_fixed_cost, support_property_cost)
    total = sum((b.annual_burden(property_count) for b in burdens), D("0"))
    recoverable = sum((b.recoverable(property_count) for b in burdens), D("0"))
    delivery = DeliveryEconomics(
        eng.shared_hours, eng.incremental_hours + eng.exception_hours, D("75"),
        eng.qa_hours, eng.deployment_hours, eng.rework_reserve_hours, other_direct,
        support.total_hours, D("75"), support.total_other_costs)
    w = BASELINE_SOLUTIONS
    solutions = SolutionsEconomics(w.prospecting_sales,
        w.discovery + w.central_interviews + w.selected_property_discovery,
        w.solution_design + w.technical_validation + w.proposal_scoping,
        w.coordination + w.acceptance, D("65"))
    scenario = OpportunityScenario(
        "James River Lodging Group", True,
        CustomerEconomics(total, recoverable, price, fee), delivery, solutions,
        SalesCharacteristics(Level.MODERATE, D("5"), Level.HIGH, Level.MODERATE),
        TechnicalCharacteristics(integration_count, Level.MODERATE, Level.MODERATE,
            Feasibility.FEASIBLE, Level.MODERATE, Level.LOW, permission),
        BuildVsBuy(finding, tuple(AlternativeType),
            "PMS-native group reporting, hotel analytics SaaS, central BI/configuration, channel reporting, low-code, process/spreadsheets, custom integration, and doing nothing were evaluated."))
    return HotelGroupCase(property_count, property_count * 132, burdens, eng,
        support, w, standardization, scenario, access_note,
        "Strong inside this deal: one framework and operating model serve all properties.",
        "Unvalidated across customers: PMSs, permissions, mappings, channels, and rules may differ.")


def baseline_case() -> HotelGroupCase:
    return _build()


def high_standardization_case() -> HotelGroupCase:
    return _build(standardization=Standardization.HIGH, per_property_hours=D("10"),
        exception_hours=D("10"), qa_hours=D("24"), rework_hours=D("14"),
        support_per_property=D("5"), support_exception=D("4"), permission=Level.LOW,
        integration_count=6,
        access_note="One PMS/version, similar exports, shared definitions, group credentials, and consistent processes are assumed.")


def fragmented_portfolio_case() -> HotelGroupCase:
    return _build(standardization=Standardization.LOW, per_property_hours=D("30"),
        exception_hours=D("180"), qa_hours=D("45"), deployment_hours=D("18"),
        rework_hours=D("50"), support_per_property=D("16"),
        support_exception=D("30"), other_direct=D("3000"),
        support_property_cost=D("650"), permission=Level.HIGH,
        integration_count=15,
        access_note="Multiple PMS versions, export-only sources, inherited identifiers, vendor approvals, credentials, and unusual workflows are assumed.")


def strong_saas_case() -> HotelGroupCase:
    return _build(finding=AlternativeFinding.ADEQUATE_BUY)


def larger_group_case() -> HotelGroupCase:
    return _build(8, per_property_hours=D("14"), exception_hours=D("55"),
                  support_per_property=D("7"), price=D("70000"), fee=D("22000"))


@dataclass(frozen=True)
class HotelComparisonRow:
    properties: int
    burden: D
    recoverable_value: D
    engineering_hours: D
    implementation_price: D
    solutions_hours: D
    annual_support_cost: D
    reuse: D | None
    payback_months: D | None
    verdict: str


def case_three_comparison() -> tuple[HotelComparisonRow, HotelComparisonRow]:
    from .analysis import analyze
    from .economics import annual_support_cost, payback_period_months, reuse_percentage, solutions_hours
    from .independent_hotel import baseline_case as case_three

    def row(properties: int, case) -> HotelComparisonRow:
        s, d = case.scenario, case.scenario.delivery
        hours = sum((d.reusable_engineering_hours, d.customer_specific_engineering_hours,
                     d.qa_hours, d.deployment_hours, d.rework_reserve_hours), D("0"))
        return HotelComparisonRow(properties, case.total_burden, case.recoverable_value,
            hours, s.customer.implementation_price, solutions_hours(s.solutions),
            annual_support_cost(d), reuse_percentage(d), payback_period_months(s.customer),
            analyze(s).verdict.value)
    return row(1, case_three()), row(4, baseline_case())
