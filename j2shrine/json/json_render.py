from ..loader import Loader
import json


class JsonLoader(Loader):

    def execute(self):
        self.processor.execute(self.loading())

    def loading(self):
        with open(self.context.source, encoding=self.context.input_encoding) as f:
            return {'data' : json.load(f)}
