#! /usr/bin/env python3
# coding:utf-8
import pymysql
import redis
import pymongo

from scrapy.conf import settings


class DataMysql(object):
    def __init__(self):
        self.conn = pymysql.connect(
            db = 'weibo',
            host = '127.0.0.1',
            charset = 'utf-8',
            passworld = 'mysql',
            port = '3306',
            user = 'mysql',
        )

    def save(self, sql, params):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        cur.close()

    def close(self):
        self.conn.close()


class MongoDatabase(object):
    def __init__(self, dc_name):
        # 获取setting主机名、端口号和数据库名
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = pymongo.MongoClient(host=host, port=port)

        # 指向指定的数据库
        mdb = client[dbname]
        # 获取数据库里存放数据的表名
        self.post = mdb[settings['MONGODB_DOCNAME'].get(dc_name)]

    def get_collection(self):
        return self.post


class _DataRedis(object):
    def __init__(self):
        self.db = redis.StrictRedis()

    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()

        return cls._instance

    def spop(self, name):
        '''
        随机返回一个元素并删除集合内这个元素
        '''
        return self.db.spop(name)

    def scard(self, name):
        '''
        返回集合个数
        '''
        return self.db.scard(name)

    def smembers(self, name):
        '''
        返回集合所有元素
        '''
        return self.db.smembers(name)

    def srandmember(self, name):
        '''
        返回一个随机元素
        '''
        return self.db.srandmember(name)

    def sadd(self, name, val):
        '''
        集合存在则追加，　否则创建集合
        '''

        try:
            self.db.sadd(name, val)
        except Exception as e:
            print '[ERROR]: %s' % e


DataRedis = _DataRedis.instance

