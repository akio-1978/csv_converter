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
class ConfigTest(J2SRenderTest):

    def test_names(self):
        """--names指定で起動"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Starter(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-s', '1', '--config-file', 'tests/csv/config/names.config.json']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_merge_parameter(self):
        """-n 指定で起動"""
        expect_file = expect_path(CSV, 'merge_parameters.yml')
        result_file = self.result_file()
        Starter(args=['csv', 'tests/csv/templates/merge_parameters.tmpl', 'tests/csv/src/parameters.csv', 
            '-o', result_file, '-H',
            '--parameters', 'list_name=Yurakucho-line-stations-in-ward', '--config-file', 'tests/csv/config/parameters.config.json', ]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)


    def result_dir(self):
        return 'config'

if __name__ == '__main__':
    unittest.main()
