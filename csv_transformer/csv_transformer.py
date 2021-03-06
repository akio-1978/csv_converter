import io
import sys
import argparse
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
            reader = csvreader(csvfile)
            firstline = True
            for columns in reader:
                # ヘッダ設定
                if firstline:
                    self.headers = self.get_headers(parameters = self.parameters, columns = columns)
                    firstline = False
                if self.parameters.header:
                    continue
                lines.append(self.transform_columns(columns = columns))
        print(
            self.template.render(
                {'lines' : lines}
            )
        )

    # 以下はオーバーライドできるようにメソッドを細かく分けた
    # jinja2カスタムテンプレートのインストール
    def install_jinja2_filters(self, *, environment, parameters):
        environment.filters['groups'] = jinja2_filters.groups
        return environment

    def get_headers(self, *, parameters, columns):
        headers = []
        for idx in range[len(columns)]:
            column = column[idx] \
                if parameters.header else parameters.header + parameters.raw_colmun_prefix.zfill(2)
            headers.append(idx).strip()
        return headers

    def get_datasource(self, *, source, input_encoding='utf-8'):
        return open(source, 'r', encoding=input_encoding, newline='')

    # 1行分の分解されたカラムを処理する
    def transform_columns(self, *, columns):
        line_no = 0
        result = {}
        for column in columns:
            header_name = self.column_name(column_no = line_no)
            result[header_name] = self.column(value = column)
            line_no = line_no + 1
        return self.transformed_line(result = result)

    # 分解されたひとつのカラムの処理
    def column(self, *, value, line_no=None, column_name=None):
        # stripだけ
        return value.strip()

    # 1行分の処理結果
    def transformed_line(self, *, result):
        # 今回はそのまま返す
        return result

class TransfomerParameters:

    def __init__(self):
        self.header = False
        self.encoding = 'utf8'
        self.separator = ','
        self.source = None
        self.raw_colmun_prefix='col_'
