import codecs
import os
import re
from setuptools import setup

def get_version():
    """Gets version from main package file"""
    main_file = os.path.join(os.path.dirname(__file__), 'DataModelDict.py')
    main_file = codecs.open(main_file, 'r').read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              main_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(name = 'DataModelDict',
      version = get_version(),
      description = "Class allowing for data models equivalently represented as Python dictionaries, JSON, and XML",
      author = 'Lucas Hale',
      author_email = 'lucas.hale@nist.gov',
      url = 'https://github.com/usnistgov/DataModelDict/',
      long_description=readme(),
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Markup :: XML',
      ],
      keywords = 'json xml dictionary',
      py_modules = ['DataModelDict'],
      install_requires=['xmltodict'])