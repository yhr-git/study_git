import os
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor

from LosmliProxyPool.crawler.ajax.ajax.spiders.cool import CoolSpider
from LosmliProxyPool.crawler.ajax.ajax.spiders.cybersyndrome import CybersyndromeSpider
from LosmliProxyPool.crawler.ajax.ajax.spiders.freeproxylists import FreeproxylistsSpider
from LosmliProxyPool.crawler.ajax.ajax.spiders.proxylists import ProxylistsSpider
from LosmliProxyPool.crawler.ajax.ajax.spiders.proxz import ProxzSpider

os.environ['SCRAPY_SETTINGS_MODULE'] = 'LosmliProxyPool.crawler.ajax.ajax.settings'
settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl_ajax_proxy():
    yield runner.crawl(CoolSpider)
    yield runner.crawl(CybersyndromeSpider)
    yield runner.crawl(ProxylistsSpider)
    yield runner.crawl(ProxzSpider)
    yield runner.crawl(FreeproxylistsSpider)
    reactor.stop()
