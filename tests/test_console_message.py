import unittest
from toj2.runner import Runner
from tests.testutils import J2SRenderingTest

class ConsoleTest(J2SRenderingTest):
    """コマンドラインの不正確な引数及びヘルプ表示、このテストは例外が発生すればok"""

    def test_no_subcommand(self):
        """サブコマンドの指定がない"""
        starter = Runner(args=[])
        self.assertRaises(BaseException, starter.execute)

    def test_csv_invalid(self):
        """csv 引数指定がない"""
        starter = Runner(args=['csv'])
        self.assertRaises(BaseException, starter.execute)

    def test_excel_invalid(self):
        """excel 引数指定がない"""
        starter = Runner(args=['excel'])
        self.assertRaises(BaseException, starter.execute)

    def test_json_invalid(self):
        """json 引数指定がない"""
        starter = Runner(args=['json'])
        self.assertRaises(BaseException, starter.execute)

    def test_csv_help(self):
        """csv ヘルプ表示"""
        starter = Runner(args=['csv', '-h'])
        self.assertRaises(BaseException, starter.execute)

    def test_excel_help(self):
        """excel ヘルプ表示"""
        starter = Runner(args=['excel', '-h'])
        self.assertRaises(BaseException, starter.execute)

    def test_json_help(self):
        """json ヘルプ表示"""
        starter = Runner(args=['json', '-h'])
        self.assertRaises(BaseException, starter.execute)

if __name__ == '__main__':
    unittest.main()
