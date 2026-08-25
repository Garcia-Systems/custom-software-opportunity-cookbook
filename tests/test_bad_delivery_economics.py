from dataclasses import FrozenInstanceError
from decimal import Decimal as D

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.bad_delivery_economics import (WorkflowBurden,
    baseline_case, better_integration_access_case, case_12_vs_13,
    case_7_vs_13, high_bespoke_logic_case, one_off_viable_case,
    paid_discovery_case, raise_price_only_case, reduced_scope_case,
    reusable_adapters_case, scenario_results)
from opportunity_cookbook.economics import (annual_support_cost,
    customer_maximum_economic_price, delivery_break_even_price,
    first_year_roi, has_feasible_price_corridor, implementation_contribution,
    payback_period_months, recurring_support_contribution, reuse_percentage,
    target_contribution_price)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison
from opportunity_cookbook.verdicts import Verdict


def test_burden_recovery_customer_economics_and_determinism():
    case = baseline_case()
    assert case == baseline_case()
    assert case.total_burden == D("93444")
    assert case.recoverable_value == D("48589.84")
    assert first_year_roi(case.scenario.customer) == D("0.7996237037037037037037037037")
    assert payback_period_months(case.scenario.customer) == D("5.770640137110409657743333468")
    with pytest.raises(FrozenInstanceError):
        case.scenario.business_name = "changed"


def test_baseline_delivery_contribution_corridor_support_and_verdict():
    case = baseline_case()
    assert case.base_engineering_hours == D("408")
    assert case.total_engineering_hours == D("620")
    assert case.direct_delivery_cost == D("45200")
    assert case.implementation_contribution == D("-25200")
    assert case.break_even_price == D("45200")
    assert case.target_price == D("51200")
    assert case.customer_maximum_price == D("27589.84")
    assert not case.feasible_price_corridor
    assert annual_support_cost(case.scenario.delivery) == D("6840")
    assert recurring_support_contribution(case.scenario.customer,
        case.scenario.delivery) == D("160")
    result = analyze(case.scenario)
    assert result.verdict is Verdict.NO_DEAL
    assert result.reasons == (
        "Implementation price does not cover delivery and solutions labor costs.",)


def test_generic_price_and_contribution_calculations_and_validation():
    assert implementation_contribution(D("18000"), D("26000")) == D("-8000")
    assert delivery_break_even_price(D("26000")) == D("26000")
    assert target_contribution_price(D("26000"), D("6000")) == D("32000")
    assert customer_maximum_economic_price(D("42000"), D("5000"), D("12000")) == D("25000")
    assert not has_feasible_price_corridor(D("32000"), D("25000"))
    assert has_feasible_price_corridor(D("22000"), D("25000"))
    for call in (lambda: implementation_contribution(D("-1"), D("1")),
                 lambda: delivery_break_even_price(D("-1")),
                 lambda: target_contribution_price(D("1"), D("-1")),
                 lambda: customer_maximum_economic_price(D("1"), D("-1"), D("0")),
                 lambda: has_feasible_price_corridor(D("-1"), D("1"))):
        with pytest.raises(ValueError): call()


def test_raise_price_only_damages_customer_economics():
    base, raised = baseline_case(), raise_price_only_case()
    assert raised.implementation_contribution > 0
    assert first_year_roi(raised.scenario.customer) < first_year_roi(base.scenario.customer)
    assert analyze(raised.scenario).verdict is Verdict.NO_DEAL
    assert not raised.feasible_price_corridor


def test_scope_access_and_reuse_change_real_delivery_effort():
    base, scoped = baseline_case(), reduced_scope_case()
    access, adapters = better_integration_access_case(), reusable_adapters_case()
    assert scoped.recoverable_value < base.recoverable_value
    assert scoped.direct_delivery_cost < base.direct_delivery_cost
    assert scoped.feasible_price_corridor
    assert access.direct_delivery_cost < base.direct_delivery_cost
    assert access.feasible_price_corridor
    assert adapters.total_engineering_hours < base.total_engineering_hours
    assert adapters.direct_delivery_cost < base.direct_delivery_cost


def test_bespoke_discovery_one_off_and_speculative_reuse_guardrail():
    base, bespoke = baseline_case(), high_bespoke_logic_case()
    discovery, one_off = paid_discovery_case(), one_off_viable_case()
    assert bespoke.scenario.delivery.customer_specific_engineering_hours > base.scenario.delivery.customer_specific_engineering_hours
    assert bespoke.direct_delivery_cost > base.direct_delivery_cost
    assert discovery.scenario.delivery.uncertainty_reserve_hours < base.scenario.delivery.uncertainty_reserve_hours
    assert discovery.implementation_contribution < 0
    assert analyze(discovery.scenario).verdict is Verdict.INVESTIGATE
    assert discovery.discovery_price == D("6000")
    assert analyze(one_off.scenario).verdict is Verdict.ONE_OFF
    assert one_off.implementation_contribution > 0
    assert reuse_percentage(one_off.scenario.delivery) < D(".40")
    # Hypothetical later reuse is not revenue or contribution in the actual engagement.
    assert baseline_case().implementation_contribution == D("-25200")
    assert analyze(baseline_case().scenario).verdict is Verdict.NO_DEAL


def test_scenarios_cross_case_comparisons_and_implemented_rows_are_stable():
    assert scenario_results() == scenario_results()
    assert len(scenario_results()) == 8
    assert scenario_results()[0][1] == Verdict.NO_DEAL.value
    assert scenario_results()[-1][1] == Verdict.ONE_OFF.value
    assert case_12_vs_13() == case_12_vs_13()
    assert case_12_vs_13()[0][1] == Verdict.BUY_CONFIGURE.value
    assert case_12_vs_13()[1][1] == Verdict.NO_DEAL.value
    assert case_7_vs_13() == case_7_vs_13()
    rows = implemented_case_comparison()
    assert len(rows) == 14
    assert rows[-2].name == "Bad delivery economics"
    assert rows[-1].name == "Bad sales motion"
    assert rows[-2].verdict == Verdict.NO_DEAL.value


@pytest.mark.parametrize("hours,cost,rate", [(D("-1"), D("1"), D(".5")),
    (D("1"), D("-1"), D(".5")), (D("1"), D("1"), D("1.01"))])
def test_invalid_burden_assumptions_are_rejected(hours, cost, rate):
    with pytest.raises(ValueError):
        WorkflowBurden("bad", hours, cost, rate)
