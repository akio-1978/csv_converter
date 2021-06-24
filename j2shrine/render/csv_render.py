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
        self.headers = []
        self.skip_lines = 0


class CsvRender(Render):

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        super().__init__(context = context)

    def build_reader(self, *, source):
        # use csv.reader
        return csv.reader(source, delimiter = self.context.delimiter)

    def read_source(self, *, reader):
        lines = []
        for line_no, columns in enumerate(reader):
            # ヘッダ読み込み、ヘッダがない場合は連番をヘッダにする
            if line_no == 0:
                self.headers = self.read_headers(context = self.context, columns = columns)
                # ヘッダとして先頭行を読み込んだ場合
                if self.context.use_header:
                    continue
            
            line = self.columns_to_dict(columns = columns)
            lines.append(line)

        return lines

    # カラムのlistをdictに変換する。dictのキーはself.headers
    def columns_to_dict(self, *, columns):
        line = {}
        # カラムとヘッダの長さは揃っていることが前提
        for header, column in zip(self.headers, columns):
            # カラム単体の変換処理を行う
            line[header] = self.read_column(name = header, column = column)

        print('dict: ', line)
        return line

    def columns_dict(self, *, columns_dict):
        return columns_dict

    def read_headers(self, *, context, columns):
        headers = []
        for idx, column in enumerate(columns):
            header = None
            if context.use_header:
                # column value equal header
                header = column.strip()
            else:
                # make header from formatted column position
                header = context.header_prefix + str(idx).zfill(2)

            headers.append(header)
        print('header: ', headers)
        return headers

    # hook by every column
    def read_column(self, *, name, column):
        return column.strip()

