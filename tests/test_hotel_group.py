from dataclasses import FrozenInstanceError
from decimal import Decimal as D
import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    implementation_delivery_cost, recurring_support_contribution,
    solutions_contribution, solutions_hours)
from opportunity_cookbook.hotel_group import (BurdenScope, GroupHotelBurden,
    baseline_case, case_three_comparison, fragmented_portfolio_case,
    high_standardization_case, larger_group_case, strong_saas_case)
from opportunity_cookbook.verdicts import Verdict


def test_property_and_central_burden_and_recovery_are_derived():
    case = baseline_case()
    assert case.property_level_burden == D("120224.0")
    assert case.central_burden == D("82576")
    assert case.total_burden == D("202800.0")
    assert case.recoverable_value == D("94484.000")
    assert case.scenario.customer.recoverable_value == sum(
        (b.annual_burden(4) * b.improvement_rate for b in case.burdens), D("0"))


def test_property_burden_scales_but_central_burden_is_separate():
    item = GroupHotelBurden("x", BurdenScope.PROPERTY, D("2"), D("10"), D("50"), D(".5"))
    central = GroupHotelBurden("y", BurdenScope.CENTRAL, D("2"), D("10"), D("50"), D(".5"))
    assert item.annual_burden(4) == D("4000")
    assert central.annual_burden(4) == D("1000")


def test_engineering_support_and_solutions_components_are_visible_and_derived():
    case = baseline_case(); e = case.engineering; s = case.support; scenario = case.scenario
    assert (e.shared_hours, e.incremental_hours, e.exception_hours, e.total_hours) == (D("130"), D("72"), D("38"), D("314"))
    assert implementation_delivery_cost(scenario.delivery) == D("25750")
    assert (s.fixed_hours, s.per_unit_hours * s.unit_count, s.exception_hours) == (D("24"), D("36"), D("12"))
    assert annual_support_cost(scenario.delivery) == D("8800")
    assert recurring_support_contribution(scenario.customer, scenario.delivery) == D("6200")
    assert solutions_hours(scenario.solutions) == case.solutions_work.total_hours == D("76")
    assert solutions_contribution(scenario.customer, scenario.delivery, scenario.solutions) == D("17310")


def test_baseline_is_immutable_deterministic_and_reasons_traceable():
    case = baseline_case()
    assert case == baseline_case()
    result = analyze(case.scenario)
    assert result.verdict is Verdict.PROMISING
    assert len(result.reasons) == 3
    with pytest.raises(FrozenInstanceError): case.property_count = 5


def test_standardization_materially_changes_delivery_without_mutating_baseline():
    baseline = baseline_case(); high = high_standardization_case(); low = fragmented_portfolio_case()
    assert implementation_delivery_cost(high.scenario.delivery) < implementation_delivery_cost(baseline.scenario.delivery)
    assert implementation_delivery_cost(low.scenario.delivery) > implementation_delivery_cost(baseline.scenario.delivery)
    assert high.engineering.exception_hours < baseline.engineering.exception_hours < low.engineering.exception_hours
    assert analyze(low.scenario).verdict is Verdict.NO_DEAL
    assert baseline == baseline_case()


def test_saas_wins_and_larger_group_scales_shared_work_only_once():
    assert analyze(strong_saas_case().scenario).verdict is Verdict.BUY_CONFIGURE
    large = larger_group_case(); base = baseline_case()
    assert large.property_count == 8
    assert large.engineering.shared_hours == base.engineering.shared_hours
    assert large.engineering.incremental_hours > base.engineering.incremental_hours
    assert large.total_burden > base.total_burden


def test_case_three_comparison_is_calculated_and_deterministic():
    first = case_three_comparison(); second = case_three_comparison()
    assert first == second
    assert first[0].properties == 1 and first[1].properties == 4
    assert first[0].recoverable_value == D("35342.80")
    assert first[1].recoverable_value == baseline_case().recoverable_value


@pytest.mark.parametrize("count", [0, -1, True, D("4")])
def test_invalid_property_counts_are_rejected(count):
    with pytest.raises(ValueError, match="positive integer"):
        # Public burden calculation validates counts without relying on private builders.
        baseline_case().burdens[0].annual_burden(count)


@pytest.mark.parametrize("hours,cost,weeks", [(D("-1"),D("1"),D("1")),(D("1"),D("-1"),D("1")),(D("1"),D("1"),D("-1"))])
def test_negative_burden_values_are_rejected(hours, cost, weeks):
    with pytest.raises(ValueError, match="negative"):
        GroupHotelBurden("bad", BurdenScope.PROPERTY, hours, cost, weeks, D(".5"))
