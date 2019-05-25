import logging
import random

import requests

from LosmliProxyPool.settings import default_settings
from LosmliProxyPool.validator.base import produce_wait_check_proxy, CheckProxyThread

logger = logging.getLogger(__name__)


class HttpbinThread(CheckProxyThread):
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
            client_ip = default_settings.CLIENT_IP
            text = response.text
            if status_code == 200 and client_ip not in text:
                with self.lock:
                    self.rds.rpush(vaild, value)
            logger.debug('%s proxy <%s:%s> take %.5f seconds to response, '
                      'response status_code is %d' % (country, ip, port, res_time, response.status_code))
        except Exception as err:
            logger.debug('%s proxy <%s:%s> cannot response, error is %s' % (country, ip, port, err))
            pass


# 多线程检测
def threading_check(ip_ports, check_url, vaild):
    threads = []
    for ip_port in ip_ports:
        p = HttpbinThread(args=(ip_port, check_url, vaild))
        p.start()
        threads.append(p)
    for thread in threads:
        thread.join()


# 验证有效proxy
def check_proxy_httpbin():
    for ip_ports in produce_wait_check_proxy(default_settings.PROXY_WAIT_CHECK_HTTPBIN):
        threading_check(ip_ports, default_settings.HTTPBIN_CHECK_URL, default_settings.PROXY_IS_VAILD_HTTPBIN)
