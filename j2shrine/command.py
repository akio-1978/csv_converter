import io
import sys
import argparse
import json

from .render import Render
from .context import RenderContext

# CommandRunnerのデフォルト実装


class Command():

    def __init__(self,*, master: argparse.ArgumentParser):
        self.parser = master.add_parser('nop', help='NOP for test')
        master.set_defaults(command_instance=self)

    _render = Render
    _context = RenderContext

    def setup(self):
        self.add_defaiult_options()
        self.add_positional_arguments()
        self.add_optional_arguments()

    def add_defaiult_options(self):
        self.parser.add_argument('-o', '--out', metavar='file',
                            help='出力先ファイル 省略時はstdout.', default=sys.stdout)
        # source encoding
        self.parser.add_argument('--input-encoding', metavar='enc',
                            help='入力時の文字エンコーディング.', default='utf-8')
        # dest encoding
        self.parser.add_argument('--output-encoding', metavar='enc',
                            help='出力時の文字エンコーディング.', default='utf-8')
        # template encoding
        self.parser.add_argument('--template-encoding', metavar='enc',
                            help='jinja2テンプレートファイルのエンコーディング.', default='utf-8')
        self.parser.add_argument('-p', '--parameters', nargs='*', default={},
                            help='テンプレート内で参照可能な追加のパラメータ [KEY=VALUE] 形式で列挙.', action=KeyValuesParseAction)

        self.parser.add_argument('-n', '--names', nargs='*',
                            help='テンプレート内で各行のカラムに付ける名前を左側から列挙 defaultは col_00 col02...')

        self.parser.add_argument('--config-file', metavar='file',
                            help='names parameters absoluteの各設定をjsonに記述したファイル')

    def add_positional_arguments(self):
        self.parser.add_argument('template', help='使用するjinja2テンプレート.')
        self.parser.add_argument('source', help='レンダリング対象ファイル 省略時はstdin.',
                            nargs='?', default=sys.stdin)

    def add_optional_arguments(self):
        pass

    def execute(self, *, args: argparse.Namespace):
        context = self._context(args=ArgsBuilder(args=args, merge_keys=self.merge_keyset()).build())
        render = self._render(context=context)
        self.call_render(render=render, source=args.source, out=args.out)

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

    def merge_keyset(self):
        """設定ファイルとコマンドラインをマージすべき項目名を返す"""
        return set(('parameters',))

class KeyValuesParseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        """=区切りで複数与えられた値をdictで格納する
            ex.
            args:A=1 B=2 C=3
            dict:{'A' : '1', 'B' : '2', 'C' : '3'}
        """
        setattr(namespace, self.dest, self.parse_key_values(values))

    def parse_key_values(self, values):
        key_values = {}
        for value in values:
            key_value = value.partition('=')
            key_values[key_value[0]] = key_value[2]
        return key_values

class ArgsBuilder:
    """ コマンドライン引数argsと設定ファイルの中身をマージする
        設定ファイルは引数--config-fileで指定されたjsonファイルであり、引数--config-fileが指定されていればロードする
        ロードしたjsonの項目を順次argsにsetattrする形でマージを行う 
        argsはjsonより優先する。jsonとargsに同じ項目が指定された場合はsetattrしない
        一部dictについて引数と設定ファイルをマージする、この場合も同一の項目は引数側を優先する
    """
    def __init__(self, args:argparse.Namespace, merge_keys:set) -> None:
        self.args = args
        self.merge_keys = merge_keys
        
    def build(self):
        """ jsonで記述された設定ファイルを読み込む
            設定ファイルとコマンドラインから同じ値が指定されている場合、コマンドラインの値を優先する
            引数parametersのみ、設定ファイルとコマンドラインをマージする
        """
        config = self.default_params()
        if self.given('config_file'):
            with open(self.args.config_file) as src:
                config.update(json.load(src))

        for key, value in config.items():
            if key in self.merge_keys:
                # dictをマージして設定し直す
                value.update(getattr(self.args, key))
                setattr(self.args, key, value)
            elif (not self.given(key)):
                # 設定ファイルの値を引数に追加する
                setattr(self.args, key, value)
        return self.args

    def given(self, k):
        """ hasattr と not None が長いのでまとめる """
        return hasattr(self.args, k) and getattr(self.args, k) is not None

    def default_params(self):
        """argsとjsonの両方で指定されなかった場合のデフォルト値"""
        return {
            'input_encoding': 'utf8',
            'output_encoding': 'utf8',
            'template_encoding': 'utf8',
        }
        
        