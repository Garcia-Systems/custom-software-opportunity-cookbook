from dataclasses import FrozenInstanceError
from decimal import Decimal as D

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.buy_dont_build import (WorkflowBurden, baseline_case,
    cheap_custom_case, expensive_saas_case, large_unique_gap_case,
    saas_support_burden_case, scenario_results, small_unique_gap_case,
    weak_saas_case)
from opportunity_cookbook.economics import (alternative_recovered_burden,
    annual_support_cost, implementation_delivery_cost, recurring_support_contribution,
    solutions_contribution)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison
from opportunity_cookbook.verdicts import Verdict


def test_initial_burden_recovery_and_stage_one_are_deterministic():
    case = baseline_case()
    assert case == baseline_case()
    assert case.total_burden == D("67652")
    assert case.recoverable_value == D("41826.20")
    assert analyze(case.stage_one).verdict is Verdict.PROMISING
    with pytest.raises(FrozenInstanceError):
        case.stage_one.business_name = "changed"


def test_stage_one_delivery_solutions_support_and_reuse_are_real_economics():
    scenario = baseline_case().stage_one
    assert implementation_delivery_cost(scenario.delivery) == D("8690")
    assert solutions_contribution(scenario.customer, scenario.delivery,
        scenario.solutions) == D("1360")
    assert annual_support_cost(scenario.delivery) == D("2000")
    assert recurring_support_contribution(scenario.customer, scenario.delivery) == D("1000")


def test_saas_residual_and_incremental_value_are_distinct():
    case = baseline_case()
    assert alternative_recovered_burden(case.total_burden,
        case.saas.residual_annual_burden) == D("37643.58")
    assert case.incremental_custom_value == D("4182.62")
    assert case.recoverable_value != case.incremental_custom_value


def test_strong_saas_changes_final_verdict_and_comparison_uses_it():
    case = baseline_case()
    assert analyze(case.final_scenario).verdict is Verdict.BUY_CONFIGURE
    assert case.recommendation == "Buy / configure"
    rows = implemented_case_comparison()
    assert len(rows) == 14
    assert rows[11].name == "Perfect-looking deal"
    assert rows[11].verdict == Verdict.BUY_CONFIGURE.value
    assert rows[11].verdict != analyze(case.stage_one).verdict.value


def test_weak_and_expensive_saas_make_custom_competitive_again():
    assert analyze(weak_saas_case().final_scenario).verdict is Verdict.PROMISING
    assert weak_saas_case().recommendation == "Full custom"
    assert analyze(expensive_saas_case().final_scenario).verdict is Verdict.PROMISING
    assert expensive_saas_case().recommendation == "Full custom"


def test_small_and_large_unique_gaps_are_separate_from_full_custom():
    assert small_unique_gap_case().recommendation == "Buy / configure"
    large = large_unique_gap_case()
    assert large.recommendation == "SaaS + narrow custom edge"
    assert large.options()[3].first_year_net_benefit > large.options()[1].first_year_net_benefit


def test_cheap_custom_still_competes_against_alternative():
    case = cheap_custom_case()
    assert case.stage_one.customer.implementation_price == D("7000")
    assert case.recommendation == "Buy / configure"
    assert analyze(case.final_scenario).verdict is Verdict.BUY_CONFIGURE


def test_saas_administration_is_included_and_can_change_comparison():
    base, burdened = baseline_case(), saas_support_burden_case()
    assert burdened.saas.internal_administration_cost == D("15000")
    assert burdened.options()[2].first_year_cost > base.options()[2].first_year_cost
    assert burdened.recommendation == "Full custom"


def test_break_even_is_deterministic_and_explainable():
    case = baseline_case()
    assert case.break_even_residual_burden == D("31225.80")
    assert case.saas.residual_annual_burden < case.break_even_residual_burden


def test_all_eight_scenarios_are_immutable_and_deterministic():
    assert scenario_results() == scenario_results()
    assert len(scenario_results()) == 8
    assert scenario_results()[0][1] == Verdict.PROMISING.value
    assert scenario_results()[1][1] == Verdict.BUY_CONFIGURE.value


@pytest.mark.parametrize("hours,cost,rate", [(D("-1"), D("1"), D(".5")),
    (D("1"), D("-1"), D(".5")), (D("1"), D("1"), D("1.01"))])
def test_invalid_negative_or_percentage_inputs_are_rejected(hours, cost, rate):
    with pytest.raises(ValueError):
        WorkflowBurden("bad", hours, cost, rate)
