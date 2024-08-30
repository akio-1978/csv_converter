import io
import sys
import argparse

from .loader import Loader
from .context import RenderContext
from .utils import get_stream

# CommandRunnerのデフォルト実装


class Command():

    def __init__(self):
        """このコンストラクタはテスト用で、何もしないコマンドを生成する"""
        self.setup()

    def loader_class(self):
        """Commandが使うLoaderのクラスを返す"""
        return Loader

    def setup(self):
        """ コマンドの引数を定義する
            引数定義は3つのメソッドに分かれており、それぞれ個別にオーバーライドできる
        """
        self.add_default_options()
        self.add_positional_arguments()
        self.add_optional_arguments()

    def add_positional_arguments(self):
        """ 位置引数をパーサに追加する
            位置引数を書き直したい場合にオーバーライドする
            引数templateとsourceは必須のため、サブコマンドではsuper呼出しするのが好ましい
        """
        self.parser.add_argument('template', help='使用するjinja2テンプレート.')
        self.parser.add_argument('source', help='レンダリング対象ファイル 省略時はstdin.',
                            nargs='?', default=sys.stdin)

    def add_optional_arguments(self):
        """サブコマンドでオプションを追加する場合にこのメソッドをオーバーライドする"""
        pass

    def add_default_options(self):
        """ オプション引数をパーサに追加する
            全てのサブコマンドで共通して使うオプションを想定しているので
            オーバーライドは不要
        """
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
                            help='テンプレート内で各行のカラムに付ける名前を左側から列挙 defaultは col_00 col02...', default=[])

        self.parser.add_argument('--config-file', metavar='file',
                            help='names parameters absoluteの各設定をjsonに記述したファイル')

    def execute(self, *, args:list, context:RenderContext):
        """ レンダリング実行 """
        # コマンドのパース argsをサブコマンドひとつ分読み進めたいので、長さをチェックする
        context = self.parser.parse_args(args[1:] if len(args) > 0 else [], 
                               namespace=context)
        
        # renderインスタンスを生成
        render = self.loader_class()(context=context)
        
        # レンダリング実行
        self.call_render(render=render, source=context.source, out=context.out)

    def call_render(self, *, render: Loader, source:str | io.TextIOWrapper, out:str | io.TextIOWrapper):
        context = render.context
        # sourceはファイル名かstdin/stdoutなので間にwrapperを挟む
        with get_stream(source=source,encoding=context.input_encoding) as src:
            with get_stream(source=out,encoding=context.output_encoding, mode='w') as dest:
                render.render(source=src, output=dest)

class KeyValuesParseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        """=区切りで複数与えられた値をdictで格納する
            ex.
            args:A=1 B=2 C=3
            dict:{'A' : '1', 'B' : '2', 'C' : '3'}
        """
        # 設定ファイルから読み込まれた値がある場合、コマンドライン側を優先してマージする
        arg_dict = self.parse_key_values(values)
        if hasattr(namespace, self.dest):
            getattr(namespace, self.dest).update(arg_dict)
        else:        
            setattr(namespace, self.dest, arg_dict)

    def parse_key_values(self, values):
        key_values = {}
        for value in values:
            key_value = value.partition('=')
            key_values[key_value[0]] = key_value[2]
        return key_values

        