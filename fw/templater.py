from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment

SITE_PATH = 'templates'


def render(template, path=SITE_PATH, **kwargs):
    environment = Environment()
    environment.loader = FileSystemLoader(path)
    res = environment.get_template(template).render(**kwargs)
    return res
