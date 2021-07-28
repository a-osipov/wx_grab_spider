import logging
from logging import getLevelName, INFO
from typing import List

import wx
import wx.adv
import wx.html2 as webview
import wx.lib.agw.buttonpanel as bp
from wx import ComboBox

import wx_spider
from wx_spider import pref, LogginSpiderView
from wx_spider.base import Handler
from wx_spider.controls import WXTYPES, ProtoControl, TextCtrlPassword
from wx_spider.images import _bp_btn1
from wx_spider.template import Template

frame_logger = logging.getLogger(__name__)


class BaseDialog(wx.Dialog):
    def __init__(self, protocontrols, preference=None):
        title = ''
        self.control_prefix = 'ctrl_'
        super(BaseDialog, self).__init__(None, -1, title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.protocontrols = protocontrols
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.widgetSizer = wx.BoxSizer(wx.VERTICAL)
        self.okButton = wx.Button(self, wx.ID_OK, "OK", pos=(15, 15))
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel", pos=(115, 15))
        self.buttonSizer.Add(self.okButton, 0, wx.CENTER | wx.ALL, 5)
        self.buttonSizer.Add(self.cancelButton, 0, wx.CENTER | wx.ALL, 5)
        self.mainSizer.Add(self.buttonSizer, 0, wx.CENTER)
        protoControl: wx_spider.ProtoControl
        for num, protoControl in enumerate(self.protocontrols):
            controlSizer = wx.BoxSizer(wx.HORIZONTAL)
            st = wx.StaticText(self, -1, protoControl.label)
            controlSizer.Add(st, 0, wx.ALL, 5)
            control: WXTYPES = protoControl.wxtype(self, 0, **protoControl.kwargs)
            if preference and protoControl.name in preference:
                control.SetValue(preference[protoControl.name])
            setattr(self, f'{self.control_prefix}{protoControl.name}', control)
            controlSizer.Add(control, 0, wx.ALL, 5)
            self.widgetSizer.Add(controlSizer, 0, wx.ALL, 2)
        self.Bind(wx.EVT_BUTTON, self.onOkButton, id=self.okButton.GetId())
        self.mainSizer.Add(self.widgetSizer, 0, wx.CENTER | wx.ALL, 10)
        self.SetSizerAndFit(self.mainSizer)

    def onOkButton(self, event):
        pass

    def control_by_name(self, name):
        return getattr(self, f'{self.control_prefix}{name}')


class LoggingDialog(BaseDialog):
    def __init__(self):
        preference = pref.PREFERENCES.get('logging') or {'level': 'ERROR'}
        levels = ['ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG']
        self.level = preference.get('level')
        protocontrols = [ProtoControl('level', ComboBox,
                                      kwargs={'choices': levels,
                                              'value': self.level}),
                         ]
        super(LoggingDialog, self).__init__(protocontrols, preference)

    def onOkButton(self, event):
        self.level = self.control_by_name('level').GetValue()
        pref.PREFERENCES.update_preferences({'logging': {'level': self.level}})
        event.Skip()


class SpiderDialog(BaseDialog):
    def __init__(self, spider: wx_spider.WxSpider):
        self.spider = spider
        preference = pref.get_spider_preference(self.spider)
        super(SpiderDialog, self).__init__(spider.controls(), preference)

    def onOkButton(self, event):
        for protoControl in self.protocontrols:
            control = self.control_by_name(protoControl.name)
            protoControl.value = control.GetValue()
        pref.set_spider_preference(self.spider)
        event.Skip()


class MainFrame(wx.Frame):
    template: Template
    spiders: List[wx_spider.WxSpider]
    webview: webview.WebView

    def __init__(self, spiders, template, id=wx.ID_ANY, title="wxGrabSpider",
                 size=(1050, 750)):
        wx.Frame.__init__(self, None, id, title, size=size)
        self.template = template
        self.spiders = spiders
        spider_names = [spider.__name__ for spider in spiders]
        mainPanel = wx.Panel(self, -1)
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)
        self.thread = None
        vSizer = wx.BoxSizer(wx.VERTICAL)
        mainPanel.SetSizer(vSizer)
        # titleBar
        self.titleBar = bp.ButtonPanel(mainPanel, -1, title,
                                       agwStyle=bp.BP_USE_GRADIENT)
        btn1 = bp.ButtonInfo(self.titleBar, wx.ID_ANY, _bp_btn1.GetBitmap())
        btn1.SetText('Start')
        self.titleBar.AddButton(btn1)
        self.Bind(wx.EVT_BUTTON, self.onButton, btn1)
        self.cbSpider = ComboBox(self.titleBar, 500, spider_names[self.spider_number()], (90, 50),
                                 (250, -1), spider_names,
                                 wx.CB_DROPDOWN
                                 | wx.CB_READONLY
                                 )
        self.webview = webview.WebView.New(mainPanel)
        self.webview_page_render()

        self.Bind(wx.EVT_COMBOBOX, self.onSpiderChanged)

        bpArt = self.titleBar.GetBPArt()
        bpArt.SetColour(bp.BP_TEXT_COLOUR, wx.BLUE)
        self.titleBar.AddSeparator()
        self.titleBar.AddControl(self.cbSpider)

        vSizer.Add(self.titleBar, 0, wx.EXPAND)
        vSizer.Add((20, 20))
        vSizer.Add(self.webview, 1, wx.EXPAND | wx.ALL, 5)

        self.titleBar.DoLayout()
        vSizer.Layout()

        self.Bind(wx.EVT_CLOSE, self.onClose)

        #     *****************************
        mb = wx.MenuBar()
        loggingMenu = wx.Menu()
        loggingItem = wx.MenuItem(loggingMenu, wx.ID_ANY, "&Logging")

        fileMenu = wx.Menu()
        fileItem = wx.MenuItem(fileMenu, wx.ID_ANY, "&Quit")
        fileMenu.Append(fileItem)
        fileMenu.Append(loggingItem)
        self.Bind(wx.EVT_MENU, self.onLogging, loggingItem)
        self.Bind(wx.EVT_MENU, self.onClose, fileItem)
        mb.Append(fileMenu, "&File")
        self.SetMenuBar(mb)

    @property
    def spider(self):
        return self.spiders[self.cbSpider.GetSelection()]

    def spider_number(self):
        preference_frame = pref.get_frame_preference()
        if preference_frame:
            preference_spider_name = preference_frame.get('spider_name')
            if preference_spider_name in [spider.__name__ for spider in self.spiders]:
                return [spider.__name__ for spider in self.spiders].index(preference_spider_name)
        return 0

    def webview_page_render(self):
        self.webview.SetPage(self.template.render(self.spider), "")

    def representation_control_value(self, control):
        if control.wxtype == TextCtrlPassword:
            return len(control.value) * '*'
        elif type(control.value) != list:
            return control.value
        else:
            return f'len - {len(control.value)}; '+str(control.value[:3]).replace(']', ', ...]')

    def onButton(self, event):
        dlg = SpiderDialog(self.spider)
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return
        dlg.Destroy()
        self._log(f'spider - "{self.spider.__name__}" ---> run')
        self._log('-------------------')
        if len(self.spider.controls()):
            self._log(chr(10).join([f'"{control.name}": {self.representation_control_value(control)}'
                                    for control in self.spider.controls()]))
            self._log('-------------------')
        for control in self.titleBar._vButtons:
            control.Disable()
        self.cbSpider.Disable()
        self.thread = wx_spider.WxSpiderThread(self.spider, self)

    def onSpiderChanged(self, event=None):
        self.webview_page_render()
        event.Skip()

    def onClose(self, event):
        data_serialized = {'spider_name': self.spider.__name__}
        pref.set_frame_preference(data_serialized)
        if self.thread:
            self.thread.stop()
        self.Destroy()
        event.Skip()

    def set_logger(self, level):
        logger = logging.getLogger()
        logger.setLevel(getLevelName(level))

    def _log(self, entry):
        style = wx_spider.LOGGING_STYLES[INFO]
        self.log(wx_spider.text2html(entry), style)

    def log(self, entry, style):
        self.webview.RunScript(f'AddLogEntry("{entry}", "{style}");')

    def logging_handler(self):
        return Handler(stream=LogginSpiderView(self.log))

    def onLogging(self, event):
        dlg = LoggingDialog()
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return
        self.set_logger(level=dlg.level)
        dlg.Destroy()

    def updateDisplay(self, results):
        if results:
            for control in self.titleBar._vButtons:
                control.Enable()
            self.cbSpider.Enable()
            self._log(f'spider - "{self.spider.__name__}" ---> end of work')


if __name__ == '__main__':
    class _SpiderDialog(SpiderDialog):
        def __init__(self):
            pass


    _ = _SpiderDialog()
    print(dir(_))
