from dataclasses import FrozenInstanceError
from decimal import Decimal as D

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    implementation_delivery_cost, recurring_support_contribution,
    reuse_percentage, solutions_contribution, solutions_hours)
from opportunity_cookbook.independent_hotel import (HotelBurden, baseline_case,
    difficult_integration_case, easy_integration_case, higher_burden_case,
    strong_saas_case)
from opportunity_cookbook.models import Feasibility, Level
from opportunity_cookbook.verdicts import Verdict


def test_burdens_and_recoverable_value_are_explicit_and_not_double_counted():
    case = baseline_case()
    assert case.total_burden == D("94196")
    assert case.recoverable_value == D("35342.80")
    assert case.scenario.customer.current_state_annual_burden == sum(
        (b.annual_burden for b in case.burdens), D("0"))
    assert case.scenario.customer.recoverable_value == sum(
        (b.annual_burden * b.improvement_rate for b in case.burdens), D("0"))
    assert len({b.name for b in case.burdens}) == len(case.burdens)
    operational = next(b for b in case.burdens if b.name == "Avoidable operational inefficiency")
    assert operational.hours_per_week == 0  # separate loss pool, not duplicate labor


def test_baseline_is_deterministic_immutable_and_framework_derived():
    first = baseline_case()
    assert first == baseline_case()
    result = analyze(first.scenario)
    assert result.verdict is Verdict.NO_DEAL
    assert result.reasons == (
        "The customer does not recover implementation price within one year.",)
    with pytest.raises(FrozenInstanceError):
        first.room_count = 140


def test_integration_access_scenarios_change_delivery_without_mutation():
    baseline = baseline_case()
    easy, difficult = easy_integration_case(), difficult_integration_case()
    assert easy.scenario.technical.integration_permission_difficulty is Level.LOW
    assert difficult.scenario.technical.integration_permission_difficulty is Level.HIGH
    assert difficult.scenario.technical.feasibility is Feasibility.UNKNOWN
    assert implementation_delivery_cost(easy.scenario.delivery) < implementation_delivery_cost(baseline.scenario.delivery)
    assert implementation_delivery_cost(difficult.scenario.delivery) > implementation_delivery_cost(baseline.scenario.delivery)
    assert analyze(difficult.scenario).verdict is Verdict.INVESTIGATE
    assert baseline == baseline_case()


def test_strong_saas_wins_before_custom_economics():
    assert analyze(strong_saas_case().scenario).verdict is Verdict.BUY_CONFIGURE


def test_higher_measured_burden_changes_customer_economics_and_verdict():
    baseline, high = baseline_case(), higher_burden_case()
    assert high.total_burden > baseline.total_burden
    assert high.recoverable_value > baseline.recoverable_value
    assert analyze(high.scenario).verdict is Verdict.PROMISING
    assert baseline == baseline_case()


def test_delivery_support_reuse_and_solutions_are_derived():
    case = baseline_case()
    s, d = case.scenario, case.scenario.delivery
    assert implementation_delivery_cost(d) == D("18750")
    assert reuse_percentage(d) == D("78") / D("176")
    assert solutions_hours(s.solutions) == case.solutions_work.total_hours == D("58")
    assert solutions_contribution(s.customer, d, s.solutions) == D("7480")
    assert annual_support_cost(d) == D("6750")
    assert recurring_support_contribution(s.customer, d) == D("2250")


@pytest.mark.parametrize("hours,cost,weeks,loss", [
    (D("-1"), D("1"), D("1"), D("0")),
    (D("1"), D("-1"), D("1"), D("0")),
    (D("1"), D("1"), D("-1"), D("0")),
    (D("0"), D("0"), D("1"), D("-1")),
])
def test_negative_hotel_assumptions_are_rejected(hours, cost, weeks, loss):
    with pytest.raises(ValueError, match="negative"):
        HotelBurden("invalid", hours, cost, weeks, D("0.5"), loss)


@pytest.mark.parametrize("rate", [D("-0.01"), D("1.01")])
def test_invalid_improvement_rates_are_rejected(rate):
    with pytest.raises(ValueError, match="between 0 and 1"):
        HotelBurden("invalid", D("1"), D("1"), D("1"), rate)
