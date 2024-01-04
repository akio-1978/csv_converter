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
        self.encoding = 'utf8'
        self.sheets = '1'
        # A2:C4 read A2:C4 => 3row * 3column = 9 cells
        # A2:C read A2:C   => 3row * all_rows = 3(all_rows) cells
        self._read_range = None
        self.absolute = []
        # assign args
        super().__init__(args=args)

    @property
    def read_range(self):
        return self._read_range
    @read_range.setter
    def read_range(self, value):
        self._read_range = self.parse_read_range(range_str=value)

    # @property
    # def sheets(self):
    #     return self._sheets

    # 引数書式をからセル範囲を特定する
    # "A4:D" など最終行を指定しないパターンがある
    def parse_read_range(self, *, range_str: str):

        (arg_left, delim, arg_right) = range_str.partition(':')

        if arg_left == range_str:
            raise ValueError('invalid range: ' + range_str)

        start = self.get_coordinate(coordinate=arg_left)
        end = self.get_coordinate(coordinate=arg_right)

        return CellRange(start, end)

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
        

        
@dataclass
class CellPosition:
    row:str
    col:str
@dataclass
class CellRange:
    start:CellPosition
    end:CellPosition
@dataclass
class Sheets:
    start:int
    end:int
