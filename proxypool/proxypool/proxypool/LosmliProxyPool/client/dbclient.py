import logging

import pymysql
import redis

from LosmliProxyPool.settings import default_settings


logger = logging.getLogger(__name__)


class MySQLClient(object):
    def __init__(self,
                 host=default_settings.MYSQL_HOST,
                 port=default_settings.MYSQL_PORT,
                 user=default_settings.MYSQL_USER,
                 password=default_settings.MYSQL_PASSWORD,
                 db=default_settings.MYSQL_DB):
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
        self.cursor = self.conn.cursor()

    def create_table(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception:
            pass

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            logger.info('MySQL insert err: %s.' % err)

    def fetch_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetch_all(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update(self, sql):
        self.insert(sql)

    def delete(self, sql):
        self.insert(sql)

    def truncate(self, sql):
        self.cursor.execute(sql)

    def alter(self, sql):
        self.create_table(sql)

    def close(self):
        self.cursor.close()
        self.conn.close()

class RedisClient(redis.Redis):
    pass
