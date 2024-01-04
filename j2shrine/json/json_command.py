
from ..command import Command
from .json_render import JsonRender
from .json_context import JsonRenderContext

# CommandRunnerのデフォルト実装


class JsonCommand(Command):

    def create_parser(self, *, main_parser):
        return main_parser.add_parser('json', help='rendaring json format')

    def new_context(self, *, args):
        return JsonRenderContext(args=args)

    def new_render(self, *, context: JsonRenderContext):
        return JsonRender(context=context)
