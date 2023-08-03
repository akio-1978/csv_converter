from ..context import RenderContext

# transformerに渡すパラメータクラス


class CsvRenderContext(RenderContext):
    def __init__(self, *, template=None, template_encoding='utf8', parameters=None):
        super().__init__(template=template,
                         template_encoding=template_encoding, parameters=parameters)
        self.read_header = False
        self.encoding = 'utf8'
        self.delimiter = ','
        self.header_prefix = 'col_'
        self.skip_lines = 0
