import sys
import argparse

from ..render.base_render import Render, RenderContext

# CommandRunnerのデフォルト実装
class Command():

    def add_arguments(self, subparser):
        subparser.add_argument('template', help='jinja2 template to use.')
        subparser.add_argument('source', help='rendering text.', nargs='?', default=sys.stdin)
        # output file (default stdout)
        subparser.add_argument('-o', '--out', metavar='file', help='output file.', default=sys.stdout)
        # source encoding
        subparser.add_argument('--input-encoding', metavar='enc', help='source encoding.', default='utf-8')
        # dest encoding
        subparser.add_argument('--output-encoding', metavar='enc', help='output encoding.', default='utf-8')
        subparser.add_argument('-p', '--parameters', nargs='*', help='additional values [KEY=VALUE] format.', action=KeyValuesParseAction)
        return subparser

    def context(self):
        return RenderContext()

    def render(self, *, context):
        return Render(context=context)


class KeyValuesParseAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.parse_key_values(values))

    def parse_key_values(self, values):
        key_values = {}
        for value in values:
            key_value = value.partition('=')
            key_values[key_value[0]] = key_value[2]
        return key_values
