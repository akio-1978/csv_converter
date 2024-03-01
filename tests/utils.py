import unittest
import argparse
from pathlib import Path

class J2SRenderTest(unittest.TestCase):
    def rendering_test(self, *, render, expect_file, source):
        result_file = 'tests/output/' + self._testMethodName + '.tmp'
        
        with open(source, encoding='utf-8') as source_reader:
            with open(result_file, 'w') as result_writer:
                render.render(source=source_reader, output=result_writer)

        return self.file_test(expect_file=expect_file, result_file=result_file)

    def file_test(self, *, expect_file:str, result_file:str):
        with open(expect_file, encoding='utf-8') as expect_reader:
            with open(result_file, encoding='utf-8') as result_reader:
                result = result_reader.read()
                self.assertEqual(expect_reader.read(), result)

            # テストに成功したファイルは削除する            
            Path(result_file).unlink()

class RenderArgs(argparse.Namespace):
    
    def __init__(self):
        self.template_encoding = 'utf-8'
        self.parameters = {}
