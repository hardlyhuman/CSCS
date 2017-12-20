###################################################
# CSCS/Source/client.py: Consists of the client script for the Client Statistics Collection System
# __author__ = "Sri Harsha"
# __copyright__ = "Copyright 2017, Sri Harsha"
# __Team__ = ["Sri Harsha"]
# __license__ = "GNU General Public License v3.0"
# __version__ = "0.6"
# __maintainer__ = "Sri Harsha"
# __email__ = "sriharsha.g15@iiits.in"
# __status__ = "Development"
####################################################



import os, sys, re, json
from Crypto.Cipher import AES
from time import time
import psutil
from Crypto import Random
import base64

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


if __name__ == '__main__':
    FinalResult = []
    DiskInfo = dict()
    users = dict()
    CPUDetail = dict()

    MemoryInfo = psutil.virtual_memory()
    SwapInfo = psutil.swap_memory()

    # print(MemoryInfo.total)

    for partition in psutil.disk_partitions():
        """
        Converts the named tuple of disk partion properties into a dictionary 
        and assigns to disk partitions dictionary with key as partition name
        """
        DiskInfo[partition[0]] = partition._asdict()

#    print(DiskInfo)

    try:
        DiskUsage = psutil.disk_usage('/')
        #  If not successful, C:// directory disk usage statistics are obtained
    except:
        DiskUsage = psutil.disk_usage('C:\\')

#    print(DiskUsage)

    for user in psutil.users():
        users[user[0]] = dict([(k, str(v)) for k, v in user._asdict().items()])


#    print(users)

    CPUDetail["BootTime"] = time() - psutil.boot_time()
    CPUDetail["Usage"] = psutil.cpu_percent()
    CPUDetail["Count"] = psutil.cpu_count()
    CPUDetail["Interrupts"] = psutil.cpu_stats().interrupts
    CPUDetail["SoftInterrupts"] = psutil.cpu_stats().soft_interrupts
    CPUDetail["SystemCalls"] = psutil.cpu_stats().syscalls
    CPUDetail["MinFreq"] = psutil.cpu_freq().min
    CPUDetail["MaxFreq"] = psutil.cpu_freq().max
    CPUDetail["CurrFreq"] = psutil.cpu_freq().current

#    print(CPUDetail)


