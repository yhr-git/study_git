import os


def update_squid_conf():
    with open('/etc/squid/squid-default.conf', 'r') as fp:
        default_conf = fp.read()
        default_conf += 'request_header_access Via deny all\n'
        default_conf += 'request_header_access X-Forwarded-For deny all\n'
        default_conf += 'request_header_access From deny all\n'
        default_conf += 'never_direct allow all\n'

    with open('/home/cdj/proxypool/LosmliProxyPool/list.txt', 'r', encoding='utf-8') as fp:
        for index, line in enumerate(fp):
            line = line.strip()
            ip, port = line.split(':')
            proxy_conf = "cache_peer %s parent %s 0 no-query weighted-round-robin weight=1 " \
                         "connect-fail-limit=2 allow-miss max-conn=5 name=proxy-%d\n" % (ip, port, index)
            default_conf += proxy_conf

    with open('/etc/squid/squid.conf', 'w', encoding='utf-8') as fp:
        fp.write(default_conf)

    message = os.system('systemctl restart squid')
    print(message)

if __name__ == '__main__':
    update_squid_conf()
