import unittest
from j2shrine.starter import Starter
from utils import J2SRenderTest

# テスト用のファイルパスが長たらしいのでヘルパー
CSV = 'csv'
EXCEL = 'excel'
EXPECT = 'tests/{}/expect/{}'
RESULT = 'tests/output/{}/{}'
def expect_path(type, file):
    return EXPECT.format(type, file)
def result_path(type, file):
    return RESULT.format(type, file)
class StarterTest(J2SRenderTest):

    def test_start(self):
        """最低限の引数で起動"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = result_path('starter', 'start.tmp')
        Starter(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-H']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_args(self):
        """オプション引数を指定して起動"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = result_path('starter', 'args.tmp')
        Starter(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple.csv',
            '-o', result_file, '-H', '--input-encoding', 'utf8', '--output-encoding', 'utf8',
            '-d',',', '-p' ,'A=B', 'C=D']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_names(self):
        """names指定で起動"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = result_path('starter', 'names.tmp')
        Starter(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-s', '1', '-n', 'group', 'number', 'name']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_excel(self):
        """Excel変換起動（引数が複雑）"""
        expect_file = 'tests/excel/expect/read_document.txt'
        result = 'tests/output/starter.read_document.tmp'
        Starter(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
            '1:', 'C7:H10', '-o', result, '--absolute', 'NAME=C3', 'DESCRIPTION=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result)

    def test_excel_demo(self):
        """同じソースを複数回レンダリングするデモ"""
        expect_file = 'tests/excel/expect/demo01.sql.txt'
        result_file = 'tests/output/starter.demo01.tmp'
        Starter(args=['excel', 'tests/excel/templates/read_demo01.tmpl', 'tests/excel/src/read_demo.xlsx',
            '1:', 'A6:G', '-o', result_file, '--absolute', 'TABLE=C3', 'LABEL=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

        expect_file = 'tests/excel/expect/demo02.html.txt'
        result_file = 'tests/output/starter.demo02.tmp'
        Starter(args=['excel', 'tests/excel/templates/read_demo02.tmpl', 'tests/excel/src/read_demo.xlsx',
            '1:', 'A6:G', '-o', result_file, '--absolute', 'TABLE=C3', 'LABEL=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_excel_help(self):
        starter = Starter(args=['excel', '-h'])
        self.assertRaises(BaseException, starter.execute)

if __name__ == '__main__':
    unittest.main()
