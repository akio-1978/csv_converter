import unittest
from j2shrine.context import RenderContext
from j2shrine.excel.excel_render import ExcelRender, CellPosition

from tests.testutils import J2SRenderTest

class ExcelRenderTest(J2SRenderTest):

    def result_dir(self):
        """出力ディレクトリ名を返す"""
        return 'excel'

    def test_read(self):
        """シート中の矩形範囲指定A2:G5"""
        context = self.default_context()
        context.template = 'tests/excel/templates/simple.tmpl'
        # context.read_range = 'A2:G5'
        context.read_range = (CellPosition('A', '2'), CellPosition('G', '5')) # A2:G5
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/simple.txt',
                                 source='tests/excel/src/simple.xlsx')

    def test_read_all(self):
        """シート中の全行指定A2:G A2:G"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_all.tmpl'
        context.read_range = 'A2:G'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_all.txt',
                                 source='tests/excel/src/simple.xlsx')

    def test_multi_sheet(self):
        """複数シート指定 3枚目から右の全てのシート"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_multi_sheet.tmpl'
        context.read_range = 'A2:G'
        context.sheets = '3:'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_multi_sheet.txt',
                                 source='tests/excel/src/multi.xlsx')

    def test_absolute_cells(self):
        """絶対位置指定でのセル取得 A1 D2"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_absolute_cells.tmpl'
        context.read_range = 'A4:G'
        context.sheets = '3:'
        context.absolute = {'CELL_A': 'A1', 'CELL_B' : 'D2'}
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_absolute_cells.txt',
                                 source='tests/excel/src/read_absolute_cells.xlsx')

    def test_sheet_range(self):
        """複数シート指定 3枚目から4枚目までの2枚"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_multi_sheet.tmpl'
        context.read_range = 'A2:G'
        context.sheets = '3:4'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_multi_sheet.txt',
                                 source='tests/excel/src/range.xlsx')

    def test_row_range(self):
        """複数シート指定 かつセル矩形範囲（これいる？）"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_multi_sheet.tmpl'
        context.read_range = 'A3:G4'
        context.sheets = '3:4'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_row_range.txt',
                                 source='tests/excel/src/range.xlsx')

    def test_sheet_name(self):
        """テンプレート内からのシート名読み取り"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_sheet_name.tmpl'
        context.read_range = 'A2:G'
        context.sheets = '3:'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_sheet_name.txt',
                                 source='tests/excel/src/multi.xlsx')

    def test_read_datetime(self):
        """Excel日付型の読み取り"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_datetime.tmpl'
        context.read_range = 'A2:C5'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_datetime.txt',
                                 source='tests/excel/src/read_datetime.xlsx')

    def test_read_custom_datetime(self):
        """Excel日付型の任意フォーマット"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_custom_datetime.tmpl'
        context.read_range = 'A2:C5'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_custom_datetime.txt',
                                 source='tests/excel/src/read_custom_datetime.xlsx')

    def test_read_data_only(self):
        """関数を読み込まないことの確認"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_data_only.tmpl'
        context.read_range = 'A2:D'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_data_only.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def test_read_document(self):
        """実利用意識テスト"""
        # それらしいドキュメントを読み込むテスト
        context = self.default_context()
        context.template = 'tests/excel/templates/read_document.tmpl'
        context.read_range = 'C7:H10'
        context.absolute = {'NAME':'C3', 'DESCRIPTION':'C4'}
        context.sheets = '1:'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_document.txt',
                                 source='tests/excel/src/read_document.xlsx')

    def test_read_by_row_index(self):
        """行をインデックス指定で取得する"""
        context = self.default_context()
        context.template = 'tests/excel/templates/read_by_row_index.tmpl'
        context.read_range = 'A2:D'
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_by_row_index.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def test_cell_by_name(self):
        """セルに名前を付けてテンプレートを適用する"""
        context = self.default_context()
        context.template = 'tests/excel/templates/cell_by_name.tmpl'
        # 読み取り開始列がcol_00になる、この場合C列がcol_00
        context.read_range = 'C7:H10'
        context.absolute = {'NAME':'C3', 'DESCRIPTION':'C4'}
        context.sheets = '1:'
        # 使用しない列は空白にする
        context.names = ['date', 'event', '', '', '', 'price']
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_document.txt',
                                 source='tests/excel/src/read_document.xlsx')

    def test_over_cell_by_name(self):
        """指定した名前よりセルが多い場合"""
        context = self.default_context()
        context.template = 'tests/excel/templates/over_cell_by_name.tmpl'
        # 読み取り開始列がcol_00になる、この場合C列がcol_00
        context.read_range = 'C7:H10'
        context.absolute = {'NAME':'C3', 'DESCRIPTION':'C4'}
        context.sheets = '1:'
        # 途中までしかカラム名を指定しない
        context.names = ['date', 'event', '',]
        self.excel_rendering_test(render=ExcelRender(context=context),
                                 expect='tests/excel/expect/read_document.txt',
                                 source='tests/excel/src/read_document.xlsx')


    def excel_rendering_test(self, *, render, expect, source, encoding='utf8'):
        result_file = self.result_file()

        with open(result_file, 'w', encoding=encoding) as result_writer:
            render.render(source=source, output=result_writer)
        self.file_test(expect_file=expect, result_file=result_file)

    def default_context(self):
        """テスト用コンテキストのデフォルト値"""
        ctx = RenderContext()
        ctx.names = None
        ctx.parameters = {}
        ctx.ansolute = {}
        ctx.template_encoding = 'utf8'
        ctx.input_encoding = 'utf8'
        ctx.output_encoding = 'utf8'
        
        return ctx


if __name__ == '__main__':
    unittest.main()
