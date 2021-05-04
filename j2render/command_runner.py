import sys
import io
import argparse
from j2render.csvrenderlogic import CsvRenderLogic, CsvRenderContext
from j2render.rendercontext import RenderContext


class ContextBuilder():

    def create(self):
        parser = self.create_parser()
        # 2021/05/05 ここから具象コマンドクラスを決定するキモのポイント
        context = self.create_context(parser=parser, args = sys.argv[1:])

    def create_parser(self):
        # コマンドライン引数の処理
        parser = argparse.ArgumentParser()
        
        # 使用するテンプレートと処理するcsvファイル
        # jinja2 template to use.
        parser.add_argument('template', help='jinja2 template to use.')
        parser.add_argument('source', help='rendering text.', nargs='?', default=sys.stdin)
        
        parser.add_argument('-f', '--format', help='source format')
        # output file (default stdout)
        parser.add_argument('-o', '--out', metavar='file', help='output file.', default=sys.stdout)
        # source encoding
        parser.add_argument('--input-encoding', metavar='enc', help='source encoding.', default='utf-8')
        # dest encoding
        parser.add_argument('--output-encoding', metavar='enc', help='output encoding.', default='utf-8')
        parser.add_argument('-p', '--parameters', nargs='*', help='additional values [KEY=VALUE] format.', action=KeyValuesParseAction)

        return parser

    def create_context(self, *, parser, args):
        namespace = self.create_context(namespace = parser.parse_args(args=args))
        context = RenderContext(template_source = namespace.template)

        context.source = namespace.source
        context.parameters = namespace.parameters
        context.use_header = namespace.use_header
        context.delimiter = namespace.delimiter
        context.input_encoding = namespace.input_encoding
        context.output_encoding = namespace.output_encoding
        context.out = namespace.out

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

def convertToFile(*, converter, source, file):
    with open(file, mode='w', encoding=converter.context.output_encoding) as output:
        with open(source) as input:
            converter.convert(source=input, output=output)

def convertToStdout(*, converter, source):
        with open(source) as input:
            converter.convert(source=input, output=sys.stdout)

