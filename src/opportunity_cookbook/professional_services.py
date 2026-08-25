"""Case 8: fictional professional-services assumptions, not industry benchmarks."""

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
class AdministrativeBurden:
    """A measurable activity burden, expressed as units x cost per unit."""

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
class ServicesEngineering:
    technical_discovery: D
    crm_integration: D
    proposal_project_handoff: D
    project_management_integration: D
    time_tracking_integration: D
    accounting_billing_integration: D
    identity_normalization: D
    utilization_reporting: D
    validation_error_handling: D
    testing: D
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
        return sum((self.technical_discovery, self.crm_integration,
                    self.proposal_project_handoff, self.project_management_integration,
                    self.time_tracking_integration, self.accounting_billing_integration,
                    self.identity_normalization, self.utilization_reporting,
                    self.validation_error_handling, self.documentation), D("0"))

    @property
    def total_hours(self) -> D:
        return self.core_hours + self.testing + self.deployment + self.rework_reserve


@dataclass(frozen=True)
class ServicesSolutionsWork:
    prospecting_sales: D
    discovery: D
    workflow_mapping: D
    system_inventory: D
    configuration_vs_code: D
    technical_validation: D
    solution_design: D
    proposal_scoping: D
    coordination: D
    acceptance: D

    def __post_init__(self) -> None:
        _nonnegative(vars(self).values())

    @property
    def total_hours(self) -> D:
        return sum(vars(self).values(), D("0"))


@dataclass(frozen=True)
class ServicesSupport:
    maintenance_engineering_hours: D
    hourly_cost: D
    hosting_monitoring: D
    api_auth_mapping_changes: D
    billing_rule_changes: D
    customer_support_and_bugs: D

    def __post_init__(self) -> None:
        _nonnegative(vars(self).values())

    @property
    def annual_cost(self) -> D:
        return (self.maintenance_engineering_hours * self.hourly_cost
                + self.hosting_monitoring + self.api_auth_mapping_changes
                + self.billing_rule_changes + self.customer_support_and_bugs)


@dataclass(frozen=True)
class ProfessionalServicesCase:
    burdens: tuple[AdministrativeBurden, ...]
    engineering: ServicesEngineering
    solutions_work: ServicesSolutionsWork
    support: ServicesSupport
    alternative: AlternativeEconomics
    custom_risk_allowance: D
    speculative_utilization_upside: D
    scenario: OpportunityScenario

    @property
    def total_burden(self) -> D:
        return sum((item.annual_burden for item in self.burdens), D("0"))

    @property
    def burden_recovery(self) -> D:
        return sum((item.recoverable for item in self.burdens), D("0"))

    @property
    def recoverable_value(self) -> D:
        return self.burden_recovery + self.speculative_utilization_upside


def _weekly(name, hours, cost, improvement):
    return AdministrativeBurden(name, D(hours) * D("52"), D(cost), D(improvement))


BASELINE_BURDENS = (
    _weekly("Sales-to-project handoff", "5", "42", ".60"),
    _weekly("Project setup administration", "6", "38", ".50"),
    _weekly("Time/billing reconciliation", "12", "42", ".55"),
    _weekly("Utilization reporting", "6", "48", ".60"),
    _weekly("Management reporting", "7", "58", ".45"),
    _weekly("Resource-planning reconciliation", "5", "50", ".35"),
    _weekly("Invoice-preparation administration", "8", "40", ".50"),
    AdministrativeBurden("Error/rework", D("40"), D("180"), D(".30"), "incidents"),
)
BASELINE_ENGINEERING = ServicesEngineering(
    D("24"), D("42"), D("32"), D("42"), D("48"), D("54"), D("34"),
    D("38"), D("46"), D("52"), D("14"), D("18"), D("34"), D("155"))
BASELINE_SOLUTIONS = ServicesSolutionsWork(
    D("10"), D("10"), D("12"), D("10"), D("14"), D("10"), D("8"), D("6"), D("5"), D("3"))
BASELINE_SUPPORT = ServicesSupport(D("72"), D("85"), D("1400"), D("1400"), D("900"), D("900"))
BASELINE_ALTERNATIVE = AlternativeEconomics(D("14000"), D("18000"), D("7000"), D("32000"), D("3000"))


def _build(*, burdens=BASELINE_BURDENS, engineering=BASELINE_ENGINEERING,
           solutions=BASELINE_SOLUTIONS, support=BASELINE_SUPPORT,
           alternative=BASELINE_ALTERNATIVE, price=D("52000"), fee=D("14000"),
           custom_risk=D("12000"), speculative_upside=D("0")) -> ProfessionalServicesCase:
    _nonnegative((price, fee, custom_risk, speculative_upside))
    total = sum((item.annual_burden for item in burdens), D("0"))
    burden_recovery = sum((item.recoverable for item in burdens), D("0"))
    customer = CustomerEconomics(total + speculative_upside,
        burden_recovery + speculative_upside, price, fee)
    finding = (AlternativeFinding.ADEQUATE_BUY
        if alternative_first_year_effect(alternative) < custom_first_year_effect(customer, custom_risk)
        else AlternativeFinding.CUSTOM_JUSTIFIED)
    delivery = DeliveryEconomics(engineering.reusable_core,
        engineering.core_hours - engineering.reusable_core, D("85"), engineering.testing,
        engineering.deployment, engineering.rework_reserve, D("2000"),
        support.maintenance_engineering_hours, support.hourly_cost,
        support.hosting_monitoring + support.api_auth_mapping_changes
        + support.billing_rule_changes + support.customer_support_and_bugs)
    scenario = OpportunityScenario("James River Advisory", True, customer, delivery,
        SolutionsEconomics(solutions.prospecting_sales,
            solutions.discovery + solutions.workflow_mapping + solutions.system_inventory,
            solutions.configuration_vs_code + solutions.technical_validation
            + solutions.solution_design + solutions.proposal_scoping,
            solutions.coordination + solutions.acceptance, D("70")),
        SalesCharacteristics(Level.MODERATE, D("4"), Level.HIGH, Level.MODERATE),
        TechnicalCharacteristics(6, Level.MODERATE, Level.HIGH, Feasibility.FEASIBLE,
            Level.MODERATE, Level.LOW, Level.MODERATE),
        BuildVsBuy(finding, tuple(AlternativeType),
            "Compared CRM and project configuration, PSA, time/billing, accounting integrations, BI, automation tooling, better spreadsheets/process, narrow custom integration, and doing nothing. The central test is whether existing tools are merely under-configured."))
    return ProfessionalServicesCase(burdens, engineering, solutions, support,
        alternative, custom_risk, speculative_upside, scenario)


def baseline_case(): return _build()


def poorly_configured_tools_case():
    return _build(alternative=AlternativeEconomics(D("9000"), D("13000"), D("5000"), D("18000"), D("1500")))


def genuine_cross_system_gap_case():
    burdens = tuple(replace(x, annual_units=x.annual_units * D("1.45")) for x in BASELINE_BURDENS)
    return _build(burdens=burdens,
        alternative=AlternativeEconomics(D("22000"), D("22000"), D("10000"), D("105000"), D("9000")))


def high_administrative_burden_case():
    burdens = tuple(replace(x, annual_units=x.annual_units * D("1.8")) for x in BASELINE_BURDENS)
    return _build(burdens=burdens, alternative=replace(BASELINE_ALTERNATIVE, residual_annual_burden=D("200000")))


def low_administrative_burden_case():
    return _build(burdens=tuple(replace(x, annual_units=x.annual_units * D(".35")) for x in BASELINE_BURDENS))


def unique_billing_workflow_case():
    burdens = tuple(replace(x, annual_units=x.annual_units * D("2.1")) for x in BASELINE_BURDENS)
    engineering = replace(BASELINE_ENGINEERING, accounting_billing_integration=D("100"),
        utilization_reporting=D("70"), reusable_core=D("120"), testing=D("66"), rework_reserve=D("45"))
    return _build(burdens=burdens, engineering=engineering, price=D("76000"), fee=D("18000"),
        alternative=AlternativeEconomics(D("30000"), D("25000"), D("12000"), D("160000"), D("12000")))


def strong_repeatability_strong_saas_case():
    engineering = replace(BASELINE_ENGINEERING, reusable_core=D("230"))
    return _build(engineering=engineering,
        alternative=AlternativeEconomics(D("8000"), D("15000"), D("5000"), D("16000"), D("1000")))


def speculative_utilization_upside_case():
    # An uncertain causal hypothesis, deliberately excluded from baseline recovery.
    return _build(speculative_upside=D("18000"))


@dataclass(frozen=True)
class CaseSevenEightComparison:
    construction_recoverable: D
    professional_services_recoverable: D
    construction_alternative_effect: D
    professional_services_alternative_effect: D
    construction_verdict: str
    professional_services_verdict: str


def case_seven_vs_eight() -> CaseSevenEightComparison:
    from .analysis import analyze
    from .construction_trades import baseline_case as construction
    c7, c8 = construction(), baseline_case()
    return CaseSevenEightComparison(c7.recoverable_value, c8.recoverable_value,
        alternative_first_year_effect(c7.alternative), alternative_first_year_effect(c8.alternative),
        analyze(c7.scenario).verdict.value, analyze(c8.scenario).verdict.value)
