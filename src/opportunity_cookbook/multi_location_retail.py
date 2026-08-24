"""Case 6: fictional multi-location retailer assumptions, not benchmarks."""

from dataclasses import dataclass, replace
from decimal import Decimal as D

from .economics import alternative_first_year_effect, custom_first_year_effect
from .models import (AlternativeEconomics, AlternativeFinding, AlternativeType,
                     BuildVsBuy, CustomerEconomics, DeliveryEconomics,
                     Feasibility, Level, OpportunityScenario,
                     SalesCharacteristics, SolutionsEconomics,
                     TechnicalCharacteristics)
from .scaling import SupportScaling


def _nonnegative(values) -> None:
    if any(value < 0 for value in values):
        raise ValueError("assumptions cannot be negative")


@dataclass(frozen=True)
class RetailBurden:
    name: str
    hours_per_week: D
    loaded_hourly_cost: D
    operating_weeks: D
    improvement_rate: D

    def __post_init__(self) -> None:
        _nonnegative((self.hours_per_week, self.loaded_hourly_cost, self.operating_weeks))
        if not D("0") <= self.improvement_rate <= D("1"):
            raise ValueError("improvement_rate must be between 0 and 1")

    @property
    def annual_burden(self) -> D:
        return self.hours_per_week * self.loaded_hourly_cost * self.operating_weeks

    @property
    def recoverable(self) -> D:
        return self.annual_burden * self.improvement_rate


@dataclass(frozen=True)
class RetailEngineering:
    shared_hours: D
    per_store_hours: D
    store_count: int
    ecommerce_hours: D
    exception_hours: D
    qa_hours: D
    deployment_hours: D
    rework_reserve_hours: D

    def __post_init__(self) -> None:
        if not isinstance(self.store_count, int) or isinstance(self.store_count, bool) or self.store_count < 1:
            raise ValueError("store_count must be a positive integer")
        _nonnegative(value for name, value in vars(self).items() if name != "store_count")

    @property
    def per_store_total_hours(self) -> D:
        return self.per_store_hours * self.store_count

    @property
    def core_hours(self) -> D:
        return self.shared_hours + self.per_store_total_hours + self.ecommerce_hours + self.exception_hours

    @property
    def total_hours(self) -> D:
        return self.core_hours + self.qa_hours + self.deployment_hours + self.rework_reserve_hours


@dataclass(frozen=True)
class RetailSolutionsWork:
    prospecting_sales: D
    discovery: D
    central_operations_interviews: D
    store_process_sampling: D
    technical_validation: D
    solution_design_scoping: D
    proposal: D
    coordination: D
    acceptance: D

    def __post_init__(self) -> None:
        _nonnegative(vars(self).values())

    @property
    def total_hours(self) -> D:
        return sum(vars(self).values(), D("0"))


@dataclass(frozen=True)
class RetailCase:
    burdens: tuple[RetailBurden, ...]
    engineering: RetailEngineering
    support: SupportScaling
    solutions_work: RetailSolutionsWork
    alternative: AlternativeEconomics
    custom_risk_allowance: D
    scenario: OpportunityScenario
    within_customer_reuse: str
    future_customer_reuse: str

    @property
    def total_burden(self) -> D:
        return sum((item.annual_burden for item in self.burdens), D("0"))

    @property
    def recoverable_value(self) -> D:
        return sum((item.recoverable for item in self.burdens), D("0"))


BASELINE_BURDENS = (
    RetailBurden("Cross-store reporting", D("10"), D("48"), D("52"), D(".60")),
    RetailBurden("Inventory reconciliation", D("12"), D("42"), D("52"), D(".45")),
    RetailBurden("E-commerce / store reconciliation", D("7"), D("45"), D("52"), D(".55")),
    RetailBurden("Purchasing and transfer analysis", D("6"), D("50"), D("52"), D(".35")),
    RetailBurden("Returns reconciliation", D("5"), D("40"), D("52"), D(".40")),
    RetailBurden("Data cleanup and exception investigation", D("8"), D("42"), D("52"), D(".35")),
)
BASELINE_ENGINEERING = RetailEngineering(D("170"), D("9"), 6, D("42"), D("30"), D("38"), D("14"), D("30"))
BASELINE_SUPPORT = SupportScaling(D("38"), D("4"), 6, D("18"), D("2400"), D("180"))
BASELINE_SOLUTIONS = RetailSolutionsWork(D("8"), D("8"), D("8"), D("10"), D("12"), D("12"), D("6"), D("8"), D("6"))
BASELINE_ALTERNATIVE = AlternativeEconomics(D("14000"), D("18000"), D("8000"), D("26000"), D("3000"))


def _build(*, burdens=BASELINE_BURDENS, engineering=BASELINE_ENGINEERING,
           support=BASELINE_SUPPORT, solutions_work=BASELINE_SOLUTIONS,
           alternative=BASELINE_ALTERNATIVE, price=D("62000"), fee=D("15000"),
           custom_risk=D("10000"), force_low_reuse=False) -> RetailCase:
    _nonnegative((price, fee, custom_risk))
    total = sum((item.annual_burden for item in burdens), D("0"))
    recoverable = sum((item.recoverable for item in burdens), D("0"))
    customer = CustomerEconomics(total, recoverable, price, fee)
    custom_effect = custom_first_year_effect(customer, custom_risk)
    finding = (AlternativeFinding.ADEQUATE_BUY
               if alternative_first_year_effect(alternative) < custom_effect
               else AlternativeFinding.CUSTOM_JUSTIFIED)
    reusable = D("90") if force_low_reuse else engineering.shared_hours
    specific = engineering.core_hours - reusable
    delivery = DeliveryEconomics(reusable, specific, D("80"), engineering.qa_hours,
        engineering.deployment_hours, engineering.rework_reserve_hours, D("2200"),
        support.total_hours, D("80"), support.total_other_costs)
    w = solutions_work
    solutions = SolutionsEconomics(w.prospecting_sales,
        w.discovery + w.central_operations_interviews + w.store_process_sampling,
        w.technical_validation + w.solution_design_scoping + w.proposal,
        w.coordination + w.acceptance, D("70"))
    scenario = OpportunityScenario("James River Outfitters", True, customer, delivery,
        solutions, SalesCharacteristics(Level.MODERATE, D("5"), Level.HIGH, Level.MODERATE),
        TechnicalCharacteristics(7, Level.MODERATE, Level.MODERATE, Feasibility.FEASIBLE,
            Level.LOW, Level.LOW, Level.MODERATE),
        BuildVsBuy(finding, tuple(AlternativeType),
            "POS-suite configuration, native reporting, e-commerce/POS integrations, retail inventory or ERP SaaS, BI, low-code, improved spreadsheets/process, narrow custom integration, and doing nothing were evaluated using total first-year effect."))
    return RetailCase(burdens, engineering, support, solutions_work, alternative,
        custom_risk, scenario,
        "High: common adapters, identifiers, validation, and reporting are shared across six stores.",
        "Plausible but unvalidated: standard APIs aid reuse while also strengthening mature SaaS competitors.")


def baseline_case() -> RetailCase:
    return _build()


def weak_saas_alternative_case() -> RetailCase:
    # A narrower scope and price are plausible when configuration cannot cover the workflow.
    return _build(alternative=replace(BASELINE_ALTERNATIVE, residual_annual_burden=D("110000")),
        price=D("40000"), fee=D("10000"))


def strong_saas_alternative_case() -> RetailCase:
    return _build(alternative=AlternativeEconomics(D("8000"), D("14000"), D("6000"), D("12000"), D("1500")))


def highly_standardized_case() -> RetailCase:
    eng = RetailEngineering(D("150"), D("4"), 6, D("24"), D("8"), D("24"), D("10"), D("14"))
    support = SupportScaling(D("28"), D("2"), 6, D("6"), D("1800"), D("120"))
    return _build(engineering=eng, support=support)


def messy_acquired_stores_case() -> RetailCase:
    eng = RetailEngineering(D("180"), D("18"), 6, D("50"), D("130"), D("55"), D("20"), D("60"))
    support = SupportScaling(D("45"), D("8"), 6, D("55"), D("3200"), D("350"))
    return _build(engineering=eng, support=support, custom_risk=D("18000"))


def higher_burden_case() -> RetailCase:
    burdens = tuple(replace(item, hours_per_week=item.hours_per_week * D("1.8")) for item in BASELINE_BURDENS)
    return _build(burdens=burdens, alternative=replace(BASELINE_ALTERNATIVE, residual_annual_burden=D("160000")))


def one_off_niche_case() -> RetailCase:
    burdens = tuple(replace(item, hours_per_week=item.hours_per_week * D("2.2"), improvement_rate=D(".65")) for item in BASELINE_BURDENS)
    alternative = replace(BASELINE_ALTERNATIVE, residual_annual_burden=D("150000"))
    return _build(burdens=burdens, alternative=alternative, price=D("70000"),
        fee=D("17000"), force_low_reuse=True)
