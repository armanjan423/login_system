import pymongo

def get_db_handle(db_name, host, port, username, password):
    client = pymongo.MongoClient(host=host,
                                 port=int(port),
                                 username=username,
                                 password=password
                                )
    db_handle = client[db_name]
    return db_handle, client

def get_db_client(connection_string):
    client = pymongo.MongoClient(connection_string)
    db = client.get_database() # Gets database from connection string if provided
    return db, client
