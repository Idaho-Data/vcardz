import logging
import json
from six import StringIO
import unittest

from vcardz import \
    get_logger, \
    set_logger, \
    Parser, \
    scrub


class TestMatch(unittest.TestCase):

    def test_count(self):
        set_logger(logging.DEBUG)
        logger = get_logger()
        with open('./data/test1.vcf') as stream:
            result,subway = scrub(stream, clean_results=True)
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
