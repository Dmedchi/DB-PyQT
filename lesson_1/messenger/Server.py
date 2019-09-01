# ************************ Сервер, реализованный через класс ********************************
# Принимает presence - запрос от клиента;
# Если presence - запрос соответствует условиям проверки:
# отправляет ​​ответ ​к​лиенту;
# добавляет клиента в список, обслуживает с помощью функции select:
# принимает сообщение от одного клиента и
# пересылает это сообщение другому клиенту.
# *******************************************************************************************

import sys
import time
import select
from socket import *
import logging
import log.log_config_Server
from log.class_Log import Log
from Library.lib_ import *
from baseDB import session
from Server_bd import Storage

# Получаем логгер серверa по имени из модуля log_config_Server
server_logger = logging.getLogger('server')
logg = Log(server_logger)


class Server:
    """ Сервер """

    @logg
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.clients = []
        # тут будут имена клиентов и их сокеты
        self.names = {}
        self.storage = Storage(session)

    def read_requests(self, r_clients, all_clients):
        """
        Читает сообщения
        """
        # список входящих сообщений
        messages = []
        for sock in r_clients:
            try:
                # получить входящее сообщение
                message = get_message(sock)
                # добавить в список входящих сообщений
                messages.append((message, sock))
                # print(messages)
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)
        return messages

    @logg
    def write_responses(self, messages, names, all_clients):
        """
        Отправляет сообщения тем клиентам, от которых поступили запросы
        """
        for message, sock in messages:
            try:
                # выполняем разные действия, в зависимости от поступающих запросов
                if message['action'] == 'get_contacts':
                    username = message['account_name']
                    # обращаемся к Хранилищу БД, чтобы получить запрашиваемый список контактов для name
                    contacts = self.storage.get_contacts(username)
                    # print('contacts: ', contacts)
                    # формируем ответ для клиента
                    respect = Response(ACCEPTED, num=len(contacts))
                    response = respect.form_response()
                    # print('response: ', response)
                    # отправляем что все ок
                    send_message(sock, response)
                    # получаем имена и отправляем клиенту
                    contact_names = [contact.name for contact in contacts]
                    # print('contact_names: ', contact_names)
                    send_message(sock, contact_names)

                elif message['action'] == 'add_contact':
                    # запрос на добавление контакта
                    username = message['account_name']
                    # print('add_contact - username: ', username)
                    user_id = message['user_id']
                    # print('add_contact - user_id: ', user_id)
                    try:
                        # выполняем запрос - добавляем контакт в БД
                        self.storage.add_contact(username, user_id)
                        # Если все ок - отправляем клиенту положительный ответ
                        good = Response(ACCEPTED)
                        response = good.form_response()
                        send_message(sock, response)
                    except Exception as e:
                        bad = Response(WRONG_REQUEST, error='Такого контакта нет.')
                        response = bad.form_response()
                        send_message(sock, response)

                elif message['action'] == 'del_contact':
                    # запрос на удаление контакта
                    username = message['account_name']
                    # print('del username: ', username)
                    user_id = message['user_id']
                    # print('user_id: ', user_id)
                    try:
                        self.storage.del_contact(username, user_id)
                        good = Response(ACCEPTED)
                        response = good.form_response()
                        send_message(sock, response)
                    except Exception as e:
                        bad = Response(WRONG_REQUEST, error='Такого контакта нет.')
                        response = bad.form_response()
                        # print(response)
                        send_message(sock, response)

                elif message['action'] == 'msg':
                    #  если получили сообщение, узнаем имя, кому оно адресовано
                    to = message['to']
                    # print('msg for ', to)
                    # print(names)
                    # получаем по имени сокет
                    client_sock = names[to]
                    # print('client_sock: ', client_sock)
                    # отправляем на этот сокет сообщение
                    send_message(client_sock, message)
            except:
                print('Клиент {} отключился'.format(sock.getpeername()))
                sock.close()
                all_clients.remove(sock)

    @logg
    def presence_response(self, msg):
        """
        создать presence - сообщение
        """
        try:
            # получаем имя клиента
            username = msg['account_name']
            # print('account_name: ', username)
            # если такого клиента не т в бд - добавляем
            if not self.storage.client_exists(username):
                self.storage.add_client(username)
                # print('good..')
        except Exception as e:
            r = Response('wrong_request')
            response = r.form_response()
            return response, None
        else:
            # отправить положительный ответ
            r = Response('ok')
            response = r.form_response()
            return response, username

    @logg
    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.sock.settimeout(0.2)
        print('Сервер запущен!')

        while True:
            try:
                conn, addr = self.sock.accept()
                # Получить presence - запрос от клиента
                msg = get_message(conn)
                # print('msg: ', msg)
                # name = msg['account_name']
                # print('account_name - ', name)
                response, client_name = self.presence_response(msg)
                send_message(conn, response)
            except OSError as err:
                pass
            else:
                print('Принят запрос на соединение от %s' % str(addr))
                # добавляем подключившегося клиента в список
                self.clients.append(conn)
                # print('clients.append: ', self.clients)
                # получаем его имя
                username = msg['account_name']
                # связываем имя с его сокетом
                self.names[username] = conn
                print('К нам подключился {}'.format(username))
            finally:
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)

                except Exception as e:
                    pass

                requests = self.read_requests(r, self.clients)
                self.write_responses(requests, self.names, self.clients)


if __name__ == '__main__':
    try:
        host = sys.argv[1]
    except IndexError:
        host = ''

    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777

    except ValueError:
        sys.exit(0)

    server = Server(host, port)
    server.run()
