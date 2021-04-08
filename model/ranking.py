from model.game_record import GameRecord


class Ranking:
    def __init__(self, number: int, gameRecord: GameRecord):
        self.number = number
        self.gameRecord = gameRecord

    def toJson(self):
        return {
            "number": self.number,
            "gameRecord": self.gameRecord.__dict__
        }