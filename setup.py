from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='vcardz-data',
      version='0.1.0',
      url='https://github.com/seajosh/vcardz-data',
      author='Josh Watts',
      author_email='josh.watts@gmail.com',
      license='GPLv2',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GPLv2',
                   'Programming Language :: Python :: 3.4'],
      keywords='vcard development',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*'])
  )
