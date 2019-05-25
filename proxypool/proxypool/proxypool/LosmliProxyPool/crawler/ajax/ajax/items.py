# -*- coding: utf-8 -*-

import scrapy


class AjaxItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    country = scrapy.Field()
