from dataclasses import FrozenInstanceError, replace
from decimal import Decimal as D

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (
    annual_support_cost, customer_net_annual_benefit,
    implementation_delivery_cost, recurring_support_contribution,
    reuse_percentage,
)
from opportunity_cookbook.independent_restaurant import (
    BurdenAssumption, baseline_case, higher_value_case,
    lower_delivery_cost_case, saas_alternative_case,
)
from opportunity_cookbook.verdicts import Verdict


def test_burden_components_and_explicit_recovery_sum():
    case = baseline_case()
    assert case.total_burden == D("35240")
    assert case.recoverable_value == D("10392")
    assert case.recoverable_value == sum(
        (b.annual_burden * b.improvement_rate for b in case.burdens), D("0"))
    assert all(b.recoverable_value <= b.annual_burden for b in case.burdens)


def test_baseline_is_deterministic_immutable_and_traceable():
    first, second = baseline_case(), baseline_case()
    assert first == second
    assert analyze(first.scenario) == analyze(second.scenario)
    assert analyze(first.scenario).verdict is Verdict.NO_DEAL
    assert analyze(first.scenario).reasons == (
        "The customer does not recover implementation price within one year.",)
    with pytest.raises(FrozenInstanceError):
        first.scenario.business_name = "Changed"


def test_higher_recovery_changes_customer_economics_without_mutating_baseline():
    baseline = baseline_case()
    higher = higher_value_case()
    assert higher.recoverable_value > baseline.recoverable_value
    assert customer_net_annual_benefit(higher.scenario.customer) > customer_net_annual_benefit(baseline.scenario.customer)
    assert analyze(higher.scenario).verdict is Verdict.PROMISING
    assert baseline == baseline_case()


def test_lower_effort_changes_delivery_economics():
    baseline, lower = baseline_case(), lower_delivery_cost_case()
    assert implementation_delivery_cost(lower.scenario.delivery) < implementation_delivery_cost(baseline.scenario.delivery)


def test_saas_alternative_can_win():
    assert analyze(saas_alternative_case().scenario).verdict is Verdict.BUY_CONFIGURE


def test_support_and_reuse_are_derived():
    delivery = baseline_case().scenario.delivery
    assert annual_support_cost(delivery) == D("2700")
    assert recurring_support_contribution(baseline_case().scenario.customer, delivery) == D("300")
    assert reuse_percentage(delivery) == D("70") / D("122")


@pytest.mark.parametrize("rate", [D("-0.01"), D("1.01")])
def test_invalid_improvement_percentage_rejected(rate):
    with pytest.raises(ValueError, match="improvement_rate"):
        BurdenAssumption("invalid", D("1"), rate)


def test_negative_burden_rejected():
    with pytest.raises(ValueError, match="annual_burden"):
        BurdenAssumption("invalid", D("-1"), D("0.5"))
