from dataclasses import replace
from decimal import Decimal as D
from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.models import *
from opportunity_cookbook.verdicts import Verdict


def scenario():
    return OpportunityScenario(
        "Fictional Test", True, CustomerEconomics(D("30000"), D("20000"), D("9000"), D("2000")),
        DeliveryEconomics(D("50"), D("40"), D("50"), annual_support_hours=D("10"), support_hourly_cost=D("50")),
        SolutionsEconomics(D("5"), D("5"), D("5"), D("5"), D("50")),
        SalesCharacteristics(Level.LOW, D("2"), Level.HIGH, Level.LOW),
        TechnicalCharacteristics(2, Level.MODERATE, Level.HIGH, Feasibility.FEASIBLE, Level.LOW, Level.LOW, Level.LOW),
        BuildVsBuy(AlternativeFinding.CUSTOM_JUSTIFIED, (AlternativeType.CUSTOM_INTEGRATION,), "reviewed"))


def test_promising_and_traceable_without_mutation():
    s = scenario(); before = repr(s); result = analyze(s)
    assert result.verdict is Verdict.PROMISING
    assert len(result.reasons) == 3 and "hypothesis" in result.reasons[-1]
    assert repr(s) == before


def test_zero_and_insufficient_value_are_no_deal():
    for value in (D("0"), D("5000")):
        s = scenario(); s = replace(s, customer=replace(s.customer, recoverable_value=value))
        result = analyze(s)
        assert result.verdict is Verdict.NO_DEAL
        assert result.reasons


def test_saas_is_buy_configure():
    s = scenario(); s = replace(s, build_vs_buy=replace(s.build_vs_buy, finding=AlternativeFinding.ADEQUATE_BUY))
    assert analyze(s).verdict is Verdict.BUY_CONFIGURE


def test_high_delivery_cost_is_no_deal():
    s = scenario(); s = replace(s, delivery=replace(s.delivery, engineering_hourly_cost=D("200")))
    assert analyze(s).verdict is Verdict.NO_DEAL


def test_difficult_sales_motion_is_poor_target():
    s = scenario(); s = replace(s, sales=replace(s.sales, procurement_difficulty=Level.HIGH))
    assert analyze(s).verdict is Verdict.POOR_TARGET


def test_low_reuse_viable_project_is_one_off():
    s = scenario(); s = replace(s, delivery=replace(s.delivery, reusable_engineering_hours=D("10"), customer_specific_engineering_hours=D("80")))
    assert analyze(s).verdict is Verdict.ONE_OFF


def test_missing_assumptions_are_investigate_and_all_reasons_exposed():
    s = scenario()
    s = replace(s, customer=replace(s.customer, current_state_annual_burden=None, recoverable_value=None),
                technical=replace(s.technical, feasibility=Feasibility.UNKNOWN),
                build_vs_buy=replace(s.build_vs_buy, finding=AlternativeFinding.UNKNOWN))
    result = analyze(s)
    assert result.verdict is Verdict.INVESTIGATE
    assert len(result.reasons) == 4


def test_infeasible_is_no_deal():
    s = scenario(); s = replace(s, technical=replace(s.technical, feasibility=Feasibility.INFEASIBLE))
    assert analyze(s).verdict is Verdict.NO_DEAL
