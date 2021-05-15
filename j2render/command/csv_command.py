from j2render.render.csvrenderlogic import CsvRenderLogic, CsvRenderContext

class CsvCommand():

    def create_subparser(self, parser):
        # flag first line is header
        parser.add_argument('-H', '--header', help='use first line is header.', dest='use_header', action='store_true')
        # flag tab separate values
        parser.add_argument('-d', '--delimiter', metavar='', help='values delimiter.', default=',')

        return parser

    def context_class(self):
        return CsvRenderContext()

    def create_render_logic(self):
        return CsvRenderLogic()

    def exeute_command(self, *, context):
        pass