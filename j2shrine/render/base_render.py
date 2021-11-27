from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from . jinja2_custom_filter import sequential_groupby

# renderの動作を決定するコンテキスト
class RenderContext:

    def __init__(self, *, template=None, template_encoding='utf8', parameters={}):
        self.template = template
        self.parameters = parameters
        self.template_encoding = template_encoding

class Render:

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        self.context = context
        self.build_convert_engine(context = context)

    # 別の方法でテンプレートを生成する場合はオーバーライドする
    def build_convert_engine(self, *, context):
        path = Path(context.template)
        environment = Environment(loader = FileSystemLoader(path.parent, encoding=context.template_encoding))
        self.install_filters(environment=environment)
        self.template = environment.get_template(path.name)

    def install_filters(self, *, environment):
        environment.filters['sequential_groupby'] = sequential_groupby

    def build_reader(self, *, source):
        return source

    def render(self, *, source, output):
        reader = self.build_reader(source = source)
        result = self.read_source(reader = reader)
        final_result = self.finish(result = result)
        self.output(final_result=final_result, output=output)

    def read_source(self, *, reader):
        print('src:', reader)
        return reader
    
    def finish(self, *, result):
        final_result = {
            'data' : result,
            'params' : self.context.parameters
        }
        return final_result

    def output(self, *, final_result, output):
        print(
            self.template.render(final_result),
            file = output
        )

