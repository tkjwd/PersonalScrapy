# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class MapspiderFourPipeline(object):
#     def process_item(self, item, spider):
#         return item

import pymysql
from twisted.enterprise import adbapi
import pymysql.cursors
import redis


class MysqlTwistedPipelines(object):
    def __init__(self, dbpool, settings):
        self.dbpool, self.settings = dbpool, settings
        # self.Rh = _Redis_Help(host='192.168.1.30', db=11)
        # self.pool = redis.ConnectionPool(host='192.168.1.30', port=6379)
        # self.r = redis.Redis(connection_pool=self.pool)
        # self.r = redis.Redis(host='localhost', port=6379, db=2)
        # self.pipe = self.r.pipeline(transaction=True)

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool, settings)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入股变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        # 处理mysql断线从链
        if failure.value.args[1] == 'MySQL server has gone away':
            try:
                dbparms = dict(
                    host=self.settings["MYSQL_HOST"],
                    db=self.settings["MYSQL_DBNAME"],
                    user=self.settings["MYSQL_USER"],
                    passwd=self.settings["MYSQL_PASSWORD"],
                    charset="utf8",
                    cursorclass=pymysql.cursors.DictCursor,
                    use_unicode=True
                )
                dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
                self.dbpool = dbpool
            except:
                pass
        else:
            print(failure)
            pass

    def do_insert(self, cursor, item):
        insert_sql, params = item.insert_sql()
        # result = self.r.sadd("Express_Item_Id", item["company_id"])
        # if result:
        if params:
            try:
                cursor.execute(insert_sql, params)
                print("插入成功", params)
            except Exception as e:
                print(e)
                pass
        else:
            print("数据不合法")