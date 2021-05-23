import os

from jinja2 import Environment, FileSystemLoader

from wx_spider import WxSpider, text2html


class Template:
    def __init__(self, images_dir, template_dir=None, template_name='base.html'):
        if template_dir is None:
            template_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'templates')
        self.template_name = template_name
        self.images_dir = images_dir
        self.env = Environment(loader=FileSystemLoader(template_dir),
                               trim_blocks=True)

    def render(self, spider: WxSpider) -> str:
        if spider.__doc__:
            doc_lines = spider.__doc__.strip().split('\n')
            headline = text2html(doc_lines[0].strip())
            rest_of_text: str = text2html('\n'.join([line.strip() for line in doc_lines[1:]]))
        else:
            headline = spider.__name__
            rest_of_text = None
        if spider.image:
            image = os.path.join(self.images_dir, spider.image)
        else:
            image = None
        return self.env.get_template(self.template_name).render(
            {'spider_name': spider.__name__,
             'headline': headline,
             'rest_of_text': rest_of_text,
             'image': image}
        )
