from pymongo import MongoClient
from pymongo import database
from pymongo.typings import _DocumentType

from utils.cosmetics import cinput, cprint

from utils.config import CONFIG

class Database:

    '''
    config.yml

    Mongo-Authentication: # Maybe allow the user to store uri's here?
      admin: admin
      myTester: test
    '''

    def __init__(self, uri):
        # self.CONNECTION_URI = uri   
        self.client = MongoClient(uri)

    def getClient(self):
        return self.client

    def listDatabases(self) -> list:
        return self.client.list_database_names()

    def getDatabase(self, database_name) -> database.Database[_DocumentType]:
        '''
        Returns a database, or a new one if not created already
        '''
        return self.client[database_name]

    def dropDatabase(self, database_name, debug=False) -> bool:
        # ensure database_name exist
        if database_name in self.listDatabases():
            # removes ' incase the user actually type these too
            v = cinput(f"\n&c[!] Type 'delete {database_name}' to confirm deletion\n>>").replace("\'", "").strip()
            if(v == f"delete {database_name}"):
                self.client.drop_database(database_name)
                if debug: print(f"Dropped database: {database_name}")
                return True
            else:
                cprint("&eIncorrect Input")                
                self.dropDatabase(database_name) # Try again, incorrect input
            
        if debug: print(f"Database {database_name} not found, Can't delete...")
        return False

    # Roles
    def enableMongoDBAuthentication(self, username, password):
        # TODO: Add input here in the future
        notCreated = self.createNewUser("admin", username, password, [{'role': 'userAdminAnyDatabase', 'db': 'admin'}, "readWriteAnyDatabase"])
        if notCreated:
            cprint("\n\n&e[!] You should now stop the mongodb (docker or service file) and start with authetication")
            cprint("&e - nano /etc/mongodb.conf")
            cprint("&e - add the following\n\nsecurity:\n\tauthorization: \"enabled\"")
            cprint("&e - systemctl restart mongodb.service && journalctl -u mongodb\n\n\n")    

    def getRoleInfo(self, database_name="", role=""):
        # return self.getDatabase(database_name).command({
        #     'rolesInfo': {'role': role, 'db': database_name},
        #     'showPrivileges': True, 'showBuiltinRoles': True
        # })
        return ["dbAdmin", "dbOwner", "read", "readWrite", "userAdmin"]

    # def authenticate(self, database_name, username, password):
    #     return self.getDatabase(database_name).authenticate(username, password)

    # Collections
    def listCollections(self, database_name) -> list:
        return self.client[database_name].list_collection_names()

    def getCollection(self, database_name, collection_name):
        return self.client[database_name][collection_name]

    # Users
    def createNewUser(self, database_name, username, password, roles=[]) -> bool:
        if username in self.listUsers(database_name):
            cprint(f"&c[!] User {username} already exsist in {database_name}")
            return False

        # ymlConfig = Yaml(PATH_TO_CONFIG_FILE)
        if CONFIG.get("Mongo-Authentication") == None:
            CONFIG["Mongo-Authentication"] = {}

        authUsers = CONFIG.get("Mongo-Authentication")
        if username in authUsers:  # if the user is already in the config for a database            
            database = authUsers[username] 
            cprint(f"&cUser already exists in config.yml &e({username} in '{database}' db)")
            return False
        else: 
            # update authUsers dict, set to CONFIG, and save. Then add to database            
            authUsers[username] = database_name 
            CONFIG.set("Mongo-Authentication", authUsers)
            CONFIG.save()
            # print(authUsers)

            # maybe do this first and ensure it works before adding to config?
            v = self.getDatabase(database_name).command({
                'createUser': username,
                'pwd': password,
                'roles': roles
            })
            print(v)
            print(f"&aUser {username} has been created in {database_name} w/ roles {roles}.")
            print("It will not show until a collection is created\n&fAdded to config")

            # check if user was created
            if username in self.listUsers(database_name):
                print(f"&aUser {username} was found in  self.listUsers of {database_name}")

        return True

    def changeUsersPassword(self, database, user):
        if user not in self.listUsers(database):
            cprint(f"&c[!] User {user} not found in {database}")
            return False

        newPass = cinput("\n&b[!] Enter new password: ")
        status = self.getDatabase(database).command({
            'updateUser': user,
            'pwd': newPass
        })
        status = self._getDocumentStatus(status)
        output = f"&aPassword for user {user} has been changed to: {newPass}"
        if status == False:
            output = f"&cPassword change was not successfull for {user}"
        cprint(output)
        return status

    def createTestCollection(self, database_name, collection_name, show_output=False):
        db = self.getDatabase(database_name)

        if not collection_name in db.list_collection_names():
            db.create_collection(collection_name)

        col = db.get_collection(collection_name)
        col.insert_one({'example': 'collection-for-showcase'})
        if show_output: print(col.find_one())

    def deleteUser(self, database_name, user):        
        if user not in self.listUsers(database_name):
            cprint(f"&c[!] User {user} not found in {database_name}")
            return False

        status = self.getDatabase(database_name).command({
            'dropUser': user
        })
        return  self._getDocumentStatus(status)

    def listUsers(self, database_name):
        listing = self.getDatabase(database_name).command("usersInfo")
        users = {}
        for doc in listing['users']:
            users[doc['user']] = doc['roles']
        return users

    def _getDocumentStatus(self, _CodecDocumentType: dict):
        '''
        Take the return from .command() -> a true or false value
        '''
        for k, v in _CodecDocumentType.items():
            if k == "ok" and v == 1.0:
                print(k, v)
                return True
        return False
