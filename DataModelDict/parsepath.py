def parsepath(pathstr, delimiter='.', openbracket='[', closebracket=']'):
    """
    Takes a path as a string and parses it into a list of terms.
    
    Parameters
    ----------
    pathstr : str
        The path string to parse.
    delimiter : str
        The delimiter between subsequent element names.
    openbracket : str
        The opening indicator of list indices.
    closebracket : str
        The closing indicator of list indices.
    """
    # Split by delimiter
    path = pathstr.split(delimiter)
    
    # Search for bracketed index values and their insertion positions
    positions = []
    values = []
    for i in range(len(path)):
        
        # Check if path field ends with the closebracket
        if path[i][-len(closebracket):] == closebracket:
            s = 0
            cropindex = None
            while True:
                
                # Search for openbracket
                try:
                    index = path[i][s:].index(openbracket)
                except:
                    break
                else:
                    # Set cropindex if needed
                    if cropindex is None:
                        cropindex = index
                        
                    # Identify starting index for the number
                    s = index + len(openbracket) + s
                         
                # Search for the next closebracket
                e = path[i][s:].index(closebracket) + s
                
                # Extract int value and set the insertion position
                values.append(int(path[i][s:e]))
                positions.append(i+1)
                
                # Set cropindex if needed
                if cropindex is None:
                    cropindex = s - len(openbracket) + 1
                
                # Shift s
                s = e
            
            # Crop the current path field
            path[i] = path[i][:cropindex]
            
    # Loop over positions and values in reverse
    for position, value in zip(reversed(positions), reversed(values)):
        path.insert(position, value)
        
    return path