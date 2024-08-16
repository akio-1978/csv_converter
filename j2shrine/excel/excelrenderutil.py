import openpyxl
from .excel_render import CellPosition

def parse_read_range(*, range_str: str):
    """引数文字列を起点と終点に分割"""
    (arg_left, delim, arg_right) = range_str.partition(':')

    if arg_left == range_str:
        raise ValueError('invalid range: ' + range_str)

    start = get_coordinate(coordinate=arg_left)
    end = get_coordinate(coordinate=arg_right)

    return (start, end)

# セル位置またはセル範囲を取得
def get_coordinate(*, coordinate: str):

    if coordinate.isalpha() and coordinate.isascii():
        # A2:Cの場合Cがここに入る
        column = openpyxl.utils.cell.column_index_from_string(coordinate)
        return CellPosition(None, column)
    else:
        # A2 C4 はここに入る
        row, col = openpyxl.utils.cell.coordinate_to_tuple(coordinate)
        return CellPosition(row, col)

# 引数書式からシート範囲を特定する
def parse_sheet_args(*, sheets_range_str: str):
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
    # この段階ではシート総数が解らないのでNoneにする
    return (start, None)
