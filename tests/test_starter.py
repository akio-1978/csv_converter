import sys
import io
import unittest
from j2shrine.starter import Starter

class StarterTest(unittest.TestCase):

    def test_start(self):
        sys.stdout = io.StringIO()
        Starter(args=['csv', 'tests/csv/templates/simple_json.tmpl', 'tests/csv/render_source_file/simple_json.csv', '-p' ,'A=B']).execute()

    def test_start_args(self):
        sys.stdout = io.StringIO()
        Starter(args=['csv', 'tests/csv/templates/simple_json.tmpl', 'tests/csv/render_source_file/simple_json.csv',
             '-d',',', '-p' ,'A=B']).execute()
    def test_start_basic_args(self):
        sys.stdout = io.StringIO()
        Starter(args=['csv', 'tests/csv/templates/simple_json.tmpl', 'tests/csv/render_source_file/simple_json.csv',
             '--input-encoding','euc-jp', '-p' ,'A=B']).execute()

    def test_excel_help(self):
        starter = Starter(args=['excel', '-h'])
        self.assertRaises(BaseException, starter.execute)
        # self.assertRaises(Starter(args=['excel', '-h']).execute())
        # Starter(args=['excel', '-h']).execute()


    # def test_raise(self):
    #     sys.stdout = io.StringIO()
    #     self.assertRaises(Starter(args=['csv', '-h']).execute())
        # try:
        #     Starter(args=['excel', '-h']).execute()
        #     # self.fail('no error occured.')
        #     print('pass')
        # except BaseException as e:
        #     print('catch')
        #     print(e)

    # <pending> test the show help
    # def test_help(self):
    #     Starter(args=['-h']).execute()

    # def test_help_csv(self):
    #     Starter(args=['csv', '-h']).execute()

if __name__ == '__main__':
    unittest.main()
