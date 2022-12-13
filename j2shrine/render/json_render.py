from .render import Render
import json


class JsonRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        self.context = context
        self.build_convert_engine(context = context)

    def read_source(self, *, reader):
        loaded = json.load(reader)
        return loaded

