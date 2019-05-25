from LosmliProxyPool.client.dbclient import MySQLClient


def create(sql):
    mysql_client = MySQLClient()
    mysql_client.create_table(sql)
    mysql_client.close()


def create_proxypool():
    mysql_client = MySQLClient()
    sql = 'CREATE TABLE proxypool1 (' \
          'id INT AUTO_INCREMENT PRIMARY KEY, ' \
          'ip VARCHAR(16) NOT NULL, ' \
          'port VARCHAR(8) NOT NULL, ' \
          'status_code SMALLINT NOT NULL,' \
          'res_time FLOAT NOT NULL,' \
          'score SMALLINT NOT NULL,' \
          'country CHAR(2) NOT NULL' \
          ')'
    mysql_client.create_table(sql)

    alter_sql = 'ALTER TABLE proxypool1 ADD UNIQUE (ip, port);'
    mysql_client.alter(alter_sql)
    mysql_client.close()


# 创建ip库
def create_vaild_proxy():
    sql = 'CREATE TABLE vaild_proxy (' \
          'id INT AUTO_INCREMENT PRIMARY KEY, ' \
          'ip VARCHAR(16) NOT NULL, ' \
          'port VARCHAR(8) NOT NULL, ' \
          'status_code SMALLINT NOT NULL,' \
          'res_time FLOAT NOT NULL,' \
          'score SMALLINT NOT NULL,' \
          'country CHAR(2) NOT NULL,' \
          'check_date DATE NOT NULL,'\
          'check_hour TINYINT NOT NULL' \
          ')'
    create(sql)


if __name__ == '__main__':
    create_proxypool()
