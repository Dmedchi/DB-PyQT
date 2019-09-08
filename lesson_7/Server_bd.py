"""Хранилище на стороне сервера."""

from baseDB import *


class Storage:

    def __init__(self, session):
        self.session = session

    def add_client(self, username, info=None):
        """Добавить клиента."""
        new_client = Client(username)
        self.session.add(new_client)
        self.session.commit()

    def client_exists(self, username):
        """Проверить наличие пользователя."""
        result = self.session.query(Client).filter(Client.name == username).count()
        return result

    def get_client_by_username(self, username):
        """Получить клиента по имени."""
        client = self.session.query(Client).filter(Client.name == username).first()
        return client

    def add_contact(self, client_username, contact_username):
        """Добавить контакт в список контактов клиента."""
        contact = self.get_client_by_username(contact_username)
        if contact:
            client = self.get_client_by_username(client_username)
            if client:
                cc = ClientContacts(client_id=client.ClientId, contact_id=contact.ClientId)
                self.session.add(cc)
                self.session.commit()
            else:
                self.session.rollback()
                print('Не удалось добавить контакт.')
        else:
            self.session.rollback()
            print('Не удалось добавить контакт.')

    def del_contact(self, client_username, contact_username):
        """Удалить контакт из списка контактов клиента."""
        contact = self.get_client_by_username(contact_username)
        if contact:
            client = self.get_client_by_username(client_username)
            if client:
                cc = self.session.query(ClientContacts).filter(
                    ClientContacts.ClientId == client.ClientId).filter(
                    ClientContacts.ContactId == contact.ClientId).first()
                self.session.delete(cc)
                self.session.commit()
            else:
                self.session.rollback()
                print('Не удалось удалить контакт.')
        else:
            self.session.rollback()
            print('Не удалось удалить контакт.')

    def get_contacts(self, client_username):
        """Получить все контакты клиента."""
        client = self.get_client_by_username(client_username)
        contacts = []
        if client:
            all_contacts = self.session.query(ClientContacts).filter(ClientContacts.ClientId == client.ClientId)
            for one_contact in all_contacts:
                contact = self.session.query(Client).filter(Client.ClientId == one_contact.ContactId).first()
                contacts.append(contact)
        return contacts
