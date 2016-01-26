DataModelDict
-------

The DataModelDict is a Python class for easy conversions between json, xml and Pyhton dictionaries.  The json conversions are handled with the json standard library, while the xml conversions are handled with the xmltodict library, with additional data parsing for value recognition.

The key features of DataModelDict so far are:

1.	It is a child of OrderedDict making it easy to build models in Python.
2.	It can load xml or json from a string or file-like object.
3.	Numeric values are converted from strings during loading, with the option to specify the int/float types.
4.	Methods allow for the whole dictionary or subcomponents to be returned as either a json or xml string with the option to specify indentation level.  
5.	Additional methods for recursive find for specific keys, and conversion of html subelements of xml to strings.
