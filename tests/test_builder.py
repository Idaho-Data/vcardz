import unittest

from vcardz import Builder


class TestBuilder(unittest.TestCase):

    def test_builder(self):
        carpenter = Builder()
        carpenter.FN('John Doe')

        test_card = carpenter.card
        self.assertEqual(str(test_card.fn), 'John Doe')

if __name__ == '__main__':
    unittest.main()
