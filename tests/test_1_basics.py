
import DataModelDict

def test_basics():
    assert isinstance(DataModelDict.__version__, str)
    assert 'uber_open_rmode' in DataModelDict.__all__
    assert 'DataModelDict' in DataModelDict.__all__
    