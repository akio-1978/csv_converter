import sys
import argparse
from .csv.csv_command import CsvCommand
from .excel.excel_command import ExcelCommand
from .json.json_command import JsonCommand


class Runner():
    """コマンドラインから呼び出される処理の起点となるクラス"""

    def __init__(self, *, args:list):
        self.args = args

    def register_subcommand(self, *, subparser_factory:argparse.ArgumentParser):
        """サブコマンドのパーサを構築する"""
        CsvCommand(factory=subparser_factory).setup()
        ExcelCommand(factory=subparser_factory).setup()
        JsonCommand(factory=subparser_factory).setup()

    def execute(self):
        """プログラムの実行本体"""
        # ArgumentParserの初期化
        self.parser = argparse.ArgumentParser(prog='j2shrine',
                                              add_help=True,
                                              )
        # ArgumentParserにサブコマンドのパーサーを追加する
        self.register_subcommand(
            subparser_factory=self.parser.add_subparsers(required=True))

        # コマンドライン引数をパースする
        namespace = self.parser.parse_args(self.args)
        # parse_argsから得られたコマンドをexecuteする
        command = namespace.command_instance
        command.execute(args=namespace)

def main():
    """argparseでsys.argvではなく明示的にリストを受け取るため、リストの長さが足りない場合を補完する"""
    starter = Runner(args=sys.argv[1:] if len(sys.argv) > 1 else ['', ''])
    starter.execute()

if __name__ == '__main__':
    main()
