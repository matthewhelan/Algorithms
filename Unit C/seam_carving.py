# CS4102 Spring 2022 -- Unit C Programming
#################################
# Collaboration Policy: You are encouraged to collaborate with up to 3 other
# students, but all work submitted must be your own independently written
# solution. List the computing ids of all of your collaborators in the comment
# at the top of your java or python file. Do not seek published or online
# solutions for any assignments. If you use any published or online resources
# (which may not include solutions) when completing this assignment, be sure to
# cite them. Do not submit a solution that you are unable to explain orally to a
# member of the course staff.
#################################
# Your Computing ID: mw3shc
# Collaborators: 
# Sources: Introduction to Algorithms, Cormen
#################################
from cmath import sqrt
import numpy as np


class SeamCarving:
    def __init__(self):
        return

    def diff(self, i, j):
        if(i[0] == j[0] and i[1] == j[1] and i[2] == j[2]):
            return 0
        #print(sqrt( (j[0]-i[0])**2+(j[1]-i[1])**2+(j[2]-i[2])**2 ))
        return sqrt( (j[0]-i[0])**2+(j[1]-i[1])**2+(j[2]-i[2])**2 ).real

    #method that will find the energy for each cell - preload our energy matrix 
    def populateEnergies(self):
        image = self.imageObj
        #initialize energy matrix
        self.ee = np.array(np.zeros((self.imageRows, self.imageCols)))

        for y in range(self.imageRows):
            for x in range(self.imageCols):
                countDiff = 0
                #check edge cases
                if(y == 0):
                    #edge case
                    if(x==0):
                        for p in range(y, y+2):
                            for k in range(x, x+2):
                                countDiff += self.diff(image[p][k],image[y][x])
                        self.ee[y][x] = (1/3)*countDiff
                        continue
                    #edge case
                    elif(x == self.imageCols-1):
                        for p in range(y, y+2):
                            for k in range(x-1, x+1):
                                countDiff += self.diff(image[p][k],image[y][x])
                        self.ee[y][x] = (1/3)*countDiff
                        continue
                    
                    #dont check the row before (top row so will throw out of bounds)
                    for p in range(y, y+2):
                        for k in range(x-1, x+2):
                            countDiff += self.diff(image[p][k],image[y][x])
                    self.ee[y][x] = (1/5)*countDiff

                #if y is bottom row
                elif(y == self.imageRows-1):
                    #edge case
                    if(x==0):
                        for p in range(y-1, y+1):
                            for k in range(x, x+2):
                                countDiff += self.diff(image[p][k],image[y][x])
                        self.ee[y][x] = (1/3)*countDiff
                        continue
                    #edge case
                    elif(x == self.imageCols-1):
                        for p in range(y-1, y+1):
                            for k in range(x-1, x+1):
                                countDiff += self.diff(image[p][k],image[y][x])
                        self.ee[y][x] = (1/3)*countDiff
                        continue
                    
                    #dont check the row after (bottom row so will throw out of bounds)
                    for p in range(y-1, y+1):
                        for k in range(x-1, x+2):
                            countDiff += self.diff(image[p][k],image[y][x])
                    self.ee[y][x] = (1/5)*countDiff

                else:
                    #edge case
                    if(x==0):
                        for p in range(y-1, y+2):
                            for k in range(x, x+2):
                                countDiff += self.diff(image[p][k],image[y][x])
                        self.ee[y][x] = (1/5)*countDiff
                        continue
                    #edge case
                    elif(x == self.imageCols-1):
                        for p in range(y-1, y+2):
                            for k in range(x-1, x+1):
                                countDiff += self.diff(image[p][k],image[y][x])
                        self.ee[y][x] = (1/5)*countDiff
                        continue

                    for p in range(y-1, y+2):
                        for k in range(x-1, x+2):
                            countDiff += self.diff(image[p][k],image[y][x])
                    self.ee[y][x] = (1/8)*countDiff


    #change from recursive structure to iterative solution
    ee = np.array([])

    indexOfSmallestXSeam = 0

    imageRows = 0
    imageCols = 0

    imageObj = []

    seamsList = []


    # This method is the one you should implement.  It will be called to perform
    # the seam carving.  You may create any additional data structures as fields
    # in this class or write any additional methods you need.
    # 
    # @return the seam's weight
    def run(self , image):
        self.imageObj = image
        self.imageRows = len(image)
        self.imageCols = len(image[0])
        #fill in energy values
        self.populateEnergies()
        e = self.ee
    
        #np array to store all the SEAMS - initialize them to the energy value at the bottom of the image
        seamsList = np.array(np.empty((self.imageRows, self.imageCols)))

        #populate bottom rows values for seams
        for i in range(self.imageCols):
            seamsList[self.imageRows-1][i] = e[self.imageRows-1][i]
              
        #start at the BOTTOM of the image - run through all y in n time (amount of rows = colLength)
        for y in range(self.imageRows-2, -1, -1):
            #print(seamsList[y+1], "at ", y+1, "\n")
            #runs through all x in m time (amount  of columns = rowLength)
            for x in range(self.imageCols):
                xx = x

                #edge cases
                if(xx == 0): 
                    #if theres a lower adjacent value then change to that x
                    if(seamsList[y+1][xx+1] < seamsList[y+1][xx]):
                        xx += 1

                elif(xx == self.imageCols-1):

                    #if theres a lower adjacent value then change to that x
                    if(seamsList[y+1][xx-1] < seamsList[y+1][xx]):
                        xx -= 1

                #if normal then look at three lower x coords
                else:
                    #if the minimum is the x+1 then add one to x
                    if(min(seamsList[y+1][xx-1], seamsList[y+1][xx], seamsList[y+1][xx+1]) == seamsList[y+1][xx]):
                        pass
                    elif(min(seamsList[y+1][xx-1], seamsList[y+1][xx], seamsList[y+1][xx+1]) == seamsList[y+1][xx+1]):
                        xx += 1
                    elif(min(seamsList[y+1][xx-1], seamsList[y+1][xx], seamsList[y+1][xx+1]) == seamsList[y+1][xx-1]):
                        xx -= 1  
                
                #for a given seamsList, choose the seam with the lowest weight (our xx coord) and add it to the energy at that cell
                seamsList[y][x] = seamsList[y+1][xx] + e[y][x]
                        
        print(seamsList[0], "at ", 0, "\n")

        #logic found: https://stackoverflow.com/questions/2474015/getting-the-index-of-the-returned-max-or-min-item-using-max-min-on-a-list
        #makes searching for index of minimum of values much faster/easier 

        #find the MIN of the seam energy values - based on starting (x=bottom seam starts)
        self.indexOfSmallestXSeam = np.argmin(seamsList[0])
        #self.seamcoord = seamsCoords
        self.seamsList = seamsList

        #print(energyList)
        return seamsList[0][self.indexOfSmallestXSeam]
                    

    seamcoord = []


    # Get the seam, in order from top to bottom, where the top-left corner of the
    # image is denoted (0,0).
    # 
    # Since the y-coordinate (row) is determined by the order, only return the x-coordinate
    # 
    # @return the ordered list of x-coordinates (column number) of each pixel in the seam
    #         as an array
    def getSeam(self):

        #print from the top to the bottom
        xx = self.indexOfSmallestXSeam
        #print(xx)

        seamsList = self.seamsList
        
        #store xPath 
        xPath = []
      
        #start at the top of the image - run through all y in n time (amount of rows = colLength)
        for y in range(1,self.imageRows+1):
            #edge cases
                if(xx == 0): 
                    #if theres a lower adjacent value then change to that x
                    if(seamsList[y-1][xx+1] < seamsList[y-1][xx]):
                        xx += 1

                elif(xx == self.imageCols-1):

                    #if theres a lower adjacent value then change to that x
                    if(seamsList[y-1][xx-1] < seamsList[y-1][xx]):
                        xx -= 1

                #if normal then look at three lower x coords
                else:
                    #if the minimum is the x+1 then add one to x
                    if(min(seamsList[y-1][xx-1], seamsList[y-1][xx], seamsList[y-1][xx+1]) == seamsList[y-1][xx]):
                        pass
                    elif(min(seamsList[y-1][xx-1], seamsList[y-1][xx], seamsList[y-1][xx+1]) == seamsList[y-1][xx+1]):
                        xx += 1
                    elif(min(seamsList[y-1][xx-1], seamsList[y-1][xx], seamsList[y-1][xx+1]) == seamsList[y-1][xx-1]):
                        xx -= 1  

                xPath.append(xx)
  
        return xPath

   