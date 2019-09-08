# Модульное тестирование
# Интеграционное тестирование

import pytest
import socket
import json
from lib_ import dict_str_bytes, bytes_str_dict, send_message, get_message
import Client_


# Модульное тестирование

def test_dict_str_bytes():
    assert dict_str_bytes({'action': 'presence'}) == b'{"action": "presence"}'

def test_bytes_str_dict():
    assert bytes_str_dict(b'{"text": "text"}') == {'text': 'text'}

def test_form_presence():
    pass



# Интеграционное тестирование

class ClientSocket:
    """ Класс-заглушка для сокета """

    def __init__(self, sock_family= socket.AF_INET, sock_type = socket.SOCK_STREAM):
        pass


    def recv(self, n):                                    # ***
        message = {'response': 200}
        j_message = json.dumps(message)
        b_message = j_message.encode('utf-8')
        return b_message


    def send(self, b_message):
        pass


def test_get_message(monkeypatch):
    monkeypatch.setattr('socket.socket', ClientSocket)   # Подмена настоящего сокета классом - заглушкой
    fake_sock = socket.socket()                          # Создаем виртуальный сокет
    assert get_message(fake_sock) == {'response': 200}   # ссылается на recv ***



def test_send_message(monkeypatch):
    monkeypatch.setattr('socket.socket', ClientSocket)
    fake_sock = socket.socket()
    assert send_message(fake_sock, {'response': 200}) is None


