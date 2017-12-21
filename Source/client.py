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



import base64
import hashlib
import json
import os
import sys
from time import time

import psutil
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


if __name__ == '__main__':
    FinalResult = dict()
    DiskInfo = dict()
    users = dict()
    CPUDetail = dict()
    MemoryDetail = dict()
    SwapDetail = dict()
    DiskDetail = dict()

    MemoryInfo = psutil.virtual_memory()
    SwapInfo = psutil.swap_memory()

    MemoryDetail["TotalMemory"] = MemoryInfo.total
    MemoryDetail["AvailMemory"] = MemoryInfo.available
    MemoryDetail["Percent"] = MemoryInfo.percent
    MemoryDetail["UsedMemory"] = MemoryInfo.used
    MemoryDetail["FreeMemory"] = MemoryInfo.free
    MemoryDetail["CacheMemory"] = MemoryInfo.cached
    MemoryDetail["BufferMemory"] = MemoryInfo.buffers
    MemoryDetail["ActiveMemory"] = MemoryInfo.active
    MemoryDetail["InactiveMemory"] = MemoryInfo.inactive
    MemoryDetail["SharedMemory"] = MemoryInfo.shared

    # print(SwapInfo)

    SwapDetail["Total"] = SwapInfo.total
    SwapDetail["Used"] = SwapInfo.used
    SwapDetail["Free"] = SwapInfo.free
    SwapDetail["Percent"] = SwapInfo.percent
    SwapDetail["SIN"] = SwapInfo.sin
    SwapDetail["SOUT"] = SwapInfo.sout

    for partition in psutil.disk_partitions():
        """
        Converts the named tuple of disk partion properties into a dictionary 
        and assigns to disk partitions dictionary with key as partition name
        """
        DiskInfo[partition[0]] = partition._asdict()

    # print(DiskInfo)

    try:
        DiskUsage = psutil.disk_usage('/')
        #  If not successful, C:// directory disk usage statistics are obtained
    except:
        DiskUsage = psutil.disk_usage('C:\\')

    DiskDetail["TotalDisk"] = DiskUsage.total
    DiskDetail["UsedDisk"] = DiskUsage.used
    DiskDetail["FreeDisk"] = DiskUsage.free
    DiskDetail["Percent"] = DiskUsage.percent

    # print(DiskUsage)

    for user in psutil.users():
        users[user[0]] = dict([(k, str(v)) for k, v in user._asdict().items()])

    # print(users)

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

    FinalResult = dict(OS=sys.platform, MemoryDetail=MemoryDetail, SwapDetail=SwapDetail, DiskInfo=DiskInfo,
                       DiskDetail=DiskDetail, User=users, CPUDetail=CPUDetail)

    if os.name == 'nt':
        import win32evtlog

        host = 'localhost'
        type_of_log = 'Security'
        hand = win32evtlog.OpenEventLog(host, type_of_log)
        readbck = win32evtlog.EVENTLOG_BACKWARDS_READ
        readsqntl = win32evtlog.EVENTLOG_SEQUENTIAL_READ
        flags = readbck | readsqntl
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if events:
            formatedEvents = ''
            for event in events:
                formatedEvents += 'Event Category: ' + str(event.EventCategory)
                formatedEvents += '\nTime Generated: ' + str(event.TimeGenerated)
                formatedEvents += '\nSource Name: ' + event.SourceName
                formatedEvents += '\nEvent ID: ' + str(event.EventID)
                formatedEvents += '\nEvent Type:' + str(event.EventType) + '\n'
            # Adds Logs to the result dictionary
            FinalResult["Logs"] = str(formatedEvents)

    print(FinalResult)

    # Converts the result dictionary into a json string
    Result = json.dumps(FinalResult)

    #  print json_result

    #  Calls the encrypt function to encrypt the json string
    key = 'CrossOver Project'
    temp = AESCipher(key)

    message = temp.encrypt(Result)
    #print(message)
