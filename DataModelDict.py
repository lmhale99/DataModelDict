#!/usr/bin/env python
"""Provides the DataModelDict class for creating, accessing and manipulating json/xml data structures."""

#Standard Python libraries
from collections import OrderedDict
import json
from copy import deepcopy

#https://github.com/martinblech/xmltodict
import xmltodict

__author__ = "Lucas Hale"
__version__ = "0.8"
__email__ = "lucas.hale@nist.gov"
__status__ = "Development"

class DataModelDict(OrderedDict, object):
    """Class for handling json/xml equivalent data structures."""
    
    def __init__(self, *args, **kwargs):
        """
        Initilizes a DataModelDict. Can be initilized like an OrderedDict, or by supplying a json/xml string or file-like object.
        
        Additional Keyword Arguments when initilizing with json/xml info:
        parse_float -- data type to use for floating point values parsed from the json/xml info
        parse_int -- data type to use for integer values parsed from the json/xml info
        """
       
        OrderedDict.__init__(self)
        
        #If string or file-like object, call load
        if len(args) == 1 and (isinstance(args[0], (str, unicode)) or hasattr(args[0], 'read')):            
            format = kwargs.get('format', None)
            parse_float = kwargs.get('parse_float', float)
            parse_int = kwargs.get('parse_int', int)
            convert_NaN = kwargs.get('convert_NaN', True) 
            encoding = kwargs.get('encoding', 'utf-8') 
            self.load(args[0], format = format, 
                               parse_int = parse_int,
                               parse_float = parse_float,                                
                               convert_NaN = convert_NaN,
                               encoding = encoding)
        
        #Otherwise, call update (from OrderedDict)
        else:
            self.update(*args, **kwargs)
   
    def __getitem__(self, key):
        """Extends OrderedDict.__getitem__() to handle path lists as keys"""
        if isinstance(key, list):
            value = self
            keys = deepcopy(key)
            while len(keys) > 0:
                value = value[keys.pop(0)]   
            return value
                
        else:
            return OrderedDict.__getitem__(self, key)
   
    def __setitem__(self, key, value):
        """Extends OrderedDict.__setitem__() to handle path lists as keys"""
        if isinstance(key, list):
            term = self
            keys = deepcopy(key)
            while len(keys) > 1:
                term = term[keys.pop(0)]   
            term[keys[0]] = value
                
        else:
            return OrderedDict.__setitem__(self, key, value)
   
    def append(self, key, value):
        """If key not assigned, assigns key. If key assigned, appends value to the current value (and converts to list if needed)."""
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
        Return the value of a subelement at any level uniquely identified by the specified conditions. Issues an error if either no match, or multiple matches are found.
        
        Arguments:
        key -- key name to search for.
        yes -- dictionary of key-value terms which the subelement must have to be considered a match.
        no -- dictionary of key-value terms which the subelement must not have to be considered a match.
        """
        matching = self.finds(key, yes, no)
        
        #Test length of matching
        if len(matching) == 1:
            return matching[0]
        elif len(matching) == 0:
            raise ValueError('No matching subelements found for key (and kwargs).')
        else:
            raise ValueError('Multiple matching subelements found for key (and kwargs).')        

    def aslist(self, key):
        """Return the value(s) in the element with key=key as a list.  Useful if the specified element may or may not be a list."""
        return [val for val in self.iteraslist(key)]
          
    def path(self, key, yes={}, no={}):
        """
        Return the path list of a subelement at any level uniquely identified by the specified conditions. Issues an error if either no match, or multiple matches are found.
        
        Arguments:
        key -- key name to search for.
        yes -- dictionary of key-value terms which the subelement must have to be considered a match.
        no -- dictionary of key-value terms which the subelement must not have to be considered a match.
        """
        matching = self.paths(key, yes, no)
        
        #Test length of matching
        if len(matching) == 1:
            return matching[0]
        elif len(matching) == 0:
            raise ValueError('No matching subelements found for key (and kwargs).')
        else:
            raise ValueError('Multiple matching subelements found for key (and kwargs).')
    
    def finds(self, key, yes={}, no={}):
        """
        Return a list of all values of all elements at any level identified by the specified conditions.
               
        Arguments:
        key -- key name to search for.
        yes -- dictionary of key-value terms which the subelement must have to be considered a match.
        no -- dictionary of key-value terms which the subelement must not have to be considered a match.
        """
        return [val for val in self.iterfinds(key, yes, no)] 
    
    def paths(self, key, yes={}, no={}):
        """
        Return a list of all path lists of all elements at any level identified by the specified conditions.
               
        Arguments:
        key -- key name to search for.
        yes -- dictionary of key-value terms which the subelement must have to be considered a match.
        no -- dictionary of key-value terms which the subelement must not have to be considered a match.
        """
        return [val for val in self.iterpaths(key, yes, no)]
    
    def iteraslist(self, key):
        """Iterate over value(s) in the element with key=key.  Useful if the specified element may or may not be a list."""
        if key in self:
            if isinstance(self[key], list):
                for val in self[key]:
                    yield val
            else:
                yield self[key]        
    
    def iterfinds(self, key, yes={}, no={}):
        """
        Return an iterator over all values of all elements at any level identified by the specified conditions.
               
        Arguments:
        key -- key name to search for.
        yes -- dictionary of key-value terms which the subelement must have to be considered a match.
        no -- dictionary of key-value terms which the subelement must not have to be considered a match.
        """
        
        #iterate over list of all subelements given by key
        for subelement in self.__gen_dict_value(key, self):
            match = True
           
            #iterate over all key, value pairs in yes
            for yes_key, yes_value in yes.iteritems():
                key_match = False
                
                #iterate over list of all values associated with kwarg_key in the subelement
                for value in self.__gen_dict_value(yes_key, subelement):
                    if value == yes_value:
                        key_match = True
                        break
                
                #if a kwarg_key-kwarg_value match is not found, then the subelement is not a match
                if not key_match:
                    match = False
                    break
          
            #iterate over all key, value pairs in no
            if match:
                for no_key, no_value in no.iteritems():
                    key_match = True
                    
                    #iterate over list of all values associated with kwarg_key in the subelement
                    for value in self.__gen_dict_value(no_key, subelement):
                        if value == no_value:
                            key_match = False
                            break
                    
                    #if a kwarg_key-kwarg_value match is not found, then the subelement is not a match
                    if not key_match:
                        match = False
                        break
           
            #if match is still true, yield subelement
            if match:
                yield subelement
    
    def iterpaths(self, key, yes={}, no={}):
        """
        Return an iterator over all path lists of all elements at any level identified by the specified conditions.
               
        Arguments:
        key -- key name to search for.
        yes -- dictionary of key-value terms which the subelement must have to be considered a match.
        no -- dictionary of key-value terms which the subelement must not have to be considered a match.
        """
        
        #iterate over list of all subelements given by key
        for path in self.__gen_dict_path(key, self):
            subelement = self[path]
            match = True
           
            #iterate over all key, value pairs in yes
            for yes_key, yes_value in yes.iteritems():
                key_match = False
                
                #iterate over list of all values associated with kwarg_key in the subelement
                for value in self.__gen_dict_value(yes_key, subelement):
                    if value == yes_value:
                        key_match = True
                        break
                
                #if a kwarg_key-kwarg_value match is not found, then the subelement is not a match
                if not key_match:
                    match = False
                    break
          
            #iterate over all key, value pairs in no
            if match:
                for no_key, no_value in no.iteritems():
                    key_match = True
                    
                    #iterate over list of all values associated with kwarg_key in the subelement
                    for value in self.__gen_dict_value(no_key, subelement):
                        if value == no_value:
                            key_match = False
                            break
                    
                    #if a kwarg_key-kwarg_value match is not found, then the subelement is not a match
                    if not key_match:
                        match = False
                        break
           
            #if match is still true, yield path
            if match:
                yield path
    
    def load(self, model, format=None, parse_int=int, parse_float=float, convert_NaN=True, encoding='utf-8'):
        """
        Read in values from a json/xml string or file-like object.
        
        Keyword Arguments (all optional):
        format -- explicitly state file is 'json' or 'xml'.  If format is None, will try both (but provide less details if load fails).  
        parse_float -- data type to use for floating point values parsed from the json/xml info.
        parse_int -- data type to use for integer values parsed from the json/xml info.
        convert_NaN -- boolean indicating if NaN, Infinity, and -Infinity are interpreted if found. Default is True.
        encoding -- encoding style of file being read. Default assumes unicode 'utf-8'. May have issues if not ASCII based.
        """
        
        #if format is not specified, try both json and xml
        if format is None:
            try:
                self.load(model, format='json', parse_int=parse_int, parse_float=parse_float, convert_NaN=convert_NaN, encoding=encoding)
            except:
                if hasattr(model, 'seek'): model.seek(0)
                try:
                    self.load(model, format='xml', parse_int=parse_int, parse_float=parse_float, convert_NaN=convert_NaN, encoding=encoding)
                except:
                    raise ValueError('Unable to parse as JSON or XML')        
        
        #if format is specified to be json, only try json
        elif format.lower() == 'json':
            if isinstance(model, (str, unicode)):
                self.update(json.loads(model, 
                                       object_pairs_hook=DataModelDict, 
                                       parse_int=parse_int, 
                                       parse_float=parse_float, 
                                       parse_constant=convert_NaN, 
                                       encoding=encoding))
            elif hasattr(model, 'read'):
                self.update(json.load(model, 
                                      object_pairs_hook=DataModelDict, 
                                      parse_int=parse_int, 
                                      parse_float=parse_float, 
                                      parse_constant=convert_NaN, 
                                      encoding=encoding))
            else:
                raise TypeError('Invalid data type for loading')
                    
        #if format is specified to be xml, only try xml
        elif format.lower() == 'xml':
            if isinstance(model, (str, unicode)) or hasattr(model, 'read'):
                self.update(xmltodict.parse(model,
                                            postprocessor=self.__xml_postprocessor(parse_int, parse_float, convert_NaN),
                                            #self.__xml_postprocessor(parse_int = parse_int, 
                                            #                                         parse_float = parse_float, 
                                            #                                         convert_NaN = convert_NaN), 
                                            dict_constructor = DataModelDict,
                                            encoding = encoding))
            else:
                raise TypeError('Invalid data type for loading')
            
        else:
            raise ValueError("Invalid format. Only 'json', 'xml', or None values supported.")                    
        
    def json(self, fp=None, indent=None, separators=(', ', ': '), convert_NaN=True, encoding='utf-8'):
        """
        Return the DataModelDict in json format.
        
        Keyword Arguments (all optional):
        fp -- file-like object.  If given, the json will be written to fp instead of returned as a string.
        indent -- int number of spaces to indent lines.  If not given, the output will be inline.
        separators --  an (item_separator, dict_separator) tuple. Default is (', ', ': ').
        convert_NaN -- boolean indicating if javascript NaN, Infinity, and -Infinity are allowed. Default is True.
        encoding -- encoding style for the output.
        """
        
        if fp is None:
            return json.dumps(self, 
                              indent=indent, 
                              separators=separators, 
                              allow_nan=convert_NaN, 
                              encoding=encoding)
        else:
            json.dump(self, 
                      fp=fp, 
                      indent=indent, 
                      separators=separators, 
                      allow_nan=convert_NaN, 
                      encoding=encoding)
    
    def xml(self, fp=None, indent=None, full_document=True, convert_NaN=True, encoding='utf-8'):
        """
        Return the DataModelDict in xml format.
        
        Keyword Arguments (all optional):
        fp -- file-like object.  If given, the xml will be written to fp instead of returned as a string.
        indent -- int number of spaces to indent lines.  If not given, the output will be inline.
        full_document -- boolean indicating if the output is associated with a full xml model.  If True, it must have only one root, and a header is added.
        convert_NaN -- boolean indicating that strings for NaN, Infinity, and -Infinity are changed to match the javascript versions. Default is True.
        encoding -- encoding style for the output.
        """

        if indent is None:
            indent = ''
            newl = ''
        else:
            indent = ''.join([' ' for i in xrange(indent)])
            newl = '\n'
        
        return xmltodict.unparse(deepcopy(self), 
                                 output=fp, 
                                 preprocessor = self.__xml_preprocessor(convert_NaN),
                                 pretty=True, 
                                 indent=indent, 
                                 newl=newl, 
                                 full_document=full_document, 
                                 encoding='utf-8')    
    
    def __xml_postprocessor(self, parse_int, parse_float, convert_NaN):
        """Internal method that defines the xmltodict postprocessor function to use."""
        if convert_NaN is True:
            parse_constant = {'':None,
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
            if not isinstance(value, (str, unicode)):
                return key, value
            if value in parse_constant:
                return key, parse_constant[value]
            try:
                value = parse_int(value)
                return key, value
            except:
                pass
            try:
                value = parse_float(value)
                return key, value
            except:
                return key, value
                    
        return postprocessor
    
    def __xml_preprocessor(self, convert_NaN):
        """Internal method that defines the xmltodict postprocessor function to use."""
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
            if hasattr(value, 'iteritems'):
                for k, v in value.iteritems():
                    value[k] = preprocessor(k,v)[1]
                return key, value
            elif hasattr(value, '__iter__'):
                for i in xrange(len(value)):
                    value[i] = preprocessor(key, value[i])[1]
                return key, value
            else:
                if not isinstance(value, (str, unicode)):
                    value = repr(value)
                if value in allow_NaN:
                    return key, allow_NaN[value]
                else:
                    return key, value            
            
        return preprocessor

    def __gen_dict_value(self, key, var):   
        """Internal method that recursively searches and yields values for all elements with key matching key."""
        
        if hasattr(var,'iteritems'):
            for k, v in var.iteritems():
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
        """Internal method that recursively searches and yields path lists for all elements with key matching key."""
        
        if hasattr(var,'iteritems'):
            for k, v in var.iteritems():
                if k == key:
                    if isinstance(v, list):
                        for i in xrange(len(v)):
                            yield [k, i]
                    else:
                        yield [k]
                if isinstance(v, dict):
                    for result in self.__gen_dict_path(key, v):
                        if result is not None:
                            yield [k] + result
                elif isinstance(v, list):
                    for i in xrange(len(v)):
                        for result in self.__gen_dict_path(key, v[i]):
                            if result is not None:
                                yield [k, i] + result
