import pytest

from wx_spider.controls import WXTYPES


@pytest.mark.parametrize("control", WXTYPES.__args__)
def test_controls(control):
    assert hasattr(control, 'GetValue')
    assert hasattr(control, 'SetValue')
