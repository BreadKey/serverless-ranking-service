import os
from typing import List

import pymysql
from model.game_record import GameRecord

__RANKING_DB = pymysql.connect(
    host=os.environ["host"],
    user=os.environ["user"],
    port=int(os.environ["port"]),
    passwd=os.environ.get("password", ""),
    db=os.environ["database"]
)


def save(gameRecord: GameRecord) -> GameRecord:
    with __RANKING_DB.cursor() as cursor:
        cursor.execute(
            f'insert into GameRecords (game, userId, score) values("{gameRecord.game}", "{gameRecord.userId}", {gameRecord.score})')
        id = cursor.lastrowid
        __RANKING_DB.commit()

    return GameRecord(gameRecord.game, gameRecord.userId, gameRecord.score, id)


def findByGameOrderByScoreDesc(game: str, count: int) -> List[GameRecord]:
    with __RANKING_DB.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(
            f'select * from GameRecords where game = "{game}" order by score desc limit {count}')

    return list(map(__gameRecordFromRow, cursor.fetchall()))


def findTopByGameAndUserId(game: str, userId: str) -> GameRecord:
    with __RANKING_DB.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(
            f'select * from GameRecords where game = "{game}" and userId = "{userId}" order by score desc limit 1'
        )

    row = cursor.fetchone()

    return None if row is None else __gameRecordFromRow(row)


def __gameRecordFromRow(row) -> GameRecord:
    return GameRecord(row["game"], row["userId"], row["score"], row["id"])
