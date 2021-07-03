import openpyxl
from openpyxl.worksheet
from . base_render import Render, RenderContext

# transformerに渡すパラメータクラス
class ExcelRenderContext(RenderContext):
    def __init__(self, *, template=None, template_encoding='utf8', parameters={}):
        super().__init__(template=template, template_encoding=template_encoding, parameters=parameters)
        self.encoding = 'utf8'
        self.sheet_no = 0
        self.header_prefix='col_'
        self.header_area = None
        self.headers = None         # Xn:Xn
        self.start_line = None      # A-Z
        self.start = '1'


class ExcelRender(Render):

    COLMUN_LABELS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # jinja2テンプレートの生成
    def __init__(self, *, context :ExcelRenderContext):
        super().__init__(context = context)
        if context.headers is not None:
            self.headers = context.headers

    def build_reader(self, *, source :any) :
        # 既にブックで渡された場合、そのまま返す
        if ( isinstance(source, openpyxl.Workbook)):
            return source
        # ファイルの場合はロードする
        return openpyxl.load_workbook(source)

    def read_source(self, *, reader):

        # ヘッダの読込み
        self.headers = self
        lines = []
        for line_no, columns in enumerate(reader):
            
            line = self.columns_to_dict(columns = columns)
            lines.append(line)

        return lines

    def read_headers(self, *, sheet:openpyxl.worksheet.workshet):
        headers = []
        if self.context.headers is not None:
            self.headers = self.context.headers
        elif self.context.header_area is not None:
            (start_col, start_row, end_col, end_row) = self.region_indice(sheet=sheet, cells=self.context.header_area)
            row = sheet.iter_rows(min_col=start_col, min_row=start_row,
                                        max_col=end_col, max_row=end_row)

            for cell in row:
                headers.append(cell.value)
            return headers
        else: # ヘッダは指定されていない
            return []

    def cell_index(self,*,  sheet, cell_name):
        cell = sheet[cell_name]
        return (cell.column, cell.row)

    def region_indice(self, *, sheet, cells:str) :
        (start_cell, end_cell) = cells.split(':')
        
        (start_col, start_row) = self.cell_index(sheet=sheet, cell_name=start_cell)
        (end_col, end_row) = self.cell_index(sheet=sheet, cell_name=end_cell)
        return (start_cell, start_row)

    # カラムのlistをdictに変換する。dictのキーはself.headers
    def columns_to_dict(self, *, columns):
        line = {}
        # カラムとヘッダの長さは揃っていることが前提
        for header, column in zip(self.headers, columns):
            # カラム単体の変換処理を行う
            line[header] = self.read_column(name = header, column = column)

        print('dict: ', line)
        return line

    def columns_dict(self, *, columns_dict):
        return columns_dict

    # hook by every column
    def read_column(self, *, name, column):
        return column.strip()

