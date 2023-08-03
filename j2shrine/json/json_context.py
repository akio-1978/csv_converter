from ..context import RenderContext

# renderの動作を決定するコンテキスト


class JsonRenderContext(RenderContext):
    def __init__(self, *, template=None, parameters={}):
        super().__init__(template=template, parameters=parameters)
