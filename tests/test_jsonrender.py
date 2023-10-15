import unittest
from io import StringIO
from j2shrine.json.json_render import JsonRender
from j2shrine.json.json_context import JsonRenderContext


class JsonRenderTest(unittest.TestCase):

    def test_simple_json(self):
        self.file_convert_test(template='tests/json/templates/simple_json.tmpl',
                               source='tests/json/src/simple_json.json',
                               expect='tests/json/expect/simple_json.sql',
                               )

    def file_convert_test(self, *, template, expect, source, parameters={}):
        context = JsonRenderContext(template=template, parameters=parameters)
        context.use_header = True
        context.parameters = parameters
        converter = JsonRender(context=context)
        rendered = StringIO()

        with open(source) as source_reader:
            converter.render(source=source_reader, output=rendered)

        with open(expect) as expect_reader:
            print(rendered.getvalue())
            self.assertEqual(expect_reader.read(), rendered.getvalue())

        return rendered


if __name__ == '__main__':
    unittest.main()
