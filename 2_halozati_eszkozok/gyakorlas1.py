from subprocess import Popen, PIPE
from time import sleep
import os
import sys
import platform

available_cores = os.cpu_count()
os_name = platform.system()

print("OS: ", os_name)
print("number of cores: ", available_cores)

cmd = ''

if os_name == "Windows": cmd = 'echo Windows'
elif os_name == "Linux": cmd = 'echo Linux'
else :
  print("ERROR: ", os_name)
  sys.exit(1)

processes = []

for i in range(0,available_cores):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    processes.append(p)

print('Number of processes running: ', len(processes))

empty = False
while (not empty) :
  runs = 0; i = 0
  while (i < len(processes)) :
    if not processes[i] is None :
      if processes[i].poll() == None :
        runs += 1
      else :
        res, err = p.communicate()
        print('Process' + str(i+1) + ' : ' + res.decode().strip())
        processes[i] = None
    i += 1
  if (runs > 1) : sleep(1)
  else : 
    print('Ran' + i + ' processes.')
    empty = True
