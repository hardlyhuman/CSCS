import sqlite3

#   Setting up database connection
conn = sqlite3.connect('CSCSMaster.db')
print("Successful connection with database")

#   System model Creation
conn.execute(("""CREATE TABLE "system" ( 
                "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "IP" CHAR(15) NOT NULL,
                "OS" VARCHAR(25) NOT NULL,
                "EntryDate" DATETIME NULL 
                );"""))

print("Successfully Created System Table")


conn.execute(("""CREATE TABLE "user" (
                 "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                 "NAME" VARCHAR(30) NULL ,
                 "HOST" VARCHAR(30) NULL ,
                 "IP" INTEGER NOT NULL
                 REFERENCES "system" ("ID") 
                 );"""))

print("Successfully Created User Table")