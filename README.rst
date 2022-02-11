
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
downloaded at `https://github.com/usnistgov/DataModelDict
<https://github.com/usnistgov/DataModelDict>`_.


Conversions
===========

Some considerations need to be taken into account for designing data
models that allow for exact reversible transformations between the
three formats:

* Valid, full XML requires that there is exactly one root element.
   In other words, the top-level DataModelDict of a data model   can
   have only one key.

* Do not use lists of lists for representing data.  The XML
   conversions are only reversible for lists of values or lists of
   dictionaries.  Future updates may allow this.

* Avoid using XML attributes if possible.  While the XML conversions
   do reversibly handle attributes, it complicates the Python and JSON
   representations.

* Embedded XML content, i.e. “text with <embed>embedded</embed>
   content”, might not be reversible:

   ..
      * If this is in a Python/JSON value, converting to XML gives
         “text with
         &amp;lt;embed&amp;gt;embedded&amp;lt;/embed&amp;gt; content”.
         This is reversible.

      * If this is an XML text field, parsing to Python pulls the
         embedded elements out of the text, which is not reversible!

* XML subelements of the same name within an element should be given
   consecutively.  When parsed, all values of subelements of the same
   name are collected together in a list.  This will alter the
   original order of subelements if matching names were not originally
   consecutive.


Conversion from Python to JSON
------------------------------

The Python-JSON conversions use the standard Python JSON library.  In
converting from Python to JSON, all elements of the DataModelDict must
be an instance of a supported data type.

+------------------+-----------+
| Python           | JSON      |
+==================+===========+
| dict             | object    |
+------------------+-----------+
| list, tuple      | array     |
+------------------+-----------+
| str              | string    |
+------------------+-----------+
| int, float       | number    |
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
| str              | text             |
+------------------+------------------+
| int, float       | repr(val)        |
+------------------+------------------+
| True             | ‘true’           |
+------------------+------------------+
| False            | ‘false’          |
+------------------+------------------+
| None             | ‘’               |
+------------------+------------------+
| np.nan           | ‘NaN’            |
+------------------+------------------+
| np.inf           | ‘Infinity’       |
+------------------+------------------+
| -np.inf          | ‘-Infinity’      |
+------------------+------------------+

Some characters in the XML text fields will also be converted to avoid
conflicts.

* XML limited characters such as <, > and & are converted to their
   HTML entities.

* n, t, r are converted to \n, \t, and \r

Any dictionary keys starting with ‘@’ will be converted into XML
attributes, and the dictionary key ‘#text’ is interpreted as the text
value of the element.


Conversion from JSON to Python
------------------------------

The Python-JSON conversions use the standard Python JSON library.  In
converting from JSON to Python, the conversions of types is
straight-forward.

+---------------+---------------+
| JSON          | Python        |
+===============+===============+
| object        | DataModelDict |
+---------------+---------------+
| array         | list          |
+---------------+---------------+
| string        | str           |
+---------------+---------------+
| number (int)  | int           |
+---------------+---------------+
| number (real) | float         |
+---------------+---------------+
| true          | True          |
+---------------+---------------+
| false         | False         |
+---------------+---------------+
| null          | None          |
+---------------+---------------+
| NaN           | np.nan        |
+---------------+---------------+
| Infinity      | np.inf        |
+---------------+---------------+
| -Infinity     | -np.inf       |
+---------------+---------------+


Conversion from XML to Python
-----------------------------

The Python-XML conversions use the xmltodict Python package.  The text
fields will be interpreted based on the following sequential tests:

+------------------------------------------+----------+
| XML text                                 | Python   |
+==========================================+==========+
| text == ‘True’ or ‘true’                 | True     |
+------------------------------------------+----------+
| text == ‘False’ or ‘false’               | False    |
+------------------------------------------+----------+
| text == ‘’                               | None     |
+------------------------------------------+----------+
| text == ‘NaN’                            | np.nan   |
+------------------------------------------+----------+
| text == ‘Infinity’                       | np.inf   |
+------------------------------------------+----------+
| text == ‘-Infinity’                      | -np.inf  |
+------------------------------------------+----------+
| try int(text) and text == str(int(text)) | int      |
+------------------------------------------+----------+
| try float(text)                          | float    |
+------------------------------------------+----------+
| otherwise                                | str      |
+------------------------------------------+----------+

The int conversion test was updated for version 0.9.8 to check that
the values can reversably be changed back into a str.  This is
necessary to properly handle values, such as journal page numbers,
that may contain leading zeroes.

The reverse conversions are done for the special characters mentioned
in the Conversion from Python to XML section above.

Any ‘attr’ attribute fields are converted to elements named ‘@attr’
and corresponding ‘#text’ elements are created if needed.


Class Documentation
===================

**class DataModelDict.DataModelDict(*args, kwargs)**

   Bases: ``collections.OrderedDict``

   Class for handling json/xml equivalent data structures.

   **append(key, value)**

      Adds a value for element key by either adding key to the
      dictionary or appending the value as a list to any current
      value.

      :Parameters:
         * **key** (*str*) – The dictionary key.

         * **value** – The value to add to the dictionary key.  If
            key exists, the element is converted to a list if needed
            and value is appended.

   **aslist(key)**

      Gets the value of a dictionary key as a list.  Useful for
      elements whose values may or may not be lists.

      :Parameters:
         **key** (*str*) – Dictionary key

      :Returns:
         The dictionary’s element value or [value] depending on if it
         already is a list.

      :Return type:
         list

   **find(key, yes={}, no={})**

      Return the value of a subelement at any level uniquely
      identified by the specified conditions.

      :Parameters:
         * **key** (*str*) – Dictionary key to search for.

         * **yes** (*dict*) – Key-value terms which the subelement
            must have to be considered a match.

         * **no** (*dict*) – Key-value terms which the subelement
            must not have to be considered a match.

      :Returns:
         The value of the uniquely identified subelement.

      :Return type:
         any

      :Raises:
         **ValueError** – If exactly one matching subelement is not
         identified.

   **finds(key, yes={}, no={})**

      Finds the values of all subelements at any level identified by
      the specified conditions.

      :Parameters:
         * **key** (*str*) – Dictionary key to search for.

         * **yes** (*dict*) – Key-value terms which the subelement
            must have to be considered a match.

         * **no** (*dict*) – Key-value terms which the subelement
            must not have to be considered a match.

      :Returns:
         The values of any matching subelements.

      :Return type:
         list

   **iteraslist(key)**

      Iterates through the values of a dictionary key.  Useful for
      elements whose values may or may not be lists.

      :Parameters:
         **key** (*str*) – Dictionary key

      :Yields:
         *any* – The dictionary’s value or each element in value if
         value is a list.

   **iterfinds(key, yes={}, no={})**

      Iterates over the values of all subelements at any level
      identified by the specified conditions.

      :Parameters:
         * **key** (*str*) – Dictionary key to search for.

         * **yes** (*dict*) – Key-value terms which the subelement
            must have to be considered a match.

         * **no** (*dict*) – Key-value terms which the subelement
            must not have to be considered a match.

      :Yields:
         *any* – The values of any matching subelements.

   **iterpaths(key, yes={}, no={})**

      Iterates over the path lists to all elements at any level
      identified by the specified conditions.

      :Parameters:
         * **key** (*str*) – Dictionary key to search for.

         * **yes** (*dict*) – Key-value terms which the subelement
            must have to be considered a match.

         * **no** (*dict*) – Key-value terms which the subelement
            must not have to be considered a match.

      :Yields:
         *list of str* – The path lists to any matching subelements.

   **itervaluepaths()**

      Iterates over path lists to all value elements at any level.

      :Yields:
         *list* – The path lists to all value subelements.

   **json(fp=None, *args, kwargs)**

      Converts the DataModelDict to JSON content.

      :Parameters:
         * **fp** (*file-like object or None, optional*) – An
            open file to write the content to.  If None (default),
            then the content is returned as a str.

         * ***args** (*any*) – Any other positional arguments
            accepted by json.dump(s)

         * ****kwargs** (*any*) – Any other keyword arguments
            accepted by json.dump(s)

      :Returns:
         The JSON content (only returned if fp is None).

      :Return type:
         str, optional

   **load(model, format=None)**

      Read in values from a json/xml string or file-like object.

      :Parameters:
         * **model** (*str or file-like object*) – The XML or
            JSON content to read.  This is allowed to be either a file
            path, a string representation, or an open file-like object
            in byte mode.

         * **format** (*str or None, optional*) – Allows for
            the format of the content to be explicitly stated (‘xml’
            or ‘json’).  If None (default), will try to determine
            which format based on if the first character of model is
            ‘<’ or ‘{‘.

      :Raises:
         **ValueError** – If format is None and unable to identify
         XML/JON content, or if     format is not equal to ‘xml’ or
         ‘json’.

   **path(key, yes={}, no={})**

      Return the path list of a subelement at any level uniquely
      identified by the specified conditions. Issues an error if
      either no match, or multiple matches are found.

      :Parameters:
         * **key** (*str*) – Dictionary key to search for.

         * **yes** (*dict*) – Key-value terms which the subelement
            must have to be considered a match.

         * **no** (*dict*) – Key-value terms which the subelement
            must not have to be considered a match.

      :Returns:
         The subelement path list to the uniquely identified
         subelement.

      :Return type:
         list of str

      :Raises:
         **ValueError** – If exactly one matching subelement is not
         identified.

   **paths(key, yes={}, no={})**

      Return a list of all path lists of all elements at any level
      identified by the specified conditions.

      :Parameters:
         * **key** (*str*) – Dictionary key to search for.

         * **yes** (*dict*) – Key-value terms which the subelement
            must have to be considered a match.

         * **no** (*dict*) – Key-value terms which the subelement
            must not have to be considered a match.

      :Returns:
         The path lists for any matching subelements.

      :Return type:
         list

   **xml(fp=None, indent=None, kwargs)**

      Return the DataModelDict as XML content.

      :Parameters:
         * **fp** (*file-like object or None, optional*) – An
            open file to write the content to.  If None (default),
            then the content is returned as a str.

         * **indent** (*int, str or None, optional*) – If
            int, number of spaces to indent lines.  If str, will use
            that as the indentation. If None (default), the content
            will be inline.

         * ****kwargs** (*any*) – Other keywords supported by
            xmltodict.unparse, except for output which is replaced by
            fp, and preprocessor, which is controlled.

      :Returns:
         The XML content (only returned if fp is None).

      :Return type:
         str, optional

**DataModelDict.joinpath(path, delimiter='.', openbracket='[',
closebracket=']')**

   Takes a path as a list and transforms it into a string.

   :Parameters:
      * **path** (*list*) – The path list to join.

      * **delimiter** (*str*) – The delimiter between subsequent
         element names.

      * **openbracket** (*str*) – The opening indicator of list
         indices.

      * **closebracket** (*str*) – The closing indicator of list
         indices.

**DataModelDict.parsepath(pathstr, delimiter='.', openbracket='[',
closebracket=']')**

   Takes a path as a string and parses it into a list of terms.

   :Parameters:
      * **pathstr** (*str*) – The path string to parse.

      * **delimiter** (*str*) – The delimiter between subsequent
         element names.

      * **openbracket** (*str*) – The opening indicator of list
         indices.

      * **closebracket** (*str*) – The closing indicator of list
         indices.

**DataModelDict.uber_open_rmode(data: Union[str, bytes, pathlib.Path,
io.IOBase]) -> io.IOBase**

   Provides a uniform means of reading data from files, file-like
   objects, and string/bytes content.

   :Parameters:
      **data** (*file-like object, file path, or str/bytes
      file content*) – The data that will be opened for reading.

   :Returns:
      An open file-like object that is in a bytes read mode.  If a
      file-like object is given, it is passed through after checking
      that it is for bytes content.  If a file path is given, the file
      is opened in ‘rb’ mode.  If bytes or string content is given,
      the content is returned in a BytesIO object.

   :Return type:
      file-like object

   :Raises:
      * **ValueError** – If a file-like object in text mode is given.

      * **TypeError** – If data is not a file-like object, bytes, str
         or Path.

      * **FileNotFoundError** – If data is a pathlib.Path object and
         is not an existing file.
