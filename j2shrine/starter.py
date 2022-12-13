import sys
import argparse
from .command.command import Command
from . command.csv_command import CsvCommand
from . command.excel_command import ExcelCommand
from . command.json_command import JsonCommand

class Starter():

    def __init__(self, *, args):
        self.args = args

    def set_subparsers(self, *, main_parser):
        CsvCommand().register_self(main_parser=main_parser)

        ExcelCommand().register_self(main_parser=main_parser)

        JsonCommand().register_self(main_parser=main_parser)

    def create_mainparser(self):
        base_parser = argparse.ArgumentParser(prog='j2shrine', 
                                                add_help=True,
                                                )
        return base_parser

    def execute(self):

        self.parser = self.create_mainparser()
        self.set_subparsers(main_parser=self.parser.add_subparsers(required=True))

        namespace = self.parser.parse_args(self.args)
        command = namespace.command_instance
        context = command.context(arguments = vars(namespace))
        self.assign_args(context=context, namespace=namespace)

        render = command.get_render(context=context)
        command.rendering(render=render, context=context)

    # コマンド引数からコンテキストを作る
    def assign_args(self, *, context, namespace):
        arguments = vars(namespace)
        for (key, value) in arguments.items():
            setattr(context, key, value)
        return context


def main():
    starter = Starter(args=sys.argv[1:] if len(sys.argv) > 1 else ['', ''])
    starter.execute()

if __name__ == '__main__':
    main()
