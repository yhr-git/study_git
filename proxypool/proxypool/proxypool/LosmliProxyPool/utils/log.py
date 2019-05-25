import logging
from logging.config import dictConfig
import os

from LosmliProxyPool.settings import default_settings

DEFAULT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
     'formatters': {
         'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(default_settings.BASE_DIR, 'losmliproxy.log'),
            'formatter': 'detailed',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    },
}

dictConfig(DEFAULT_CONFIG)
root_logger = logging.getLogger(__name__)
