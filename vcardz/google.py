from six import StringIO

import xml.etree.ElementTree as ET

from .builder import (Builder, Builder2)
from .outlook import OutlookCSV
from .utils import smash


class GoogleFeed():
    feed = None
    root = None
    entries = None

    def __init__(self, feed):
        self.feed = feed
        # http://stackoverflow.com/questions/13412496/python-elementtree-module-how-to-ignore-the-namespace-of-xml-files-to-locate-ma
        it = ET.iterparse(StringIO(self.feed))
        for _, el in it:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
        self.root = it.root
        self.entries = self.root.iter('entry')

    def __iter__(self):
        return self

    def __next__(self):
        entry = next(self.entries)
        builder = Builder2()

        def check(path):
            node = entry
            for step in path:
                node = node.find(step)
                if node is None:
                    break
            if node is None:
                return ''
            else:
                return node.text

        def children(path):
            node = entry.findall(path)
            return node if node is not None else iter(())

        builder.FN(check(('name', 'fullName')))
        builder.N(family=check(('name', 'familyName')),
                  given=check(('name', 'givenName')),
                  additional=check(('name', 'additionalName')))

        for email in children('email'):
            type = email.attrib['rel'].split('#', 1)[1]
            builder.EMAIL(email.attrib['address'], type)

        for phone in children('phoneNumber'):
            type = phone.attrib['rel'].split('#', 1)[1]
            builder.TEL(phone.text, type)

        return builder.card


class GoogleCSV(OutlookCSV):

    def next(self):
        self.row = next(self.reader)
        builder = Builder()

        builder.FN(self.row['Name'])
        builder.N([self.row['Family Name'],
                   self.row['Given Name'],
                   self.row['Additional Name'],
                   self.row['Name Prefix'],
                   self.row['Name Suffix']])

        builder.TEL(self.row['Phone 1 - Value'],
                    smash(self.row['Phone 1 - Type'], ','))
        builder.TEL(self.row['Phone 2 - Value'],
                    smash(self.row['Phone 2 - Type'], ','))
        builder.TEL(self.row['Phone 3 - Value'],
                    smash(self.row['Phone 3 - Type'], ','))

        builder.EMAIL(self.row['E-mail 1 - Value'],
                      smash(self.row['E-mail 1 - Type'], ','))
        builder.EMAIL(self.row['E-mail 2 - Value'],
                      smash(self.row['E-mail 2 - Type'], ','))
        builder.EMAIL(self.row['E-mail 3 - Value'],
                      smash(self.row['E-mail 3 - Type'], ','))

        builder.ADR([self.row['Address 1 - PO Box'],
                     '',
                     self.row['Address 1 - Street'],
                     self.row['Address 1 - City'],
                     self.row['Address 1 - Region'],
                     self.row['Address 1 - Postal Code'],
                     self.row['Address 1 - Country']],
                    smash(self.row['Address 1 - Type'], ','))
        builder.ADR([self.row['Address 2 - PO Box'],
                     '',
                     self.row['Address 2 - Street'],
                     self.row['Address 2 - City'],
                     self.row['Address 2 - Region'],
                     self.row['Address 2 - Postal Code'],
                     self.row['Address 2 - Country']],
                    smash(self.row['Address 2 - Type'], ','))
        builder.URL(self.row['Website 1 - Value'])
        builder.NOTE(self.row['Notes'])
        builder.BDAY(self.row['Birthday'])
        builder.ORG(self.row['Organization 1 - Name'])
        builder.ROLE(self.row['Organization 1 - Title'])

        return str(builder.card)


# class GoogleOAuth2():
#     credentials = None
#     client = None

#     def __init__(self):
#         storage = Storage('moderator.dat')
#         credentials = storage.get()

#         if credentials is None or credentials.invalid == True:
#             flow = OAuth2WebServerFlow(
#                 client_id = '920736374014-ad9f6ar07gr8cd90uqoi2esjiead09jl.apps.googleusercontent.com',
#                 client_secret = 'CflWzr36BxmMudL0tQSnTC5n',
#                 scope = 'https://www.google.com/m8/feeds https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
#                 user_agent = 'kontexa/1.0')
#             credentials = run(flow, storage)
#         self.credentials = credentials

#         token = gdata.gauth.OAuth2Token(client_id = self.credentials.client_id,
#                                         client_secret = self.credentials.client_secret,
#                                         scope = 'https://www.google.com/m8/feeds https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
#                                         access_token = self.credentials.access_token,
#                                         refresh_token = self.credentials.refresh_token,
#                                         user_agent = self.credentials.user_agent)
#         self.client = token.authorize(gdata.contacts.client.ContactsClient())

#     @staticmethod
#     def vcard_from_entry(entry):
#         builder = Builder()
#         if entry.name:
#             builder.FN(entry.name.full_name.text if entry.name.full_name else '')
#             builder.N([entry.name.family_name.text if entry.name.family_name else '',
#                        entry.name.given_name.text if entry.name.given_name else '',
#                        entry.name.additional_name.text if entry.name.additional_name else '',
#                        entry.name.name_prefix.text if entry.name.name_prefix else '',
#                        entry.name.name_suffix.text if entry.name.name_suffix else ''])

#         for phone in entry.phone_number:
#             phone_type = phone.rel.split('#')[1] if phone.rel else ''
#             builder.TEL(phone.text, phone_type)

#         for email in entry.email:
#             email_type = email.rel.split('#')[1] if email.rel else ''
#             builder.EMAIL(email.address, email_type)

#         for adr in entry.structured_postal_address:
#             builder.ADR([adr.po_box.text if adr.po_box else '',
#                          '',
#                          adr.street.text if adr.street else '',
#                          adr.city.text if adr.city else '',
#                          adr.region.text if adr.region else '',
#                          adr.postcode.text if adr.postcode else '',
#                          adr.country.text if adr.country else ''],
#                         '')

#         builder.NOTE(entry.content.text if entry.content else '')
#         if entry.organization:
#             builder.ORG(entry.organization.name.text if entry.organization.name else '')
#             builder.ROLE(entry.organization.title.text if entry.organization.title else '')

#         builder.UID(entry.GetEditLink().href)
#         return builder.card

#     def get_entry(self, url):
#         return self.client.GetContact(url)


#     def update_entry(self, entry):
#         return self.client.Update(entry)

#     def delete_entry(self, entry):
#         return self.client.Delete(entry)
    
#     @staticmethod
#     def get_rel(vals):
#         rel_vals = {'work': gdata.data.WORK_REL,
#                     'fax': gdata.data.FAX_REL,
#                     'fax_work': gdata.data.WORK_FAX_REL,
#                     'home': gdata.data.HOME_REL,
#                     'fax_home': gdata.data.HOME_FAX_REL,
#                     'mobile': gdata.data.MOBILE_REL,
#                     'cell': gdata.data.MOBILE_REL,
#                     'other': gdata.data.OTHER_REL}

#         tokens = list(filter((lambda x: x if x.lower() != "internet" else None), vals))
#         if 0 == len(tokens):
#             return gdata.data.OTHER_REL

#         tokens.sort()
#         return rel_vals['_'.join(tokens)]
        

#     def get_stream(self):
#         buff = StringIO.StringIO()
#         # token = gdata.gauth.OAuth2Token(client_id = self.credentials.client_id,
#         #                         client_secret = self.credentials.client_secret,
#         #                         scope = 'https://www.google.com/m8/feeds https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
#         #                         access_token = self.credentials.access_token,
#         #                         refresh_token = self.credentials.refresh_token,
#         #                         user_agent = self.credentials.user_agent)
#         # contacts = token.authorize(gdata.contacts.client.ContactsClient())
#         i = 1
#         while True:
#             query = gdata.contacts.client.ContactsQuery()
#             query.max_results = 100
#             query.start_index = i

#             feed = self.client.GetContacts(q = query)
#             if not feed.entry:
#                 break
#             else:
#                 entries = iter(feed.entry)
#                 for entry in entries:
#                     i += 1
#                     buff.write(GoogleOAuth2.vcard_from_entry(entry))

#         buff.seek(0)
#         return buff

