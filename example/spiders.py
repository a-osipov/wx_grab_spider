import logging

import wx
from grab.spider.base import Task

from wx_spider import WxSpider
from wx_spider.controls import *

logger = logging.getLogger(__name__)


class DemoSpider1(WxSpider):
    wx_controls = [
        ProtoControl('login', TextCtrl),
        ProtoControl('password', TextCtrlPassword),

    ]

    initial_urls = ['https://pypi.org/account/login/', ]

    def task_initial(self, grab, task):
        logger.debug('Sign in to pypi')
        csrf_token = grab.doc.select('//input[@name="csrf_token"]').node_list()[0].attrib['value']
        logger.info(f'csrf_token - "{csrf_token}"')
        grab.setup(method='POST', url='https://pypi.org/account/login/')
        password = self.control_by_name("password").value
        login = self.control_by_name("login").value
        grab.setup(post={'csrf_token': csrf_token,
                         'username': login,
                         'password': password})
        yield Task('login', grab=grab)

    class Meta:
        abstract = True


class DemoSpider2(DemoSpider1):
    """
    DemoSpider2
    is the spider that shows you
    how to use the controls
    """
    image = 'spider4.jpg'
    wx_controls = [
        ProtoControl('date1', wxtype=DatePickerCtrl,
                     kwargs=dict(dt=wx.DateTime().Now())),
        ProtoControl('date2', wxtype=DatePickerCtrl),
        ProtoControl('file', wxtype=FilePickerCtrl),
        ProtoControl('check4', wxtype=CheckBox),
        ProtoControl('year', wxtype=MaskedTextCtrl, kwargs={'mask': '#{4}'}),
    ]

    def task_login(self, grab, task):
        logger.debug('login')


class DemoSpider3(DemoSpider1):
    """
    DemoSpider3
    is the spider that shows you
    how to use the controls
    """

    image = 'full-frame-watercolor-textured-background.jpg'
    wx_controls = [
        ProtoControl('date1', wxtype=DatePickerCtrl,
                     kwargs=dict(dt=wx.DateTime().Now())),
    ]

    def task_login(self, grab, task):
        logger.debug('login')


class DemoSpider4(DemoSpider1):
    """
    DemoSpider4
    is the spider that shows you
    how to use the controls
    """

    image = 'full-frame-watercolor-textured-background.jpg'

    def task_login(self, grab, task):
        logger.debug('login')

