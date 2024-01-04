from ..context import RenderContext
from .json_render import JsonRender

# renderの動作を決定するコンテキスト


class JsonRenderContext(RenderContext):
    def __init__(self, *, args):
        super().__init__(args=args)

    def get_render(self):
        return JsonRender(context=self)
