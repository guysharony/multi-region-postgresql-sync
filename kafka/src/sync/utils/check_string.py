def is_special(value: str) -> bool:
    pattern = " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    return any((c in set(pattern)) for c in value)


def is_ascii(value: str) -> bool:
    return all(ord(c) < 128 for c in value)


def is_string(val) -> bool:
    return val and (type(val) == str)


def is_string_list(items) -> bool:
    return all(isinstance(item, str) for item in items)
