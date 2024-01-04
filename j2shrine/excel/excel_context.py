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
        # A2:C4  (read cells from A2 to C4) or A2:C (read cells in all rows from 2)
        self.read_range = None
        self.absolute = []
        # assign args
        super().__init__(args=args)
        
    def new_render(self):
        return ExcelRender(context=self)
