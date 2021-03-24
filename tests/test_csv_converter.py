import unittest
from io import StringIO
from csv_converter import CsvConverter, ConverterContext,__version__
from jinja2 import Environment, DictLoader

def test_version():
    assert __version__ == '0.1.0'

class CsvConverterTest(unittest.TestCase):

    def test_transforme_headless(self):

        context = ConverterContext(template_source={'template' : "{% for line in lines %}{{line.col_00}}\n{% endfor %}"})
        context.template_name = 'template'
        converter = DictConverter(context = context)

        source = StringIO('A0001,C0002 \n B0001,C0002  \n   C0001,C0002')
        result = StringIO()

        converter.convert(source = source, output = result)

        self.assertEqual('A0001\nB0001\nC0001\n\n', result.getvalue())

    def test_transforme_headered(self):

        context = ConverterContext(template_source={'template' : "{% for line in lines %}{{line.FIRST}}<=>{{line.SECOND}}{% endfor %}"})
        context.template_name = 'template'
        context.use_header = True
        converter = DictConverter(context = context)

        source = StringIO('FIRST, SECOND\n C0001,C0002')
        result = StringIO()

        converter.convert(source = source, output = result)

        self.assertEqual('C0001<=>C0002\n', result.getvalue())

    def test_simple_json(self):
        context = ConverterContext(template_source='tests/templates/simple_json.tmpl')
        context.use_header = True
        converter = CsvConverter(context = context)
        converted = StringIO()

        with open('tests/convert_source_file/simple_json.csv') as source:
            converter.convert(source=source, output=converted)

        with open('tests/converted_file/simple_json.txt') as expect:
            self.assertEqual(expect.read(), converted.getvalue())


# テスト用にDictLoaderを使うTransformer
class DictConverter(CsvConverter):

    def init_template(self, *, context):
        print(context.template_source)
        environment = Environment(loader = DictLoader(context.template_source))
        self.template = environment.get_template(context.template_name)

if __name__ == '__main__':
    unittest.main()
