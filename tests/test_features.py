import logging
import json
from six import StringIO
import unittest

from vcardz import \
    get_logger, \
    set_logger, \
    Parser, \
    scrub


class TestFeatures(unittest.TestCase):

    def test_feature_attr(self):
        set_logger(logging.DEBUG)
        logger = get_logger()
        with open('./data/test1.vcf') as stream:
            engine = Parser(stream)
            card = next(engine)
            email = card.email
            for test in email:
                logger.debug(str(test))
                logger.debug(','.join(test.tag.types))

            phone = list(card.phone)
            for test in phone:
                logger.debug(','.join(test.tag.types))


if __name__ == '__main__':
    unittest.main()
