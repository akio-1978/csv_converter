import sys
import io
import argparse
from j2render.csvrenderlogic import CsvRenderLogic, CsvRenderContext


class CsvContextBuilder():

    def argument_to_context(self, args):
        # コマンドライン引数の処理
        parser = argparse.ArgumentParser()
        
        # 使用するテンプレートと処理するcsvファイル
        # jinja2 template to use.
        parser.add_argument('template', help='jinja2 template to use.')
        parser.add_argument('csv', help='transform csv.')
        parser.add_argument('-O', '--options', nargs='*', help='additional values [KEY=VALUE] format.', action=KeyValuesParseAction)
        # flag first line is header
        parser.add_argument('-H', '--header', help='use first line is header.', dest='use_header', action='store_true')
        # flag tab separate values
        parser.add_argument('-D', '--delimiter', metavar='', help='values delimiter.', default=',')
        # output file (default stdout)
        parser.add_argument('-O', '--output', metavar='file', help='output file.')
        # source encoding
        parser.add_argument('--input-encoding', metavar='enc', help='file encoding.', default='utf-8')
        # dest encoding
        parser.add_argument('--output-encoding', metavar='enc', help='output file encoding.', default='utf-8')

        context = self.create_context(namespace = parser.parse_args(args=args))

        return context

    def create_context(self, *, namespace):
        context = CsvRenderContext(template_source = namespace.template)        

        context.csv = namespace.csv
        context.options = namespace.options
        context.use_header = namespace.use_header
        context.delimiter = namespace.delimiter
        context.input_encoding = namespace.input_encoding
        context.output_encoding = namespace.output_encoding
        context.output = namespace.output

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


if __name__ == '__main__':
    # windows対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    context = CsvContextBuilder().argument_to_context(sys.argv[1:])
    converter = CsvRenderLogic(context=context)

    if context.output is not None:
        convertToFile(converter=converter, source=context.csv, file=context.output)
    else:
        convertToStdout(converter=converter, source=context.csv)
