import argparse
from ..command import Command
from .json_render import JsonRender

# CommandRunnerのデフォルト実装


class JsonCommand(Command):
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='j2render json mode')
        self.setup()


    def render_class(self):
        """Commandが使うRenderのクラスを返す"""
        return JsonRender
