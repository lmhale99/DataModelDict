from ast import parse
from DataModelDict import parsepath, joinpath

def test_path_manipulations():
    path1 = ['my-data-model', 1, 'measurement', 9, 7, 'length', 'unit']

    pathstr1 = joinpath(path1)
    path2 = parsepath(pathstr1)
    pathstr2 = joinpath(path2)

    assert path1 == path2
    assert pathstr1 == pathstr2