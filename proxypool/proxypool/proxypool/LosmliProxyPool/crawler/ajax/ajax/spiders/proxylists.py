# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest

from LosmliProxyPool.crawler.ajax.ajax.items import AjaxItem


class ProxylistsSpider(scrapy.Spider):
    name = 'proxylists'
    allowed_domains = ['proxylists.net']
    base_url = 'http://www.proxylists.net/us_%d_ext.html'

    def start_requests(self):
        for page in range(21):
            url = self.base_url % page
            yield SplashRequest(url=url, args={'wait': 3, 'images': 0})

    def parse(self, response):
        result_list = response.xpath('//table/tbody/tr')
        for result in result_list[3:13]:
            item = AjaxItem()
            item['ip'] = result.xpath('./td[1]/text()').extract_first().strip()
            item['port'] = result.xpath('./td[2]/text()').extract_first().strip()
            item['country'] = 'US'
            yield item
