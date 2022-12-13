import argparse
import sys
from . base_command import Command
from ..render.excel_render import ExcelRender, ExcelRenderContext
class ExcelCommand(Command):

    HELP_SHEETS = """read sheets range ('1' sheet1 only. '1:4' read 1 to 4. '1:' read 1 to all)"""
    HELP_READ_RANGE = """read cells range ('A1:D4' read A1 to D4 'A1:D' read A1 to D all rows.)"""

    def create_parser(self,*, main_parser):
        return main_parser.add_parser('excel', help = 'rendaring excel file', formatter_class=argparse.RawTextHelpFormatter)

    def add_positional_arguments(self, *, parser):
        parser.add_argument('template', help='jinja2 template to use.')
        # source book can't read from stdin
        parser.add_argument('source', help='rendering Excel book.')
        parser.add_argument('sheets', help=ExcelCommand.HELP_SHEETS)
        parser.add_argument('read_range', help=ExcelCommand.HELP_READ_RANGE)
        return parser

    def add_optional_arguments(self, *, parser):
        super().add_optional_arguments(parser=parser)
        parser.add_argument('-F', '--fixed', help='get fixed position cells. ex: A1 B2...', dest='fixed', nargs='*', default=[])
        return parser

    def newContext(self):
        return ExcelRenderContext()

    def get_render(self, *, context):
        return ExcelRender(context=context)

    def rendering(self, *, render, context):
        """
        openpyxlがxlsxファイルのストリームを開けないので、in側はファイル名だけを扱う
        """
        out_stream = sys.stdout
        try:
            if context.out is not sys.stdout:
                out_stream = open(context.out, encoding=context.output_encoding, mode='w')

            render.render(source = context.source, output = out_stream)
        finally:
            if context.out is not sys.stdout:
                out_stream.close()
