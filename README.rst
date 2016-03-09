DataModelDict
-------

DataModelDict is a lightweight Python class for easy transformation and manipulation of JSON and XML structured data models.  It is designed to take the best aspects of JSON, XML, and Python dictionaries to allow the user to interact with any of these formats in the same manner.

The key features of DataModelDict so far are:

1. It is a child of OrderedDict meaning that it has all the features one would expect of a Python dictionary.

2. JSON conversions use the standard Python json library, and XML conversions use the xmltodict package.  This allows both data formats to be converted, manipulated and represented in similar ways.

3. Numbers and key terms (True, False, etc.) are converted from strings to appropriate Python types. 

4. Recursive searching methods  
    a. When converting to/from XML, certain elements of the model may or may not be lists depending on the specific data instance. Methods exist that allow for the treatment of these elements without knowing if they are a list or not.

    b. Recursive searching methods are added to help and modify specific components of the data model without knowing where in the full model the components are located.    


DataModelDict works by parsing in a JSON or XML data model such that every dictionary level is an instance of DataModelDict.  This allows for the conversion and functional methods to be callable both on the full model and on subcomponents. 

Basic examples can be found in the DataModelDict_Basics.ipynb Jupyter Notebook (and equivalent html).  Full documentation can be found in Documentation.html
