import unittest
import argparse
from pathlib import Path

class J2SRenderTest(unittest.TestCase):
    """テストのベースクラス ファイル変換の検証に関するユーティリティを持つ """
    def rendering_test(self, *, render, expect_file, source, delete_on_success=True):
        """renderのレンダリングを行ってファイル比較を行う"""
        result_file = self.result_file()
        
        with open(source, encoding='utf-8') as source_reader:
            with open(result_file, 'w') as result_writer:
                render.render(source=source_reader, output=result_writer)

        return self.file_test(expect_file=expect_file, result_file=result_file, delete_on_success=delete_on_success)

    def file_test(self, *, expect_file:str, result_file:str, encoding:str='utf-8', delete_on_success=True):
        """ファイル比較のみを行う
            テストに成功したファイルはexpect_fileと内容が同じなので削除し、失敗したファイルだけ残す
        """
        with open(expect_file, encoding=encoding) as expect_reader:
            with open(result_file, encoding=encoding) as result_reader:
                result = result_reader.read()
                self.assertEqual(expect_reader.read(), result)

            # テストに成功したファイルは削除する
            if delete_on_success:
                Path(result_file).unlink()

    def result_file(self, name=None):
        """変換結果ファイルのファイル名を組み立てる"""
        if name is None:
            name = self._testMethodName
        return f'tests/output/{self.result_dir()}/{name}.tmp'

    def result_dir(self):
        """変換結果の出力ディレクトリ 各テストクラスでオーバーライド必須"""
        return None

    # Runnerからコマンドライン引数を与えてテストするクラスのためのパス生成
    CSV = 'csv'
    EXCEL = 'excel'
    def expect_path(self, type, file):
        """比較元ファイル"""
        return f'tests/{type}/expect/{file}'

class RenderArgs(argparse.Namespace):
    
    def __init__(self):
        self.template_encoding = 'utf-8'
        self.parameters = {}

