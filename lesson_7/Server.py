"""
Сервер

Принимает presence - запрос от клиента;
Если presence - запрос соответствует условиям проверки:
    отправляет ​​ответ ​к​лиенту;
    добавляет клиента в список, обслуживает с помощью функции select:
    принимает и обрабатывает поступившие сообщения от клиентов ;
    отправляет ответы в зависимости от поступивших запросов.
"""

import sys
import time
import select
from socket import *
import logging
from log import log_config_Server
from log.class_Log import Log
from Library.lib_ import *
from baseDB import session
from Server_bd import Storage
from form_start import Ui_Start

# Получить логгер серверa по имени из модуля log_config_Server
server_logger = logging.getLogger('server')
logg = Log(server_logger)


class Server:

    @logg
    def __init__(self, host, port):
        """Настроить сервер."""
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.clients = []
        self.names = {}
        self.storage = Storage(session)

    def read_requests(self, r_clients, all_clients):
        """Читать сообщения."""
        messages = []
        for sock in r_clients:
            try:
                message = get_message(sock)
                messages.append((message, sock))
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)
        return messages

    @logg
    def write_responses(self, messages, names, all_clients):
        """Отправлять сообщения тем клиентам, от которых поступили запросы."""
        for message, sock in messages:
            try:
                if message['action'] == 'get_contacts':
                    username = message['account_name']
                    contacts = self.storage.get_contacts(username)
                    respect = Response(ACCEPTED, num=len(contacts))
                    response = respect.form_response()
                    send_message(sock, response)
                    contact_names = [contact.name for contact in contacts]
                    send_message(sock, contact_names)

                elif message['action'] == 'add_contact':
                    username = message['account_name']
                    user_id = message['user_id']
                    try:
                        self.storage.add_contact(username, user_id)
                        good = Response(ACCEPTED)
                        response = good.form_response()
                        send_message(sock, response)
                    except Exception as e:
                        bad = Response(WRONG_REQUEST, error='Такого контакта нет.')
                        response = bad.form_response()
                        send_message(sock, response)

                elif message['action'] == 'del_contact':
                    username = message['account_name']
                    user_id = message['user_id']
                    try:
                        self.storage.del_contact(username, user_id)
                        good = Response(ACCEPTED)
                        response = good.form_response()
                        send_message(sock, response)
                    except Exception as e:
                        bad = Response(WRONG_REQUEST, error='Такого контакта нет.')
                        response = bad.form_response()
                        send_message(sock, response)

                elif message['action'] == 'msg':
                    to = message['to']
                    # получить по имени сокет
                    client_sock = names[to]
                    send_message(client_sock, message)
            except:
                print('Клиент {} отключился'.format(sock.getpeername()))
                sock.close()
                all_clients.remove(sock)

    @logg
    def presence_response(self, msg):
        """Создать presence - сообщение."""
        try:
            username = msg['account_name']
            # если такого клиента нет в бд - добавляем
            if not self.storage.client_exists(username):
                self.storage.add_client(username)
        except Exception as e:
            r = Response('wrong_request')
            response = r.form_response()
            return response, None
        else:
            r = Response('ok')
            response = r.form_response()
            return response, username

    @logg
    def run(self):
        """Запустить работу сокета на сервере."""
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.sock.settimeout(0.2)
        print('Сервер запущен!')
        while True:
            try:
                conn, addr = self.sock.accept()
                msg = get_message(conn)
                response, client_name = self.presence_response(msg)
                send_message(conn, response)
            except OSError as err:
                pass
            else:
                print('Принят запрос на соединение от %s' % str(addr))
                self.clients.append(conn)
                username = msg['account_name']
                # связать имя подключившегося клиента с его сокетом
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
