def joinpath(path:list, delimiter:str='.', openbracket:str='[',
             closebracket:str=']') -> str:
    """
    Takes a path as a list and transforms it into a string.
    
    Parameters
    ----------
    path : list
        The path list to join.
    delimiter : str
        The delimiter between subsequent element names.
    openbracket : str
        The opening indicator of list indices.
    closebracket : str
        The closing indicator of list indices.
    
    Returns
    -------
    The path as a delimited string.
    """
    # Start str as first element of path list
    pathstr = path[0]
    
    # Loop over subsequent list elements
    for i in range(1, len(path)):
        
        # Append str element names using the delimiter
        if isinstance(path[i], str):
            pathstr += f'{delimiter}{path[i]}'
            
        # Append int index terms inside the specified brackets
        elif isinstance(path[i], int):
            pathstr += f'{openbracket}{path[i]}{closebracket}'
        
        # Raise error for other element tyles
        else:
            raise TypeError('path fields limited to str names or int indices')
            
    return pathstr