# import logging
import logging
import mimetypes
import os               # Функции для работы с операционной системой, не зависящие от используемой операционной системы
import smtplib          # Импортируем библиотеку по работе с SMTP
from email import encoders
# from email.mime.audio import MIMEAudio
# from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from mail.html import get_html
import wget
import loader


#----------------------------------------------------------------------
def send_email_with_attachment(e_mail,
                                     firma,
                                     full_name,
                                     cont_telefon,
                                     description,
                                     priority,
                                     http_to_attach=None
                                     ):
    """
    Send an email with an attachment
    """
    if loader.debug_on:
        logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO,
                        # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                        )
    # base_path = os.path.dirname(os.path.abspath(__file__))
    # config_path = os.path.join(base_path, "email.ini")
    # header = 'Content-Disposition', 'attachment; filename="%s"' % http_to_attach

    host = loader.server
    FROM = loader.FROM
    password = loader.passwd
    to_addrs = loader.to_addrs

    # create the message
    msg = MIMEMultipart()
    msg["From"] = FROM
    msg["To"] = e_mail
    msg['Reply-To'] = e_mail
    msg["Subject"] = "Уведобление о внешнем IP на устройстве"
    msg["Date"] = formatdate(localtime=True)

    # msg["To"] = ', '.join(e_mail)
    # msg["cc"] = ', '.join(cc_emails)

    html = get_html(e_mail, firma, full_name, cont_telefon, description, priority)

    if html:
        msg.attach(MIMEText(html, "html"))

    files_list = []
    if http_to_attach is not None:
        for key_iter in http_to_attach.keys():
            try:
                path = f'documents/{http_to_attach[key_iter][0]}/{http_to_attach[key_iter][1]}'
                os.makedirs(path)
            except OSError:
                pass
                # logging.info("Создать директорию %s не удалось" % path)
            pahh_file = wget.download(key_iter,
                                      f'documents/{http_to_attach[key_iter][0]}/'
                                      f'{http_to_attach[key_iter][1]}/'
                                      f'{http_to_attach[key_iter][2]}')
            files_list.append(pahh_file)
        process_attachement(msg, files_list)
    logging.info(
        f"\nhost: {type(host)} {host}\n"
        f"FROM: {type(FROM)} {FROM}\n"
        f"password: {type(password)} {password}\n"
        f"to_addrs: {type(to_addrs)} {to_addrs}\n"
        )
    server = smtplib.SMTP(host)
    server.starttls()
    try:
        server.login(FROM, password)
        server.sendmail(FROM, to_addrs, msg.as_string())
    except smtplib.SMTPAuthenticationError as e:
        logging.info(f"Неудачная попытка аутентификации на сервере SMTP\n"
                     f"{e}")
    server.quit()


    #==========================================================================================================================

def process_attachement(msg, files):                        # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):                               # Если файл существует
            attach_file(msg,f)                              # Добавляем файл к сообщению
        elif os.path.exists(f):                             # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)                             # Получаем список файлов в папке
            for file in dir:                                # Перебираем все файлы и...
                attach_file(msg,f+"/"+file)                 # ...добавляем каждый файл к сообщению

def attach_file(msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)                   # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        ctype = 'application/octet-stream'                  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
    # if maintype == 'text':                                  # Если текстовый файл
    #     with open(filepath) as fp:                          # Открываем файл для чтения
    #         file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
    #         fp.close()                                      # После использования файл обязательно нужно закрыть
    # elif maintype == 'image':                               # Если изображение
    #     with open(filepath, 'rb') as fp:
    #         file = MIMEImage(fp.read(), _subtype=subtype)
    #         fp.close()
    # elif maintype == 'audio':                               # Если аудио
    #     with open(filepath, 'rb') as fp:
    #         file = MIMEAudio(fp.read(), _subtype=subtype)
    #         fp.close()
    # else:                                                   # Неизвестный тип файла
    #     with open(filepath, 'rb') as fp:
    #         file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
    #         file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
    #         fp.close()
    #         encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64

    with open(filepath, 'rb') as fp:
        file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
        file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
        fp.close()
        encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64

    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
    msg.attach(file)                                        # Присоединяем файл к сообщению

#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(send_email_with_attachment(e_mail='dffdvfd@fd.ru',
#                                firma="фирма",
#                                full_name='Иван',
#                                cont_telefon='49834889',
#                                description='Ура!')
#     )
#     loop.close()
