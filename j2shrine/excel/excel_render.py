import openpyxl
from ..render import Render
from ..context import RenderContext
from .excel_custom_filter import excel_time

class ExcelRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context: RenderContext):
        super().__init__(context=context)
        # 変更される可能性があるためcopyする
        self.cols = context.names.copy() if context.names is not None else []

    def install_filters(self, *, environment):
        super().install_filters(environment=environment)
        environment.filters['excel_time'] = excel_time

    def get_source_reader(self, *, source: str):
        """openpyxlでブックを開く"""
        return openpyxl.load_workbook(source, data_only=True)

    def read_source(self, *, reader):
        """Workbookの中身をcontextに従って読み取る"""
        # シート内セルの読み込み範囲
        (start, end) = self.context.read_range
        # 読み込むシートの範囲
        (first_sheet, end_sheet) = self.context.sheets

        # 読み取りシート範囲の指定
        if (end_sheet is None):
            # endがNoneの場合最後のシートまで読む
            end_sheet = len(reader.worksheets)-1

        results = []
        sheet_idx = first_sheet
        while sheet_idx <= end_sheet:
            sheet = reader.worksheets[sheet_idx]

            # シート読込み開始
            sheet_data = {
                # シート名
                'name': reader.sheetnames[sheet_idx], 
                # 絶対座標指定セル
                'abs': self.absolute_cells(sheet=sheet, cells=self.context.absolute),
                # シート内容の行
                'rows': [],
            }
            # シート内の指定範囲のセルの読み込み
            for line_no, row in enumerate(sheet.iter_rows(min_col=start.col, min_row=start.row,
                                       max_col=end.col, max_row=end.row, )):
                # rowsを一行ずつ処理
                sheet_data['rows'].append(self.read_row(line_no=line_no, cells=row))

            results.append(sheet_data)
            sheet_idx = 1 + sheet_idx
        return results

    def read_row(self, *, line_no:int, cells:list):
        """カラムのlistをdictに変換する。dictのキーはcontext.namesで与えられた名前か、連番になる。"""
        line = {}
        for index, cell in enumerate(cells):
            name = self.get_name(index)
            # カラムから値を取り出す
            line[name] = self.read_value(name=name, cell=cell)
        return line

    def absolute_cells(self, *, sheet, cells: dict):
        """絶対座標セル値の取得"""
        cell_values = {}
        for name, addr in cells.items():
            cell_values[name] = self.read_value(name=name, cell=sheet[addr])
        return cell_values

    def read_value(self, *, name, cell):
        """value属性が存在すればセルの値を取得する"""
        return cell.value if hasattr(cell, 'value') else None

    # jinja2へ渡す読み取り結果
    def read_finish(self, *, result):
        final_result = {
            'sheets': result,
            'params': self.context.parameters
        }
        return final_result
