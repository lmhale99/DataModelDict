=============
DataModelDict
=============

Introduction
------------

The DataModelDict class is used for handling data models that have equivalent
representations in XML, JSON, and Python.  Constructing data models in this
way is convenient as it supports compatibility across different software
tools, such as different types of databases.

The DataModelDict class:

- is a child of OrderedDict,
- has methods for converting to/from XML and JSON, 
- has methods for searching through elements, and
- has methods that help with constructing and interacting with compliant data
  models.

Setup
-----

The code has no requirements that limit which systems it can be used on, i.e.
it should work on Linux, Mac and Windows computers.

The latest release can be installed using pip::

    pip install DataModelDict

The code and all documentation is hosted on GitHub and can be directly
downloaded at `https://github.com/usnistgov/DataModelDict`_.

.. _https://github.com/usnistgov/DataModelDict: 
   https://github.com/usnistgov/DataModelDict

Conversions
-----------

Some considerations need to be taken into account for designing data models
that allow for exact reversible transformations between the three formats:

- Valid, full XML requires that there is exactly one root element.  In other
  words, the top-level DataModelDict of a data model   can have only one key.
- Do not use lists of lists for representing data.  The XML conversions are
  only reversible for lists of values or lists of dictionaries.  Future
  updates may allow this.
- Avoid using XML attributes if possible.  While the XML conversions do
  reversibly handle attributes, it complicates the Python and JSON
  representations.
- Embedded XML content, i.e. "text with <embed>embedded</embed> content",
  might not be reversible:

    - If this is in a Python/JSON value, converting to XML gives "text with
      &amp;lt;embed&amp;gt;embedded&amp;lt;/embed&amp;gt; content". This is
      reversible.
    - If this is an XML text field, parsing to Python pulls the embedded
      elements out of the text, which is not reversible!

- XML subelements of the same name within an element should be given
  consecutively.  When parsed, all values of subelements of the same name are
  collected together in a list.  This will alter the original order of
  subelements if matching names were not originally consecutive. 

Conversion from Python to JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Python-JSON conversions use the standard Python JSON library.  In
converting from Python to JSON, all elements of the DataModelDict must be an
instance of a supported data type (with unicode and long being specific to
Python 2).

================  =========
Python            JSON     
================  =========
dict              object   
list, tuple       array    
str, unicode      string   
int, long, float  number   
True              true     
False             false    
None              null     
np.nan            NaN      
np.inf            Infinity 
-np.inf           -Infinity
================  =========

As DataModelDict is a child of OrderedDict, it registers as being an instance
of dict. Any other objects would first need to be converted to one of these
types, e.g. a numpy array would need to be converted to a list.

Conversion from Python to XML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Python-XML conversions use the xmltodict Python package. The XML content
is constructed based on the Python data types.

================  ================
Python            XML             
================  ================
dict              subelement      
list, tuple       repeated element
str, unicode      text            
int, long, float  text (from repr)
True              text = True     
False             text = False    
None              empty text field
np.nan            text = NaN      
np.inf            text = Infinity 
-np.inf           text = -Infinity
================  ================

Some characters in the XML text fields will also be converted to avoid
conflicts.

- XML limited characters such as <, > and & are converted to their
  HTML entities.
- \n, \t, \r are converted to \\\n, \\\t, and \\\r

Any dictionary keys starting with '@' will be converted into XML attributes,
and the dictionary key '#text' is interpreted as the text value of the
element.

Conversion from JSON to Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Python-JSON conversions use the standard Python JSON library.  In
converting from JSON to Python, the conversions of types is straight-forward.

=============  =============  =============
JSON           Python 2       Python 3     
=============  =============  =============
object         DataModelDict  DataModelDict
array          list           list         
string         unicode        str          
number (int)   long           int          
number (real)  float          float        
true           True           True         
false          False          False        
null           None           None         
NaN            np.nan         np.nan       
Infinity       np.inf         np.inf       
-Infinity      -np.inf        -np.inf      
=============  =============  =============

Conversion from XML to Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Python-XML conversions use the xmltodict Python package.  The text fields
will be interpreted based on the following sequential tests:

================  ========  ========
XML text          Python 2  Python 3
================  ========  ========
== 'True'         True      True    
== 'False'        False     False   
== ''             None      None    
== 'NaN'          np.nan    np.nan  
== 'Infinity'     np.inf    np.inf  
== '-Infinity'    -np.inf   -np.inf 
try: int(text)    long      int     
try: float(text)  float     float   
otherwise         unicode   str     
================  ========  ========

The reverse conversions are done for the special characters mentioned in the
Conversion from Python to XML section above.

Any 'attr' attribute fields are converted to elements named '\@attr' and
corresponding '#text' elements are created if needed.

Class Documentation
-------------------

.. automodule:: DataModelDict
    :members:
    :undoc-members:
    :show-inheritance: