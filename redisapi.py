import logging

from twisted.internet import reactor, defer
from txredis.client import RedisClientFactory


class RedisConnection(object):
    def __init__(self, host, port, password, factory, factory_attr, use_hiredis=False, db=0):
        self.host = host
        self.port = port
        self.password = password
        self.use_hiredis = use_hiredis
        self.db = db
        self.factory = factory
        self.factory_attr = factory_attr
        self.redis_factory = None
        self.redis_conn = None

    @defer.inlineCallbacks
    def connect(self):
        factory = RedisClientFactory(password=self.password, db=self.db, use_hiredis=self.use_hiredis)
        reactor.connectTCP(self.host, self.port, factory)
        self.redis_conn, new_defer = yield factory.deferred
        logging.debug("self.redis_conn is %s" % str(self.redis_conn))
        setattr(self.factory, self.factory_attr, self.redis_conn)
        new_defer.addCallback(self.reconnect_callback)

    def reconnect_callback(self, reconnect_info):
        redis_db, new_defer = reconnect_info
        logging.info("Service has been reconnected to redis %s:%d db: %d" % (self.host, self.port, self.db))
        logging.info("Passed redis_db is %s" % str(redis_db))
        self.redis_conn = redis_db
        setattr(self.factory, self.factory_attr, self.redis_conn)
        new_defer.addCallback(self.reconnect_callback)



class LuaScriptManager(object):
    def __init__(self, dir_with_scripts, factory):
        self.dir_with_scripts = dir_with_scripts
        self.script_map = {}
        self.factory = factory

    @defer.inlineCallbacks
    def load_all(self):
        """WARNING: LuaScriptManager constructor has blocking calls 
        which work with file system!!
        """
        import os
        for root, dirs, files in os.walk(self.dir_with_scripts):
            for f_name in files:
                if f_name[-4:] == ".lua":
                    script_path = os.path.join(root, f_name)
                    yield self.load_script(f_name[:-4], open(script_path).read())


    @defer.inlineCallbacks
    def load_script(self, script_name, script):
        try:
            script_sha1 = yield self.factory.system_db.redis_db.script_load(script)
            logging.info("Script `%s` has been loaded, sha1 is is %s" % (str(script_name), str(script_sha1)))
            self.script_map[script_name] = script_sha1
        except Exception, e:
            logging.error("Cannot load lua script `%s` because of `%s`, skipped" % (str(script_name), str(e)))


    @defer.inlineCallbacks
    def call_script(self, script_name, *args):
        if script_name not in self.script_map:
            logging.warning("Script %s is not loaded into server and redis cache" % str(script_name))
            defer.returnValue(None)

        res = yield self.factory.system_db.redis_db.script_eval_sha(self.script_map[script_name], len(args), *args)

        defer.returnValue(res)

