import argparse
import sys

from j2shrine.context import RenderContext
from ..command import Command, KeyValuesParseAction
from .excel_render import ExcelRender
from .excel_context import ExcelRenderContext


class ExcelCommand(Command):

    HELP_SHEETS = """読込対象シート ('1' シート1のみ. '1:4' シート1からシート4まで. '1:' シート1からすべてのシート)"""
    HELP_READ_RANGE = """読込セル範囲 ('A1:D4' A1:D4の16セル 'A1:D' A1を起点として、AからDまでの全ての行.)"""

    def create_parser(self, *, main_parser):
        return main_parser.add_parser('excel', help='Excelのレンダリングを行う', formatter_class=argparse.RawTextHelpFormatter)

    def add_positional_arguments(self, *, parser):
        parser.add_argument('template', help='使用するjinja2テンプレート.')
        # source book can't read from stdin
        parser.add_argument('source', help='レンダリング対象ブック xlsxファイルのみ対象.')
        parser.add_argument('sheets', help=ExcelCommand.HELP_SHEETS)
        parser.add_argument('read_range', help=ExcelCommand.HELP_READ_RANGE)
        return parser

    def add_optional_arguments(self, *, parser):
        super().add_optional_arguments(parser=parser)
        parser.add_argument(
            '-a', '--absolute', help='絶対位置指定でセル値を固定で取得する [セル位置=名前]の形式で列挙する. ex: A1=NAME1 A2=NAME2...', dest='absolute', nargs='*', default={}, action=KeyValuesParseAction)
        return parser

    def new_context(self, *, args):
        return ExcelRenderContext(args=args)

    def new_render(self, *, context: RenderContext):
        return ExcelRender(context=context)

    def call_render(self, *, render, source, out):
        """
        openpyxlがxlsxファイルのストリームを開けないので、in側はファイル名だけを扱う
        """
        context = render.context
        out_stream = sys.stdout
        try:
            if out is not sys.stdout:
                out_stream = open(
                    out, encoding=context.output_encoding, mode='w')

            render.render(source=source, output=out_stream)
        finally:
            if out is not sys.stdout:
                out_stream.close()
