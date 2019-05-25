from twisted.internet import reactor

from LosmliProxyPool.client.dbclient import RedisClient
from LosmliProxyPool.crawler.ajax.run import crawl_ajax_proxy
from LosmliProxyPool.crawler.spider import XroxySpider, UsProxySpider
from LosmliProxyPool.settings import default_settings
from LosmliProxyPool.utils.load import redis2mysql
from LosmliProxyPool.utils.log import root_logger
from LosmliProxyPool.validator.httpbin import check_proxy_httpbin

SPIDERS = {
    'XroxySpider': {
        'url': 'https://www.xroxy.com/free-proxy-lists/',
        'spider': XroxySpider()
    },
    'UsProxySpider': {
        'url': 'https://www.us-proxy.org/',
        'spider': UsProxySpider()
    },
}


# 爬取proxy
def run_spider():
    rds = RedisClient(host=default_settings.REDIS_HOST, password=default_settings.REDIS_PASSWORD, db=default_settings.REDIS_DB)
    for spider in SPIDERS.values():
        spider_obj = spider['spider']
        url = spider['url']
        response = spider_obj.get(url)
        for item in spider_obj.parse(response):
            value = ':'.join([item['ip'], item['port'], item['country']])
            rds.sadd(default_settings.PROXY_WAIT_CHECK_HTTPBIN, value)


def crawl_proxy():
    root_logger.info('Start to crawl proxy.')
    run_spider()

    crawl_ajax_proxy()
    reactor.run()

    check_proxy_httpbin()
    redis2mysql('proxypool', default_settings.PROXY_IS_VAILD_HTTPBIN)
