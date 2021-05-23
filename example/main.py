import logging
import os

import wx

from example.spiders import DemoSpider2, DemoSpider3
from wx_spider import Template
from wx_spider.frame import MainFrame


if __name__ == "__main__":
    spiders = [DemoSpider2, DemoSpider3]
    app = wx.App()
    template = Template(images_dir=os.path.join(os.path.dirname(__file__), 'images'))
    frame = MainFrame(spiders=spiders, template=template)
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=[frame.logging_handler(), ]
    )
    frame.Show()
    app.MainLoop()
