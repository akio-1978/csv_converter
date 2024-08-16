import sys
import argparse
import json
from .csv.csv_command import CsvCommand
from .excel.excel_command import ExcelCommand
from .json.json_command import JsonCommand


class Runner():
    """コマンドラインから呼び出される処理の起点となるクラス"""

    def __init__(self, *, args:list):
        self.args = args

    def add_command(self, *, parser:argparse.ArgumentParser):
        """サブコマンドのパーサを構築する
            各コマンドはインスタンスを生成した時点でパーサに登録されている
            dictは事前チェックのために使う
            """
        parsers=parser.add_subparsers(required=True)
        return {
            'csv' : CsvCommand(parsers=parsers),
            'excel' : ExcelCommand(parsers=parsers),
            'json' : JsonCommand(parsers=parsers),
        }

    def execute(self):
        """プログラム実行"""
        # コマンドラインパーサーの作成
        parser = argparse.ArgumentParser(prog='j2shrine', add_help=True)
        # サブコマンドの設定と取得
        commands = self.add_command(parser=parser)
        # コマンドのcontextを取得する
        context = self.get_context(commands=commands, args=self.args)

        # コマンドライン引数をパースする。contextに直接書きこむ。
        context = parser.parse_args(self.args, namespace=context)
        # parse_argsから得られたコマンドをexecuteする
        command = context.command_instance
        command.execute(context=context)

    def get_context(self, *, commands:dict, args:list):
        """引数を一部だけパースしてcontextを得る"""
        # サブコマンドと設定ファイルだけを取得する
        # このパースでは他の引数は無視する
        ctx_parser = argparse.ArgumentParser(add_help=False,)
        ctx_parser.add_argument('cmd', default=None)
        ctx_parser.add_argument('--config-file', default=None)
        ns, unknown = ctx_parser.parse_known_args(args)

        if ns.cmd not in commands:
            # サブコマンドが特定できない場合にNamespaceを返す
            # このルートは後のparse_argsで確実に失敗して、ヘルプを表示させる
            return argparse.Namespace()

        # コマンドからコンテキストの取得
        ctx = commands[ns.cmd].context_class()()
        if ns.config_file:
            # 設定ファイルが存在すればコンテキストに書き込む
            self.load_config(ctx=ctx, filename=ns.config_file)
        return ctx

    def load_config(self,*, ctx, filename):
        """ 設定ファイルの内容をcontextにsetattrする"""
        with open(filename) as src:
            config = json.load(src)

            # 設定ファイルの中身を順次argsに反映する
            for key, value in config.items():
                setattr(ctx, key, value)
        return ctx

def main():
    """sys.argvをargparseに直接渡さない（Ruunerのテスト対策）"""
    starter = Runner(args=sys.argv[1:] if len(sys.argv) > 1 else ['', ''])
    starter.execute()

if __name__ == '__main__':
    main()
