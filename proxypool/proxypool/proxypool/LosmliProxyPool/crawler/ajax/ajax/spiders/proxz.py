# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest

from LosmliProxyPool.crawler.ajax.ajax.items import AjaxItem


class ProxzSpider(scrapy.Spider):
    name = 'proxz'
    allowed_domains = ['proxz.com']
    base_url = 'http://www.proxz.com/proxy_list_anonymous_us_%d_ext.html'

    def start_requests(self):
        for page in range(3):
            url = self.base_url % page
            yield SplashRequest(url=url, args={'wait': 3, 'images': 0})

    def parse(self, response):
        result_list = response.xpath('//table/tbody/tr')
        for result in result_list[3:-1]:
            ip = result.xpath('./td[1]/text()').extract_first()
            port = result.xpath('./td[2]/text()').extract_first()
            if ip is not None and port is not None:
                item = AjaxItem()
                item['ip'] = ip.strip()
                item['port'] = port.strip()
                item['country'] = 'US'
                # print(item['ip'], item['port'])
                yield item
