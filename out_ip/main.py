import logging
import sys
import urllib.request
import socket
from loader import url_helper, external_ip_pattern, to_addrs, firma
from mail.send_mail import send_email_with_attachment


def print_ip():
    external_ip = urllib.request.urlopen(url_helper).read().decode('utf8')
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    str_my = f"Имя устройства: {hostname}. \n" \
             f"Локальный IP адрес устройства: {ip_local}. \n" \
             f"Сейчас внешний IP адрес для устройства: {external_ip}"
    if external_ip == external_ip_pattern:
        description = f"{str_my}, \n" \
                      f"и это соответсвует, установленному ранее IP адресу."
        # priority = ""
        logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO,
                        # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                        )
        logging.info(f"Сработал планировщик заданий\n"
                     f"{description}")
        sys.exit("Выход из программы, на почту уведомление не отправлялось.")
    else:
        description = f"{str_my}, " \
                      f"ВНИМАНИЕ!!! это не соответсвует, установленному ранее IP адресу: {external_ip_pattern}. " \
                      f"Примите меры"
        priority = "Критично"
    send_email_with_attachment(firma=firma, e_mail=to_addrs, full_name="Я робот, слежу за внешним IP",
                                     cont_telefon=" ", description=description, priority=priority)


if __name__ == '__main__':
    print_ip()
