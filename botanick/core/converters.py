def tostring(output):
    """
    Convert list of results to string output
    """
    return ", ".join(list(set(output))).replace('\n', '')
