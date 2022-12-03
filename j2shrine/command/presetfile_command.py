
from . base_command import Command
from ..render.csv_render import CsvRender, CsvRenderContext
import sys
class CsvCommand(Command):

    def create_parser(self,*, main_parser):
        return main_parser.add_parser('csv', help = 'rendaring csv format')

    def add_positional_arguments(self, *, parser):
        parser.add_argument('template', help='jinja2 template to use.')
        parser.add_argument('preset', help='preset config file.')
        parser.add_argument('source', help='rendering text.', nargs='?', default=sys.stdin)

    def add_optional_arguments(self,*, parser):
        # flag first line is header
        parser.add_argument('-H', '--header', help='csv with header.', dest='read_header', action='store_true')
        # flag tab separate values
        parser.add_argument('-d', '--delimiter', metavar='', help='column delimiter.', default=',')
        # skip head lines
        parser.add_argument('-s', '--skip-lines', metavar='', type=int, help='skip n lines.', default=0)
        return parser

    def context(self):
        return CsvRenderContext()

    def render(self, *, context):
        return CsvRender(context=context)
