from LosmliProxyPool.settings import default_settings
from LosmliProxyPool.validator.base import produce_wait_check_proxy, CheckProxyThread


# 多线程检测
def threading_check(ip_ports, check_url, vaild):
    threads = []
    for ip_port in ip_ports:
        p = CheckProxyThread(args=(ip_port, check_url, vaild))
        p.start()
        threads.append(p)
    for thread in threads:
        thread.join()


# 验证有效proxy
def check_proxy_amazon():
    for ip_ports in produce_wait_check_proxy(default_settings.PROXY_WAIT_CHECK_AMAZON):
        threading_check(ip_ports, default_settings.AMAZON_CHECK_URL, default_settings.PROXY_IS_VAILD_AMAZON)
