
from database import Database
from utils.config import CONFIG
from utils.cosmetics import cprint, cinput

'''
This file is the user panel which wraps Database class.
That class should be used for CLI arguments, this is for user input
'''

def userAccessControl():
    # Add check here to see if UAC is enabled
    adminUsername = input("Admin Username: ")
    adminPassword = input("Admin Password: ")
    db = Database("mongodb://127.0.0.1:27017/") # bc no auth yet
    db.enableMongoDBAuthentication(adminUsername, adminPassword)
    # Then you do what it says to do in this functiuon ^

class DatabasePanel:

    

    # Login to database. Input Username. If so, show the user that database.
    # Confirm. Then ask for password. Put into URI
    # def __init__(self, user="", password="", authSource="admin", hostIP="127.0.0.1", port=27017):
    def __init__(self):
        self.databaseFunctions = {
            "1": ["Create DB", print],
            "2": ["Delete DB", print],
            "3": ["Show DBS\n", self.printDatabases],

            "4": ["Create User", self.createNewUser],
            "5": ["Delete User", print],
            "6": ["Show Users\n", print],

            "UAC": ["Enable user access control", userAccessControl],
            # find collection
        }

        ## Login
        # if len(user) == 0:
        # user = cinput("Username: ")
        user = "myUserAdmin"
        # user = "myTester"

        # if len(password) == 0:
        # password = cinput("Password: ")
        password = 'password123' # myUserAdmin
        # password = 'myPassXYZ' # myTester

        users = CONFIG.get("Mongo-Authentication")
        if user in users:
            authSource = users[user]
            print(f"Auto authenticating with the {authSource} database from config.yml...")
        else:
            authSource = input(f"Authentication Database ({authSource}): ") or authSource

        hostIP = input("Host IP (127.0.0.1): ") or "127.0.0.1"
        port = input("Port (27017): ") or "27017"

        ip_addr = f"{hostIP}:{port}" #input("Auth IP (127.0.0.1:27017): ")
        uri = f"mongodb://{user}:{password}@{ip_addr}/?authSource={authSource}"
        self.dbObj = Database(uri)

        self.printDatabases()

        while True:
            # cfiglet("&3", "Control Panel", clearScreen=True)
            for k, v in self.databaseFunctions.items():
                cprint(f"[{k}]\t {v[0]}")

            # Split it into args so we can pass through functions? This needed?
            request = input("\nDATABASE> ")
            self.databaseFunctions[request][1]() 
    

    def createNewUser(self):
        username = input("New User Username: ")
        password = input("New User Password: ")
        database = input("Database: ")

        print("""ROLES:
          [{'role': 'readWrite', 'db': 'test'}, {'role': 'read', 'db': 'test_db'}]

            Input as:
            rw test;r test_db
        """)

        shortHand = {
            "rw": "readWrite",
            "r": "read",
            "w": "write",
            "d": "dbOwner",
        }

        userRoles = input("Roles: ") # make copy paste / builder for this?
        
        if userRoles.endswith(";"): # remove last ;
            userRoles = userRoles[:-1]

        roles = []
        for action in userRoles.split(";"):
            permission = action.split(" ")[0] # rw, r, w, d, etc
            db = action.split(" ")[1] # databaseName

            if permission in shortHand:
                permission = shortHand[permission]

            roles.append({"role": permission, "db": db})

        self.dbObj.createNewUser(username, password, database, roles)
        # dbObj.createNewUser('newDB', 'mynewDBUser', 'test', [])

        placeholderCollection = input("Create a placeholder collection so the database appears? ((y)/n)")
        if placeholderCollection == "y":
            self.dbObj.createTestCollection(database, 'panel-placeholder-collection')
        
    def printDatabases(self):
        print(f"{self.dbObj.listDatabases()}")
        input("Enter to continue...")

    def listUsersInDatabase(self):
        database = input("Database: ")
        print(self.dbObj.listUsers(database))
        input("Enter to continue...")

    def deleteDatabase(self):
        database = input("Database: ")
        self.dbObj.dropDatabase(database, True)

   

    # cfiglet("&a", "Database Panel", clearScreen=True)
    # for k, v in databaseFunctions.items():
    #     cprint(f"[{k}]\t {v[0]}")
    # request = input("\nDATABASE> ")
    # databaseFunctions[request][1] # check if is object or is a function with (). Then do the opposite?




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


    # collections = database.listCollections("admin")
    # print(collections)