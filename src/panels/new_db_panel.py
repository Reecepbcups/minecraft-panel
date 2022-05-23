from cryptocode import encrypt, decrypt
import json, os
import ast
import pymongo

## ! not attached to the main panel yet, just testing

'''
Class to save an encrypted dict via password
https://pymongo.readthedocs.io/en/stable/api/pymongo/database.html#pymongo.database.Database.command
'''


def main():
    m = MongoServerCache()
    # m.newServer()
    # m.decryptServer()
    uri = m.serverInfoToURI(m.decryptServer())
    
    # m.connectToServer(uri)

    a = MongoStuff(uri)
    a.insert('test', 'reece2', {"name": "reece", 'age': 25})

    print(f'Databaseas: {a.getDatabases()}')
    
    a.getUsers(Database(a.client, 'admin'))


def userAccessControl():
    # Add check here to see if UAC is enabled
    adminUsername = input("Admin Username: ")
    adminPassword = input("Admin Password: ")
    db = Database("mongodb://127.0.0.1:27017/") # bc no auth yet
    db.enableMongoDBAuthentication(adminUsername, adminPassword)
    # Then you do what it says to do in this functiuon ^

'''
databasePanel = {
        "1": createDatabase,
        "2": deleteDatabase,
        "3": showDatabases,
        "4": createNewUser,
        "5": deleteUser,
        "6": showUser,
        "exit": exit,
    }


def __init__(self):
    self.databaseFunctions = {
        "1": ["Create DB", print],
        "2": ["Delete DB", print],
        "3": ["Show DBS\n", self.printDatabases],

        "4": ["Create User", self.createNewUser],
        "5": ["Delete User", print],
        "6": ["Show Users\n", print],

        "UAC": ["Enable user access control", userAccessControl],

        "cp": ["Main Menu", print],
        "exit": ["Main Menu", exit]
        # find collection
    }
'''


from pymongo.database import Database
from pymongo.results import InsertOneResult
class MongoStuff():
    def __init__(self, uri):
        self.client = pymongo.MongoClient(uri)

    def getDatabases(self) -> list:
        return self.client.list_database_names()

    def getCollections(self, myDB: Database) -> list:
        return myDB.list_collection_names()

    def getUsers(self, db: Database):
        listing = db.command('usersInfo')
        for document in listing['users']:
            print(document['user'] +" "+ document['roles'][0]['role'])
        return listing['users'] # what are other listings?

    def createDatabase(self, dbName) -> Database:
        myDB = self.client[dbName]
        return myDB

    # maybe just have a func to insert? since the DB stuff will auto be handled?
    # unless we find a way to get all roles
    # def createCollection() -> InsertOneResult:    
    #     return x.inserted_id

    def insert(self, dbName, collectionName, values={}) -> InsertOneResult:
        myCol = self.client[dbName][collectionName]
        x = myCol.insert_one(values)
        return x.inserted_id

class MongoServerCache:
    def __init__(self, file_name="MongoDBSCache.json"):
        # Gets current folder held location
        self.location = os.path.dirname(os.path.abspath(__file__))
        self.FILE_NAME = f"{self.location}/{file_name}"
        # print(self.FILE_NAME)

        self.servers = self._loadServersFromJSON()  

    def _askPassword(self, text="Enter your password to encrypt: "):
        return input(text)

    def decryptServer(self, server='') -> dict:
        if len(server) == 0:
            self.printServers()
        server = input("Enter Server Name to connect: ")
        if server not in self.servers:
            print("Server not found")
            self.decryptServer()
        else:
            dec_obj_str = decrypt(self.servers[server], self._askPassword("Enter password to unlock: "))
            print(f"{dec_obj_str}")
        # converts object to a dict from string
        return ast.literal_eval(dec_obj_str)

    def serverInfoToURI(self, decryptedServerInfo: dict) -> str:
        fmt = "mongodb://{user}:{password}@{addr}:{port}/?authSource={authdb}"
        uri = fmt.format(**decryptedServerInfo)
        print(uri)
        return uri

    def connectToServer(self, uri):
        os.system(f"mongo {uri}")

    def printServers(self):
        print(', '.join(self.servers.keys()))

    def newServer(self):
        server_name = input("Enter Server Name: ") or 'myServer'
        tempObj = {
            "addr": input("Enter IP Address: ") or '127.0.0.1',
            "port": input("Enter Port: ") or 27017,
            "user": input("Enter Username: ") or 'admin',
            "authdb": input("Enter AuthDB: ") or 'admin',
            "password": input("Enter Password: ") or 'password'
        }

        # removes http(s):// & the / at the end
        if tempObj['addr'].startswith("http"):
            tempObj['addr'] = tempObj['addr'].split("//")[-1]
        if tempObj['addr'].endswith("/"):
            tempObj['addr'] = tempObj['addr'][:-1]

        tempObj['port'] = int(tempObj['port'])

        myPass = self._askPassword()
        confirmPass = self._askPassword("Confirm Password: ")
        if myPass != confirmPass:
            print("Passwords do not match")
            self.newServer()

        enc_obj = encrypt(str(tempObj), myPass)

        self.servers[server_name] = enc_obj
        self._saveServersToJSON()

        print(f"Saved {server_name} as {enc_obj}")
    
    def _saveServersToJSON(self):
        with open(self.FILE_NAME, "w") as f:
            json.dump(self.servers, f, indent=4)

    def _loadServersFromJSON(self) -> dict:
        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "w") as f:
                json.dump({}, f)
                return {}

        with open(self.FILE_NAME, "r") as f:
            return json.load(f)


if __name__ == "__main__":
    main()