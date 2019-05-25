# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest

from LosmliProxyPool.crawler.ajax.ajax.items import AjaxItem


class CybersyndromeSpider(scrapy.Spider):
    name = 'cybersyndrome'
    allowed_domains = ['ybersyndrome.net']
    start_urls = ['http://www.cybersyndrome.net/pld6.html']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, args={'wait': 3, 'images': 0})

    def parse(self, response):
        result_list = response.xpath('//ol/li')
        for result in result_list:
            item = AjaxItem()
            proxy = result.xpath('./a/text()').extract_first().strip()
            item['ip'], item['port'] = proxy.split(':')
            item['country'] = result.xpath('./a/@title').extract_first() or ''
            # print(item['ip'], item['port'], item['country'])
            yield item
