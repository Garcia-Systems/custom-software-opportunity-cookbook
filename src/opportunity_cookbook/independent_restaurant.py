"""Fictional educational assumptions for Case 1; no industry data is used."""

from dataclasses import dataclass, replace
from decimal import Decimal as D

from .models import (
    AlternativeFinding, AlternativeType, BuildVsBuy, CustomerEconomics,
    DeliveryEconomics, Feasibility, Level, OpportunityScenario,
    SalesCharacteristics, SolutionsEconomics, TechnicalCharacteristics,
)


def _nonnegative(value: D, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} cannot be negative")


@dataclass(frozen=True)
class BurdenAssumption:
    """One measured burden and the fraction the proposed integration may remove."""

    name: str
    annual_burden: D
    improvement_rate: D

    def __post_init__(self) -> None:
        _nonnegative(self.annual_burden, "annual_burden")
        if not D("0") <= self.improvement_rate <= D("1"):
            raise ValueError("improvement_rate must be between 0 and 1")

    @property
    def recoverable_value(self) -> D:
        return self.annual_burden * self.improvement_rate


@dataclass(frozen=True)
class DeliveryWork:
    name: str
    hours: D
    reusable: bool

    def __post_init__(self) -> None:
        _nonnegative(self.hours, "hours")


@dataclass(frozen=True)
class RestaurantCase:
    scenario: OpportunityScenario
    burdens: tuple[BurdenAssumption, ...]
    delivery_work: tuple[DeliveryWork, ...]
    support_obligations: tuple[str, ...]

    @property
    def total_burden(self) -> D:
        return sum((item.annual_burden for item in self.burdens), D("0"))

    @property
    def recoverable_value(self) -> D:
        return sum((item.recoverable_value for item in self.burdens), D("0"))


BASELINE_BURDENS = (
    BurdenAssumption("Management reconciliation labor", D("10400"), D("0.45")),
    BurdenAssumption("Operational analysis labor", D("6240"), D("0.30")),
    BurdenAssumption("Avoidable waste / purchasing inefficiency", D("9000"), D("0.20")),
    BurdenAssumption("Avoidable labor-planning inefficiency", D("7200"), D("0.20")),
    BurdenAssumption("Other measurable administration", D("2400"), D("0.25")),
)

BASELINE_WORK = (
    DeliveryWork("Discovery-supported technical validation", D("8"), False),
    DeliveryWork("POS adapter/import", D("14"), True),
    DeliveryWork("Reservation adapter/import", D("10"), False),
    DeliveryWork("Scheduling adapter/import", D("10"), False),
    DeliveryWork("Inventory CSV import", D("12"), True),
    DeliveryWork("Feedback import", D("8"), False),
    DeliveryWork("Normalization", D("18"), True),
    DeliveryWork("Business calculations", D("10"), False),
    DeliveryWork("Management briefing", D("12"), True),
    DeliveryWork("Validation/error handling", D("14"), True),
    DeliveryWork("Testing", D("12"), True),
    DeliveryWork("Deployment", D("6"), True),
    DeliveryWork("Documentation", D("6"), False),
    DeliveryWork("Rework reserve", D("10"), False),
)


def _scenario(burdens: tuple[BurdenAssumption, ...], work: tuple[DeliveryWork, ...],
              finding: AlternativeFinding = AlternativeFinding.CUSTOM_JUSTIFIED) -> RestaurantCase:
    total = sum((b.annual_burden for b in burdens), D("0"))
    recoverable = sum((b.recoverable_value for b in burdens), D("0"))
    excluded = {"Testing", "Deployment", "Rework reserve"}
    reusable = sum((w.hours for w in work if w.reusable and w.name not in excluded), D("0"))
    specific = sum((w.hours for w in work if not w.reusable and w.name not in
                    excluded), D("0"))
    named = {w.name: w.hours for w in work}
    delivery = DeliveryEconomics(
        reusable, specific, D("70"), qa_hours=named["Testing"],
        deployment_hours=named["Deployment"], rework_reserve_hours=named["Rework reserve"],
        other_direct_costs=D("400"), annual_support_hours=D("30"),
        support_hourly_cost=D("70"), annual_support_other_direct_costs=D("600"),
    )
    scenario = OpportunityScenario(
        "James River Kitchen", True,
        CustomerEconomics(total, recoverable, D("15000"), D("3000")), delivery,
        SolutionsEconomics(D("5"), D("8"), D("7"), D("8"), D("60")),
        SalesCharacteristics(Level.LOW, D("1.5"), Level.HIGH, Level.LOW),
        TechnicalCharacteristics(5, Level.MODERATE, Level.MODERATE, Feasibility.FEASIBLE,
                                 Level.LOW, Level.LOW, Level.MODERATE),
        BuildVsBuy(finding, tuple(AlternativeType),
                   "Fictional review: cheaper options remain viable candidates, but none is assumed to cover the selected cross-system briefing in the baseline."),
    )
    return RestaurantCase(scenario, burdens, work, (
        "hosting and monitoring", "import failures and changed CSV formats",
        "API changes and bug fixes", "customer support and periodic maintenance",
    ))


def baseline_case() -> RestaurantCase:
    return _scenario(BASELINE_BURDENS, BASELINE_WORK)


def higher_value_case() -> RestaurantCase:
    rates = (D("0.75"), D("0.60"), D("0.45"), D("0.45"), D("0.50"))
    burdens = tuple(replace(item, improvement_rate=rate)
                    for item, rate in zip(BASELINE_BURDENS, rates, strict=True))
    return _scenario(burdens, BASELINE_WORK)


def lower_delivery_cost_case() -> RestaurantCase:
    reductions = {"POS adapter/import": D("6"), "Inventory CSV import": D("5"),
                  "Normalization": D("9"), "Validation/error handling": D("8")}
    work = tuple(replace(item, hours=reductions.get(item.name, item.hours)) for item in BASELINE_WORK)
    return _scenario(BASELINE_BURDENS, work)


def saas_alternative_case() -> RestaurantCase:
    return _scenario(BASELINE_BURDENS, BASELINE_WORK, AlternativeFinding.ADEQUATE_BUY)
