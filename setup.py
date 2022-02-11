from setuptools import setup, find_packages

def getversion():
    """Fetches version information from VERSION file"""
    with open('DataModelDict/VERSION') as version_file:
        return version_file.read().strip()

def getreadme():
    """Fetches readme information from README file"""
    with open('README.rst') as readme_file:
        return readme_file.read()
    
setup(name = 'DataModelDict',
      version = getversion(),
      description = "Class allowing for data models equivalently represented as Python dictionaries, JSON, and XML",
      long_description=getreadme(),
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Text Processing :: Markup :: XML',
      ],
      keywords = [
        'json',
        'xml',
        'dictionary',
      ],
      url = 'https://github.com/usnistgov/DataModelDict/',
      author = 'Lucas Hale',
      author_email = 'lucas.hale@nist.gov',
      packages = find_packages(),
      install_requires=[
        'xmltodict'
      ],
      package_data={'': ['*']},
      )