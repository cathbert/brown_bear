import json
from Pages.database_engine import ClientDatabase

clients = ClientDatabase()


def create_clients_json():
    data_ = {}
    data_['clients'] = []

    for client in clients.get_all_clients():
        data_['clients'].append({'Firstname': f'{client[0]}',
                                'Lastname': f'{client[1]}',
                                'Phone': f'{client[2]}',
                                'Email': f'{client[3]}',
                                'Home Address': f'{client[4]}'
                                })

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_, f, ensure_ascii=False, indent=4)

