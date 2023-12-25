import unittest
from j2shrine.excel.excel_render import ExcelRender
from j2shrine.excel.excel_context import ExcelRenderContext
from tests.utils import file_test

class ExcelRenderTest(unittest.TestCase):

    def test_read(self):

        context = ExcelRenderContext(
            template='tests/excel/templates/simple.tmpl')
        context.read_range = 'A2:G5'
        context.header_row = '1'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/simple.txt',
                                 source='tests/excel/src/simple.xlsx')

    def test_read_all(self):
        context = ExcelRenderContext(
            template='tests/excel/templates/read_all.tmpl')
        context.read_range = 'A2:G'
        context.header_row = '1'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_all.txt',
                                 source='tests/excel/src/simple.xlsx')

    def test_multi_sheet(self):
        context = ExcelRenderContext(
            template='tests/excel/templates/read_multi_sheet.tmpl')
        context.read_range = 'A2:G'
        context.header_row = '1'
        context.sheets = '3:'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_multi_sheet.txt',
                                 source='tests/excel/src/multi.xlsx')

    def test_fixed_cells(self):
        context = ExcelRenderContext(
            template='tests/excel/templates/read_fixed_cells.tmpl')
        context.read_range = 'A4:G'
        context.header_row = '3'
        context.sheets = '3:'
        context.fixed = ['A1', 'D2']
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_fixed_cells.txt',
                                 source='tests/excel/src/read_fixed_cells.xlsx')

    def test_sheet_range(self):
        context = ExcelRenderContext(
            template='tests/excel/templates/read_multi_sheet.tmpl')
        context.read_range = 'A2:G'
        context.header_row = '1'
        context.sheets = '3:4'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_multi_sheet.txt',
                                 source='tests/excel/src/range.xlsx')

    def test_row_range(self):
        context = ExcelRenderContext(
            template='tests/excel/templates/read_multi_sheet.tmpl')
        context.read_range = 'A3:G4'
        context.header_row = '1'
        context.sheets = '3:4'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_row_range.txt',
                                 source='tests/excel/src/range.xlsx')

    def test_sheet_name(self):
        context = ExcelRenderContext(
            template='tests/excel/templates/read_sheet_name.tmpl')
        context.read_range = 'A2:G'
        context.header_row = '1'
        context.sheets = '3:'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_sheet_name.txt',
                                 source='tests/excel/src/multi.xlsx')

    def test_read_datetime(self):

        context = ExcelRenderContext(
            template='tests/excel/templates/read_datetime.tmpl')
        context.read_range = 'A2:C5'
        context.header_row = '1'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_datetime.txt',
                                 source='tests/excel/src/read_datetime.xlsx')

    def test_read_custom_datetime(self):

        context = ExcelRenderContext(
            template='tests/excel/templates/read_custom_datetime.tmpl')
        context.read_range = 'A2:C5'
        context.header_row = '1'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_custom_datetime.txt',
                                 source='tests/excel/src/read_custom_datetime.xlsx')

    def test_read_data_only(self):

        context = ExcelRenderContext(
            template='tests/excel/templates/read_data_only.tmpl')
        context.read_range = 'A2:D'
        context.header_row = '1'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_data_only.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def test_read_document(self):
        # それらしいドキュメントを読み込むテスト
        context = ExcelRenderContext(
            template='tests/excel/templates/read_document.tmpl')
        context.read_range = 'C7:H10'
        context.header_row = '6'
        context.fixed = ['C3', 'C4']
        context.sheets = '1:'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_document.txt',
                                 source='tests/excel/src/read_document.xlsx')

    def test_read_by_column_letter(self):

        context = ExcelRenderContext(
            template='tests/excel/templates/read_data_by_column_letter.tmpl')
        context.read_range = 'A2:D'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_data_only.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def test_read_by_column_letter_single(self):

        context = ExcelRenderContext(
            template='tests/excel/templates/read_data_by_column_letter_single.tmpl')
        context.read_range = 'A2:A'
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_data_only_single.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def test_column_number(self):
        context = ExcelRenderContext(
            template='tests/excel/templates/simple.tmpl')
        render = ExcelRender(context=context)
        self.assertEqual(1, render.column_number(column='A'))
        self.assertEqual(27, render.column_number(column='AA'))
        self.assertEqual(703, render.column_number(column='AAA'))

    def file_rendering_test(self, *, context, expect, source, encoding='utf8'):
        converter = ExcelRender(context=context)
        result_file = 'tests/output/' + expect.rpartition('/')[2] + '.tmp'

        with open(result_file, 'w', encoding=encoding) as result_writer:
            converter.render(source=source, output=result_writer)
            
        return file_test(ut=self, expect_file=expect, result_file=result_file)


if __name__ == '__main__':
    unittest.main()
