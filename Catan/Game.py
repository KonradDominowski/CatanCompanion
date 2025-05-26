from Catan.PlayerColor import PlayerColor


class Game:
    def __init__(self, players: dict[PlayerColor, str]):
        super().__init__()

        self._players = players

    def get_players(self) -> dict[PlayerColor, str]:
        return self._players
    