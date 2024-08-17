import sys
import argparse
import json
import j2shrine
from .csv.csv_command import CsvCommand
from .excel.excel_command import ExcelCommand
from .json.json_command import JsonCommand
from .context import RenderContext


class Runner():
    """コマンドラインから呼び出される処理の起点となるクラス"""

    def __init__(self, *, args:list):
        self.args = args
        self.commands = {
            'csv' : CsvCommand,
            'excel' : ExcelCommand,
            'json' : JsonCommand,
        }

    def execute(self):
        """プログラム実行"""
        # 実行するcommandの決定と設定ファイルがあれば読み取り
        command, context = self.get_context(args=self.args)

        # コマンドライン引数をパースする。contextに直接書きこむ。
        command().execute(args=self.args, context=context)

    def get_context(self, *, args:list):
        """引数を一部だけパースしてcontextとcommandを取得する"""
        # サブコマンドと設定ファイルだけを取得する、サブコマンドが対象外の場合ここで終了する
        ctx_parser = CustomHelpParser(prog=j2shrine.PROG_NAME)
        ctx_parser.add_argument('cmd', choices=['csv', 'excel', 'json'], default='')
        ctx_parser.add_argument('--config-file', default=None)
        ns, unknown = ctx_parser.parse_known_args(args)

        # コマンドからコンテキストの取得
        ctx = RenderContext()
        if ns.config_file:
            # 設定ファイルが存在すればコンテキストに書き込む
            self.load_config(ctx=ctx, filename=ns.config_file)
        return self.commands[ns.cmd], ctx

    def load_config(self,*, ctx, filename):
        """ 設定ファイルの内容をcontextにsetattrする"""
        with open(filename) as src:
            config = json.load(src)
            # 設定ファイルの中身を順次argsに反映する
            for key, value in config.items():
                setattr(ctx, key, value)
        return ctx

class CustomHelpParser(argparse.ArgumentParser):
    
    def format_usage(self) -> str:
        """一回目の予備パースでエラーが出た時、congi-fileオプションについて表示しない"""
        return f'usage: {j2shrine.PROG_NAME} [-h] {{csv,excel,json}} ...\n'

def main():
    """sys.argvをargparseに直接渡さない（Ruunerのテスト対策）"""
    starter = Runner(args=sys.argv[1:] if len(sys.argv) > 1 else ['', ''])
    starter.execute()

if __name__ == '__main__':
    main()
