from dataclasses import dataclass
import openpyxl

from ..context import RenderContext
from .excel_render import ExcelRender


# 取得するシート a a-b a-
# 取得するカラムのレンジ A A-Z A-
# 取得する行 a a-b a-
# option
# ヘッダ行
# ヘッダ直接指定
# 追加取得セル...
class ExcelRenderContext(RenderContext):
    def __init__(self, *, args):
        # defalut
        # A2:C4 read A2:C4 => 3row * 3column = 9 cells
        # A2:C read A2:C   => 3row * all_rows = 3(all_rows) cells
        self._read_range = None
        self._sheets = (0, 0)
        self.absolute = {}
        self.prefix = 'col_'
        self.names = []
        # assign args
        super().__init__(args=args)

    # 読み取り領域
    @property
    def read_range(self):
        return self._read_range
    @read_range.setter
    def read_range(self, value):
        self._read_range = self.parse_read_range(range_str=value)

    @property
    def sheets(self):
        return self._sheets
    @sheets.setter
    def sheets(self, value):
        self._sheets = self.parse_sheet_args(sheets_range_str=value)

    # 引数書式をからセル範囲を特定する
    # "A4:D" など最終行を指定しないパターンがある
    def parse_read_range(self, *, range_str: str):

        (arg_left, delim, arg_right) = range_str.partition(':')

        if arg_left == range_str:
            raise ValueError('invalid range: ' + range_str)

        start = self.get_coordinate(coordinate=arg_left)
        end = self.get_coordinate(coordinate=arg_right)

        return (start, end)

    # セル位置またはセル範囲を取得
    def get_coordinate(self, *, coordinate: str):
        if coordinate.isalpha() and coordinate.isascii():
            # read all rows.
            column = openpyxl.utils.cell.column_index_from_string(coordinate)
            return CellPosition(None, column)
        else:
            # read to specified cell.
            row, col = openpyxl.utils.cell.coordinate_to_tuple(coordinate)
            return CellPosition(row, col)
        
    # 引数書式からシート範囲を特定する
    def parse_sheet_args(self, *, sheets_range_str: str):
        # コロン区切りの数値を左右に分割
        params = sheets_range_str.split(':')

        # 戻り値は0オリジンにする
        start = int(params[0]) - 1
        
        if len(params) < 2:
            # 単一のシ－トが対象 ex "1"
            return (start, start)
        elif params[1].isnumeric():
            # シート範囲を指定 ex "1:3"
            return (start, int(params[1]) - 1)
        # 指定のシ－トより右側の全てが対象 ex "1:"
        # ワークシートのシート数が解らないのでNoneにする
        return (start, None)

@dataclass
class CellPosition:
    """セル位置を表す行番号と列名"""
    row:str
    col:str
