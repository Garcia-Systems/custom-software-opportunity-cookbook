from dataclasses import replace
from decimal import Decimal as D
import pytest
from opportunity_cookbook.economics import *
from opportunity_cookbook.models import CustomerEconomics, DeliveryEconomics, SolutionsEconomics


def test_customer_calculations():
    c = CustomerEconomics(D("20000"), D("12000"), D("5000"), D("2000"))
    assert customer_net_annual_benefit(c) == D("10000")
    assert first_year_roi(c) == D("5") / D("7")
    assert payback_period_months(c) == D("6")


def test_delivery_solutions_support_and_reuse():
    d = DeliveryEconomics(D("30"), D("20"), D("100"), D("5"), D("5"), D("10"), D("500"), D("12"), D("100"))
    s = SolutionsEconomics(D("2"), D("3"), D("4"), D("1"), D("50"))
    c = CustomerEconomics(D("20000"), D("15000"), D("10000"), D("2000"))
    assert implementation_delivery_cost(d) == D("7500")
    assert annual_support_cost(d) == D("1200")
    assert recurring_support_contribution(c, d) == D("800")
    assert solutions_contribution(c, d, s) == D("2000")
    assert effective_contribution_per_solutions_hour(c, d, s) == D("200")
    assert reuse_percentage(d) == D("0.6")


@pytest.mark.parametrize("field", ["current_state_annual_burden", "recoverable_value", "implementation_price", "recurring_annual_fee"])
def test_negative_money_rejected(field):
    values = dict(current_state_annual_burden=D("1"), recoverable_value=D("1"), implementation_price=D("1"), recurring_annual_fee=D("1"))
    values[field] = D("-1")
    with pytest.raises(ValueError): CustomerEconomics(**values)


def test_burden_bounds_recoverable_value():
    with pytest.raises(ValueError): CustomerEconomics(D("10"), D("11"), D("1"), D("0"))


def test_negative_hours_rejected_and_zero_denominators_explicit():
    with pytest.raises(ValueError): DeliveryEconomics(D("-1"), D("0"), D("1"))
    d = DeliveryEconomics(D("0"), D("0"), D("0"))
    s = SolutionsEconomics(D("0"), D("0"), D("0"), D("0"), D("0"))
    c = CustomerEconomics(D("0"), D("0"), D("0"), D("0"))
    assert reuse_percentage(d) is None
    assert first_year_roi(c) is None
    assert payback_period_months(c) is None
    assert effective_contribution_per_solutions_hour(c, d, s) is None
