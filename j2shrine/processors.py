import pathlib
from jinja2 import Environment, FileSystemLoader
from .context import RenderContext
from .jinja2_custom_filter import sequential_group_by
from .excel.excel_custom_filter import excel_time
from .utils import get_stream

class Processor:
    def __init__(self, context:RenderContext) -> None:
        self.context = context
        self._setup()

    def _setup (self):
        pass

    def execute(self, loaded_object):
        pass

class Jinja2Processor(Processor):
    def __init__(self, context:RenderContext) -> None:
        super().__init__(context)
    
    def _setup(self):
        """jinja2テンプレート生成"""
        path = pathlib.Path(self.context.template)
        environment = Environment(loader=FileSystemLoader(
            path.parent, encoding=self.context.template_encoding))
        self._install_filters(environment=environment)
        self.template = environment.get_template(path.name)

    def _install_filters(self, environment):
        """追加のフィルタを設定する"""
        environment.filters['sequential_group_by'] = sequential_group_by
        environment.filters['excel_time'] = excel_time
        
    def execute(self, loaded_object):
        with get_stream(source=self.context.out ,encoding=self.context.output_encoding, mode='w') as dest:
            loaded_object['params'] = self.context.parameters
            dest.write(self.template.render(loaded_object))
