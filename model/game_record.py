class GameRecord:
    def __init__(self, game: str, userId: str, score: int, id: int = None):
        self.game = game
        self.userId = userId
        self.score = score
        self.id = id
