#!/usr/bin/python
# coding: utf-8
"""
Wrapper for twisted.enterprise.adbapi.ConnectionPool 
with SQL query logging and support for new inserted 
ID retrieving.
"""

import logging
from string import find

import MySQLdb.cursors
from _mysql_exceptions import OperationalError
from twisted.enterprise import adbapi
from twisted.internet import defer

from ro.model.vocabulary import Vocabulary

class ConnectionPool (object):
    """ Connection pool class """
    def __init__ (self, db_host, db_port, db_name, db_user, db_passwd, cp_min=3, cp_max=50):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.vocabulary = Vocabulary(self)
        self.cached_object = {}
        self.cp_min = cp_min
        self.cp_max = cp_max
        self._connect()        
    
    def _connect(self):
        self.dbpool = adbapi.ConnectionPool("MySQLdb", cursorclass=MySQLdb.cursors.DictCursor,
                                            host=self.db_host, port=self.db_port,
                                            db=self.db_name, user=self.db_user, 
                                            passwd=self.db_passwd, use_unicode = True,
                                            charset='utf8', cp_min=self.cp_min, 
                                            cp_max=self.cp_max) 
            
    
    @defer.inlineCallbacks
    def runQuery (self, strSQL, *args, **kw):
        """ runQuery wrapper """        
        logging.debug(" *> sql: %s, args are `%s`" % (strSQL, str(args)))
        try: 
            res = yield self.dbpool.runQuery(strSQL, *args, **kw)
        except OperationalError:
            self._connect()
            res = yield self.dbpool.runQuery(strSQL, *args, **kw)
            
        defer.returnValue(res)

    @defer.inlineCallbacks
    def runOperation (self, strSQL, *args, **kw):
        """ runOperation wrapper """        
        logging.debug(" *> sql: %s, args are `%s`" % (strSQL, str(args)))
        res = yield self.dbpool.runOperation(strSQL, *args, **kw)
        defer.returnValue(res)

    @defer.inlineCallbacks
    def runInteraction (self, strSQL, *args, **kw):
        """ runInteraction wrapper and new inserted ID retrieving """ 
        logging.debug(" *> sql: %s, args are `%s`" % (strSQL, str(args)))
        ret_id = yield self.dbpool.runInteraction(self._returnID, strSQL, *args, **kw)
        defer.returnValue(ret_id)
    
    @defer.inlineCallbacks        
    def loadObject(self, object_class, object_id, mode = 2):
        """
            mode = [0, 1, 2]
            0 - Загрузка из кэша объектов, если нет, то загрузить из базы и положить в кэш
            1 - Загрузка из базы и помещение в кэш
            2 - Загрузка из базы
        """
        o_inst = None
        if mode in [0] and object_class in self.cached_object:
            if object_id in self.cached_object[object_class]:
                o_inst = self.cached_object[object_class][object_id] 
        
        if o_inst is None:
            o_inst = object_class(object_id)
            yield o_inst.load(self)
            if mode in [0, 1]:
                if object_class not in self.cached_object:
                    self.cached_object[object_class] = {}
                self.cached_object[object_class][object_id] = o_inst
            
        defer.returnValue(o_inst)
    
    @defer.inlineCallbacks
    def loadTable2Map(self, table, use_field_cache=True):
        if self.vocabulary.voc_tables_desc.has_key(table) and use_field_cache:
            properties = self.vocabulary.voc_tables_desc[table]   
        else:
            properties = yield self._loadFields(table)
            self.vocabulary.voc_tables_desc[table]=properties

        data = {}
        sql_query = "SELECT %s FROM %s" % (', '.join(properties), table)
        res = yield self.runQuery(sql_query)
        for row in res:
            obj_id = row['id']
            data[obj_id] = row
            for k, val in row.iteritems():
                data[obj_id][k] = val
        defer.returnValue(data)
        
    @defer.inlineCallbacks
    def loadTable2Object(self, table, id, obj, properties=None):
        if properties == None:
            properties = []
            if not self.vocabulary.voc_tables_desc.has_key(table):
                properties = yield self._loadFields(table)
                self.vocabulary.voc_tables_desc[table]=properties
            else:
                properties = self.vocabulary.voc_tables_desc[table]
        sql_query = "SELECT %s FROM %s WHERE id='%d'" % (', '.join([p for p in properties]), table, id)
        res = yield self.runQuery(sql_query)
        if not res:
            defer.returnValue(None)
            
        
        for prop_name in properties:
            prop_value = res[0][prop_name]    
            setattr(obj, prop_name, prop_value)
        defer.returnValue(obj)


    @defer.inlineCallbacks
    def _loadFields(self, table):
        properties = []
        sql_query = "DESCRIBE %s" % table
        res = yield self.runQuery(sql_query)
        for row in res:
            column_name = str(row["Field"])
            if column_name.startswith("comment"):
                continue
            if column_name.lower().startswith("gd_"):
                continue
            properties.append(column_name)
        defer.returnValue(properties)

    def _type_name(self, name):
        i = find(name, "%")
        if i == -1:
            return (None, name)
        else:
            return (name[:i], name[i+1:])

    def _returnID (self, cursor, strSQL, *args, **kw):
        """new inserted ID retrieving"""
        cursor.execute(strSQL, *args, **kw)
        new_row_id = int(cursor.lastrowid)
        return new_row_id
        
