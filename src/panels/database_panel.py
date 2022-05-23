
from database import Database
from utils.config import CONFIG
from utils.cosmetics import cprint, cinput



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
'''

class DatabasePanel:
    '''
    This class is the user panel which wraps Database class.
    This is for user input & should wrap those functions
    '''
        
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







    # collections = database.listCollections("admin")
    # print(collections)