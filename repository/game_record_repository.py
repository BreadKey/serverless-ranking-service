import os
from typing import List, Tuple

import pymysql
from model.game_record import GameRecord

from enum import Enum

__RANKING_DB = pymysql.connect(
    host=os.environ.get("host", "localhost"),
    user=os.environ.get("user", "root"),
    port=int(os.environ.get("port", 3306)),
    passwd=os.environ.get("password", ""),
    db=os.environ.get("database", "ranking")
)


class Order(Enum):
    ASC = 1
    DESC = 2


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
            __selectBuilder(GameRecord,
                           where={"game": game},
                           orderBy=("score", Order.DESC),
                           limit=count)
        )

    return list(map(__gameRecordFromRow, cursor.fetchall()))


def findTopByGameAndUserId(game: str, userId: str) -> GameRecord:
    with __RANKING_DB.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(
            __selectBuilder(GameRecord,
                           where={"game": game, "userId": userId},
                           orderBy=("score", Order.DESC),
                           limit=1)
        )

    row = cursor.fetchone()

    return None if row is None else __gameRecordFromRow(row)


def __gameRecordFromRow(row) -> GameRecord:
    return GameRecord(row["game"], row["userId"], row["score"], row["id"])

def __selectBuilder(
        entity,
        select: List[str] = [],
        where: dict = {},
        orderBy: Tuple[str, Order] = None,
        limit: int = None) -> str:
    query = "select "
    query += '*' if len(select) == 0 else ",".join(select)
    query += f' from {entity.__name__}s '

    if (len(where) > 0):
        query += "where " + " and ".join(
            list(
                map(lambda key:
                    f'{key} = ' +
                    (f'"{where[key]}"' if isinstance(
                        where[key], str) else f'{where[key]}'),
                    where)
            )
        )

    if (orderBy is not None):
        query += f" order by {orderBy[0]} {orderBy[1].name}"

    if (limit is not None):
        query += f" limit {limit}"

    return query
