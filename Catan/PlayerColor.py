from enum import StrEnum


class PlayerColor(StrEnum):
    WHITE = 'white'
    ORANGE = 'orange'
    BLUE = 'blue'
    RED = 'red'

    @property
    def hex(self) -> str:
        return {
            PlayerColor.WHITE: '#FFFFFF',
            PlayerColor.ORANGE: '#FFA500',
            PlayerColor.BLUE: '#0000FF',
            PlayerColor.RED: '#FF0000'
        }[self]

    @property
    def r(self) -> int:
        return {
            PlayerColor.WHITE: 255,
            PlayerColor.ORANGE: 255,
            PlayerColor.BLUE: 0,
            PlayerColor.RED: 255,
        }[self]

    @property
    def g(self) -> int:
        return {
            PlayerColor.WHITE: 255,
            PlayerColor.ORANGE: 165,
            PlayerColor.BLUE: 0,
            PlayerColor.RED: 0,
        }[self]

    @property
    def b(self) -> int:
        return {
            PlayerColor.WHITE: 255,
            PlayerColor.ORANGE: 0,
            PlayerColor.BLUE: 255,
            PlayerColor.RED: 0,
        }[self]
