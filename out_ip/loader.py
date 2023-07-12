import base64
import os
import logging

from environs import Env
import sys

env = Env()
env.read_env()
url_helper = env.str("URL_HELPER")
firma = env.str("FIRMA")
server = env.str("SERVER")
FROM = env.str("FROM")
to_addrs = env.str("TO_ADDRS")
external_ip_pattern = env.str("EXTERNAL_IP_PATTERN")
debug_on = bool
try:
    passwd = sys.argv[1]
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO,
                        # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                        )
    logging.info(f'приложению: {sys.argv} параметры передали: {passwd} ')
    debug_on = True
except IndexError as e:
    debug_on = False
    cmd = "wmic csproduct get uuid"
    __uuid_current1 = os.popen(cmd, "r").read().replace('UUID', '').strip()
    __passwd_from_env = env.str("PASSWD")
    __pass_encode = bytes(__passwd_from_env, "utf-8")
    __passwd_not_replace = base64.b64decode(__pass_encode).decode("utf-8")
    passwd = __passwd_not_replace.replace(__uuid_current1,"")
