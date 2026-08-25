from dataclasses import FrozenInstanceError
from decimal import Decimal as D
from pathlib import Path

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    implementation_delivery_cost, recurring_support_contribution,
    reuse_percentage, solutions_contribution, solutions_hours)
from opportunity_cookbook.healthcare import (AdministrativeBurden,
    BASELINE_BURDENS, CASE_NINE_TEN_ELEVEN_PROGRESSION, baseline_case,
    case_seven_vs_eleven, difficult_proprietary_integration_case,
    high_customer_value_case, high_reuse_high_validation_case,
    narrow_read_only_case, underpriced_support_case, unresolved_access_case,
    vendor_supported_interfaces_case, vendor_supported_product_case)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison
from opportunity_cookbook.verdicts import Verdict


def test_administrative_burden_and_recovery_are_explicit():
    item = AdministrativeBurden("admin", D("100"), D("40"), D(".5"))
    assert item.annual_burden == D("4000")
    assert item.recoverable == D("2000.0")
    case = baseline_case()
    assert case.total_burden == D("315080")
    assert case.recoverable_value == D("155026.00")
    assert case.scenario.customer.recoverable_value == case.recoverable_value


def test_baseline_is_deterministic_immutable_and_framework_derived():
    case = baseline_case()
    assert case == baseline_case()
    result = analyze(case.scenario)
    assert result.verdict is Verdict.NO_DEAL
    assert result.reasons == ("The customer does not recover implementation price within one year.",)
    with pytest.raises(FrozenInstanceError): case.scope = "changed"


def test_security_validation_uncertainty_and_delivery_are_transparent():
    case = baseline_case(); e = case.engineering
    assert e.security_privacy == D("82")
    assert e.integration_validation == D("72")
    assert e.validation_reconciliation + e.testing == D("196")
    assert e.rework_reserve == D("72")
    assert e.integration_uncertainty_reserve == D("90")
    assert e.total_hours == D("946")
    assert implementation_delivery_cost(case.scenario.delivery) == D("105830")
    assert case.scenario.delivery.uncertainty_reserve_hours == D("90")


def test_solutions_reuse_and_support_economics_are_explicit():
    case = baseline_case(); scenario = case.scenario
    assert solutions_hours(scenario.solutions) == case.solutions_work.total_hours == D("196")
    assert solutions_contribution(scenario.customer, scenario.delivery, scenario.solutions) == D("3510")
    assert annual_support_cost(scenario.delivery) == case.support.annual_cost == D("34350")
    assert recurring_support_contribution(scenario.customer, scenario.delivery) == D("3650")
    assert scenario.delivery.reusable_engineering_hours == D("190")
    assert scenario.delivery.customer_specific_engineering_hours == D("364")


def test_interface_and_difficult_integration_scenarios_move_economics():
    base = baseline_case(); supported = vendor_supported_interfaces_case()
    difficult = difficult_proprietary_integration_case()
    assert analyze(supported.scenario).verdict is Verdict.PROMISING
    assert supported.engineering.integration_uncertainty_reserve < base.engineering.integration_uncertainty_reserve
    assert implementation_delivery_cost(supported.scenario.delivery) < implementation_delivery_cost(base.scenario.delivery)
    assert analyze(difficult.scenario).verdict is Verdict.NO_DEAL
    assert implementation_delivery_cost(difficult.scenario.delivery) > implementation_delivery_cost(base.scenario.delivery)
    assert annual_support_cost(difficult.scenario.delivery) > annual_support_cost(base.scenario.delivery)


def test_high_value_does_not_cancel_delivery_and_vendor_product_can_win():
    high = high_customer_value_case()
    assert high.recoverable_value > baseline_case().recoverable_value
    assert high.engineering == baseline_case().engineering
    assert analyze(high.scenario).verdict is Verdict.POOR_TARGET
    assert analyze(vendor_supported_product_case().scenario).verdict is Verdict.BUY_CONFIGURE
    assert analyze(unresolved_access_case().scenario).verdict is Verdict.INVESTIGATE


def test_underpriced_support_weakens_an_otherwise_attractive_implementation():
    case = underpriced_support_case()
    assert solutions_contribution(case.scenario.customer, case.scenario.delivery,
        case.scenario.solutions) > 0
    assert recurring_support_contribution(case.scenario.customer, case.scenario.delivery) < 0
    assert analyze(case.scenario).verdict is Verdict.NO_DEAL


def test_narrow_scope_reduces_value_delivery_and_support_burden():
    base, narrow = baseline_case(), narrow_read_only_case()
    assert narrow.recoverable_value < base.recoverable_value
    assert narrow.engineering.total_hours < base.engineering.total_hours
    assert annual_support_cost(narrow.scenario.delivery) < annual_support_cost(base.scenario.delivery)
    assert "read-only" in narrow.scope
    assert analyze(narrow.scenario).verdict is Verdict.PROMISING


def test_high_reuse_does_not_erase_customer_validation():
    case = high_reuse_high_validation_case()
    assert reuse_percentage(case.scenario.delivery) > D(".5")
    assert case.engineering.validation_reconciliation + case.engineering.testing == D("310")
    assert analyze(case.scenario).verdict is Verdict.NO_DEAL


def test_no_clinical_benefit_or_patient_fixture_and_comparisons_are_deterministic():
    assert all("administrative" in b.basis for b in BASELINE_BURDENS)
    source = Path("src/opportunity_cookbook/healthcare.py").read_text()
    assert "patient_name" not in source and "date_of_birth" not in source
    comparison = case_seven_vs_eleven()
    assert comparison == case_seven_vs_eleven()
    assert comparison.healthcare_value > comparison.construction_value
    assert comparison.healthcare_support_cost > comparison.construction_support_cost
    assert CASE_NINE_TEN_ELEVEN_PROGRESSION[0].startswith("Case 9: the project")
    assert "authority and governance" in CASE_NINE_TEN_ELEVEN_PROGRESSION[1]
    assert "delivery and support complexity" in CASE_NINE_TEN_ELEVEN_PROGRESSION[2]
    rows = implemented_case_comparison()
    assert len(rows) == 12 and rows[-2].name == "Healthcare organization"


@pytest.mark.parametrize("units,cost,rate", [(D("-1"), D("1"), D(".5")),
    (D("1"), D("-1"), D(".5")), (D("1"), D("1"), D("1.1"))])
def test_invalid_negative_or_rate_assumptions_are_rejected(units, cost, rate):
    with pytest.raises(ValueError): AdministrativeBurden("bad", units, cost, rate)
