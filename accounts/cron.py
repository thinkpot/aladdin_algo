from .models import Client
from pya3 import *


def new_alice_sessionid():
    all_clients = Client.objects.filter(broker__broker_symbol='ALCB')
    for client in all_clients:
        alice = Aliceblue(user_id=client.client_user_id, api_key=client.client_id)
        session_id = alice.get_session_id()
        if session_id:
            client.session_id = session_id.get('sessionID')
            client.connected = True
            client.save()