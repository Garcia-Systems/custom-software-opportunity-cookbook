"""Case 11: fictional administrative healthcare opportunity economics only."""

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
class AdministrativeBurden:
    name: str
    annual_units: D
    cost_per_unit: D
    improvement_rate: D
    basis: str = "administrative labor hours"

    def __post_init__(self) -> None:
        _nonnegative((self.annual_units, self.cost_per_unit))
        if not D("0") <= self.improvement_rate <= D("1"):
            raise ValueError("improvement_rate must be between 0 and 1")

    @property
    def annual_burden(self) -> D: return self.annual_units * self.cost_per_unit

    @property
    def recoverable(self) -> D: return self.annual_burden * self.improvement_rate


@dataclass(frozen=True)
class HealthcareEngineering:
    technical_discovery: D; integration_validation: D; adapters: D
    data_minimization_design: D; normalization: D; validation_reconciliation: D
    audit_logging: D; error_handling: D; security_privacy: D; testing: D
    deployment_monitoring: D; documentation: D; acceptance: D
    rework_reserve: D; integration_uncertainty_reserve: D; reusable_core: D

    def __post_init__(self) -> None:
        _nonnegative(vars(self).values())
        if self.reusable_core > self.base_engineering_hours:
            raise ValueError("reusable_core cannot exceed base engineering hours")

    @property
    def base_engineering_hours(self) -> D:
        return sum((self.technical_discovery, self.adapters,
            self.data_minimization_design, self.normalization, self.audit_logging,
            self.error_handling, self.documentation, self.acceptance), D("0"))

    @property
    def total_hours(self) -> D:
        return sum((self.base_engineering_hours, self.integration_validation,
            self.security_privacy, self.validation_reconciliation, self.testing,
            self.deployment_monitoring, self.rework_reserve,
            self.integration_uncertainty_reserve), D("0"))


@dataclass(frozen=True)
class HealthcareSolutionsWork:
    prospecting: D; discovery: D; workflow_mapping: D; stakeholder_interviews: D
    security_privacy_discovery: D; vendor_integration_validation: D
    solution_design: D; proposal_scoping: D; procurement_security_coordination: D
    acceptance_planning: D

    def __post_init__(self) -> None: _nonnegative(vars(self).values())

    @property
    def total_hours(self) -> D: return sum(vars(self).values(), D("0"))


@dataclass(frozen=True)
class HealthcareSupport:
    engineering_hours: D; hourly_cost: D; hosting: D; monitoring: D
    failed_integrations: D; interface_changes: D; credential_changes: D
    security_updates: D; incident_response: D; mapping_changes: D
    data_quality: D; customer_support: D; periodic_validation: D

    def __post_init__(self) -> None: _nonnegative(vars(self).values())

    @property
    def annual_cost(self) -> D:
        return self.engineering_hours * self.hourly_cost + sum((self.hosting,
            self.monitoring, self.failed_integrations, self.interface_changes,
            self.credential_changes, self.security_updates, self.incident_response,
            self.mapping_changes, self.data_quality, self.customer_support,
            self.periodic_validation), D("0"))


@dataclass(frozen=True)
class HealthcareCase:
    burdens: tuple[AdministrativeBurden, ...]
    engineering: HealthcareEngineering
    solutions_work: HealthcareSolutionsWork
    support: HealthcareSupport
    alternative: AlternativeEconomics
    custom_risk_allowance: D
    scope: str
    scenario: OpportunityScenario

    @property
    def total_burden(self) -> D:
        return sum((x.annual_burden for x in self.burdens), D("0"))

    @property
    def recoverable_value(self) -> D:
        return sum((x.recoverable for x in self.burdens), D("0"))


def _weekly(name, hours, cost, rate):
    return AdministrativeBurden(name, D(hours) * D("52"), D(cost), D(rate))


BASELINE_BURDENS = (
    _weekly("Administrative reconciliation", "30", "42", ".55"),
    _weekly("Duplicate administrative entry", "18", "38", ".45"),
    _weekly("Billing-status reconciliation", "24", "46", ".50"),
    _weekly("Management reporting", "16", "55", ".60"),
    _weekly("Exception-list preparation", "14", "41", ".55"),
    _weekly("Cross-location reporting", "12", "49", ".50"),
    AdministrativeBurden("Avoidable administrative rework", D("180"), D("280"), D(".30"),
        "fictional administrative incidents; excludes clinical work and revenue"),
)
BASELINE_ENGINEERING = HealthcareEngineering(D("32"), D("72"), D("150"), D("32"),
    D("58"), D("86"), D("46"), D("38"), D("82"), D("110"), D("34"),
    D("20"), D("24"), D("72"), D("90"), D("190"))
BASELINE_SOLUTIONS = HealthcareSolutionsWork(D("12"), D("18"), D("20"), D("18"),
    D("24"), D("32"), D("18"), D("14"), D("26"), D("14"))
BASELINE_SUPPORT = HealthcareSupport(D("150"), D("105"), D("2400"), D("2200"),
    D("1800"), D("2600"), D("900"), D("1800"), D("1600"), D("1200"),
    D("1500"), D("1200"), D("1400"))
BASELINE_ALTERNATIVE = AlternativeEconomics(D("65000"), D("52000"), D("24000"),
    D("205000"), D("30000"))


def _build(*, burdens=BASELINE_BURDENS, engineering=BASELINE_ENGINEERING,
        solutions_work=BASELINE_SOLUTIONS, support=BASELINE_SUPPORT,
        alternative=BASELINE_ALTERNATIVE, price=D("126000"), fee=D("38000"),
        custom_risk=D("38000"), procurement=Level.HIGH, cycle=D("8"),
        accessibility=Level.HIGH, close=Level.HIGH, integration=Level.HIGH,
        availability=Level.MODERATE, permission=Level.HIGH,
        feasibility=Feasibility.FEASIBLE,
        scope="approved administrative imports/APIs; no clinical decision-making"):
    _nonnegative((price, fee, custom_risk, cycle))
    total = sum((x.annual_burden for x in burdens), D("0"))
    recovery = sum((x.recoverable for x in burdens), D("0"))
    customer = CustomerEconomics(total, recovery, price, fee)
    custom_effect = custom_first_year_effect(customer, custom_risk)
    finding = (AlternativeFinding.UNKNOWN if feasibility is Feasibility.UNKNOWN else
        AlternativeFinding.ADEQUATE_BUY
        if alternative_first_year_effect(alternative) < custom_effect
        else AlternativeFinding.CUSTOM_JUSTIFIED)
    delivery = DeliveryEconomics(engineering.reusable_core,
        engineering.base_engineering_hours - engineering.reusable_core
            + engineering.integration_validation + engineering.security_privacy,
        D("105"), engineering.validation_reconciliation + engineering.testing,
        engineering.deployment_monitoring, engineering.rework_reserve, D("6500"),
        support.engineering_hours, support.hourly_cost,
        support.annual_cost - support.engineering_hours * support.hourly_cost,
        uncertainty_reserve_hours=engineering.integration_uncertainty_reserve,
    )
    w = solutions_work
    solutions = SolutionsEconomics(w.prospecting,
        w.discovery + w.workflow_mapping + w.stakeholder_interviews,
        w.security_privacy_discovery + w.vendor_integration_validation
            + w.solution_design + w.proposal_scoping,
        w.procurement_security_coordination + w.acceptance_planning, D("85"))
    scenario = OpportunityScenario("James River Specialty Clinic Group", True,
        customer, delivery, solutions,
        SalesCharacteristics(procurement, cycle, accessibility, close),
        TechnicalCharacteristics(6, integration, availability, feasibility,
            Level.HIGH, Level.HIGH, permission),
        BuildVsBuy(finding, tuple(AlternativeType),
            "Compared existing system reporting, vendor modules/interfaces, practice-management and revenue-cycle reporting, approved BI, vendor professional services, narrow custom integration, full replacement, and doing nothing."))
    return HealthcareCase(burdens, engineering, solutions_work, support,
        alternative, custom_risk, scope, scenario)


def baseline_case(): return _build()


def vendor_supported_interfaces_case():
    e = replace(BASELINE_ENGINEERING, integration_validation=D("28"), adapters=D("85"),
        validation_reconciliation=D("58"), testing=D("72"), rework_reserve=D("32"),
        integration_uncertainty_reserve=D("20"))
    support = replace(BASELINE_SUPPORT, engineering_hours=D("95"),
        failed_integrations=D("800"), interface_changes=D("900"))
    return _build(engineering=e, support=support, price=D("112000"),
        procurement=Level.MODERATE, cycle=D("5"), close=Level.MODERATE,
        permission=Level.LOW, availability=Level.HIGH, integration=Level.MODERATE)


def difficult_proprietary_integration_case():
    e = replace(BASELINE_ENGINEERING, integration_validation=D("130"), adapters=D("250"),
        validation_reconciliation=D("150"), testing=D("175"), rework_reserve=D("130"),
        integration_uncertainty_reserve=D("190"))
    support = replace(BASELINE_SUPPORT, engineering_hours=D("240"),
        failed_integrations=D("4500"), interface_changes=D("6000"))
    return _build(engineering=e, support=support)


def high_customer_value_case():
    burdens = tuple(replace(x, annual_units=x.annual_units * D("1.8")) for x in BASELINE_BURDENS)
    # Value changes; delivery and the relative capability of alternatives do not.
    alternative = replace(BASELINE_ALTERNATIVE,
        residual_annual_burden=BASELINE_ALTERNATIVE.residual_annual_burden * D("1.8"))
    return _build(burdens=burdens, alternative=alternative)


def vendor_supported_product_case():
    return _build(alternative=AlternativeEconomics(D("32000"), D("36000"),
        D("12000"), D("72000"), D("8000")))


def underpriced_support_case():
    support = replace(BASELINE_SUPPORT, engineering_hours=D("260"), monitoring=D("5000"),
        failed_integrations=D("5000"), incident_response=D("4500"))
    return _build(support=support, procurement=Level.MODERATE, cycle=D("5"),
        close=Level.MODERATE)


def narrow_read_only_case():
    burdens = tuple(replace(x, improvement_rate=x.improvement_rate * D(".55"))
        for x in BASELINE_BURDENS)
    e = HealthcareEngineering(D("20"), D("18"), D("48"), D("18"), D("34"),
        D("32"), D("18"), D("16"), D("28"), D("42"), D("16"), D("12"),
        D("12"), D("18"), D("12"), D("100"))
    support = replace(BASELINE_SUPPORT, engineering_hours=D("60"), hosting=D("900"),
        monitoring=D("800"), failed_integrations=D("400"), interface_changes=D("500"),
        incident_response=D("300"), periodic_validation=D("500"))
    return _build(burdens=burdens, engineering=e, support=support, price=D("62000"),
        fee=D("18000"), custom_risk=D("9000"), procurement=Level.MODERATE,
        cycle=D("4"), close=Level.MODERATE, integration=Level.LOW,
        availability=Level.HIGH, permission=Level.LOW,
        scope="stable approved read-only administrative exports; minimum fields")


def high_reuse_high_validation_case():
    return _build(engineering=replace(BASELINE_ENGINEERING, reusable_core=D("300"),
        validation_reconciliation=D("150"), testing=D("160")))


def unresolved_access_case():
    return _build(feasibility=Feasibility.UNKNOWN, availability=Level.LOW)


@dataclass(frozen=True)
class CaseSevenElevenComparison:
    construction_value: D; healthcare_value: D
    construction_hours: D; healthcare_hours: D
    construction_integration: str; healthcare_integration: str
    construction_support_cost: D; healthcare_support_cost: D
    construction_verdict: str; healthcare_verdict: str


def case_seven_vs_eleven():
    from .analysis import analyze
    from .construction_trades import baseline_case as construction
    from .economics import annual_support_cost, implementation_delivery_cost
    c, h = construction(), baseline_case()
    return CaseSevenElevenComparison(c.scenario.customer.recoverable_value,
        h.recoverable_value,
        implementation_delivery_cost(c.scenario.delivery) / c.scenario.delivery.engineering_hourly_cost,
        h.engineering.total_hours, c.scenario.technical.integration_complexity.value,
        h.scenario.technical.integration_complexity.value,
        annual_support_cost(c.scenario.delivery), annual_support_cost(h.scenario.delivery),
        analyze(c.scenario).verdict.value, analyze(h.scenario).verdict.value)


CASE_NINE_TEN_ELEVEN_PROGRESSION = (
    "Case 9: the project may be good, but procurement makes the customer unattractive.",
    "Case 10: the department may want the project, but authority and governance block execution.",
    "Case 11: the customer may want and authorize the project, but delivery and support complexity can break the economics.",
)
