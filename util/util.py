# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

log = None
def get_log(name="main"):
    global log
    if log:
        return log
    log = logging.getLogger('log')
    log.setLevel(logging.DEBUG)
    # logG.setLevel(logging.INFO)
    fmt = "%(filename)s:%(module)s:%(funcName)s:%(lineno)d:%(levelname)s:%(asctime)s>>%(message)s"
    formater = logging.Formatter(fmt)
    if not os.path.exists("./log/"):
        os.mkdir("./log/")
    handler = logging.handlers.TimedRotatingFileHandler("./log/{}.log".format(name), "midnight", 1, 7)
    handler.setFormatter(formater)
    log.addHandler(handler)
    return log

log = get_log()