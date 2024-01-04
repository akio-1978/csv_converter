import unittest
from io import StringIO
from j2shrine.csv.csv_render import CsvRender
from j2shrine.csv.csv_context import CsvRenderContext

from jinja2 import Environment, DictLoader
from tests.utils import rendering_test, RenderArgs

class CsvRenderTest(unittest.TestCase):

    def test_convert_headless(self):

        args = RenderArgs()
        args.template = {
            'template': "{% for line in rows %}{{line.col_00}}\n{% endfor %}"}
        args.template_name = 'template'

        context = CsvRenderContext(args=args)
        converter = DictRender(context=context)

        source = StringIO('A0001,C0002\nB0001,C0002\nC0001,C0002')
        result = StringIO()

        converter.render(source=source, output=result)

        self.assertEqual('A0001\nB0001\nC0001\n\n', result.getvalue())

    def test_convert_escaped(self):

        args = RenderArgs()
        args.template = {
            'template': "{% for line in rows %}{{line.col_00}}\n{% endfor %}"}
        args.template_name = 'template'
        converter = DictRender(context=CsvRenderContext(args=args))

        source = StringIO('"A00,01",C0002\nB0001,C0002\nC0001,C0002')
        result = StringIO()

        converter.render(source=source, output=result)

        self.assertEqual('A00,01\nB0001\nC0001\n\n', result.getvalue())

    def test_convert_headered(self):

        args = RenderArgs()
        args.template ={'template': "{% for line in rows %}{{line.FIRST}}<=>{{line.SECOND}}{% endfor %}"}
        args.template_name = 'template'
        args.read_header = True
        converter = DictRender(context=CsvRenderContext(args=args))

        source = StringIO('FIRST,SECOND\nC0001,C0002')
        result = StringIO()

        converter.render(source=source, output=result)

        self.assertEqual('C0001<=>C0002\n', result.getvalue())

    def test_simple_json(self):
        self.file_convert_test(template='tests/csv/templates/simple_json.tmpl',
                               expect='tests/csv/expect/simple_json.txt',
                               source='tests/csv/src/simple_json.csv')

    def test_skip_with_header(self):
        self.file_convert_test(template='tests/csv/templates/simple_json.tmpl',
                               expect='tests/csv/expect/simple_json.txt',
                               source='tests/csv/src/skip_with_header.csv',
                               skip_lines=3, read_header=True)

    def test_skip_with_headerless(self):
        self.file_convert_test(template='tests/csv/templates/skip_with_headerless.tmpl',
                               expect='tests/csv/expect/simple_json.txt',
                               source='tests/csv/src/skip_with_headerless.csv',
                               skip_lines=3, read_header=False)

    def test_group_by(self):
        self.file_convert_test(template='tests/csv/templates/group_by.tmpl',
                               expect='tests/csv/expect/group_by.yml',
                               source='tests/csv/src/group_by.csv')

    def test_parameters(self):
        self.file_convert_test(template='tests/csv/templates/parameters.tmpl',
                               expect='tests/csv/expect/parameters.yml',
                               source='tests/csv/src/parameters.csv',
                               parameters={'list_name': 'Yurakucho-line-stations-in-ward'})

    def test_headers(self):
        self.file_convert_test(template='tests/csv/templates/headers.tmpl',
                               expect='tests/csv/expect/headers.txt',
                               source='tests/csv/src/simple_json.csv')

    def test_headers_over(self):
        self.file_convert_test(template='tests/csv/templates/headers.tmpl',
                               expect='tests/csv/expect/headers_over.txt',
                               source='tests/csv/src/header_over.csv')

    def test_headers_auto(self):
        self.file_convert_test(template='tests/csv/templates/headers.tmpl',
                               expect='tests/csv/expect/headers_auto.txt',
                               source='tests/csv/src/simple_json.csv',
                               read_header=False)

    def test_header_names(self):
        self.file_convert_test(template='tests/csv/templates/header_names.tmpl',
                               expect='tests/csv/expect/header_names.txt',
                               source='tests/csv/src/header_names.csv',
                               read_header=True)

    def file_convert_test(self, *, template, expect, source,
                          parameters={}, skip_lines=0, read_header=True, headers=None):
        
        args = RenderArgs()
        args.template = template
        # headerの使用有無
        args.read_header = read_header
        args.headers = headers
        # 追加パラメータ
        args.parameters = parameters
        # 行の読み飛ばし
        args.skip_lines = skip_lines
        
        context = CsvRenderContext(args=args)

        return rendering_test(ut=self, render=CsvRender(context=context), expect_file=expect, source=source)

# テスト用にDictLoaderを使うRender


class DictRender (CsvRender):

    def build_convert_engine(self, *, context):
        self.headers = None
        environment = Environment(loader=DictLoader(context.template))
        self.template = environment.get_template(context.template_name)


if __name__ == '__main__':
    unittest.main()
