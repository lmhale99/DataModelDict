"""DataModelDict class for representing data models equivalently in Python, JSON, and XML."""

# Standard Python libraries
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)
import os
import sys
import json
from io import BytesIO, open
from copy import deepcopy
from collections import OrderedDict

# https://github.com/martinblech/xmltodict
import xmltodict

# Python 2 settings
if sys.version_info[0] == 2:
    stringtype = basestring
    range = xrange
    
    def iteritems(d):
        for key, value in d.iteritems():
            yield key, value
    
# Python 3 settings
elif sys.version_info[0] == 3:
    stringtype = str
    unicode = str
    long = int
    
    def iteritems(d):
        for key, value in d.items():
            yield key, value
    
else:
    raise ValueError("Unsupported Python version")

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file) as version_f:
        return version_f.read().strip()
        
__author__ = "Lucas Hale"
__email__ = "lucas.hale@nist.gov"
__status__ = "Development"
__version__ = get_version()

__all__ = ['DataModelDict']

class DataModelDict(OrderedDict, object):
    """Class for handling json/xml equivalent data structures."""
    
    def __init__(self, *args, **kwargs):
        """
        Initilizes a DataModelDict.
        If one args is given and it is a str or file-like object, then load()
        is called.
        Otherwise, the OrderedDict initializer is called.
        
        Parameters
        ----------
        args
            If one args is given which is a str or file-like object, then
            self.load(args[0], **kwargs) is called.  Otherwise, the
            DataModelDict is initialized like an OrderedDict.
        kwargs
            Variable keyword arguments. Passed on to either self.load() or
            self.update(), which is inherited from OrderedDict.
        
        Returns
        -------
        DataModelDict
        """
        
        OrderedDict.__init__(self)
        
        # If string or file-like object, call load
        if len(args) == 1 and (isinstance(args[0], stringtype) or hasattr(args[0], 'read')):
            self.load(args[0], **kwargs)
        
        # Otherwise, call update (from OrderedDict)
        else:
            self.update(*args, **kwargs)
    
    def __getitem__(self, key):
        """
        Extends OrderedDict.__getitem__() to handle path lists as keys.
        
        Parameters
        ----------
        key
            Dictionary key.  If key is a list, then subsequent keys down the
            structure are accessed.
        
        Returns
        -------
        any
            The value of the element associated with key or the path list.
        """
        if isinstance(key, list):
            value = self
            keys = deepcopy(key)
            while len(keys) > 0:
                value = value[keys.pop(0)]
            return value
        
        else:
            return OrderedDict.__getitem__(self, key)
    
    def __setitem__(self, key, value):
        """
        Extends OrderedDict.__setitem__() to handle path lists as keys.
        
        Parameters
        ----------
        key
            Dictionary key.  If key is a list, then subsequent keys down the
            structure are accessed.
        """
        if isinstance(key, list):
            term = self
            keys = deepcopy(key)
            while len(keys) > 1:
                term = term[keys.pop(0)]
            term[keys[0]] = value
        
        else:
            return OrderedDict.__setitem__(self, key, value)
    
    def append(self, key, value):
        """
        Adds a value for element key by either adding key to the dictionary or
        appending the value as a list to any current value.
        
        Parameters
        ----------
        key
            The dictionary key.
        value
            The value to add to the dictionary key.  If key exists, the
            element is converted to a list if needed and value is appended.
        """
        if key in self:
            if isinstance(self[key], list):
                self[key].append(value)
            else:
                self[key] = [self[key]]
                self[key].append(value)
        else:
            self[key] = value
    
    def find(self, key, yes={}, no={}):
        """
        Return the value of a subelement at any level uniquely identified by
        the specified conditions.
        
        Parameters
        ----------
        key
            Dictionary key to search for.
        yes : dict
            Key-value terms which the subelement must have to be considered a
            match.
        no : dict
            Key-value terms which the subelement must not have to be
            considered a match.
        
        Returns
        -------
        any
            The value of the uniquely identified subelement.
        
        Raises
        ------
        ValueError
            If exactly one matching subelement is not identified.
        """
        matching = self.finds(key, yes, no)
        
        # Test length of matching
        if len(matching) == 1:
            return matching[0]
        elif len(matching) == 0:
            raise ValueError('No matching subelements found for key (and kwargs).')
        else:
            raise ValueError('Multiple matching subelements found for key (and kwargs).')
    
    def aslist(self, key):
        """
        Gets the value of a dictionary key as a list.  Useful for elements
        whose values may or may not be lists.
        
        Parameters
        ----------
        key
            Dictionary key
            
        Returns
        -------
        list
            The dictionary's element value or [value] depending on if it
            already is a list.
        """
        return [val for val in self.iteraslist(key)]
    
    def path(self, key, yes={}, no={}):
        """
        Return the path list of a subelement at any level uniquely identified
        by the specified conditions. Issues an error if either no match, or
        multiple matches are found.
        
        Parameters
        ----------
        key
            Dictionary key to search for.
        yes : dict
            Key-value terms which the subelement must have to be considered a
            match.
        no : dict
            Key-value terms which the subelement must not have to be
            considered a match.
            
        Returns
        -------
        list of str
            The subelement path list to the uniquely identified subelement.
        
        Raises
        ------
        ValueError
            If exactly one matching subelement is not identified.
        """
        matching = self.paths(key, yes, no)
        
        # Test length of matching
        if len(matching) == 1:
            return matching[0]
        elif len(matching) == 0:
            raise ValueError('No matching subelements found for key (and kwargs).')
        else:
            raise ValueError('Multiple matching subelements found for key (and kwargs).')
    
    def finds(self, key, yes={}, no={}):
        """
        Finds the values of all subelements at any level identified by the
        specified conditions.
        
        Parameters
        ----------
        key
            Dictionary key to search for.
        yes : dict
            Key-value terms which the subelement must have to be considered a
            match.
        no : dict
            Key-value terms which the subelement must not have to be
            considered a match.
        
        Returns
        -------
        list
            The values of any matching subelements.
        """
        return [val for val in self.iterfinds(key, yes, no)] 
    
    def paths(self, key, yes={}, no={}):
        """
        Return a list of all path lists of all elements at any level
        identified by the specified conditions.
               
        Parameters
        ----------
        key
            Dictionary key to search for.
        yes : dict
            Key-value terms which the subelement must have to be considered a
            match.
        no : dict
            Key-value terms which the subelement must not have to be
            considered a match.
        
        Returns
        -------
        list 
            The path lists for any matching subelements.
        """
        return [val for val in self.iterpaths(key, yes, no)]
    
    def iteraslist(self, key):
        """
        Iterates through the values of a dictionary key.  Useful for elements
        whose values may or may not be lists.
        
        Parameters
        ----------
        key
            Dictionary key
            
        Yields
        ------
        any
            The dictionary's value or each element in value if value is a
            list.
        """
        if key in self:
            if isinstance(self[key], list):
                for val in self[key]:
                    yield val
            else:
                yield self[key]
    
    def iterfinds(self, key, yes={}, no={}):
        """
        Iterates over the values of all subelements at any level identified by
        the specified conditions.
        
        Parameters
        ----------
        key
            Dictionary key to search for.
        yes : dict
            Key-value terms which the subelement must have to be considered a
            match.
        no : dict
            Key-value terms which the subelement must not have to be
            considered a match.
            
        Yields
        ------
        any
            The values of any matching subelements.
        """
        
        # Iterate over list of all subelements given by key
        for subelement in self.__gen_dict_value(key, self):
            match = True
            
            # Iterate over all key, value pairs in yes
            for yes_key, yes_value in iteritems(yes):
                key_match = False
                
                # Iterate over list of all values associated with kwarg_key
                # in the subelement
                for value in self.__gen_dict_value(yes_key, subelement):
                    if value == yes_value:
                        key_match = True
                        break
                
                # If a kwarg_key-kwarg_value match is not found, then the
                # subelement is not a match
                if not key_match:
                    match = False
                    break
            
            # Iterate over all key, value pairs in no
            if match:
                for no_key, no_value in iteritems(no):
                    key_match = True
                    
                    # Iterate over list of all values associated with
                    # kwarg_key in the subelement
                    for value in self.__gen_dict_value(no_key, subelement):
                        if value == no_value:
                            key_match = False
                            break
                    
                    # If a kwarg_key-kwarg_value match is not found, then the
                    # subelement is not a match
                    if not key_match:
                        match = False
                        break
            
            # If match is still true, yield subelement
            if match:
                yield subelement
    
    def iterpaths(self, key, yes={}, no={}):
        """
        Iterates over the path lists to all elements at any level identified
        by the specified conditions.
        
        Parameters
        ----------
        key
            Dictionary key to search for.
        yes : dict
            Key-value terms which the subelement must have to be considered a
            match.
        no : dict
            Key-value terms which the subelement must not have to be
            considered a match.
        
        Yields
        ------
        list of str
            The path lists to any matching subelements.
        """
        
        # Iterate over list of all subelements given by key
        for path in self.__gen_dict_path(key, self):
            subelement = self[path]
            match = True
            
            # Iterate over all key, value pairs in yes
            for yes_key, yes_value in iteritems(yes):
                key_match = False
                
                # Iterate over list of all values associated with kwarg_key in
                # the subelement
                for value in self.__gen_dict_value(yes_key, subelement):
                    if value == yes_value:
                        key_match = True
                        break
                
                # If a kwarg_key-kwarg_value match is not found, then the
                # subelement is not a match
                if not key_match:
                    match = False
                    break
            
            # Iterate over all key, value pairs in no
            if match:
                for no_key, no_value in iteritems(no):
                    key_match = True
                    
                    # Iterate over list of all values associated with
                    # kwarg_key in the subelement
                    for value in self.__gen_dict_value(no_key, subelement):
                        if value == no_value:
                            key_match = False
                            break
                    
                    # If a kwarg_key-kwarg_value match is not found, then the
                    # subelement is not a match
                    if not key_match:
                        match = False
                        break
           
            # If match is still true, yield path
            if match:
                yield path
    
    def load(self, model, format=None):
        """
        Read in values from a json/xml string or file-like object.
        
        Parameters
        ----------
        model : str or file-like object
            The XML or JSON content to read.  This is allowed to be either a
            file path, a string representation, or an open file-like object in
            byte mode.
        format : str or None, optional
            Allows for the format of the content to be explicitly stated
            ('xml' or 'json').  If None (default), will try to determine which
            format based on if the first character of model is '<' or '{'.
        
        Raises
        ------
        ValueError
            If format is None and unable to identify XML/JON content, or if
            format is not equal to 'xml' or 'json'.
        """
        
        # Read in model as file-like object if file, model string, or file
        # path string
        with uber_open_rmode(model) as model:
            
            # If format is not specified, identify from first character
            if format is None:
                test = ''
                while test == '':
                    test = model.readline().strip()
                try:
                    test = chr(test[0])
                except:
                    test = test[0]
                if test == '{':
                    format = 'json'
                elif test == '<':
                    format = 'xml'
                else:
                    raise ValueError('JSON/XML content not found')
                
                model.seek(0)
            
            # Load json using json package
            if format.lower() == 'json':
                self.update(json.load(model,
                                      object_pairs_hook = DataModelDict,
                                      parse_int = long,
                                      parse_float = float,
                                      parse_constant = True))
            
            # Load xml using xmltodict package
            elif format.lower() == 'xml':
                self.update(xmltodict.parse(model,
                                            postprocessor = self.__xml_postprocessor(),
                                            dict_constructor = DataModelDict))
            
            else:
                raise ValueError("Invalid format. Only 'json', 'xml', or None values supported.")
    
    def json(self, fp=None, indent=None, separators=(', ', ': ')):
        """
        Converts the DataModelDict to JSON content.
        
        Parameters
        ----------
        fp : file-like object or None, optional
            An open file to write the content to.  If None (default), then
            the content is returned as a str.
        indent : int or None, optional 
            Number of spaces to indent lines.  If None (default), the content
            will be inline.
        separators : tuple of str, optional
            Allows for item_separator and dict_separator) to be changed.
            Default is (', ', ': ').
        
        Returns
        -------
        str, optional
            The JSON content (only returned if fp is None).
        """
        
        if fp is None:
            return json.dumps(self,
                              indent = indent,
                              separators = separators)
        else:
            json.dump(self,
                      fp = fp,
                      indent = indent,
                      separators = separators)
    
    def xml(self, fp=None, indent=None, full_document=True):
        """
        Return the DataModelDict as XML content.
        
        Parameters
        ----------
        fp : file-like object or None, optional
            An open file to write the content to.  If None (default), then
            the content is returned as a str.
        indent : int or None, optional 
            Number of spaces to indent lines.  If None (default), the content
            will be inline.
        full_document : bool, otional
            Indicates if the output is associated with a full xml model.  If
            True (default), the content can have only one root, and a header
            is added.
        
        Returns
        -------
        str, optional
            The XML content (only returned if fp is None).
        """
        
        if indent is None:
            indent = ''
            newl = ''
        else:
            indent = ''.join([' ' for i in range(indent)])
            newl = '\n'
        
        return xmltodict.unparse(deepcopy(self),
                                 output = fp,
                                 preprocessor = self.__xml_preprocessor(),
                                 pretty = True,
                                 indent = indent,
                                 newl = newl,
                                 full_document = full_document)
    
    def __xml_postprocessor(self, convert_NaN=True):
        """
        Internal method that defines the xmltodict postprocessor function.
        """
        if convert_NaN is True:
            parse_constant = {'': None,
                              'True': True,
                              'False': False,
                              '-Infinity': float('-Inf'),
                              'Infinity': float('Inf'),
                              'NaN': float('NaN')}
                              
        elif convert_NaN is False:
            parse_constant = {'': None,
                              'True': True,
                              'False': False}
        
        def postprocessor(path, key, value):
            
            # Return non-string terms
            if not isinstance(value, unicode):
                return key, value
            
            # Decode string contents
            else:
                value = value.replace('\\n', '\n')
                value = value.replace('\\t', '\t')
                value = value.replace('\\r', '\r')
            
            # Convert identified constants
            if value in parse_constant:
                return key, parse_constant[value]
            
            # Try to convert to integer
            try:
                return key, long(value)
            except:
                # Try to convert to float
                try:
                    return key, float(value)
                except:
                    return key, value
        
        return postprocessor
    
    def __xml_preprocessor(self, convert_NaN=True):
        """
        Internal method that defines the xmltodict preprocessor function.
        """
        if convert_NaN is True:
            allow_NaN = {'None': '',
                         'True': 'True',
                         'False': 'False',
                         '-inf': '-Infinity',
                         'inf': 'Infinity',
                         'nan': 'NaN'}
        
        elif convert_NaN is False:
            allow_NaN = {'None': '',
                         'True': 'True',
                         'False': 'False'}
        
        def preprocessor(key, value):
            
            # Iterate through dictionary keys
            if isinstance(value, dict):
                for k, v in iteritems(value):
                    value[k] = preprocessor(k,v)[1]
                return key, value
            
            # Iterate through list/tuple values
            elif isinstance(value, (list,tuple)):
                for i in range(len(value)):
                    value[i] = preprocessor(key, value[i])[1]
                return key, value
            
            # Convert ints and floats to strings
            elif isinstance(value, (int, long, float)) or value is None:
                value = unicode(repr(value)).strip("""L""")
                return key, value
            
            # Parse and convert strings
            elif isinstance(value, stringtype):
                if value in allow_NaN:
                    return key, allow_NaN[value]
                else:
                    value = value.replace('\n', '\\n')
                    value = value.replace('\t', '\\t')
                    value = value.replace('\r', '\\r')
                    return key, unicode(value)
            else:
                raise TypeError('unknown value type ' + repr(value))
        
        return preprocessor

    def __gen_dict_value(self, key, var):
        """
        Internal method that recursively searches and yields values for all
        elements with key matching key.
        """
        
        if isinstance(var, dict):
            for k, v in iteritems(var):
                if k == key:
                    if isinstance(v, list):
                        for d in v:
                            yield d
                    else:
                        yield v
                if isinstance(v, dict):
                    for result in self.__gen_dict_value(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.__gen_dict_value(key, d):
                            yield result

    def __gen_dict_path(self, key, var):
        """
        Internal method that recursively searches and yields path lists for
        all elements with key matching key.
        """
        
        if isinstance(var, dict):
            for k, v in iteritems(var):
                if k == key:
                    if isinstance(v, list):
                        for i in range(len(v)):
                            yield [k, i]
                    else:
                        yield [k]
                if isinstance(v, dict):
                    for result in self.__gen_dict_path(key, v):
                        if result is not None:
                            yield [k] + result
                elif isinstance(v, list):
                    for i in range(len(v)):
                        for result in self.__gen_dict_path(key, v[i]):
                            if result is not None:
                                yield [k, i] + result

class uber_open_rmode():
    """
    Context manager for reading data from file-like objects, file names,
    and data strings in the same manner.
    """
    
    def __init__(self, data):
        self.data = data
        
    def __enter__(self):
        if hasattr(self.data, 'read'):
            self.open_file = self.data
            self.to_close = False
        
        elif os.path.isfile(self.data):
            self.open_file = open(self.data, 'rb')
            self.to_close = True
        
        elif not isinstance(self.data, unicode):
            self.open_file = BytesIO(self.data)
            self.to_close = True
            
        else:
            self.open_file = BytesIO(self.data.encode('utf-8'))
            self.to_close = True
        
        return self.open_file
    
    def __exit__(self, *args):
        if self.to_close:
            self.open_file.close()