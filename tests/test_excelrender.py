import unittest
import sys
from io import StringIO
from j2shrine.render.excel_render import ExcelRender, ExcelRenderContext


class ExcelRenderTest(unittest.TestCase):

    def test_by_name(self):

        context = ExcelRenderContext(template='tests/excel/templates/simple.tmpl')
        context.header_area ='A1:G1'
        context.start_line='A2:G2'
        rendered = StringIO()        
        render = ExcelRender(context=context)
        render.render(source='tests/excel/render_source_file/simple.xlsx', output=rendered)
        print(rendered.getvalue())

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


if __name__ == '__main__':
    unittest.main()
