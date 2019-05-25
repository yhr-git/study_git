import logging

import requests
from lxml import etree


logger = logging.getLogger(__name__)


class BaseSpider(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    def get(self, url):
        response = requests.get(url, headers=self.headers)
        return etree.HTML(response.content)

    def parse(self, response):
        pass

# https://www.xroxy.com/free-proxy-lists/
class XroxySpider(BaseSpider):
    def parse(self, response):
        result_list = response.xpath('//tr[@class]')
        for result in result_list:
            item = {}
            item['ip'] = result.xpath('./td[1]/text()')[0]
            item['port'] = result.xpath('./td[2]/text()')[0]
            item['country'] = 'US'
            logger.debug('Crawl proxy <%s:%s>' % (item['ip'], item['port']))
            yield item

# https://www.us-proxy.org/
class UsProxySpider(BaseSpider):
    def parse(self, response):
        result_list = response.xpath('//table/tbody/tr')
        for result in result_list:
            item = {}
            item['ip'] = result.xpath('./td[1]/text()')[0]
            item['port'] = result.xpath('./td[2]/text()')[0]
            item['country'] = 'US'
            logger.debug('Crawl proxy <%s:%s>' % (item['ip'], item['port']))
            yield item
