import unittest
from j2shrine.starter import Starter
from utils import J2SRenderTest

class StarterTest(J2SRenderTest):

    def test_start(self):
        """最低限の引数で起動"""
        expect = 'tests/csv/expect/simple_json.txt'
        result = 'tests/output/starter.start.tmp'
        Starter(args=['csv', 'tests/csv/templates/simple_json.tmpl', 'tests/csv/src/simple_json.csv', 
            '-o', result, '-H']).execute()
        self.file_test(expect_file=expect, result_file=result)

    def test_start_args(self):
        """オプション引数を指定して起動"""
        expect = 'tests/csv/expect/simple_json.txt'
        result = 'tests/output/starter.args.tmp'
        Starter(args=['csv', 'tests/csv/templates/simple_json.tmpl', 'tests/csv/src/simple_json.csv',
            '-o', result, '-H', '--input-encoding', 'utf8', '--output-encoding', 'utf8',
            '-d',',', '-p' ,'A=B', 'C=D']).execute()
        self.file_test(expect_file=expect, result_file=result)

    def test_start_excel(self):
        """Excel変換起動（引数が複雑）"""
        expect = 'tests/excel/expect/read_document.txt'
        result = 'tests/output/starter.read_document.tmp'
        Starter(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
            '1:', 'C7:H10', '-o', result, '--absolute', 'C3', 'C4']).execute()
        self.file_test(expect_file=expect, result_file=result)

    def test_excel_demo(self):
        """同じソースを複数回レンダリングするデモ"""
        expect = 'tests/excel/expect/demo01.sql.txt'
        result = 'tests/output/starter.demo01.tmp'
        Starter(args=['excel', 'tests/excel/templates/read_demo01.tmpl', 'tests/excel/src/read_demo.xlsx',
            '1:', 'A6:G', '-o', result, '--absolute', 'C3', 'C4']).execute()
        self.file_test(expect_file=expect, result_file=result)

        expect = 'tests/excel/expect/demo02.html.txt'
        result = 'tests/output/starter.demo02.tmp'
        Starter(args=['excel', 'tests/excel/templates/read_demo02.tmpl', 'tests/excel/src/read_demo.xlsx',
            '1:', 'A6:G', '-o', result, '--absolute', 'C3', 'C4']).execute()
        self.file_test(expect_file=expect, result_file=result)

    def test_excel_help(self):
        starter = Starter(args=['excel', '-h'])
        self.assertRaises(BaseException, starter.execute)

if __name__ == '__main__':
    unittest.main()
