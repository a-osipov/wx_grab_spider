from wx_spider.controls import ProtoControl, TextCtrl


def test_proto_control():
    pc = ProtoControl('name2', label='name 2', wxtype=TextCtrl)
    assert pc.value == None
    assert pc.name == 'name2'
    assert pc.label == 'name 2'
    assert pc.wxtype == TextCtrl
    assert pc.kwargs == {}
