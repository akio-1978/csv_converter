import unittest
import sys
import contextlib
from j2shrine.runner import Runner
from tests.testutils import J2SRenderTest

class RunnerTest(J2SRenderTest):

    def result_dir(self):
        """出力ディレクトリ名を返す"""
        return 'runner'

    def test_start(self):
        """最低限の引数で起動"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-H']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_jp(self):
        """日本語読み書き"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple_sjis.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple_sjis.csv', 
            '-o', result_file, '-H', '--input-encoding', 'sjis', '--output-encoding', 'sjis']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file, encoding='sjis')


    def test_start_args(self):
        """オプション引数を指定して起動"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple.csv',
            '-o', result_file, '-H', '--input-encoding', 'utf8', '--output-encoding', 'utf8',
            '-d',',', '-p' ,'A=B', 'C=D']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)


    def test_header_names(self):
        """--headerと--namesを同時に指定した場合はheaderを優先する"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-H', '--names', 'not', 'use', 'names', ]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_names(self):
        """--names指定で起動"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-s', '1', '--names', 'group', 'number', 'name']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_names_short(self):
        """-n 指定で起動"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-s', '1', '-n', 'group', 'number', 'name']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_excel(self):
        """Excel変換起動（引数が複雑）"""
        expect_file = self.expect_path(J2SRenderTest.EXCEL, 'read_document.txt')
        result_file = self.result_file()
        Runner(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
            '1:', 'C7:H10', '-o', result_file, '--absolute', 'NAME=C3', 'DESCRIPTION=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_excel_demo(self):
        """同じソースを複数回レンダリングするデモ"""
        expect_file = self.expect_path(J2SRenderTest.EXCEL, 'demo01.sql.txt')
        result_file = self.result_file('demo01')
        Runner(args=['excel', 'tests/excel/templates/read_demo01.tmpl', 'tests/excel/src/read_demo.xlsx',
            '1:', 'A6:G', '-o', result_file, '--absolute', 'TABLE=C3', 'LABEL=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

        expect_file = self.expect_path(J2SRenderTest.EXCEL, 'demo02.html.txt')
        result_file = self.result_file('demo02')
        Runner(args=['excel', 'tests/excel/templates/read_demo02.tmpl', 'tests/excel/src/read_demo.xlsx',
            '1:', 'A6:G', '-o', result_file, '--absolute', 'TABLE=C3', 'LABEL=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_stdout(self):
        """標準出力への書き出し"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple.txt')
        result_file = self.result_file()
        with open(result_file, mode='w', encoding='utf8') as file:
            with contextlib.redirect_stdout(file):
                Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple.csv', 
                    '-H']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file, delete_on_success=False)

    def test_stdout_sjis(self):
        """標準出力日本語読み書き"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple_sjis.txt')
        result_file = self.result_file()
        with open(result_file, mode='w', encoding='utf8') as file:
            with contextlib.redirect_stdout(file):
                Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple_sjis.csv', 
                    '-H', '--input-encoding', 'sjis', '--output-encoding', 'sjis']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file, encoding='sjis', delete_on_success=False)

    def test_stdin(self):
        """標準入力から読込み"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple.txt')
        result_file = self.result_file()
        tmp_stdin = sys.stdin
        try:
            with open('tests/csv/src/simple.csv', encoding='utf8') as file:
                sys.stdin = file
                Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 
                    '-o', result_file, '-H']).execute()
        finally:
            sys.stdin = tmp_stdin
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_stdin_jp(self):
        """標準入力から日本語読込み"""
        expect_file = self.expect_path(J2SRenderTest.CSV, 'simple_sjis.txt')
        result_file = self.result_file()
        tmp_stdin = sys.stdin
        try:
            with open('tests/csv/src/simple_sjis.csv', encoding='utf8') as file:
                sys.stdin = file
                Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 
                    '-o', result_file, '-H', '--input-encoding', 'sjis', '--output-encoding', 'sjis']).execute()
        finally:
            sys.stdin = tmp_stdin
        self.file_test(expect_file=expect_file, result_file=result_file, encoding='sjis')


    def test_csv_help(self):
        starter = Runner(args=['csv', '-h'])
        self.assertRaises(BaseException, starter.execute)

    def test_excel_help(self):
        starter = Runner(args=['excel', '-h'])
        self.assertRaises(BaseException, starter.execute)

    def test_json_help(self):
        starter = Runner(args=['json', '-h'])
        self.assertRaises(BaseException, starter.execute)

    def test_csv_invalid(self):
        starter = Runner(args=['csv'])
        self.assertRaises(BaseException, starter.execute)

if __name__ == '__main__':
    unittest.main()
