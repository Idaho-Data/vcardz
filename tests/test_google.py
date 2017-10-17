import unittest

from vcardz.google import GoogleFeed


class TestGoogleFeed(unittest.TestCase):
    def test_sanity(self):
        feed = """<?xml version="1.0" encoding="UTF-8"?>
<feed gd:etag="&quot;abcdefghijklkmop&quot;" xmlns="http://www.w3.org/2005/Atom" xmlns:batch="http://schemas.google.com/gdata/batch" xmlns:gContact="http://schemas.google.com/contact/2008" xmlns:gd="http://schemas.google.com/g/2005" xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/">
    <id>john.doe@gmail.com</id>
    <updated>2015-01-28T16:09:38.786Z</updated>
    <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
    <title>Josh Watts's Contacts</title>
    <link rel="alternate" type="text/html" href="https://www.google.com/"/>
    <link rel="http://schemas.google.com/g/2005#feed" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/john.doe%40gmail.com/full"/>
    <link rel="http://schemas.google.com/g/2005#post" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/john.doe%40gmail.com/full"/>
    <link rel="http://schemas.google.com/g/2005#batch" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/john.doe%40gmail.com/full/batch"/>
    <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/john.doe%40gmail.com/full?max-results=25"/>
    <link rel="next" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/john.doe%40gmail.com/full?max-results=25&amp;start-index=26"/>
    <author>
        <name>John Doe</name>
        <email>john.doe@gmail.com</email>
    </author>
    <generator version="1.0" uri="http://www.google.com/m8/feeds">Contacts</generator>
    <openSearch:totalResults>25</openSearch:totalResults>
    <openSearch:startIndex>1</openSearch:startIndex>
    <openSearch:itemsPerPage>25</openSearch:itemsPerPage>
    <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
        <id>http://www.google.com/m8/feeds/contacts/john.doe%40gmail.com/base/1</id>
        <updated>2014-01-11T13:42:53.232Z</updated>
        <app:edited xmlns:app="http://www.w3.org/2007/app">2014-01-11T13:42:53.232Z</app:edited>
        <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
        <title>John Doe</title>
        <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/john.doe%40gmail.com/1"/>
        <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/john.doe%40gmail.com/full/1"/>
        <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/john.doe%40gmail.com/full/1"/>
        <gd:name>
            <gd:fullName>John Doe</gd:fullName>
            <gd:givenName>John</gd:givenName>
            <gd:familyName>Doe</gd:familyName>
        </gd:name>
        <gd:email rel="http://schemas.google.com/g/2005#work" address="john.doe@foobar.com" primary="true"/>
        <gd:email rel="http://schemas.google.com/g/2005#home" address="john.doe@gmail.com"/>
        <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-555-1234">2085551234</gd:phoneNumber>
        <gd:phoneNumber rel="http://schemas.google.com/g/2005#home" uri="tel:+1-208-555-6789">208-555-6789</gd:phoneNumber>
    </entry>
</feed>
        """
        google = GoogleFeed(feed)
        card = next(google)
        self.assertEqual(str(card.fn), 'John Doe')


if __name__ == '__main__':
    unittest.main()
