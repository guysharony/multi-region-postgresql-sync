def as_list_of_string(val) -> list:
    if isinstance(val, (str, int, float)):
        return [val]
    elif all(isinstance(table, (str, int, float)) for table in val):
        return val
    else:
        raise TypeError('Parameter should be a string or a list of string.')
