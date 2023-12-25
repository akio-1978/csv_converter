import openpyxl
from ..render import Render
from .excel_context import ExcelRenderContext
from .excel_custom_filter import excel_time


class ReadSetting:
    def __init__(self, *, sheet_left: int, sheet_right: int, left_row: str, left_column: str, right_row: str, right_column: str) -> None:
        self.sheet_left = sheet_left
        self.sheet_right = sheet_right
        self.left_row = left_row
        self.left_column = left_column
        self.right_row = right_row
        self.right_column = right_column

    def get_sheet_right(self, sheets: openpyxl.worksheet.worksheet):
        if self.sheet_right is not None:
            return self.sheet_right
        else:
            return len(sheets) - 1


class ExcelRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context: ExcelRenderContext):
        super().__init__(context=context)

    def install_filters(self, *, environment):
        super().install_filters(environment=environment)
        environment.filters['excel_time'] = excel_time

    def setup_range(self):

        (left_row, left_column, right_row, right_column) = self.get_read_range(
            arg_range=self.context.read_range)
        (sheet_left, sheet_right) = self.get_sheet_range(
            sheets_range=self.context.sheets)

        return ReadSetting(sheet_left=sheet_left, sheet_right=sheet_right,
                           left_row=left_row, left_column=left_column, right_row=right_row, right_column=right_column)

    def build_reader(self, *, source: any):
        # 既にブックで渡された場合、そのまま返す
        if (isinstance(source, openpyxl.Workbook)):
            return source
        # ファイルの場合はロードする
        return openpyxl.load_workbook(source, data_only=True)

    def read_source(self, *, reader):

        setting = self.setup_range()
        sheet_right = setting.get_sheet_right(sheets=reader.worksheets)

        all_sheets = []
        sheet_idx = setting.sheet_left
        while sheet_idx <= sheet_right:
            sheet = reader.worksheets[sheet_idx]

            # コンテンツ読込み
            sheet_data = {
                'name': reader.sheetnames[sheet_idx],
                'rows': [],
                'fixed': self.read_fixed_cells(sheet=sheet)
            }
            for row in sheet.iter_rows(min_col=setting.left_column, min_row=setting.left_row,
                                       max_col=setting.right_column, max_row=setting.right_row, ):
                sheet_data['rows'].append(self.columns_to_dict(columns=row))

            all_sheets.append(sheet_data)
            sheet_idx = 1 + sheet_idx
        return all_sheets

    def read_fixed_cells(self, *, sheet):
        cells = {}
        for addr in self.context.fixed:
            cells[addr] = sheet[addr].value
        return cells

    def finish(self, *, result):

        final_result = {
            'sheets': result,
            'params': self.context.parameters
        }

        return final_result

    # カラムのlistをdictに変換する。dictのキーはself.headers
    def columns_to_dict(self, *, columns):
        line = {}

        for column in columns:
            letter = self.get_column_letter(column=column)
            # カラム単体の変換処理を行う
            line[letter] = self.read_column(name=letter, column=column)
        return line

    def columns_dict(self, *, columns_dict):
        return columns_dict

    # hook by every column
    def read_column(self, *, name, column):
        # データの取り出し
        if (hasattr(column, 'value')):
            return column.value
        else:
            return None

    # 読み込むシートの範囲をタプルで取得
    def get_sheet_range(self, *, sheets_range: str):
        # コロン区切りの数値を左右に分割
        params = sheets_range.split(':')

        # 戻り値は0オリジンにする
        start = int(params[0]) - 1
        
        if len(params) < 2:
            # 単一のシ－トが対象 ex "1"
            return (start, start)
        elif params[1].isnumeric():
            # シート範囲を指定 ex "1:3"
            return (start, int(params[1]) - 1)
        # 指定のシ－トより右側の全てが対象 ex "1:"
        return (start, None)

    def get_read_range(self, *, arg_range: str):

        (left, delim, right) = arg_range.partition(':')

        if left == arg_range:
            raise ValueError('invalid range: ' + arg_range)

        (left_row, left_column) = self.get_coordinate(coordinate=left)
        (right_row, right_column) = self.get_coordinate(coordinate=right)

        return (left_row, left_column, right_row, right_column)

    def get_coordinate(self, *, coordinate: str):
        if coordinate.isalpha() and coordinate.isascii():
            # args is column only. read all rows.
            column = openpyxl.utils.cell.column_index_from_string(coordinate)
            return (None, column)
        else:
            # full specified coordinate.
            return openpyxl.utils.cell.coordinate_to_tuple(coordinate)

    def get_cell_value(self, *, sheet, cell):

        if hasattr(sheet[cell], 'value'):
            return sheet[cell].value
        else:
            return None

    def get_column_letter(self, *, column):
        return openpyxl.utils.cell.get_column_letter(column.column)
