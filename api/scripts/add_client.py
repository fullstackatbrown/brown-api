from datetime import datetime
from sys import argv
from uuid import uuid4
import sqlite3
import os

# The maximum number of Client IDs per student email address.
MAX_IDS_PER_STUDENT = 1

# simplify collection name
# clients = db.clients


def add_client_id(email, username, client_id=None):
    if email[-10:] != '@brown.edu':
        print("Invalid student email")
        return None
    client_id = str(uuid4())
    with sqlite3.connect(os.environ['DB_LOCATION']) as con:
        newuser = (client_id, username, email, str(datetime.now()))
        passed = False
        while not passed:
            passed = True
            try:
                con.execute("INSERT INTO auth (key, name, email, joined) VALUES(?,?,?,?)", newuser)
            except:
                client_id = str(uuid4())
                passed = False
        return client_id

if __name__ == '__main__':
    if len(argv) < 3 or len(argv) > 4:
        print("Usage:  python -m api.scripts.add_client <client_email> <username> [client_id]")
        print("\tclient_email - Required. An @brown.edu email address.")
        print("\tusername - Required. A user who owns this client (typically a first and last name, like 'Josiah Carberry').")
        print("\tclient_id - Optional. Provide a string representation of a UUID4 client ID.")
        exit()

    if len(argv) == 3:
        client_id = add_client_id(argv[1], argv[2])
    if len(argv) == 4:
        client_id = add_client_id(argv[1], argv[2], client_id=argv[3])

    if not client_id:
        print("Email is not a Brown address. Unable to add client to database.")
    else:
        print("Client ID: ", client_id)
