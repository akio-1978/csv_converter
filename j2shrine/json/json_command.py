import argparse
from ..command import Command
from .json_render import JsonLoader
import j2shrine

# CommandRunnerのデフォルト実装


class JsonCommand(Command):
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog=f'{j2shrine.PROG_NAME} json mode')
        self.setup()


    def loader_class(self):
        """Commandが使うRenderのクラスを返す"""
        return JsonLoader
