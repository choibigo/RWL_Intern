import sys

sum = 0
args = sys.argv[1:]
for i in args:
    sum = sum + int(i)

print(sum)