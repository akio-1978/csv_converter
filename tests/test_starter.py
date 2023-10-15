import unittest
from j2shrine.starter import Starter

class StarterTest(unittest.TestCase):

    def test_start(self):
        Starter(args=['csv', 'tests/csv/templates/simple_json.tmpl', 'tests/csv/src/simple_json.csv', 
            '-o', 'tests/output/test_start.tmp', '-p' ,'A=B']).execute()

    def test_start_args(self):
        Starter(args=['csv', 'tests/csv/templates/simple_json.tmpl', 'tests/csv/src/simple_json.csv',
            '-o', 'tests/output/test_start.tmp', '-d',',', '-p' ,'A=B']).execute()
    def test_start_basic_args(self):
        Starter(args=['csv', 'tests/csv/templates/simple_json.tmpl', 'tests/csv/src/simple_json.csv',
            '-o', 'tests/output/test_start.tmp',  '--input-encoding','euc-jp', '-p' ,'A=B']).execute()

    def test_start_excel(self):
        Starter(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
            '1:', 'C7:H10', '-o', 'tests/output/test_start.tmp', '--fixed', 'C3', 'C4']).execute()

    def test_excel_help(self):
        starter = Starter(args=['excel', '-h'])
        self.assertRaises(BaseException, starter.execute)

if __name__ == '__main__':
    unittest.main()
