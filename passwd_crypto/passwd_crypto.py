import base64
import stdiomask
import sys
import os
import logging


def action():
    cmd = "wmic csproduct get uuid"
    # uuid_current = os.popen(cmd, "r").read().replace('UUID', '').strip()
    uuid_current = "D889EEF7-2A55-F548-9B0F-CB2C4225E30D"
    global my_input_passwd
    try:
        my_input_passwd = sys.argv[1]
    except IndexError as e:
        logging.info(f'приложению: {sys.argv} параметры не передали')
        return False
        # my_input_passwd = stdiomask.getpass("Введите пароль, в ответ получите зашифрованный:")

    my_input_passwd_part1 = my_input_passwd[: int(len(my_input_passwd)/2-1)]
    my_input_passwd_part2 = my_input_passwd[int(len(my_input_passwd)/2-1):]
    pass_encode = base64.b64encode(f"{my_input_passwd_part1}{uuid_current}{my_input_passwd_part2}".encode("utf-8"))
    pass_str = pass_encode.decode("utf-8")
    print(pass_str)

    with open("passwd_crypto.txt", "w") as file:
        file.write(pass_str)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    action()
