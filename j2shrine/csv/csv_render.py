import csv
from ..render import Render
from ..context import RenderContext

class CsvRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context: RenderContext):
        super().__init__(context=context)
        self.cols = context.names.copy()

    def build_reader(self, *, source):
        # csvヘッダの有無が不定のため、DictReaderは使用しない
        return csv.reader(source, delimiter=self.context.delimiter)

    def read_source(self, *, reader):
        lines = []

        # スキップ指定があれば行を読み飛ばす
        # ヘッダ行の処理は読み飛ばし後から始める
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

    def finish(self, *, result):
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
            name = self.column_name(index)
            line[name] = column
        return line

    # カラム名取得
    def column_name(self, index):
        if len(self.cols) <= index:
            # カラム名が定義されていない場合
            # または定義済みのカラム名よりも実際のカラムが多い場合はカラム名を追加で生成する
            self.cols.append(self.context.prefix + str(index).zfill(2))
        return self.cols[index]
    