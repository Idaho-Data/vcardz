import json
from six import StringIO
import unittest

from vcardz import Parser


card = """
BEGIN:VCARD
VERSION:3.0
N:Doe;John;;;
FN:John Doe
ORG:Example.com Inc.;
TITLE:Imaginary test person
EMAIL;type=INTERNET;type=WORK;type=pref:johnDoe@example.org
TEL;type=WORK;type=pref:+1 617 555 1212
TEL;type=WORK:+1 (617) 555-1234
TEL;type=CELL:+1 781 555 1212
TEL;type=HOME:+1 202 555 1212
item1.ADR;type=WORK:;;2 Enterprise Avenue;Worktown;NY;01111;USA
item1.X-ABADR:us
item2.ADR;type=HOME;type=pref:;;3 Acacia Avenue;Hoemtown;MA;02222;USA
item2.X-ABADR:us
NOTE:John Doe has a long and varied history\, being documented on more police files that anyone else. Reports of his death are alas numerous.
item3.URL;type=pref:http\://www.example.com/doe
item3.X-ABLabel:_$!<HomePage>!$_
item4.URL:http\://www.example.com/Joe/foaf.df
item4.X-ABLabel:FOAF
item5.X-ABRELATEDNAMES;type=pref:Jane Doe
item5.X-ABLabel:_$!<Friend>!$_
CATEGORIES:Work,Test group
X-ABUID:5AD380FD-B2DE-4261-BA99-DE1D1DB52FBE\:ABPerson
END:VCARD
"""


class TestVcard(unittest.TestCase):

    def test_sanity(self):
        stream = StringIO(card)
        engine = Parser(stream)
        test_card = next(engine)

        self.assertEqual(str(test_card.fn), 'John Doe')
        self.assertEqual(str(test_card.n), 'Doe;John;;;')
        self.assertEqual(str(test_card.org), 'Example.com Inc.;')

        temp_emails = [str(x) for x in test_card.email]
        self.assertIn('johndoe@example.org', temp_emails)

        temp_tel = [str(x) for x in test_card.phone]
        self.assertIn('617-555-1234', temp_tel)
        self.assertIn('781-555-1212', temp_tel)
        self.assertIn('202-555-1212', temp_tel)
        self.assertIn('617-555-1212', temp_tel)

        temp_adr = [str(x) for x in test_card.adr]
        self.assertIn(';;3 Acacia Avenue;Hoemtown;MA;02222;USA', temp_adr)
        self.assertIn(';;2 Enterprise Avenue;Worktown;NY;01111;USA', temp_adr)

    def test_json(self):
        stream = StringIO(card)
        engine = Parser(stream)
        test_card = next(engine)

        json_payload = test_card.to_json()
        payload = json.loads(json_payload)
        self.assertEqual(payload['fn']['val'], 'John Doe')
        self.assertEqual(payload['n']['val'], 'Doe;John;;;')
        self.assertEqual(payload['org']['val'], 'Example.com Inc.;')

        temp_emails = [x['val'] for x in payload['email']]
        self.assertIn('johndoe@example.org', temp_emails)

        temp_tel = [x['val'] for x in payload['phone']]
        self.assertIn('617-555-1234', temp_tel)
        self.assertIn('781-555-1212', temp_tel)
        self.assertIn('202-555-1212', temp_tel)
        self.assertIn('617-555-1212', temp_tel)

        temp_adr = [';'.join(x['val']) for x in payload['adr']]
        self.assertIn(';;3 Acacia Avenue;Hoemtown;MA;02222;USA', temp_adr)
        self.assertIn(';;2 Enterprise Avenue;Worktown;NY;01111;USA', temp_adr)


if __name__ == '__main__':
    unittest.main()
