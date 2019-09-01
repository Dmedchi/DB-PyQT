# класс Storage на сервере:
#    - добавляет нового клиента в БД;
#    - проверяет наличие клиента в БД;
#    - получает клиента из БД по имени;
# класс ContactsList :
#    - наследуется от класса Storage;
#    - добавляет контакт в список контактов клиента;
#    - удаляет контакт из списка контактов клиента;
#    - получает список контактов клиента из БД

from baseDB import *


class Storage:
    """Хранилище"""

    def __init__(self, session):
        self.session = session

    def add_client(self, username, info=None):
        """Добавление клиента"""
        new_client = Client(username)
        self.session.add(new_client)
        self.session.commit()

    def client_exists(self, username):
        """Проверить наличие пользователя"""
        result = self.session.query(Client).filter(Client.name == username).count()
        return result

    def get_client_by_username(self, username):
        """Получить клиента по имени"""
        client = self.session.query(Client).filter(Client.name == username).first()
        return client

    def add_contact(self, client_username, contact_username):
        """Добавить контакт в список контактов клиента"""
        # получить клиента по имени и присвоить переменной contact
        contact = self.get_client_by_username(contact_username)
        # если удалось получить контакт
        if contact:
            # получить клиента по имени, который хочет добавить контакт
            client = self.get_client_by_username(client_username)
            # если удалось получить клиент
            if client:
                # получить id клиента и id контакта
                cc = ClientContacts(client_id=client.ClientId, contact_id=contact.ClientId)
                # и добавить их в таблицу "список контактов"
                self.session.add(cc)
                self.session.commit()
            else:
                self.session.rollback()
                print('что-то пошло не так..№1')
        else:
            self.session.rollback()
            print('что-то пошло не так..№2')

    def del_contact(self, client_username, contact_username):
        """Удалить контакт из списка контактов клиента"""
        # получить клиента по имени и присвоить переменной contact
        contact = self.get_client_by_username(contact_username)
        # если удалось получить контакт
        if contact:
            # получить клиента по имени, который хочет удалить контакт
            client = self.get_client_by_username(client_username)
            # если удалось получить клиент
            if client:
                # сделать запрос - найти нужный контакт по id в списке контактов
                cc = self.session.query(ClientContacts).filter(
                    ClientContacts.ClientId == client.ClientId).filter(
                    ClientContacts.ContactId == contact.ClientId).first()
                # и удалить его
                self.session.delete(cc)
                self.session.commit()
            else:
                self.session.rollback()
                print('что-то пошло не так..#1')

        else:
            self.session.rollback()
            print('что-то пошло не так..#2')

    def get_contacts(self, client_username):
        """Получить все контакты клиента"""
        client = self.get_client_by_username(client_username)
        contacts = []
        if client:
            all_contacts = self.session.query(ClientContacts).filter(ClientContacts.ClientId == client.ClientId)
            for one_contact in all_contacts:
                contact = self.session.query(Client).filter(Client.ClientId == one_contact.ContactId).first()
                contacts.append(contact)
        return contacts


if __name__ == '__main__':
    print('__name__ == __main__')
    print('***', Client.__table__, '***')
    print('***', ClientContacts.__table__, '***')
