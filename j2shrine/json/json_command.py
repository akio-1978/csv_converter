import argparse
from ..command import Command
from .json_render import JsonRender
from .json_context import JsonRenderContext

# CommandRunnerのデフォルト実装


class JsonCommand(Command):
    def __init__(self,*, parsers: argparse.ArgumentParser):
        self.parser = parsers.add_parser('json', help='jsonのレンダリングを行う')
        self.parser.set_defaults(command_instance=self)
        self.setup()


    def render_class(self):
        """Commandが使うRenderのクラスを返す"""
        return JsonRender
    def context_class(self):
        """Commandが使うContextのクラスを返す"""
        return JsonRenderContext
