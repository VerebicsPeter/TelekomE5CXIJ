from subprocess import Popen, PIPE
from time import sleep
import json

to_ping = ['elte.hu', 'berkeley.edu', 'google.com']

processes = []

for url in to_ping :
    p = Popen("ping " + url, stdout=PIPE, stderr=PIPE)
    processes.append(p)

print('Number of processes started:',len(processes))

processes_dictionary = []

empty = False
while (not empty):
    runs = 0
    i    = 0
    while(i < len(processes)):
        if not processes[i] is None:
            if processes[i].poll() == None: # if the process is running
                runs += 1
            else:                           # if the process ran
                res,err = p.communicate()
                
                x = {
                    'process' : 'ping ' + to_ping[i],
                    'result'  : res.decode().strip()
                    }
                processes_dictionary.append(x)
                
                processes[i] = None
        i += 1
    if (runs > 0):
        sleep(1)
    else:
        print('Processes finished: ', i)
        empty = True

json_result = json.dumps(processes_dictionary, indent=2)

# Writing to processes.json
with open("processes.json", "w") as outfile: outfile.write(json_result)