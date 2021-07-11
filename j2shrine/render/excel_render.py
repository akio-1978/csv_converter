import openpyxl
from . base_render import Render, RenderContext

# 取得するシート a a-b a-
# 取得するカラムのレンジ A A-Z A-
# 取得する行 a a-b a-
# option
# ヘッダ行
# ヘッダ直接指定
# 追加取得セル...
class ExcelRenderContext(RenderContext):
    def __init__(self, *, template=None, template_encoding='utf8', parameters={}):
        super().__init__(template=template, template_encoding=template_encoding, parameters=parameters)
        self.encoding = 'utf8'
        self.sheets = '0'
        self.header_prefix='col_'
        self.headers = None         
        self.header_row = '0'     # ex."A2:M2"
        self.start_row = None      # ex."A3:M3"
        self.columns = 'A'
        self.limit = None
        self.extra_cells =[]

class ExcelRender(Render):

    ALPHABET_TABLE = '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # ALPHABET_TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # jinja2テンプレートの生成
    def __init__(self, *, context :ExcelRenderContext):
        super().__init__(context = context)

    def build_reader(self, *, source :any) :
        # 既にブックで渡された場合、そのまま返す
        if ( isinstance(source, openpyxl.Workbook)):
            return source
        # ファイルの場合はロードする
        return openpyxl.load_workbook(source)

    def read_source(self, *, reader):
        # シート取り出し
        (start_sheet, end_sheet) = self.sheets_range(sheets=self.context.sheets)
        end_sheet = end_sheet if end_sheet is not None else len(reader.worksheets)

        all_sheets = []
        for sheet_idx in range(start_sheet, end_sheet+1):
            print('----')
            sheet = reader.worksheets[sheet_idx]
            # ヘッダの読込み
            self.headers = self.read_headers(sheet=sheet)
            # コンテンツ読込み範囲決定
            (start, end) = self.column_range(columns= self.context.columns)
            # コンテンツ読込み
            sheet_content = []
            for row in sheet.iter_rows(min_col=start, min_row=self.context.start_row , max_col=end, max_row=self.context.limit, ):
                sheet_content.append(self.columns_to_dict(columns = row))
            all_sheets.append(sheet_content)
            if (sheet_idx == end_sheet):
                break
        return all_sheets

    def read_headers(self, *, sheet:openpyxl.worksheet.worksheet):
        headers = []
        if self.context.headers is not None:
            headers = self.context.headers
        elif self.context.header_area is not None:
            (start, end) = self.column_range(columns= self.context.columns)
            for row in sheet.iter_rows(min_col=start, min_row=int(self.context.header_row),
                                        max_col=end, max_row=int(self.context.header_row)):
                for cell in row:
                    headers.append(cell.value)
        else: 
            (start, end) = self.column_range(self.context.columns)
            for row in sheet.iter_rows(min_col=start, min_row=self.context.start_row,
                                        max_col=end, max_row=self.context.start_row):
                for cell in row:
                    headers.append(cell.column_letter)

        return headers

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
        number = number + (int( ExcelRender.ALPHABET_TABLE.find(fulldigit[0])) * 26 * 26)
        number = number + (int(ExcelRender.ALPHABET_TABLE.find(fulldigit[1])) * 26)
        number = number + (int(ExcelRender.ALPHABET_TABLE.find(fulldigit[2])))

        return number
    
    def column_range(self, *, columns:str):
        divided = columns.partition('-')
        if divided[0] == columns:
            return (self.column_number(column=divided[0]), self.column_number(column=divided[0]))
        if divided[2] != '':
            return (int(divided[0]), int(divided[2]))
        else:
            return (int(divided[0]), None)

    def sheets_range(self, *, sheets):
        divided = sheets.partition('-')
        if divided[0] == sheets:
            return (int(sheets), int(sheets))
        if divided[2] != '':
            return (int(divided[0]), int(divided[2]))
        else:
            return (int(divided[0]), None)

    def get_cell_value(self, *, sheet, cell):
        return sheet[cell].value

