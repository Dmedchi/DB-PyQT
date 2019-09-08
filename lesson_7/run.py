"""Создать клиента и добавить к нему несколько контактов."""

from baseDB import Client, ClientContacts, session

# добавить клиента
new_client = Client(name='Homer')
session.add(new_client)

new_client = Client(name='Marge')
session.add(new_client)

session.add_all([Client(name='Bart'),
                 Client(name='Lisa')])

clients = session.query(Client).all()
print(clients)

for client in clients:
    print(client.ClientId)

# добавить контакт
new_friend = ClientContacts(1, 2)
session.add(new_friend)

new_friend = ClientContacts(1, 3)
session.add(new_friend)

new_friend = ClientContacts(1, 4)
session.add(new_friend)

contacts = session.query(ClientContacts).all()
print(contacts)

session.commit()

