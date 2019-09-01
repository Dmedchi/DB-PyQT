# *********************************************** КЛИЕНТ **********************************************************

# подключается к серверу
# Формирует presence - сообщение;
# Отправляет presence - сообщение на сервер;
# Получает ответ от сервера;
# Читает или пишет сообщения (в зависимости от того, в каком режиме находится: 'r' или 'w')

# *****************************************************************************************************************

import sys
import threading
from queue import Queue
from socket import *
import logging
import log.log_config_Client
from log.class_Log import Log
from Library.lib_ import *
from base import ConsoleReciever

# Получаем логгер клиентa по имени из модуля log_config_Client
client_Logger = logging.getLogger('client')
logg = Log(client_Logger)


class Client:
    """ Клиент """

    def __init__(self, login):
        self.login = login
        self.shared_queue = Queue()

    @logg
    def run(self):
        """ Подключение к серверу """
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(('localhost', 7777))
        presence = self.form_presence()
        # print('presence', presence)
        send_message(self.sock, presence)
        response = get_message(self.sock)
        return response

    def end(self):
        """ Отключение клиента """
        self.sock.close()

    @logg
    def form_presence(self):
        """
        Формирует presence - сообщение
        """
        presence = Presence(self.login)
        message = presence.form_dict()
        # print('message: ', message)
        return message

    @logg
    def form_msg(self, to_contact, text):
        """ Создает сообщение и возвращает его в виде словаря """
        msg = Message(to_contact, self.login, text)
        message = msg.form_dict()
        # print(message)
        return message

    @logg
    def get_contacts(self):
        """запрос на получение контактов """
        contacts = GetContacts(self.login)
        request = contacts.form_dict()
        # print('запрос на получение контактов: ', request)
        # отправить запрос на сервер
        send_message(self.sock, request)
        # получаем ответ
        response = self.shared_queue.get()
        # print('ответ от сервера: ', response)
        # получаем количество друзей и их имена
        num = response['num']
        print('У Вас', num, 'друзей:')
        contacts = self.shared_queue.get()
        for contact in contacts:
            print(contact)
        return contacts

    @logg
    def add_contact(self, username):
        """сформировать запрос на добавление контакта """
        add_contact = AddContact(self.login, username)
        new_contact = add_contact.form_dict()
        send_message(self.sock, new_contact)
        # получаем ответ
        response = self.shared_queue.get()
        if response['response'] == ACCEPTED:
            print('Контакт добавлен.')
        else:
            print(response['error'])
        # print('ответ от сервера: ', response)
        return response

    @logg
    def del_contact(self, username):
        """сформировать запрос на удаление контакта """
        del_contact = DelContact(self.login, username)
        ex_contact = del_contact.form_dict()
        send_message(self.sock, ex_contact)
        response = self.shared_queue.get()
        if response['response'] == ACCEPTED:
            print('Контакт удален.')
        else:
            print(response['error'])
        return response

    @logg
    def send_message(self, to, msg):
        """ отправляет сообщение адресату """
        message = Message(to, self.login, msg)
        # message = msg.form_dict()
        # print(message)
        send_message(self.sock, message.form_dict())


if __name__ == '__main__':

    try:
        name = sys.argv[3]
        print(name)
    except:
        name = input('Name: ')
    user = Client(name)
    user.run()

    listener = ConsoleReciever(user.sock, user.shared_queue)
    th_listen = threading.Thread(target=listener.poll)
    th_listen.daemon = True
    th_listen.start()

    while True:
        text = input('Введите сообщение: ')
        if text == 'get':
            contacts = user.get_contacts()
            # print(contacts)
        elif text.startswith('add'):
            try:
                username = text.split()[1]
                # print('add name', username)
            except IndexError:
                print('Вы забыли указать имя контакта.')
            else:
                user.add_contact(username)
        elif text.startswith('del'):
            try:
                username = text.split()[1]
            except IndexError:
                print('Вы забыли указать имя контакта.')
            else:
                user.del_contact(username)
        elif text.startswith('message'):
            params = text.split()
            try:
                to = params[1]
                # print('to', to)
                msg = params[2]
                # print('msg:', msg)
            except IndexError:
                print('wrong...')
            else:
                user.send_message(to, msg)
        elif text == 'exit':
            break
        else:
            print('Что-то пошло не так..')

# user.end()
