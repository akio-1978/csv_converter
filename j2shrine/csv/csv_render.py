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
        for lineno, columns in enumerate(reader):
            line = self.readline(lineno=lineno, columns=columns)
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
    def readline(self, *, lineno:int, columns: str):
        line = {}
        for index, column in enumerate(columns):
            header = self.next_header(index)
            line[header] = column
        return line

    # カラム名取得
    def next_header(self, index):
        if len(self.cols) <= index:
            # ヘッダが定義されていない場合
            # または定義済みのヘッダよりも実際のカラムが多い場合はヘッダを追加で生成する
            self.cols.append(self.context.header_prefix + str(index).zfill(2))
        return self.cols[index]
    