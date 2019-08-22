
# *********************************************** КЛИЕНТ **********************************************************

# Формирует presence - сообщение;
# Отправляет presence - сообщение на сервер;
# Получает ответ от сервера;
# Читает или пишет сообщения (в зависимости от того, в каком режиме находится: 'r' или 'w')

# *****************************************************************************************************************

import sys
from socket import *
import logging
import log.log_config_Client
from log.class_Log import Log
from Library.lib_ import *


# Получаем логгер клиентa по имени из модуля log_config_Client
client_Logger = logging.getLogger('client')
logg = Log(client_Logger)


class Client:
    """ Клиент """

    def __init__(self, login):
        self.login = login

    @logg
    def form_presence(self):
        """
        Формирует presence - сообщение
        """
        presence = Presence(self.login)
        message = presence.form_dict()
        # print('message: ', message)
        return message


    def read_msg(self, server):
        """
        Читает входящие сообщения
        """
        while True:
            print('Read..')
            msg = get_message(server)
            print(msg)

    @logg
    def write(self, server):
        """
        Пишет сообщения
        """
        while True:
            text = input('Введите сообщение(get, add name, del name): ')
            if text == 'get':
                # сформировать запрос на получение контактов
                get_contacts = GetContacts(self.login)
                request = get_contacts.form_dict()
                # print('запрос на получение контактов: ', request)

                # отправить запрос на сервер
                send_message(server, request)

                # получаем ответ от сервера
                response = get_message(server)
                # print('ответ от сервера: ', response)

                # получаем количество друзей и их имена
                num = response['num']
                # print(num)
                print('У Вас ', num, 'друзей:')
                friends = get_message(server)
                for friend in friends:
                    print(friend)
            else:
                command, contact = text.split()
                if command == 'add':
                    try:
                        contact = text.split()[1]
                    except IndexError:
                        print('Name - ?')
                    # сформировать запрос на добавление контакта
                    add_contact = AddContact(self.login, contact)
                    new_contact = add_contact.form_dict()
                    # print(new_contact)

                    # отправить запрос на сервер
                    send_message(server, new_contact)

                    # получить ответ от сервера
                    response = get_message(server)
                    # print('ответ от сервера: ', response)

                    if response['response'] == ACCEPTED:
                        print('Контакт добавлен.')
                    else:
                        print(response['error'])

                elif command == 'del':
                    # сформировать запрос на удаление контакта
                    del_contact = DelContact(self.login, contact)
                    ex_contact = del_contact.form_dict()

                    # отправить запрос на сервер
                    send_message(server, ex_contact)

                    # получить ответ от сервера
                    response = get_message(server)
                    # print('ответ от сервера: ', response)

                    if response['response'] == ACCEPTED:
                        print('Контакт удален.')
                    else:
                        print(response['error'])


if __name__ == '__main__':

    # создать сокет TCP
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        mode = sys.argv[1]
    except IndexError:
        mode = 'w'

    # соединиться с сервером
    sock.connect(('localhost', 7777))

    # создать пользователя
    user = Client('Homer')

    # сформировать presence-сообщение
    presence = user.form_presence()
    # print('presence: ', presence)

    # отправить presence-сообщение на сервер
    send_message(sock, presence)

    # получить ответ от сервера
    response = get_message(sock)
    # print('response: ', response)

    # проверить ответ: если все ок
    if response['response'] == 'ok':
        # проверить, в каком режиме находится клиент
        # если в режиме чтения - то ждем сообщение на чтение
        if mode == 'r':
            user.read_msg(sock)
        # если в режиме записи - будем отправлять сообщения
        elif mode == 'w':
            user.write(sock)
        else:
            raise Exception('Неверный режим чтения/записи.')
    elif response['response'] == 'wrong_request':
        print('Неправильный запрос.')


