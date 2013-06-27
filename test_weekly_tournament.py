import sys
import datetime
import argparse
import random
import pprint

import yaml
from twisted.internet import reactor, defer
from twisted.python import log

import mysql_weekly_tournament 
import redis_weekly_tournament



def defer_sleep(secs):
    d = defer.Deferred()
    reactor.callLater(secs, d.callback, None)
    return d


@defer.inlineCallbacks
def mysql_init_test(*args, **kwargs):
    if "warmup_time" in kwargs:
        yield defer_sleep(int(kwargs["warmup_time"]))

    yield mysql_weekly_tournament.reset_weekly_tournament()
    start_person_id = 1
    if "start_person_id" in kwargs:
        start_person_id = int(kwargs["start_person_id"])
    end_person_id = 10**5
    if "end_person_id" in kwargs:
        end_person_id = int(kwargs["end_person_id"])

    money_at_least = 1
    if "money_at_least" in kwargs:
        money_at_least = int(kwargs["money_at_least"])
    money_at_most = 10**6
    if "money_at_most" in kwargs:
        money_at_most = int(kwargs["money_at_most"])

    log.msg("init_test: inserting {0} tournament records".format(end_person_id - start_person_id + 1))
    for person_id in xrange(start_person_id, end_person_id+1):
        yield mysql_weekly_tournament.update_weekly_tournament(person_id, random.randint(money_at_least, money_at_most))



@defer.inlineCallbacks
def redis_init_test(*args, **kwargs):
    if "warmup_time" in kwargs:
        yield defer_sleep(int(kwargs["warmup_time"]))

    yield redis_weekly_tournament.reset_weekly_tournament()
    start_person_id = 1
    if "start_person_id" in kwargs:
        start_person_id = int(kwargs["start_person_id"])
    end_person_id = 10**5
    if "end_person_id" in kwargs:
        end_person_id = int(kwargs["end_person_id"])

    money_at_least = 1
    if "money_at_least" in kwargs:
        money_at_least = int(kwargs["money_at_least"])
    money_at_most = 10**6
    if "money_at_most" in kwargs:
        money_at_most = int(kwargs["money_at_most"])

    log.msg("init_test: inserting {0} tournament records".format(end_person_id - start_person_id + 1))
    for person_id in xrange(start_person_id, end_person_id+1):
        yield redis_weekly_tournament.update_weekly_tournament(person_id, random.randint(money_at_least, money_at_most))


@defer.inlineCallbacks
def mysql_update_test(*args, **kwargs):
    if "warmup_time" in kwargs:
        yield defer_sleep(int(kwargs["warmup_time"]))

    start_person_id = 1
    if "start_person_id" in kwargs:
        start_person_id = int(kwargs["start_person_id"])
    end_person_id = 10**5
    if "end_person_id" in kwargs:
        end_person_id = int(kwargs["end_person_id"])

    log.msg("update_test: updating {0} tournament records".format(end_person_id - start_person_id + 1))
    for person_id in xrange(start_person_id, end_person_id+1):
        yield mysql_weekly_tournament.update_weekly_tournament(person_id, random.randint(0, 1000))


@defer.inlineCallbacks
def redis_update_test(*args, **kwargs):
    if "warmup_time" in kwargs:
        yield defer_sleep(int(kwargs["warmup_time"]))

    start_person_id = 1
    if "start_person_id" in kwargs:
        start_person_id = int(kwargs["start_person_id"])
    end_person_id = 10**5
    if "end_person_id" in kwargs:
        end_person_id = int(kwargs["end_person_id"])

    log.msg("update_test: updating {0} tournament records".format(end_person_id - start_person_id + 1))
    for person_id in xrange(start_person_id, end_person_id+1):
        yield redis_weekly_tournament.update_weekly_tournament(person_id, random.randint(0, 1000))



@defer.inlineCallbacks
def redis_smoke_test(*args, **kwargs):
    yield redis_weekly_tournament.update_weekly_tournament(1, 100)
    yield redis_weekly_tournament.update_weekly_tournament(1, -100)
    page = yield redis_weekly_tournament.get_weekly_tournament_page(1, 1)
    log.msg("page is {0}".format(pprint.pformat(page)))


@defer.inlineCallbacks
def mysql_smoke_test(*args, **kwargs):
    yield mysql_weekly_tournament.update_weekly_tournament(1, 100)
    yield mysql_weekly_tournament.update_weekly_tournament(1, -100)
    page = yield mysql_weekly_tournament.get_weekly_tournament_page(1, 1)
    log.msg("page is {0}".format(pprint.pformat(page)))


@defer.inlineCallbacks
def mysql_select_test(*args, **kwargs):
    if "warmup_time" in kwargs:
        yield defer_sleep(int(kwargs["warmup_time"]))

    start_person_id = 1
    if "start_person_id" in kwargs:
        start_person_id = int(kwargs["start_person_id"])

    end_person_id = 30
    if "end_person_id" in kwargs:
        end_person_id = int(kwargs["end_person_id"])

    page_count = 1000
    if "page_count" in kwargs:
        page_count = int(kwargs["page_count"]) 

    person_count = end_person_id - start_person_id + 1
    log.msg("person_count: selecting {0} rating pages X {1} persons".format(page_count, person_count))
    #counter = 1
    for i in range(page_count):
        for person_id in range(start_person_id, end_person_id + 1):
            page_index = random.randint(0, person_count/10)
            #start_time = datetime.datetime.now()
            yield mysql_weekly_tournament.get_weekly_tournament_page(person_id, page_index)
            #finish_time = datetime.datetime.now()
            #log.msg("{0}th rating page, spent {1}".format(counter, finish_time-start_time))
            #counter += 1




@defer.inlineCallbacks
def redis_select_test(*args, **kwargs):
    if "warmup_time" in kwargs:
        yield defer_sleep(int(kwargs["warmup_time"]))

    page_count = 1
    if "page_count" in kwargs:
        page_count = int(kwargs["page_count"]) 

    start_person_id = 1
    if "start_person_id" in kwargs:
        start_person_id = int(kwargs["start_person_id"])

    end_person_id = 30000
    if "end_person_id" in kwargs:
        end_person_id = int(kwargs["end_person_id"])

    person_count = end_person_id - start_person_id + 1
    log.msg("person_count: selecting {0} rating pages X {1} persons".format(page_count, person_count))
    for i in range(page_count):
        for person_id in range(start_person_id, end_person_id + 1):
            page_index = random.randint(0, person_count/10)
            yield redis_weekly_tournament.get_weekly_tournament_page(person_id, page_index)



@defer.inlineCallbacks
def main():
    supported_tests = {
        "mysql_init_test": mysql_init_test,
        "mysql_smoke_test": mysql_smoke_test,
        "mysql_select_test": mysql_select_test,
        "mysql_update_test": mysql_update_test,
        "redis_init_test": redis_init_test,
        "redis_smoke_test": redis_smoke_test,
        "redis_select_test": redis_select_test,
        "redis_update_test": redis_update_test,
    }
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument('-c', '--concurrency', metavar='NUM', default=1, type=int,
                            help='Specify the number of concurrent requests during the test.')
    arg_parser.add_argument('-n', '--run-count', metavar='NUM', default=1, type=int,
                            help='Specify the number of times which specified thest will be executed.')
    arg_parser.add_argument('-t', '--do-test', metavar='TEST_NAME', choices=supported_tests,
                            help='Execute specified test set on the current data set.')
    arg_parser.add_argument('-d', '--test-data', metavar='DATA', 
                            help='Specify test configuration data in YAML format')

    args = arg_parser.parse_args()
    if not args.do_test:
        arg_parser.print_help()
        sys.exit(1)
    
    yield mysql_weekly_tournament.setUp()
    yield redis_weekly_tournament.setUp()

    test_data = {}
    if args.test_data:
        test_data = yaml.load(args.test_data)


    for i in range(args.run_count):
        log.msg("Starting {0}, {1}th time with concurrency {2}".format(args.do_test, i + 1, args.concurrency))
        start = datetime.datetime.now()
        if args.concurrency == 1:
            yield supported_tests[args.do_test](**test_data)
        else:
            defer_list = []
            person_count = int(test_data["person_count"])
            shift = 0
            if "shift" in test_data:
                shift = int(test_data["shift"])
            for j in range(args.concurrency):
                test_data["start_person_id"] = j * (person_count/args.concurrency) + shift
                test_data["end_person_id"] = (j + 1) * (person_count/args.concurrency) - 1 + shift
                log.msg("Starting concurrent test {0} #{1}. start_person_id is {2}, end_person_id is {3}".format(\
                        args.do_test, j + 1, test_data["start_person_id"], test_data["end_person_id"]))
                d = supported_tests[args.do_test](**test_data)
                defer_list.append(d)
            
            for d in defer_list:
                yield d

        finish = datetime.datetime.now()
        time_spent = finish - start
        log.msg("Finished. Time spent on test: {0}".format(time_spent))

@defer.inlineCallbacks
def _main():
    try:
        yield main()
    except SystemExit:
        pass
    finally:
        reactor.stop()
    
log.startLogging(sys.stderr)
reactor.callWhenRunning(_main)
reactor.run()
