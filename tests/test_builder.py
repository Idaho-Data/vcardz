import json
from six import StringIO
import unittest

from vcardz_data import builder

class TestBuilder(unittest.TestCase):
    
    def test_builder(self):
        carpenter = builder()
        carpenter.FN('John Doe')
        
        test_card = carpenter.card
        self.assertEqual(str(test_card.fn),'John Doe')

if __name__ == '__main__':
    unittest.main()
