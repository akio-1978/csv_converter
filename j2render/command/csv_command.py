
from . command import Command
from ..render.csv_render import CsvRender, CsvRenderContext
class CsvCommand(Command):

    def subcommand_parser(self, parser):
        # flag first line is header
        parser.add_argument('-H', '--header', help='use first line is header.', dest='use_header', action='store_true')
        # flag tab separate values
        parser.add_argument('-d', '--delimiter', metavar='', help='values delimiter.', default=',')
        # skip head lines
        parser.add_argument('-s', '--skip-lines', metavar='', help='skip head lines.', default=0)

        return parser

    def context_class(self):
        return CsvRenderContext()

    def render_class(self, *, context):
        return CsvRender(context=context)
