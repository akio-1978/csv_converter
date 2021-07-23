from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from . jinja2_custom_filter import sequential_group_by

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
        environment.filters['sequential_group_by'] = sequential_group_by
        self.template = environment.get_template(path.name)

    def build_reader(self, *, source):
        return source

    def render(self, *, source, output):
        reader = self.build_reader(source = source)
        result = self.read_source(reader = reader)
        result = self.read_finish(source_data = result)
        self.result(result = result, output = output)

    def read_source(self, *, reader):
        return reader
    
    def result(self, *, result, output):

        if (isinstance(result, dict)) and (not 'parameters' in result):
            result['parameters'] = self.context.parameters

        self.output(result=result, output=output)

    def output(self, *, result, output):
        print(result)
        print(
            self.template.render(
                result
            ),
            file = output
        )

    # 全て読み込みが終わった後に変換が必要な場合の処理
    def read_finish(self, *, source_data):
        # 何もしない
        return source_data

