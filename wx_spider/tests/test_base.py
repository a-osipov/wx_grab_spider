import pytest
from wx_spider import text2html
from wx_spider.tests.spiders import WxSpider1, WxSpider2, WxSpider3, WxSpider4, WxSpider5, WxSpider6, \
    WxSpider7, WxSpider8, WxSpider9, WxSpiderPr1, WxSpiderAbs1, WxSpiderPr2


class TestWxSpider:
    def test_control_by_name(self):
        assert WxSpider3.control_by_name('name3').name == 'name3'
        assert WxSpider3.control_by_name('name2.5').name == 'name2.5'
        with pytest.raises(ValueError):
            WxSpider3.control_by_name('nameZero')

    def test_controls(self):
        ws1 = WxSpider1()
        control_names = [control.name for control in ws1.controls()]
        assert control_names == ['name1', ]
        ws2 = WxSpider2()
        control_names = [control.name for control in ws2.controls()]
        assert control_names == ['name1', 'name2', 'name2.5']
        ws3 = WxSpider3()
        control_names = [control.name for control in ws3.controls()]
        assert control_names == ['name1', 'name2', 'name2.5', 'name3']
        ws4 = WxSpider4()
        control_names = [control.name for control in ws4.controls()]
        assert control_names == ['name1', 'name2', 'name2.5', 'name4']
        ws5 = WxSpider5()
        control_names = [control.name for control in ws5.controls()]
        assert control_names == ['name5', ]
        ws6 = WxSpider6()
        assert ws6.controls() == []
        ws9 = WxSpider9()
        control_names = [control.name for control in ws9.controls()]
        assert control_names == ['name1', 'name2', 'name2.5', 'name4']

    def test_controlled_parents(self):
        assert WxSpider1.controlled_parents() == []
        assert WxSpider2.controlled_parents() == [WxSpider1, ]
        assert WxSpider7.controlled_parents() == []
        assert WxSpider8.controlled_parents() == [WxSpider7, ]

    def test_abstract_parents(self):
        ws1 = WxSpiderPr1()
        assert ws1.abstract_parents() == [WxSpiderAbs1, ]
        ws2 = WxSpiderPr2()
        assert ws2.abstract_parents() == []


def test_text2html():
    text = """Grab Installation
     Common problems"""
    assert text2html(text) == 'Grab Installation</br>     Common problems'
