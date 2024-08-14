import argparse
from j2shrine.context import RenderContext
from ..command import Command
from .csv_render import CsvRender
from .csv_context import CsvRenderContext


class CsvCommand(Command):

    def __init__(self,*, parsers: argparse.ArgumentParser):
        self.parser = parsers.add_parser('csv', help='csvのレンダリングを行う')
        self.parser.set_defaults(command_instance=self)
        self.setup()


    def render_class(self):
        """Commandが使うRenderのクラスを返す"""
        return CsvRender
    def context_class(self):
        """Commandが使うContextのクラスを返す"""
        return CsvRenderContext

    def add_optional_arguments(self):
        """csv固有のオプション引数を定義する
        """
        # flag first line is header
        self.parser.add_argument('-H', '--header', help='先頭行をヘッダとして解釈するか？ヘッダは各カラムの名前として使用可能.',
                            dest='read_header', action='store_true')
        # flag tab separate values
        self.parser.add_argument('-d', '--delimiter', metavar='',
                            help="カラムの区切り文字 defaultは ',' .")
        # skip head lines
        self.parser.add_argument('-s', '--skip-lines', metavar='',
                            type=int, help='指定した数値分だけ先頭から行を読み飛ばす.')
