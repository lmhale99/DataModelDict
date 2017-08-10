
DataModelDict
*************


Introduction
============

The DataModelDict class is used for handling data models that have
equivalent representations in XML, JSON, and Python.  Constructing
data models in this way is convenient as it supports compatibility
across different software tools, such as different types of databases.

The DataModelDict class:

* is a child of OrderedDict,

* has methods for converting to/from XML and JSON,

* has methods for searching through elements, and

* has methods that help with constructing and interacting with
  compliant data models.


Setup
=====

The code has no requirements that limit which systems it can be used
on, i.e. it should work on Linux, Mac and Windows computers.

The latest release can be installed using pip:

::

   pip install DataModelDict

The code and all documentation is hosted on GitHub and can be directly
downloaded at https://github.com/usnistgov/DataModelDict.


Conversions
===========

Some considerations need to be taken into account for designing data
models that allow for exact reversible transformations between the
three formats:

* Valid, full XML requires that there is exactly one root element.  In
  other words, the top-level DataModelDict of a data model   can have
  only one key.

* Do not use lists of lists for representing data.  The XML
  conversions are only reversible for lists of values or lists of
  dictionaries.  Future updates may allow this.

* Avoid using XML attributes if possible.  While the XML conversions
  do reversibly handle attributes, it complicates the Python and JSON
  representations.

* Embedded XML content, i.e. "text with <embed>embedded</embed>
  content", might not be reversible:

  ..
     * If this is in a Python/JSON value, converting to XML gives
       "text with &amp;lt;embed&amp;gt;embedded&amp;lt;/embed&amp;gt;
       content". This is reversible.

     * If this is an XML text field, parsing to Python pulls the
       embedded elements out of the text, which is not reversible!

* XML subelements of the same name within an element should be given
  consecutively.  When parsed, all values of subelements of the same
  name are collected together in a list.  This will alter the original
  order of subelements if matching names were not originally
  consecutive.


Conversion from Python to JSON
------------------------------

The Python-JSON conversions use the standard Python JSON library.  In
converting from Python to JSON, all elements of the DataModelDict must
be an instance of a supported data type (with unicode and long being
specific to Python 2).

+------------------+-----------+
| Python           | JSON      |
+==================+===========+
| dict             | object    |
+------------------+-----------+
| list, tuple      | array     |
+------------------+-----------+
| str, unicode     | string    |
+------------------+-----------+
| int, long, float | number    |
+------------------+-----------+
| True             | true      |
+------------------+-----------+
| False            | false     |
+------------------+-----------+
| None             | null      |
+------------------+-----------+
| np.nan           | NaN       |
+------------------+-----------+
| np.inf           | Infinity  |
+------------------+-----------+
| -np.inf          | -Infinity |
+------------------+-----------+

As DataModelDict is a child of OrderedDict, it registers as being an
instance of dict. Any other objects would first need to be converted
to one of these types, e.g. a numpy array would need to be converted
to a list.


Conversion from Python to XML
-----------------------------

The Python-XML conversions use the xmltodict Python package. The XML
content is constructed based on the Python data types.

+------------------+------------------+
| Python           | XML              |
+==================+==================+
| dict             | subelement       |
+------------------+------------------+
| list, tuple      | repeated element |
+------------------+------------------+
| str, unicode     | text             |
+------------------+------------------+
| int, long, float | text (from repr) |
+------------------+------------------+
| True             | text = True      |
+------------------+------------------+
| False            | text = False     |
+------------------+------------------+
| None             | empty text field |
+------------------+------------------+
| np.nan           | text = NaN       |
+------------------+------------------+
| np.inf           | text = Infinity  |
+------------------+------------------+
| -np.inf          | text = -Infinity |
+------------------+------------------+

Some characters in the XML text fields will also be converted to avoid
conflicts.

* XML limited characters such as <, > and & are converted to their
  HTML entities.

* n, t, r are converted to \n, \t, and \r

Any dictionary keys starting with '@' will be converted into XML
attributes, and the dictionary key '#text' is interpreted as the text
value of the element.


Conversion from JSON to Python
------------------------------

The Python-JSON conversions use the standard Python JSON library.  In
converting from JSON to Python, the conversions of types is
straight-forward.

+---------------+---------------+---------------+
| JSON          | Python 2      | Python 3      |
+===============+===============+===============+
| object        | DataModelDict | DataModelDict |
+---------------+---------------+---------------+
| array         | list          | list          |
+---------------+---------------+---------------+
| string        | unicode       | str           |
+---------------+---------------+---------------+
| number (int)  | long          | int           |
+---------------+---------------+---------------+
| number (real) | float         | float         |
+---------------+---------------+---------------+
| true          | True          | True          |
+---------------+---------------+---------------+
| false         | False         | False         |
+---------------+---------------+---------------+
| null          | None          | None          |
+---------------+---------------+---------------+
| NaN           | np.nan        | np.nan        |
+---------------+---------------+---------------+
| Infinity      | np.inf        | np.inf        |
+---------------+---------------+---------------+
| -Infinity     | -np.inf       | -np.inf       |
+---------------+---------------+---------------+


Conversion from XML to Python
-----------------------------

The Python-XML conversions use the xmltodict Python package.  The text
fields will be interpreted based on the following sequential tests:

+------------------+----------+----------+
| XML text         | Python 2 | Python 3 |
+==================+==========+==========+
| == 'True'        | True     | True     |
+------------------+----------+----------+
| == 'False'       | False    | False    |
+------------------+----------+----------+
| == ''            | None     | None     |
+------------------+----------+----------+
| == 'NaN'         | np.nan   | np.nan   |
+------------------+----------+----------+
| == 'Infinity'    | np.inf   | np.inf   |
+------------------+----------+----------+
| == '-Infinity'   | -np.inf  | -np.inf  |
+------------------+----------+----------+
| try: int(text)   | long     | int      |
+------------------+----------+----------+
| try: float(text) | float    | float    |
+------------------+----------+----------+
| otherwise        | unicode  | str      |
+------------------+----------+----------+

The reverse conversions are done for the special characters mentioned
in the Conversion from Python to XML section above.

Any 'attr' attribute fields are converted to elements named '@attr'
and corresponding '#text' elements are created if needed.


Class Documentation
===================

Provides the DataModelDict class for creating, accessing and
manipulating json/xml data structures.

**class DataModelDict.DataModelDict(*args, **kwargs)**

   Bases: ``collections.OrderedDict``, ``object``

   Class for handling json/xml equivalent data structures.

   **append(key, value)**

      Adds a value for element key by either adding key to the
      dictionary or appending the value as a list to any current
      value.

      :Parameters:
         * **key** -- The dictionary key.

         * **value** -- The value to add to the dictionary key.  If
           key exists, the element is converted to a list if needed
           and value is appended.

   **aslist(key)**

      Gets the value of a dictionary key as a list.  Useful for
      elements whose values may or may not be lists.

      :Parameters:
         **key** -- Dictionary key

      :Returns:
         The dictionary's element value or [value] depending on if it
         already is a list.

      :Return type:
         list

   **find(key, yes={}, no={})**

      Return the value of a subelement at any level uniquely
      identified by the specified conditions.

      :Parameters:
         * **key** -- Dictionary key to search for.

         * **yes** (*dict*) -- Key-value terms which the subelement
           must have to be considered a match.

         * **no** (*dict*) -- Key-value terms which the subelement
           must not have to be considered a match.

      :Returns:
         The value of the uniquely identified subelement.

      :Return type:
         any

      :Raises:
         ``ValueError`` -- If exactly one matching subelement is not
         identified.

   **finds(key, yes={}, no={})**

      Finds the values of all subelements at any level identified by
      the specified conditions.

      :Parameters:
         * **key** -- Dictionary key to search for.

         * **yes** (*dict*) -- Key-value terms which the subelement
           must have to be considered a match.

         * **no** (*dict*) -- Key-value terms which the subelement
           must not have to be considered a match.

      :Returns:
         The values of any matching subelements.

      :Return type:
         list

   **iteraslist(key)**

      Iterates through the values of a dictionary key.  Useful for
      elements whose values may or may not be lists.

      :Parameters:
         **key** -- Dictionary key

      :Yields:
         *any* -- The dictionary's value or each element in value if
         value is a list.

   **iterfinds(key, yes={}, no={})**

      Iterates over the values of all subelements at any level
      identified by the specified conditions.

      :Parameters:
         * **key** -- Dictionary key to search for.

         * **yes** (*dict*) -- Key-value terms which the subelement
           must have to be considered a match.

         * **no** (*dict*) -- Key-value terms which the subelement
           must not have to be considered a match.

      :Yields:
         *any* -- The values of any matching subelements.

   **iterpaths(key, yes={}, no={})**

      Iterates over the path lists to all elements at any level
      identified by the specified conditions.

      :Parameters:
         * **key** -- Dictionary key to search for.

         * **yes** (*dict*) -- Key-value terms which the subelement
           must have to be considered a match.

         * **no** (*dict*) -- Key-value terms which the subelement
           must not have to be considered a match.

      :Yields:
         *list of str* -- The path lists to any matching subelements.

   **json(fp=None, indent=None, separators=(u', ', u': '))**

      Converts the DataModelDict to JSON content.

      :Parameters:
         * **fp** (*file-like object** or **None**, **optional*) -- An
           open file to write the content to.  If None (default), then
           the content is returned as a str.

         * **indent** (*int** or **None**, **optional*) -- Number of
           spaces to indent lines.  If None (default), the content
           will be inline.

         * **separators** (*tuple of str**, **optional*) -- Allows for
           item_separator and dict_separator) to be changed. Default
           is (', ', ': ').

      :Returns:
         The JSON content (only returned if fp is None).

      :Return type:
         str, optional

   **load(model, format=None)**

      Read in values from a json/xml string or file-like object.

      :Parameters:
         * **model** (*str** or **file-like object*) -- The XML or
           JSON content to read.  This is allowed to be either a file
           path, a string representation, or an open file-like object
           in byte mode.

         * **format** (*str** or **None**, **optional*) -- Allows for
           the format of the content to be explicitly stated ('xml' or
           'json').  If None (default), will try to determine which
           format based on if the first character of model is '<' or
           '{'.

      :Raises:
         ``ValueError`` -- If format is None and unable to identify
         XML/JON content, or if format is not equal to 'xml' or
         'json'.

   **path(key, yes={}, no={})**

      Return the path list of a subelement at any level uniquely
      identified by the specified conditions. Issues an error if
      either no match, or multiple matches are found.

      :Parameters:
         * **key** -- Dictionary key to search for.

         * **yes** (*dict*) -- Key-value terms which the subelement
           must have to be considered a match.

         * **no** (*dict*) -- Key-value terms which the subelement
           must not have to be considered a match.

      :Returns:
         The subelement path list to the uniquely identified
         subelement.

      :Return type:
         list of str

      :Raises:
         ``ValueError`` -- If exactly one matching subelement is not
         identified.

   **paths(key, yes={}, no={})**

      Return a list of all path lists of all elements at any level
      identified by the specified conditions.

      :Parameters:
         * **key** -- Dictionary key to search for.

         * **yes** (*dict*) -- Key-value terms which the subelement
           must have to be considered a match.

         * **no** (*dict*) -- Key-value terms which the subelement
           must not have to be considered a match.

      :Returns:
         The path lists for any matching subelements.

      :Return type:
         list

   **xml(fp=None, indent=None, full_document=True)**

      Return the DataModelDict as XML content.

      :Parameters:
         * **fp** (*file-like object** or **None**, **optional*) -- An
           open file to write the content to.  If None (default), then
           the content is returned as a str.

         * **indent** (*int** or **None**, **optional*) -- Number of
           spaces to indent lines.  If None (default), the content
           will be inline.

         * **full_document** (*bool**, **otional*) -- Indicates if the
           output is associated with a full xml model.  If True
           (default), the content can have only one root, and a header
           is added.

      :Returns:
         The XML content (only returned if fp is None).

      :Return type:
         str, optional
