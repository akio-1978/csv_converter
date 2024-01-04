
from ..command import Command
from .csv_render import CsvRender
from .csv_context import CsvRenderContext


class CsvCommand(Command):

    def create_parser(self, *, main_parser):
        return main_parser.add_parser('csv', help='rendaring csv format')

    def add_optional_arguments(self, *, parser):
        # flag first line is header
        parser.add_argument('-H', '--header', help='csv with header.',
                            dest='read_header', action='store_true')
        # flag tab separate values
        parser.add_argument('-d', '--delimiter', metavar='',
                            help='column delimiter.', default=',')
        # skip head lines
        parser.add_argument('-s', '--skip-lines', metavar='',
                            type=int, help='skip n lines.', default=0)
        return parser

    def new_context(self, *, args):
        return CsvRenderContext(args=args)

    def new_render(self, *, context):
        return CsvRender(context=context)
