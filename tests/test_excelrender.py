import unittest
import sys
from io import StringIO
from j2shrine.render.excel_render import ExcelRender, ExcelRenderContext


class ExcelRenderTest(unittest.TestCase):

    def test_by_name(self):

        context = ExcelRenderContext(template='tests/excel/templates/simple.tmpl')
        context.header_area ='A1:G1'
        context.start_line='A2:G2'
        render = ExcelRender(context=context)
        render.render(source='tests/excel/render_source_file/simple.xlsx', output=sys.stdout)

    # openしたファイルを渡すとエラーが起きる
    # def test_by_object(self):

    #     context = ExcelRenderContext(template='tests/excel/templates/simple.tmpl')
    #     context.header_area ='A1:J1'
    #     context.start_line='A2:J2'
    #     render = ExcelRender(context=context)
    #     render.render(source=open('tests/excel/render_source_file/simple.xlsx'), output=sys.stdout)

if __name__ == '__main__':
    unittest.main()
