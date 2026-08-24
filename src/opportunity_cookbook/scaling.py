"""Reusable, immutable scaling assumptions for multi-unit delivery and support."""

from dataclasses import dataclass
from decimal import Decimal


def _nonnegative(value: Decimal, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} cannot be negative")


def _units(value: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError("unit_count must be a positive integer")


@dataclass(frozen=True)
class EngineeringScaling:
    """Shared work plus work that scales by unit and exceptional work."""

    shared_hours: Decimal
    per_unit_hours: Decimal
    unit_count: int
    exception_hours: Decimal
    qa_hours: Decimal = Decimal("0")
    deployment_hours: Decimal = Decimal("0")
    rework_reserve_hours: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        _units(self.unit_count)
        for name, value in vars(self).items():
            if name != "unit_count":
                _nonnegative(value, name)

    @property
    def incremental_hours(self) -> Decimal:
        return self.per_unit_hours * self.unit_count

    @property
    def core_hours(self) -> Decimal:
        return self.shared_hours + self.incremental_hours + self.exception_hours

    @property
    def total_hours(self) -> Decimal:
        return (self.core_hours + self.qa_hours + self.deployment_hours
                + self.rework_reserve_hours)


@dataclass(frozen=True)
class SupportScaling:
    """Recurring obligations that are fixed, per-unit, or exceptional."""

    fixed_hours: Decimal
    per_unit_hours: Decimal
    unit_count: int
    exception_hours: Decimal = Decimal("0")
    fixed_other_costs: Decimal = Decimal("0")
    per_unit_other_costs: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        _units(self.unit_count)
        for name, value in vars(self).items():
            if name != "unit_count":
                _nonnegative(value, name)

    @property
    def total_hours(self) -> Decimal:
        return self.fixed_hours + self.per_unit_hours * self.unit_count + self.exception_hours

    @property
    def total_other_costs(self) -> Decimal:
        return self.fixed_other_costs + self.per_unit_other_costs * self.unit_count
