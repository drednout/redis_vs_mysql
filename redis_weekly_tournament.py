import collections
import datetime

from twisted.python import log
from twisted.internet import defer

from ro.engine.utils import load_config
import redisapi


class FakeFactory(object):
    pass

#server-side rudiment, needed for sharing
#data between sessions and containing 
factory = FakeFactory()

def get_pvp_rating_name():
    """Obtains the name of current weekly PVP-rating.
    """
    today = datetime.datetime.now()
    year, week, _ = today.isocalendar()
    return "global_pvp_rating:%d:%d" % (year, week)



@defer.inlineCallbacks
def reset_weekly_tournament():
    global factory
    yield factory.redis_db.flushdb()


@defer.inlineCallbacks
def get_weekly_tournament_page(person_id, page_num, page_size=10):
    global factory

    rating_page = []
    person_rating_info = {
        "person_id": person_id,
    }
    res = {}
    res["@rating_page"] = rating_page
    res["@my"] = person_rating_info

    start_pos = page_num * page_size
    end_pos = (page_num + 1) * page_size - 1
    raw_res = yield factory.redis_db.zrevrange(get_pvp_rating_name(), start_pos, end_pos, withscores=True)
  
    cur_pos = 0
    for page_person_id, rating_score in raw_res:
        page_person_id = int(page_person_id)
        rating_page.append({"person_id": page_person_id, "pvp_rating": rating_score, 
                             "rank": page_num*page_size + cur_pos + 1})
        cur_pos += 1
     
    if not rating_page:
        defer.returnValue(res)


    rank = yield factory.redis_db.zrevrank(get_pvp_rating_name(), person_id)
    if rank is not None:
        person_rating_info["rank"] = int(rank) + 1
    score = yield factory.redis_db.zscore(get_pvp_rating_name(), person_id)
    if score is not None:
        person_rating_info["score"] = int(score)

    
    defer.returnValue(res)



@defer.inlineCallbacks
def update_weekly_tournament(person_id, delta):
    yield factory.redis_db.zincr(get_pvp_rating_name(), person_id, delta)



@defer.inlineCallbacks
def setUp():
    global factory

    config = load_config("redis_conf.yml")
    redis_conn = redisapi.RedisConnection(config["redis"]["host"],
                                          config["redis"]["port"],
                                          config["redis"]["password"],
                                          factory, "redis_db",
                                          db=config["redis"]["db"],
                                          use_hiredis=config["redis"]["use_hiredis"])
    yield redis_conn.connect()
    yield factory.redis_db.select(config["redis"]["db"])
