# coding: utf-8
from importlib import resources
__all__ = ['DataModelDict', 'uber_open_rmode', 'parsepath', 'joinpath']

# Read version from VERSION file
if hasattr(resources, 'files'):
    __version__ = resources.files('DataModelDict').joinpath('VERSION').read_text(encoding='UTF-8')
else:
    __version__ = resources.read_text('DataModelDict', 'VERSION', encoding='UTF-8').strip()

# Local imports
from .uber_open_rmode import uber_open_rmode
from .parsepath import parsepath
from .joinpath import joinpath
from .DataModelDict import DataModelDict