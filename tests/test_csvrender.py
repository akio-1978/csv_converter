import unittest
from io import StringIO
from j2shrine.csv.csv_render import CsvRender
from j2shrine.csv.csv_context import CsvRenderContext

from jinja2 import Environment, DictLoader
from tests.utils import rendering_test, RenderArgs

class CsvRenderTest(unittest.TestCase):

    def test_convert_headless(self):
        """ヘッダのない単純なCSV"""
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
        """CSVデータのエスケープ"""
        args = RenderArgs()
        args.template = {
            'template': "{% for line in rows %}{{line.col_00}}\n{% endfor %}"}
        args.template_name = 'template'
        converter = DictRender(context=CsvRenderContext(args=args))

        source = StringIO('"A00,01",C0002\nB0001,C0002\nC0001,C0002')
        result = StringIO()

        converter.render(source=source, output=result)

        self.assertEqual('A00,01\nB0001\nC0001\n\n', result.getvalue())

    def test_header(self):
        """ヘッダ行付き"""
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
        """ヘッダ付きCSVからjsonファイル変換"""
        self.file_convert_test(template='tests/csv/templates/simple_json.tmpl',
                               expect='tests/csv/expect/simple_json.txt',
                               source='tests/csv/src/simple_json.csv')

    def test_skip_with_header(self):
        """先頭3行を読み飛ばした後にヘッダ付き"""
        self.file_convert_test(template='tests/csv/templates/simple_json.tmpl',
                               expect='tests/csv/expect/skip_with_header.txt',
                               source='tests/csv/src/skip_with_header.csv',
                               skip_lines=3, read_header=True)

    def test_skip_no_header(self):
        """先頭3行を読み飛ばした後にヘッダなし"""
        self.file_convert_test(template='tests/csv/templates/skip_no_header.tmpl',
                               expect='tests/csv/expect/skip_no_header.txt',
                               source='tests/csv/src/skip_no_header.csv',
                               skip_lines=3, read_header=False)

    def test_group_by(self):
        """テンプレート内でgroup byを行う"""
        self.file_convert_test(template='tests/csv/templates/group_by.tmpl',
                               expect='tests/csv/expect/group_by.yml',
                               source='tests/csv/src/group_by.csv')

    def test_parameters(self):
        """変換時のパラメータ渡し"""
        self.file_convert_test(template='tests/csv/templates/parameters.tmpl',
                               expect='tests/csv/expect/parameters.yml',
                               source='tests/csv/src/parameters.csv',
                               parameters={'list_name': 'Yurakucho-line-stations-in-ward'})

    def test_headers_only(self):
        """ヘッダ行だけを読み取る"""
        self.file_convert_test(template='tests/csv/templates/headers_only.tmpl',
                               expect='tests/csv/expect/headers_only.txt',
                               source='tests/csv/src/simple_json.csv')

    def test_too_many_columns(self):
        """ヘッダ行より長い行のカラム名を自動生成"""
        self.file_convert_test(template='tests/csv/templates/headers_only.tmpl',
                               expect='tests/csv/expect/too_many_columns.txt',
                               source='tests/csv/src/too_many_columns.csv')

    def test_auto_naming(self):
        """ヘッダ行を使わずにカラム名を自動生成"""
        self.file_convert_test(template='tests/csv/templates/headers_only.tmpl',
                               expect='tests/csv/expect/auto_naming.txt',
                               source='tests/csv/src/simple_json.csv',
                               read_header=False)

    def test_read_by_name(self):
        """テンプレート内でカラム名から値を読み取る"""
        self.file_convert_test(template='tests/csv/templates/read_by_name.tmpl',
                               expect='tests/csv/expect/read_by_name.txt',
                               source='tests/csv/src/read_by_name.csv',
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
