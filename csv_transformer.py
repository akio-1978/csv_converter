import io
import sys
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader

class CsvTransformer:

    def __init__(self, *, template):
        path = Path(template)
        self.loader_directory = path.parent
        self.template_file = path.name
        environment = Environment(loader = FileSystemLoader(self.loader_directory, encoding='utf-8'))
        self.template = environment.get_template(self.template_file)

    def transform(self, *, file):
        lines = []
        with open(file, 'r', encoding='utf-8') as source:
            for line in source:
                lines.append(self.transform_columns(columns = self.parse_tokens(line = line)))
        print(
            self.template.render(
                {'lines' : lines}
            )
        )

    def column_name(self, *, column_no):
        # 'column_01'とかの文字列
        return 'column_' + str(column_no).zfill(2)

    def parse_tokens(self, *, line):
        return line.split(',')

    def transform_columns(self, *, columns):
        line_no = 0
        result = {}
        for column in columns:
            column_name = self.column_name(column_no = line_no)
            result[column_name] = self.column(token = column)
            line_no = line_no + 1
        return result

    def column(self, *, token, line_no=None, column_name=None):
        return token.strip()


if __name__ == '__main__':
    # windows対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    template_file = sys.argv[1]
    format_changer = CsvTransformer(template = template_file)
    format_changer.transform(file = sys.argv[2])
