###################################################
# CSCS/Source/server.py: Consists of the server script for the Client Statistics Collection System
# __author__ = "Sri Harsha"
# __copyright__ = "Copyright 2017, Sri Harsha"
# __Team__ = ["Sri Harsha"]
# __license__ = "GNU General Public License v3.0"
# __version__ = "1.0"
# __maintainer__ = "Sri Harsha"
# __email__ = "sriharsha.g15@iiits.in"
# __status__ = "Development"
####################################################




import base64
import codecs
import hashlib
import json
import os
import smtplib
import sqlite3
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import paramiko
import xmltodict
from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-s[-1]]


class AESCipher:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


def sshconn(ip, port, username, password):
    try:
        Client = paramiko.SSHClient()
        Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        Client.connect(ip, port, username, password)
        print("SSH connection Successful.")

        SFTPClient = Client.open_sftp()
        stdin, stdout, stderr = Client.exec_command('echo "SampleTest"')
        stdin.close()
        response = str(stdout.read())
        output = response.find('"')

        if output != -1:
            flag = True
        else:
            flag = False

        parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if flag:
            Dir = "C:\\Windows\\Temp\\"
            command = "python C:\\Windows\\Temp\\client.py"
        else:
            Dir = "/tmp/"
            command = 'sudo python /tmp/client.py'

        if not os.path.exists(Dir):
            os.makedirs(Dir)

        SFTPClient.put(parent + '/Source/client.py', Dir + 'client.py')
        print("File Transferred!")

        stdin, stdout, stderr = Client.exec_command(command)

        if not flag:
            stdin.write(password + '\n')
            stdin.flush()
            stdin.close()

        temp = AESCipher('CrossOver Project')

        response = stdout.read()
        OriginalMessage = temp.decrypt(response)

        FinalOutput = json.loads(OriginalMessage)

        SFTPClient.close()
        Client.close()
        return FinalOutput

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication has failed!")
        quit()

    except paramiko.ssh_exception.BadHostKeyException:
        print("Server hostkey could not be verified!")
        quit()

    except paramiko.ssh_exception.SSHException:
        print("Error connecting or establishing SSH Session!")
        quit()

    except paramiko.ssh_exception.socket.error:
        print("Socket error occurred while connecting!")
        quit()

    except IOError:
        print("IOError while trying to read file!")
        quit()

    except:
        print("Unknown exception: {0}!".format(str(sys.exc_info()[0])))
        quit()


def sender(toaddr, body, current, limit, subject):
    try:
        Opener = codecs.open("EmailConfig.json", encoding="UTF-8")
        Emailer = json.loads(Opener.read())
        Opener.close()
        fromaddr = Emailer["email_configurations"]["username"]
        pswd = Emailer["email_configurations"]["password"]

    except IOError:
        print("Cannot open file")
        quit()

    except FileNotFoundError:
        print("Check whether file exists or not")
        quit()

    except ConnectionError:
        print("Connection Error")
        quit()

    mail = MIMEMultipart()
    mail['From'] = fromaddr
    mail['To'] = toaddr
    mail['Subject'] = subject
    Body = body + "\nCurrent:" + current + "\nLimit:" + limit
    mail.attach(MIMEText(Body))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, pswd)
    server.sendmail(fromaddr, toaddr, mail.as_string())
    server.quit()


if __name__ == '__main__':
    try:
        XMLOpener = codecs.open("config.xml", encoding="UTF-8")
        data = XMLOpener.read()
        XMLOpener.close()

    except IOError:
        print("Cannot open file")
        quit()

    except FileNotFoundError:
        print("Check whether file exists or not")
        quit()

    except ConnectionError:
        print("Connection Error")
        quit()

    clients = xmltodict.parse(data)

    for client in clients:
        host = str(clients[client]["client"]["@ip"])
        port = int(clients[client]["client"]["@port"])
        uname = str(clients[client]["client"]["@username"])
        pswd = str(clients[client]["client"]["@password"])
        FinalOutput = sshconn(host, port, uname, pswd)
        time = str(datetime.now())

        if FinalOutput["MemoryDetail"]["Percent"] > clients[client]["client"]["alert"][0]["@limit"]:
            sender(uname, "Dear Client," + "\n" + "Memory Limit Exceeded", FinalOutput["MemoryDetail"]["Percent"],
                   clients[client]["client"]["alert"][0]["@limit"], "Urgent! Memory Usage limit exceeded")

        if FinalOutput["CPUDetail"]["Usage"] > clients[client]["client"]["alert"][1]["@limit"]:
            sender(uname, "Dear Client," + "\n" + "CPU Usage Limit Exceeded", FinalOutput["CPUDetail"]["Usage"],
                   clients[client]["client"]["alert"][1]["@limit"], "Urgent! CPU Usage limit exceeded")

        conn = sqlite3.connect('CSCSMaster.db')
        print("Successful connection with database")

        k = conn.execute("SELECT ID FROM system WHERE IP = '" + host + "';").fetchall()
        value = "'" + host + "', '" + FinalOutput["OS"] + "', '" + time + "'"
        if len(k) == 0:
            conn.execute("INSERT INTO system (IP, OS, EntryDate) VALUES (" + value + ");")

        for user in FinalOutput["User"]:
            value = "'" + FinalOutput["User"][user]["name"] + "', '" + FinalOutput["User"][user]["terminal"] + \
                    "', '" + FinalOutput["User"][user]["host"] + "', '" + FinalOutput["User"][user]["started"] + \
                    "', '" + time + "', (SELECT ID FROM system WHERE IP = '" + host + "')"

            conn.execute(("INSERT INTO user (NAME , TERMINAL, HOST, STARTED, EntryDate, IP) VALUES (" + value + ");"))

        if "Logs" in FinalOutput.iterkeys():
            value = "'" + FinalOutput["CPUDetail"]["BootTime"] + "', '" + FinalOutput["CPUDetail"]["Usage"] + "', '" + \
                    FinalOutput["CPUDetail"]["Count"] + "', '" + FinalOutput["CPUDetail"]["Interrupts"] + "', '" + \
                    FinalOutput["CPUDetail"]["SoftInterrupts"] + "', '" + FinalOutput["CPUDetail"]["SystemCalls"] + \
                    "', '" + FinalOutput["CPUDetail"]["MinFreq"] + "', '" + FinalOutput["CPUDetail"]["MaxFreq"] + \
                    "', '" + FinalOutput["CPUDetail"]["CurrFreq"] + "', '" + FinalOutput["Logs"] + "', '" + time + \
                    "', (SELECT ID FROM system WHERE IP = '" + host + "')"

            conn.execute("INSERT INTO CPUDetail (BootTime, Usage, Count, Interrupts, SoftInterrupts, SystemCalls, "
                         "MinFreq, MaxFreq, CurrFreq, Logs, EntryDate, IP) VALUES (" + value + ");")
        else:
            value = "'" + FinalOutput["CPUDetail"]["BootTime"] + "', '" + FinalOutput["CPUDetail"]["Usage"] + "', '" + \
                    FinalOutput["CPUDetail"]["Count"] + "', '" + FinalOutput["CPUDetail"]["Interrupts"] + "', '" + \
                    FinalOutput["CPUDetail"]["SoftInterrupts"] + "', '" + FinalOutput["CPUDetail"]["SystemCalls"] + \
                    "', '" + FinalOutput["CPUDetail"]["MinFreq"] + "', '" + FinalOutput["CPUDetail"]["MaxFreq"] + \
                    "', '" + FinalOutput["CPUDetail"]["CurrFreq"] + "', '" + time + \
                    "', (SELECT ID FROM system WHERE IP = '" + host + "')"

            conn.execute("INSERT INTO CPUDetail (BootTime, Usage, Count, Interrupts, SoftInterrupts, SystemCalls, "
                         "MinFreq, MaxFreq, CurrFreq, EntryDate, IP) VALUES (" + value + ");")

        for each in FinalOutput["DiskInfo"]:
            value = "'" + FinalOutput["DiskInfo"][each]["device"] + "', '" + \
                    FinalOutput["DiskInfo"][each]["mountpoint"] + "', '" + FinalOutput["DiskInfo"][each]["fstype"] + \
                    "', '" + FinalOutput["DiskInfo"][each]["opts"] + "', '" + time + \
                    "', (SELECT ID FROM system WHERE IP = '" + host + "')"
            conn.execute("INSERT INTO diskinfo (AgentName, MountPoint, FSType, OPTS, EntryDate, IP) VALUES (" +
                         value + ");")

        value = "'" + FinalOutput["DiskDetail"]["TotalDisk"] + "', '" + FinalOutput["DiskDetail"]["UsedDisk"] + \
                "', '" + FinalOutput["DiskDetail"]["FreeDisk"] + "', '" + FinalOutput["DiskDetail"]["Percent"] + \
                "', '" + time + "', (SELECT ID FROM system WHERE IP = '" + host + "')"
        conn.execute("INSERT INTO diskdetail (TotalDisk, UsedDisk, FreeDisk, Percent, EntryDate, IP) VALUES (" +
                     value + ");")

        value = "'" + FinalOutput["SwapDetail"]["Total"] + "', '" + FinalOutput["SwapDetail"]["Used"] + \
                "', '" + FinalOutput["SwapDetail"]["Free"] + "', '" + FinalOutput["SwapDetail"]["Percent"] + \
                "', '" + FinalOutput["SwapDetail"]["SIN"] + "', '" + FinalOutput["SwapDetail"]["SOUT"] + "', '" + \
                time + "', (SELECT ID FROM system WHERE IP = '" + host + "')"
        conn.execute("INSERT INTO swapdetail (Total, Used, Free, Percent, SIN, SOUT, EntryDate, IP) VALUES (" +
                     value + ");")

        value = "'" + FinalOutput["MemoryDetail"]["TotalMemory"] + "', '" + FinalOutput["MemoryDetail"]["AvailMemory"] + \
                "', '" + FinalOutput["MemoryDetail"]["Percent"] + "', '" + FinalOutput["MemoryDetail"]["UsedMemory"] + \
                "', '" + FinalOutput["MemoryDetail"]["FreeMemory"] + "', '" + \
                FinalOutput["MemoryDetail"]["CacheMemory"] + "', '" + FinalOutput["MemoryDetail"]["BufferMemory"] + \
                "', '" + FinalOutput["MemoryDetail"]["ActiveMemory"] + "', '" + FinalOutput["MemoryDetail"][
                    "InactiveMemory"] + \
                "', '" + FinalOutput["MemoryDetail"]["SharedMemory"] + "', '" + time + "', (SELECT ID FROM system " \
                                                                                       "WHERE IP = '" + host + "') "

        conn.execute("INSERT INTO memory (TotalMemory, AvailMemory, Percent, UsedMemory, FreMemory, CacheMemory, "
                     "BufferMemory, ActiveMemory, InactiveMemory, SharedMemory, EntryDate, ID) VALUES (" +
                     value + ");")

        conn.commit()
        print("Database updated with required entried")
        conn.close()
