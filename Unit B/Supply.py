# CS4102 Spring 2022 - Unit B Programming
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


class Supply:
    def __init__(self):
        return

    
    def checkValidInput(self, a, b):
        #can't pair rail hub and stores together
        if((a in self.rails) & (b in self.stores) | (b in self.rails) & (a in self.stores)):
            return 0
        #can't pair ports and stores together
        if((a in self.ports) & (b in self.stores) | (b in self.ports) & (a in self.stores)):
            return 0
        #can't pair distribution centers with other ones
        if((a in self.dists) & (b in self.dists)):
            return 0
        #can't pair distribution centers with stores that AREN'T IN THAT STORE'S LIST OF DEPENDENCIES
        if((a in self.dists) & (b in self.stores)):
            if(b not in self.distDependency[a]):
                return 0
        if((b in self.dists) & (a in self.stores)):
            #print(self.distDependency[a])
            if(a not in self.distDependency[b]):
                return 0

        return 1
    
    rails = []
    dists = []
    stores = []
    ports = []

    distDependency = {}
    nodes = {}
    vertices = set()

    #disjoint set method to find parent node
    def find(self, disjointsets, node):
        #if index == value then we have found the root parent node
        if(disjointsets[node] == node):
            return node
        #else lookup that node's parent in recursive call to find
        return self.find(disjointsets, disjointsets[node])

    #union to make i's parent point to j's parent
    def union(self, disjointsets, rank, i, j):
        i_parent = self.find(disjointsets, i)
        j_parent = self.find(disjointsets, j)
        #if i is larger then j in terms of rank, then make j's parent node point to i's parent node (optimization by rank from the slides)
        if(rank[i_parent] > rank[j_parent]):
            disjointsets[j_parent] = i_parent 
        else:
            disjointsets[i_parent] = j_parent
            if(rank[i_parent] == rank[j_parent]):
                rank[j_parent] += 1


    def kruskals(self, vertices):
        #sort nodes by value (increasing edge weight) - source: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        sortedNodes = {k: v for k, v in sorted(self.nodes.items(), key=lambda item: item[1])}
        #lists are easier to iterate on - just nodes and edges in graph
        edgeWeights = list(sortedNodes.values())
        nodesSorted = list(sortedNodes)
        
        #assign integer ids for each vertex (its index in this list of unique vertices)
        verts = list(vertices)
        #disjoint sets list
        disjointsets = []

        #my code was running too slow - so I tried implementing optimizations: union by rank and path compression to make it run faster
        #create list that holds the rank of each node
        rank = []
        #final list to add to
        finalMST = {}
        #keep track of how many edges in MST
        edgesAccepted = 0
        i = 0
        #initialize disjointssets with index of parent (itself for now)
        for vertex in range(len(vertices)):
            disjointsets.append(vertex)
            #initialize all the ranks as 0
            rank.append(0)

        # in this loop used some of the logic from: https://www.programiz.com/dsa/kruskal-algorithm
        while(edgesAccepted < (len(vertices)-1) ):
            first_parent = self.find(disjointsets, verts.index(nodesSorted[i][0]))
            second_parent = self.find(disjointsets, verts.index(nodesSorted[i][1]))
            #if not part of same tree then add, unioning first to second to combine them
            if(first_parent != second_parent):
                self.union(disjointsets, rank, first_parent, second_parent)
                finalMST[nodesSorted[i]] = edgeWeights[i]
                edgesAccepted +=  1
            i += 1
            #print(disjointsets)
        return finalMST




#         Port: Items that arrive at a port can be transported by rail to a rail hub, or by truck to a distribution
# center, but not directly to a store.

# Rail Hub: Items that arrive at a rail hub can be transported by rail to another rail hub, or by truck
# to a distribution center, but not directly to a store.


# Distribution Center: Each distribution center exists to get goods to a particular set of stores.
# Goods arrive by rail or truck from a port or rail hub, and then a truck leaves the distribution
# center and goes to one or more stores that it serves. Goods will never be transported from
# one distribution center to another.

# Store: Goods will arrive at a store from a distribution center or from another store. Each store
# can only be served by one distribution center.
    


    # This is the method that should set off the computation
    # of the supply chain problem.  It takes as input a list containing lines of input
    # as strings.  You should parse that input and then call a
    # subroutine that you write to compute the total edge-weight sum
    # and return that value from this method
    #
    # @return the total edge-weight sum of a tree that connects nodes as described
    # in the problem statement
    def compute(self, file_data):
        numNodes = 0
        numEdges = 0
        splitt = file_data[0].split(' ')
        numNodes = (int)(splitt[0])
        numEdges = (int)(splitt[1])

        distrib = 0
        storesUnderDistrib = []

        for i in range(1, numNodes+1):
            if(file_data[i].split() == []):
                continue
            splitted = file_data[i].split(' ')

            #if we come across another distribution center, we should add the list of dependent stores previously gathered
            #as long as this is not the first dist-center - then clear list of dependencies
            if(splitted[1] == 'dist-center'):
                if(distrib != 0):
                    self.distDependency[distrib] = storesUnderDistrib[:]
                    storesUnderDistrib.clear()

                distrib = splitted[0]
                self.dists.append(splitted[0])
            
            #when we come across a store, if it is preceded by a dist center (assumption in instructions), then add it to a list
            #the list will form the dependency for a given dist-center
            elif(splitted[1] == 'store'):
                self.stores.append(splitted[0])
                #add the name of the store
                if(distrib != 0):
                    storesUnderDistrib.append(splitted[0])

            
            elif(splitted[1] == 'port'):
                self.ports.append(splitted[0])
            
            elif(splitted[1] == 'rail-hub'):
                self.rails.append(splitted[0])

            #if last iteration, add the list to the distDependency
            if(i == numNodes):
                self.distDependency[distrib] = storesUnderDistrib[:]
                

        for j in range(numNodes+1, numEdges+numNodes+1):
            splitted2 = file_data[j].split(' ')
            #if the input is valid, then add it to our list of valid nodes
            if(self.checkValidInput(splitted2[0], splitted2[1])):
                self.nodes[(splitted2[0], splitted2[1])] = splitted2[2]
                #add to set of vertices (no duplicate vertices)
                self.vertices.add(splitted2[0])
                self.vertices.add(splitted2[1])

        print(self.vertices)
        
        #print(self.nodes)
        #print(self.vertices)
        #call kruskals algorithm
        MST = self.kruskals(self.vertices)

        #print(MST)

        #to find the edgeWeightSum, iterate through MST's values and sum them
        edgeWeightSum = 0
        for i in MST.values():
            edgeWeightSum += (int)(i)

        print(MST)

        # your function to compute the result should be called here

        return edgeWeightSum