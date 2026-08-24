from dataclasses import FrozenInstanceError
from decimal import Decimal as D

import pytest

from opportunity_cookbook.scaling import EngineeringScaling, SupportScaling


def test_engineering_scaling_keeps_shared_work_fixed():
    scaling = EngineeringScaling(D("100"), D("10"), 5, D("30"), D("20"), D("5"), D("10"))
    assert scaling.incremental_hours == D("50")
    assert scaling.core_hours == D("180")
    assert scaling.total_hours == D("215")


def test_support_scaling_combines_fixed_and_incremental_obligations():
    scaling = SupportScaling(D("10"), D("3"), 5, D("2"), D("100"), D("20"))
    assert scaling.total_hours == D("27")
    assert scaling.total_other_costs == D("200")


@pytest.mark.parametrize("count", [0, -1, 1.5, True])
def test_scaling_rejects_invalid_unit_counts(count):
    with pytest.raises(ValueError, match="positive integer"):
        EngineeringScaling(D("1"), D("1"), count, D("1"))


def test_scaling_is_immutable():
    scaling = SupportScaling(D("1"), D("1"), 1)
    with pytest.raises(FrozenInstanceError):
        scaling.unit_count = 2
