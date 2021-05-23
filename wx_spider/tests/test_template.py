import os

from wx_spider.template import Template
from wx_spider.tests.spiders import WxSpider1


def test_template():
    template = Template(images_dir=os.path.dirname(__file__))
    assert template.template_name == 'base.html'
    assert template.images_dir == os.path.dirname(__file__)


def test_render():
    template = Template(images_dir=os.path.dirname(__file__), template_dir=os.path.dirname(__file__))
    assert template.render(WxSpider1) == 'None\nGrab Installation\nCommon problems'
