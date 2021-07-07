import openpyxl
from . base_render import Render, RenderContext

# transformerに渡すパラメータクラス
class ExcelRenderContext(RenderContext):
    def __init__(self, *, template=None, template_encoding='utf8', parameters={}):
        super().__init__(template=template, template_encoding=template_encoding, parameters=parameters)
        self.encoding = 'utf8'
        self.sheet_no = 0
        self.header_prefix='col_'
        self.headers = None         
        self.header_area = None     # ex."A2:M2"
        self.start_line = None      # ex."A3:M3"
        self.read_limit = None 

class ExcelRender(Render):

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
        # シート取り出し
        sheet = reader.worksheets[0]
        lines = []
        # ヘッダの読込み
        self.headers = self.read_headers(sheet=sheet)
       # コンテンツ読込み
        (left, right) = self.get_cells(sheet=sheet, cells=self.context.start_line)

        for row in sheet.iter_rows(min_col=left.column, min_row=left.row , max_col=right.column, max_row=self.context.read_limit, ):
            lines.append(self.columns_to_dict(columns = row))

        return lines

    def read_headers(self, *, sheet:openpyxl.worksheet.worksheet):
        headers = []
        if self.context.headers is not None:
            self.headers = self.context.headers
        elif self.context.header_area is not None:

            (left, right) = self.get_cells(sheet=sheet, cells=self.context.header_area)
            for row in sheet.iter_rows(min_col=left.column, min_row=left.row,
                                        max_col=right.column, max_row=right.row):
                for cell in row:
                    headers.append(cell.value)
            return headers
        else: # ヘッダは指定されていない
            return []

    def get_cells(self, *, sheet, cells):
        (left, right) = cells.split(':')
        return (sheet[left], sheet[right])

    # カラムのlistをdictに変換する。dictのキーはself.headers
    def columns_to_dict(self, *, columns):
        line = {}
        # カラムとヘッダの長さは揃っていることが前提
        for header, column in zip(self.headers, columns):
            # カラム単体の変換処理を行う
            line[header] = self.read_column(name = header, column = column)

        return line

    def columns_dict(self, *, columns_dict):
        return columns_dict

    # hook by every column
    def read_column(self, *, name, column):
        # データの取り出し
        return column.value

