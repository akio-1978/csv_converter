import unittest
from io import StringIO
from j2shrine.json.json_render import JsonRender
from j2shrine.json.json_context import JsonRenderContext
from tests.utils import rendering_test


class JsonRenderTest(unittest.TestCase):

    def test_simple_json(self):
        self.file_convert_test(template='tests/json/templates/simple_json.tmpl',
                               source='tests/json/src/simple_json.json',
                               expect='tests/json/expect/simple_json.sql',
                               )

    def file_convert_test(self, *, template, expect, source, parameters={}):
        context = JsonRenderContext(template=template, parameters=parameters)
        context.parameters = parameters
        converter = JsonRender(context=context)

        return rendering_test(ut=self, render=converter, expect_file=expect, source=source)


if __name__ == '__main__':
    unittest.main()
