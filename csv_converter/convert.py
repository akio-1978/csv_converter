import sys
import io
import argparse
from csv_converter.converter import CsvConverter, ConverterContext


class ContextBuilder():

    def argument_to_context(self, args):
        # コマンドライン引数の処理
        parser = argparse.ArgumentParser()
        
        # 使用するテンプレートと処理するcsvファイル
        # jinja2 template to use.
        parser.add_argument('template', help='jinja2 template to use.')
        parser.add_argument('csv', help='transform csv.')
        parser.add_argument('key_value_options', nargs='*', help='additional values [KEY=VALUE] format.', action=KeyValuesParseAction)
        # flag first line is header
        parser.add_argument('-H', '--header', help='first line is header.', dest='use_header', action='store_true')
        # flag tab separate values
        parser.add_argument('-T', '--tab', metavar='', help='tab separate values.', dest='delimiter', default=',', action=DelimiterSelectAction)
        # output file (default stdout)
        parser.add_argument('-O', '--output', metavar='file', help='output file.')
        # source encoding
        parser.add_argument('--input-encoding', metavar='enc', help='file encoding.', default='utf-8')
        # dest encoding
        parser.add_argument('--output-encoding', metavar='enc', help='output file encoding.', default='utf-8')

        context = self.create_context(namespace = parser.parse_args(args=args))

        return context

    def create_context(self, *, namespace):
        context = ConverterContext(template_source = namespace.template)        

        context.csv = namespace.csv
        context.options = namespace.key_value_options
        context.use_header = namespace.use_header
        context.delimiter = namespace.delimiter
        context.input_encoding = namespace.input_encoding
        context.output_encoding = namespace.output_encoding
        context.output = namespace.output

        return context

    # def parse_addtional(self, values):
    #     addtional = {}
    #     for value in values:
    #         key_value = value.split('=')
    #         addtional[key_value[0]] = key_value[1]
    #     return addtional

class KeyValuesParseAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.parse_key_values(values))

    def parse_key_values(self, values):
        key_values = {}
        for value in values:
            key_value = value.partition('=')
            key_values[key_value[0]] = key_value[2]
        return key_values

class DelimiterSelectAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string):
        delimiter = ','
        if option_string == '-T' or option_string == '--tab':
            delimiter = '\t'

        setattr(namespace, self.dest, delimiter)


def convertToFile(*, converter, source, file):
    with open(file, mode='w') as output:
        with open(source) as input:
            converter.convert(source=input, output=output)


def convertToStdout(*, converter, source):
        with open(source) as input:
            converter.convert(source=input, output=sys.stdout)


if __name__ == '__main__':
    # windows対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    context = ContextBuilder().argument_to_context(sys.argv[1:])
    converter = CsvConverter(context=context)

    if context.output is not None:
        convertToFile(converter=converter, source=context.csv, file=context.output)
    else:
        convertToStdout(converter=converter, source=context.csv)
