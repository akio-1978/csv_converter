import io
import sys
import argparse
import json

from .render import Render
from .context import RenderContext
from .renderutils import StreamWrapper

# CommandRunnerのデフォルト実装


class Command():

    def __init__(self,*, factory: argparse.ArgumentParser):
        """このコンストラクタはテスト用で、何もしないサブコマンドを生成する"""
        self.parser = factory.add_parser('nop', help='NOP for test')
        factory.set_defaults(command_instance=self)

    def render_class(self):
        """Commandが使うRenderのクラスを返す"""
        return Render
    def context_class(self):
        """Commandが使うContextのクラスを返す"""
        return RenderContext

    def setup(self):
        """ 各コマンドの引数を定義する
            サブコマンドでoverrideすることが前提
        """
        self.add_defaiult_options()
        self.add_positional_arguments()
        self.add_optional_arguments()

    def add_positional_arguments(self):
        """ 位置引数をパーサに追加する
            位置引数を書き直したい場合にオーバーライドする
        """
        self.parser.add_argument('template', help='使用するjinja2テンプレート.')
        self.parser.add_argument('source', help='レンダリング対象ファイル 省略時はstdin.',
                            nargs='?', default=sys.stdin)

    def add_defaiult_options(self):
        """ オプション引数をパーサに追加する
            ここで全てのサブコマンドで共通して使うオプションの追加を想定している
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
                            help='テンプレート内で各行のカラムに付ける名前を左側から列挙 defaultは col_00 col02...')

        self.parser.add_argument('--config-file', metavar='file',
                            help='names parameters absoluteの各設定をjsonに記述したファイル')

    def add_optional_arguments(self):
        """サブコマンドでオプション引数を追加する場合にオーバーライドする"""
        pass

    def execute(self, *, args: argparse.Namespace):
        """ パーサから返された値を使ってコマンドの処理を実行
        """
        # context及びrenderのクラスを取得
        ctx_class = self.context_class()
        render_class = self.render_class()

        # context及びrenderのインスタンスを生成
        context = ctx_class(args=ParamsBuilder(args=args, merge_keys=self.merge_keys(), default_params=self.default_params()).build())
        render = render_class(context=context)
        
        # レンダリング実行
        self.call_render(render=render, source=args.source, out=args.out)

    def call_render(self, *, render: Render, source:str | io.TextIOWrapper, out:str | io.TextIOWrapper):
        context = render.context
        # ファイル名でもstdin stdoutでも区別せずStreamWrapperで吸収する
        with StreamWrapper(useof=source,encoding=context.input_encoding) as src:
            with StreamWrapper(useof=out,encoding=context.output_encoding, mode='w') as dest:
                render.render(source=src, output=dest)

    def merge_keys(self):
        """設定ファイルとコマンドラインをマージすべき項目名を返す"""
        return set(('parameters',))

    def default_params(self):
        """argsとjsonの両方で指定されなかった場合のデフォルト値"""
        return {
            'input_encoding': 'utf8',
            'output_encoding': 'utf8',
            'template_encoding': 'utf8',
        }


class KeyValuesParseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        """=区切りで複数与えられた値をdictで格納する
            ex.
            args:A=1 B=2 C=3
            dict:{'A' : '1', 'B' : '2', 'C' : '3'}
        """
        setattr(namespace, self.dest, self.parse_key_values(values))

    def parse_key_values(self, values:str):
        key_values = {}
        for value in values:
            key_value = value.partition('=')
            key_values[key_value[0]] = key_value[2]
        return key_values

class ParamsBuilder:
    """ argparse.Namespaceとjsonファイルをマージして、レンダリングの設定を得る。
        jsonファイルはNamespaceに属性config_fileで指定される。このjsonはロードしてdictとして扱う。
        dict内の全てのkey/valueをNamespaceにsetattrする。
        ただし、Namespaceに既にkeyと同名のattrがある場合はsetattrせずにNamespaceを優先する。
        
        Namespace中にdictを持つ特定のキーについて、Namespaceとdictの値をマージする。
        Namespaceとdict双方に存在しない特定のキーについて、別途指定した値で補完する。
    """
    def __init__(self, args:argparse.Namespace, merge_keys:set, default_params:dict) -> None:
        self.args = args
        self.merge_keys = merge_keys
        self.default_params = default_params
        
    def build(self):
        """ jsonで記述された設定ファイルを読み込む
            設定ファイルとコマンドラインから同じ値が指定されている場合、コマンドラインの値を優先する
            引数parametersのみ、設定ファイルとコマンドラインをマージする
        """
        config = self.default_params
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

    def given(self, k:str):
        """ 属性が存在しないか、値がNoneではない """
        return hasattr(self.args, k) and getattr(self.args, k)

        
        