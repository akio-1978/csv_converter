import argparse
import sys
from . base_command import Command
from ..render.excel_render import ExcelRender, ExcelRenderContext
class ExcelCommand(Command):

    HELP_COLUMNS = """read column letters
A   read column A only
A-C read column A B C
A-  read from column A to last column
"""

    # HELP_ROWS = "row read range ex: 2 2-3 2-"
    HELP_ROWS = """read row numbers
2   read row 2 only
2-4 read row 2 3 4
2-  read from 2 to last row
"""

    HELP_SHEETS = """read sheets 
0   read sheets 2 only
0-2 read sheets 0 1 2
2-  read from 2 to last sheet
"""
    def create_parser(self,*, parser_creator):
        return parser_creator.add_parser('excel', help = 'rendaring excel file', formatter_class=argparse.RawTextHelpFormatter)

    def add_positional_arguments(self, *, parser):
        parser.add_argument('template', help='jinja2 template to use.')
        # source book can't read from stdin
        parser.add_argument('source', help='rendering Excel book.')
        parser.add_argument('sheets', help=ExcelCommand.HELP_SHEETS)
        parser.add_argument('columns', help=ExcelCommand.HELP_COLUMNS)
        parser.add_argument('rows', help=ExcelCommand.HELP_ROWS)
        # header from sheet rows
        parser.add_argument('header_row', help='row of use as header. if not specified use column letter.', nargs='?')

    def add_optional_arguments(self, *, parser):
        super().add_optional_arguments(parser=parser)
        # user specified headers
        parser.add_argument('--headers', help='user specified headers. ex: aaa bbb ccc...', dest='headers', nargs='*')
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
