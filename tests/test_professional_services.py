from dataclasses import FrozenInstanceError
from decimal import Decimal as D

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (alternative_first_year_effect,
    annual_support_cost, implementation_delivery_cost, reuse_percentage,
    solutions_contribution, solutions_hours)
from opportunity_cookbook.professional_services import (AdministrativeBurden,
    baseline_case, case_seven_vs_eight, genuine_cross_system_gap_case,
    high_administrative_burden_case, low_administrative_burden_case,
    poorly_configured_tools_case, speculative_utilization_upside_case,
    strong_repeatability_strong_saas_case, unique_billing_workflow_case)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison
from opportunity_cookbook.verdicts import Verdict


def test_burdens_and_recoverable_value_are_explicitly_derived():
    burden = AdministrativeBurden("report", D("100"), D("50"), D(".4"))
    assert burden.annual_burden == D("5000")
    assert burden.recoverable == D("2000.0")
    case = baseline_case()
    assert case.total_burden == D("121912")
    assert case.burden_recovery == case.recoverable_value == D("60410.40")
    assert case.scenario.customer.current_state_annual_burden == case.total_burden


def test_baseline_is_deterministic_immutable_and_configuration_wins_by_economics():
    case = baseline_case()
    assert case == baseline_case()
    assert analyze(case.scenario).verdict is Verdict.BUY_CONFIGURE
    assert alternative_first_year_effect(case.alternative) == D("74000")
    assert analyze(case.scenario).reasons == (
        "An existing buy/configure alternative adequately meets the need at materially lower cost or risk.",)
    with pytest.raises(FrozenInstanceError):
        case.speculative_utilization_upside = D("1")


def test_configuration_gap_and_burden_scenarios_move_the_decision():
    assert analyze(poorly_configured_tools_case().scenario).verdict is Verdict.BUY_CONFIGURE
    assert analyze(genuine_cross_system_gap_case().scenario).verdict is Verdict.PROMISING
    assert analyze(high_administrative_burden_case().scenario).verdict is Verdict.PROMISING
    assert high_administrative_burden_case().recoverable_value > baseline_case().recoverable_value
    assert analyze(low_administrative_burden_case().scenario).verdict is Verdict.BUY_CONFIGURE
    assert low_administrative_burden_case().recoverable_value < baseline_case().recoverable_value


def test_unique_workflow_can_be_one_off_and_reuse_cannot_override_saas():
    unique = unique_billing_workflow_case()
    assert analyze(unique.scenario).verdict is Verdict.ONE_OFF
    assert reuse_percentage(unique.scenario.delivery) < D(".4")
    repeatable = strong_repeatability_strong_saas_case()
    assert reuse_percentage(repeatable.scenario.delivery) > D(".6")
    assert analyze(repeatable.scenario).verdict is Verdict.BUY_CONFIGURE


def test_speculative_utilization_upside_is_separate_and_does_not_drive_baseline():
    baseline, speculative = baseline_case(), speculative_utilization_upside_case()
    assert baseline.speculative_utilization_upside == 0
    assert speculative.burden_recovery == baseline.burden_recovery
    assert speculative.recoverable_value - baseline.recoverable_value == D("18000")
    assert analyze(speculative.scenario).verdict is Verdict.BUY_CONFIGURE


def test_delivery_solutions_and_support_economics_are_derived():
    case = baseline_case(); scenario = case.scenario
    assert case.engineering.total_hours == D("478")
    assert implementation_delivery_cost(scenario.delivery) == D("42630")
    assert solutions_hours(scenario.solutions) == case.solutions_work.total_hours == D("88")
    assert solutions_contribution(scenario.customer, scenario.delivery, scenario.solutions) == D("3210")
    assert case.support.annual_cost == annual_support_cost(scenario.delivery) == D("10720")


def test_case_seven_eight_and_eight_case_comparisons_are_calculated_and_deterministic():
    comparison = case_seven_vs_eight()
    assert comparison == case_seven_vs_eight()
    assert comparison.construction_verdict == "PROMISING — VALIDATE IN DISCOVERY"
    assert comparison.professional_services_verdict == "BUY / CONFIGURE"
    assert comparison.construction_alternative_effect > comparison.professional_services_alternative_effect
    rows = implemented_case_comparison()
    assert len(rows) == 14
    assert rows[7].name == "Professional services"
    assert rows[7].recoverable_value == baseline_case().recoverable_value


def test_all_verdict_reasons_are_traceable():
    factories = (baseline_case, poorly_configured_tools_case,
        genuine_cross_system_gap_case, high_administrative_burden_case,
        low_administrative_burden_case, unique_billing_workflow_case,
        strong_repeatability_strong_saas_case, speculative_utilization_upside_case)
    assert all(analyze(factory().scenario).reasons for factory in factories)


@pytest.mark.parametrize("units,cost", [(D("-1"), D("1")), (D("1"), D("-1"))])
def test_negative_assumptions_are_rejected(units, cost):
    with pytest.raises(ValueError, match="negative"):
        AdministrativeBurden("bad", units, cost, D(".5"))


@pytest.mark.parametrize("rate", [D("-.01"), D("1.01")])
def test_invalid_improvement_percentages_are_rejected(rate):
    with pytest.raises(ValueError, match="between 0 and 1"):
        AdministrativeBurden("bad", D("1"), D("1"), rate)
