from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .jinja2_custom_filter import sequential_group_by

class Render:

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        self.context = context
        self.setup_template(context=context)
        # カラム名prefix
        self.col_prefix='col_'

    def setup_template(self, *, context):
        """jinja2テンプレート生成"""
        path = Path(context.template)
        environment = Environment(loader=FileSystemLoader(
            path.parent, encoding=context.template_encoding))
        self.install_filters(environment=environment)
        self.template = environment.get_template(path.name)

    def install_filters(self, *, environment):
        """追加のフィルタを設定する"""
        environment.filters['sequential_group_by'] = sequential_group_by

    def get_source_reader(self, *, source):
        return source

    def render(self, *, source, output):
        reader = self.get_source_reader(source=source)
        result = self.read_source(reader=reader)
        final_result = self.read_finish(result=result)
        self.output_template(final_result=final_result, output=output)

    def read_source(self, *, reader):
        return reader

    def read_finish(self, *, result):
        final_result = {
            'data': result,
            'params': self.context.parameters
        }
        return final_result

    def output_template(self, *, final_result, output):
        print(
            self.template.render(final_result),
            file=output
        )

    # カラム名取得
    # cols属性がないとこのメソッドは動かない
    def get_name(self, index):
        if len(self.cols) <= index:
            # カラム名が定義されていない場合
            # または定義済みのカラム名よりも実際のカラムが多い場合はカラム名を追加で生成する
            self.cols.append(self.col_prefix + str(index).zfill(2))
        return self.cols[index]
