from cryptocode import encrypt, decrypt
import json, os
import ast
import pymongo

# from database import Database
# from utils.config import CONFIG
from utils.cosmetics import cprint, cinput

# TODO: Combine all this into 1 class?

## ! not attached to the main panel yet, just testing

'''
Class to save an encrypted dict via password
https://pymongo.readthedocs.io/en/stable/api/pymongo/database.html#pymongo.database.Database.command

Can delete / query with regex as well.
myquery = { "address": {"$regex": "^S"} }


MongoDB Commands I always forget:
- db.getUsers()
- db.getRoles({showPrivileges:false,showBuiltinRoles: true})
'''

'''
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
'''

def main():
    # m = MongoServerCache()
    # m.newServer()
    # m.decryptServer()
    # uri = m.serverInfoToURI(m.decryptServer())
    
    # m.connectToServer(uri)
    uri = "mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin"
    a = MongoStuff(uri)
    # a.insert('reece', 't2', {"name": "v", 'age': 12})

    # print(a.find_one('test', 'reece2', filter={"name": "reece"}))

    # docs = a.get_all_documents('test', 'reece2')
    # for d in docs:
    #     print(d)

    # a.test()

    # a.create_new_user()

    # a._actual_create_user('admin', username='reece', password='1234', roles=[{'role': 'readWrite', 'db': 'test'}])

    print(f'Databases: {a.get_databases()}')
    # a.get_users(Database(a.client, 'admin'))


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

    def get_databases(self) -> list:
        return self.client.list_database_names()

    def get_collections(self, myDB: Database) -> list:
        return myDB.list_collection_names()

    def get_users(self, db: Database):
        listing = db.command('usersInfo')
        for document in listing['users']:
            # print("user: " + document['user'] +" roles: "+ document['roles'][0]['role'])
            print("user: " + document['user'] +" roles: "+ str(document['roles']))
        return listing['users'] # what are other listings?
    # --------------
    def insert(self, dbName, collectionName, values={}) -> InsertOneResult:
        myCol = self.client[dbName][collectionName]
        x = myCol.insert_one(values)
        return x.inserted_id

    def find_one(self, dbName, collectionName, filter=None) -> dict:
        # find_one(dbname, collection, {"name": "Reece"})
        myCol = self.client[dbName][collectionName]
        return myCol.find_one(filter)

    def get_all_documents(self, dbName, collectionName, limit=0) -> list:
        # get_all_documents(dbname, collection)
        myCol = self.client[dbName][collectionName]
        return [doc for doc in myCol.find().limit(limit)]

    def delete_one(self, dbName, collectionName, filter=None) -> int:
        # delete_one(dbname, collection, filter={"name": "reece"})
        myCol = self.client[dbName][collectionName]
        return myCol.delete_one(filter)

    def delete_all_documents(self, dbName, collectionName) -> int:
        '''
        Deletes all documents in a collection. 
        @Returns the number of documents deleted.
        '''
        myCol = self.client[dbName][collectionName]
        x = myCol.delete_many({})
        return x.deleted_count

    def drop_collection(self, dbName, collectionName) -> bool:
        return self.client[dbName][collectionName].drop()

    def update_one(self, dbName, collectionName, filter={}, newValue={}):
        # update_one(db, collection, filter={"address": "123 street"}, newValue={"address": "124 main"})
        myCol = self.client[dbName][collectionName]
        myCol.update_one(filter, { "$set": newValue})

    ## -- test
    def create_new_user(self):
        username = input("New User Username: ")
        password = input("New User Password: ")
        database = input("Database (admin): ") or 'admin'

        print("""ROLES:""")
        shortHand = { # db.getRoles({showPrivileges:false,showBuiltinRoles: true})
            "rw": "readWrite",
            "r": "read",
            "w": "write",
            "dbo": "dbOwner",
            "backup": "backup",
            "restore": "restore",
            "-": "", # seperator
            "rad": "readAnyDatabase",
            "rwad": "readWriteAnyDatabase",
            "uad": "userAdminAnyDatabase",
            "dbaad": "dbAdminAnyDatabase",
            "--": "", # seperator
            "dba": "dbAdmin",            
            "ua": "userAdmin",
            "---": "", # seperator
            "ca": "clusterAdmin",
            "cm": "clusterManager",
            "root": "root",
        }
        for k, v in shortHand.items():
            if '-' in k:
                print(); continue
            print(f"[{k} ({v})]", end=" ")
            
        print(f"\n\n&eExample Input as>>> &fr;rw test;dbo reece;  &7(if no db is provided, {database} is used)")

        userRoles = input("Roles: ") # make copy paste / builder for this?
        
        if userRoles.endswith(";"): # remove last ;
            userRoles = userRoles[:-1]

        roles = []
        for action in userRoles.split(";"):
            values = action.split(" ") # rw, r, w, d, etc
            
            permission = values[0] # rw (even if its the only thing, it has to be index 0)
            db = database # our database name by default            
            # print(f"{values}=")

            if len(values) != 1: # ['rw']
                db = values[1] # supplied name ['rw', 'myDB']

            if permission in shortHand:
                permission = shortHand[permission]

            roles.append({"role": permission, "db": db})

        # confirm roles is correct:
        print(f"\n\nRoles: {roles}")
        if input("\nConfirm? (y/n): ").lower() != "y":
            self.create_new_user()

        self._actual_create_user(database, username, password, roles)
        # does not create any databases if they do not exist.

    def _actual_create_user(self, db, username, password, roles: list):
        db = self.client[db]
        db.command('createUser', username, 
            pwd=password,
            roles=roles
            # roles=[{'role': 'read', 'db': 'admin'}, {'role': 'readWrite', 'db': 'test'}]
        )


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


    # # 'Enable Access Control' `mongodb://myDBReader:password@127.0.0.1:27017/?authSource=admin`.
    # # mongo -u myUserAdmin -p OR mongo, then 'use admin; db.auth("myUserAdmin", "password123");'
    # database = Database("mongodb://myUserAdmin:password123@127.0.0.1:27017/?authSource=admin") 
    # # database = Database("mongodb://127.0.0.1:27017/")
    # dbs = database.listDatabases()
    # print(dbs)
    # database.dropDatabase("test_db", debug=True)
    # # print(database.listDatabaseRoles("admin"))
    # print("admin db users:", database.listUsers(database_name="admin"))
    # database.enableMongoDBAuthentication()
    # # creates user on the test database, with roles to access other databases as well. This means the myTester user MUST auth with the test database in the uri
    # # mongo -u myTester -p --authenticationDatabase test OR mongo, then 'use test; db.auth("myTester", "myPassXYZ");'
    # database.createNewUser("test", "myTester", "myPassXYZ", [{'role': 'readWrite', 'db': 'test'}, {'role': 'read', 'db': 'test_db'}])
    # print("test db users:", database.listUsers(database_name="test"))
    # database.changeUsersPassword("test", "myTester")
    # database.createTestCollection(collection_name="test-s", database_name="test")
    # print("="*20)
    # # database.createNewUser("test", "testingacc", "myPassXYZ", [{'role': 'readWrite', 'db': 'test'}])
    # print("test db users:", database.listUsers(database_name="test"))
    # database.deleteUser("test", "testingacc")
    # print("test db users:", database.listUsers(database_name="test"))