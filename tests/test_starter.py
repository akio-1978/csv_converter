import sys
import io
import unittest
from j2render.starter import Starter

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

    # <pending> test the show help
    # def test_help(self):
    #     Starter(args=['-h']).execute()

    # def test_help_csv(self):
    #     Starter(args=['csv', '-h']).execute()

if __name__ == '__main__':
    unittest.main()