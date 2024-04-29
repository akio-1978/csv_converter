import openpyxl
from openpyxl import Workbook
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

    def build_reader(self, *, source: str) -> Workbook:
        """openpyxlでブックを開く"""
        return openpyxl.load_workbook(source, data_only=True)

    def read_source(self, *, reader: Workbook):
        """Workbookの中身をcontextに従って読み取る"""
        (start, end) = self.context.read_range
        (first_sheet, end_sheet) = self.context.sheets
        # endがNoneの場合最後のシートまで読む
        if (end_sheet is None):
            end_sheet = len(reader.worksheets)-1

        results = []
        sheet_idx = first_sheet
        while sheet_idx <= end_sheet:
            sheet = reader.worksheets[sheet_idx]

            # コンテンツ読込み
            sheet_data = {
                'name': reader.sheetnames[sheet_idx],
                'rows': [],
                'abs': self.absolute_cells(sheet=sheet, cells=self.context.absolute)
            }
            for line_no, row in enumerate(sheet.iter_rows(min_col=start.col, min_row=start.row,
                                       max_col=end.col, max_row=end.row, )):
                sheet_data['rows'].append(self.read_row(line_no=line_no, columns=row))

            results.append(sheet_data)
            sheet_idx = 1 + sheet_idx
        return results

    # カラムのlistをdictに変換する。dictのキーはセル位置
    def read_row(self, *, line_no, columns):
        line = {}
        for index, column in enumerate(columns):
            letter = self.column_name(index)
            # カラムから値を取り出す
            line[letter] = self.read_column(name=letter, column=column)
        return line

    def absolute_cells(self, *, sheet, cells: dict):
        cell_values = {}
        for name, addr in cells.items():
            cell_values[name] = self.read_column(name=name, column=sheet[addr])
        return cell_values

    # openpyxlのCellオブジェクトからの値読み出し
    def read_column(self, *, name, column):
        # value属性が存在しない場合がある
        if (hasattr(column, 'value')):
            return column.value
        else:
            return None

    # jinja2へ渡す読み取り結果
    def finish(self, *, result):
        final_result = {
            'sheets': result,
            'params': self.context.parameters
        }
        return final_result
