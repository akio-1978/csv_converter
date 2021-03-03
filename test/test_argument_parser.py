import unittest
from csvtransformer import TransformArgumentParser, TransfomerParameters


class ArgumentParserTest(unittest.TestCase):
    
    def test_minimum_args(self):
        params = TransformArgumentParser().parse_parameters(['template', 'csv'])
        
        self.assertEqual('template', params.template)
        self.assertEqual('csv', params.csv)
        
if __name__ == '__main__':
    unittest.main()