"""Immutable assumptions for an opportunity model."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class Level(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class Feasibility(Enum):
    UNKNOWN = "unresolved"
    FEASIBLE = "feasible"
    INFEASIBLE = "infeasible"


class AlternativeFinding(Enum):
    UNKNOWN = "not adequately evaluated"
    ADEQUATE_BUY = "existing buy/configure option is adequate and preferable"
    CUSTOM_JUSTIFIED = "alternatives are incomplete; custom is economically preferable"


class AlternativeType(Enum):
    EXISTING_SAAS = "existing SaaS"
    SAAS_CONFIGURATION = "SaaS configuration"
    AUTOMATION_TOOLING = "automation tooling"
    SPREADSHEET_PROCESS = "spreadsheet/process change"
    CUSTOM_INTEGRATION = "custom integration"
    CUSTOM_APPLICATION = "custom application"
    DO_NOTHING = "doing nothing"


def _nonnegative(value: Decimal | int, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} cannot be negative")


@dataclass(frozen=True)
class CustomerEconomics:
    current_state_annual_burden: Decimal | None
    recoverable_value: Decimal | None
    implementation_price: Decimal
    recurring_annual_fee: Decimal

    def __post_init__(self) -> None:
        for name in ("current_state_annual_burden", "recoverable_value"):
            value = getattr(self, name)
            if value is not None:
                _nonnegative(value, name)
        _nonnegative(self.implementation_price, "implementation_price")
        _nonnegative(self.recurring_annual_fee, "recurring_annual_fee")
        if (self.current_state_annual_burden is not None
                and self.recoverable_value is not None
                and self.recoverable_value > self.current_state_annual_burden):
            raise ValueError("recoverable_value cannot exceed current-state burden")


@dataclass(frozen=True)
class DeliveryEconomics:
    reusable_engineering_hours: Decimal
    customer_specific_engineering_hours: Decimal
    engineering_hourly_cost: Decimal
    qa_hours: Decimal = Decimal("0")
    deployment_hours: Decimal = Decimal("0")
    rework_reserve_hours: Decimal = Decimal("0")
    other_direct_costs: Decimal = Decimal("0")
    annual_support_hours: Decimal = Decimal("0")
    support_hourly_cost: Decimal = Decimal("0")
    annual_support_other_direct_costs: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            _nonnegative(value, name)


@dataclass(frozen=True)
class SolutionsEconomics:
    prospecting_sales_hours: Decimal
    discovery_hours: Decimal
    solution_design_hours: Decimal
    coordination_acceptance_hours: Decimal
    hourly_cost: Decimal

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            _nonnegative(value, name)


@dataclass(frozen=True)
class SalesCharacteristics:
    procurement_difficulty: Level
    sales_cycle_months: Decimal
    customer_accessibility: Level
    close_friction: Level

    def __post_init__(self) -> None:
        _nonnegative(self.sales_cycle_months, "sales_cycle_months")


@dataclass(frozen=True)
class TechnicalCharacteristics:
    integration_count: int
    integration_complexity: Level
    data_availability: Level
    feasibility: Feasibility
    security_burden: Level
    compliance_burden: Level
    integration_permission_difficulty: Level

    def __post_init__(self) -> None:
        if self.integration_count < 0:
            raise ValueError("integration_count cannot be negative")


@dataclass(frozen=True)
class BuildVsBuy:
    finding: AlternativeFinding
    considered: tuple[AlternativeType, ...]
    note: str


@dataclass(frozen=True)
class AlternativeEconomics:
    """Comparable first-year costs for a buy/configure alternative."""

    setup_cost: Decimal
    recurring_annual_cost: Decimal
    internal_administration_cost: Decimal
    residual_annual_burden: Decimal
    risk_allowance: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            _nonnegative(value, name)


@dataclass(frozen=True)
class OpportunityScenario:
    business_name: str
    meaningful_problem: bool
    customer: CustomerEconomics
    delivery: DeliveryEconomics
    solutions: SolutionsEconomics
    sales: SalesCharacteristics
    technical: TechnicalCharacteristics
    build_vs_buy: BuildVsBuy
