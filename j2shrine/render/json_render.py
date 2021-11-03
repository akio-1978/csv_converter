from . base_render import Render, RenderContext
import json

# renderの動作を決定するコンテキスト
class JsonRenderContext(RenderContext):
    def __init__(self, *, template=None, parameters={}):
        super().__init__(template=template, parameters=parameters)

class JsonRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        self.context = context
        self.build_convert_engine(context = context)

    def read_source(self, *, reader):
        loaded = json.load(reader)
        return loaded

