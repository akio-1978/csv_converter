import sys
import argparse
from . command.csv_command import CsvCommand
from . render.csv_render import CsvRenderContext


class Starter():

    def setup(self):
        self.parser = self.create_mainparser()
        self.subparsers = self.parser.add_subparsers(required=True)
        self.set_subparsers()

    def set_subparsers(self):
        csv_parser = self.parser.add_parser('csv', help = 'rendaring csv format')
        csv_parser.set_defaults(command_class = CsvCommand)
        csv_parser.set_defaults(context_class = CsvRenderContext)

    def create_mainparser():
        base_parser = argparse.ArgumentParser()
        base_parser.add_argument('template', help='jinja2 template to use.')
        base_parser.add_argument('source', help='rendering text.', nargs='?', default=sys.stdin)
        base_parser.add_argument('-p', '--parameters', nargs='*', help='additional values [KEY=VALUE] format.', action=KeyValuesParseAction)
        # output file (default stdout)
        base_parser.add_argument('-o', '--out', metavar='file', help='output file.', default=sys.stdout)
        # source encoding
        base_parser.add_argument('--input-encoding', metavar='enc', help='source encoding.', default='utf-8')
        # dest encoding
        base_parser.add_argument('--output-encoding', metavar='enc', help='output encoding.', default='utf-8')

        return base_parser

    def create_render(self):
        namespace = self.parser.parse_args()
        command = namespace.command_class()
        context = command.create_context()
        self.assign_args(context=context, namespace=namespace)
        return command.render_class(context=context)

    def execute(self, *, context):

        render = self.create_render()

        in_stream = sys.stdin
        out_stream = sys.stdout
        try:
            if in_stream is not context.source:
                in_stream = open(context.source, encoding=context.input_encoding)
            if out_stream is not context.out:
                out_stream = open(context.out, encoding=context.output_encoding)

            render.render(source = in_stream, output = out_stream)
        finally:
            if in_stream is not context.source:
                in_stream.close()
            if out_stream is not context.out:
                out_stream.close()


    # コマンド引数からコンテキストを作る
    def assign_args(self, *, context, namespace):
        arguments = vars(namespace)
        for (key, value) in arguments:
            setattr(context, key, value)
        return context

class KeyValuesParseAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.parse_key_values(values))

    def parse_key_values(self, values):
        key_values = {}
        for value in values:
            key_value = value.partition('=')
            key_values[key_value[0]] = key_value[2]
        return key_values


if __name__ == '__main__':
    starter = Starter()
    starter.setup()
    starter.execute()
