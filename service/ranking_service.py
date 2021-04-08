from model.ranking import Ranking
from model.game_record import GameRecord
from repository import game_record_repository
from typing import List

max_ranking_number = 1000

def addGameRecord(gameRecord: GameRecord) -> Ranking:
    savedGameRecord = game_record_repository.save(gameRecord)
    orderByScoreDesc = game_record_repository.findByGameOrderByScoreDesc(gameRecord.game, max_ranking_number)

    rankingNumber: int = __calculateRankingNumber(orderByScoreDesc, savedGameRecord)

    return Ranking(rankingNumber, savedGameRecord)

def top10(game: str) -> List[Ranking]:
    records = game_record_repository.findByGameOrderByScoreDesc(game, 10)

    return [Ranking(i + 1, record) for i, record in enumerate(records)]

def my(game: str, userId: str) -> Ranking:
    myTopRecord = game_record_repository.findTopByGameAndUserId(game, userId)

    if (myTopRecord is None): return None

    orderByScoreDesc = game_record_repository.findByGameOrderByScoreDesc(game, max_ranking_number)

    rankingNumber: int = __calculateRankingNumber(orderByScoreDesc, myTopRecord)

    return Ranking(rankingNumber, myTopRecord)

def __calculateRankingNumber(orderByScoreDesc: List[GameRecord], gameRecord: GameRecord) -> int:
    if (orderByScoreDesc[-1].score > gameRecord.score):
        return None
    
    start: int = 0
    end: int = len(orderByScoreDesc) - 1

    while(start < end):
        mid = (start + end) // 2

        if (orderByScoreDesc[mid].score > gameRecord.score):
            start = mid + 1
        else:
            end = mid - 1

    return start + 1