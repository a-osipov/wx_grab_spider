import html
import threading
from logging import FATAL, CRITICAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET, StreamHandler
from threading import Thread
from typing import List, Dict, Any

import grab.spider
from wx import CallAfter

from wx_spider.controls.prototypes import ProtoControl

LOGGING_STYLES = {CRITICAL: 'err', FATAL: 'err', ERROR: 'err', WARNING: 'warn', WARN: 'warn',
                  INFO: 'info', DEBUG: 'debug', NOTSET: 'info'}


class MetaWxSpider(type(grab.spider.Spider)):
    _spider_tree: Dict[str, Any] = {}

    def __new__(mcs, name, bases, attrs):
        parent_name = bases[0].__name__
        mcs._spider_tree[name] = []
        if parent_name in mcs._spider_tree:
            for controlled_parent in mcs._spider_tree[parent_name]:
                mcs._spider_tree[name].append(controlled_parent)
        if 'wx_controls' in bases[0].__dict__ and bases[0].wx_controls:
            mcs._spider_tree[name].append(bases[0])
        return super().__new__(mcs, name, bases, attrs)


class WxSpider(grab.spider.Spider, metaclass=MetaWxSpider):
    wx_controls: List[ProtoControl] = []
    image: str = None

    @classmethod
    def control_by_name(cls, name):
        for control in cls.controls():
            if control.name == name:
                return control
        raise ValueError(f'{cls.__name__} - control named "{name}" not found')

    @classmethod
    def controls(cls):
        controls = []
        for parent in cls.controlled_parents():
            for control in parent.wx_controls:
                controls.append(control)
        for control in cls.wx_controls:
            controls.append(control)
        return controls

    @classmethod
    def controlled_parents(cls):
        return MetaWxSpider._spider_tree.get(cls.__name__) or []

    @classmethod
    def abstract_parents(cls):
        return [parent for parent in cls.controlled_parents() if parent.Meta.abstract]


class WxSpiderThread(Thread):
    def __init__(self, spider: WxSpider, window):
        super(WxSpiderThread, self).__init__()
        self.window = window
        self.spider = spider()
        self.spider.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.start()

    def stop(self):
        self.spider.stop()
        self.timeToQuit.set()

    def run(self):
        CallAfter(self.window.updateDisplay, False)
        self.spider.run()
        CallAfter(self.window.updateDisplay, True)

    def abort(self):
        self.exit = True


class LogginSpiderView:
    levelno: int

    def __init__(self, log):
        self.log = log
        self.levelno = 0

    def write(self, *args, **kwargs):
        text = text2html(args[0].strip())
        style = LOGGING_STYLES[self.levelno]
        CallAfter(self.log, text, style)


def text2html(text: str) -> str:
        return html.escape(text).replace('\n', '</br>')


class Handler(StreamHandler):
    def emit(self, record):
        self.stream.levelno = record.levelno
        super(Handler, self).emit(record)