import sys
import time
from ClosestPair import ClosestPair

fp = open("80k vertical.txt", 'r')
lines = fp.readlines()
points = []
for line in lines:
    points.append(line.strip())


# Call the closest_pair function passing in the
# contents of the file
start = time.time()
cp = ClosestPair()
print(cp.compute(points))
end = time.time()
print("time: "+ str(end-start))
