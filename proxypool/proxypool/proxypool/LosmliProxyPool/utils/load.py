from datetime import date, datetime

from LosmliProxyPool.client.dbclient import MySQLClient, RedisClient
from LosmliProxyPool.settings import default_settings


# 保存有效proxy到MySQL
def redis2mysql(table, key):
    mysql_client = MySQLClient()
    redis_client = RedisClient(host=default_settings.REDIS_HOST, password=default_settings.REDIS_PASSWORD, db=default_settings.REDIS_DB)

    proxy_num = redis_client.llen(key)
    for i in range(proxy_num):
        result = redis_client.lpop(key)
        result = result.decode('utf-8')
        ip, port, status_code, res_time, country = result.split(':')
        score = 1 if int(status_code) == 200 else 0

        sql = 'INSERT INTO %s VALUES (NULL, "%s", "%s", %s, %s, %s, "%s");' % \
              (table, ip, port, int(status_code), float(res_time), score, country)
        # print(sql)
        mysql_client.insert(sql)
    mysql_client.close()


# 加载proxy到redis队列中待检测
def mysql2redis(key):
    mysql_client = MySQLClient()
    redis_client = RedisClient(host=default_settings.REDIS_HOST, password=default_settings.REDIS_PASSWORD, db=default_settings.REDIS_DB)
    sql = 'SELECT ip, port, country FROM proxypool;'
    data = mysql_client.fetch_all(sql)
    for ip, port, country in data:
        value = ':'.join([ip, port, country])
        redis_client.sadd(key, value)
    mysql_client.close()


# 检测有效proxy后更新MySQL
def update2mysql(key):
    mysql_client = MySQLClient()
    redis_client = RedisClient(host=default_settings.REDIS_HOST, password=default_settings.REDIS_PASSWORD,
                               db=default_settings.REDIS_DB)
    proxy_num = redis_client.llen(key)
    check_date = date.today()
    check_hour = datetime.today().hour

    select_sql = 'SELECT id, score, check_date, check_hour FROM vaild_proxy WHERE ip="%s" AND port="%s";'
    for i in range(proxy_num):
        result = redis_client.lpop(key)
        result = result.decode('utf-8')
        ip, port, status_code, res_time, country = result.split(':')

        select = select_sql % (ip, port)
        proxy_data = mysql_client.fetch_one(select)
        if proxy_data is None:
            # 新可用代理
            score = 1 if int(status_code) == 200 else 0
            insert_sql = 'INSERT INTO vaild_proxy VALUES (NULL, "%s", "%s", %s, %s, %s, "%s", "%s", %s);' % \
                         (ip, port, int(status_code), float(res_time), score, country, check_date, check_hour)
            # print(insert_sql)
            mysql_client.insert(insert_sql)
        else:
            proxy_id, pre_score, pre_check_date, pre_check_hour = proxy_data
            update_sql = 'UPDATE vaild_proxy SET score=%s, res_time=%s, status_code=%s, check_date="%s", check_hour=%s WHERE id=%s;'
            if int(status_code) == 200 and check_hour == pre_check_hour + 1:
                pre_score += 1
            elif int(status_code) == 200 and pre_check_hour == 23:
                pre_score += 1
            else:
                pre_score -= 1

            update = update_sql % (pre_score, float(res_time), int(status_code), check_date, check_hour, proxy_id)
            # print(update)
            mysql_client.update(update)

    update_others = 'UPDATE vaild_proxy SET status_code=503,score=score-1 WHERE check_hour!=%s;' % check_hour
    mysql_client.update(update_others)
    mysql_client.close()


# 获取有效proxy到list文件
def mysql2file():
    mysql_client = MySQLClient()
    max_sql = 'SELECT MAX(score) FROM vaild_proxy;'
    max_score, = mysql_client.fetch_one(max_sql)
    vaild_score = max_score - 3
    sql = 'SELECT ip, port FROM vaild_proxy WHERE status_code=200 AND score>%d AND country="US";' % vaild_score
    data = mysql_client.fetch_all(sql)
    with open(default_settings.PROXY_FILE, 'w', encoding='utf-8') as fp:
        for ip, port in data:
            proxy = ':'.join([ip, port])
            fp.write(proxy + '\n')
