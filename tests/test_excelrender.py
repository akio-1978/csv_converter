import unittest
from j2shrine.excel.excel_render import ExcelRender
from j2shrine.excel.excel_context import ExcelRenderContext
from tests.utils import J2SRenderTest, RenderArgs

class ExcelRenderTest(J2SRenderTest):

    def test_read(self):
        """シート中の矩形範囲指定A2:G5"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/simple.tmpl'
        args.read_range = 'A2:G5'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/simple.txt',
                                 source='tests/excel/src/simple.xlsx')

    def test_read_all(self):
        """シート中の全行指定A2:G A2:G"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_all.tmpl'
        args.read_range = 'A2:G'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_all.txt',
                                 source='tests/excel/src/simple.xlsx')

    def test_multi_sheet(self):
        """複数シート指定 3枚目から右の全てのシート"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_multi_sheet.tmpl'
        args.read_range = 'A2:G'
        args.sheets = '3:'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_multi_sheet.txt',
                                 source='tests/excel/src/multi.xlsx')

    def test_absolute_cells(self):
        """絶対位置指定でのセル取得 A1 D2"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_absolute_cells.tmpl'
        args.read_range = 'A4:G'
        args.sheets = '3:'
        args.absolute = ['CELL_A=A1', 'CELL_B=D2']
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_absolute_cells.txt',
                                 source='tests/excel/src/read_absolute_cells.xlsx')

    def test_sheet_range(self):
        """複数シート指定 3枚目から4枚目までの2枚"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_multi_sheet.tmpl'
        args.read_range = 'A2:G'
        args.sheets = '3:4'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_multi_sheet.txt',
                                 source='tests/excel/src/range.xlsx')

    def test_row_range(self):
        """複数シート指定 かつセル矩形範囲（これいる？）"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_multi_sheet.tmpl'
        args.read_range = 'A3:G4'
        args.sheets = '3:4'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_row_range.txt',
                                 source='tests/excel/src/range.xlsx')

    def test_sheet_name(self):
        """テンプレート内からのシート名読み取り"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_sheet_name.tmpl'
        args.read_range = 'A2:G'
        args.sheets = '3:'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_sheet_name.txt',
                                 source='tests/excel/src/multi.xlsx')

    def test_read_datetime(self):
        """Excel日付型の読み取り"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_datetime.tmpl'
        args.read_range = 'A2:C5'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_datetime.txt',
                                 source='tests/excel/src/read_datetime.xlsx')

    def test_read_custom_datetime(self):
        """Excel日付型の任意フォーマット"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_custom_datetime.tmpl'
        args.read_range = 'A2:C5'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_custom_datetime.txt',
                                 source='tests/excel/src/read_custom_datetime.xlsx')

    def test_read_data_only(self):
        """関数を読み込まないことの確認"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_data_only.tmpl'
        args.read_range = 'A2:D'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_data_only.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def test_read_document(self):
        """実利用意識テスト"""
        # それらしいドキュメントを読み込むテスト
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_document.tmpl'
        args.read_range = 'C7:H10'
        args.absolute = ['NAME=C3', 'DESCRIPTION=C4']
        args.sheets = '1:'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_document.txt',
                                 source='tests/excel/src/read_document.xlsx')

    def test_read_by_row_index(self):
        """行をインデックス指定で取得する"""
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_by_row_index.tmpl'
        args.read_range = 'A2:D'
        self.excel_rendering_test(render=ExcelRender(context=ExcelRenderContext(args=args)),
                                 expect='tests/excel/expect/read_by_row_index.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def excel_rendering_test(self, *, render, expect, source, encoding='utf8'):
        result_file = 'tests/output/' + expect.rpartition('/')[2] + '.tmp'

        with open(result_file, 'w', encoding=encoding) as result_writer:
            render.render(source=source, output=result_writer)
            
        return self.file_test(expect_file=expect, result_file=result_file)


if __name__ == '__main__':
    unittest.main()
