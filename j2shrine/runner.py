import sys
import argparse
from .csv.csv_command import CsvCommand
from .excel.excel_command import ExcelCommand
from .json.json_command import JsonCommand


class Runner():

    def __init__(self, *, args):
        self.args = args

    def set_subparsers(self, *, main_parser):
        CsvCommand(master=main_parser).setup()
        ExcelCommand(master=main_parser).setup()
        JsonCommand(master=main_parser).setup()

    def create_mainparser(self):
        base_parser = argparse.ArgumentParser(prog='j2shrine',
                                              add_help=True,
                                              )
        return base_parser

    def execute(self):

        self.parser = self.create_mainparser()
        self.set_subparsers(
            main_parser=self.parser.add_subparsers(required=True))

        namespace = self.parser.parse_args(self.args)
        command = namespace.command_instance
        command.execute(args=namespace)


def main():
    starter = Runner(args=sys.argv[1:] if len(sys.argv) > 1 else ['', ''])
    starter.execute()


if __name__ == '__main__':
    main()
