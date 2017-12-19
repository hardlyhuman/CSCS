import sqlite3

#   Setting up database connection
conn = sqlite3.connect('CSCSMaster.db')
print("Successful connection with database")

#   System model Creation
conn.execute(("""CREATE TABLE "system" ( 
                "ID" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "IP" char(15) NOT NULL,
                "OS" VARCHAR(25) NOT NULL,
                "EntryDate" DATETIME NULL 
                );"""))

print("Successfully Created System Table")