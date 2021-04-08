import json

from model.game_record import GameRecord
from service import ranking_service

from handler import response


def addGameRecord(event, context):
    newGameRecord = GameRecord(event["game"], event["userId"], event["score"])

    ranking = ranking_service.addGameRecord(newGameRecord)

    return response.created(json.dumps(ranking.toJson()))


def top10(event, context):
    game = __getPathParameter(event, "game")

    return response.ok(json.dumps([ranking.toJson() for ranking in ranking_service.top10(game)]))


def my(event, context):
    game = __getPathParameter(event, "game")
    userId = __getPathParameter(event, "userId")

    ranking = ranking_service.my(game, userId)

    return response.ok(None if ranking is None else json.dumps(ranking.toJson()))


def __getPathParameter(event, parameter: str):
    return event["pathParameters"][parameter]
