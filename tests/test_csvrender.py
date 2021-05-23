import unittest
from io import StringIO
from j2render.render.csv_render import CsvRender, CsvRenderContext
from jinja2 import Environment, DictLoader

class CsvRenderTest(unittest.TestCase):

    def test_convert_headless(self):

        context = CsvRenderContext()
        context.template = {'template' : "{% for line in data %}{{line.col_00}}\n{% endfor %}"}
        context.template_name = 'template'
        converter = DictConverter(context = context)

        source = StringIO('A0001,C0002 \n B0001,C0002  \n   C0001,C0002')
        result = StringIO()

        converter.render(source = source, output = result)

        self.assertEqual('A0001\nB0001\nC0001\n\n', result.getvalue())

    def test_convert_escaped(self):

        context = CsvRenderContext()
        context.template = {'template' : "{% for line in data %}{{line.col_00}}\n{% endfor %}"}
        context.template_name = 'template'
        converter = DictConverter(context = context)

        source = StringIO('"A00,01",C0002 \n B0001,C0002  \n   C0001,C0002')
        result = StringIO()

        converter.render(source = source, output = result)

        self.assertEqual('A00,01\nB0001\nC0001\n\n', result.getvalue())

    def test_convert_headered(self):

        context = CsvRenderContext(template={'template' : "{% for line in data %}{{line.FIRST}}<=>{{line.SECOND}}{% endfor %}"})
        context.template_name = 'template'
        context.use_header = True
        converter = DictConverter(context = context)

        source = StringIO('FIRST, SECOND\n C0001,C0002')
        result = StringIO()

        converter.render(source = source, output = result)

        self.assertEqual('C0001<=>C0002\n', result.getvalue())

    def test_simple_json(self):
        self.file_convert_test(template = 'tests/templates/simple_json.tmpl',
                                expect = 'tests/rendered_file/simple_json.txt',
                                source = 'tests/render_source_file/simple_json.csv')

    def test_group_by(self):
        self.file_convert_test(template = 'tests/templates/group_by.tmpl',
                                expect = 'tests/rendered_file/group_by.yml',
                                source ='tests/render_source_file/group_by.csv')

    def test_parameters(self):
        self.file_convert_test(template = 'tests/templates/options.tmpl',
                                expect = 'tests/rendered_file/options.yml',
                                source = 'tests/render_source_file/options.csv',
                                parameters = {'list_name' : 'Yurakucho-line-stations-in-ward'})


    def file_convert_test(self, *, template, expect, source, parameters={}):
        context = CsvRenderContext(template=template, parameters=parameters)
        context.use_header = True
        context.parameters = parameters
        converter = CsvRender(context = context)
        rendered = StringIO()

        with open(source) as source_reader:
            converter.render(source=source_reader, output=rendered)

        with open(expect) as expect_reader:
            self.assertEqual(expect_reader.read(), rendered.getvalue())
        
        return rendered

# テスト用にDictLoaderを使うTransformer
class DictConverter (CsvRender):

    def build_convert_engine(self, *, context):
        print(context.template)
        environment = Environment(loader = DictLoader(context.template))
        self.template = environment.get_template(context.template_name)

if __name__ == '__main__':
    unittest.main()
