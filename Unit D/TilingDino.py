# CS4102 Spring 2022 -- Unit D Programming
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
import networkx as nx

class TilingDino:
    def __init__(self):
        return

    # This is the method that should set off the computation
    # of tiling dino.  It takes as input a list lines of input
    # as strings.  You should parse that input, find a tiling,
    # and return a list of strings representing the tiling
    #
    # @return the list of strings representing the tiling
    def compute(self, lines):
        rows = len(lines)
        cols = len(lines[0])

        #create digraph with source and target nodes
        g = nx.DiGraph()
        g.add_node('s')
        g.add_node('t')

        #first scan to create graph nodes
        for y in range(rows):
            for x in range(cols):
                #we need some way of differentiating tiles to its adjacent one for bipartite matching like shown in lecture
                #most intuitive example given to me from TAs is checkerboard
                #where black squares are the squares that have the same type of number index (odd or even)
                #and the red squares are the squares with a different ordered index (odd and even only)
                if lines[y][x] == "#":
                    #we can do this using mod - these should be black squares (connected to start)
                    if (y % 2) == (x % 2):
                        g.add_node('s row ' + str(y) + ' col ' + str(x) )
                        g.add_edge('s', 's row ' + str(y) + ' col ' + str(x), c=1) #note - we need to specify capacity
                    else:
                        #these should be red squares (connected to target)
                        #these go directly to the target node so mark them as special so they are not counted in the maximum_flow 
                        g.add_node('t row ' + str(y) + ' col ' + str(x) )
                        g.add_edge('t row ' + str(y) + ' col ' + str(x), 't', c=1)    

        print("list length before tile fitting ", len(list(g)))
        #if the length of the graph in terms of nodes is not divisible by 2 then this is not possible to tile
        if( (len(list(g)) % 2) == 1):
            return ["impossible"]
        
        #prevent index out of bounds
        #scan through and look for all possible tile fits (adjacent tiles but not on diagonal)
        for y in range(rows-1):
            for x in range(cols-1):
                if lines[y][x] == "#":
                    #if current cell is a # see if adjacent cells - first check adjacen row
                    if lines[y+1][x] == '#':

                        if ( (y+1) % 2) == (x % 2): #adjacent tile is black so original was a red tile - so add edge from adj -> cur
                            g.add_edge('s row ' + str(y+1) + ' col ' + str(x), 't row ' + str(y) + ' col ' + str(x), c=1)
                        else: #otherwise edge is from cur -> adj
                            g.add_edge('s row ' + str(y) + ' col ' + str(x), 't row ' + str(y+1) + ' col ' + str(x), c=1)

                    #also check adjacent col
                    if lines[y][x+1] == '#':
                        if (y % 2) == ( (x+1) % 2): #adjacent tile is black so original was a red tile - so add edge from adj -> cur
                            g.add_edge('s row ' + str(y) + ' col ' + str(x+1), 't row ' + str(y) + ' col ' + str(x), c=1)
                        else: #otherwise edge is from cur -> adj
                            g.add_edge('s row ' + str(y) + ' col ' + str(x), 't row ' + str(y) + ' col ' + str(x+1), c=1)

        #check for corner cases (last row)
        for x in range(cols-1):
            if lines[rows-1][x] == "#":
                #if current cell is a # see if adjacent cells - first check adjacen row
                if lines[rows-1][x+1] == '#':
                    if ((rows-1) % 2) == ( (x+1) % 2): #adjacent tile is black so original was a red tile - so add edge from adj -> cur
                        g.add_edge('s row ' + str(rows-1) + ' col ' + str(x+1), 't row ' + str(rows-1) + ' col ' + str(x), c=1)
                    else: #otherwise edge is from cur -> adj
                        g.add_edge('s row ' + str(rows-1) + ' col ' + str(x), 't row ' + str(rows-1) + ' col ' + str(x+1), c=1)
        
        #other corner case (last column)
        for y in range(rows-1):
            if lines[y][cols-1] == "#":
                if lines[y+1][cols-1] == "#":
                    if ( (y+1) % 2) == ( (cols-1) % 2): #adjacent tile is black so original was a red tile - so add edge from adj -> cur
                        g.add_edge('s row ' + str(y+1) + ' col ' + str(cols-1), 't row ' + str(y) + ' col ' + str(cols-1), c=1)
                    else: #otherwise edge is from cur -> adj
                        g.add_edge('s row ' + str(y) + ' col ' + str(cols-1), 't row ' + str(y+1) + ' col ' + str(cols-1), c=1)

        outputList = set()
        #from doc the first index is the integer of maximum flow and the second index is the list
        maxFlow = nx.maximum_flow(g, 's', 't', capacity='c')
        #make sure that the value for maximum flow is the same as the number of edges = eligible nodes / 2 for bipartite matching
        if(maxFlow[0] != (len(list(g))-2)/2):
            return ["impossible"]

        print(maxFlow)
        MaxFlowList = maxFlow[1]
        #MaxFlowList = list(MaxFlowList)
        print("the max flow", MaxFlowList)
        # print("len is ", len(MaxFlowList))
        # print("first ", MaxFlowList[0])
        # print("sec ", MaxFlowList[1])
        #FlowSet = set()

        #MaxFlowList is a dict
        for entry in MaxFlowList:
            #print("ENRY ", entry)
            for val in MaxFlowList[entry]:
                #get rid of duplicate/useless entries - only include the paths in the max_flow
                if(val != "t" and entry != "s" and MaxFlowList[entry][val] == 1):
                    #print("Entry ", entry, " val ", val, " VALUE ", MaxFlowList[entry][val])
                    #print("ENTRY ", val, " ", entry, " ", val[0])
                    #we need to split the lines to see what where the edge is coming from - but 
                    parent, row, rowNum, col, colNum = entry.split(" ")
                    parent2, row2, rowNum2, col2, colNum2 = val.split(" ")
                    outputList.add(colNum + " " + rowNum + " " + colNum2 + " " + rowNum2)

        return list(outputList)
