import unittest
from j2shrine.context import AppContext
from j2shrine.csv.csv_loader import CsvLoader
from j2shrine.processors import Jinja2Processor
from jinja2 import Environment, DictLoader
from tests.testutils import J2SRenderingTest

class CsvTest(J2SRenderingTest):

    def result_dir(self):
        """出力ディレクトリ名を返す"""
        return 'csv'

    def test_convert_headless(self):
        """ヘッダのない単純なCSV"""
        self.file_convert_test(template='tests/csv/templates/convert_headless.tmpl',
                               expect='tests/csv/expect/convert_headless.txt',
                               source='tests/csv/src/convert_headless.csv',
                               read_header=False)

    def test_convert_escaped(self):
        """CSVデータのエスケープ"""
        self.file_convert_test(template='tests/csv/templates/convert_escaped.tmpl',
                               expect='tests/csv/expect/convert_escaped.txt',
                               source='tests/csv/src/convert_escaped.csv',
                               read_header=False)

    def test_simple(self):
        """ヘッダ付きCSVからjsonファイル変換"""
        self.file_convert_test(template='tests/csv/templates/simple.tmpl',
                               expect='tests/csv/expect/simple.txt',
                               source='tests/csv/src/simple.csv')

    def test_skip_with_header(self):
        """先頭3行を読み飛ばした後にヘッダ付き"""
        self.file_convert_test(template='tests/csv/templates/simple.tmpl',
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
        self.file_convert_test(template='tests/csv/templates/write_headers_only.tmpl',
                               expect='tests/csv/expect/headers_only.txt',
                               source='tests/csv/src/simple.csv')

    def test_auto_naming(self):
        """ヘッダ行とは関係なくカラム名を自動生成する"""
        self.file_convert_test(template='tests/csv/templates/write_headers_only.tmpl',
                               expect='tests/csv/expect/auto_naming.txt',
                               source='tests/csv/src/simple.csv',
                               read_header=False)

    def test_name_by_header(self):
        """テンプレート内でカラム名から値を読み取る"""
        self.file_convert_test(template='tests/csv/templates/use_column_names.tmpl',
                               expect='tests/csv/expect/simple.txt',
                               source='tests/csv/src/simple.csv',
                               read_header=True)

    def test_name_by_context(self):
        """カラム名をcontext.namesで指定する"""
        self.file_convert_test(template='tests/csv/templates/use_column_names.tmpl',
                               expect='tests/csv/expect/simple.txt',
                               source='tests/csv/src/simple.csv',
                               read_header=False,
                               skip_lines=1,
                               names=['group', 'number', 'name'],
                               )

    def test_over_columns_use_header(self):
        """ヘッダ行のカラム数を超過する行には、カラム名を自動生成する
            ex:
            headers: group, number, name
            columns: group, number, name, col03, col04
        """
        self.file_convert_test(template='tests/csv/templates/use_column_names.tmpl',
                               expect='tests/csv/expect/over_columns.txt',
                               source='tests/csv/src/over_columns.csv',
                               read_header=True)

    def test_over_columns_use_context(self):
        """context.namesのカラム数を超過する行には、カラム名を自動生成する"""
        self.file_convert_test(template='tests/csv/templates/use_column_names.tmpl',
                               expect='tests/csv/expect/over_columns.txt',
                               source='tests/csv/src/over_columns.csv',
                               read_header=False,
                               skip_lines=1,
                               names=['group', 'number', 'name'],
                                )

    def test_header_ignore_context(self):
        """ヘッダ行の使用とnamesが両方指定されている場合、ヘッダが優先される"""
        self.file_convert_test(template='tests/csv/templates/use_column_names.tmpl',
                               expect='tests/csv/expect/over_columns.txt',
                               source='tests/csv/src/over_columns.csv',
                               names=['invalid', 'names', 'specified'],
                               read_header=True)


    def test_include_template(self):
        """テンプレート内でincludeが正常に行えるか"""
        self.file_convert_test(template='tests/csv/templates/include_file.tmpl',
                               expect='tests/csv/expect/simple.txt',
                               source='tests/csv/src/simple.csv')


    def file_convert_test(self, *, template, expect, source,
                          parameters={}, skip_lines=0, read_header=True, headers=None, names=[]):
        
        context = self.default_context()
        context.template = template
        # headerの使用有無
        context.read_header = read_header
        context.headers = headers
        # 追加パラメータ
        context.parameters = parameters
        # 行の読み飛ばし
        context.skip_lines = skip_lines
        # カラム名指定
        context.names = names
        # ソース指定
        context.source = source
        # 出力先指定
        context.out = self.result_file()
        
        processor = Jinja2Processor(context=context)
        loader = CsvLoader(context=context, processor=processor)
        
        return self.processor_test(loader=loader, expect_file=expect)

    def default_context(self):
        ctx = AppContext()
        ctx.names = None
        ctx.delimiter = ','
        ctx.skip_lines = 0
        ctx.read_header = False
        ctx.parameters = {}
        ctx.template_encoding = 'utf8'
        ctx.input_encoding = 'utf8'
        ctx.output_encoding = 'utf8'
        ctx.col_prefix = 'col_'
        
        return ctx

# テスト用にDictLoaderを使うRender
class DictRender (CsvLoader):

    def setup_template(self, *, context):
        self.headers = None
        environment = Environment(loader=DictLoader(context.template))
        self.template = environment.get_template(context.template_name)


if __name__ == '__main__':
    unittest.main()
