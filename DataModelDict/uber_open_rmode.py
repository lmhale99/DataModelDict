from pathlib import Path
from typing import Union
import io
from contextlib import contextmanager

@contextmanager
def uber_open_rmode(data:Union[str, bytes, Path, io.IOBase]) -> io.IOBase:
    """
    Provides a uniform means of reading data from files, file-like objects,
    and string/bytes content.  
    
    Parameters
    ----------
    data : file-like object, file path, or str/bytes file content
        The data that will be opened for reading.

    Returns
    -------
    file-like object
        An open file-like object that is in a bytes read mode.  If a file-like
        object is given, it is passed through after checking that it is for
        bytes content.  If a file path is given, the file is opened in 'rb'
        mode.  If bytes or string content is given, the content is returned
        in a BytesIO object.

    Raises
    ------
    ValueError
        If a file-like object in text mode is given.
    TypeError
        If data is not a file-like object, bytes, str or Path.
    FileNotFoundError
        If data is a pathlib.Path object and is not an existing file.
    """
    
    # Define is_file function
    def is_file(data):
        """Tests if data is a file path. Invalid paths return False instead of raising errors"""
        try:
            return Path(data).is_file()
        except ValueError:
            return False
    
    # Check if data is a file-like object
    if isinstance(data, io.IOBase):
        
        # Check that object is not a subclass of TextIOBase
        if isinstance(data, io.TextIOBase):
            raise ValueError('open file-like objects need to be in a bytes mode not text mode')
        
        f = data
        to_close = False

    # Check if data is a str
    elif isinstance(data, str):
        
        # Check if str data is a file path
        if is_file(data):
            f = open(data, 'rb')
            to_close = True
        
        # Encode to bytes and read using BytesIO
        else:
            f = io.BytesIO(data.encode())
            to_close = True
    
    # Check if data is a Path    
    elif isinstance(data, Path):
        
        # Check if path is a file 
        if data.is_file():
            f = open(data, 'rb')
            to_close = True

        else:
            raise FileNotFoundError(f"no such file '{data.as_posix}'")

    # If data is bytes, read using BytesIO
    elif isinstance(data, bytes):
        f = io.BytesIO(data)
        to_close = True

    else:
        raise TypeError('data must be a file-like object, str or bytes')
    
    # Return the open file-like object
    try:
        yield f
    
    # Close the file-like object if needed
    finally:
        if to_close:
            f.close()