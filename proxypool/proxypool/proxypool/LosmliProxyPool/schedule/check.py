from LosmliProxyPool.settings import default_settings
from LosmliProxyPool.utils.load import mysql2redis, update2mysql
from LosmliProxyPool.utils.log import root_logger
from LosmliProxyPool.validator.amazon import check_proxy_amazon


def check_proxy():
    root_logger.info('Start to check proxy.')
    mysql2redis(default_settings.PROXY_WAIT_CHECK_AMAZON)
    check_proxy_amazon()
    update2mysql(default_settings.PROXY_IS_VAILD_AMAZON)
