from wx_spider.base import WxSpider
from wx_spider.controls import ProtoControl, DatePickerCtrl, TextCtrl, TextCtrlPassword


class WxSpider1(WxSpider):
    """
    Grab Installation
    Common problems
    """
    wx_controls = [
        ProtoControl('name1', label='name 1', wxtype=DatePickerCtrl),

    ]


class WxSpider2(WxSpider1):
    wx_controls = [
        ProtoControl('name2', label='name 2', wxtype=TextCtrl),
        ProtoControl('name2.5', label='name 2.5', wxtype=TextCtrl),
    ]


class WxSpider3(WxSpider2):
    wx_controls = [
        ProtoControl('name3', label='name 3', wxtype=TextCtrl),

    ]


class WxSpider4(WxSpider2):
    wx_controls = [
        ProtoControl('name4', label='name 4', wxtype=TextCtrl),

    ]


class WxSpider5(WxSpider):
    wx_controls = [
        ProtoControl('name5', label='name 5', wxtype=DatePickerCtrl),

    ]


class WxSpider6(WxSpider):
    pass


class WxSpider7(WxSpider6):
    wx_controls = [
        ProtoControl('name7', label='name 7', wxtype=DatePickerCtrl),

    ]


class WxSpider8(WxSpider7):
    pass


class WxSpider9(WxSpider4):
    pass


class WxSpiderAbs1(WxSpider):
    wx_controls = [
        ProtoControl('login', wxtype=TextCtrl),
    ]

    class Meta:
        abstract = True


class WxSpiderNotAbs(WxSpider):
    wx_controls = [
        ProtoControl('login', wxtype=TextCtrl),
    ]


class WxSpiderPr1(WxSpiderAbs1):
    wx_controls = [
        ProtoControl('date1', label='date 1', wxtype=DatePickerCtrl),
    ]


class WxSpiderPr2(WxSpiderNotAbs):
    wx_controls = [
        ProtoControl('name2', label='name 2', wxtype=TextCtrl),
    ]


class TestSpiderPassw(WxSpider):
    wx_controls = [
        ProtoControl('login', TextCtrl),
        ProtoControl('password', TextCtrlPassword),

    ]


print(WxSpider1.controlled_parents())
