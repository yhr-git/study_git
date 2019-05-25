# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest

from LosmliProxyPool.crawler.ajax.ajax.items import AjaxItem


class FreeproxylistsSpider(scrapy.Spider):
    name = 'freeproxylists'
    allowed_domains = ['freeproxylists.com']
    start_urls = ['http://www.freeproxylists.com/us.html']
    base_url = 'http://www.freeproxylists.com/'

    def parse(self, response):
        result_list = response.xpath('//table[@style]/tr/td[1]/a')
        for result in result_list:
            href = result.xpath('./@href').extract_first()
            if href.startswith('us'):
                url = self.base_url + href
                yield SplashRequest(url=url, callback=self.parse_proxy, args={'wait': 3, 'images': 0})

    def parse_proxy(self, response):
        result_list = response.xpath('//table/tbody/tr')
        for result in result_list[3:]:
            ip = result.xpath('./td[1]/text()').extract_first()
            port = result.xpath('./td[2]/text()').extract_first()
            if ip is not None and port is not None:
                item = AjaxItem()
                item['ip'] = ip
                item['port'] = port
                item['country'] = 'US'
                # print(item['ip'], item['port'])
                yield item
