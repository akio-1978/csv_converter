import io
import sys
import argparse
from csvtransformer.csv_transformer import CsvTransformer, TransfomerParameters

def parse_additinal(values):
    addtional = {}
    for value in values:
        key_value = value.split('=')
        addtional[key_value[0]] = key_value[1]
    return addtional

def parse_argument():
    # コマンドライン引数の処理
    parser = argparse.ArgumentParser()
    
    # 使用するテンプレートと処理するcsvファイル
    # jinja2 template to use.
    parser.add_argument('template', help='jinja2 template to use.')
    parser.add_argument('csv', help='transform csv.')
    parser.add_argument('additional', nargs='*', help='additional values [KEY=VALUE] format.')

    # flag first line is header
    parser.add_argument('-H', '--header', help='first line is header.', action='store_true')
    # flag tab separate values
    parser.add_argument('-T', '--tab', help='tab separate values.', action='store_true')
    # source encoding
    parser.add_argument('-E', '--encoding', metavar='enc', help='file encoding.', nargs=1, default='utf-8')
    # output file (default stdout)
    parser.add_argument('-O', '--output', metavar='file', help='output file.', nargs=1)

    options = TransfomerParameters()
    parser.parse_args(namespace=options)
    options.additional = parse_additinal(options.additional)

    return options


if __name__ == '__main__':
    # windows対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

