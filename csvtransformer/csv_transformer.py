import io
import sys
import argparse
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader
from csv import reader as csvreader

class CsvTransformer:

    # jinja2テンプレートの生成
    def __init__(self, *, parameters):
        self.parameters = parameters
        self.init_template(template_source=parameters)

    # オーバーライドすると、ファイル名指定以外の方法でテンプレートを取得できる
    def init_template(self, *, parameters):
        path = Path(parameters.source)
        environment = Environment(loader = FileSystemLoader(path.parent, encoding='utf-8'))
        self.template = environment.get_template(path.name)

    # CSVファイルの各行にテンプレートを適用して、出力する
    def transform(self, *, source, output):
        lines = []
        with open(source, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csvreader(csvfile)
            firstline = True
            for columns in reader:
                # ヘッダ設定
                if self.parameters.header and firstline:
                    firstline = False
                    continue
                lines.append(self.transform_columns(columns = columns))
        print(
            self.template.render(
                {'lines' : lines}
            )
        )

    # 以下はオーバーライドできるようにメソッドを細かく分けた

    # 1行分の分解されたカラムを処理する
    def transform_columns(self, *, columns):
        line_no = 0
        result = {}
        for column in columns:
            column_name = self.column_name(column_no = line_no)
            result[column_name] = self.column(token = column)
            line_no = line_no + 1
        return self.transformed_line(result = result)

    # CSVのカラムに名前を付ける
    # このカラム名がテンプレートから参照される
    def column_name(self, *, column_no):
        # 'column_01'とかの文字列
        return 'column_' + str(column_no).zfill(2)

    # 分解されたひとつのカラムの処理
    def column(self, *, token, line_no=None, column_name=None):
        # stripだけ
        return token.strip()

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
