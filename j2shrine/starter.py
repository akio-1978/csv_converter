import sys
import argparse
from . command.base_command import Command
from . command.csv_command import CsvCommand
from . render.base_render import RenderContext
from . render.csv_render import CsvRenderContext
from . command.excel_command import ExcelCommand

class Starter():

    def __init__(self, *, args):
        self.args = args

    def set_subparsers(self, *, main_parser):
        CsvCommand().register_self(main_parser=main_parser)
        # csv_parser = parser_creator.add_parser('csv', help = 'rendaring csv format')
        # csv_command.add_arguments(subparser=csv_parser)
        # csv_parser.set_defaults(command_instance = csv_command)

        ExcelCommand().register_self(main_parser=main_parser)
        # excel_parser = parser_creator.add_parser('excel', help = 'rendaring excel file', formatter_class=argparse.RawTextHelpFormatter)
        # excel_command.add_arguments(subparser=excel_parser)
        # excel_parser.set_defaults(command_instance = excel_command)

        Command().register_self(main_parser=main_parser)
        # nop_parser = parser_creator.add_parser('nop', help = 'NOP for test')
        # nop_command.add_arguments(subparser=nop_parser)
        # nop_parser.set_defaults(command_instance = nop_command)

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
        context = command.context()
        self.assign_args(context=context, namespace=namespace)
        render = command.render(context=context)

        command.render_io(render=render, context=context)

    # def render_io(self, *, render, context):
    #     in_stream = sys.stdin
    #     out_stream = sys.stdout
    #     try:
    #         if context.source is not sys.stdin:
    #             in_stream = open(context.source, encoding=context.input_encoding)
    #         if context.out is not sys.stdout:
    #             out_stream = open(context.out, encoding=context.output_encoding)

    #         render.render(source = in_stream, output = out_stream)
    #     finally:
    #         if context.source is not sys.stdin:
    #             in_stream.close()
    #         if context.out is not sys.stdout:
    #             out_stream.close()

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
