import unittest
from j2shrine.excel.excel_render import ExcelRender
from j2shrine.excel.excel_context import ExcelRenderContext
from tests.utils import file_test, RenderArgs

class ExcelRenderTest(unittest.TestCase):

    def test_read(self):
        args = RenderArgs()
        args.template = 'tests/excel/templates/simple.tmpl'
        args.read_range = 'A2:G5'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/simple.txt',
                                 source='tests/excel/src/simple.xlsx')

    def test_read_all(self):
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_all.tmpl'
        args.read_range = 'A2:G'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_all.txt',
                                 source='tests/excel/src/simple.xlsx')

    def test_multi_sheet(self):
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_multi_sheet.tmpl'
        args.read_range = 'A2:G'
        args.sheets = '3:'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_multi_sheet.txt',
                                 source='tests/excel/src/multi.xlsx')

    def test_fixed_cells(self):
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_fixed_cells.tmpl'
        args.read_range = 'A4:G'
        args.sheets = '3:'
        args.absolute = ['A1', 'D2']
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_fixed_cells.txt',
                                 source='tests/excel/src/read_fixed_cells.xlsx')

    def test_sheet_range(self):
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_multi_sheet.tmpl'
        args.read_range = 'A2:G'
        args.sheets = '3:4'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_multi_sheet.txt',
                                 source='tests/excel/src/range.xlsx')

    def test_row_range(self):
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_multi_sheet.tmpl'
        args.read_range = 'A3:G4'
        args.sheets = '3:4'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_row_range.txt',
                                 source='tests/excel/src/range.xlsx')

    def test_sheet_name(self):
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_sheet_name.tmpl'
        args.read_range = 'A2:G'
        args.sheets = '3:'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_sheet_name.txt',
                                 source='tests/excel/src/multi.xlsx')

    def test_read_datetime(self):

        args = RenderArgs()
        args.template = 'tests/excel/templates/read_datetime.tmpl'
        args.read_range = 'A2:C5'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_datetime.txt',
                                 source='tests/excel/src/read_datetime.xlsx')

    def test_read_custom_datetime(self):

        args = RenderArgs()
        args.template = 'tests/excel/templates/read_custom_datetime.tmpl'
        args.read_range = 'A2:C5'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_custom_datetime.txt',
                                 source='tests/excel/src/read_custom_datetime.xlsx')

    def test_read_data_only(self):

        args = RenderArgs()
        args.template = 'tests/excel/templates/read_data_only.tmpl'
        args.read_range = 'A2:D'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_data_only.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def test_read_document(self):
        # それらしいドキュメントを読み込むテスト
        args = RenderArgs()
        args.template = 'tests/excel/templates/read_document.tmpl'
        args.read_range = 'C7:H10'
        args.absolute = ['C3', 'C4']
        args.sheets = '1:'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_document.txt',
                                 source='tests/excel/src/read_document.xlsx')

    def test_read_by_column_letter(self):

        args = RenderArgs()
        args.template = 'tests/excel/templates/read_data_by_column_letter.tmpl'
        args.read_range = 'A2:D'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_data_only.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def test_read_by_column_letter_single(self):

        args = RenderArgs()
        args.template = 'tests/excel/templates/read_data_by_column_letter_single.tmpl'
        args.read_range = 'A2:A'
        context = ExcelRenderContext(args=args)
        self.file_rendering_test(context=context,
                                 expect='tests/excel/expect/read_data_only_single.txt',
                                 source='tests/excel/src/data_only.xlsx')

    def file_rendering_test(self, *, context, expect, source, encoding='utf8'):
        converter = context.new_render()
        result_file = 'tests/output/' + expect.rpartition('/')[2] + '.tmp'

        with open(result_file, 'w', encoding=encoding) as result_writer:
            converter.render(source=source, output=result_writer)
            
        return file_test(ut=self, expect_file=expect, result_file=result_file)


if __name__ == '__main__':
    unittest.main()
