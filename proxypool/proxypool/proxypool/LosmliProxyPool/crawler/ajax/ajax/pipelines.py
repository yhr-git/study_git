# -*- coding: utf-8 -*-
from redis import Redis

from LosmliProxyPool.crawler.ajax.ajax import settings


class AjaxPipeline(object):
    def open_spider(self, spider):
        self.rds = Redis(host=settings.REDIS_HOST, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB)

    def process_item(self, item, spider):
        value = ':'.join([item['ip'], item['port'], item['country']])
        self.rds.sadd(settings.PROXY_WAIT_CHECK_HTTPBIN, value)
        return item
