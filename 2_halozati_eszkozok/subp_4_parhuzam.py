#!/usr/bin/env python3
from subprocess import PIPE, Popen
from time import sleep

cmd = ["timeout","5"] #windows
process = []
for i in range(4): #max active process
    p = Popen(cmd, stdout=PIPE, stderr=PIPE) #open process
    process.append(p)
ures = False
while (not ures):
    fut = 0
    i = 0 
    while(i < len(process)):
        if not process[i] is None:
            if process[i].poll() == None:
                fut += 1
            else:
                print(p.communicate())
                process[i] = None
        i += 1
    if (fut > 0):
        print("Meg futnak")
        sleep(1)
    else:
        ures = True
