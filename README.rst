DataModelDict
=============

DataModelDict is a lightweight Python class for easy transformation and 
manipulation of JSON and XML structured data models.  It is designed to 
take the best aspects of JSON, XML, and Python dictionaries to allow the 
user to interact with any of these formats in the same manner.

The code has no requirements that limit which systems it can be used on, i.e.
it should work on Linux, Mac and Windows computers.

The latest release can be installed using pip::

pip install DataModelDict

The code and all documentation is hosted on GitHub and can be directly 
downloaded at: `https://github.com/usnistgov/DataModelDict`_.  

Basic examples can be found in the Jupyter Notebook `DataModelDict Basics.ipynb`_.
Full documentation of the class methods can be found in Documentation.md_.

.. _DataModelDict Basics.ipynb: https://github.com/usnistgov/DataModelDict/blob/master/DataModelDict%20Basics.ipynb
.. _Documentation.md: https://github.com/usnistgov/DataModelDict/blob/master/Documentation.md

The key features of DataModelDict (so far) are:

1. It is a child of OrderedDict meaning that it has all the features one 
   would expect of a Python dictionary.

2. It has built-in conversion methods for reading and writing JSON and XML.  
   JSON conversions use the standard Python `json library`_ and XML conversions 
   use the `xmltodict package`_.  

.. _json library: https://docs.python.org/2/library/json.html
.. _xmltodict package: https://github.com/martinblech/xmltodict

3. Numbers (int, float) and key terms (True, False, None) are recognized and converted during parsing. 

4. Methods for recusively searching the data model for specific keys and key-value pairs allow for the values 
   and paths (as lists of indices) of elements to be easily found.

5. Path lists can also be directly used to get and set values. 

.. code:: python
    
    #These two return the exact same val.
    val = my_model['a']['b']['c']['d'] 
    
    path = ['a', 'b', 'c', 'd']
    val = my_model[path]
  
6. Additional methods for simplified handling of cases where XML does not directly map to JSON and Python 
   dictionaries.

DataModelDict works by parsing in a JSON or XML data model such that every 
dictionary level is an instance of DataModelDict.  This allows for the conversion 
and functional methods to be callable both on the full model and on subcomponents. 
