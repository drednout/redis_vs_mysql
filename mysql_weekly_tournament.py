import logging
import datetime
import random

from twisted.internet import defer
from twisted.python import log

from ro.engine.dbapi import ConnectionPool
from ro.engine.utils import load_config


class FakeFactory(object):
    pass

#server-side rudiment, needed for sharing
#data between sessions and containing 
factory = FakeFactory()

persons_in_tournament = set()


def get_tournament_id():
    """Calculate the current weekly tournament identifier.
    """
    today = datetime.datetime.now()
    year, week, _ = today.isocalendar()
    return int(str(year) + str(week))


def get_prev_tournament_id():
    """Calculate the current weekly tournament identifier.
    """
    yesterweek = datetime.datetime.now() - datetime.timedelta(days=7)
    year, week, _ = yesterweek.isocalendar()
    return int(str(year) + str(week))


@defer.inlineCallbacks
def reset_weekly_tournament():
    yield factory.dbpool.runOperation("TRUNCATE TABLE weekly_tournament")
    persons_in_tournament.clear()


@defer.inlineCallbacks
def update_weekly_tournament(person_id, money_earned):
    global persons_in_tournament
    tournament_id = get_tournament_id()
    if person_id not in persons_in_tournament:
        sql_cmd = """INSERT INTO weekly_tournament (tournament_id, person_id) VALUES
                     (%(tournament_id)s, %(person_id)s)"""
        yield factory.dbpool.runOperation(sql_cmd, {"tournament_id": tournament_id,
                                                    "person_id": person_id, 
                                                    "money_earned": money_earned})
        persons_in_tournament.add(person_id)
    else:
        sql_cmd = """UPDATE weekly_tournament SET money_earned=money_earned+%(money_earned)s WHERE
                     person_id=%(person_id)s and tournament_id=%(tournament_id)s"""
        yield factory.dbpool.runOperation(sql_cmd, {"tournament_id": tournament_id,
                                                    "person_id": person_id,
                                                    "money_earned": money_earned})

       
@defer.inlineCallbacks
def get_weekly_tournament_page(person_id, page_num, page_size=10):
    sql_cmd = """SELECT person_id, money_earned FROM weekly_tournament WHERE
                 tournament_id=%(tournament_id)s ORDER 
                 BY money_earned DESC LIMIT %(offset)s, %(page_size)s""" 

    tournament_id = get_tournament_id()
    offset = page_num * page_size
    raw_res = yield factory.dbpool.runQuery(sql_cmd, {"tournament_id": tournament_id, "offset": offset,
                                                      "page_size": page_size})
    for rank, row in enumerate(raw_res, 1):
        row["rank"] = rank + page_num*page_size


    sql_cmd = """SELECT wo.money_earned, 
                    (SELECT COUNT(*) + 1 FROM weekly_tournament wi WHERE 
                     wi.tournament_id=%(tournament_id)s AND
                     (wi.money_earned, wi.person_id) > (wo.money_earned, wo.person_id)) AS
                     rank
                 FROM weekly_tournament wo WHERE
                 wo.tournament_id=%(tournament_id)s AND wo.person_id=%(person_id)s"""
   
    person_info = yield factory.dbpool.runQuery(sql_cmd, {"person_id": person_id,
                                                          "tournament_id": tournament_id})
    
    res = {}
    res["@rating_page"] = raw_res
    res["@my"] = person_info

    defer.returnValue(res)


@defer.inlineCallbacks
def setUp():
    global factory, persons_in_tournament
    config = load_config("mysql_conf.yml")
    factory.dbpool = ConnectionPool(config["mysql"]["host"],
                                    config["mysql"]["db"], 
                                    config["mysql"]["user"], 
                                    config["mysql"]["password"])

    sql_cmd = """SELECT person_id FROM weekly_tournament WHERE 
                 tournament_id=%(tournament_id)s"""
    res = yield factory.dbpool.runQuery(sql_cmd, {"tournament_id": get_tournament_id()})
    for row in res:
        persons_in_tournament.add(row["person_id"])

    log.msg("DEBUG: len of persons_in_tournament is {0}".format(len(persons_in_tournament)))
