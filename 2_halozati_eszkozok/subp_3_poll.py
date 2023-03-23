from subprocess import PIPE, Popen
import time

p1 = Popen(["ping", '-n', '5', 'berkeley.edu'], stdout=PIPE)
while p1.poll()==None:
    print(" még fut ")
    time.sleep(1)
print(p1.communicate())

print('\n')