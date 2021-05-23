from typing import Any, Dict

from wx_spider.controls import WXTYPES


class ProtoControl:
    value: Any
    name: str
    label: str
    wxtype: WXTYPES
    kwargs: dict

    def __init__(self, name, wxtype: WXTYPES, label=None, kwargs=None):
        if kwargs is None:
            kwargs = {}
        self.name = name
        self.value = None
        if not label:
            self.label = name
        else:
            self.label = label
        self.wxtype = wxtype
        self.kwargs = kwargs

    def __str__(self):
        return f"{self.__class__.__name__}(name='{self.name}', " \
               f"label='{self.label}', wxtype={self.wxtype} )"
