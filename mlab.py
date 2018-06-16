import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds153460.mlab.com:53460/demochatxiec


host = "ds153460.mlab.com"
port = 53460
db_name = "demochatxiec"
user_name = "admin1"
password = "admin1"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())
