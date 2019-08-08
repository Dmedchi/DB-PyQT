# ************************************ Класс Message *******************************
# Используется сервером и клиентом;
# Формирует сообщение:
# Преобразование: словарь - строка - байты;
#                байты - строка - словарь;
# Отправляет и читает сообщения.
# *********************************** Класс Response *******************************************
import json
import time

# кортеж действий
# ACTIONS = ('presence', 'msg', 'get_contacts', 'contact_list', 'add_contact', 'del_contact')
PRESENCE = 'presence'
MSG = 'msg'
ADD_CONTACT = 'add_contact'
GET_CONTACTS = 'get_contacts'
DEL_CONTACT = 'del_contact'

# Коды ответов сервера
BASIC_NOTICE = 100  # базовое уведомление
OK = 200  # успешное завершение
CREATED = 201  # объект создан
ACCEPTED = 202
WRONG_REQUEST = 400  # неправильный запрос/JSON-объект
SERVER_ERROR = 500  # ошибка сервера

# кортеж ответов сервера
RESPONSES = (BASIC_NOTICE, OK, CREATED, ACCEPTED, WRONG_REQUEST, SERVER_ERROR)


def dict_str_bytes(dict_message):
    """ Преобразование: словарь - строка - байты """

    # проверяем:
    # если полученное сообщение - словарь
    if isinstance(dict_message, dict) or isinstance(dict_message, list):

        # то преобразуем словарь в строку
        str_message = json.dumps(dict_message)

        # строку преобразуем в байты
        b_message = str_message.encode('utf-8')

        # возвращаем байты
        return b_message
    else:
        # передан неверный тип
        raise TypeError


def bytes_str_dict(b_message):
    """ Преобразование: байты - строка - словарь """

    # проверяем:
    # если полученное сообщение - байты
    if isinstance(b_message, bytes):

        # байты преобразуем в строку
        str_message = b_message.decode('utf-8')

        # строку - в словарь
        message = json.loads(str_message)

        # если после преобразования получили словарь, то возвращаем его
        if isinstance(message, dict) or isinstance(message, list):
            return message
        else:
            # передан неверный тип
            raise TypeError
    else:
        # передан неверный тип
        raise TypeError


def send_message(sock, dict_message):
    """Отправить сообщение"""
    b_msg = dict_str_bytes(dict_message)
    sock.send(b_msg)


def get_message(sock):
    """Прочитать сообщение """
    b_message = sock.recv(1024)
    dict_data = bytes_str_dict(b_message)
    return dict_data


################################################################
class Action:

    def __init__(self, action):
        self.action = action
        self.time = time.ctime()

    def form_dict(self):
        result = {}
        result['action'] = self.action
        result['time'] = self.time
        return result


class Presence(Action):

    def __init__(self, account_name):
        self.account_name = account_name
        super().__init__(PRESENCE)

    def form_dict(self):
        result = super().form_dict()
        result['account_name'] = self.account_name
        return result


class Message(Action):

    def __init__(self, to, from_, message):
        self.to = to
        self.from_ = from_
        self.message = message
        super().__init__(MSG)

    def form_dict(self):
        result = super().form_dict()
        result['to'] = self.to
        result['from_'] = self.from_
        result['message'] = self.message
        return result


class GetContacts(Action):
    def __init__(self, account_name):
        self.account_name = account_name
        super().__init__(GET_CONTACTS)

    def form_dict(self):
        result = super().form_dict()
        result['account_name'] = self.account_name
        return result


class AddContact(Action):

    def __init__(self, account_name, user_id):
        self.account_name = account_name
        self.user_id = user_id
        super().__init__(ADD_CONTACT)

    def form_dict(self):
        result = super().form_dict()
        result['account_name'] = self.account_name
        result['user_id'] = self.user_id
        return result


class DelContact(Action):

    def __init__(self, account_name, user_id):
        self.account_name = account_name
        self.user_id = user_id
        super().__init__(DEL_CONTACT)

    def form_dict(self):
        result = super().form_dict()
        result['account_name'] = self.account_name
        result['user_id'] = self.user_id
        return result


class Response:

    def __init__(self, response, error=None, num=None):
        self.response = response
        self.error = error
        self.num = num

    def form_response(self):
        """ Формируем ответ клиенту """
        result = {}
        result['response'] = self.response
        if self.error is not None:
            result['error'] = self.error
        if self.num is not None:
            result['num'] = self.num
            # Если все хорошо, отправляем ОК
        return result
