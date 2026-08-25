"""Case 13: fictional customer value that cannot fund sustainable delivery."""

from dataclasses import dataclass, replace
from decimal import Decimal as D

from .analysis import analyze
from .economics import (customer_maximum_economic_price,
    delivery_break_even_price, has_feasible_price_corridor,
    implementation_contribution, implementation_delivery_cost,
    target_contribution_price)
from .models import (AlternativeFinding, AlternativeType, BuildVsBuy,
    CustomerEconomics, DeliveryEconomics, Feasibility, Level,
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
    improvement_rate: D

    def __post_init__(self) -> None:
        if self.hours_per_week < 0 or self.hourly_cost < 0:
            raise ValueError("burden assumptions cannot be negative")
        _rate(self.improvement_rate, "improvement_rate")

    @property
    def annual_burden(self) -> D:
        return self.hours_per_week * D("52") * self.hourly_cost

    @property
    def recoverable_value(self) -> D:
        return self.annual_burden * self.improvement_rate


@dataclass(frozen=True)
class EngineeringWork:
    name: str
    hours: D
    reusable: bool

    def __post_init__(self) -> None:
        if self.hours < 0:
            raise ValueError("engineering hours cannot be negative")


@dataclass(frozen=True)
class BadDeliveryCase:
    burdens: tuple[WorkflowBurden, ...]
    base_work: tuple[EngineeringWork, ...]
    scenario: OpportunityScenario
    required_implementation_contribution: D
    required_customer_retained_benefit: D
    discovery_price: D = D("0")

    def __post_init__(self) -> None:
        if any(x < 0 for x in (self.required_implementation_contribution,
                               self.required_customer_retained_benefit,
                               self.discovery_price)):
            raise ValueError("commercial assumptions cannot be negative")

    @property
    def total_burden(self) -> D:
        return sum((x.annual_burden for x in self.burdens), D("0"))

    @property
    def recoverable_value(self) -> D:
        return sum((x.recoverable_value for x in self.burdens), D("0"))

    @property
    def base_engineering_hours(self) -> D:
        return sum((x.hours for x in self.base_work), D("0"))

    @property
    def total_engineering_hours(self) -> D:
        d = self.scenario.delivery
        return sum((d.reusable_engineering_hours, d.customer_specific_engineering_hours,
                    d.qa_hours, d.deployment_hours, d.rework_reserve_hours,
                    d.uncertainty_reserve_hours), D("0"))

    @property
    def direct_delivery_cost(self) -> D:
        return implementation_delivery_cost(self.scenario.delivery)

    @property
    def implementation_contribution(self) -> D:
        return implementation_contribution(
            self.scenario.customer.implementation_price, self.direct_delivery_cost)

    @property
    def break_even_price(self) -> D:
        return delivery_break_even_price(self.direct_delivery_cost)

    @property
    def target_price(self) -> D:
        return target_contribution_price(self.direct_delivery_cost,
            self.required_implementation_contribution)

    @property
    def customer_maximum_price(self) -> D:
        return customer_maximum_economic_price(self.recoverable_value,
            self.scenario.customer.recurring_annual_fee,
            self.required_customer_retained_benefit)

    @property
    def feasible_price_corridor(self) -> bool:
        return has_feasible_price_corridor(self.target_price,
            self.customer_maximum_price)


BASELINE_BURDENS = (
    WorkflowBurden("Order validation and duplicate entry", D("9"), D("34"), D(".58")),
    WorkflowBurden("Supplier and special-order coordination", D("10"), D("38"), D(".55")),
    WorkflowBurden("Inventory and order reconciliation", D("7"), D("36"), D(".52")),
    WorkflowBurden("Shipping-status reconciliation", D("5"), D("34"), D(".48")),
    WorkflowBurden("Invoice reconciliation", D("5"), D("37"), D(".50")),
    WorkflowBurden("Exception handling and avoidable rework", D("8"), D("40"), D(".50")),
    WorkflowBurden("Management reporting", D("4"), D("46"), D(".45")),
)

BASELINE_WORK = (
    EngineeringWork("Technical discovery", D("28"), False),
    EngineeringWork("Customer portal integration", D("34"), False),
    EngineeringWork("Warehouse / inventory integration", D("48"), False),
    EngineeringWork("Supplier adapter A", D("34"), False),
    EngineeringWork("Supplier adapter B", D("38"), False),
    EngineeringWork("Supplier adapter C", D("42"), False),
    EngineeringWork("Shipping integration", D("24"), False),
    EngineeringWork("Accounting integration", D("32"), False),
    EngineeringWork("Customer-specific rules and exceptions", D("48"), False),
    EngineeringWork("Generic order-state normalization", D("34"), True),
    EngineeringWork("Validation / idempotency framework", D("24"), True),
    EngineeringWork("Logging and monitoring", D("22"), True),
)


def _build(*, burdens=BASELINE_BURDENS, work=BASELINE_WORK,
        price=D("20000"), fee=D("7000"), qa=D("70"), deployment=D("12"),
        rework=D("55"), uncertainty=D("75"), other=D("1800"),
        support_hours=D("72"), support_other=D("1800"),
        required_contribution=D("6000"), retained_benefit=D("14000"),
        feasibility=Feasibility.FEASIBLE, discovery_price=D("0")) -> BadDeliveryCase:
    total = sum((x.annual_burden for x in burdens), D("0"))
    recovery = sum((x.recoverable_value for x in burdens), D("0"))
    reusable = sum((x.hours for x in work if x.reusable), D("0"))
    specific = sum((x.hours for x in work if not x.reusable), D("0"))
    delivery = DeliveryEconomics(reusable, specific, D("70"), qa, deployment,
        rework, other, support_hours, D("70"), support_other, uncertainty)
    scenario = OpportunityScenario("James River Specialty Distribution", True,
        CustomerEconomics(total, recovery, price, fee), delivery,
        SolutionsEconomics(D("5"), D("18"), D("14"), D("18"), D("65")),
        SalesCharacteristics(Level.MODERATE, D("4"), Level.HIGH, Level.MODERATE),
        TechnicalCharacteristics(8, Level.HIGH, Level.LOW, feasibility,
            Level.LOW, Level.LOW, Level.HIGH),
        BuildVsBuy(AlternativeFinding.CUSTOM_JUSTIFIED,
            (AlternativeType.EXISTING_SAAS, AlternativeType.SAAS_CONFIGURATION,
             AlternativeType.AUTOMATION_TOOLING, AlternativeType.CUSTOM_INTEGRATION,
             AlternativeType.DO_NOTHING),
            "Fictional discovery found no supported product that handles the unusual supplier, inventory, accounting, and exception rules."))
    return BadDeliveryCase(tuple(burdens), tuple(work), scenario,
        required_contribution, retained_benefit, discovery_price)


def baseline_case(): return _build()
def raise_price_only_case(): return _build(price=baseline_case().target_price)


def reduced_scope_case():
    burdens = tuple(b for b in BASELINE_BURDENS if b.name not in
        ("Shipping-status reconciliation", "Invoice reconciliation"))
    work = tuple(replace(w, hours=w.hours * D(".55")) for w in BASELINE_WORK if w.name not in
        ("Supplier adapter C", "Shipping integration", "Accounting integration"))
    return _build(burdens=burdens, work=work, price=D("24000"), fee=D("6000"),
        qa=D("38"), rework=D("22"), uncertainty=D("25"), other=D("1000"),
        support_hours=D("42"), support_other=D("1000"),
        required_contribution=D("4000"), retained_benefit=D("8000"))


def better_integration_access_case():
    work = tuple(replace(w, hours=w.hours * D(".60")) for w in BASELINE_WORK)
    return _build(work=work, price=D("32000"), qa=D("42"), rework=D("20"),
        uncertainty=D("15"), other=D("1200"), support_hours=D("52"),
        retained_benefit=D("8000"))


def reusable_adapters_case():
    names = {"Supplier adapter A", "Supplier adapter B", "Supplier adapter C"}
    work = tuple(replace(w, hours=w.hours * D(".35"), reusable=True)
                 if w.name in names else w for w in BASELINE_WORK)
    return _build(work=work, price=D("30000"), qa=D("45"), rework=D("25"),
        uncertainty=D("22"), other=D("1200"), support_hours=D("50"))


def high_bespoke_logic_case():
    work = tuple(replace(w, hours=D("90")) if
        w.name == "Customer-specific rules and exceptions" else w
        for w in BASELINE_WORK)
    return _build(work=work, rework=D("75"), uncertainty=D("95"))


def paid_discovery_case():
    # Paid discovery narrows the reserve, but the estimated implementation still loses money.
    return _build(uncertainty=D("30"), feasibility=Feasibility.UNKNOWN,
        discovery_price=D("6000"))


def one_off_viable_case():
    work = tuple(replace(w, hours=w.hours * D(".58")) for w in BASELINE_WORK)
    return _build(work=work, price=D("32000"), qa=D("42"), rework=D("24"),
        uncertainty=D("18"), other=D("1000"), support_hours=D("55"),
        required_contribution=D("4000"), retained_benefit=D("7000"))


def scenario_results():
    cases = (("Baseline", baseline_case()), ("Raise price only", raise_price_only_case()),
        ("Reduced scope", reduced_scope_case()),
        ("Better integration access", better_integration_access_case()),
        ("Reusable supplier adapters", reusable_adapters_case()),
        ("High bespoke logic", high_bespoke_logic_case()),
        ("Paid discovery", paid_discovery_case()),
        ("One-off but viable", one_off_viable_case()))
    return tuple((name, analyze(case.scenario).verdict.value) for name, case in cases)


def case_12_vs_13():
    from .buy_dont_build import baseline_case as case12
    return (("Case 12", analyze(case12().final_scenario).verdict.value,
             case12().final_scenario.build_vs_buy.finding.value),
            ("Case 13", analyze(baseline_case().scenario).verdict.value,
             baseline_case().scenario.build_vs_buy.finding.value))


def case_7_vs_13():
    from .construction_trades import baseline_case as case7
    return (("Case 7", analyze(case7().scenario).verdict.value,
             case7().scenario.technical.integration_complexity.value),
            ("Case 13", analyze(baseline_case().scenario).verdict.value,
             baseline_case().scenario.technical.integration_complexity.value))
