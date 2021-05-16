from ..render.render import Render

# CommandRunnerのデフォルト実装
class Command():

    def subcommand_parser(self, parser):
        parser.add_argument('--no-use')
        return parser

    def context_class(self):
        return {}

    def render_class(self, *, context):
        return Render(context=context)
