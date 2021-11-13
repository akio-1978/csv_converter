import unittest
import openpyxl
from io import StringIO
from j2shrine.render.excel_render import ExcelRender, ExcelRenderContext


class ExcelRenderTest(unittest.TestCase):

    def test_read(self):

        context = ExcelRenderContext(template='tests/excel/templates/simple.tmpl')
        context.read_range = 'A2:G5'
        context.header_row ='1'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/simple.txt',
                source = 'tests/excel/render_source_file/simple.xlsx')

    def test_read_all(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_all.tmpl')
        context.read_range = 'A2:G'
        context.header_row ='1'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_all.txt',
                source = 'tests/excel/render_source_file/simple.xlsx')

    def test_multi_sheet(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_multi_sheet.tmpl')
        context.read_range = 'A2:G'
        context.header_row ='1'
        context.sheets = '3:'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_multi_sheet.txt',
                source = 'tests/excel/render_source_file/multi.xlsx')

    def test_extra_cells(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_extra_cells.tmpl')
        context.read_range = 'A4:G'
        context.header_row ='3'
        context.sheets = '3:'
        context.extra = ['A1', 'D2']
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_extra_cells.txt',
                source = 'tests/excel/render_source_file/read_extra_cells.xlsx')

    def test_sheet_range(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_multi_sheet.tmpl')
        context.read_range = 'A2:G'
        context.header_row ='1'
        context.sheets = '3:4'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_multi_sheet.txt',
                source = 'tests/excel/render_source_file/range.xlsx')

    def test_row_range(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_multi_sheet.tmpl')
        context.read_range = 'A3:G4'
        context.header_row ='1'
        context.sheets = '3:4'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_row_range.txt',
                source = 'tests/excel/render_source_file/range.xlsx')


    def test_sheet_name(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_sheet_name.tmpl')
        context.read_range = 'A2:G'
        context.header_row ='1'
        context.sheets = '3:'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_sheet_name.txt',
                source = 'tests/excel/render_source_file/multi.xlsx')

    def test_read_datetime(self):

        context = ExcelRenderContext(template='tests/excel/templates/read_datetime.tmpl')
        context.read_range = 'A2:C5'
        context.header_row ='1'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_datetime.txt',
                source = 'tests/excel/render_source_file/read_datetime.xlsx')

    def test_read_custom_datetime(self):

        context = ExcelRenderContext(template='tests/excel/templates/read_custom_datetime.tmpl')
        context.read_range = 'A2:C5'
        context.header_row ='1'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_custom_datetime.txt',
                source = 'tests/excel/render_source_file/read_custom_datetime.xlsx')

    def test_read_data_only(self):

        context = ExcelRenderContext(template='tests/excel/templates/read_data_only.tmpl')
        context.read_range = 'A2:D'
        context.header_row ='1'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_data_only.txt',
                source = 'tests/excel/render_source_file/data_only.xlsx')

    def test_read_document(self):
        # それらしいドキュメントを読み込むテスト
        context = ExcelRenderContext(template='tests/excel/templates/read_document.tmpl')
        context.read_range = 'C7:H10'
        context.header_row ='6'
        context.extra = ['C3', 'C4']
        context.sheets = '1:'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_document.txt',
                source = 'tests/excel/render_source_file/read_document.xlsx')


    def test_column_number(self):
        context = ExcelRenderContext(template='tests/excel/templates/simple.tmpl')
        render = ExcelRender(context=context)
        self.assertEqual(1, render.column_number(column='A'))
        self.assertEqual(27, render.column_number(column='AA'))
        self.assertEqual(703, render.column_number(column='AAA'))

    # def test_read_limit(self):
    #     context = ExcelRenderContext(template='tests/excel/templates/read_limit.tmpl')
    #     context.header_area ='B2:F2'
    #     context.start_line='B3:F3'
    #     render = ExcelRender(context=context)
    #     render.render(source='tests/excel/render_source_file/simple.xlsx', output=sys.stdout)
    #     rendered = StringIO()

    def file_rendering_test(self, *, context, expect, source, encoding='utf8'):
        converter = ExcelRender(context = context)
        rendered = StringIO()

        converter.render(source=source, output=rendered)
        # print(rendered.getvalue())
        with open(expect, encoding=encoding) as expect_reader:
            self.assertEqual(expect_reader.read(), rendered.getvalue())
        
        return rendered


if __name__ == '__main__':
    unittest.main()
