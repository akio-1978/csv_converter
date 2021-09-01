
from ..render.json_render import JsonRender, JsonRenderContext

# CommandRunnerのデフォルト実装
class JsonCommand():

    def create_parser(self,*, main_parser):
        return main_parser.add_parser('json', help = 'rendaring json format')

    def context_class(self):
        return JsonRenderContext

    def render_class(self, *, context):
        return JsonRender(context=context)
