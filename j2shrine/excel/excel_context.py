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
    def __init__(self):
        pass
        # defalut
        # A2:C4 read A2:C4 => 3row * 3column = 9 cells
        # A2:C read A2:C   => 3row * all_rows = 3(all_rows) cells
