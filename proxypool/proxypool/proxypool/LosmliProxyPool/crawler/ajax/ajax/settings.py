# -*- coding: utf-8 -*-
import os

BOT_NAME = 'ajax'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

SPIDER_MODULES = ['LosmliProxyPool.crawler.ajax.ajax.spiders']
NEWSPIDER_MODULE = 'LosmliProxyPool.crawler.ajax.ajax.spiders'


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

SPLASH_URL = 'http://localhost:8050/'
# SPLASH_URL = 'http://192.168.99.100:8050/'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

ITEM_PIPELINES = {
    'LosmliProxyPool.crawler.ajax.ajax.pipelines.AjaxPipeline': 300,
}

# redis配置
REDIS_HOST = '172.105.220.160'
REDIS_PORT = 6379
REDIS_PASSWORD = 'hb_root123456'
REDIS_DB = 1

# redis key
PROXY_WAIT_CHECK_HTTPBIN = 'proxyWaitCheckHttpbin'

LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(BASE_DIR, 'losmliproxy.log')
