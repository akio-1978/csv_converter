import unittest


class OtherTest(unittest.TestCase):

    def test_split(self):
        try:
            (a, b,) = 'cantaplit'.split(':')
        except ValueError:
            pass

        splitted = 'cantaplit'.split(':')
        self.assertEqual(1, len(splitted))

    def test_partition(self):
        values = 'A-Z'.partition('-')
        self.assertEqual(3, len(values))
        self.assertEqual('A', values[0])
        self.assertEqual('-', values[1])
        self.assertEqual('Z', values[2])

        values = 'A-'.partition('-')
        self.assertEqual(3, len(values))
        self.assertEqual('A', values[0])
        self.assertEqual('-', values[1])
        self.assertEqual('', values[2])
        
        values = 'A'.partition('-')
        self.assertEqual(3, len(values))
        self.assertEqual('A', values[0])
        self.assertEqual('', values[1])
        self.assertEqual('', values[2])


if __name__ == '__main__':
    unittest.main()
