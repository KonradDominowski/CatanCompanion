from os import PathLike
from pathlib import Path
from typing import Iterable

from Catan.PlayerColor import PlayerColor
from Widgets.Game.Resource import ResourceType
from custom_types import ResourcesDict


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


def sort_resource_counts_desc(resources: ResourcesDict) -> ResourcesDict:
    """
    Returns a new dict where each player's resources are sorted in descending order by count.

    :param resources: A dict mapping players to their resource counts.
    :return: A new dict with sorted inner dicts by descending resource count.
    """
    return {
        player: dict(
            sorted(player_resources.items(), key=lambda item: item[1], reverse=True)
        )
        for player, player_resources in resources.items()
    }


def empty_resources_dict(player_colors: Iterable[PlayerColor]) -> ResourcesDict:
    """
    Creates an empty resource dictionary for each player color.

    For each player color provided, this function creates a dictionary of all resource types,
    with each resource initialized to 0.

    :param player_colors: An iterable of player colors (e.g. list of PlayerColor values).
    :type player_colors: Iterable[PlayerColor]
    :return: A dictionary mapping each player color to a resource count dictionary initialized with zeros.
    :rtype: ResourcesDict
    """
    return {
        color: {resource: 0 for resource in ResourceType}
        for color in player_colors
    };
