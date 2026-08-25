"""Plain, deterministic calculations; monetary inputs and outputs are Decimal."""

from decimal import Decimal
from .models import AlternativeEconomics, CustomerEconomics, DeliveryEconomics, SolutionsEconomics


def alternative_first_year_effect(a: AlternativeEconomics) -> Decimal:
    """Cash costs, retained burden, and an explicit risk allowance."""
    return sum(vars(a).values(), Decimal("0"))


def alternative_recovered_burden(original_burden: Decimal,
                                  residual_burden: Decimal) -> Decimal:
    """Burden removed by an alternative, kept separate from its cash cost."""
    if original_burden < 0 or residual_burden < 0:
        raise ValueError("burdens cannot be negative")
    if residual_burden > original_burden:
        raise ValueError("residual_burden cannot exceed original_burden")
    return original_burden - residual_burden


def incremental_custom_value(custom_recoverable_value: Decimal,
                             alternative_recoverable_value: Decimal) -> Decimal:
    """Additional annual burden custom removes above the best alternative."""
    if custom_recoverable_value < 0 or alternative_recoverable_value < 0:
        raise ValueError("recoverable values cannot be negative")
    return max(Decimal("0"), custom_recoverable_value - alternative_recoverable_value)


def break_even_alternative_residual_burden(
        custom_first_year_total_effect: Decimal,
        alternative: AlternativeEconomics) -> Decimal:
    """Residual burden at which buy/configure and custom first-year effects tie."""
    if custom_first_year_total_effect < 0:
        raise ValueError("custom_first_year_total_effect cannot be negative")
    fixed = (alternative.setup_cost + alternative.recurring_annual_cost
             + alternative.internal_administration_cost + alternative.risk_allowance)
    return max(Decimal("0"), custom_first_year_total_effect - fixed)


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


def implementation_contribution(implementation_revenue: Decimal,
                                direct_implementation_cost: Decimal) -> Decimal:
    """Revenue left after direct implementation cost (before solutions labor)."""
    if implementation_revenue < 0 or direct_implementation_cost < 0:
        raise ValueError("implementation revenue and cost cannot be negative")
    return implementation_revenue - direct_implementation_cost


def delivery_break_even_price(direct_implementation_cost: Decimal) -> Decimal:
    """The implementation price that exactly covers direct delivery."""
    if direct_implementation_cost < 0:
        raise ValueError("direct_implementation_cost cannot be negative")
    return direct_implementation_cost


def target_contribution_price(direct_implementation_cost: Decimal,
                              required_contribution: Decimal) -> Decimal:
    """Direct delivery cost plus an explicit required implementation contribution."""
    if direct_implementation_cost < 0 or required_contribution < 0:
        raise ValueError("price-corridor assumptions cannot be negative")
    return direct_implementation_cost + required_contribution


def customer_maximum_economic_price(recoverable_annual_value: Decimal,
                                    recurring_annual_fee: Decimal,
                                    required_retained_benefit: Decimal) -> Decimal:
    """Highest implementation price preserving a stated first-year benefit."""
    if any(value < 0 for value in (recoverable_annual_value,
                                   recurring_annual_fee,
                                   required_retained_benefit)):
        raise ValueError("price-corridor assumptions cannot be negative")
    return max(Decimal("0"), recoverable_annual_value - recurring_annual_fee
               - required_retained_benefit)


def has_feasible_price_corridor(minimum_sustainable_price: Decimal,
                                maximum_economic_price: Decimal) -> bool:
    if minimum_sustainable_price < 0 or maximum_economic_price < 0:
        raise ValueError("price-corridor bounds cannot be negative")
    return minimum_sustainable_price <= maximum_economic_price


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
