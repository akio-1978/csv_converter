import openpyxl
from . base_render import Render, RenderContext

# 取得するシート a-b
# 取得するカラムのレンジ A-Z
# 取得する行 n
# option
# ヘッダ行
# ヘッダ直接指定
# 追加取得セル...
class ExcelRenderContext(RenderContext):
    def __init__(self, *, template=None, template_encoding='utf8', parameters={}):
        super().__init__(template=template, template_encoding=template_encoding, parameters=parameters)
        self.encoding = 'utf8'
        self.sheets = None
        self.header_prefix='col_'
        self.headers = None         
        self.header_row = None     # ex."A2:M2"
        self.start_row = None      # ex."A3:M3"
        self.columns = None
        self.limit = None
        self.extra_cells =[]

class ExcelRender(Render):

    ALPHABET_TABLE = '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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
        (start, end) = self.column_range(self.context.columns)

        for row in sheet.iter_rows(min_col=start, min_row=self.context.start_row , max_col=end, max_row=self.context.limit, ):
            lines.append(self.columns_to_dict(columns = row))

        return lines

    def read_headers(self, *, sheet:openpyxl.worksheet.worksheet):
        headers = []
        if self.context.headers is not None:
            headers = self.context.headers
        elif self.context.header_area is not None:

            (start, end) = self.column_range(self.context.columns)
            for row in sheet.iter_rows(min_col=start, min_row=self.context.header_row,
                                        max_col=end, max_row=self.context.header_row):
                for cell in row:
                    headers.append(cell.value)
        else: 
            (start, end) = self.column_range(self.context.columns)
            for number in range(start. end):
                headers.append(self.context.header_prefix + str(number).zfill(2))

        return headers


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

    def result(self, *, result, output):

        item = {
            'headers' : self.headers,
            'data' : result,
            'parameters' : self.context.parameters,
        }

        return self.output(result=item, output = output)
    
    def column_number(self, *, column:str):
        fulldigit = column.zfill(3)

        number = 0
        number = number + (int( self.ALPHABET_TABLE.find(fulldigit[0])) * 26 * 26)
        number = number + (int(self.ALPHABET_TABLE.find(fulldigit[1])) * 26)
        number = number + (int(self.ALPHABET_TABLE.find(fulldigit[2])))

        return number
    
    def column_range(self, *, column_range:str):
        (start, end) = column_range.split('-')
        return (self.column_number(start), self.column_number(end))

    def sheets_range(self, *, sheets):
        (start, end) = sheets.split('-')
        return (int(start), int(end))
