from .render import Render
# renderの動作を決定するコンテキスト
class RenderContext:
    def __init__(self, *, args):
        self.set_params(args=vars(args))

    def set_params(self, *, args):
        for (key, value) in args.items():
            setattr(self, key, value)

    def get_render(self):
        return Render(self)
