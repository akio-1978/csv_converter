from ..loader import Loader
from ..context import RenderContext
import json


class JsonRender(Loader):

    # jinja2テンプレートの生成
    def __init__(self, *, context: RenderContext):
        self.context = context
        self.setup_template(context=context)

    def loading(self, *, reader):
        loaded = json.load(reader)
        return loaded
