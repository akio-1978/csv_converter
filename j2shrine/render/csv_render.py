import csv
from . base_render import Render, RenderContext

# transformerに渡すパラメータクラス
class CsvRenderContext(RenderContext):
    def __init__(self, *, template=None, template_encoding='utf8', parameters={}):
        super().__init__(template=template, template_encoding=template_encoding, parameters=parameters)
        self.use_header = False
        self.encoding = 'utf8'
        self.delimiter = ','
        self.header_prefix='col_'
        self.skip_lines = 0


class CsvRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        super().__init__(context = context)
        self.headers = None

    def build_reader(self, *, source):
        # use csv.reader
        return csv.reader(source, delimiter = self.context.delimiter)

    def read_source(self, *, reader):
        lines = []

        # スキップ指定があれば行を読み飛ばす
        # ヘッダ行の処理は読み飛ばし後から始める
        for n in range(self.context.skip_lines):
            next(reader)

        if self.context.use_header:
            self.headers = self.read_headers(columns= next(reader))

        for line_no, columns in enumerate(reader):
            # ヘッダ読み込み、ヘッダがない場合は連番をヘッダにする
            if self.headers is None:
                self.headers = self.create_headers(context = self.context, columns = columns)

            print('read_records.')
            line = self.columns_to_dict(columns = columns)
            lines.append(line)

        return lines

    def finish(self, *, result):
        final_result = {
            'data' : result,
            'headers' : self.headers,
            'params' : self.context.parameters
        }
        return final_result

    # カラムのlistをdictに変換する。dictのキーはself.headers
    def columns_to_dict(self, *, columns):
        line = {}
        # カラムとヘッダの長さは揃っていることが前提
        for header, column in zip(self.headers, columns):
            # カラム単体の変換処理を行う
            line[header] = self.read_column(name = header, column = column)

        return line

    def columns_dict(self, *, columns_dict):
        return columns_dict

    def read_headers(self, *, columns):
        headers = []
        for column in columns:
            headers.append(column.strip())
        return headers


    def create_headers(self, *, context, columns):
        headers = []
        for idx, column in enumerate(columns):
            # make header from line length
            headers.append(context.header_prefix + str(idx).zfill(2))
        return headers

    # hook by every column
    def read_column(self, *, name, column):
        return column.strip()

