import unittest
from io import StringIO
from csv_transformer import TransfomerParameters
from csv_transformer import CsvTransformer
from csv_transformer import __version__
from jinja2 import Environment, DictLoader

def test_version():
    assert __version__ == '0.1.0'

class CsvTransformerTest(unittest.TestCase):

    def test_transforme_headless(self):

        parameters = TransfomerParameters(template_source={'template' : "{% for line in lines %}{{line.col_00}}\n{% endfor %}"})
        parameters.template_name = 'template'
        transformer = DictTransformer(parameters = parameters)

        source = StringIO('A0001,C0002 \n B0001,C0002  \n   C0001,C0002')
        result = StringIO()

        transformer.transform(source = source, output = result)

        self.assertEqual('A0001\nB0001\nC0001\n\n', result.getvalue())

    def test_transforme_headered(self):

        parameters = TransfomerParameters(template_source={'template' : "{% for line in lines %}{{line.FIRST}}<=>{{line.SECOND}}{% endfor %}"})
        parameters.template_name = 'template'
        parameters.header = True
        transformer = DictTransformer(parameters = parameters)

        source = StringIO('FIRST, SECOND\n C0001,C0002')
        result = StringIO()

        transformer.transform(source = source, output = result)

        self.assertEqual('C0001<=>C0002\n', result.getvalue())

    def test_simple_json(self):
        parameters = TransfomerParameters(template_source='tests/templates/simple_json.tmpl')
        parameters.header = True
        transformer = CsvTransformer(parameters = parameters)
        transformed = StringIO()

        with open('tests/transform_file/simple_json.csv') as source:
            transformer.transform(source=source, output=transformed)

        with open('tests/transformed_file/simple_json.txt') as expect:
            self.assertEqual(expect.read(), transformed.getvalue())


# テスト用にDictLoaderを使うTransformer
class DictTransformer(CsvTransformer):

    def init_template(self, *, parameters):
        print(parameters.template_source)
        environment = Environment(loader = DictLoader(parameters.template_source))
        self.template = environment.get_template(parameters.template_name)

if __name__ == '__main__':
    unittest.main()
