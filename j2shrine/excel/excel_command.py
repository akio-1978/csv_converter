import argparse
import sys

from j2shrine.context import RenderContext
from ..command import Command, KeyValuesParseAction
from .excel_render import ExcelRender
from .excel_context import ExcelRenderContext
from ..renderutils import get_stream, KeyValuesParseAction

class ExcelCommand(Command):

    HELP_SHEETS = """読込対象シート ('1' シート1のみ. '1:4' シート1からシート4まで. '1:' シート1からすべてのシート)"""
    HELP_READ_RANGE = """読込セル範囲 ('A1:D4' A1:D4の16セル 'A1:D' A1を起点として、AからDまでの全ての行.)"""

    def __init__(self,*, factory: argparse.ArgumentParser):
        self.parser = factory.add_parser('excel', help='Excelのレンダリングを行う', formatter_class=argparse.RawTextHelpFormatter)
        self.parser.set_defaults(command_instance=self)

    def render_class(self):
        """Commandが使うRenderのクラスを返す"""
        return ExcelRender
    def context_class(self):
        """Commandが使うContextのクラスを返す"""
        return ExcelRenderContext

    def add_positional_arguments(self):
        """excel固有の必須引数があるので、位置引数を定義しなおす
            * excelブックをstdinから受け取れないため、ファイル名は必須
            * 読み取り対象シートの指定は必須
            * 読み取りセル範囲の指定は必須
        """
        self.parser.add_argument('template', help='使用するjinja2テンプレート.')
        # source book can't read from stdin
        self.parser.add_argument('source', help='レンダリング対象ブック xlsxファイルのみ対象.')
        self.parser.add_argument('sheets', help=ExcelCommand.HELP_SHEETS)
        self.parser.add_argument('read_range', help=ExcelCommand.HELP_READ_RANGE)

    def add_optional_arguments(self):
        """excel固有のオプションを追加する"""
        # 基本的なオプションは引き継ぐ
        super().add_optional_arguments()
        # 絶対位置指定セルを追加する
        self.parser.add_argument(
            '-a', '--absolute', help='絶対位置指定でセル値を固定で取得する [セル位置=名前]の形式で列挙する. ex: A1=NAME1 A2=NAME2...', dest='absolute', nargs='*', default={}, action=KeyValuesParseAction)

    def call_render(self, *, render, source, out):
        """
        in側はopenpyxlにファイル名を直接渡す必要があるため、call_renderをoverrideする
        """
        with get_stream(source=out, 
                           encoding=render.context.output_encoding, 
                           mode='w' ) as dest:
            render.render(source=source, output=dest)
