from j2render.render.renderlogic import RenderLogic

# CommandRunnerのデフォルト実装
class BaseCommandRunner():

    def subcommand_parser(self, parser):
        return parser

    def context_class(self):
        return {}

    def render_logic(self, *, context):
        return None

    def render(self, *, render_logic=None, context=None, source, output):
        render_logic.render(context, source, output)

    def exeute_command(self, *, context):
        logic = self.render_logic(context=context)

