import sys
import time
from Supply import Supply

fp = open("test1.txt", 'r')
lines = fp.readlines()
inputLines = []
for line in lines:
    inputLines.append(line.strip())


# Call the compute() function in your class, passing in the
# contents of the file
start = time.time()
supply = Supply()
print(supply.compute(inputLines))
end = time.time()
print("time: "+ str(end-start))
