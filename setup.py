from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(name='DataModelDict',
      version='0.1',
      description='DataModelDict class for xml/json/dictionary conversions',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Physics'
      ],
      keywords='json xml dictionary', 
      url='git@github.com:lmhale99/DatamodelDict.git',
      author='Lucas Hale',
      author_email='lucas.hale@nist.gov',
      license='NIST',
      packages=['DataModelDict'],
      install_requires=[
        'xmltodict'
      ],
      include_package_data=True,
      zip_safe=False)