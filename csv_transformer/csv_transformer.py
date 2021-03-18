from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import csv

# transformerに渡すパラメータクラス
class TransfomerParameters:

    def __init__(self, *, template_source):
        self.use_header = False
        self.encoding = 'utf8'
        self.delimiter = ','
        self.header_prefix='col_'
        self.options={}
        self.template_source = template_source

class CsvTransformer:

    # jinja2テンプレートの生成
    def __init__(self, *, parameters):
        self.parameters = parameters
        self.init_template(parameters = parameters)

    # オーバーライドすると、ファイル名指定以外の方法でテンプレートを取得できる
    def init_template(self, *, parameters):
        path = Path(parameters.template_source)
        environment = Environment(loader = FileSystemLoader(path.parent, encoding=parameters.encoding))
        self.template = environment.get_template(path.name)

    # CSVファイルの各行にテンプレートを適用して、出力する
    def transform(self, *, source, output):
        lines = []
        # csvreaderを使って読み込み
        reader = csv.reader(source, delimiter = self.parameters.delimiter)
        for line_no, columns in enumerate(reader):
            # ヘッダ読み込み、ヘッダがない場合は連番をヘッダにする
            if line_no == 0:
                self.headers = self.get_headers(parameters = self.parameters, columns = columns)
            # 先頭行がヘッダだった場合は先頭行をデータとして扱わない
            if line_no == 0 and self.parameters.use_header:
                continue
            # 1行分の読み込みと変換
            transformed_line = self.transform_line(line = self.read_line_columns_hook(columns = columns))
            lines.append(transformed_line)

        # 全体読み込み後の変換
        transformed_all = self.read_all_line_hook(all_lines = lines)

        print(
            self.template.render(
                {'lines' : transformed_all}
            ),
            file = output
        )


    # カラムのlistをdictに変換する。dictのキーはself.headers
    def read_line_columns_hook(self, *, columns):
        line = {}
        # カラムとヘッダの長さは揃っていることが前提
        for header, column in zip(self.headers, columns):
            # カラム単体の変換処理を行う
            line[header] = self.read_column_hook(column = column)

        return line

    def get_headers(self, *, parameters, columns):
        headers = []
        for idx, column in enumerate(columns):
            header = None
            if parameters.use_header:
                # ヘッダあり指定の場合、カラム文字列をそのままヘッダにする
                header = column.strip()
            else:
                # ヘッダなしの場合、カラムのインデックスからヘッダを作る
                header = parameters.header_prefix + str(idx).zfill(2)

            headers.append(header)
        return headers

    # 以下をオーバーライドして変換をカスタマイズできる
    # jinja2カスタムテンプレートのインストール
    def install_jinja2_filters(self, *, environment, parameters):
        return environment

    # 1カラム分の読込結果を変換する。
    # デフォルトではstripをかけて余分なスペースを取り除く
    def read_column_hook(self, *, column):
        return column.strip()

    # 1行分の読込結果を変換する。
    # resultはヘッダをキーにしたカラムのリスト
    # 返値はdictであること。デフォルトではresultをそのまま返す。
    def transform_line(self, *, line):
        # 何もしない
        return line

    # 全て読み込みが終わった後に変換が必要な場合の処理
    def read_all_line_hook(self, *, all_lines):
        # 何もしない
        return all_lines

