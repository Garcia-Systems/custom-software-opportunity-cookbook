"""Plain, deterministic calculations; monetary inputs and outputs are Decimal."""

from decimal import Decimal
from .models import AlternativeEconomics, CustomerEconomics, DeliveryEconomics, SolutionsEconomics


def alternative_first_year_effect(a: AlternativeEconomics) -> Decimal:
    """Cash costs, retained burden, and an explicit risk allowance."""
    return sum(vars(a).values(), Decimal("0"))


def custom_first_year_effect(c: CustomerEconomics,
                             risk_allowance: Decimal = Decimal("0")) -> Decimal | None:
    """Custom spend plus burden the intervention is not expected to recover."""
    if risk_allowance < 0:
        raise ValueError("risk_allowance cannot be negative")
    if c.current_state_annual_burden is None or c.recoverable_value is None:
        return None
    return (c.implementation_price + c.recurring_annual_fee
            + c.current_state_annual_burden - c.recoverable_value + risk_allowance)


def customer_net_annual_benefit(c: CustomerEconomics) -> Decimal | None:
    return None if c.recoverable_value is None else c.recoverable_value - c.recurring_annual_fee


def first_year_roi(c: CustomerEconomics) -> Decimal | None:
    """First-year net gain / first-year customer spend; undefined at zero spend."""
    benefit = customer_net_annual_benefit(c)
    spend = c.implementation_price + c.recurring_annual_fee
    if benefit is None or spend == 0:
        return None
    return (benefit - c.implementation_price) / spend


def payback_period_months(c: CustomerEconomics) -> Decimal | None:
    """Implementation price / net annual benefit, expressed in months."""
    benefit = customer_net_annual_benefit(c)
    if benefit is None or benefit <= 0:
        return None
    return c.implementation_price / benefit * Decimal("12")


def implementation_delivery_cost(d: DeliveryEconomics) -> Decimal:
    hours = (d.reusable_engineering_hours + d.customer_specific_engineering_hours
             + d.qa_hours + d.deployment_hours + d.rework_reserve_hours
             + d.uncertainty_reserve_hours)
    return hours * d.engineering_hourly_cost + d.other_direct_costs


def annual_support_cost(d: DeliveryEconomics) -> Decimal:
    """Annual engineering plus non-labor obligations such as hosting."""
    return (d.annual_support_hours * d.support_hourly_cost
            + d.annual_support_other_direct_costs)


def solutions_hours(s: SolutionsEconomics) -> Decimal:
    return (s.prospecting_sales_hours + s.discovery_hours + s.solution_design_hours
            + s.coordination_acceptance_hours)


def solutions_labor_cost(s: SolutionsEconomics) -> Decimal:
    return solutions_hours(s) * s.hourly_cost


def solutions_contribution(c: CustomerEconomics, d: DeliveryEconomics,
                           s: SolutionsEconomics) -> Decimal:
    """Implementation price less direct delivery and internal solutions labor."""
    return c.implementation_price - implementation_delivery_cost(d) - solutions_labor_cost(s)


def effective_contribution_per_solutions_hour(c: CustomerEconomics,
                                               d: DeliveryEconomics,
                                               s: SolutionsEconomics) -> Decimal | None:
    hours = solutions_hours(s)
    return None if hours == 0 else solutions_contribution(c, d, s) / hours


def recurring_support_contribution(c: CustomerEconomics, d: DeliveryEconomics) -> Decimal:
    return c.recurring_annual_fee - annual_support_cost(d)


def reuse_percentage(d: DeliveryEconomics) -> Decimal | None:
    total = d.reusable_engineering_hours + d.customer_specific_engineering_hours
    return None if total == 0 else d.reusable_engineering_hours / total
