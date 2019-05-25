import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

if __name__ == '__main__':
    from LosmliProxyPool.schedule.crawl import crawl_proxy

    crawl_proxy()
