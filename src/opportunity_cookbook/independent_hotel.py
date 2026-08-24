"""Case 3: fictional educational hotel assumptions, never industry benchmarks."""

from dataclasses import dataclass, replace
from decimal import Decimal as D

from .models import (AlternativeFinding, AlternativeType, BuildVsBuy,
                     CustomerEconomics, DeliveryEconomics, Feasibility, Level,
                     OpportunityScenario, SalesCharacteristics,
                     SolutionsEconomics, TechnicalCharacteristics)


@dataclass(frozen=True)
class HotelBurden:
    """One non-overlapping, measurable burden and its credible improvement."""

    name: str
    hours_per_week: D
    loaded_hourly_cost: D
    operating_weeks: D
    improvement_rate: D
    annual_nonlabor_loss: D = D("0")

    def __post_init__(self) -> None:
        if not D("0") <= self.improvement_rate <= D("1"):
            raise ValueError("improvement_rate must be between 0 and 1")
        if any(value < 0 for value in (self.hours_per_week,
                                       self.loaded_hourly_cost,
                                       self.operating_weeks,
                                       self.annual_nonlabor_loss)):
            raise ValueError("hotel burden assumptions cannot be negative")

    @property
    def annual_burden(self) -> D:
        return (self.hours_per_week * self.loaded_hourly_cost * self.operating_weeks
                + self.annual_nonlabor_loss)

    @property
    def recoverable_value(self) -> D:
        return self.annual_burden * self.improvement_rate


@dataclass(frozen=True)
class HotelSolutionsWork:
    prospecting_sales: D
    discovery: D
    solution_design: D
    integration_validation: D
    proposal_scoping: D
    coordination: D
    acceptance: D

    def __post_init__(self) -> None:
        if any(value < 0 for value in vars(self).values()):
            raise ValueError("solutions hours cannot be negative")

    @property
    def total_hours(self) -> D:
        return sum(vars(self).values(), D("0"))


@dataclass(frozen=True)
class IndependentHotelCase:
    room_count: int
    burdens: tuple[HotelBurden, ...]
    scenario: OpportunityScenario
    solutions_work: HotelSolutionsWork
    integration_access_note: str

    @property
    def total_burden(self) -> D:
        return sum((item.annual_burden for item in self.burdens), D("0"))

    @property
    def recoverable_value(self) -> D:
        return sum((item.recoverable_value for item in self.burdens), D("0"))


BASELINE_BURDENS = (
    HotelBurden("Management reconciliation", D("8"), D("55"), D("52"), D("0.50")),
    HotelBurden("Reporting / spreadsheets", D("6"), D("42"), D("52"), D("0.55")),
    HotelBurden("Housekeeping coordination", D("10"), D("30"), D("52"), D("0.35")),
    HotelBurden("Staffing coordination", D("5"), D("45"), D("52"), D("0.30")),
    HotelBurden("Booking-channel analysis", D("4"), D("48"), D("52"), D("0.40")),
    HotelBurden("Guest-feedback review", D("3"), D("38"), D("52"), D("0.25")),
    # Kept separate from labor: a conservative fictional pool, not room revenue.
    HotelBurden("Avoidable operational inefficiency", D("0"), D("0"), D("52"),
                D("0.15"), annual_nonlabor_loss=D("15000")),
)

BASELINE_SOLUTIONS = HotelSolutionsWork(
    D("8"), D("10"), D("9"), D("10"), D("6"), D("9"), D("6"))


def _build(*, burdens: tuple[HotelBurden, ...] = BASELINE_BURDENS,
           reusable_hours: D = D("78"), specific_hours: D = D("98"),
           qa_hours: D = D("24"), deployment_hours: D = D("10"),
           rework_hours: D = D("20"), support_hours: D = D("66"),
           support_other: D = D("1800"),
           feasibility: Feasibility = Feasibility.FEASIBLE,
           permission: Level = Level.MODERATE,
           finding: AlternativeFinding = AlternativeFinding.CUSTOM_JUSTIFIED,
           access_note: str = "Documented exports are assumed available, but API rights, fees, credentials, and contract restrictions require validation.") -> IndependentHotelCase:
    total = sum((item.annual_burden for item in burdens), D("0"))
    recoverable = sum((item.recoverable_value for item in burdens), D("0"))
    delivery = DeliveryEconomics(
        reusable_hours, specific_hours, D("75"), qa_hours, deployment_hours,
        rework_hours, D("1500"), support_hours, D("75"), support_other)
    work = BASELINE_SOLUTIONS
    solutions = SolutionsEconomics(
        work.prospecting_sales, work.discovery,
        work.solution_design + work.integration_validation + work.proposal_scoping,
        work.coordination + work.acceptance, D("65"))
    scenario = OpportunityScenario(
        "James River Inn", True,
        CustomerEconomics(total, recoverable, D("30000"), D("9000")), delivery,
        solutions,
        SalesCharacteristics(Level.MODERATE, D("4"), Level.HIGH, Level.MODERATE),
        TechnicalCharacteristics(5, Level.MODERATE, Level.MODERATE, feasibility,
                                 Level.MODERATE, Level.LOW, permission),
        BuildVsBuy(finding, tuple(AlternativeType),
                   "PMS reports/modules, hotel reporting SaaS, channel tools, BI, low-code, spreadsheets, custom integration, and doing nothing were considered."))
    return IndependentHotelCase(138, burdens, scenario, work, access_note)


def baseline_case() -> IndependentHotelCase:
    return _build()


def strong_saas_case() -> IndependentHotelCase:
    return _build(finding=AlternativeFinding.ADEQUATE_BUY)


def easy_integration_case() -> IndependentHotelCase:
    return _build(reusable_hours=D("70"), specific_hours=D("60"), qa_hours=D("16"),
                  rework_hours=D("8"), support_hours=D("42"), permission=Level.LOW,
                  access_note="Clean documented PMS access and standardized source exports are assumed granted.")


def difficult_integration_case() -> IndependentHotelCase:
    return _build(specific_hours=D("190"), qa_hours=D("38"), rework_hours=D("55"),
                  support_hours=D("100"), support_other=D("3000"),
                  feasibility=Feasibility.UNKNOWN, permission=Level.HIGH,
                  access_note="Poor PMS access, uncertain permissions, extensive mapping, and elevated maintenance remain unresolved.")


def higher_burden_case() -> IndependentHotelCase:
    burdens = tuple(replace(item, hours_per_week=item.hours_per_week * D("1.5"))
                    if item.name in {"Management reconciliation", "Reporting / spreadsheets"}
                    else item for item in BASELINE_BURDENS)
    return _build(burdens=burdens)
