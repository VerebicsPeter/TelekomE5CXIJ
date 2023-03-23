from subprocess import Popen, PIPE
import os
import platform
import sys
from time import sleep

print("CPU:", os.cpu_count())
print("OS:", platform.system())

availableCore = os.cpu_count()

cmd = ''
if platform.system() == "Windows":
    cmd = 'echo "Windows"'
elif platform.system() == "Linux":
    cmd = 'echo "Linux"'
else:
    print("ERROR",platform.system())
    sys.exit(1)

process = []

for i in range(0,availableCore):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    process.append(p)

print('Futtattott processek szama:',len(process))

ures = False
while (not ures):
    fut = 0
    i   = 0
    while(i < len(process)):
        if not process[i] is None:
            if process[i].poll() == None: # ezzel ellenorizzuk hogy lefutott-e
                fut += 1
            else:
                res,err = p.communicate()
                print('Process ' + str(i+1) + ' : ' + res.decode().strip())
                process[i] = None
        i += 1
    if (fut > 0):
        sleep(1)
    else:
        print('Lefutott processek szama:', i)
        ures = True