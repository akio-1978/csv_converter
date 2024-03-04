
from j2shrine.context import RenderContext
from ..command import Command
from .csv_render import CsvRender
from .csv_context import CsvRenderContext


class CsvCommand(Command):

    def create_parser(self, *, main_parser):
        return main_parser.add_parser('csv', help='csvのレンダリングを行う')

    def add_optional_arguments(self, *, parser):
        # flag first line is header
        parser.add_argument('-H', '--header', help='先頭行をヘッダとして解釈するか？ヘッダは各カラムの名前として使用可能.',
                            dest='read_header', action='store_true')
        # flag tab separate values
        parser.add_argument('-d', '--delimiter', metavar='',
                            help="カラムの区切り文字 defaultは ',' .", default=',')
        # skip head lines
        parser.add_argument('-s', '--skip-lines', metavar='',
                            type=int, help='指定した数値分だけ先頭から行を読み飛ばす.', default=0)
        return parser

    def new_context(self, *, args):
        return CsvRenderContext(args=args)

    def new_render(self, *, context: RenderContext):
        return CsvRender(context=context)