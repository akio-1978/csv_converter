import argparse
from ..command import Command
from .json_render import JsonRender
from .json_context import JsonRenderContext

# CommandRunnerのデフォルト実装


class JsonCommand(Command):
    def __init__(self,*, master: argparse.ArgumentParser):
        self.parser = master.add_parser('json', help='jsonのレンダリングを行う')
        self.parser.set_defaults(command_instance=self)

    _render = JsonRender
    _context = JsonRenderContext
