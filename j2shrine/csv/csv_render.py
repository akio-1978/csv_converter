import csv
from ..loader import Loader
from ..context import RenderContext
from ..processors import Processor
from ..utils import get_stream

class CsvLoader(Loader):

    # jinja2テンプレートの生成
    def __init__(self, *, context: RenderContext, processor: Processor):
        super().__init__(context=context, processor=processor)
        # カラム名は追加される可能性があるためcopyする
        self.cols = context.names.copy() if context.names is not None else []

    def loading(self):
        with get_stream(source=self.context.source,encoding=self.context.input_encoding) as src:
            reader = csv.reader(src, delimiter=self.context.delimiter)
            # スキップ指定があれば行を読み飛ばす
            # ヘッダ行の処理は読み飛ばし後から始める
            if self.context.skip_lines:
                for n in range(self.context.skip_lines):
                    next(reader)

            # 指定されていれば先頭行をヘッダにする
            # context.read_headerはcontext.namesより優先される
            if self.context.read_header:
                self.cols = next(reader)

            # line単位ループ
            lines = []
            for line_no, columns in enumerate(reader):
                line = self.read_row(line_no=line_no, columns=columns)
                lines.append(line)

            return {
                'rows': lines,
                'cols': self.cols,
            }


    # カラムのlistをdictに変換する。
    def read_row(self, *, line_no:int, columns: str):
        line = {}
        for index, column in enumerate(columns):
            name = self.get_name(index)
            line[name] = column
        return line

