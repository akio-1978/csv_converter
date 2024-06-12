from ..render import Render
from ..context import RenderContext
import json


class JsonRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context: RenderContext):
        self.context = context
        self.setup_template(context=context)

    def read_source(self, *, reader):
        loaded = json.load(reader)
        return loaded
