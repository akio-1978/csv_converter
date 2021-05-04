import unittest
from j2render import CsvContextBuilder
import sys

class ArgumentParserTest(unittest.TestCase):
    
    def test_minimum_args(self):
        params = CsvContextBuilder().argument_to_context(['template', 'csv'])
        
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.source)
        self.assertFalse(params.use_header)

    def test_header(self):
        params = CsvContextBuilder().argument_to_context(['template', 'csv', '-H'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.source)
        self.assertTrue(params.use_header)

        params = CsvContextBuilder().argument_to_context(['template', 'csv', '--header'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.source)
        self.assertTrue(params.use_header)

    def test_encoding(self):
        params = CsvContextBuilder().argument_to_context(['template', 'csv'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.source)
        self.assertEqual('utf-8', params.input_encoding)

        params = CsvContextBuilder().argument_to_context(['template', 'csv', '--input-encoding', 'sjis'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.source)
        self.assertEqual('sjis', params.input_encoding)

    def test_key_values_action(self):
        params = CsvContextBuilder().argument_to_context(['template', 'csv', '--parameters', 'A=B', 'C=D'])
        
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.source)
        self.assertFalse(params.use_header)
        self.assertEqual(params.parameters['A'], 'B')
        self.assertEqual(params.parameters['C'], 'D')

    def test_delimiter_comma_action(self):
        params = CsvContextBuilder().argument_to_context(['template', 'csv'])
        
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.source)
        self.assertFalse(params.use_header)
        self.assertEqual(params.delimiter, ',')

    def test_delimiter_tab_action(self):
        params = CsvContextBuilder().argument_to_context(['template', 'csv', '-d' , '\t'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.source)
        self.assertFalse(params.use_header)
        self.assertEqual(params.delimiter, '\t')

        params = CsvContextBuilder().argument_to_context(['template', 'csv', '--delimiter' , '\t'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.source)
        self.assertFalse(params.use_header)
        self.assertEqual(params.delimiter, '\t')

    def test_use_stdin(self):
        params = CsvContextBuilder().argument_to_context(['template'])
        self.assertEqual('template', params.template_source)
        self.assertTrue(sys.stdin is params.source)


if __name__ == '__main__':
    unittest.main()