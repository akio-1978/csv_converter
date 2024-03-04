from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .jinja2_custom_filter import sequential_group_by

class Render:

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        self.context = context
        self.build_convert_engine(context=context)

    # 別の方法でテンプレートを生成する場合はオーバーライドする
    def build_convert_engine(self, *, context):
        path = Path(context.template)
        environment = Environment(loader=FileSystemLoader(
            path.parent, encoding=context.template_encoding))
        self.install_filters(environment=environment)
        self.template = environment.get_template(path.name)

    def install_filters(self, *, environment):
        environment.filters['sequential_group_by'] = sequential_group_by

    def build_reader(self, *, source):
        return source

    def render(self, *, source, output):
        reader = self.build_reader(source=source)
        result = self.read_source(reader=reader)
        final_result = self.finish(result=result)
        self.output(final_result=final_result, output=output)

    def read_source(self, *, reader):
        print('src:', reader)
        return reader

    def finish(self, *, result):
        final_result = {
            'data': result,
            'params': self.context.parameters
        }
        return final_result

    def output(self, *, final_result, output):
        print(
            self.template.render(final_result),
            file=output
        )

    # カラム名取得
    # cols属性がないとこのメソッドは動かない
    def column_name(self, index):
        if len(self.cols) <= index:
            # カラム名が定義されていない場合
            # または定義済みのカラム名よりも実際のカラムが多い場合はカラム名を追加で生成する
            self.cols.append(self.context.prefix + str(index).zfill(2))
        return self.cols[index]
