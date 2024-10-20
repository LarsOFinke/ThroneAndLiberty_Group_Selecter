import os, sqlite3
from main import ROLES


CONNECTION_STRING: str = f"{os.path.abspath(__file__)[:-7]}MembersDB.db"



def create_database():
    con = sqlite3.connect(CONNECTION_STRING)
    cursor = con.cursor()
    
    with con:
        sql: str =  "CREATE TABLE tblMembers(" \
                    "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                    "Name TEXT NOT NULL UNIQUE, " \
                    "RolesIDRef INTEGER NOT NULL)"
        cursor.execute(sql)
        
        sql: str =  "CREATE TABLE tblRoles(" \
                    "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                    "RolesName TEXT NOT NULL UNIQUE)"
        cursor.execute(sql)
        
        sql: str = "INSERT INTO tblRoles(RolesName) VALUES ('Tank')"
        cursor.execute(sql)
        sql: str = "INSERT INTO tblRoles(RolesName) VALUES ('Heal')"
        cursor.execute(sql)
        sql: str = "INSERT INTO tblRoles(RolesName) VALUES ('DPS')"
        cursor.execute(sql)

if not os.path.exists(CONNECTION_STRING):
    create_database()
   
   
    
CON = sqlite3.connect(CONNECTION_STRING)
CURSOR = CON.cursor()


def add_player(name: str, role: int):   # Role 1 = Tank | 2 = Heal | 3 = DPS
    with CON:
        sql: str = "INSERT INTO tblMembers(Name, RolesIDRef) VALUES (?, ?)"
        CURSOR.execute(sql, (name, role))
       

def get_single_player(name: str) -> tuple:
    with CON:
        sql: str = "SELECT Name, RolesIDRef FROM tblMembers WHERE Name = ?"
        CURSOR.execute(sql, (name,))
        
        for player in CURSOR:
            return player

def read_players() -> dict: # Name : Role
    players: dict = {} 
    
    with CON:
        sql: str = "SELECT Name, RolesIDRef FROM tblMembers ORDER BY Name"
        CURSOR.execute(sql)
        
        for player in CURSOR:
            players[player[0]] = ROLES[player[1]]  
            
    return players


def update_player(role: int, name: str):    # Role 1 = Tank | 2 = Heal | 3 = DPS
    with CON:
        sql: str = "UPDATE tblMembers SET RolesIDRef = ? WHERE Name = ?"
        CURSOR.execute(sql, (role, name))
        

def delete_player(name: str):
    with CON:
        sql: str = "DELETE FROM tblMembers WHERE Name = ?"
        CURSOR.execute(sql, (name,))

