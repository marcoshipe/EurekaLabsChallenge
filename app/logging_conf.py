import sys


logging_conf = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'rotating_file': {
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app/logs/app.log' if 'pytest' not in sys.modules else 'app/logs/app_test.log',
            'maxBytes': 100000000,
            'backupCount': 5,
        },
    },
    'loggers': {
        'default': {'handlers': ['rotating_file'], 'level': 'DEBUG'},
    },
}
