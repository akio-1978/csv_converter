import sys
from jinja2 import Template, Environment, FileSystemLoader

class FormatChanger:

    def __init__(self, *, template):
        self.template = template
        environment = Environment(loader = FileSystemLoader('./templates', encoding='utf-8'))
        self.jinja_template = environment.get_template(self.template)
    

if __name__ == '__main__':
    template_file = sys.argv[1]
    format_changer = FormatChanger(template = template_file)
    print(template_file, 'ok.')
