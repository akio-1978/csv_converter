import io
import sys
import argparse

from .render import Render
from .context import RenderContext

# CommandRunnerのデフォルト実装


class Command():

    def register_self(self, *, main_parser: argparse.ArgumentParser) -> None:
        parser = self.create_parser(main_parser=main_parser)
        self.add_arguments(parser=parser)
    def create_parser(self, *, main_parser):
        return main_parser.add_parser('nop', help='NOP for test')

    def add_arguments(self, *, parser):
        parser.set_defaults(command_instance=self)

        self.add_defaiult_options(parser=parser)
        self.add_positional_arguments(parser=parser)
        self.add_optional_arguments(parser=parser)

        return parser

    def add_defaiult_options(self, *, parser):
        parser.add_argument('-o', '--out', metavar='file',
                            help='output file(default stdout).', default=sys.stdout)
        # source encoding
        parser.add_argument('--input-encoding', metavar='enc',
                            help='source encoding.', default='utf-8')
        # dest encoding
        parser.add_argument('--output-encoding', metavar='enc',
                            help='output encoding.', default='utf-8')
        # template encoding
        parser.add_argument('--template-encoding', metavar='enc',
                            help='jinja2 template encoding.', default='utf-8')
        parser.add_argument('-p', '--parameters', nargs='*',
                            help='additional values [KEY=VALUE] format.', action=KeyValuesParseAction)

    def add_positional_arguments(self, *, parser):
        parser.add_argument('template', help='jinja2 template to use.')
        parser.add_argument('source', help='rendering text.',
                            nargs='?', default=sys.stdin)

    def add_optional_arguments(self, *, parser):
        pass

    def execute(self, *, args: argparse.Namespace):
        context = self.new_context(args=args)
        render = self.new_render(context=context)
        self.call_render(render=render, source=args.source, out=args.out)

    def new_context(self, *, args: argparse.Namespace):
        return RenderContext(args=args)

    def new_render(self, *, context:RenderContext):
        return Render(context=context)

    def call_render(self, *, render: Render, source, out):
        context = render.context
        in_stream = sys.stdin
        out_stream = sys.stdout
        try:
            if source is not sys.stdin:
                in_stream = open(
                    source, encoding=context.input_encoding)
            if out is not sys.stdout:
                out_stream = open(context.out, mode='w',
                                  encoding=context.output_encoding)
            else:
                out_stream = io.TextIOWrapper(
                    sys.stdout.buffer, encoding=context.output_encoding)

            render.render(source=in_stream, output=out_stream)
        finally:
            if source is not sys.stdin:
                in_stream.close()
            if out is not sys.stdout:
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
