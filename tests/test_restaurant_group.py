from dataclasses import FrozenInstanceError
from decimal import Decimal as D

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (
    annual_support_cost, implementation_delivery_cost, reuse_percentage,
    solutions_contribution, solutions_hours,
)
from opportunity_cookbook.restaurant_group import (
    BurdenScope, GroupBurdenAssumption, baseline_case, case_comparison,
    high_standardization_case, low_standardization_case,
    saas_alternative_case, ten_location_case,
)
from opportunity_cookbook.verdicts import Verdict


def test_per_location_and_group_burdens_and_recovery_are_derived():
    case = baseline_case()
    assert case.location_level_burden == D("133500")
    assert case.group_level_burden == D("40000")
    assert case.total_burden == D("173500")
    assert case.recoverable_value == D("67070")
    assert case.scenario.customer.current_state_annual_burden == case.total_burden
    assert case.scenario.customer.recoverable_value == sum(
        (b.burden(5) * b.improvement_rate for b in case.burdens), D("0"))


def test_delivery_shared_incremental_specific_and_total_hours():
    case = baseline_case()
    assert case.engineering.shared_hours == D("100")
    assert case.engineering.incremental_hours == D("50")
    assert case.engineering.exception_hours == D("30")
    assert case.engineering.total_hours == D("234")
    assert case.scenario.delivery.customer_specific_engineering_hours == D("80")
    assert implementation_delivery_cost(case.scenario.delivery) == D("19000")


def test_support_scales_while_fixed_obligations_remain_fixed():
    five, ten = baseline_case(), ten_location_case()
    assert five.support.fixed_hours == ten.support.fixed_hours == D("18")
    assert five.support.total_hours == D("68")
    assert ten.support.total_hours == D("108")
    assert annual_support_cost(five.scenario.delivery) == D("6900")
    assert annual_support_cost(ten.scenario.delivery) == D("10400")


def test_one_group_sales_effort_does_not_multiply_by_locations():
    case = baseline_case()
    assert case.location_count == 5
    assert solutions_hours(case.scenario.solutions) == D("52")
    assert solutions_hours(case.scenario.solutions) != D("28") * 5
    assert solutions_contribution(case.scenario.customer, case.scenario.delivery,
                                  case.scenario.solutions) == D("19620")


def test_baseline_is_deterministic_immutable_and_traceable():
    first, second = baseline_case(), baseline_case()
    assert first == second
    result = analyze(first.scenario)
    assert result == analyze(second.scenario)
    assert result.verdict is Verdict.PROMISING
    assert result.reasons == (
        "Customer value, delivery contribution, and recurring support economics work under the assumptions.",
        "At least 40% of core engineering work is modeled as demonstrably reusable.",
        "Promising is an economic hypothesis; market validation still requires discovery.",
    )
    with pytest.raises(FrozenInstanceError):
        first.location_count = 6


def test_standardization_scenarios_change_effort_without_mutating_baseline():
    baseline = baseline_case()
    high, low = high_standardization_case(), low_standardization_case()
    assert high.engineering.total_hours < baseline.engineering.total_hours
    assert low.engineering.total_hours > baseline.engineering.total_hours
    assert implementation_delivery_cost(high.scenario.delivery) < implementation_delivery_cost(baseline.scenario.delivery)
    assert implementation_delivery_cost(low.scenario.delivery) > implementation_delivery_cost(baseline.scenario.delivery)
    assert analyze(high.scenario).verdict is Verdict.PROMISING
    assert analyze(low.scenario).verdict is Verdict.ONE_OFF
    assert reuse_percentage(low.scenario.delivery) < D("0.40")
    assert baseline == baseline_case()


def test_strong_saas_alternative_wins():
    assert analyze(saas_alternative_case().scenario).verdict is Verdict.BUY_CONFIGURE


def test_case_one_comparison_is_calculated_and_deterministic():
    first = case_comparison()
    assert first == case_comparison()
    one, five = first
    assert (one.locations, one.burden, one.recoverable_value, one.engineering_hours,
            one.verdict) == (1, D("35240"), D("10392"), D("150"), "NO DEAL")
    assert (five.locations, five.burden, five.recoverable_value, five.engineering_hours,
            five.verdict) == (5, D("173500"), D("67070"), D("234"),
                             "PROMISING — VALIDATE IN DISCOVERY")
    assert five.recoverable_value / one.recoverable_value > five.engineering_hours / one.engineering_hours


@pytest.mark.parametrize("count", [0, -1, 2.5, True])
def test_invalid_location_counts_are_rejected(count):
    burden = GroupBurdenAssumption("test", BurdenScope.PER_LOCATION, D("1"), D("0.5"))
    with pytest.raises(ValueError, match="positive integer"):
        burden.burden(count)


@pytest.mark.parametrize("amount,rate", [(D("-1"), D("0.5")), (D("1"), D("-0.1")), (D("1"), D("1.1"))])
def test_invalid_per_location_assumptions_are_rejected(amount, rate):
    with pytest.raises(ValueError):
        GroupBurdenAssumption("invalid", BurdenScope.PER_LOCATION, amount, rate)
