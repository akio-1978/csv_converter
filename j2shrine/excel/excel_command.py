import argparse
import openpyxl
from j2shrine.context import RenderContext
from ..command import Command, KeyValuesParseAction
from .excel_render import ExcelRender, CellPosition
from ..renderutils import get_stream, KeyValuesParseAction

class ExcelCommand(Command):

    HELP_SHEETS = """読込対象シート ('1' シート1のみ. '1:4' シート1からシート4まで. '1:' シート1からすべてのシート)"""
    HELP_READ_RANGE = """読込セル範囲 ('A1:D4' A1:D4の16セル 'A1:D' A1を起点として、AからDまでの全ての行.)"""

    def __init__(self,*, parsers: argparse.ArgumentParser):
        self.parser = parsers.add_parser('excel', help='Excelのレンダリングを行う', formatter_class=argparse.RawTextHelpFormatter)
        self.parser.set_defaults(command_instance=self)
        self.setup()

    def render_class(self):
        """Commandが使うRenderのクラスを返す"""
        return ExcelRender
    def context_class(self):
        """Commandが使うContextのクラスを返す"""
        return RenderContext

    def add_positional_arguments(self):
        """excel固有の必須引数があるので、位置引数を定義しなおす
            * excelブックをstdinから受け取れないため、ファイル名は必須
            * 読み取り対象シートの指定は必須
            * 読み取りセル範囲の指定は必須
        """
        self.parser.add_argument('template', help='使用するjinja2テンプレート.')
        # source book can't read from stdin
        self.parser.add_argument('source', help='レンダリング対象ブック xlsxファイルのみ対象.')
        self.parser.add_argument('sheets', help=ExcelCommand.HELP_SHEETS, action=SheetRangeAction)
        self.parser.add_argument('read_range', help=ExcelCommand.HELP_READ_RANGE, action=CellRangeAction)

    def add_optional_arguments(self):
        """excel固有のオプションを追加する"""
        # 基本的なオプションは引き継ぐ
        super().add_optional_arguments()
        # 絶対位置指定セルを追加する
        self.parser.add_argument(
            '-a', '--absolute', help='絶対位置指定でセル値を固定で取得する [セル位置=名前]の形式で列挙する. ex: A1=NAME1 A2=NAME2...', dest='absolute', nargs='*', default={}, action=KeyValuesParseAction)

    def call_render(self, *, render, source, out):
        """
        in側はopenpyxlにファイル名を直接渡す必要があるため、call_renderをoverrideする
        """
        with get_stream(source=out, 
                           encoding=render.context.output_encoding, 
                           mode='w' ) as dest:
            render.render(source=source, output=dest)

class CellRangeAction(argparse.Action):
    """ 読み取るセル範囲を表す座標情報をセットする
        ex. 指定値毎の動作
        A2:C4 => 3row * 3column = 9 cells
        A2:C  => 3row * all_rows = 3(all_rows) cells
        setattrされる値は2つのCellPositionのタプル（起点、終点）
        以下のコメントは引数がA2:C4またはA2:Cだった場合で書く
    """
    
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.parse_read_range(range_str=values))
    
    def parse_read_range(self, *, range_str: str):
        """引数文字列を起点と終点に分割"""
        (arg_left, delim, arg_right) = range_str.partition(':')

        if arg_left == range_str:
            raise ValueError('invalid range: ' + range_str)

        start = self.get_coordinate(coordinate=arg_left)
        end = self.get_coordinate(coordinate=arg_right)

        return (start, end)

    # セル位置またはセル範囲を取得
    def get_coordinate(self, *, coordinate: str):

        if coordinate.isalpha() and coordinate.isascii():
            # A2:Cの場合Cがここに入る
            column = openpyxl.utils.cell.column_index_from_string(coordinate)
            return CellPosition(None, column)
        else:
            # A2 C4 はここに入る
            row, col = openpyxl.utils.cell.coordinate_to_tuple(coordinate)
            return CellPosition(row, col)
        
class SheetRangeAction(argparse.Action):
    """処理対象シートを決定するアクション
        ex. 指定値毎の動作
        1    => 1枚目のシートを処理対象とする
        1:4  => 1-4枚目のシートを処理対象とする
        1:   => 1枚目以降全てのシートを処理対象とする
        setattrされる値は起点、終点のtuple(int)
    """
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.parse_sheet_args(range_str=values))

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
        # この段階ではシート総数が解らないのでNoneにする
        return (start, None)

