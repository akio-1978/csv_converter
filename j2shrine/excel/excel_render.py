from typing import NamedTuple
import openpyxl
from ..render import Render
from .excel_custom_filter import excel_time

class CellPosition(NamedTuple):
    row:str
    col:str

class CellRange(NamedTuple):
    start:CellPosition
    end:CellPosition
class Sheets(NamedTuple):
    start:int
    end:int

class ExcelRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        super().__init__(context=context)

    def install_filters(self, *, environment):
        super().install_filters(environment=environment)
        environment.filters['excel_time'] = excel_time

    def build_reader(self, *, source: any):
        # 既にブックで渡された場合、そのまま返す
        if (isinstance(source, openpyxl.Workbook)):
            return source
        # ファイルの場合はロードする
        return openpyxl.load_workbook(source, data_only=True)

    def read_source(self, *, reader):

        cells = self.parse_cell_args(
            arg_range=self.context.read_range)

        sheets = self.parse_sheet_args(
            sheets_range=self.context.sheets, sheets=reader.worksheets)

        results = []
        sheet_idx = sheets.start
        while sheet_idx <= sheets.end:
            sheet = reader.worksheets[sheet_idx]

            # コンテンツ読込み
            sheet_data = {
                'name': reader.sheetnames[sheet_idx],
                'rows': [],
                'abs': self.read_absolute_cells(sheet=sheet)
            }
            for row in sheet.iter_rows(min_col=cells.start.col, min_row=cells.start.row,
                                       max_col=cells.end.col, max_row=cells.end.row, ):
                sheet_data['rows'].append(self.columns_to_dict(columns=row))

            results.append(sheet_data)
            sheet_idx = 1 + sheet_idx
        return results

    def read_absolute_cells(self, *, sheet):
        cells = {}
        for addr in self.context.absolute:
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

    def read_column(self, *, name, column):
        # データの取り出し
        if (hasattr(column, 'value')):
            return column.value
        else:
            return None

    # 引数書式からシート範囲を特定する
    def parse_sheet_args(self, *, sheets_range: str, sheets: openpyxl.worksheet.worksheet):
        # コロン区切りの数値を左右に分割
        params = sheets_range.split(':')

        # 戻り値は0オリジンにする
        start = int(params[0]) - 1
        
        if len(params) < 2:
            # 単一のシ－トが対象 ex "1"
            return Sheets(start, start)
        elif params[1].isnumeric():
            # シート範囲を指定 ex "1:3"
            return Sheets(start, int(params[1]) - 1)
        # 指定のシ－トより右側の全てが対象 ex "1:"
        return Sheets(start, len(sheets) - 1)

    # 引数書式をからセル範囲を特定する
    # "A4:D" など最終行を指定しないパターンがある
    def parse_cell_args(self, *, arg_range: str):

        (arg_left, delim, arg_right) = arg_range.partition(':')

        if arg_left == arg_range:
            raise ValueError('invalid range: ' + arg_range)

        left = self.get_coordinate(coordinate=arg_left)
        right = self.get_coordinate(coordinate=arg_right)

        return CellRange(left, right)

    def get_coordinate(self, *, coordinate: str):
        if coordinate.isalpha() and coordinate.isascii():
            # args is column only. read all rows.
            column = openpyxl.utils.cell.column_index_from_string(coordinate)
            return CellPosition(None, column)
        else:
            # full specified coordinate.
            row, col = openpyxl.utils.cell.coordinate_to_tuple(coordinate)
            return CellPosition(row, col)

    def get_cell_value(self, *, sheet, cell):

        if hasattr(sheet[cell], 'value'):
            return sheet[cell].value
        else:
            return None

    def get_column_letter(self, *, column):
        return openpyxl.utils.cell.get_column_letter(column.column)
