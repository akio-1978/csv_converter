import unittest
from io import StringIO
from text_converter import CsvConverter, CsvConverterContext,__version__
from jinja2 import Environment, DictLoader

def test_version():
    assert __version__ == '0.1.0'

class CsvConverterTest(unittest.TestCase):

    def test_convert_headless(self):

        context = CsvConverterContext(template_source={'template' : "{% for line in data %}{{line.col_00}}\n{% endfor %}"})
        context.template_name = 'template'
        converter = DictConverter(context = context)

        source = StringIO('A0001,C0002 \n B0001,C0002  \n   C0001,C0002')
        result = StringIO()

        converter.convert(source = source, output = result)

        self.assertEqual('A0001\nB0001\nC0001\n\n', result.getvalue())

    def test_convert_escaped(self):

        context = CsvConverterContext(template_source={'template' : "{% for line in data %}{{line.col_00}}\n{% endfor %}"})
        context.template_name = 'template'
        converter = DictConverter(context = context)

        source = StringIO('"A00,01",C0002 \n B0001,C0002  \n   C0001,C0002')
        result = StringIO()

        converter.convert(source = source, output = result)

        self.assertEqual('A00,01\nB0001\nC0001\n\n', result.getvalue())

    def test_convert_headered(self):

        context = CsvConverterContext(template_source={'template' : "{% for line in data %}{{line.FIRST}}<=>{{line.SECOND}}{% endfor %}"})
        context.template_name = 'template'
        context.use_header = True
        converter = DictConverter(context = context)

        source = StringIO('FIRST, SECOND\n C0001,C0002')
        result = StringIO()

        converter.convert(source = source, output = result)

        self.assertEqual('C0001<=>C0002\n', result.getvalue())

    def test_simple_json(self):
        self.file_convert_test(template = 'tests/templates/simple_json.tmpl',
                                expect = 'tests/converted_file/simple_json.txt',
                                source = 'tests/convert_source_file/simple_json.csv')

    def test_group_by(self):
        self.file_convert_test(template = 'tests/templates/group_by.tmpl',
                                expect = 'tests/converted_file/group_by.yml',
                                source ='tests/convert_source_file/group_by.csv')

    def test_options(self):
        self.file_convert_test(template = 'tests/templates/group_by.tmpl',
                                expect = 'tests/converted_file/group_by.yml',
                                source = 'tests/convert_source_file/group_by.csv',
                                options = {'list_name' : 'Yurakucho-line-stations-in-ward'})


    def file_convert_test(self, *, template, expect, source, options={}):
        context = CsvConverterContext(template_source=template)
        context.use_header = True
        context.options = options
        converter = CsvConverter(context = context)
        converted = StringIO()

        with open(source) as source_reader:
            converter.convert(source=source_reader, output=converted)

        with open(expect) as expect_reader:
            self.assertEqual(expect_reader.read(), converted.getvalue())

# テスト用にDictLoaderを使うTransformer
class DictConverter(CsvConverter):

    def build_convert_engine(self, *, context):
        print(context.template_source)
        environment = Environment(loader = DictLoader(context.template_source))
        self.template = environment.get_template(context.template_name)

if __name__ == '__main__':
    unittest.main()
