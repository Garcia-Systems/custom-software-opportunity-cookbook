from dataclasses import FrozenInstanceError
from decimal import Decimal as D

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    implementation_delivery_cost, recurring_support_contribution,
    reuse_percentage, solutions_contribution, solutions_hours)
from opportunity_cookbook.tourism_attraction import (SeasonalBurden,
    SeasonalProfile, baseline_case, fragmented_integrations_case,
    high_reconciliation_burden_case, high_seasonality_low_burden_case,
    implemented_case_comparison, standardized_integrations_case,
    strong_vertical_saas_case, uncertain_revenue_upside_case)
from opportunity_cookbook.verdicts import Verdict


def test_seasonal_burden_and_recovery_are_transparent_and_derived():
    season = SeasonalProfile(D("10"), D("20"))
    burden = SeasonalBurden("labor", D("4"), D("2"), D("50"), D(".25"), "hours")
    assert season.operating_weeks == D("30")
    assert burden.annual_burden(season) == D("4000")
    assert burden.recoverable(season) == D("1000.00")


def test_baseline_component_sums_and_recovery_are_derived():
    case = baseline_case()
    assert case.total_burden == D("44264")
    assert case.burden_recovery == case.recoverable_value == D("16915.60")
    assert case.scenario.customer.current_state_annual_burden == sum(
        (b.annual_burden(case.season) for b in case.burdens), D("0"))
    assert case.scenario.customer.recoverable_value == sum(
        (b.annual_burden(case.season) * b.improvement_rate for b in case.burdens), D("0"))


def test_baseline_is_deterministic_immutable_and_framework_derived():
    case = baseline_case()
    assert case == baseline_case()
    result = analyze(case.scenario)
    assert result.verdict is Verdict.NO_DEAL
    assert result.reasons == ("The customer does not recover implementation price within one year.",)
    with pytest.raises(FrozenInstanceError):
        case.season = SeasonalProfile(D("1"), D("1"))


def test_seasonality_and_high_burden_change_annual_economics():
    baseline = baseline_case()
    seasonal = high_seasonality_low_burden_case()
    high = high_reconciliation_burden_case()
    assert seasonal.season.operating_weeks < baseline.season.operating_weeks
    assert seasonal.total_burden < baseline.total_burden
    assert seasonal.recoverable_value < baseline.recoverable_value
    assert high.total_burden > baseline.total_burden
    assert high.recoverable_value > baseline.recoverable_value
    assert analyze(high.scenario).verdict is Verdict.PROMISING


def test_integration_quality_changes_delivery_and_support_without_mutation():
    baseline = baseline_case()
    standard = standardized_integrations_case()
    fragmented = fragmented_integrations_case()
    assert implementation_delivery_cost(standard.scenario.delivery) < implementation_delivery_cost(baseline.scenario.delivery)
    assert implementation_delivery_cost(fragmented.scenario.delivery) > implementation_delivery_cost(baseline.scenario.delivery)
    assert annual_support_cost(standard.scenario.delivery) < annual_support_cost(baseline.scenario.delivery)
    assert annual_support_cost(fragmented.scenario.delivery) > annual_support_cost(baseline.scenario.delivery)
    assert analyze(fragmented.scenario).verdict is Verdict.NO_DEAL
    assert baseline == baseline_case()


def test_vertical_saas_can_win():
    result = analyze(strong_vertical_saas_case().scenario)
    assert result.verdict is Verdict.BUY_CONFIGURE


def test_delivery_reuse_solutions_and_support_are_derived():
    case = baseline_case(); s = case.scenario
    assert reuse_percentage(s.delivery) == D("100") / D("220")
    assert solutions_hours(s.solutions) == case.solutions_work.total_hours == D("50")
    assert implementation_delivery_cost(s.delivery) == D("23025")
    assert solutions_contribution(s.customer, s.delivery, s.solutions) == D("725")
    assert annual_support_cost(s.delivery) == D("6150")
    assert recurring_support_contribution(s.customer, s.delivery) == D("1050")


def test_uncertain_upside_is_explicit_and_does_not_contaminate_baseline():
    baseline = baseline_case(); upside = uncertain_revenue_upside_case()
    assert baseline.uncertain_revenue_upside == D("0")
    assert upside.uncertain_revenue_upside == D("8000")
    assert upside.total_burden == baseline.total_burden
    assert upside.recoverable_value == baseline.recoverable_value + D("8000")
    assert baseline == baseline_case()


def test_implemented_comparison_has_cases_one_through_ten_and_is_calculated():
    rows = implemented_case_comparison()
    assert rows == implemented_case_comparison()
    assert tuple(r.name for r in rows) == ("Independent restaurant", "Restaurant group",
        "Independent hotel", "Hotel group", "Tourism attraction", "Multi-location retailer",
        "Construction / trades", "Professional services", "Local government",
        "University department")
    assert rows[4].recoverable_value == baseline_case().recoverable_value


@pytest.mark.parametrize("peak,off", [(D("-1"), D("1")), (D("1"), D("-1"))])
def test_negative_seasonal_weeks_are_rejected(peak, off):
    with pytest.raises(ValueError, match="negative"):
        SeasonalProfile(peak, off)


@pytest.mark.parametrize("peak,off,cost", [(D("-1"),D("1"),D("1")),
    (D("1"),D("-1"),D("1")), (D("1"),D("1"),D("-1"))])
def test_negative_burden_values_are_rejected(peak, off, cost):
    with pytest.raises(ValueError, match="negative"):
        SeasonalBurden("bad", peak, off, cost, D(".5"), "test")


@pytest.mark.parametrize("rate", [D("-0.01"), D("1.01")])
def test_invalid_improvement_rates_are_rejected(rate):
    with pytest.raises(ValueError, match="between 0 and 1"):
        SeasonalBurden("bad", D("1"), D("1"), D("1"), rate, "test")
