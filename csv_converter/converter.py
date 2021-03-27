from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import csv
from . jinja2_custom_filter import sequential_group_by

# transformerに渡すパラメータクラス
class ConverterContext:

    def __init__(self, *, template_source):
        self.use_header = False
        self.encoding = 'utf8'
        self.delimiter = ','
        self.header_prefix='col_'
        self.options={}
        self.template_source = template_source
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

    # CSVファイルの各行にテンプレートを適用して、出力する
    def convert(self, *, source, output):
        lines = []
        # csvreaderを使って読み込み
        reader = csv.reader(source, delimiter = self.context.delimiter)
        for line_no, columns in enumerate(reader):
            # ヘッダ読み込み、ヘッダがない場合は連番をヘッダにする
            if line_no == 0:
                self.headers = self.get_headers(context = self.context, columns = columns)
                # ヘッダとして先頭行を読み込んだ場合
                if self.context.use_header:
                    continue

            # 1行分の読み込みと変換
            line = self.read_line_hook(line = self.columns_to_dict(columns = columns))
            lines.append(line)

        # 全体読み込み後の変換
        all_lines = self.read_all_line_hook(all_lines = lines)

        print(
            self.template.render(
                {'lines' : all_lines}
            ),
            file = output
        )


    # カラムのlistをdictに変換する。dictのキーはself.headers
    def columns_to_dict(self, *, columns):
        line = self.context.line_object()
        # カラムとヘッダの長さは揃っていることが前提
        for header, column in zip(self.headers, columns):
            # カラム単体の変換処理を行う
            setattr(line, header, self.read_column_hook(header = header, column = column))
#            line[header] = self.read_column_hook(header = header, column = column)

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
    def read_column_hook(self, *, header, column):
        return column.strip()

    # 1行分の読込結果を変換する。
    # resultはヘッダをキーにしたカラムのリスト
    # 返値はdictであること。デフォルトではresultをそのまま返す。
    def read_line_hook(self, *, line):
        # 何もしない
        return line

    # 全て読み込みが終わった後に変換が必要な場合の処理
    def read_all_line_hook(self, *, all_lines):
        # 何もしない
        return all_lines

