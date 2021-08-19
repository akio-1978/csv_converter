import sys
import argparse

from ..render.base_render import Render, RenderContext

# CommandRunnerのデフォルト実装
class Command():

    def add_arguments(self, subparser):
        subparser = self.add_positional_arguments(subparser)
        return self.add_optional_arguments(subparser)

    def add_positional_arguments(self, subparser):
        subparser.add_argument('template', help='jinja2 template to use.')
        subparser.add_argument('source', help='rendering text.', nargs='?', default=sys.stdin)
        return subparser

    def add_optional_arguments(self, subparser):
        subparser.add_argument('-o', '--out', metavar='file', help='output file.', default=sys.stdout)
        # source encoding
        subparser.add_argument('--input-encoding', metavar='enc', help='source encoding.', default='utf-8')
        # dest encoding
        subparser.add_argument('--output-encoding', metavar='enc', help='output encoding.', default='utf-8')
        subparser.add_argument('-p', '--parameters', nargs='*', help='additional values [KEY=VALUE] format.', action=KeyValuesParseAction)
        return subparser

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
