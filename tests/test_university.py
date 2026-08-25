from dataclasses import FrozenInstanceError
from decimal import Decimal as D
import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    effective_contribution_per_solutions_hour, implementation_delivery_cost,
    recurring_support_contribution, reuse_percentage, solutions_contribution,
    solutions_hours)
from opportunity_cookbook.models import Level
from opportunity_cookbook.tourism_attraction import implemented_case_comparison
from opportunity_cookbook.university import (AuthorityMap, UniversityBurden,
    approved_exports_only_case, baseline_case, case_nine_vs_ten,
    centrally_sponsored_case, department_only_champion_case, existing_bi_tool_case,
    high_reuse_unique_governance_case, higher_contract_value_case)
from opportunity_cookbook.verdicts import Verdict


def test_university_burden_and_recoverable_value_are_explicit():
    item = UniversityBurden("reconciliation", D("100"), D("40"), D(".5"))
    assert item.annual_burden == D("4000")
    assert item.recoverable == D("2000.0")
    case = baseline_case()
    assert case.total_burden == D("199448")
    assert case.recoverable_value == D("105727.00")
    assert case.scenario.customer.recoverable_value == case.recoverable_value


def test_baseline_is_deterministic_immutable_and_authority_is_fragmented():
    case = baseline_case()
    assert case == baseline_case()
    assert case.authority.system_control is Level.LOW
    assert case.authority.integration_approval_difficulty is Level.HIGH
    assert case.authority.integration_approved
    assert analyze(case.scenario).verdict is Verdict.POOR_TARGET
    assert analyze(case.scenario).verdict is not Verdict.NO_DEAL
    with pytest.raises(FrozenInstanceError): case.scope = "changed"


def test_delivery_governance_and_support_economics_are_included():
    case = baseline_case(); scenario = case.scenario
    assert case.engineering.total_hours == D("528")
    assert case.engineering.security_access_hours == D("92")
    assert implementation_delivery_cost(scenario.delivery) == D("54160")
    assert solutions_hours(scenario.solutions) == case.governance.total_hours == D("208")
    assert solutions_contribution(scenario.customer, scenario.delivery, scenario.solutions) == D("7200")
    assert effective_contribution_per_solutions_hour(scenario.customer, scenario.delivery, scenario.solutions) < D("50")
    assert annual_support_cost(scenario.delivery) == case.support.annual_cost == D("20875")
    assert recurring_support_contribution(scenario.customer, scenario.delivery) == D("3125")


def test_authority_scenarios_change_the_opportunity_without_bypassing_controls():
    central = centrally_sponsored_case()
    department = department_only_champion_case()
    exports = approved_exports_only_case()
    assert analyze(central.scenario).verdict is Verdict.PROMISING
    assert central.authority.integration_approved
    assert not department.authority.integration_approved
    assert analyze(department.scenario).verdict is Verdict.NO_DEAL
    assert department.scenario.technical.feasibility.value == "feasible"
    assert solutions_hours(department.scenario.solutions) > solutions_hours(baseline_case().scenario.solutions)
    assert "read-only" in exports.scope and exports.authority.integration_approved
    assert analyze(exports.scenario).verdict is Verdict.PROMISING
    assert exports.scenario.delivery.customer_specific_engineering_hours < baseline_case().scenario.delivery.customer_specific_engineering_hours


def test_alternative_price_and_reuse_scenarios_follow_framework_gates():
    assert analyze(existing_bi_tool_case().scenario).verdict is Verdict.BUY_CONFIGURE
    high = higher_contract_value_case()
    assert solutions_contribution(high.scenario.customer, high.scenario.delivery, high.scenario.solutions) > solutions_contribution(baseline_case().scenario.customer, baseline_case().scenario.delivery, baseline_case().scenario.solutions)
    assert analyze(high.scenario).verdict is Verdict.POOR_TARGET
    reuse = high_reuse_unique_governance_case()
    assert reuse_percentage(reuse.scenario.delivery) > D(".75")
    assert analyze(reuse.scenario).verdict is Verdict.POOR_TARGET


def test_unauthorized_access_is_rejected_and_not_confused_with_feasibility():
    values = dict(problem_owner="department", budget_owner="school",
        system_owner="central IT", data_owner="institution",
        security_approver="security", integration_approver="central IT",
        procurement="purchasing", end_users="staff", buyer_authority=Level.LOW,
        system_control=Level.LOW, integration_approval_difficulty=Level.HIGH,
        integration_approved=False)
    with pytest.raises(ValueError): AuthorityMap(**values, unauthorized_access_allowed=True)
    assert baseline_case().scenario.technical.feasibility.value == "feasible"


def test_case_nine_ten_and_implemented_comparison_are_deterministic():
    comparison = case_nine_vs_ten()
    assert comparison == case_nine_vs_ten()
    assert comparison.university_solutions_hours > comparison.government_solutions_hours
    assert comparison.university_permission_difficulty == "high"
    rows = implemented_case_comparison()
    assert len(rows) == 14 and rows[9].name == "University department"


@pytest.mark.parametrize("units,cost,rate", [(D("-1"), D("1"), D(".5")),
    (D("1"), D("-1"), D(".5")), (D("1"), D("1"), D("1.1"))])
def test_invalid_negative_or_rate_assumptions_are_rejected(units, cost, rate):
    with pytest.raises(ValueError): UniversityBurden("bad", units, cost, rate)
