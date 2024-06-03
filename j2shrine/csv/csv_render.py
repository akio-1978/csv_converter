import io
import csv
from ..render import Render
from ..context import RenderContext

class CsvRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context: RenderContext):
        super().__init__(context=context)
        # 変更される可能性があるためcopyする
        self.cols = context.names.copy() if context.names is not None else []

    def build_reader(self, *, source: io.TextIOWrapper):
        # csvヘッダの有無が不定のため、DictReaderは使用しない
        return csv.reader(source, delimiter=self.context.delimiter)

    def read_source(self, *, reader):
        lines = []

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
        for line_no, columns in enumerate(reader):
            line = self.read_row(line_no=line_no, columns=columns)
            lines.append(line)

        return lines

    def finish(self, *, result:list):
        final_result = {
            'rows': result,
            'cols': self.cols,
            'params': self.context.parameters
        }
        return final_result

    # カラムのlistをdictに変換する。
    def read_row(self, *, line_no:int, columns: str):
        line = {}
        for index, column in enumerate(columns):
            name = self.get_name(index)
            line[name] = column
        return line

