# renderの動作を決定するコンテキスト
class RenderContext:

    def __init__(self, *, template=None, template_encoding='utf8', parameters={}):
        self.template = template
        self.parameters = parameters
        self.template_encoding = template_encoding

    def set_arguments(self, *, arguments):
        for (key, value) in arguments.items():
            setattr(self, key, value)
        return self
