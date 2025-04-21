from os import PathLike
from pathlib import Path


def read_css_file(file_path: str | PathLike[str]) -> str:
    """
    Reads the contents of a CSS file and returns it as a string.

    Parameters:
        file_path (str): The path to the CSS file.

    Returns:
        str: The contents of the CSS file.
    """
    path = Path(file_path)
    return path.read_text(encoding='utf-8')
