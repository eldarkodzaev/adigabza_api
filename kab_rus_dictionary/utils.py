import re


def normalize_string(string: str) -> str:
    """
    Удаляет из строки символы разрывов строк и заменяет двойные пробелы на одинарные
    """
    return re.sub(r"^\s+|\n|\r|\s+$", '', string).replace("  ", " ")
