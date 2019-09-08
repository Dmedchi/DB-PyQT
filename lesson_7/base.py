"""Консольный и GUI обработчик входящих сообщений."""

from Library.lib_ import *
from PyQt5.QtCore import QObject, pyqtSignal


class Receiver:
    """Класс - получатель информации из сокета."""
    def __init__(self, sock, shared_queue):
        self.shared_queue = shared_queue
        self.sock = sock
        self.is_alive = False

    def process_message(self, message):
        """Обработать принятое сообщение, будет переопределен в наследниках."""
        pass

    def poll(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            data = self.sock.recv(1024)
            if data:
                msg = bytes_str_dict(data)
                if 'action' in msg and msg['action'] == 'msg':
                    self.process_message(msg)
                else:
                    self.shared_queue.put(msg)

            else:
                break

    def stop(self):
        self.is_alive = False


class ConsoleReciever(Receiver):
    """Консольный обработчик входящих сообщений."""

    def process_message(self, message):
        """Отобразить текст сообщения в консоль и от кого оно пришло."""
        print("\n>> от {}: {}".format(message['from_'], message['message']))


class GuiReciever(Receiver, QObject):
    """GUI обработчик входящих сообщений."""
    data = pyqtSignal(str)
    # finished = pyqtSignal(int)

    def __init__(self, sock, shared_queue):
        Receiver.__init__(self, sock, shared_queue)
        QObject.__init__(self)

    def process_message(self, message):
        text = "{} >>> {}".format(message['from_'], message['message'])
        self.data.emit(text)

    def poll(self):
        super().poll()
        self.finished.emit(0)

