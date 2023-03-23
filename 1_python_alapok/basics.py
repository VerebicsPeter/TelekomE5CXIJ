################
# File Reading #
################

f = open("in.txt", "r")

print(f.read())

#print(f.readline())

#for x in f:
#   print(x)

f.close()

################
# File Writing #
################

f2 = open("out.txt", "w")
f2.write("I wrote this with python!!!")

#############
# Arguments #
#############

import sys

print(sys.argv[0])

##################
# Standard input #
##################

x = input("Read x from standard input! ")
print(x)

###########
# Classes #
###########

class Emberke:
    nev = ""
    kor = 0

    def __init__(self, _nev, _kor):
        self.nev = _nev
        self.kor = _kor

    def __str__(self):
        return self.nev+"("+str(self.kor)+")"

emberke = Emberke("Jani", 42)

print(emberke)
