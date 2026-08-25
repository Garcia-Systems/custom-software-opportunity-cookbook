from dataclasses import FrozenInstanceError
from decimal import Decimal as D

import pytest

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.construction_trades import (BillingTimingBurden,
    HandoffBurden, baseline_case, clean_integrations_case,
    difficult_integrations_case, existing_saas_case, high_burden_case,
    highly_customer_specific_case, low_burden_case,
    unsustainable_support_case)
from opportunity_cookbook.economics import (annual_support_cost,
    implementation_delivery_cost, recurring_support_contribution,
    reuse_percentage, solutions_contribution, solutions_hours)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison
from opportunity_cookbook.verdicts import Verdict


def test_handoff_burden_and_recoverable_value_are_transparent_and_derived():
    burden = HandoffBurden("entry", D("100"), D("40"), D(".6"))
    assert burden.annual_burden == D("4000")
    assert burden.recoverable == D("2400.0")
    case = baseline_case()
    assert case.total_burden == D("130584.2191780821917808219178")
    assert case.recoverable_value == D("64619.28767123287671232876712")
    assert case.scenario.customer.current_state_annual_burden == case.total_burden
    assert case.scenario.customer.recoverable_value == case.recoverable_value


def test_billing_delay_counts_financing_cost_not_invoice_principal():
    timing = BillingTimingBurden(D("2400000"), D("8"), D(".08"), D(".4"))
    assert timing.annual_burden == D("2400000") * D("8") / D("365") * D(".08")
    assert timing.recoverable == timing.annual_burden * D(".4")
    assert timing.recoverable < timing.annual_invoice_flow * D(".001")


def test_baseline_is_deterministic_immutable_and_framework_derived():
    case = baseline_case()
    assert case == baseline_case()
    result = analyze(case.scenario)
    assert result.verdict is Verdict.PROMISING
    assert result.reasons == (
        "Customer value, delivery contribution, and recurring support economics work under the assumptions.",
        "At least 40% of core engineering work is modeled as demonstrably reusable.",
        "Promising is an economic hypothesis; market validation still requires discovery.",)
    with pytest.raises(FrozenInstanceError):
        case.custom_risk_allowance = D("0")


def test_reliability_delivery_solutions_support_and_reuse_are_derived():
    case = baseline_case(); s = case.scenario; e = case.engineering
    assert e.reliability_error_handling == D("48")
    assert e.qa_testing == D("54")
    assert e.total_hours == D("466")
    assert implementation_delivery_cost(s.delivery) == D("42110")
    assert solutions_hours(s.solutions) == case.solutions_work.total_hours == D("88")
    assert solutions_contribution(s.customer, s.delivery, s.solutions) == D("1730")
    assert annual_support_cost(s.delivery) == case.support.annual_cost == D("10820")
    assert recurring_support_contribution(s.customer, s.delivery) == D("1180")
    assert reuse_percentage(s.delivery) == D("190") / D("360")


def test_integration_access_materially_changes_delivery_and_support():
    base = baseline_case(); clean = clean_integrations_case(); difficult = difficult_integrations_case()
    assert implementation_delivery_cost(clean.scenario.delivery) < implementation_delivery_cost(base.scenario.delivery)
    assert annual_support_cost(clean.scenario.delivery) < annual_support_cost(base.scenario.delivery)
    assert analyze(clean.scenario).verdict is Verdict.PROMISING
    assert implementation_delivery_cost(difficult.scenario.delivery) > implementation_delivery_cost(base.scenario.delivery)
    assert annual_support_cost(difficult.scenario.delivery) > annual_support_cost(base.scenario.delivery)
    assert analyze(difficult.scenario).verdict is Verdict.NO_DEAL


def test_burden_saas_specificity_and_support_scenarios():
    assert high_burden_case().recoverable_value > baseline_case().recoverable_value
    assert analyze(high_burden_case().scenario).verdict is Verdict.PROMISING
    assert low_burden_case().recoverable_value < baseline_case().recoverable_value
    assert analyze(low_burden_case().scenario).verdict is Verdict.NO_DEAL
    assert analyze(existing_saas_case().scenario).verdict is Verdict.BUY_CONFIGURE
    specific = highly_customer_specific_case()
    assert reuse_percentage(specific.scenario.delivery) < D(".4")
    assert analyze(specific.scenario).verdict is Verdict.ONE_OFF
    unsupported = unsustainable_support_case()
    assert annual_support_cost(unsupported.scenario.delivery) > unsupported.scenario.customer.recurring_annual_fee
    assert analyze(unsupported.scenario).verdict is Verdict.NO_DEAL


def test_verdict_reasons_remain_traceable_and_comparison_has_case_7():
    assert all(analyze(factory().scenario).reasons for factory in (
        baseline_case, clean_integrations_case, difficult_integrations_case,
        existing_saas_case, high_burden_case, low_burden_case,
        highly_customer_specific_case, unsustainable_support_case))
    rows = implemented_case_comparison()
    assert len(rows) == 14
    assert rows[6].name == "Construction / trades"
    assert rows[6].recoverable_value == baseline_case().recoverable_value


@pytest.mark.parametrize("units,cost", [(D("-1"), D("1")), (D("1"), D("-1"))])
def test_negative_handoff_assumptions_are_rejected(units, cost):
    with pytest.raises(ValueError, match="negative"):
        HandoffBurden("bad", units, cost, D(".5"))


@pytest.mark.parametrize("rate", [D("-.01"), D("1.01")])
def test_invalid_improvement_percentages_are_rejected(rate):
    with pytest.raises(ValueError, match="between 0 and 1"):
        HandoffBurden("bad", D("1"), D("1"), rate)
    with pytest.raises(ValueError, match="between 0 and 1"):
        BillingTimingBurden(D("1"), D("1"), D(".1"), rate)
