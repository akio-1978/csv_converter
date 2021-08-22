import sys
import argparse

from ..render.base_render import Render, RenderContext

# CommandRunnerのデフォルト実装
class Command():

    def __init__(self,*, parser_creator) -> None:
        parser = self.create_parser(parser_creator=parser_creator)
        self.add_arguments(parser=parser)

    def create_parser(self,*, parser_creator):
        return parser_creator.add_parser('nop', help = 'NOP for test')

    def add_arguments(self,*,parser):
        parser.set_defaults(command_instance = self)

        self.add_defaiult_options(parser=parser)
        self.add_positional_arguments(parser=parser)
        self.add_optional_arguments(parser=parser)

        return parser

    def add_defaiult_options(self, *, parser):
        parser.add_argument('-o', '--out', metavar='file', help='output file(default stdout).', default=sys.stdout)
        # source encoding
        parser.add_argument('--input-encoding', metavar='enc', help='source encoding.', default='utf-8')
        # dest encoding
        parser.add_argument('--output-encoding', metavar='enc', help='output encoding.', default='utf-8')
        parser.add_argument('-p', '--parameters', nargs='*', help='additional values [KEY=VALUE] format.', action=KeyValuesParseAction)

    def add_positional_arguments(self, *, parser):
        parser.add_argument('template', help='jinja2 template to use.')
        parser.add_argument('source', help='rendering text.', nargs='?', default=sys.stdin)

    def add_optional_arguments(self, *, parser):
        pass

    def context(self):
        return RenderContext()

    def render(self, *, context):
        return Render(context=context)

    def render_io(self, *, render, context):
        in_stream = sys.stdin
        out_stream = sys.stdout
        try:
            if context.source is not sys.stdin:
                in_stream = open(context.source, encoding=context.input_encoding)
            if context.out is not sys.stdout:
                out_stream = open(context.out, encoding=context.output_encoding)

            render.render(source = in_stream, output = out_stream)
        finally:
            if context.source is not sys.stdin:
                in_stream.close()
            if context.out is not sys.stdout:
                out_stream.close()


class KeyValuesParseAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.parse_key_values(values))

    def parse_key_values(self, values):
        key_values = {}
        for value in values:
            key_value = value.partition('=')
            key_values[key_value[0]] = key_value[2]
        return key_values
