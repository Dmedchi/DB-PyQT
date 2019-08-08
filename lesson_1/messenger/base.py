from Library.lib_ import *


# class SockHandler:
#     """
#     Базовый класс для работы с сокетом
#     """
#     def __init__(self, sock, shared_queue):
#         self.sock = sock
#         self.shared_queue = shared_queue
#         self.is_alive = False
#
#     def __call__(self):
#         ''' Класс-наследник должен выставить флаг is_alive = True '''
#         raise NotImplemented
#
#     def stop(self):
#         self.is_alive = False


class Receiver:
    """
    Класс - получатель информации из сокета
    """

    def __init__(self, sock, shared_queue):
        self.shared_queue = shared_queue
        self.sock = sock
        self.is_alive = False

    def process_message(self, message):
        """метод для обработки принятого сообщения, будет переопределен в наследниках"""
        pass

    def poll(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            msg = get_message(self.sock)
            # print('Нам пришло сообщение: ', msg)
            # print(type(msg))
            # try:
            if 'action' in msg and msg['action'] == 'msg':
                self.process_message(msg)
            else:
                self.shared_queue.put(msg)
            # except Exception as e:
            #     print(e)

    def stop(self):
        self.is_alive = False


class ConsoleReciever(Receiver):
    """
    Консольный обработчик входящих сообщений
    """

    def process_message(self, message):
        # Выводим текст сообщения в консоль и рисуем от кого пришло
        print("\n>> от {}: {}".format(message['from_'], message['message']))
