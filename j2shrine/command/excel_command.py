import argparse
import sys
from . base_command import Command
from ..render.excel_render import ExcelRender, ExcelRenderContext
class ExcelCommand(Command):

    HELP_COLUMNS = """read columns range (A A-C A-)"""
    HELP_ROWS = """read row numbers range (1 2-4 1-)"""
    HELP_SHEETS = """read sheets range (1 1-4 1-)"""
    HELP_EPILOG = """range arguments format
  1   read 1 only
  1-4 read 1 2 3 4
  1-  read from 1 to last
  for column, specify letter ex: A, A-C, B-
"""

    def create_parser(self,*, main_parser):
        return main_parser.add_parser('excel', epilog= ExcelCommand.HELP_EPILOG, help = 'rendaring excel file', formatter_class=argparse.RawTextHelpFormatter)

    def add_positional_arguments(self, *, parser):
        parser.add_argument('template', help='jinja2 template to use.')
        # source book can't read from stdin
        parser.add_argument('source', help='rendering Excel book.')
        parser.add_argument('sheets', help=ExcelCommand.HELP_SHEETS)
        parser.add_argument('columns', help=ExcelCommand.HELP_COLUMNS)
        parser.add_argument('rows', help=ExcelCommand.HELP_ROWS)
        # header from sheet rows
        parser.add_argument('header-row', help='headers row number. default headers use column letter.', nargs='?')

    def add_optional_arguments(self, *, parser):
        super().add_optional_arguments(parser=parser)
        parser.add_argument('-E', '--extra', help='get fixed position cells. ex: A1 B2...', dest='extra', nargs='*')

    def context(self):
        return ExcelRenderContext()

    def render(self, *, context):
        return ExcelRender(context=context)

    def render_io(self, *, render, context):
        """
        openpyxlがxlsxファイルのストリームを開けないので、in側はファイル名だけを扱う
        """
        out_stream = sys.stdout
        try:
            if context.out is not sys.stdout:
                out_stream = open(context.out, encoding=context.output_encoding)

            render.render(source = context.source, output = out_stream)
        finally:
            if context.out is not sys.stdout:
                out_stream.close()
