class RenderContext:

    def __init__(self, *, template_source, parameters={}):
        self.template_source = template_source
        self.parameters = parameters
