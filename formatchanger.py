from jinja2 import Template, Environment, FileSystemLoader

class FormatChanger:

    def __init__(self, *, template):
        self.template = template
    
