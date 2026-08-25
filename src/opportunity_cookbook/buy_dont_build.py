"""Case 12: a fictional deal changed by discovery of a strong alternative."""

from dataclasses import dataclass, replace
from decimal import Decimal as D

from .analysis import analyze
from .economics import (alternative_first_year_effect, alternative_recovered_burden,
    break_even_alternative_residual_burden, custom_first_year_effect,
    incremental_custom_value)
from .models import (AlternativeEconomics, AlternativeFinding, AlternativeType,
    BuildVsBuy, CustomerEconomics, DeliveryEconomics, Feasibility, Level,
    OpportunityScenario, SalesCharacteristics, SolutionsEconomics,
    TechnicalCharacteristics)


def _rate(value: D, name: str) -> None:
    if not D("0") <= value <= D("1"):
        raise ValueError(f"{name} must be between 0 and 1")


@dataclass(frozen=True)
class WorkflowBurden:
    name: str
    hours_per_week: D
    hourly_cost: D
    recovery_rate: D

    def __post_init__(self) -> None:
        if self.hours_per_week < 0 or self.hourly_cost < 0:
            raise ValueError("burden assumptions cannot be negative")
        _rate(self.recovery_rate, "recovery_rate")

    @property
    def annual_burden(self) -> D:
        return self.hours_per_week * D("52") * self.hourly_cost

    @property
    def recoverable(self) -> D:
        return self.annual_burden * self.recovery_rate


@dataclass(frozen=True)
class EdgeEconomics:
    implementation_cost: D
    recurring_annual_cost: D
    residual_burden_recovered: D

    def __post_init__(self) -> None:
        if any(x < 0 for x in vars(self).values()):
            raise ValueError("edge assumptions cannot be negative")


@dataclass(frozen=True)
class OptionOutcome:
    name: str
    first_year_cost: D
    recurring_cost: D
    burden_remaining: D
    burden_removed: D
    first_year_net_benefit: D
    payback_months: D | None


@dataclass(frozen=True)
class BuyDontBuildCase:
    burdens: tuple[WorkflowBurden, ...]
    saas: AlternativeEconomics
    saas_name: str
    saas_solve_rate: D
    edge: EdgeEconomics
    stage_one: OpportunityScenario
    final_scenario: OpportunityScenario

    def __post_init__(self) -> None:
        _rate(self.saas_solve_rate, "saas_solve_rate")
        if self.saas.residual_annual_burden > self.total_burden:
            raise ValueError("SaaS residual burden cannot exceed original burden")
        if self.edge.residual_burden_recovered > self.saas.residual_annual_burden:
            raise ValueError("edge cannot recover more than the SaaS residual burden")

    @property
    def total_burden(self) -> D:
        return sum((x.annual_burden for x in self.burdens), D("0"))

    @property
    def recoverable_value(self) -> D:
        return sum((x.recoverable for x in self.burdens), D("0"))

    @property
    def saas_recoverable_value(self) -> D:
        return alternative_recovered_burden(self.total_burden,
            self.saas.residual_annual_burden)

    @property
    def incremental_custom_value(self) -> D:
        return incremental_custom_value(self.recoverable_value,
            self.saas_recoverable_value)

    @property
    def break_even_residual_burden(self) -> D:
        effect = custom_first_year_effect(self.stage_one.customer)
        assert effect is not None
        return break_even_alternative_residual_burden(effect, self.saas)

    def options(self) -> tuple[OptionOutcome, ...]:
        burden = self.total_burden
        custom = self.stage_one.customer
        custom_cash = custom.implementation_price + custom.recurring_annual_fee
        custom_remaining = burden - self.recoverable_value
        saas_cash = (self.saas.setup_cost + self.saas.recurring_annual_cost
                     + self.saas.internal_administration_cost + self.saas.risk_allowance)
        edge_cash = saas_cash + self.edge.implementation_cost + self.edge.recurring_annual_cost
        edge_remaining = self.saas.residual_annual_burden - self.edge.residual_burden_recovered

        def outcome(name, cash, recurring, remaining, setup):
            removed = burden - remaining
            annual_net = removed - recurring
            payback = None if annual_net <= 0 else setup / annual_net * D("12")
            return OptionOutcome(name, cash, recurring, remaining, removed,
                removed - cash, payback)
        return (
            outcome("Do nothing", D("0"), D("0"), burden, D("0")),
            outcome("Full custom", custom_cash, custom.recurring_annual_fee,
                custom_remaining, custom.implementation_price),
            outcome("Buy / configure", saas_cash,
                self.saas.recurring_annual_cost + self.saas.internal_administration_cost,
                self.saas.residual_annual_burden, self.saas.setup_cost),
            outcome("SaaS + narrow custom edge", edge_cash,
                self.saas.recurring_annual_cost + self.saas.internal_administration_cost
                    + self.edge.recurring_annual_cost,
                edge_remaining, self.saas.setup_cost + self.edge.implementation_cost),
        )

    @property
    def recommendation(self) -> str:
        viable = self.options()[1:]
        best = max(viable, key=lambda x: x.first_year_net_benefit)
        return best.name


BASELINE_BURDENS = (
    WorkflowBurden("Duplicate entry", D("5"), D("32"), D(".70")),
    WorkflowBurden("Scheduling reconciliation", D("6"), D("36"), D(".65")),
    WorkflowBurden("Technician-status reconciliation", D("5"), D("35"), D(".65")),
    WorkflowBurden("Service-record administration", D("7"), D("34"), D(".60")),
    WorkflowBurden("Invoice preparation", D("4"), D("38"), D(".55")),
    WorkflowBurden("Customer follow-up", D("3"), D("32"), D(".55")),
    WorkflowBurden("Management reporting", D("4"), D("45"), D(".65")),
    WorkflowBurden("Avoidable rework", D("2"), D("42"), D(".50")),
)
BASELINE_SAAS = AlternativeEconomics(D("3000"), D("4200"), D("2400"),
    D("30008.42"))
BASELINE_EDGE = EdgeEconomics(D("4500"), D("800"), D("2600"))


def _scenario(burdens, alternative, *, price=D("12000"), fee=D("3000"),
        finding=AlternativeFinding.CUSTOM_JUSTIFIED):
    total = sum((x.annual_burden for x in burdens), D("0"))
    recovery = sum((x.recoverable for x in burdens), D("0"))
    customer = CustomerEconomics(total, recovery, price, fee)
    delivery = DeliveryEconomics(D("55"), D("35"), D("70"), D("12"), D("5"),
        D("10"), D("500"), D("20"), D("70"), D("600"))
    solutions = SolutionsEconomics(D("4"), D("10"), D("9"), D("7"), D("65"))
    return OpportunityScenario("James River Equipment Services", True, customer,
        delivery, solutions,
        SalesCharacteristics(Level.LOW, D("2"), Level.HIGH, Level.LOW),
        TechnicalCharacteristics(4, Level.MODERATE, Level.HIGH,
            Feasibility.FEASIBLE, Level.LOW, Level.LOW, Level.MODERATE),
        BuildVsBuy(finding, (AlternativeType.EXISTING_SAAS,
            AlternativeType.SAAS_CONFIGURATION, AlternativeType.CUSTOM_INTEGRATION,
            AlternativeType.DO_NOTHING),
            "Discovery compares total outcomes, residual burden, and the true custom edge."))


def _build(*, burdens=BASELINE_BURDENS, saas=BASELINE_SAAS,
        solve_rate=D(".90"), edge=BASELINE_EDGE, price=D("12000"), fee=D("3000")):
    _rate(solve_rate, "solve_rate")
    stage_one = _scenario(burdens, saas, price=price, fee=fee)
    custom_effect = custom_first_year_effect(stage_one.customer)
    finding = (AlternativeFinding.ADEQUATE_BUY
        if alternative_first_year_effect(saas) < custom_effect
        else AlternativeFinding.CUSTOM_JUSTIFIED)
    final = replace(stage_one, build_vs_buy=replace(stage_one.build_vs_buy,
        finding=finding))
    return BuyDontBuildCase(burdens, saas, "ServiceFlow Pro (fictional)",
        solve_rate, edge, stage_one, final)


def baseline_case(): return _build()
def pre_alternative_case(): return baseline_case()
def strong_saas_case(): return baseline_case()
def weak_saas_case(): return _build(saas=replace(BASELINE_SAAS, residual_annual_burden=D("42000")), solve_rate=D(".61"))
def expensive_saas_case(): return _build(saas=replace(BASELINE_SAAS, setup_cost=D("20000"), recurring_annual_cost=D("12000")))
def small_unique_gap_case(): return baseline_case()
def large_unique_gap_case(): return _build(saas=replace(BASELINE_SAAS, residual_annual_burden=D("20000")), solve_rate=D(".61"), edge=EdgeEconomics(D("5000"), D("1000"), D("14000")))
def cheap_custom_case(): return _build(price=D("7000"), fee=D("8000"))
def saas_support_burden_case(): return _build(saas=replace(BASELINE_SAAS, internal_administration_cost=D("15000")))


def scenario_results():
    cases = (("Pre-alternative discovery", pre_alternative_case()),
        ("Strong SaaS", strong_saas_case()), ("Weak SaaS", weak_saas_case()),
        ("Expensive SaaS", expensive_saas_case()),
        ("Small unique gap", small_unique_gap_case()),
        ("Large unique gap", large_unique_gap_case()),
        ("Cheap custom", cheap_custom_case()),
        ("SaaS support burden", saas_support_burden_case()))
    return tuple((name, analyze(case.stage_one).verdict.value if name.startswith("Pre-")
        else (analyze(case.final_scenario).verdict.value
              if case.recommendation != "SaaS + narrow custom edge"
              else case.recommendation.upper())) for name, case in cases)
