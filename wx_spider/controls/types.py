import datetime

import wx
import wx.adv
import wx.lib.masked


class DatePickerCtrl(wx.adv.DatePickerCtrl):
    def __init__(self, *args, **kwargs):
        if 'style' not in kwargs:
            kwargs['style'] = wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY
        super(DatePickerCtrl, self).__init__(*args, **kwargs)

    def GetValue(self):
        value: datetime.date = wx.wxdate2pydate(super(DatePickerCtrl, self).GetValue()).date()
        return value

    def SetValue(self, date: datetime.date):
        super(DatePickerCtrl, self).SetValue(wx.pydate2wxdate(date))


class TextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        if 'style' not in kwargs:
            kwargs['style'] = wx.TE_RICH
        super(TextCtrl, self).__init__(*args, **kwargs)


class TextCtrlPassword(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        if 'style' not in kwargs:
            kwargs['style'] = wx.TE_PASSWORD
        super(TextCtrlPassword, self).__init__(*args, **kwargs)


class MaskedTextCtrl(wx.lib.masked.TextCtrl):
    def __init__(self, *args, **kwargs):
        if 'mask' not in kwargs:
            raise ValueError('mask expected')
        if 'style' not in kwargs:
            kwargs['style'] = wx.TE_RICH
        super(MaskedTextCtrl, self).__init__(*args, **kwargs)


class FilePickerCtrl(wx.FilePickerCtrl):
    def GetValue(self):
        return super(FilePickerCtrl, self).GetPath()

    def SetValue(self, filename):
        super(FilePickerCtrl, self).SetPath(filename)


class CheckBox(wx.CheckBox):
    def __init__(self, *args, **kwargs):
        value = kwargs.get('Value')
        if 'Value' in kwargs:
            del kwargs['Value']
        super(CheckBox, self).__init__(*args, **kwargs)
        if value != None:
            self.SetValue(value)
