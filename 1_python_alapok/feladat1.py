def isLeapYear (year):
    if year % 100 == 0 :
        return year % 400 == 0
    else: return year % 4 == 0

with open("years.txt", "r") as f :
    for x in f:
        x = x.rstrip()
        if isLeapYear(int(x)) : print(x + " is a leap year.")
        else                  : print(x + " is not a leap year.")

"""
f = open("years.txt", "r")

for x in f:
    x = x.rstrip()
    if isLeapYear(int(x)) : print(x + " is a leap year.")
    else                  : print(x + " is not a leap year.")

f.close()
"""