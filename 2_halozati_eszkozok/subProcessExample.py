from subprocess import Popen, PIPE
import os
import platform
import queue
import sys
from time import sleep

print("CPU:", os.cpu_count())
print("OS:", platform.system())

availableCores = os.cpu_count()
maxLevel = int(sys.argv[1])

cmd = ''
if platform.system() == "Windows":
	cmd = 'echo "Windows"'
elif platform.system() == "Linux":
	cmd = 'echo "Linux"'
else:
	print("ERROR",platform.system())
	sys.exit(1)

processes = [None]*availableCores # None-nal feltott tomb
activeProcesses = 0
levelQueue = queue.Queue()
levelQueue.put(0)

def addProcess(level):
	global activeProcesses
	activeProcesses += 1
	p = Popen(cmd, stdout= PIPE, stderr=PIPE, shell=True)
	for i in range(availableCores):
		if  processes[i] == None:
			processes[i] = (level, p)
			break

def processRes(l, res):
	global activeProcesses
	activeProcesses -= 1
	if l < maxLevel:
		for i in range(l+1):
			levelQueue.put(l+1)
	print("  "*l,l,res.decode().strip())  #decode = bytes --> string
	
runs = 1
while (runs > 0 or not levelQueue.empty()):
	runs = 0
	if not levelQueue.empty() and activeProcesses < availableCores:
		level = levelQueue.get_nowait()
		addProcess(level)
	
	for i in range(len(processes)):
		tupl = processes[i]
		if not tupl is None:
			l, p = tupl
			if p.poll() != None:
				(res,err) = p.communicate()
				processRes(l,res)
				processes[i] = None
			else:
				runs += 1
	sleep(0.1)

#addProcess(0)