"""Case 5: fictional tourism-attraction opportunity assumptions, not benchmarks."""

from dataclasses import dataclass, replace
from decimal import Decimal as D

from .models import (AlternativeFinding, AlternativeType, BuildVsBuy,
                     CustomerEconomics, DeliveryEconomics, Feasibility, Level,
                     OpportunityScenario, SalesCharacteristics,
                     SolutionsEconomics, TechnicalCharacteristics)


@dataclass(frozen=True)
class SeasonalProfile:
    peak_weeks: D
    non_peak_weeks: D

    def __post_init__(self) -> None:
        if self.peak_weeks < 0 or self.non_peak_weeks < 0:
            raise ValueError("seasonal weeks cannot be negative")

    @property
    def operating_weeks(self) -> D:
        return self.peak_weeks + self.non_peak_weeks


@dataclass(frozen=True)
class SeasonalBurden:
    name: str
    peak_weekly_units: D
    non_peak_weekly_units: D
    cost_per_unit: D
    improvement_rate: D
    basis: str

    def __post_init__(self) -> None:
        if any(v < 0 for v in (self.peak_weekly_units, self.non_peak_weekly_units,
                               self.cost_per_unit)):
            raise ValueError("burden values cannot be negative")
        if not D("0") <= self.improvement_rate <= D("1"):
            raise ValueError("improvement_rate must be between 0 and 1")

    def annual_burden(self, season: SeasonalProfile) -> D:
        return ((self.peak_weekly_units * season.peak_weeks
                 + self.non_peak_weekly_units * season.non_peak_weeks)
                * self.cost_per_unit)

    def recoverable(self, season: SeasonalProfile) -> D:
        return self.annual_burden(season) * self.improvement_rate


@dataclass(frozen=True)
class AttractionSolutionsWork:
    prospecting: D
    discovery: D
    workflow_interviews: D
    solution_design: D
    integration_validation: D
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
class ContextInputs:
    weather_condition: str
    holiday_flag: bool
    local_event_flag: bool
    school_break_flag: bool


@dataclass(frozen=True)
class AttractionCase:
    season: SeasonalProfile
    burdens: tuple[SeasonalBurden, ...]
    solutions_work: AttractionSolutionsWork
    context: ContextInputs
    scenario: OpportunityScenario
    uncertain_revenue_upside: D = D("0")

    @property
    def total_burden(self) -> D:
        return sum((b.annual_burden(self.season) for b in self.burdens), D("0"))

    @property
    def burden_recovery(self) -> D:
        return sum((b.recoverable(self.season) for b in self.burdens), D("0"))

    @property
    def recoverable_value(self) -> D:
        return self.burden_recovery + self.uncertain_revenue_upside


BASELINE_SEASON = SeasonalProfile(D("18"), D("26"))
BASELINE_BURDENS = (
    SeasonalBurden("Management reconciliation", D("10"), D("5"), D("48"), D(".55"), "management labor hours"),
    SeasonalBurden("Attendance-context analysis", D("4"), D("2"), D("50"), D(".30"), "management labor hours"),
    SeasonalBurden("Staffing coordination", D("5"), D("2"), D("44"), D(".30"), "operations labor hours"),
    SeasonalBurden("Concession / preparation", D("180"), D("70"), D("1"), D(".25"), "fictional avoidable dollars; excludes revenue"),
    SeasonalBurden("Membership reporting", D("2"), D("1"), D("38"), D(".45"), "administration labor hours"),
    SeasonalBurden("Post-event analysis", D("3"), D("1"), D("48"), D(".40"), "management labor hours"),
    SeasonalBurden("Operating preparation", D("200"), D("80"), D("1"), D(".20"), "fictional avoidable dollars; distinct from concessions"),
)
BASELINE_SOLUTIONS = AttractionSolutionsWork(D("6"), D("6"), D("8"), D("7"), D("8"), D("5"), D("6"), D("4"))


def _build(*, season: SeasonalProfile = BASELINE_SEASON,
           burdens: tuple[SeasonalBurden, ...] = BASELINE_BURDENS,
           reusable_hours: D = D("100"), specific_hours: D = D("120"),
           qa_hours: D = D("30"), deployment_hours: D = D("12"),
           rework_hours: D = D("25"), other_direct: D = D("1500"),
           support_hours: D = D("58"), support_other: D = D("1800"),
           price: D = D("27000"), fee: D = D("7200"),
           finding: AlternativeFinding = AlternativeFinding.CUSTOM_JUSTIFIED,
           integration_complexity: Level = Level.MODERATE,
           data_availability: Level = Level.MODERATE,
           permission: Level = Level.MODERATE,
           uncertain_upside: D = D("0")) -> AttractionCase:
    if uncertain_upside < 0:
        raise ValueError("uncertain_upside cannot be negative")
    total = sum((b.annual_burden(season) for b in burdens), D("0"))
    recovered = sum((b.recoverable(season) for b in burdens), D("0")) + uncertain_upside
    delivery = DeliveryEconomics(reusable_hours, specific_hours, D("75"), qa_hours,
        deployment_hours, rework_hours, other_direct, support_hours, D("75"), support_other)
    w = BASELINE_SOLUTIONS
    solutions = SolutionsEconomics(w.prospecting, w.discovery + w.workflow_interviews,
        w.solution_design + w.integration_validation + w.proposal_scoping,
        w.coordination + w.acceptance, D("65"))
    scenario = OpportunityScenario(
        "James River Adventure Park", True,
        CustomerEconomics(total, recovered, price, fee), delivery, solutions,
        SalesCharacteristics(Level.MODERATE, D("5"), Level.HIGH, Level.MODERATE),
        TechnicalCharacteristics(7, integration_complexity, data_availability,
            Feasibility.FEASIBLE, Level.LOW, Level.LOW, permission),
        BuildVsBuy(finding, tuple(AlternativeType),
            "Ticketing and POS reports, attraction/venue SaaS, BI/configuration, low-code automation, improved spreadsheets/process, narrow custom integration, and doing nothing were evaluated."))
    return AttractionCase(season, burdens, w,
        ContextInputs("fictional mixed conditions", False, True, False),
        scenario, uncertain_upside)


def baseline_case() -> AttractionCase:
    return _build()


def high_seasonality_low_burden_case() -> AttractionCase:
    season = SeasonalProfile(D("12"), D("10"))
    burdens = tuple(replace(b, non_peak_weekly_units=b.non_peak_weekly_units * D(".5"))
                    for b in BASELINE_BURDENS)
    return _build(season=season, burdens=burdens)


def high_reconciliation_burden_case() -> AttractionCase:
    burdens = tuple(replace(b, peak_weekly_units=D("32"), non_peak_weekly_units=D("18"))
                    if b.name == "Management reconciliation" else b
                    for b in BASELINE_BURDENS)
    return _build(burdens=burdens)


def standardized_integrations_case() -> AttractionCase:
    return _build(reusable_hours=D("92"), specific_hours=D("70"), qa_hours=D("20"),
        rework_hours=D("10"), support_hours=D("38"), support_other=D("1200"),
        integration_complexity=Level.LOW, data_availability=Level.HIGH,
        permission=Level.LOW)


def fragmented_integrations_case() -> AttractionCase:
    return _build(reusable_hours=D("105"), specific_hours=D("220"), qa_hours=D("48"),
        deployment_hours=D("16"), rework_hours=D("55"), other_direct=D("2600"),
        support_hours=D("95"), support_other=D("3000"),
        integration_complexity=Level.HIGH, data_availability=Level.LOW,
        permission=Level.HIGH)


def strong_vertical_saas_case() -> AttractionCase:
    return _build(finding=AlternativeFinding.ADEQUATE_BUY)


def uncertain_revenue_upside_case() -> AttractionCase:
    # Deliberately absent from baseline: a fictional $8,000 hypothesis, not a forecast.
    return _build(uncertain_upside=D("8000"))


@dataclass(frozen=True)
class ImplementedCaseRow:
    name: str
    recoverable_value: D
    engineering_hours: D
    reuse: D | None
    verdict: str
    delivery_difficulty: str
    sales_procurement_difficulty: str


def implemented_case_comparison() -> tuple[ImplementedCaseRow, ...]:
    """Calculated comparison for implemented Cases 1–13; no composite score."""
    from .analysis import analyze
    from .economics import reuse_percentage
    from .hotel_group import baseline_case as hotel_group
    from .independent_hotel import baseline_case as hotel
    from .independent_restaurant import baseline_case as restaurant_case
    from .multi_location_retail import baseline_case as retail
    from .restaurant_group import baseline_case as restaurant_group
    from .construction_trades import baseline_case as construction
    from .professional_services import baseline_case as professional_services
    from .local_government import baseline_case as local_government
    from .university import baseline_case as university
    from .healthcare import baseline_case as healthcare
    from .buy_dont_build import baseline_case as buy_dont_build
    from .bad_delivery_economics import baseline_case as bad_delivery

    sources = (("Independent restaurant", restaurant_case().scenario),
               ("Restaurant group", restaurant_group().scenario),
               ("Independent hotel", hotel().scenario),
               ("Hotel group", hotel_group().scenario),
               ("Tourism attraction", baseline_case().scenario),
               ("Multi-location retailer", retail().scenario),
               ("Construction / trades", construction().scenario),
               ("Professional services", professional_services().scenario),
               ("Local government", local_government().scenario),
               ("University department", university().scenario),
               ("Healthcare organization", healthcare().scenario),
               ("Perfect-looking deal", buy_dont_build().final_scenario),
               ("Bad delivery economics", bad_delivery().scenario))
    rows = []
    for name, scenario in sources:
        d = scenario.delivery
        hours = sum((d.reusable_engineering_hours, d.customer_specific_engineering_hours,
                     d.qa_hours, d.deployment_hours, d.rework_reserve_hours,
                     d.uncertainty_reserve_hours), D("0"))
        rows.append(ImplementedCaseRow(name, scenario.customer.recoverable_value,
            hours, reuse_percentage(d), analyze(scenario).verdict.value,
            scenario.technical.integration_complexity.value,
            scenario.sales.procurement_difficulty.value))
    return tuple(rows)
