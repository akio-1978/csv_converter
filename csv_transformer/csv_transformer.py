import io
import sys
import itertools
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader
from csv import reader as csvreader
from csv_transformer import jinja2_filters

class CsvTransformer:

    # jinja2テンプレートの生成
    def __init__(self, *, parameters):
        self.parameters = parameters
        self.init_template(template_source=parameters)

    # オーバーライドすると、ファイル名指定以外の方法でテンプレートを取得できる
    def init_template(self, *, parameters):
        path = Path(parameters.template)
        environment = Environment(loader = FileSystemLoader(path.parent, encoding='utf-8'))
        self.template = environment.get_template(path.name)

    # CSVファイルの各行にテンプレートを適用して、出力する
    def transform(self, *, source, output):
        lines = []
        with self.get_datasource(source=source) as csvfile:
            # csvreaderを使って読み込み
            reader = csvreader(csvfile, delimiter = self.parameters.delimiter)
            firstline = True
            for columns in reader:
                # ヘッダ読み込み、ヘッダがない場合は連番をヘッダにする
                if firstline:
                    self.headers = self.get_headers(parameters = self.parameters, columns = columns)
                    firstline = False
                # 先頭行がヘッダだった場合は読み飛ばす
                if self.parameters.header:
                    continue
                # カラムに分けられた行の処理
                lines.append(self.parse_columns(columns = columns))
        print(
            self.template.render(
                {'lines' : lines}
            )
        )

    # 以下はオーバーライドできるようにメソッドを細かく分けた
    # jinja2カスタムテンプレートのインストール
    def install_jinja2_filters(self, *, environment, parameters):
        # environment.filters['groups'] = jinja2_filters.groups
        return environment

    def get_headers(self, *, parameters, columns):
        headers = []
        for idx in range[len(columns)]:
            header = None
            if parameters.header:
                # ヘッダあり指定の場合、カラム文字列をそのままヘッダにする
                header = columns[idx].strip()
            else:
                # ヘッダなしの場合、カラムのインデックスからヘッダを作る
                header = parameters.raw_colmun_prefix + ''.zfill(2)

            headers.append(header)
        return headers

    # csvファイル読込
    def get_datasource(self, *, source, input_encoding='utf-8'):
        return open(source, 'r', encoding=input_encoding, newline='')

    # カラムに分けられた行の処理
    def parse_columns(self, *, columns):
        line_no = 0
        result = {}
        # カラムとヘッダの長さは揃っていることが前提
        for header, column in zip(self.headers, columns):
            # カラム単体の変換処理を行う
            result[header] = self.parsed_column(header, column)
        # 行全体の変換処理を行う
        return self.parsed_line(result = result)

    # 分解されたひとつのカラムの処理
    def parsed_column(self, *, column_name, value):
        # stripだけ
        return value.strip()

    # 1行分の処理結果
    def parsed_line(self, *, result):
        # 何もしない
        return result

class TransfomerParameters:

    def __init__(self):
        self.header = False
        self.encoding = 'utf8'
        self.delimiter = ','
        self.raw_colmun_prefix='col_'
        self.option=None
