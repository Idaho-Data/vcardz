import csv
from six import StringIO

from .builder import Builder


class OutlookCSV:
    """
    Parser
    """
    stream = None
    reader = None
    card = None
    row = None

    def __init__(self, stream):
        self.stream = stream

    def fix_stream(self):
        buff = StringIO.StringIO()
        writer = csv.writer(buff,
                            dialect='excel',
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_ALL)
        dialect = csv.Sniffer().sniff(self.stream.read(2048))
        print("**%s**" % dialect.delimiter)
        self.stream.seek(0)
        reader = csv.reader(self.stream,
                            dialect)
        for row in reader:
            fixed = []
            for field in row:
                fixed.append(field.replace('\n', ' ').encode('utf-8'))
            writer.writerow(fixed)
        buff.seek(0)
        self.stream = buff
        self.reader = csv.DictReader(self.stream,
                                     dialect='excel',
                                     delimiter=',',
                                     quotechar='"',
                                     quoting=csv.QUOTE_ALL)
        self.fields = self.reader.fieldnames

    def __iter__(self):
        return self

    def next(self):
        self.row = next(self.reader)
        builder = Builder()
        builder.N([self.row['Last Name'],
                   self.row['First Name'],
                   self.row['Middle Name'],
                   "",
                   self.row['Suffix']])
        builder.FN(' '.join([self.row['First Name'],
                             self.row['Last Name']]))
        for phone in (self.row['Business Phone'],
                      self.row['Business Phone 2']):
            builder.TEL(phone, 'work')
        builder.TEL(self.row['Business Fax'], 'work,fax')
        builder.TEL(self.row['Callback'], 'callback')
        builder.TEL(self.row['Car Phone'], 'mobile')
        builder.TEL(self.row['Company Main Phone'], 'work')
        builder.TEL(self.row['Home Fax'], 'home,fax')
        builder.TEL(self.row['Home Phone'], 'home')
        builder.TEL(self.row['Home Phone 2'], 'home')
        builder.TEL(self.row['ISDN'], '')
        builder.TEL(self.row['Mobile Phone'], 'mobile')
        builder.TEL(self.row['Other Fax'], 'fax')
        builder.TEL(self.row['Other Phone'], '')
        builder.TEL(self.row['Pager'], 'pager')
        builder.TEL(self.row['Primary Phone'], 'pref')
        builder.EMAIL(self.row['E-mail Address'], self.row['E-mail Type'])
        builder.EMAIL(self.row['E-mail 2 Address'], self.row['E-mail 2 Type'])
        builder.EMAIL(self.row['E-mail 3 Address'], self.row['E-mail 3 Type'])
        builder.ADR([self.row['Business Address PO Box'],
                     self.row['Business Street 2'],
                     self.row['Business Street'],
                     self.row['Business City'],
                     self.row['Business State'],
                     self.row['Business Postal Code'],
                     self.row['Business Country/Region']],
                    'work')
        builder.ADR([self.row['Home Address PO Box'],
                     self.row['Home Street 2'],
                     self.row['Home Street'],
                     self.row['Home City'],
                     self.row['Home State'],
                     self.row['Home Postal Code'],
                     self.row['Home Country/Region']],
                    'home')
        builder.ADR([self.row['Other Address PO Box'],
                     self.row['Other Street 2'],
                     self.row['Other Street'],
                     self.row['Other City'],
                     self.row['Other State'],
                     self.row['Other Postal Code'],
                     self.row['Other Country/Region']],
                    '')
        builder.URL(self.row['Web Page'])
        builder.NOTE(self.row['Notes'])
        builder.BDAY(self.row['Birthday'])
        builder.ORG(self.row['Company'])
        builder.ROLE(self.row['Job Title'])
        return str(builder.card)
