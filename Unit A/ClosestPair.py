
# CS4102 Spring 2022 - Unit A Programming 
#################################
# Collaboration Policy: You are encouraged to collaborate with up to 3 other
# students, but all work submitted must be your own independently written
# solution. List the computing ids of all of your collaborators in the
# comments at the top of each submitted file. Do not share written notes,
# documents (including Google docs, Overleaf docs, discussion notes, PDFs), or
# code. Do not seek published or online solutions, including pseudocode, for
# this assignment. If you use any published or online resources (which may not
# include solutions) when completing this assignment, be sure to cite them. Do
# not submit a solution that you are unable to explain orally to a member of
# the course staff. Any solutions that share similar text/code will be
# considered in breach of this policy. Please refer to the syllabus for a
# complete description of the collaboration policy.
#################################
# Your Computing ID: mw3shc
# Collaborators: 
# Sources: Introduction to Algorithms, Cormen
#################################

from cProfile import run
import numpy
import math

class Points:
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    points = []
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def __eq__(self, other):
        #return true if points are same order and both equal or are out of order but still equal
        return ( ((self.x1 == other.x1) & (self.x2 == other.x2) & (self.y1 == other.y1) & (self.y2 == other.y2)) | ((self.x1 == other.x2) & (self.x2 == other.x1) & (self.y1 == other.y2) & (self.y2 == other.y1)) )
    
    def append(self, p):
        self.points.append(p)
        
    def check(self, x1,y1,x2,y2):
        if Points(x1,y1,x2,y2) in self.points:
            return True
        return False

    def remove(self, p):
        self.points.remove(p)


    def __str__(self, p):
        print(self.x1, self.x2, self.x3, self.x4)



class ClosestPair:

    def __init__(self):
        return

    #method to mathematically calculate distance between two given points
    def distance(x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2)


    def brute(sublist):
        min1 = float('inf')
        min2 = min1-1
        # p_inf = Points(float('-inf'),float('-inf'),float('inf'),float('inf'))
        # pmin1 = p_inf
        # pmin2 = p_inf
        for i in range(len(sublist)-1):
            j=i+1
            #compare to next element(s)
            while(j < len(sublist)):
                tempDist = ClosestPair.distance(sublist[i][0], sublist[i][1], sublist[j][0], sublist[j][1])
                #p = Points(sublist[i][0], sublist[i][1], sublist[j][0], sublist[j][1])
                # if(tempDist == 1.4142135623730951):
                #     print("tuple ", i, "and " , j, " ", (sublist[i][0], sublist[i][1]), (sublist[j][0], sublist[j][1]))
                if(tempDist < min1):
                    min2 = min1
                    min1 = tempDist
                    #swap points
                    # pmin2 = pmin1
                    # pmin1 = p
                elif(tempDist < min2):
                    min2 = tempDist
                    # pmin2 = p
                #increment j at end of each while loop iteration
                j+=1
            
        return min1, min2

    def get_runway(x, delta, delta2, median):
        runwayPoints = []
        left = median - delta2
        right = median + delta2
        for i in x:
            if left <= i[0] <= right:
                runwayPoints.append(i)
        return runwayPoints



    #recursive method to find the smallest, and second smallest, distance between two given points in a given sublist of points sorted by x value
    #DO this by implementing an algorithm based on the principles of QuickSort and its Partition, which runs in worst-case O(n*logn)
    def smallestDists(sublistX):
        #base case is if there is only THREE OR FEWER points in the sublist, then return their distance
        # **** if there is an odd number of points to begin with one of the sublists will end up withh one (1) point at some point, which makes it impossible to find distance of other points ****
        # therefore have TWO BASE CASES, one for a sublist with 2 points and one for a sublist with 3 points
        #print(sublistX)
        if(n <= 4):
            return ClosestPair.brute(sublistX)
        
        #find median for vertical line
        med = ((len(sublistX))//2)
        median = sublistX[med]

        #divide data further, recursively split into the left and right sublists (if point has the same x coord place in right sublist)
        leftX = sublistX[:med]
        rightX = sublistX[med:]


        lDist0, lDist1 = ClosestPair.smallestDists(leftX)
        rDist0, rDist1 = ClosestPair.smallestDists(rightX)

        deltaOne = lDist0
        deltaTwo = lDist1

        dis = [rDist0, rDist1]

        for i in dis:
            if i < deltaTwo:
                if i < deltaOne:
                    deltaTwo = deltaOne
                    deltaOne = i
                else:
                    deltaTwo = i

    
        runwayPoints = ClosestPair.get_runway(sublistX, deltaOne, deltaTwo, median[0])
        #sortted y
        runwayPoints = sorted(runwayPoints,key=lambda y: y[1])
        min1, min2 = ClosestPair.runway(runwayPoints, deltaOne, deltaTwo, median)
    
        return min1, min2


    #this function creates a runway around the median x value (vertical line) and tries to find points closer than min1 or min2 to update the mins that span the runway
    def runway(list, min1, min2, med):
        #print(runwayPoints)
        #sort by Y Coordinate of Runway Points - use lambda function as key to only sorted the second index (Y COORD) amd sort in reverse order
        #sortedByY = [y for y in runwayPoints if runwayPoints[(int)((len(runwayPoints)+1)/2)][0] - min1 <= y[0] <= runwayPoints[(int)((len(runwayPoints)+1)/2)][0] + min1]
        
        runwaypts = []
        cut = med[0]
        midy = med[1]

        if len(runwaypts) >= 2:
            runway_min = ClosestPair.distance(runwaypts[0], runwaypts[1])

            for i in range(len(runwaypts)):
                for j in range(i + 1, min(i + 8, len(runwaypts))):
                    dst = ClosestPair.distance(runwaypts[i], runwaypts[j]) 

                    if dst < runway_min:
                        runway_min = dst

                    ix = runwaypts[i][0]
                    iy = runwaypts[i][1]
                    jx = runwaypts[j][0]
                    jy = runwaypts[j][1]
                    #if a runway pair is on opp sides of the cut, we have not seen this pair before so check it.
                    if (ix < cut and jx >= cut) or (ix >= cut and jx < cut) or ((ix == cut and jx == cut) and ((iy < midy and jy >= midy) or (iy >= midy and jy < midy))):
                        self.checkmins(dst)

            return runway_min
            
        else:
            return closest_dist


    # This is the method that should set off the computation
    # of closest pair.  It takes as input a list containing lines of input
    # as strings.  You should parse that input and then call a
    # subroutine that you write to compute the closest pair distances
    # and return those values from this method
    #
    # @return the distances between the closest pair and second closest pair
    # with closest at position 0 and second at position 1 
    def compute(self, file_data):
        arr = []
        #initialize new array for holding x coordinates of points
        #initial run - parse input
        for i in file_data:
            splitted = i.split(' ')
            splitted[0] = (float) (splitted[0])
            splitted[1] = (float) (splitted[1])
            arr.append( (splitted[0],splitted[1]) )

        coord = numpy.array(arr)

        
        
        #sort by x coordinate, the sorted() algorithm has a worst case runtime of O(n*logn)
        #link: https://wiki.python.org/moin/TimeComplexity, under sort
        sortedListX = coord[coord[:,0].argsort()]
        sortedListY = coord[coord[:,1].argsort()]

        #print(ClosestPair.brute(sortedListX))
        #exit()


        #find the index of median of the sorted array ((n+1)/2) which must be an integer index
        median = sortedListX[(len(sortedListX))//2][0]
        #make median a line between this median and thhe next point:
        #medi2 = sortedListX[med+1][0]
        #median = (medi+medi2)/2

        print("med;",median)

        #call the smallestDist method to find the shortest distance between points in both sublists
        #this recursively finds smallest distance in left and right sublists
        delta, delta2 = ClosestPair.smallestDists(sortedListX)

        print(delta,delta2)
        #print(p1.x1, p1.x2, p1.y1,p1.y2)
        #print(p2.x1, p2.x2, p2.y1,p2.y2)


        #now that we know delta is the min, lets make a runway of size delta
        #but to do that we need to find all the points within delta

        runwayPoints = []

        y = sortedListY.tolist()


        # for i in range(len(y)):
        #     #this will be sorted by y value since the loop is iterating over the list sorted with respect to Y coord
        #     if abs(y[i][0] - median) <= delta2:
        #         runwayPoints.append(sortedListY[i])

        left = median - delta2
        right = median + delta2
        for i in sortedListX:
            if left <= i[0] <= right:
                runwayPoints.append(i)
        
        #print(runwayPoints)

        #run = numpy.where(abs(sortedListY.tolist()[:][0] - median) < delta2)
        #runwayPoints = sortedListY[run]
        runwayD1, runwayD2 = ClosestPair.runway(runwayPoints, delta, delta2, median)

        return [runwayD1, runwayD2]
