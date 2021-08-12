import unittest
from io import StringIO
from j2shrine.render.csv_render import CsvRender, CsvRenderContext
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
        self.file_convert_test(template = 'tests/csv/templates/simple_json.tmpl',
                                expect = 'tests/csv/rendered_file/simple_json.txt',
                                source = 'tests/csv/render_source_file/simple_json.csv')
    def test_skip_with_header(self):
        self.file_convert_test(template = 'tests/csv/templates/simple_json.tmpl',
                                expect = 'tests/csv/rendered_file/simple_json.txt',
                                source = 'tests/csv/render_source_file/skip_with_header.csv',
                                skip_lines=3)

    def test_skip_with_headerless(self):
        self.file_convert_test(template = 'tests/csv/templates/skip_with_headerless.tmpl',
                                expect = 'tests/csv/rendered_file/simple_json.txt',
                                source = 'tests/csv/render_source_file/skip_with_headerless.csv',
                                skip_lines=3, use_header=False)

    def test_group_by(self):
        self.file_convert_test(template = 'tests/csv/templates/group_by.tmpl',
                                expect = 'tests/csv/rendered_file/group_by.yml',
                                source ='tests/csv/render_source_file/group_by.csv')

    def test_parameters(self):
        self.file_convert_test(template = 'tests/csv/templates/parameters.tmpl',
                                expect = 'tests/csv/rendered_file/parameters.yml',
                                source = 'tests/csv/render_source_file/parameters.csv',
                                parameters = {'list_name' : 'Yurakucho-line-stations-in-ward'})

    def test_headers(self):
        self.file_convert_test(template = 'tests/csv/templates/headers.tmpl',
                                expect = 'tests/csv/rendered_file/headers.txt',
                                source ='tests/csv/render_source_file/simple_json.csv')

    def file_convert_test(self, *, template, expect, source, 
            parameters={}, skip_lines=0, use_header=True, headers=None):
        context = CsvRenderContext(template=template, parameters=parameters)
        # headerの使用有無
        context.use_header = use_header
        context.headers = headers
        # 追加パラメータ
        context.parameters = parameters
        # 行の読み飛ばし
        context.skip_lines = skip_lines

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
        environment = Environment(loader = DictLoader(context.template))
        self.template = environment.get_template(context.template_name)

if __name__ == '__main__':
    unittest.main()
