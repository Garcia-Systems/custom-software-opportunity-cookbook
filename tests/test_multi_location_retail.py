from dataclasses import FrozenInstanceError
from decimal import Decimal as D

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (alternative_first_year_effect,
    annual_support_cost, custom_first_year_effect, implementation_delivery_cost,
    recurring_support_contribution, solutions_contribution, solutions_hours)
from opportunity_cookbook.models import AlternativeEconomics
from opportunity_cookbook.multi_location_retail import (RetailBurden,
    baseline_case, higher_burden_case, highly_standardized_case,
    messy_acquired_stores_case, one_off_niche_case,
    strong_saas_alternative_case, weak_saas_alternative_case)
from opportunity_cookbook.verdicts import Verdict


def test_retail_burden_and_recoverable_value_are_derived():
    item = RetailBurden("work", D("4"), D("50"), D("52"), D(".4"))
    assert item.annual_burden == D("10400")
    assert item.recoverable == D("4160.0")
    case = baseline_case()
    assert case.total_burden == D("111020")
    assert case.recoverable_value == D("51513.80")
    assert case.scenario.customer.current_state_annual_burden == sum(
        (item.annual_burden for item in case.burdens), D("0"))
    assert case.scenario.customer.recoverable_value == sum(
        (item.recoverable for item in case.burdens), D("0"))


def test_baseline_is_deterministic_immutable_and_buy_traceable():
    case = baseline_case()
    assert case == baseline_case()
    result = analyze(case.scenario)
    assert result.verdict is Verdict.BUY_CONFIGURE
    assert result.reasons == ("An existing buy/configure alternative adequately meets the need at materially lower cost or risk.",)
    assert alternative_first_year_effect(case.alternative) < custom_first_year_effect(
        case.scenario.customer, case.custom_risk_allowance)
    with pytest.raises(FrozenInstanceError):
        case.custom_risk_allowance = D("0")


def test_shared_store_ecommerce_exception_and_total_effort_are_explicit():
    engineering = baseline_case().engineering
    assert engineering.shared_hours == D("170")
    assert engineering.per_store_total_hours == D("54")
    assert engineering.ecommerce_hours == D("42")
    assert engineering.exception_hours == D("30")
    assert engineering.total_hours == D("378")


def test_support_delivery_and_solutions_economics_are_derived():
    case = baseline_case(); scenario = case.scenario
    assert case.support.total_hours == D("80")
    assert annual_support_cost(scenario.delivery) == D("9880")
    assert recurring_support_contribution(scenario.customer, scenario.delivery) == D("5120")
    assert implementation_delivery_cost(scenario.delivery) == D("32440")
    assert solutions_hours(scenario.solutions) == case.solutions_work.total_hours == D("78")
    assert solutions_contribution(scenario.customer, scenario.delivery, scenario.solutions) == D("24100")


def test_saas_strength_changes_framework_derived_verdict():
    weak = weak_saas_alternative_case()
    strong = strong_saas_alternative_case()
    assert analyze(weak.scenario).verdict is Verdict.PROMISING
    assert analyze(strong.scenario).verdict is Verdict.BUY_CONFIGURE
    assert alternative_first_year_effect(weak.alternative) > custom_first_year_effect(
        weak.scenario.customer, weak.custom_risk_allowance)


def test_standardized_and_messy_scenarios_change_delivery_and_support():
    baseline = baseline_case(); standard = highly_standardized_case(); messy = messy_acquired_stores_case()
    assert implementation_delivery_cost(standard.scenario.delivery) < implementation_delivery_cost(baseline.scenario.delivery)
    assert standard.engineering.exception_hours < baseline.engineering.exception_hours
    assert annual_support_cost(standard.scenario.delivery) < annual_support_cost(baseline.scenario.delivery)
    assert implementation_delivery_cost(messy.scenario.delivery) > implementation_delivery_cost(baseline.scenario.delivery)
    assert messy.engineering.exception_hours > baseline.engineering.exception_hours
    assert annual_support_cost(messy.scenario.delivery) > annual_support_cost(baseline.scenario.delivery)
    assert baseline == baseline_case()


def test_higher_burden_and_one_off_niche_behaviors():
    assert higher_burden_case().total_burden > baseline_case().total_burden
    assert analyze(higher_burden_case().scenario).verdict is Verdict.PROMISING
    assert analyze(one_off_niche_case().scenario).verdict is Verdict.ONE_OFF


def test_generic_alternative_economics_and_validation():
    alternative = AlternativeEconomics(D("1"), D("2"), D("3"), D("4"), D("5"))
    assert alternative_first_year_effect(alternative) == D("15")
    with pytest.raises(ValueError, match="negative"):
        AlternativeEconomics(D("-1"), D("0"), D("0"), D("0"))
    with pytest.raises(ValueError, match="negative"):
        custom_first_year_effect(baseline_case().scenario.customer, D("-1"))


@pytest.mark.parametrize("hours,cost,weeks", [(D("-1"),D("1"),D("1")),
    (D("1"),D("-1"),D("1")), (D("1"),D("1"),D("-1"))])
def test_negative_burden_inputs_are_rejected(hours, cost, weeks):
    with pytest.raises(ValueError, match="negative"):
        RetailBurden("bad", hours, cost, weeks, D(".5"))


@pytest.mark.parametrize("rate", [D("-.01"), D("1.01")])
def test_invalid_retail_percentages_are_rejected(rate):
    with pytest.raises(ValueError, match="between 0 and 1"):
        RetailBurden("bad", D("1"), D("1"), D("1"), rate)
