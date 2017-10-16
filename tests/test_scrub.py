import logging
import json
from six import StringIO
import unittest

from vcardz import \
    get_logger, \
    set_logger, \
    Parser, \
    scrub


class TestScrub(unittest.TestCase):

    def run_scrub(self, data):
        logger = get_logger()
        with open(data) as stream:
            logger.warning('file => %s', data)
            engine = Parser(stream)
            count = 0
            for card in engine:
                count += 1
            logger.warning('raw count => %d', count)
            stream.seek(0)
            result,subway = scrub(stream, clean_results=True)
            logger.warning('scrub count => %d', len(result))    

    def test_scrub_1(self):
        self.run_scrub('./data/test1.vcf')


    def test_name_nonmatches(self):
        self.run_scrub('./data/test2.vcf')


if __name__ == '__main__':
    set_logger(logging.WARNING)
    unittest.main()
