# vcardz

vcardz is a Python 3 library for managing
[vCard data](https://tools.ietf.org/html/rfc6350 "RFC 6350 :: vCard Format Specification") and
[deduplication / entity resolution based on Swoosh](http://ilpubs.stanford.edu:8090/708/1/2005-5.pdf "Swoosh: A Generic Approch to Entity Resolution")

## Setup
```bash
pip install vcardz-data
```

## Howto

### Hello, World
```python
from vcardz import Parser

data = './tests/data/test1.vcf'
with open(data) as stream:
    engine = Parser(stream)
    for card in engine:
        print(str(card))
```

### Get one card
```python
from vcardz import Parser

data = './tests/data/test1.vcf'
with open(data) as stream:
    engine = Parser(stream)
    card = next(engine)
    print(str(card))
```

### Create a card
```python
from vcardz import Builder2

builder = Builder2()
builder.FN('John Doe')
builder.N(family='Doe',
          given='John',
          additional='Edward',
          prefix='Dr.',
          suffix='Jr.')
builder.TEL('mobile', '208-555-1234')
builder.TEL('home', '(208) 555-6789')
builder.TEL('work,fax', '2085550000')
builder.EMAIL('home', 'jdoe@email.org')
builder.EMAIL('work', 'john.doe@xyz.com')
builder.ADR(['Box 456',
             'Suite 200',
             '123 Main',
             'Boise',
             'ID',
             '83756',
             'USA'],
            'work,delivery')
builder.ADR(['',
             '',
             '718 Elm',
             'Boise',
             'ID',
             '83711'],
            'home')
builder.URL('http://xyz.com')
builder.NOTE('lorem ipsum')
builder.BDAY('1968-09-30')
builder.ORG('XYZ Inc.')
builder.ROLE('VP Research')

card = builder.card
print(str(card))
```

### Deduplication
```python
from vcardz import \
    get_logger, \
    set_logger, \
    Parser, \
    scrub

set_logger(logging.WARNING)
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
    for card in result:
        print(str(card)) 
```
