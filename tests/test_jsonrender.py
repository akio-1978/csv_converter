import unittest
from io import StringIO
from j2shrine.json.json_render import JsonRender
from j2shrine.json.json_context import JsonRenderContext


class JsonRenderTest(unittest.TestCase):

    def test_simple_json(self):
        self.file_convert_test(template='tests/json/templates/simple_json.tmpl',
                               expect='tests/json/rendered_file/simple_json.sql',
                               source='tests/json/render_source_file/simple_json.json')

    # def test_group_by(self):
    #     self.file_convert_test(template = 'tests/csv/templates/group_by.tmpl',
    #                             expect = 'tests/csv/rendered_file/group_by.yml',
    #                             source ='tests/csv/render_source_file/group_by.csv')

    # def test_parameters(self):
    #     self.file_convert_test(template = 'tests/csv/templates/options.tmpl',
    #                             expect = 'tests/csv/rendered_file/options.yml',
    #                             source = 'tests/csv/render_source_file/options.csv',
    #                             parameters = {'list_name' : 'Yurakucho-line-stations-in-ward'})

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
