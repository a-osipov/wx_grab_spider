import datetime
from typing import Dict, Any, List

import keyring
from pypref import Preferences

from wx_spider import WxSpider
from wx_spider.controls import DatePickerCtrl, TextCtrlPassword, ProtoControl

PREFERENCES: Preferences = None


class PreferencesBase(Preferences):
    def __init__(self, *args, **kwargs):
        filename: str = kwargs.get('filename') or 'wx_spider_pref.py'
        super(PreferencesBase, self).__init__(filename=filename, *args, **kwargs)

    def get_password(self, spider_name, control_name):
        return keyring.get_password(spider_name, control_name)


def set_preferences(preferences=None):
    if preferences:
        globals()['PREFERENCES'] = preferences()
    else:
        globals()['PREFERENCES'] = PreferencesBase()


set_preferences()


def get_spider_preference(spider: WxSpider) -> Dict[str, Any]:
    data_deserialized: Dict[str, Any] = {}
    protoControl: ProtoControl
    for controlled_spider in spider.abstract_parents() + [spider, ]:
        data: Dict[str, Any] = PREFERENCES.get(controlled_spider.__name__)
        if not data:
            continue
        for key, value in deserialize_spider_data(controlled_spider, data).items():
            if key not in data_deserialized:
                data_deserialized[key] = value
        data_deserialized.update(get_passwords(controlled_spider))
    return data_deserialized


def set_spider_preference(spider: WxSpider):
    protocontrols: List[ProtoControl] = []
    for parent in spider.controlled_parents():
        if parent.Meta.abstract:
            PREFERENCES.update_preferences({parent.__name__: serialize_spider_data(parent, parent.wx_controls)})
        else:
            protocontrols += parent.wx_controls
    protocontrols += spider.wx_controls
    PREFERENCES.update_preferences({spider.__name__: serialize_spider_data(spider, protocontrols)})


def set_frame_preference(data_serialized: Dict[str, str]):
    PREFERENCES.update_preferences({'frame': data_serialized})


def get_frame_preference():
    return PREFERENCES.get('frame')


def get_passwords(spider: WxSpider):
    passwords: Dict[str, str] = {}
    protoControl: ProtoControl
    for protoControl in get_password_controls(spider):
        value = PREFERENCES.get_password(spider.__name__, protoControl.name)
        if value:
            passwords[protoControl.name] = value
    return passwords


def serialize_spider_data(spider: WxSpider, protocontrols: List[ProtoControl]):
    data_serialized = {}
    protoControl: ProtoControl
    for protoControl in protocontrols:
        value = protoControl.value
        if protoControl.wxtype == TextCtrlPassword:
            keyring.set_password(spider.__name__, protoControl.name, value)
            continue
        if isinstance(value, (datetime.date, datetime.datetime)):
            data_serialized[protoControl.name] = value.isoformat()
        else:
            data_serialized[protoControl.name] = value
    return data_serialized


def deserialize_spider_data(spider: WxSpider, data: Dict[str, str]):
    data_deserialized: Dict[str, Any] = {}
    protoControl: ProtoControl
    if not data:
        return data_deserialized
    for protoControl in spider.controls():
        if protoControl.name in data:
            value = data[protoControl.name]
            if protoControl.wxtype == DatePickerCtrl:
                data_deserialized[protoControl.name] = datetime.date.fromisoformat(value)
            else:
                data_deserialized[protoControl.name] = value
    return data_deserialized


def get_password_controls(spider: WxSpider):
    password_controls = []
    for controlled_spider in spider.abstract_parents() + [spider, ]:
        for protoControl in controlled_spider.wx_controls:
            if protoControl.wxtype != TextCtrlPassword:
                continue
            else:
                password_controls.append(protoControl)
    return password_controls
