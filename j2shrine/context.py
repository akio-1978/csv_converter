import json
from .render import Render
# renderの動作を決定するコンテキスト
class RenderContext:
    def __init__(self, *, args):
        self.input_encoding = 'utf8'
        self.output_encoding = 'utf8'
        self.template_encoding = 'utf8'
        self.set_params(args=vars(args))

    def set_params(self, *, args):
        for (key, value) in args.items():
            if value is not None:
                setattr(self, key, value)
