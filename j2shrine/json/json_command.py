import argparse
from ..command import Command
from .json_render import JsonRender
import j2shrine

# CommandRunnerのデフォルト実装


class JsonCommand(Command):
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog=f'{j2shrine.PROG_NAME} json mode')
        self.setup()


    def render_class(self):
        """Commandが使うRenderのクラスを返す"""
        return JsonRender
