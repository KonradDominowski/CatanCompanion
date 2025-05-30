from typing import TypeAlias

from Catan import PlayerColor
from Widgets.Game.Resource import ResourceType

ResourcesDict: TypeAlias = dict[PlayerColor, dict[ResourceType, int]]
