from dataclasses import FrozenInstanceError
from decimal import Decimal as D
import pytest

from opportunity_cookbook.bad_sales_motion import (AcquisitionMotion, Burden,
    baseline_case, case_13_vs_14, case_9_vs_14, close_rate_sensitivity,
    higher_close_rate_case, higher_price_only_case, larger_customer_case,
    partner_channel_case, productized_sales_case, scenario_results,
    very_high_reuse_case, warm_referral_case)
from opportunity_cookbook.economics import (acquisition_adjusted_minimum_price,
    expected_acquisition_cost, expected_sales_hours_per_win, first_year_roi,
    payback_period_months, reuse_percentage)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison
from opportunity_cookbook.verdicts import Verdict


def test_baseline_customer_delivery_reuse_support_and_immutability():
    case = baseline_case()
    assert case == baseline_case()
    assert case.total_burden == D("17628")
    assert case.recoverable_value == D("10930.20")
    assert first_year_roi(case.scenario.customer) == D("0.2144666666666666666666666667")
    assert payback_period_months(case.scenario.customer) < D("10")
    assert reuse_percentage(case.scenario.delivery) == D(".8")
    assert sum((case.scenario.delivery.reusable_engineering_hours,
                case.scenario.delivery.customer_specific_engineering_hours,
                case.scenario.delivery.qa_hours, case.scenario.delivery.deployment_hours,
                case.scenario.delivery.rework_reserve_hours,
                case.scenario.delivery.uncertainty_reserve_hours), D("0")) == D("45")
    assert case.delivery_cost == D("3500")
    assert case.implementation_contribution == D("3500")
    assert case.support_cost == D("900") and case.recurring_contribution == D("1100")
    with pytest.raises(FrozenInstanceError): case.acquisition.close_probability = D("1")


def test_acquisition_unit_economics_corridor_and_verdict():
    case = baseline_case()
    assert case.expected_sales_hours == D("140")
    assert case.acquisition_cost == D("9100")
    assert case.contribution_before_acquisition == D("4600")
    assert case.contribution_after_acquisition == D("-4500")
    assert case.customer_maximum_price == D("5530.20")
    assert case.acquisition_adjusted_minimum_price == D("13500")
    assert not case.feasible_corridor
    assert case.result.verdict is Verdict.POOR_TARGET
    assert case.result.reasons == (
        "Expected customer acquisition effort is too high relative to contract value.",
        "Contribution after expected acquisition cost is below the required contribution.",
        "The acquisition-adjusted minimum price exceeds the customer's economic maximum.",)


def test_generic_acquisition_calculations_and_validation():
    assert expected_sales_hours_per_win(D("28"), D(".2")) == D("140")
    assert expected_acquisition_cost(D("140"), D("65")) == D("9100")
    assert expected_acquisition_cost(D("10"), D("65"), D("700")) == D("1350")
    assert acquisition_adjusted_minimum_price(D("3500"), D("9100"), D("2000"), D("1100")) == D("13500")
    for probability in (D("0"), D("-1"), D("1.01")):
        with pytest.raises(ValueError): expected_sales_hours_per_win(D("1"), probability)
    for call in (lambda: expected_sales_hours_per_win(D("-1"), D(".5")),
                 lambda: expected_acquisition_cost(D("-1"), D("1")),
                 lambda: acquisition_adjusted_minimum_price(D("-1"), D("1"), D("1"))):
        with pytest.raises(ValueError): call()
    with pytest.raises(ValueError): Burden("bad", D("-1"), D("1"), D(".5"))
    with pytest.raises(ValueError): AcquisitionMotion(D("1"), D(".5"), D("-1"))


def test_channels_close_rate_productization_upmarket_price_and_reuse():
    base, referral = baseline_case(), warm_referral_case()
    close, product = higher_close_rate_case(), productized_sales_case()
    larger, price = larger_customer_case(), higher_price_only_case()
    reuse, channel = very_high_reuse_case(), partner_channel_case()
    assert referral.result.verdict is Verdict.PROMISING
    assert referral.scenario.delivery == base.scenario.delivery
    assert close.acquisition_cost < base.acquisition_cost
    assert close.contribution_after_acquisition > base.contribution_after_acquisition
    assert product.result.verdict is Verdict.PROMISING and product.acquisition.sales_reuse > base.acquisition.sales_reuse
    assert larger.result.verdict is Verdict.PROMISING and larger.contribution_after_acquisition > 0
    assert first_year_roi(price.scenario.customer) < first_year_roi(base.scenario.customer)
    assert price.result.verdict is Verdict.NO_DEAL
    assert reuse.delivery_cost < base.delivery_cost and reuse.result.verdict is Verdict.POOR_TARGET
    assert channel.acquisition.channel_cost == D("700")
    assert channel.acquisition_cost > channel.expected_sales_hours * channel.scenario.solutions.hourly_cost
    assert channel.result.verdict is Verdict.PROMISING


def test_sensitivity_sales_reuse_comparisons_and_fourteen_rows_are_stable():
    assert scenario_results() == scenario_results() and len(scenario_results()) == 8
    assert close_rate_sensitivity() == close_rate_sensitivity()
    rows = close_rate_sensitivity()
    assert [r[1] for r in rows] == sorted((r[1] for r in rows), reverse=True)
    case = baseline_case()
    assert reuse_percentage(case.scenario.delivery) == D(".8")
    assert case.acquisition.sales_reuse == D(".25")
    assert case_13_vs_14() == case_13_vs_14()
    assert case_13_vs_14()[0][-1] == "BUILD" and case_13_vs_14()[1][-1] == "ACQUIRE"
    assert case_9_vs_14() == case_9_vs_14()
    comparison = implemented_case_comparison()
    assert len(comparison) == 14 and comparison[-1].name == "Bad sales motion"
    assert comparison[-1].verdict == Verdict.POOR_TARGET.value
