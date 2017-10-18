# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='vcardz-data',
      version='0.9.2',
      url='https://github.com/IdahoDataEngineers/vcardz',
      download_url='https://github.com/IdahoDataEngineers/vcardz/archive/v0.9.2.tar.gz',
      author='Idaho Data Engineers',
      author_email='info@idahodata.io',
      description='Python 3 vCard and deduplication',
      long_description=long_description,
      license='GPLv2',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',  # noqa
                   'Programming Language :: Python :: 3.6'],
      keywords=['vcard', 'deduplication', 'entity resolution', 'swoosh', 'RFC6350'],
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      install_requires=['jellyfish>=0.3.3',
                        'networkx>=1.9.1',
                        'six>=1.9.0',
                        'nameparser>=0.3.3',
                        'requests>=2.5.1']
  )
