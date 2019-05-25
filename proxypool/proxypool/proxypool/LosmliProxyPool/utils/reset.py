from LosmliProxyPool.client.dbclient import MySQLClient


def reset_score():
    mysql_client = MySQLClient()
    max_sql = 'SELECT MAX(score) FROM vaild_proxy;'
    max_score, = mysql_client.fetch_one(max_sql)
    score_limit = max_score - 3
    # 删除低效代理
    del_sql = 'DELETE FROM vaild_proxy WHERE score<=%d;' % score_limit
    mysql_client.delete(del_sql)
    # 重置有效代理score
    vaild_sql = 'UPDATE vaild_proxy SET score=1 WHERE score<%d;' % max_score
    mysql_client.update(vaild_sql)
    vaild_sql = 'UPDATE vaild_proxy SET score=2 WHERE status_code=200 AND score=%d;' % max_score
    mysql_client.update(vaild_sql)
    mysql_client.close()
