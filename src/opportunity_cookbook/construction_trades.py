"""Case 7: fictional construction/trades assumptions, not industry benchmarks."""

from dataclasses import dataclass, replace
from decimal import Decimal as D

from .economics import alternative_first_year_effect, custom_first_year_effect
from .models import (AlternativeEconomics, AlternativeFinding, AlternativeType,
                     BuildVsBuy, CustomerEconomics, DeliveryEconomics, Feasibility,
                     Level, OpportunityScenario, SalesCharacteristics,
                     SolutionsEconomics, TechnicalCharacteristics)


def _nonnegative(values) -> None:
    if any(value < 0 for value in values):
        raise ValueError("assumptions cannot be negative")


@dataclass(frozen=True)
class HandoffBurden:
    """An explicit activity or incident burden; never an opaque handoff score."""

    name: str
    annual_units: D
    cost_per_unit: D
    improvement_rate: D
    kind: str = "administrative labor"

    def __post_init__(self) -> None:
        _nonnegative((self.annual_units, self.cost_per_unit))
        if not D("0") <= self.improvement_rate <= D("1"):
            raise ValueError("improvement_rate must be between 0 and 1")

    @property
    def annual_burden(self) -> D:
        return self.annual_units * self.cost_per_unit

    @property
    def recoverable(self) -> D:
        return self.annual_burden * self.improvement_rate


@dataclass(frozen=True)
class BillingTimingBurden:
    """Financing cost of invoice delay—not the invoice principal or lost revenue."""

    annual_invoice_flow: D
    avoidable_delay_days: D
    annual_financing_rate: D
    improvement_rate: D

    def __post_init__(self) -> None:
        _nonnegative((self.annual_invoice_flow, self.avoidable_delay_days))
        for name in ("annual_financing_rate", "improvement_rate"):
            value = getattr(self, name)
            if not D("0") <= value <= D("1"):
                raise ValueError(f"{name} must be between 0 and 1")

    @property
    def annual_burden(self) -> D:
        return self.annual_invoice_flow * self.avoidable_delay_days / D("365") * self.annual_financing_rate

    @property
    def recoverable(self) -> D:
        return self.annual_burden * self.improvement_rate


@dataclass(frozen=True)
class TradesEngineering:
    technical_discovery: D
    api_validation: D
    adapters: D
    identity_normalization: D
    orchestration: D
    reliability_error_handling: D
    exception_workflow: D
    qa_testing: D
    deployment: D
    documentation: D
    rework_reserve: D
    reusable_core: D

    def __post_init__(self) -> None:
        _nonnegative(vars(self).values())
        if self.reusable_core > self.core_hours:
            raise ValueError("reusable_core cannot exceed core engineering hours")

    @property
    def core_hours(self) -> D:
        return sum((self.technical_discovery, self.api_validation, self.adapters,
                    self.identity_normalization, self.orchestration,
                    self.reliability_error_handling, self.exception_workflow,
                    self.documentation), D("0"))

    @property
    def total_hours(self) -> D:
        return self.core_hours + self.qa_testing + self.deployment + self.rework_reserve


@dataclass(frozen=True)
class TradesSolutionsWork:
    prospecting_sales: D
    discovery: D
    workflow_mapping: D
    stakeholder_interviews: D
    integration_feasibility: D
    requirements_scoping: D
    solution_design: D
    proposal: D
    coordination: D
    acceptance: D

    def __post_init__(self) -> None:
        _nonnegative(vars(self).values())

    @property
    def total_hours(self) -> D:
        return sum(vars(self).values(), D("0"))


@dataclass(frozen=True)
class TradesSupport:
    engineering_hours: D
    hourly_cost: D
    hosting_monitoring: D
    vendor_and_incident_costs: D

    def __post_init__(self) -> None:
        _nonnegative(vars(self).values())

    @property
    def annual_cost(self) -> D:
        return (self.engineering_hours * self.hourly_cost + self.hosting_monitoring
                + self.vendor_and_incident_costs)


@dataclass(frozen=True)
class ConstructionTradesCase:
    burdens: tuple[HandoffBurden, ...]
    billing_timing: BillingTimingBurden
    engineering: TradesEngineering
    solutions_work: TradesSolutionsWork
    support: TradesSupport
    alternative: AlternativeEconomics
    custom_risk_allowance: D
    scenario: OpportunityScenario

    @property
    def total_burden(self) -> D:
        return sum((x.annual_burden for x in self.burdens), self.billing_timing.annual_burden)

    @property
    def recoverable_value(self) -> D:
        return sum((x.recoverable for x in self.burdens), self.billing_timing.recoverable)


def _weekly(name, hours, cost, improvement):
    return HandoffBurden(name, D(hours) * D("52"), D(cost), D(improvement))


BASELINE_BURDENS = (
    _weekly("Duplicate entry", "12", "38", ".65"),
    _weekly("Estimate-to-job reconciliation", "8", "45", ".55"),
    _weekly("Scheduling coordination", "7", "42", ".40"),
    _weekly("Materials / purchasing coordination", "5", "40", ".35"),
    _weekly("Field-to-office reconciliation", "9", "40", ".55"),
    _weekly("Completion-to-invoice administration", "6", "38", ".50"),
    HandoffBurden("Error correction / rework", D("72"), D("240"), D(".35"), "incidents"),
    _weekly("Management status reporting", "4", "50", ".50"),
)
BASELINE_BILLING = BillingTimingBurden(D("2400000"), D("8"), D(".08"), D(".40"))
BASELINE_ENGINEERING = TradesEngineering(D("24"), D("36"), D("104"), D("34"), D("58"),
    D("48"), D("34"), D("54"), D("16"), D("22"), D("36"), D("190"))
BASELINE_SOLUTIONS = TradesSolutionsWork(D("8"), D("10"), D("14"), D("12"), D("12"),
    D("10"), D("10"), D("5"), D("4"), D("3"))
BASELINE_SUPPORT = TradesSupport(D("92"), D("85"), D("1800"), D("1200"))
BASELINE_ALTERNATIVE = AlternativeEconomics(D("26000"), D("30000"), D("12000"), D("88000"), D("8000"))


def _build(*, burdens=BASELINE_BURDENS, billing=BASELINE_BILLING,
           engineering=BASELINE_ENGINEERING, solutions=BASELINE_SOLUTIONS,
           support=BASELINE_SUPPORT, alternative=BASELINE_ALTERNATIVE,
           price=D("50000"), fee=D("12000"), custom_risk=D("12000")) -> ConstructionTradesCase:
    _nonnegative((price, fee, custom_risk))
    total = sum((x.annual_burden for x in burdens), billing.annual_burden)
    recoverable = sum((x.recoverable for x in burdens), billing.recoverable)
    customer = CustomerEconomics(total, recoverable, price, fee)
    custom_effect = custom_first_year_effect(customer, custom_risk)
    finding = (AlternativeFinding.ADEQUATE_BUY
               if alternative_first_year_effect(alternative) < custom_effect
               else AlternativeFinding.CUSTOM_JUSTIFIED)
    delivery = DeliveryEconomics(engineering.reusable_core,
        engineering.core_hours - engineering.reusable_core, D("85"),
        engineering.qa_testing, engineering.deployment, engineering.rework_reserve,
        D("2500"), support.engineering_hours, support.hourly_cost,
        support.hosting_monitoring + support.vendor_and_incident_costs)
    s = solutions
    solution_econ = SolutionsEconomics(s.prospecting_sales,
        s.discovery + s.workflow_mapping + s.stakeholder_interviews,
        s.integration_feasibility + s.requirements_scoping + s.solution_design + s.proposal,
        s.coordination + s.acceptance, D("70"))
    scenario = OpportunityScenario("James River Mechanical", True, customer, delivery,
        solution_econ, SalesCharacteristics(Level.MODERATE, D("4"), Level.HIGH, Level.MODERATE),
        TechnicalCharacteristics(6, Level.HIGH, Level.MODERATE, Feasibility.FEASIBLE,
            Level.MODERATE, Level.LOW, Level.MODERATE),
        BuildVsBuy(finding, tuple(AlternativeType),
            "Vertical construction/field-service SaaS, suite expansion, accounting and native integrations, low-code, process redesign, spreadsheets, narrow custom integration, full replacement, and doing nothing were compared. Full replacement is the highest-risk scope."))
    return ConstructionTradesCase(burdens, billing, engineering, solutions, support,
        alternative, custom_risk, scenario)


def baseline_case(): return _build()

def existing_saas_case():
    return _build(alternative=AlternativeEconomics(D("12000"), D("24000"), D("7000"), D("28000"), D("3000")))

def clean_integrations_case():
    e = replace(BASELINE_ENGINEERING, api_validation=D("18"), adapters=D("70"),
        reliability_error_handling=D("36"), qa_testing=D("40"), rework_reserve=D("20"), reusable_core=D("170"))
    return _build(engineering=e, support=replace(BASELINE_SUPPORT, engineering_hours=D("60"), vendor_and_incident_costs=D("700")))

def difficult_integrations_case():
    e = replace(BASELINE_ENGINEERING, api_validation=D("80"), adapters=D("190"),
        reliability_error_handling=D("80"), qa_testing=D("82"), rework_reserve=D("90"))
    return _build(engineering=e, support=replace(BASELINE_SUPPORT, engineering_hours=D("150"), vendor_and_incident_costs=D("3000")), custom_risk=D("26000"))

def high_burden_case():
    return _build(burdens=tuple(replace(x, annual_units=x.annual_units * D("1.6")) for x in BASELINE_BURDENS),
        alternative=replace(BASELINE_ALTERNATIVE, residual_annual_burden=D("180000")))

def low_burden_case():
    return _build(burdens=tuple(replace(x, annual_units=x.annual_units * D(".35")) for x in BASELINE_BURDENS),
        billing=replace(BASELINE_BILLING, avoidable_delay_days=D("2")))

def highly_customer_specific_case():
    e = replace(BASELINE_ENGINEERING, adapters=D("180"), orchestration=D("105"),
        exception_workflow=D("75"), reusable_core=D("140"), qa_testing=D("70"), rework_reserve=D("50"))
    burdens = tuple(replace(x, annual_units=x.annual_units * D("1.7")) for x in BASELINE_BURDENS)
    return _build(engineering=e, burdens=burdens, price=D("85000"), fee=D("18000"),
        alternative=replace(BASELINE_ALTERNATIVE, residual_annual_burden=D("150000")))

def unsustainable_support_case():
    return _build(support=replace(BASELINE_SUPPORT, engineering_hours=D("190"),
        hosting_monitoring=D("3500"), vendor_and_incident_costs=D("3500")))
