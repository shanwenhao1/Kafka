import os
import platform

Log_Dir = os.path.dirname(os.path.abspath(__file__))
Log_Path = os.path.join(Log_Dir, "ZKAdmin.log")
# 判断是否是windows
Log_File = Log_Path.replace("/", "\\") if platform.architecture()[1].rfind("Windows") == 0 else Log_Path

# 定义三种日志输出格式 开始
Standard_Format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'    # 其中name为getlogger指定的名字
Simple_Format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
Id_Simple_Format = '[%(levelname)s][%(asctime)s] %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': Standard_Format
        },
        'simple': {
            'format': Simple_Format
        },
        "idSimple": {
            'format': Id_Simple_Format
        }
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',                   # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',    # 保存到文件
            'formatter': 'idSimple',
            'filename': Log_File,                               # 日志文件
            'maxBytes': 1024 * 1024 * 5,                        # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'INFO',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}

# LOGGING使用方法, 不用LOGGING的原因是会打印第三方包的日志
# cfg_dict = LOGGING
# logging.config.dictConfig(cfg_dict)
# Logger = logging.getLogger(Log_File)
