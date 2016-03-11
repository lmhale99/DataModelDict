#!/usr/bin/env python

from setuptools import setup
import DataModelDict

def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(name = 'DataModelDict',
      version =      DataModelDict.__version__,
      description =  DataModelDict.__doc__,
      author =       DataModelDict.__author__,
      author_email = DataModelDict.__email__,
      url = 'git@github.com:lmhale99/DataModelDict.git',
      long_description=readme(),
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Physics'
      ],
      keywords = 'json xml dictionary ', 
      py_modules = ['DataModelDict'],
      install_requires=[
        'xmltodict'
      ],
      include_package_data = True,
      zip_safe = False)