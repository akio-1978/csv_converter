import sys
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader

class CsvTransformer:

    def __init__(self, *, template):
        path = Path(template)
        self.loader_directory = path.parent()
        self.template_file = path.name()
        environment = Environment(loader = FileSystemLoader(self.loader_directory, encoding='utf-8'))
        self.template = environment.get_template(self.template_file)
    
    def execute(self, *, file, encoding='utf-8'):
        lines = []
        with open(file) as source:
            line = source.readline()
            lines.append(line.split(','))
        print(self.template.render({'lines' : lines}))

    def transform_line(self, *, line):
        line = 0
        result = {}
        for token in line:
            result[self.column_name(name = nil, columne_no = line)] = token
        return result

    def column_name(self, *, name = nil, column_no):
        # 'column_01'とかの文字列
        return 'column_' + str(column_no).zfill(2)


if __name__ == '__main__':
    template_file = sys.argv[1]
    format_changer = CsvTransformer(template = template_file)
    format_changer.execute(file = None)