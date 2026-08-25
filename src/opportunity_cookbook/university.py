"""Case 10: fictional university-department opportunity assumptions."""

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
class UniversityBurden:
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
class AuthorityMap:
    problem_owner: str
    budget_owner: str
    system_owner: str
    data_owner: str
    security_approver: str
    integration_approver: str
    procurement: str
    end_users: str
    buyer_authority: Level
    system_control: Level
    integration_approval_difficulty: Level
    integration_approved: bool
    unauthorized_access_allowed: bool = False

    def __post_init__(self) -> None:
        if self.unauthorized_access_allowed:
            raise ValueError("unauthorized data access is never an acceptable assumption")


@dataclass(frozen=True)
class UniversityEngineering:
    technical_discovery: D; access_validation: D; export_api_integration: D
    identity_mapping: D; program_normalization: D; finance_mapping: D
    validation: D; audit_logging: D; security: D; accessibility: D; testing: D
    deployment_constraints: D; documentation: D; acceptance: D; rework_reserve: D
    reusable_core: D

    def __post_init__(self) -> None:
        _nonnegative(vars(self).values())
        if self.reusable_core > self.core_hours:
            raise ValueError("reusable_core cannot exceed core hours")

    @property
    def security_access_hours(self) -> D:
        return self.access_validation + self.security + self.accessibility

    @property
    def core_hours(self) -> D:
        return sum((self.technical_discovery, self.access_validation,
            self.export_api_integration, self.identity_mapping,
            self.program_normalization, self.finance_mapping, self.validation,
            self.audit_logging, self.security, self.accessibility,
            self.documentation, self.acceptance), D("0"))

    @property
    def total_hours(self) -> D:
        return self.core_hours + self.testing + self.deployment_constraints + self.rework_reserve


@dataclass(frozen=True)
class GovernanceWork:
    prospecting: D; department_discovery: D; stakeholder_mapping: D
    central_it_coordination: D; system_owner_meetings: D; access_validation: D
    security_documentation: D; procurement_support: D; proposal_scoping: D
    solution_design: D; acceptance: D; other_coordination: D

    def __post_init__(self) -> None: _nonnegative(vars(self).values())

    @property
    def total_hours(self) -> D: return sum(vars(self).values(), D("0"))


@dataclass(frozen=True)
class UniversitySupport:
    engineering_hours: D; hourly_cost: D; hosting: D; monitoring: D
    export_api_changes: D; identity_changes: D; security_updates: D
    accessibility_fixes: D; reporting_changes: D; user_support: D
    documentation: D; change_control: D

    def __post_init__(self) -> None: _nonnegative(vars(self).values())

    @property
    def annual_cost(self) -> D:
        return self.engineering_hours * self.hourly_cost + sum((self.hosting,
            self.monitoring, self.export_api_changes, self.identity_changes,
            self.security_updates, self.accessibility_fixes, self.reporting_changes,
            self.user_support, self.documentation, self.change_control), D("0"))


@dataclass(frozen=True)
class UniversityCase:
    burdens: tuple[UniversityBurden, ...]
    authority: AuthorityMap
    engineering: UniversityEngineering
    governance: GovernanceWork
    support: UniversitySupport
    alternative: AlternativeEconomics
    custom_risk_allowance: D
    scope: str
    scenario: OpportunityScenario

    @property
    def total_burden(self) -> D:
        return sum((item.annual_burden for item in self.burdens), D("0"))

    @property
    def recoverable_value(self) -> D:
        return sum((item.recoverable for item in self.burdens), D("0"))


def _weekly(name, hours, cost, rate):
    return UniversityBurden(name, D(hours) * D("52"), D(cost), D(rate))


BASELINE_BURDENS = (
    _weekly("Duplicate entry", "14", "36", ".55"),
    _weekly("Registration reconciliation", "18", "40", ".60"),
    _weekly("Program/course reporting", "12", "44", ".65"),
    _weekly("Instructor coordination administration", "10", "38", ".35"),
    _weekly("Finance reconciliation", "12", "46", ".55"),
    _weekly("Status lookup", "15", "37", ".45"),
    _weekly("Management reporting", "7", "55", ".60"),
    UniversityBurden("Avoidable administrative rework", D("50"), D("220"), D(".30"), "incidents"),
)
BASELINE_AUTHORITY = AuthorityMap("Continuing Education Department",
    "Department / school administration", "Central IT / application owners",
    "James River University", "Central security", "Central IT and system owners",
    "Institutional purchasing", "Department staff", Level.MODERATE, Level.LOW,
    Level.HIGH, True)
BASELINE_ENGINEERING = UniversityEngineering(D("26"), D("34"), D("66"), D("38"),
    D("42"), D("36"), D("30"), D("28"), D("38"), D("20"), D("58"), D("30"),
    D("20"), D("14"), D("48"), D("178"))
BASELINE_GOVERNANCE = GovernanceWork(D("16"), D("18"), D("16"), D("28"), D("20"),
    D("18"), D("18"), D("26"), D("16"), D("14"), D("10"), D("8"))
BASELINE_SUPPORT = UniversitySupport(D("105"), D("95"), D("1800"), D("1200"),
    D("1800"), D("900"), D("1400"), D("700"), D("900"), D("800"), D("500"), D("900"))
BASELINE_ALTERNATIVE = AlternativeEconomics(D("36000"), D("30000"), D("18000"), D("158000"), D("15000"))


def _build(*, burdens=BASELINE_BURDENS, authority=BASELINE_AUTHORITY,
        engineering=BASELINE_ENGINEERING, governance=BASELINE_GOVERNANCE,
        support=BASELINE_SUPPORT, alternative=BASELINE_ALTERNATIVE,
        price=D("78000"), fee=D("24000"), custom_risk=D("22000"),
        procurement=Level.HIGH, cycle=D("10"), accessibility=Level.LOW,
        close=Level.HIGH, permission=Level.HIGH, scope="approved exports and APIs"):
    _nonnegative((price, fee, custom_risk, cycle))
    total = sum((x.annual_burden for x in burdens), D("0"))
    recovery = sum((x.recoverable for x in burdens), D("0"))
    customer = CustomerEconomics(total, recovery, price, fee)
    finding = (AlternativeFinding.ADEQUATE_BUY
        if alternative_first_year_effect(alternative) < custom_first_year_effect(customer, custom_risk)
        else AlternativeFinding.CUSTOM_JUSTIFIED)
    delivery = DeliveryEconomics(engineering.reusable_core,
        engineering.core_hours - engineering.reusable_core, D("95"), engineering.testing,
        engineering.deployment_constraints, engineering.rework_reserve, D("4000"),
        support.engineering_hours, support.hourly_cost,
        support.annual_cost - support.engineering_hours * support.hourly_cost)
    solutions = SolutionsEconomics(governance.prospecting, governance.department_discovery,
        governance.stakeholder_mapping + governance.central_it_coordination
        + governance.system_owner_meetings + governance.access_validation
        + governance.security_documentation + governance.procurement_support
        + governance.proposal_scoping + governance.solution_design,
        governance.acceptance + governance.other_coordination, D("80"))
    scenario = OpportunityScenario("James River University — Continuing Education", True,
        customer, delivery, solutions, SalesCharacteristics(procurement, cycle, accessibility, close),
        TechnicalCharacteristics(6, Level.HIGH, Level.MODERATE, Feasibility.FEASIBLE,
            Level.HIGH, Level.HIGH, permission), BuildVsBuy(finding, tuple(AlternativeType),
            "Compared enterprise reporting, vendor modules, university BI, approved low-code, process improvement, better spreadsheets, narrow custom integration, full replacement, and doing nothing."))
    return UniversityCase(burdens, authority, engineering, governance, support,
        alternative, custom_risk, scope, scenario)


def baseline_case(): return _build()


def centrally_sponsored_case():
    authority = replace(BASELINE_AUTHORITY, buyer_authority=Level.HIGH,
        system_control=Level.HIGH, integration_approval_difficulty=Level.LOW)
    work = GovernanceWork(D("5"), D("8"), D("5"), D("8"), D("5"), D("5"),
        D("5"), D("4"), D("4"), D("5"), D("4"), D("2"))
    return _build(authority=authority, governance=work, procurement=Level.LOW,
        cycle=D("3"), accessibility=Level.HIGH, close=Level.LOW, permission=Level.LOW)


def department_only_champion_case():
    authority = replace(BASELINE_AUTHORITY, buyer_authority=Level.LOW,
        integration_approved=False)
    work = replace(BASELINE_GOVERNANCE, central_it_coordination=D("55"),
        system_owner_meetings=D("45"), access_validation=D("42"),
        procurement_support=D("40"), other_coordination=D("25"))
    return _build(authority=authority, governance=work, cycle=D("14"))


def approved_exports_only_case():
    authority = replace(BASELINE_AUTHORITY, integration_approval_difficulty=Level.LOW,
        integration_approved=True)
    engineering = UniversityEngineering(D("18"), D("16"), D("32"), D("18"),
        D("30"), D("24"), D("20"), D("18"), D("16"), D("12"), D("34"), D("14"),
        D("12"), D("8"), D("20"), D("105"))
    work = GovernanceWork(D("6"), D("8"), D("6"), D("8"), D("5"), D("5"),
        D("5"), D("5"), D("5"), D("6"), D("4"), D("2"))
    support = UniversitySupport(D("65"), D("95"), D("900"), D("700"), D("900"),
        D("300"), D("700"), D("400"), D("600"), D("500"), D("300"), D("500"))
    return _build(authority=authority, engineering=engineering, governance=work,
        support=support, price=D("52000"), fee=D("18000"), procurement=Level.MODERATE, cycle=D("5"),
        accessibility=Level.HIGH, close=Level.MODERATE, permission=Level.LOW,
        scope="stable approved read-only exports; no write access")


def existing_bi_tool_case():
    return _build(alternative=AlternativeEconomics(D("12000"), D("10000"),
        D("8000"), D("65000"), D("3000")))


def higher_contract_value_case(): return _build(price=D("81000"))


def high_reuse_unique_governance_case():
    return _build(engineering=replace(BASELINE_ENGINEERING, reusable_core=D("300")))


@dataclass(frozen=True)
class CaseNineTenComparison:
    government_solutions_hours: D; university_solutions_hours: D
    government_sales_cycle_months: D; university_sales_cycle_months: D
    government_permission_difficulty: str; university_permission_difficulty: str
    government_verdict: str; university_verdict: str


def case_nine_vs_ten():
    from .analysis import analyze
    from .economics import solutions_hours
    from .local_government import baseline_case as government
    g, u = government(), baseline_case()
    return CaseNineTenComparison(solutions_hours(g.scenario.solutions),
        solutions_hours(u.scenario.solutions), g.scenario.sales.sales_cycle_months,
        u.scenario.sales.sales_cycle_months,
        g.scenario.technical.integration_permission_difficulty.value,
        u.scenario.technical.integration_permission_difficulty.value,
        analyze(g.scenario).verdict.value, analyze(u.scenario).verdict.value)
