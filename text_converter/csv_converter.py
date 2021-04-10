from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import csv
from . jinja2_custom_filter import sequential_group_by
from . converter_context import ConverterContext

# transformerに渡すパラメータクラス
class CsvConverterContext(ConverterContext):

    def __init__(self, *, template_source):
        super().__init__(template_source = template_source)
        self.use_header = False
        self.encoding = 'utf8'
        self.delimiter = ','
        self.header_prefix='col_'
        self.options={}
        self.headers = None
        self.line_object = LineValues

class LineValues:
    pass

class CsvConverter:

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        self.context = context
        self.build_convert_engine(context = context)

    # 別の方法でテンプレートを生成する場合はオーバーライドする
    def build_convert_engine(self, *, context):
        path = Path(context.template_source)
        environment = Environment(loader = FileSystemLoader(path.parent, encoding=context.encoding))
        environment.filters['sequential_group_by'] = sequential_group_by
        self.template = environment.get_template(path.name)

    def build_reader(self, *, source):
        # csvreaderを使って読み込み
        return csv.reader(source, delimiter = self.context.delimiter)

    # CSVファイルの各行にテンプレートを適用して、出力する
    def convert(self, *, source, output):
        reader = self.build_reader(source = source)
        read_result = self.read_source(reader = reader)
        self.output_result(read_result = read_result, output = output)

    def read_source(self, *, reader):
        lines = []
        for line_no, columns in enumerate(reader):
            # ヘッダ読み込み、ヘッダがない場合は連番をヘッダにする
            if line_no == 0:
                self.headers = self.get_headers(context = self.context, columns = columns)
                # ヘッダとして先頭行を読み込んだ場合
                if self.context.use_header:
                    continue
            line = self.read_line(columns = columns)
            lines.append(line)
        # 全体読み込み後の変換
        return self.read_finish(all_lines = lines)

    def output_result(self, *, read_result, output):
        print(
            self.template.render(
                {'data' : read_result, 'options' : self.context.options}
            ),
            file = output
        )

    # カラムのlistをdictに変換する。dictのキーはself.headers
    def read_line(self, *, columns):
        line = self.context.line_object()
        # カラムとヘッダの長さは揃っていることが前提
        for header, column in zip(self.headers, columns):
            # カラム単体の変換処理を行う
            setattr(line, header, self.read_column(name = header, column = column))

        return line

    def get_headers(self, *, context, columns):
        headers = []
        for idx, column in enumerate(columns):
            header = None
            if context.use_header:
                # ヘッダあり指定の場合、カラム文字列をそのままヘッダにする
                header = column.strip()
            else:
                # ヘッダなしの場合、カラムのインデックスからヘッダを作る
                header = context.header_prefix + str(idx).zfill(2)

            headers.append(header)
        return headers

    # 1カラム分の読込結果を変換する。
    # デフォルトではstripをかけて余分なスペースを取り除く
    def read_column(self, *, name, column):
        return column.strip()

    # 全て読み込みが終わった後に変換が必要な場合の処理
    def read_finish(self, *, all_lines):
        # 何もしない
        return all_lines

