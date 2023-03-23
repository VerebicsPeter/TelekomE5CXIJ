import sys
import subprocess

p = subprocess.Popen(["echo", "hello world"], shell = True, stdout=subprocess.PIPE)
print(p.communicate())

print('\n')