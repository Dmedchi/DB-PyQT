"""Служебный скрипт запуска/остановки нескольких клиентов"""

from subprocess import Popen, CREATE_NEW_CONSOLE
import time

# список запущенных процессов
p_list = []

while True:
    user = input("Запустить сервер и клиентов (s) / Выйти (q)")

    if user == 's':
        # запустить сервер
        # Запустить серверный скрипт и добавить его в список процессов
        p_list.append(Popen('python Server.py',
                            creationflags=CREATE_NEW_CONSOLE))
        print('Сервер запущен')
        time.sleep(1)

        # Запустить клиентский скрипт и добавить его в список процессов
        for i in range(2):
            p_list.append(Popen('python console_Client.py localhost 7777 console{}'.format(i),
                                creationflags=CREATE_NEW_CONSOLE))
        print('Консольне клиенты запущены')
        for i in range(2):
            # Запустить клиентов с графическим интерфейсом
            p_list.append(Popen('python gui_Client.py localhost 7777 Gui{}'.format(i),
                                creationflags=CREATE_NEW_CONSOLE))
        print('Gui клиенты запущены')

    elif user == 'q':
        print('Открыто процессов {}'.format(len(p_list)))
        for p in p_list:
            print('Закрываю {}'.format(p))
            p.kill()
        p_list.clear()
        print('Выхожу')
        break
