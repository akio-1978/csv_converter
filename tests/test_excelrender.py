import unittest
import openpyxl
from io import StringIO
from j2shrine.render.excel_render import ExcelRender, ExcelRenderContext


class ExcelRenderTest(unittest.TestCase):

    def test_read(self):

        context = ExcelRenderContext(template='tests/excel/templates/simple.tmpl')
        context.columns = 'A-G'
        context.rows = '2-5'
        context.header_row ='1'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/simple.txt',
                source = 'tests/excel/render_source_file/simple.xlsx')

    def test_read_all(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_all.tmpl')
        context.columns = 'A-'
        context.rows = '2-'
        context.header_row ='1'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_all.txt',
                source = 'tests/excel/render_source_file/simple.xlsx')

    def test_multi_sheet(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_multi_sheet.tmpl')
        context.columns = 'A-'
        context.rows = '2-'
        context.header_row ='1'
        context.sheets = '2-'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_multi_sheet.txt',
                source = 'tests/excel/render_source_file/multi.xlsx')

    def test_sheet_range(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_multi_sheet.tmpl')
        context.columns = 'A-'
        context.rows = '2-'
        context.header_row ='1'
        context.sheets = '2-3'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_multi_sheet.txt',
                source = 'tests/excel/render_source_file/range.xlsx')

    def test_row_range(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_multi_sheet.tmpl')
        context.columns = 'A-'
        context.rows = '3-4'
        context.header_row ='1'
        context.sheets = '2-3'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_row_range.txt',
                source = 'tests/excel/render_source_file/range.xlsx')


    def test_sheet_name(self):
        context = ExcelRenderContext(template='tests/excel/templates/read_sheet_name.tmpl')
        context.columns = 'A-'
        context.rows = '2-'
        context.header_row ='1'
        context.sheets = '2-'
        self.file_rendering_test(context=context,
                expect = 'tests/excel/rendered_file/read_sheet_name.txt',
                source = 'tests/excel/render_source_file/multi.xlsx')


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

    def file_rendering_test(self, *, context, expect, source):
        converter = ExcelRender(context = context)
        rendered = StringIO()

        # with openpyxl.load_workbook(source) as source_reader:
        #     converter.render(source=source_reader, output=rendered)
        converter.render(source=source, output=rendered)
        print(rendered.getvalue())
        with open(expect) as expect_reader:
            self.assertEqual(expect_reader.read(), rendered.getvalue())
        
        return rendered


if __name__ == '__main__':
    unittest.main()
