
from . base_command import Command
from ..render.csv_render import CsvRender, CsvRenderContext
class CsvCommand(Command):

    def add_arguments(self, subparser):
        csv_command_parser = super().add_arguments(subparser=subparser)
        # flag first line is header
        csv_command_parser.add_argument('-H', '--header', help='with header.', dest='use_header', action='store_true')
        # flag tab separate values
        csv_command_parser.add_argument('-d', '--delimiter', metavar='', help='column delimiter.', default=',')
        # skip head lines
        csv_command_parser.add_argument('-s', '--skip-lines', metavar='', help='skip n lines.', default=0)
        return csv_command_parser

    def context(self):
        return CsvRenderContext()

    def render(self, *, context):
        return CsvRender(context=context)
