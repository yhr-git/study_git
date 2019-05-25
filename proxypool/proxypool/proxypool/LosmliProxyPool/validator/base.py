import logging
import random
from threading import Thread, Lock

import requests

from LosmliProxyPool.client.dbclient import RedisClient
from LosmliProxyPool.settings import default_settings
from LosmliProxyPool.settings.default_settings import MAX_CONCURRENT


logger = logging.getLogger(__name__)

# 检测ip可用线程
class CheckProxyThread(Thread):
    def __init__(self, args, name=None):
        super().__init__()
        self.args = args
        self.name = name
        self.lock = Lock()
        self.rds = RedisClient(host=default_settings.REDIS_HOST, password=default_settings.REDIS_PASSWORD, db=default_settings.REDIS_DB)

    def run(self):
        self.check(*self.args)

    def check(self, ip_port, check_url, vaild):
        ip, port, country = ip_port.split(':')
        proxies = {
            'http': 'http://%s:%s' % (ip, port),
            'https': 'https://%s:%s' % (ip, port)
        }
        headers = {
            'User-Agent': random.choice(default_settings.USER_AGENTS_LIST),
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
        }

        try:
            response = requests.get(check_url, proxies=proxies, timeout=5, headers=headers, verify=False)

            res_time = response.elapsed.total_seconds()
            status_code = response.status_code

            value = ':'.join([ip, port, str(status_code), str(res_time), country])
            if status_code == 200 and 'Set-Cookie' in response.headers:
                with self.lock:
                    self.rds.rpush(vaild, value)
            logger.debug('%s proxy <%s:%s> take %.5f seconds to response, '
                      'response status_code is %d' % (country, ip, port, res_time, response.status_code))
        except Exception as err:
            logger.debug('%s proxy <%s:%s> cannot response, error is %s' % (country, ip, port, err))
            pass


# 生成有效代理
def produce_wait_check_proxy(wait_check):
    rds = RedisClient(host=default_settings.REDIS_HOST, password=default_settings.REDIS_PASSWORD, db=default_settings.REDIS_DB)
    proxy_num = rds.scard(wait_check)
    times = proxy_num // MAX_CONCURRENT
    num = times if proxy_num % MAX_CONCURRENT == 0 else times + 1
    for i in range(num):
        ip_ports = []
        for j in range(MAX_CONCURRENT):
            ip_port = rds.spop(wait_check)
            if ip_port is None:
                break
            ip_ports.append(ip_port.decode('utf-8'))
        yield ip_ports
