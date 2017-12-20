###################################################
# CSCS/Source/Database.py: Consists of all the required models for the Client Statistics Collection System
# __author__ = "Sri Harsha"
# __copyright__ = "Copyright 2017, Sri Harsha"
# __Team__ = ["Sri Harsha"]
# __license__ = "GNU General Public License v3.0"
# __version__ = "0.5"
# __maintainer__ = "Sri Harsha"
# __email__ = "sriharsha.g15@iiits.in"
# __status__ = "Development"
####################################################


import sqlite3

#   Setting up database connection
conn = sqlite3.connect('CSCSMaster.db')
print("Successful connection with database")

#   System Model Creation
conn.execute(("""CREATE TABLE "system" ( 
                "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "IP" CHAR(15) NOT NULL,
                "OS" VARCHAR(25) NOT NULL,
                "EntryDate" DATETIME NULL 
                );"""))

#print("Successfully Created System Table")

#   User Model Creation
conn.execute(("""CREATE TABLE "user" (
                 "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                 "NAME" VARCHAR(30) NULL ,
                 "HOST" VARCHAR(30) NULL ,
                 "IP" INTEGER NOT NULL
                 REFERENCES "system" ("ID") 
                 );"""))

#print("Successfully Created User Table")


#print("Indexed User Model ON IP Field")

#   CPUInfo Model Creation
conn.execute(("""CREATE TABLE "cpuinfo" (
                "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "BootTime" BIGINT NULL,
                "Usage" DOUBLE NOT NULL,
                "Count" DOUBLE NOT NULL,
                "Interrupts" BIGINT NULL,
                "SoftInterrupts" BIGINT NULL,
                "SystemCalls" BIGINT NULL,
                "Logs" TEXT NULL,
                "MinFreq" DOUBLE NULL,
                "MaxFreq" DOUBLE NULL,
                "CurrFreq" DOUBLE NULL,
                "EntryDate" DATETIME NULL,
                "IP" INTEGER NOT NULL
                REFERENCES "system" ("ID")
);"""))

#print("Successfully Created CPUInfo Table")

#print("Indexed Cpuinfo Model ON IP Field")

#   DiskInfo Model Creation
conn.execute(("""CREATE TABLE "diskinfo" (
                 "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                 "AgentName" VARCHAR(30) NULL ,
                 "MountPoint" VARCHAR(30) NULL,
                 "FSType" VARCHAR(30) NULL,
                 "OPTS" TEXT NULL,
                 "EntryDate" DATETIME NULL,
                 "IP" INTEGER NOT NULL 
                 REFERENCES "system" ("ID")
);"""))

#print("Successfully Created DiskInfo Table")

#print("Indexed Diskinfo Model ON IP Field")

#   DiskDetail Model Creation
conn.execute(("""CREATE TABLE "diskdetail" (
                 "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                 "TotalDisk" BIGINT NOT NULL,
                 "UsedDisk" BIGINT NOT NULL,
                 "FreeDisk" BIGINT NOT NULL,
                 "Percent" DOUBLE NOT NULL,
                 "EntryDate" DATETIME NULL,
                 "IP" INTEGER NOT NULL
                 REFERENCES "system" ("ID")
);"""))

#   SwapDetail Model Creation
conn.execute(("""CREATE TABLE "swapdetail" (
                 "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                 "Total" BIGINT NOT NULL,
                 "Used" BIGINT NOT NULL,
                 "Free" BIGINT NOT NULL,
                 "Percent" DOUBLE NOT NULL,
                 "EntryDate" DATETIME NULL,
                 "IP" INTEGER NOT NULL
                 REFERENCES "system" ("ID")
);"""))

#print("Successfully Created DiskDetail Table")

#print("Indexed DiskDetail Model ON IP Field")


#   MemoryDetail Model Creation
conn.execute(("""CREATE TABLE "memorydetail" (
                 "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                 "TotalMemory" BIGINT NOT NULL,
                 "AvailMemory" BIGINT NOT NULL,
                 "Percent" DOUBLE NOT NULL,
                 "UsedMemory" BIGINT NOT NULL,
                 "FreeMemory" BIGINT NOT NULL,
                 "CacheMemory" BIGINT NULL,
                 "BufferMemory" BIGINT NULL,
                 "ActiveMemory" BIGINT NULL,
                 "InactiveMemory" BIGINT NULL,
                 "SharedMemory" BIGINT NULL,
                 "EntryDate" DATETIME NULL,
                 "IP" INTEGER NOT NULL
                 REFERENCES "system" ("ID") 
);"""))

#print("Successfully Created MemoryDetail Table")
print("Successfully created models")



conn.execute("""CREATE INDEX "user_ip" ON "user" ("IP");""")  #   Index Creation ON user(model) - IP (field)
conn.execute("""CREATE INDEX "diskdetail_ip" ON "diskdetail" ("IP");""")    #   Index Creation ON diskdetail(model) - IP (field)
conn.execute("""CREATE INDEX "diskinfo_ip" ON "diskinfo" ("IP");""")    #   Index Creation ON diskinfo(model) - IP (field)
conn.execute("""CREATE INDEX "cpuinfo_ip" ON "cpuinfo" ("IP");""")  #   Index Creation ON cpuinfo(model) - IP (field)
