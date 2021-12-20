def dict_min_length(values: dict = None,
                    keys: list = [],
                    minimum_length: int = 1):
    if not (dict_contain_keys(values, keys) and values):
        return False

    for i, (key, value) in enumerate(values.items()):
        if not value or len(value) < minimum_length:
            return False

    return True


def dict_contain_keys(values: dict = None, keys: list = []):
    return True if all(key in values for key in keys) else False
