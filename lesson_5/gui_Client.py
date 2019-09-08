"""Клиент с графическим интерфейсом."""

import sys
import threading
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from base import GuiReciever
from Client import Client

# создать приложение
app = QtWidgets.QApplication(sys.argv)
name = input('Name: ')
window = uic.loadUi('Window.ui')
window.setWindowTitle(name)

# создать клиента
user = Client(name)
user.connect()
listener = GuiReciever(user.sock, user.shared_queue)


@pyqtSlot(str)
def show_chat(data):
    try:
        msg = data
        window.storyMessage.addItem(msg)
    except Exception as e:
        print('error: ', e)


listener.data.connect(show_chat)
th = QThread()
listener.moveToThread(th)
th.started.connect(listener.poll)
th.start()

# получить список контактов
contacts = user.get_contacts()


def list_contacts(contacts):
    """Отобразить список контактов."""
    window.listWidget.clear()
    for contact in contacts:
        window.listWidget.addItem(contact)


list_contacts(contacts)


def add_contact():
    """Добавить контакт."""
    try:
        username = window.textEdit.toPlainText()
        if username:
            user.add_contact(username)
            window.listWidget.addItem(username)
    except Exception as e:
        print('error in add: ', e)


window.ButtonAdd.clicked.connect(add_contact)


def delete_contact():
    """Удалить контакт."""
    try:
        current_item = window.listWidget.currentItem()
        username = current_item.text()
        user.del_contact(username)
        current_item = window.listWidget.takeItem(window.listWidget.row(current_item))
        del current_item
    except Exception as e:
        print('error in del:', e)


def send_message():
    """Отправить сообщение."""
    try:
        text = window.InputText.toPlainText()
        if text:
            selected_index = window.listWidget.currentIndex()
            user_name = selected_index.data()
            user.send_message(user_name, text)
            msg = '{} >>> {}'.format(name, text)
            window.storyMessage.addItem(msg)
    except Exception as e:
        print('error in send: ', e)


window.ButtonDelete.clicked.connect(delete_contact)
window.ButtonSend.clicked.connect(send_message)

window.show()
sys.exit(app.exec_())
