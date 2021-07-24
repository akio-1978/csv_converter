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
        self.header_row = '0'     # ex. 1
        self.rows = '1'      # 1 1-2 1-
        self.columns = 'A'  # A A-B A-
        self.limit = None
        self.extra_cells =[]

class ExcelRender(Render):

    ALPHABET_TABLE = '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    TO_END = -1

    # jinja2テンプレートの生成
    def __init__(self, *, context :ExcelRenderContext):
        super().__init__(context = context)
        # シートからの取得範囲は最初に特定する
        self.setup_range()

    def setup_range(self):
        (left, right) = self.parse_range(arg_range = self.context.columns)
        self.left = self.column_number(column=left) if left is not None else 1
        self.right = self.column_number(column=right) if right is not None else None

        (top, bottom) = self.parse_range(arg_range = self.context.rows)
        self.top = int(top) if top is not None else 1
        self.bottom = int(bottom) if bottom is not None else None

        (sheet_left, sheet_right) = self.parse_range(arg_range = self.context.sheets, all=ExcelRender.TO_END)
        self.sheet_left = int(sheet_left) if sheet_left is not None else 0
        self.sheet_right = int(sheet_right) if sheet_right is not None else 0


    def build_reader(self, *, source :any) :
        # 既にブックで渡された場合、そのまま返す
        if ( isinstance(source, openpyxl.Workbook)):
            return source
        # ファイルの場合はロードする
        return openpyxl.load_workbook(source)

    def read_source(self, *, reader):
        # シート取り出し
        sheet_right = self.sheet_right if self.sheet_right != ExcelRender.TO_END else len(reader.worksheets) - 1

        all_sheets = []
        sheet_idx = self.sheet_left
        print('idx:', sheet_idx, 'right:', sheet_right)
        while sheet_idx <= sheet_right:
            sheet = reader.worksheets[sheet_idx]
            # ヘッダの読込み
            self.headers = self.read_headers(sheet=sheet)

            # コンテンツ読込み
            sheet_data = {
                'name' : reader.sheetnames[sheet_idx],
                'rows' : [],
                'ext' : {}
            }
            print('min-col', self.left, 'min-row', self.top, 'max-col', self.right, 'max-row', self.bottom,)
            for row in sheet.iter_rows(min_col=self.left, min_row=self.top , max_col=self.right, max_row=self.bottom, ):
                sheet_data['rows'].append(self.columns_to_dict(columns = row))
            all_sheets.append(sheet_data)
            print('total sheets:', len(all_sheets))
            sheet_idx = 1 + sheet_idx
        return all_sheets

    def read_finish(self, *, source_data):

        return {'sheets' : source_data, 'headers' : self.headers,}


    def read_headers(self, *, sheet:openpyxl.worksheet.worksheet):
        headers = []
        if self.context.headers is not None:
            headers = self.context.headers
        elif self.context.header_row is not None:
            for row in sheet.iter_rows(min_col=self.left, min_row=int(self.context.header_row),
                                        max_col=self.right, max_row=int(self.context.header_row)):
                for cell in row:
                    headers.append(cell.value)
        else: 
            for row in sheet.iter_rows(min_col=self.left, min_row=self.bottom,
                                        max_col=self.right, max_row=self.top):
                for cell in row:
                    headers.append(cell.column_letter)

        print('headers', headers)
        return headers

    # カラムのlistをdictに変換する。dictのキーはself.headers
    def columns_to_dict(self, *, columns):
        line = {}
        # カラムとヘッダの長さは揃っていることが前提
        for header, column in zip(self.headers, columns):
            # カラム単体の変換処理を行う
            line[header] = self.read_column(name = header, column = column)
            # print('read:', header, 'value:', line[header])
        return line

    def columns_dict(self, *, columns_dict):
        return columns_dict

    # hook by every column
    def read_column(self, *, name, column):
        # データの取り出し
        return column.value
    
    def column_number(self, *, column:str):
        fulldigit = column.zfill(3)

        number = 0
        number = number + (int( ExcelRender.ALPHABET_TABLE.find(fulldigit[0])) * 26 * 26)
        number = number + (int(ExcelRender.ALPHABET_TABLE.find(fulldigit[1])) * 26)
        number = number + (int(ExcelRender.ALPHABET_TABLE.find(fulldigit[2])))

        return number
    
    def parse_range(self, *, arg_range:str, all=None):

        if (arg_range is None):
            return (None, None)

        divided = arg_range.partition('-')
        if divided[0] == arg_range:
            # only one
            return (divided[0], divided[0])
        if divided[2] != '':
            # start to end
            return (divided[0], divided[2])
        else:
            # start to all
            return (divided[0], all)


    def get_cell_value(self, *, sheet, cell):
        return sheet[cell].value

