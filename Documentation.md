#DataModelDict Python Class

DataModelDict is a lightweight Python class for easy transformation and manipulation of JSON and XML structured data models.  It is designed to take the best aspects of JSON, XML, and Python dictionaries to allow the user to interact with any of these formats in a similar and convieneint manner. This class was designed to offer tools making it easy to read, modify, create and transform tiered and branching data models.

This webpage outlines the features of DataModelDict and fully documents the class methods.  Simple demonstrations can be found in the [DataModelDict Basics.ipynb Jupyter Notebook](https://github.com/usnistgov/DataModelDict/blob/master/DataModelDict%20Basics.ipynb).


##Class Methods

###1. Basic Functionality

These are extentions to the basic methods of the root class OrderedDict.

####DataModelDict.\_\_init\_\_(self, \*args, **kwargs)

DataModelDict.\_\_init\_\_() extends OrdereDict.\_\_init\_\_() by allowing for instances to be initialized using JSON or XML formatted data.  Basically, if one argument is given that is a string or file-like object, then DataModelDict.load() is called and all keyword arguments passed along.  Otherwise, the class is initialized in the same fashion as an OrderedDict.

####DataModelDict.\_\_getitem\_\_(self, key)

DataModelDict.\_\_getitem\_\_() extends OrdereDict.\_\_getitem\_\_() by allowing for keys to be path-lists. In short, the following two lines of code are equivalent:

    element_abcd = my_model['a']['b']['c']['d']
    element_abcd = my_model['a','b','c','d']
    
The items in the path lists can be both dictionary keys list indexes, assuming that my_model is a DataModelDict.

####DataModelDict.\_\_setitem\_\_(self, key, value)

DataModelDict.\_\_setitem\_\_() extends OrdereDict.\_\_setitem\_\_() by allowing for keys to be path-lists. In short, the following two lines of code are equivalent:

    my_model['a']['b']['c']['d'] = element_abcd
    my_model['a','b','c','d'] = element_abcd 
    
The items in the path lists can be both dictionary keys list indexes, assuming that my_model is a DataModelDict.

###2. Format Conversion

####DataModelDict.load(self, model, format=None, parse_int=int, parse_float=float, convert_NaN=True, encoding='utf-8')

Read in a data model from a JSON/XML string or file-like object. The optional keyword arguments are:

- __format__: explicitly state file is 'json' or 'xml'.  If format is None, both will be tried.  Explicitly stating the format is useful when loading fails as it allows for the parser's errors to be directly accessed.

- __parse_float__: data type to use for floating point values parsed from the json/xml info.
        
- __parse_int__: data type to use for integer values parsed from the json/xml info.

- __convert_NaN__: boolean indicating if NaN, Infinity, and -Infinity are interpreted if found.

- __encoding__: encoding style of file being read. The parsers may have issues if the input is not ASCII based. 

####DataModelDict.json(self, fp=None, indent=None, separators=(', ', ': '), convert_NaN=True, encoding='utf-8')

Return the DataModelDict in JSON format. The optional keyword arguments are:
        
- __fp__: file-like object.  If given, the JSON will be written to fp instead of returned as a string.

- __indent__: integer number of spaces to indent lines.  If not given, the output will be inline.

- __separators__:  an (item_separator, dict_separator) tuple. Default is (', ', ': ').

- __convert_NaN__: boolean indicating if javascript NaN, Infinity, and -Infinity are allowed. Default is True.

- __encoding__: encoding style to use for the output.

####DataModelDict.xml(self, fp=None, indent=None, full_document=True, convert_NaN=True, encoding='utf-8')

Return the DataModelDict in XML format. The optional keyword arguments are:
        
- __fp__: file-like object.  If given, the XML will be written to fp instead of returned as a string.

- __indent__: int number of spaces to indent lines.  If not given, the output will be inline.

- __full_document__: boolean indicating if the output is associated with a full xml model.  If True, it must have only one root, and a header is added.

- __convert_NaN__: boolean indicating that strings for NaN, Infinity, and -Infinity are changed to match the javascript versions. Default is True.

- __encoding__: encoding style for the output.

###3. Search Functionality

With tiered data models, it can be tedious to locate or access specific elements, especially when you are only interested in certain elements (and may not know exactly where they are buried).  These methods help by recursively searching the data structure for you. 

The arguments for all of the functions in this section are identical:

- __key__: element key name that is recursively searched for.

- __yes__: dictionary of sub-element key-value pairs that must all be included in the key element in order for the element to be considered a match.

- __no__: dictionary of sub-element key-value pairs which if they are found in the key element will exclude the element from being considered a match.

####DataModelDict.finds(self, key, yes={}, no={})

This performs a recursive search and returns a list containing all elements and sub-elements at any level of the DataModelDict corresponding to the matching conditions.  

####DataModelDict.find(self, key, yes={}, no={})

Same as finds(), except returns one matching element not as a list. Issues an error if no matching elements are found, or multiple matching elements are found. This is useful for working with a sub-element of a data model without knowing (or caring) where it is located.

####DataModelDict.iterfinds(self, key, yes={}, no={})

Same as finds(), except returns an iterator over the matching elements instead of a list. 

####DataModelDict.paths(self, key, yes={}, no={})

This performs a recursive search and returns a list containing path-lists to all elements and sub-elements at any level of the DataModelDict corresponding to the matching conditions. Each path-list contains the dictionary keys and list indexes necessary to walk down to a matching element.

####DataModelDict.path(self, key, yes={}, no={})

Same as paths(), except returns one matching path-list. Issues an error if no matching elements are found, or multiple matching elements are found. 

####DataModelDict.iterpaths(self, key, yes={}, no={})

Same as paths(), except returns an iterator over the path-lists for the matching elements instead of a list. 


###4. XML-Related Convenience Methods

There are some aspects of XML that do not offer a direct 1-1 relationship in Python (or JSON).  The methods listed in this section are tools designed to help with these peculiarities.

####DataModelDict.append(self, key, value)

This is a convenience method for working with unbounded XML sequences, where in Python the corresponding elements may or may not be lists.  DataModelDict.append() allows for values to be appended to elements whether the elements do or don't exist, and whether the elements are or are not lists. The logic is that if key does not exist in the DataModelDict, then value is assigned to that key.  If key does exist, then the current value is converted into a list if it is not already one, and the supplied value is appended.

####DataModelDict.aslist(self, key)

This is a convenience method for working with unbounded XML sequences, where in Python the corresponding elements may or may not be lists.  It returns the element specified by key as a list, whether or not it actually is one.  If the element does not exist, an empty list is returned.

####DataModelDict.iteraslist(self, key)

This is a convenience method for working with unbounded XML sequences, where in Python the corresponding elements may or may not be lists.  This is the same as aslist(), except it returns an iterator over the value(s) in the element instead of a list containing the value(s).