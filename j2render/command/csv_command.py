
from . base_command import Command
from ..render.csv_render import CsvRender, CsvRenderContext
class CsvCommand(Command):

    def subcommand_parser(self, parser):
        csv_command_parser = super().subcommand_parser(parser=parser)
        # flag first line is header
        csv_command_parser.add_argument('-H', '--header', help='use first line is header.', dest='use_header', action='store_true')
        # flag tab separate values
        csv_command_parser.add_argument('-d', '--delimiter', metavar='', help='values delimiter.', default=',')
        # skip head lines
        csv_command_parser.add_argument('-s', '--skip-lines', metavar='', help='skip first n lines.', default=0)
        return csv_command_parser

    def context_class(self):
        return CsvRenderContext()

    def render_class(self, *, context):
        return CsvRender(context=context)
