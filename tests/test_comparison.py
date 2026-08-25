from decimal import Decimal

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.comparison import (DEFINITIONS, PATTERN_CASES,
    comparison_rows, group_by_verdict, money_fields, render_comparison)
from opportunity_cookbook.verdicts import Verdict


def test_all_baselines_are_unique_ordered_and_framework_generated():
    rows = comparison_rows()
    assert tuple(r.case_id for r in rows) == tuple(range(1, 15))
    assert len({r.case_id for r in rows}) == len(rows)
    assert len({r.title for r in rows}) == len(rows)
    for row in rows:
        expected = analyze(row.scenario)
        if row.case_id == 14:  # its documented acquisition extension refines the base gate
            assert expected.verdict is Verdict.POOR_TARGET
        else:
            assert row.analysis == expected
        assert row.analysis.reasons


def test_case_12_is_post_alternative_and_no_variant_replaces_baseline():
    rows = comparison_rows()
    assert rows[11].analysis.verdict is Verdict.BUY_CONFIGURE
    assert rows[11].scenario.build_vs_buy.finding.value.startswith("existing buy/configure")
    assert all(definition.builder.__name__ == "baseline_case" for definition in DEFINITIONS)


def test_money_is_decimal_and_grouping_is_deterministic():
    rows = comparison_rows()
    for row in rows:
        for name in money_fields():
            value = getattr(row, name)
            assert value is None or isinstance(value, Decimal)
    assert group_by_verdict(rows) == group_by_verdict(rows)
    assert [v for v, _ in group_by_verdict(rows)] == [
        Verdict.PROMISING, Verdict.BUY_CONFIGURE, Verdict.POOR_TARGET, Verdict.NO_DEAL]


def test_synthesis_sets_reference_only_existing_cases():
    ids = {r.case_id for r in comparison_rows()}
    flattened = set()
    for value in PATTERN_CASES.values():
        for item in value:
            flattened.update(item if isinstance(item, tuple) else (item,))
    assert flattened <= ids
    assert PATTERN_CASES["single_vs_multi"] == ((1, 2), (3, 4))
    assert 13 in PATTERN_CASES["delivery_risk"]
    assert PATTERN_CASES["sales_failure"] == (14,)
    assert PATTERN_CASES["institutional_friction"] == (9, 10)


def test_render_is_fixed_width_descriptive_and_has_no_composite_score():
    rendered = render_comparison()
    assert rendered.count("\n1     Independent restaurant") == 1
    for case_id in range(2, 15):
        assert f"\n{case_id:<5}" in rendered
    assert "OPPORTUNITY SCORE" not in rendered.upper()
    assert "DISCOVERY HYPOTHESES" in rendered
    assert "COLUMNS" not in rendered  # no terminal-width lookup/dependency
