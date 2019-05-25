# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest

from LosmliProxyPool.crawler.ajax.ajax.items import AjaxItem


class CoolSpider(scrapy.Spider):
    name = 'cool'
    allowed_domains = ['cool-proxy.net']
    base_url = 'https://www.cool-proxy.net/proxies/http_proxy_list/page:%d/country_code:US/port:/anonymous:'

    def start_requests(self):
        for page in range(1, 11):
            url = self.base_url % page
            yield SplashRequest(url=url, args={'wait': 3, 'images': 0})

    def parse(self, response):
        result_list = response.xpath('//table/tbody/tr')
        for result in result_list:
            ip = result.xpath('./td[@style]/text()').extract_first()
            if ip is None:
                continue
            else:
                item = AjaxItem()
                item['ip'] = ip
                item['port'] = result.xpath('./td[2]/text()').extract_first()
                item['country'] = 'US'
                # print(ip)
                yield item
