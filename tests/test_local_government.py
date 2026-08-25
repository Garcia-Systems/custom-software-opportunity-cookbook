from dataclasses import FrozenInstanceError
from decimal import Decimal as D
import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    effective_contribution_per_solutions_hour, implementation_delivery_cost,
    recurring_support_contribution, reuse_percentage, solutions_contribution,
    solutions_hours)
from opportunity_cookbook.local_government import (GovernmentBurden, baseline_case,
    case_seven_vs_nine, closed_legacy_integration_case, cooperative_pilot_case,
    existing_vendor_module_case, formal_rfp_case, high_contract_value_case,
    reusable_technical_hard_sales_case)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison
from opportunity_cookbook.verdicts import Verdict


def test_government_burden_and_recovery_are_explicit():
    item = GovernmentBurden("lookup", D("100"), D("40"), D(".5"))
    assert item.annual_burden == D("4000") and item.recoverable == D("2000.0")
    case = baseline_case()
    assert case.total_burden == D("201232")
    assert case.recoverable_value == D("104002.80")
    assert case.scenario.customer.current_state_annual_burden == case.total_burden


def test_baseline_is_deterministic_immutable_and_poor_target_is_traceable():
    case = baseline_case()
    assert case == baseline_case()
    result = analyze(case.scenario)
    assert result.verdict is Verdict.POOR_TARGET and len(result.reasons) == 4
    assert any("Procurement" in reason for reason in result.reasons)
    assert result.verdict is not Verdict.NO_DEAL
    with pytest.raises(FrozenInstanceError): case.custom_risk_allowance = D("1")


def test_delivery_security_sales_and_support_are_included():
    case = baseline_case(); s = case.scenario
    assert case.engineering.total_hours == D("522")
    assert case.engineering.security_accessibility_hours == D("68")
    assert implementation_delivery_cost(s.delivery) == D("53090")
    assert solutions_hours(s.solutions) == case.procurement.total_hours == D("192")
    assert solutions_contribution(s.customer, s.delivery, s.solutions) == D("9550")
    assert effective_contribution_per_solutions_hour(s.customer, s.delivery, s.solutions) < D("50")
    assert annual_support_cost(s.delivery) == case.support.annual_cost == D("21050")
    assert recurring_support_contribution(s.customer, s.delivery) == D("2950")


def test_procurement_scenarios_materially_change_sales_economics():
    pilot, baseline, rfp = cooperative_pilot_case(), baseline_case(), formal_rfp_case()
    assert analyze(pilot.scenario).verdict is Verdict.PROMISING
    assert analyze(rfp.scenario).verdict is Verdict.POOR_TARGET
    assert solutions_hours(pilot.scenario.solutions) < solutions_hours(baseline.scenario.solutions) < solutions_hours(rfp.scenario.solutions)
    assert effective_contribution_per_solutions_hour(pilot.scenario.customer, pilot.scenario.delivery, pilot.scenario.solutions) > effective_contribution_per_solutions_hour(baseline.scenario.customer, baseline.scenario.delivery, baseline.scenario.solutions)
    assert effective_contribution_per_solutions_hour(rfp.scenario.customer, rfp.scenario.delivery, rfp.scenario.solutions) < D("2")


def test_value_access_alternative_and_reuse_scenarios_follow_ordered_gates():
    high = high_contract_value_case()
    assert analyze(high.scenario).verdict is Verdict.POOR_TARGET
    assert solutions_contribution(high.scenario.customer, high.scenario.delivery, high.scenario.solutions) > solutions_contribution(baseline_case().scenario.customer, baseline_case().scenario.delivery, baseline_case().scenario.solutions)
    assert analyze(closed_legacy_integration_case().scenario).verdict is Verdict.NO_DEAL
    assert analyze(existing_vendor_module_case().scenario).verdict is Verdict.BUY_CONFIGURE
    reuse = reusable_technical_hard_sales_case()
    assert reuse_percentage(reuse.scenario.delivery) > D(".75")
    assert analyze(reuse.scenario).verdict is Verdict.POOR_TARGET


def test_case_seven_nine_and_nine_case_comparison_are_deterministic():
    comparison = case_seven_vs_nine()
    assert comparison == case_seven_vs_nine()
    assert comparison.construction_verdict == "PROMISING — VALIDATE IN DISCOVERY"
    assert comparison.government_verdict == "POOR TARGET CUSTOMER"
    assert comparison.government_solutions_hours > comparison.construction_solutions_hours
    rows = implemented_case_comparison()
    assert len(rows) == 10 and rows[-2].name == "Local government"
    assert rows[-2].sales_procurement_difficulty == "high"


@pytest.mark.parametrize("units,cost,rate", [(D("-1"), D("1"), D(".5")), (D("1"), D("-1"), D(".5")), (D("1"), D("1"), D("1.1"))])
def test_invalid_assumptions_are_rejected(units, cost, rate):
    with pytest.raises(ValueError): GovernmentBurden("bad", units, cost, rate)
