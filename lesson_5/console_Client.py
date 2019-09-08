"""Консольный клиент."""

import sys
import threading
from Client import Client
from base import ConsoleReciever

try:
    name = sys.argv[3]
    print(name)
except:
    name = input('Name: ')
user = Client(name)
user.connect()

listener = ConsoleReciever(user.sock, user.shared_queue)
th_listen = threading.Thread(target=listener.poll)
th_listen.daemon = True
th_listen.start()

while True:
    text = input('Введите сообщение: ')
    if text == 'get':
        contacts = user.get_contacts()
    elif text.startswith('add'):
        try:
            username = text.split()[1]
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
            msg = params[2]
        except IndexError:
            print('wrong in message')
        else:
            user.send_message(to, msg)
    elif text == 'exit':
        break
    else:
        print('Что-то пошло не так..')
