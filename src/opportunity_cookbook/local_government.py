"""Case 9: entirely fictional local-government opportunity assumptions."""

from dataclasses import dataclass, replace
from decimal import Decimal as D

from .economics import alternative_first_year_effect, custom_first_year_effect
from .models import (AlternativeEconomics, AlternativeFinding, AlternativeType,
    BuildVsBuy, CustomerEconomics, DeliveryEconomics, Feasibility, Level,
    OpportunityScenario, SalesCharacteristics, SolutionsEconomics,
    TechnicalCharacteristics)


def _nonnegative(values) -> None:
    if any(value < 0 for value in values):
        raise ValueError("assumptions cannot be negative")


@dataclass(frozen=True)
class GovernmentBurden:
    name: str
    annual_units: D
    cost_per_unit: D
    improvement_rate: D
    basis: str = "labor hours"

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
class GovernmentEngineering:
    technical_discovery: D; integration_access_validation: D; legacy_adapter: D
    document_status_integration: D; normalization: D; workflow_status_model: D
    audit_logging: D; security_hardening: D; accessibility: D; documentation: D
    testing: D; deployment_constraints: D; rework_reserve: D; reusable_core: D

    def __post_init__(self) -> None:
        _nonnegative(vars(self).values())
        if self.reusable_core > self.core_hours:
            raise ValueError("reusable_core cannot exceed core hours")

    @property
    def security_accessibility_hours(self) -> D:
        return self.security_hardening + self.accessibility

    @property
    def core_hours(self) -> D:
        return sum((self.technical_discovery, self.integration_access_validation,
            self.legacy_adapter, self.document_status_integration, self.normalization,
            self.workflow_status_model, self.audit_logging, self.security_hardening,
            self.accessibility, self.documentation), D("0"))

    @property
    def total_hours(self) -> D:
        return self.core_hours + self.testing + self.deployment_constraints + self.rework_reserve


@dataclass(frozen=True)
class ProcurementWork:
    prospecting: D; discovery: D; stakeholder_meetings: D; technical_validation: D
    security_documentation: D; accessibility_review: D; proposal_rfp: D
    procurement_support: D; contract_coordination: D; implementation_planning: D
    acceptance: D; other_coordination: D

    def __post_init__(self) -> None: _nonnegative(vars(self).values())

    @property
    def security_procurement_hours(self) -> D:
        return (self.security_documentation + self.accessibility_review
                + self.procurement_support + self.contract_coordination)

    @property
    def total_hours(self) -> D: return sum(vars(self).values(), D("0"))


@dataclass(frozen=True)
class GovernmentSupport:
    engineering_hours: D; hourly_cost: D; hosting: D; monitoring: D
    security_updates: D; vendor_api_changes: D; audit_logging: D
    accessibility_fixes: D; incident_response: D; documentation: D; change_control: D

    def __post_init__(self) -> None: _nonnegative(vars(self).values())

    @property
    def annual_cost(self) -> D:
        return self.engineering_hours * self.hourly_cost + sum((self.hosting,
            self.monitoring, self.security_updates, self.vendor_api_changes,
            self.audit_logging, self.accessibility_fixes, self.incident_response,
            self.documentation, self.change_control), D("0"))


@dataclass(frozen=True)
class LocalGovernmentCase:
    burdens: tuple[GovernmentBurden, ...]
    engineering: GovernmentEngineering
    procurement: ProcurementWork
    support: GovernmentSupport
    alternative: AlternativeEconomics
    custom_risk_allowance: D
    scenario: OpportunityScenario

    @property
    def total_burden(self): return sum((x.annual_burden for x in self.burdens), D("0"))
    @property
    def recoverable_value(self): return sum((x.recoverable for x in self.burdens), D("0"))


def _weekly(name, hours, cost, rate):
    return GovernmentBurden(name, D(hours) * D("52"), D(cost), D(rate))


BASELINE_BURDENS = (
    _weekly("Duplicate entry", "18", "38", ".55"),
    _weekly("Status reconciliation", "22", "42", ".60"),
    _weekly("Report preparation", "12", "46", ".65"),
    _weekly("Document/status lookup", "16", "40", ".45"),
    _weekly("Correction administration", "10", "41", ".35"),
    _weekly("Management reporting", "7", "58", ".50"),
    GovernmentBurden("Avoidable administrative rework", D("55"), D("240"), D(".30"), "incidents"),
)
BASELINE_ENGINEERING = GovernmentEngineering(
    D("28"), D("32"), D("70"), D("40"), D("40"), D("46"), D("38"),
    D("44"), D("24"), D("18"), D("64"), D("28"), D("50"), D("185"))
BASELINE_PROCUREMENT = ProcurementWork(
    D("18"), D("16"), D("20"), D("16"), D("14"), D("12"), D("22"),
    D("28"), D("18"), D("12"), D("10"), D("6"))
BASELINE_SUPPORT = GovernmentSupport(D("110"), D("95"), D("1800"), D("1200"),
    D("1600"), D("1800"), D("800"), D("600"), D("1200"), D("600"), D("1000"))
BASELINE_ALTERNATIVE = AlternativeEconomics(D("35000"), D("32000"), D("18000"), D("155000"), D("18000"))


def _build(*, burdens=BASELINE_BURDENS, engineering=BASELINE_ENGINEERING,
        procurement=BASELINE_PROCUREMENT, support=BASELINE_SUPPORT,
        alternative=BASELINE_ALTERNATIVE, price=D("78000"), fee=D("24000"),
        custom_risk=D("20000"), procurement_level=Level.HIGH,
        cycle=D("9"), accessibility=Level.LOW, close=Level.HIGH,
        feasibility=Feasibility.FEASIBLE, permission=Level.HIGH) -> LocalGovernmentCase:
    _nonnegative((price, fee, custom_risk, cycle))
    total = sum((x.annual_burden for x in burdens), D("0"))
    recovery = sum((x.recoverable for x in burdens), D("0"))
    customer = CustomerEconomics(total, recovery, price, fee)
    finding = (AlternativeFinding.ADEQUATE_BUY
        if alternative_first_year_effect(alternative) < custom_first_year_effect(customer, custom_risk)
        else AlternativeFinding.CUSTOM_JUSTIFIED)
    delivery = DeliveryEconomics(engineering.reusable_core,
        engineering.core_hours - engineering.reusable_core, D("95"), engineering.testing,
        engineering.deployment_constraints, engineering.rework_reserve, D("3500"),
        support.engineering_hours, support.hourly_cost,
        support.annual_cost - support.engineering_hours * support.hourly_cost)
    solutions = SolutionsEconomics(procurement.prospecting, procurement.discovery,
        procurement.stakeholder_meetings + procurement.technical_validation
        + procurement.security_documentation + procurement.accessibility_review
        + procurement.proposal_rfp + procurement.procurement_support
        + procurement.contract_coordination + procurement.implementation_planning,
        procurement.acceptance + procurement.other_coordination, D("80"))
    scenario = OpportunityScenario("James River County Permitting Department", True,
        customer, delivery, solutions,
        SalesCharacteristics(procurement_level, cycle, accessibility, close),
        TechnicalCharacteristics(5, Level.HIGH, Level.MODERATE, feasibility,
            Level.HIGH, Level.HIGH, permission),
        BuildVsBuy(finding, tuple(AlternativeType),
            "Compared incumbent modules and services, government case-management SaaS, configuration, approved low-code, process/reporting improvements, narrow custom integration, full replacement, and doing nothing."))
    return LocalGovernmentCase(burdens, engineering, procurement, support,
        alternative, custom_risk, scenario)


def baseline_case(): return _build()

def cooperative_pilot_case():
    procurement = ProcurementWork(D("4"), D("8"), D("6"), D("8"), D("4"),
        D("3"), D("4"), D("5"), D("3"), D("5"), D("4"), D("2"))
    return _build(procurement=procurement, procurement_level=Level.LOW, cycle=D("2"),
        accessibility=Level.HIGH, close=Level.LOW, permission=Level.LOW)

def formal_rfp_case():
    p = replace(BASELINE_PROCUREMENT, stakeholder_meetings=D("38"), proposal_rfp=D("70"),
        procurement_support=D("50"), contract_coordination=D("30"), other_coordination=D("18"))
    return _build(procurement=p, cycle=D("12"))

def high_contract_value_case(): return _build(price=D("80000"))

def closed_legacy_integration_case():
    return _build(feasibility=Feasibility.INFEASIBLE, permission=Level.HIGH)

def existing_vendor_module_case():
    return _build(alternative=AlternativeEconomics(D("18000"), D("24000"),
        D("9000"), D("60000"), D("5000")))

def reusable_technical_hard_sales_case():
    return _build(engineering=replace(BASELINE_ENGINEERING, reusable_core=D("300")))


@dataclass(frozen=True)
class CaseSevenNineComparison:
    construction_recoverable: D; government_recoverable: D
    construction_solutions_hours: D; government_solutions_hours: D
    construction_sales_cycle_months: D; government_sales_cycle_months: D
    construction_verdict: str; government_verdict: str


def case_seven_vs_nine():
    from .analysis import analyze
    from .construction_trades import baseline_case as construction
    from .economics import solutions_hours
    c7, c9 = construction(), baseline_case()
    return CaseSevenNineComparison(c7.recoverable_value, c9.recoverable_value,
        solutions_hours(c7.scenario.solutions), solutions_hours(c9.scenario.solutions),
        c7.scenario.sales.sales_cycle_months, c9.scenario.sales.sales_cycle_months,
        analyze(c7.scenario).verdict.value, analyze(c9.scenario).verdict.value)
