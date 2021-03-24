import unittest
from csv_converter import ContextBuilder


class ArgumentParserTest(unittest.TestCase):
    
    def test_minimum_args(self):
        params = ContextBuilder().argument_to_context(['template', 'csv'])
        
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.csv)
        self.assertFalse(params.use_header)

    def test_header(self):
        params = ContextBuilder().argument_to_context(['template', 'csv', '-H'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.csv)
        self.assertTrue(params.use_header)

        params = ContextBuilder().argument_to_context(['template', 'csv', '--header'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.csv)
        self.assertTrue(params.use_header)

    def test_encoding(self):
        params = ContextBuilder().argument_to_context(['template', 'csv'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.csv)
        self.assertEqual('utf-8', params.input_encoding)

        params = ContextBuilder().argument_to_context(['template', 'csv', '--input-encoding', 'sjis'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.csv)
        self.assertEqual('sjis', params.input_encoding)

    def test_key_values_action(self):
        params = ContextBuilder().argument_to_context(['template', 'csv', 'A=B', 'C=D'])
        
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.csv)
        self.assertFalse(params.use_header)
        self.assertEqual(params.options['A'], 'B')
        self.assertEqual(params.options['C'], 'D')

    def test_delimiter_comma_action(self):
        params = ContextBuilder().argument_to_context(['template', 'csv', 'A=B'])
        
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.csv)
        self.assertFalse(params.use_header)
        self.assertEqual(params.delimiter, ',')

    def test_delimiter_tab_action(self):
        params = ContextBuilder().argument_to_context(['template', 'csv', '-T' , 'A=B'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.csv)
        self.assertFalse(params.use_header)
        self.assertEqual(params.delimiter, '\t')

        params = ContextBuilder().argument_to_context(['template', 'csv', '--tab' , 'A=B'])
        self.assertEqual('template', params.template_source)
        self.assertEqual('csv', params.csv)
        self.assertFalse(params.use_header)
        self.assertEqual(params.delimiter, '\t')

if __name__ == '__main__':
    unittest.main()