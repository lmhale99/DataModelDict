from importlib.metadata import version
__version__ = version('DataModelDict')

from .uber_open_rmode import uber_open_rmode
from .parsepath import parsepath
from .joinpath import joinpath
from .DataModelDict import DataModelDict

__all__ = ['DataModelDict', 'uber_open_rmode', 'parsepath', 'joinpath']
