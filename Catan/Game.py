from Catan.PlayerColor import PlayerColor


class Game:
    def __init__(self, players: dict[PlayerColor, str]):
        super().__init__()

        self._players = players
        self._players_list = list(players.values())
        self._player_colors = list(players.keys())

    def get_players(self) -> dict[PlayerColor, str]:
        return self._players

    def get_colors(self):
        return self._player_colors
