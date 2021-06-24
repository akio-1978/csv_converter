
from ..render.json_render import JsonRender, JsonRenderContext

# CommandRunnerのデフォルト実装
class JsonCommand():

    def context_class(self):
        return JsonRenderContext

    def render_class(self, *, context):
        return JsonRender(context=context)
