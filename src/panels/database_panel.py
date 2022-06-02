from cryptocode import encrypt, decrypt
import json, os
import ast
import pymongo

from utils.cosmetics import cprint, cinput, cfiglet

from typing import Tuple
import bson

from pymongo.database import Database
from pymongo.results import InsertOneResult

from pick import pick

'''
https://pymongo.readthedocs.io/en/stable/api/pymongo/database.html#pymongo.database.Database.command

Can delete / query with regex as well.
myquery = { "address": {"$regex": "^S"} }

"UAC": ["Enable user access control", userAccessControl],

MongoDB Commands I always forget:
- db.getUsers()
- db.getRoles({showPrivileges:false,showBuiltinRoles: true})
'''

class DatabasePanel():
    '''
    Main panel for calling from the console
    '''
    def __init__(self):
        self.m = MongoServerCache()
        self.uri = ""
        self.currentServer = "" # changes with each URI change
        self.databasePanel = {
            'ld': ["List Databases", self.showDatabases],            
            # "drop": ["Drop Database", self.deleteDatabase],

            "cu": ["Create User", self.createNewUser],
            # "ud": ["Delete User", self.deleteUser],
            "su": ["Show Users\n", self.showUsers],

            "suri": ["Show URI\n", self.showURI],

            "ch": ["Change Active Instance", self._change_uri],
            "sh": [f"Server Shell", self.connectToServer],
            "add": ["Add a New Mongo Instance\n", self.addInstance],
            
            "dump": ["Backup Database", self.backupDatabase],
            "rstr": ["Backup Database", self.restoreFromBackup],

            "exit": ["exit", exit],
        }
        self.run()

    def run(self): 
        cfiglet("&a", "MongoDB Panel", clearScreen=True)               
        while True: 
            if len(self.currentServer) > 0:
                cprint(f"\t&eCurrent connected server: {self.currentServer}\n")        
            for k, v in self.databasePanel.items():
                cprint(f"[{k}]\t {v[0]}")

            # Split it into args so we can pass through functions? This needed?
            request = cinput("\nDB> ")
            if request == "cp":
                from console import main
                main()
            if request not in self.databasePanel.keys():
                cprint(f"\t&c{request} not in database panel")
                continue
            self.databasePanel[request][1]() 
            cfiglet("&a", "MongoDB Panel", clearScreen=False)            

    def showURI(self):
        if len(self.uri) == 0:
            self._change_uri()        
        print(self.uri)

    def backupDatabase(self):
        # TODO: allow a user to select databases to backup?
        # Allow user to change output DIR OR auto put in there from the one in config
        os.system(f"mongodump --uri {self.uri}")

    def restoreFromBackup(self):
        cmd = 'mongorestore --uri mongodb://localhost:27017/dbName --db YOUR_DB_NAME YOUR_TARGET_FOLDER/YOUR_DB_NAME'
        print("THIS COMMAND IS NOT DONE YET")

    def connectToServer(self):        
        self._set_server_uri()
        self.m.connectToServer(self.uri)

    def showDatabases(self):    
        self._set_server_uri()        
        cprint(f"\n&fDatabases: &b{self.mFuncs.get_databases()}")
        cinput("\n&7Enter to continue...")

    def addInstance(self):
        self.m.newServer()

    def createNewUser(self):
        self._set_server_uri()    
        username = input("New User Username: ")
        password = input("New User Password: ")
        database = input("Database (admin): ") or 'admin'    
        self.mFuncs.create_new_user(username, password, database)
        input("Enter to continue...")

    def deleteDatabase(self):
        dbToDelete = input("DB to delete:")
        if dbToDelete not in self.mFuncs.get_databases():
            cprint(f"\t&c{dbToDelete} not in this server's mongodb")
            return

        confirm = cinput(f"\n&c[!] Type 'delete {dbToDelete}' to confirm deletion\n>>").replace("\'", "").strip()
        if dbToDelete == confirm:
            self.mFuncs.drop_database(dbToDelete)
            cprint(f"\t&aDatabase {dbToDelete} deleted")
        else:
            cprint(f"\t&cDatabase names do not match... {dbToDelete} != {confirm}")
        

    def deleteUser(self):
        userToDel = input("User to delete:")
        usersDatabase = input("Database they are in:")
        usersInTheDB = self.mFuncs.get_users(usersDatabase)
        if userToDel not in usersInTheDB:
            cprint(f"\t&c{userToDel} not in this server's mongodb")
            return
        self.mFuncs.drop_user(usersDatabase, userToDel)

    def showUsers(self):
        self._set_server_uri()        
        print("Databases:", self.mFuncs.get_databases())

        db = cinput("&eDatabase you want to show users for &e>> ")
        if db not in self.mFuncs.get_databases():
            cprint(f"&cDatabase {db} not in this server's mongodb")
            self.showUsers()

        print()
        users = {}
        for u in self.mFuncs.get_users(db):      
            roles = []
            for r in u['roles']:
                roles.append(str(r['role']) + ": " + str(r['db']))
            # print(f"{u['user']}\n\t{roles}")
            users[u['user']] = roles

        for k, v in users.items():
            print(f"{k}\t{v}")
        input("Enter to continue...")


    def _set_server_uri(self):
        if len(self.uri) > 0:
            return self.uri
        self._change_uri()
        return self.uri
    def _change_uri(self):
        server, serverName = self.m.decryptServer()
        if server == {} and serverName == "":            
            return
        self.uri = self.m.serverInfoToURI(server, debug=False)
        self.mFuncs = MongoHelper(self.uri)
        self.currentServer = serverName

def main():
    # m = MongoServerCache()
    # m.newServer()
    # m.decryptServer()
    # uri = m.serverInfoToURI(m.decryptServer())
    
    # m.connectToServer(uri)
    # uri = "mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin"
    # a = MongoHelper(uri)
    # a.insert('reece', 't2', {"name": "v", 'age': 12})

    # print(a.find_one('test', 'reece2', filter={"name": "reece"}))

    # docs = a.get_all_documents('test', 'reece2')
    # for d in docs:
    #     print(d)

    # a.test()

    # a.create_new_user()

    # a._actual_create_user('admin', username='reece', password='1234', roles=[{'role': 'readWrite', 'db': 'test'}])

    # print(f'Databases: {a.get_databases()}')
    # a.get_users(Database(a.client, 'admin'))
    pass

class MongoHelper():
    '''
    Helper class to make functions easier with MongoDB collections
    '''
    def __init__(self, uri):
        self.client = pymongo.MongoClient(uri)

    def get_databases(self) -> list:         
        return self.client.list_database_names()

    def get_collections(self, myDB: Database) -> list:
        if isinstance(myDB, str):
            myDB = Database(self.client, myDB) 
        return myDB.list_collection_names()

    def get_users(self, db: Database, debug=False):
        if isinstance(db, str):
            db = Database(self.client, db)        

        listing = db.command('usersInfo')
        if debug == True:
            for document in listing['users']:
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

    def drop_database(self, dbName) -> bool:
        return self.client[dbName].drop()

    def update_one(self, dbName, collectionName, filter={}, newValue={}):
        # update_one(db, collection, filter={"address": "123 street"}, newValue={"address": "124 main"})
        myCol = self.client[dbName][collectionName]
        myCol.update_one(filter, { "$set": newValue})

    ## -- test
    def create_new_user(self, username, password, database):
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
    def drop_user(self, db, username):
        db = self.client[db]
        db.command('dropUser', username)


# TODO make a parent class for EncyrptedLogin, also so redis can use it
class MongoServerCache:
    '''
    ServerCache which handles the file, encrypting, decrypting, and URI information
    '''
    def __init__(self, file_name="cache_mongodb.json"):
        # Gets current folder held location
        self.location = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.FILE_NAME = f"{self.location}/{file_name}"
        # print(self.FILE_NAME)

        self.servers = self._loadServersFromJSON()  

    def _askPassword(self, text="&eEnter your password to encrypt >> "):
        return cinput(text)

    def decryptServer(self, server='') -> Tuple[dict, str]:      
        if len(server) == 0:  
            server, _ = pick(list(self.servers.keys()), 'Mongo Server to Connect too: ', multiselect=False, indicator=' =>')

        cprint(f"\n&a[!] Selected server: {server}")
        
        dec_obj_str = decrypt(self.servers[server], self._askPassword("&eEnter password to unlock &f>> "))
            # print(f"{dec_obj_str}") # prints dict of all values
        # converts object to a dict from string        
        return ast.literal_eval(dec_obj_str), server

    def serverInfoToURI(self, decryptedServerInfo: dict, debug=False) -> str:
        fmt = "mongodb://{user}:{password}@{addr}:{port}/?authSource={authdb}"
        uri = fmt.format(**decryptedServerInfo)
        if debug: print(uri)
        return uri

    def connectToServer(self, uri):
        os.system(f"mongo {uri}")

    def printServers(self):
        print(', '.join(self.servers.keys()))

    def newServer(self):
        server_name = input("New MongoDB Instance Name: ") or 'myServer'
        tempObj = {
            "addr": input("Enter IP Address/URL (127.0.0.1): ") or '127.0.0.1',
            "port": input("Enter Port (27017): ") or 27017,
            "user": input("Enter Username: ") or 'admin',            
            "password": input("Enter Password: ") or 'password',
            "authdb": input("Enter Authentication Database (admin): ") or 'admin',
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


# def userAccessControl():
#     # Add check here to see if UAC is enabled
#     adminUsername = input("Admin Username: ")
#     adminPassword = input("Admin Password: ")
#     db = Database("mongodb://127.0.0.1:27017/") # bc no auth yet
#     db.enableMongoDBAuthentication(adminUsername, adminPassword)
#     # Then you do what it says to do in this functiuon ^