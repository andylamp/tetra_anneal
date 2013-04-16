# Author: Andrew Grammenos
#
# Description:
#     A Simple, kind of heuristic Simulated Annealing based version of TetraVex game for
#     NxN matrices that almost never reaches a solution in a reasonable time due to the nature
#     of the algorithm used :)
#
# Date: 2/6/2012
# License: BSD License (if you don't know it, get me a beer)
# Contact: andreas.grammenos@gmail.com
#

# Libraries used, nothing special here...
import time
import random
import math

# Tile data type
# Holds {up,left,right,down} values 
# Used state T/F?

class Tile:    
    def __init__(self,  i):
        # tile_id
        self.id = i
        # tile edge values
        self.values = {'up':-1, 'left':-1,  'right':-1,  'down':-1} # asdf
        self.tScore = 0 # 4 is the max

class IterationInfo:
    def __init__(self, i):
        # iteration id
        self.id = i
        # iteration values
        self.boardGrade = 0
        self.proposedBoardGrade = 0
        self.randomizedSteps = 0
        self.temperatureNow = 0
	#self.currentCorrectBoardTiles = 0

# AdjustTemp
#
# This function is used to distribute the temperatures based on
# our maximum allowed steps and temperature value
def AdjustTemp(curTemp):
    return (curTemp-1)

# This prints the tiles in the game board.
def pt(tboard):

    # Info, print the range
    print("\nTable Range is: " + str(range(n)) + "\n")
    
    # traverse the rows...!
    for i in range(n):
            # print them!
            for j in range(0,n):
                print " --" + tboard[i*n+j].values["up"] + "-- " ,
            
            print("\n")
            for j in range(0,n):
                print " " + tboard[i*n+j].values["left"] + "---" + tboard[i*n+j].values["right"] + " ", 
            
            print("\n")
            for j in range(0,n):
                print " --" + tboard[i*n+j].values["down"] + "-- ", 
            print("\n\n")
          
    # end  
    return
            
# gradeBoard
#
# This function is used to grade a board state based on the grading system
# which was described in gradingTile function and returns its total grade
def gradeBoard(boardToGrade, silent):
    # loop it
    boardGrade = 0
    correctBoardTiles = 0
    tileGrade = 0

    print("Board Grading Taking place...\n")

    # grade the board
    for index in range(n*n):
        # print grade, it's useful
        tileGrade = gradeBoardTiles(index, boardToGrade[index], boardToGrade)
        if(silent == False):
            print(" --> Grade of current tile with index: " + str(index) + " is: " + str(tileGrade) + " (out of 4)")
        # check if this is a correct tile in the board
        if(tileGrade == 4):
            correctBoardTiles = correctBoardTiles + 1
            
        boardGrade = boardGrade + tileGrade
        
    #if(silent == False):
    print("\nBoard had " + str(correctBoardTiles) + " correct Tiles in it")    
    print("Board grade was: " + str(boardGrade) + "\n")
        

    return boardGrade        
            

# This function, prints the result to a given file using the same
# algorithm we used to print the tile-board
def writeToFile(filename):
    global debug
    global iterations
    for i in range(n*n):
        if board[i] == 'nill':
            print ('Invalid Board... please try again! bye!')
            return -1
            
    with open(filename, "w") as f:
        # write stats
        f.write("Tetravex solver v1\n")
        f.write("Andrew Grammenos (andreas.grammenos@gmail.com\n")
        f.write("Tetravex solver using Simulated Annealing did " + str(iterations) + 
		" iterations and lasted approximately: {0:.4f} ".format(et)+" seconds\n")
        if(debug == 'y' or debug == 'Y'):
            f.write("Debug info was enabled, slowdown due to input redirection is expected...\n")
        f.write("Solution is: \n\n")
        # write board
        for i in range(n):
            for j in range(n):
                f.write("--"+(board[i*n+j].values["up"])+"-- ") ,
            f.write('\n')
            for j in range(n):
                f.write(board[i*n+j].values["left"]+"---"+board[i*n+j].values["right"]+" "), 
            f.write('\n')
            for j in range(n):
                f.write("--"+board[i*n+j].values["down"]+"-- " ), 
            f.write('\n\n')
    return 1

# Grade Tiles 
#
# This function checks the tile score based on it's current state and the violations 
# it produces; the grading system is quite simple... for each tile in the board loop
# and grade based on how many edge restriction violations we have, max is 4 and the
# grading is zero if we have everything right then it's 4.
#
# This is then used as a total index in the state score where we use that for 'grading'
# a specific state and check if that is better from our current state; the acceptance
# rate is determined by our temperature in our current iteration.
def gradeBoardTiles(index,  tile, boardToGrade):
    # FIRST row
    # reset tile score
    tile.tScore = 0
    if (index < n):
        
        # up left corner for checking
        if(index == 0):
            # grant the +2 bonus
            #tile.tScore = 2
            if(boardToGrade[index+1].values['left'] == boardToGrade[index].values['right']):
                tile.tScore = tile.tScore + 1
            if(boardToGrade[index+n].values['up'] == boardToGrade[index].values['down']):
                tile.tScore = tile.tScore + 1
                
        # up right corner                                    
        if (index == n-1):                        
            # we can put +2 due to the fact that we don't have violations
            #tile.tScore = 2
            if(( tile.values['left'] == boardToGrade[index-1].values['right'])):
                tile.tScore = tile.tScore + 1
            # check it
            if(tile.values['down'] == boardToGrade[index+n].values['up']):
                tile.tScore = tile.tScore + 1
        else:
            # 1st Row tile, not corner
            
            # we can put +1 due to up
            #tile.tScore = tile.tScore + 1
            # now check for the other borders...right,left and down and 
            # change tScore accordingly
            if(tile.values['left'] == boardToGrade[index-1].values['right']):
                tile.tScore = tile.tScore + 1
            if(tile.values['down'] == boardToGrade[index+n].values['up']):
                tile.tScore = tile.tScore + 1 
            if(tile.values['right'] == boardToGrade[index+1].values['left']):
                tile.tScore = tile.tScore + 1
            
    # Last row
    elif (index >= (n-1)*n):
        # Left down corner
        if (index == (n-1)*n) :
            # we can put +2 due to down and right being correct
            tile.tScore = tile.tScore + 2
            # Now grade based on up and left position                  
            if(tile.values['up'] == boardToGrade[index-n].values['down']): 
                tile.tScore = tile.tScore + 1
            if(tile.values['right'] == boardToGrade[index+1].values['left']):
                tile.tScore = tile.tScore + 1
        # Right down corner
        elif (index == (n*n - 1)):                #down-right corner (last element to put?)
            # Similar analogy here... grade it based on it's correctness
            
            # grant +2 due to the fact that down and left are correct
            tile.tScore = tile.tScore + 2
            if (tile.values['left'] == boardToGrade[index-1].values['right']): 
                tile.tScore = tile.tScore + 1
            if(tile.values['up'] == boardToGrade[index-n].values['down']):
                tile.tScore = tile.tScore + 1
                
        # Last row random position    
        else:                            
            # grant one bonus for being down
            #tile.tScore = tile.tScore + 1                
            if(tile.values['up'] == boardToGrade[index-n].values['down']): 
                tile.tScore = tile.tScore + 1
            if(tile.values['right'] == boardToGrade[index+1].values['left']): 
                tile.tScore = tile.tScore + 1
            if(tile.values['left'] == boardToGrade[index-1].values['right']):
                tile.tScore = tile.tScore + 1
    elif (index % n == 0): 
        
        # FIRST column! (and not corners - check above if's)
        
        # grant the + 1 bonus for up
        #tile.tScore + tile.tScore + 1
        if(tile.values['up'] == boardToGrade[index-n].values['down']):             
            tile.tScore + tile.tScore + 1
        if(tile.values['right'] == boardToGrade[index+1].values['left']):
            tile.tScore + tile.tScore + 1 
        if(tile.values['down'] == boardToGrade[index+n].values['up'] ):
            tile.tScore + tile.tScore + 1
            
    elif (index % n == n-1):                     
        
        #LAST column! (and not corners - check above ifs)
        
        # grant the +1 bonus for down
        #tile.tScore + tile.tScore + 1
        if(tile.values['up'] == boardToGrade[index-n].values['down'] ):
            tile.tScore + tile.tScore + 1
        if(tile.values['left'] == boardToGrade[index-1].values['right']):
            tile.tScore + tile.tScore + 1
        if(tile.values['down'] == boardToGrade[index+n].values['up']):
            tile.tScore + tile.tScore + 1
    else:
        # Custom tile in the middle not boundary!                                                 
        if(tile.values['up'] == boardToGrade[index-n].values['down']):
            tile.tScore + tile.tScore + 1  
        if(tile.values['left'] == boardToGrade[index-1].values['right']):
            tile.tScore + tile.tScore + 1
        if(tile.values['down'] == boardToGrade[index+n].values['up'] ):
            tile.tScore + tile.tScore + 1
        if(tile.values['right'] == board[index+1].values['left']):
            tile.tScore + tile.tScore + 1
            
    return tile.tScore

# Simulated Annealing for Tetravex game.
def simulatedAnnealing(board, tboard, tMin, tCurrent, maxSteps, maxTries):
    
    # global variables
    global iterations
    global iterationArray
    
    iterationArray = []
    
    proposedStateGrade = 0
    correctBoardGrade = n*n*4
    
    stateEntropy = 0
    totalTries = 0
    iterations = 0
    # get our grade for this our board
    stateGrade = gradeBoard(board, True)
    curSteps = 0
    
    while tMin <= tCurrent and maxTries > totalTries and stateGrade < correctBoardGrade:
    
        # more info!
        print("Iteration number: " + str(iterations) + " with temperature: " + str(tCurrent) + 
              " and steps performed: " + str(curSteps) + " (out of " + str(maxSteps) + ")\n")
        
        # if max steps are reached for this temperature try
        # decreasing temperature by the amount we want
        if(curSteps >= maxSteps):
            tCurrent = AdjustTemp(tCurrent)
            curSteps = 0
    
        # initialize our backup board
        tboard = board
        proposedStateGrade = 0
        # randomize input based on current temperature and steps
        # take two random values between [0,n] different with each other
        # and switch them
       
        
        # info!
        
        # swap that many times based on n and current temperature
        # we ensure at least one swap occurs, and gradually decrease swaps based on temperature
        swaps = (tCurrent / ((n*n))) + 1
        swaps = int(swaps)
        
        print("Swaps to perform: " + str(swaps) + "\n")
        for i in range(swaps):
            # swap tiles, in our backup tile-board 
            random.seed(tCurrent*(0.9*i)) # this is important! We have to provide different seed!
            t1 = random.randint(0,(n*n)-1)
            random.seed(tCurrent*(0.9*i)/2) # this is important! We have to provide different seed!
            t2 = random.randint(0,(n*n)-1)
            tTile = tboard[t1]
            tboard[t1] = tboard[t2]
            tboard[t2] = tTile
            #print("t1 was: " + str(t1) + " t2 was: " + str(t2) + " swapping tiles with those indexes\n")
            #print("t3 was: " + str(t3) + " t4 was: " + str(t4) + " swapping tiles with those indexes\n")         
        
        
        
        #print("Grading new board\n")
        
        # grade the proposed solution
        proposedStateGrade = gradeBoard(tboard, True)
        
        # get the proposed state entropy
        stateEntropy = proposedStateGrade - stateGrade
        # get the prop
        entropyProb = math.exp(stateEntropy/(tCurrent+2))
        prob = random.random()
        
        print("Pro Prob: " + str(entropyProb) + " Prob Rand: " + str(prob) + " DT was: " + str(stateEntropy) + " temp is: " + str(tCurrent) +"\n")
        
        print("Grade of new board was: " + str(proposedStateGrade) + 
              " compared to the existing state: " + str(stateGrade) + " (out of " + str(correctBoardGrade) +")\n")
        
        # gg
        it = IterationInfo(iterations+1)
        it.boardGrade = stateGrade
        #it.correctBoardGrade = correctBoardGrade
        it.proposedBoardGrade = proposedStateGrade
        it.randomizedSteps = swaps
        it.temperatureNow = tCurrent
        
        # we got a good result! Nice!
        if(stateEntropy > 0):
            # swap boards since solution is better
            print(" --> Great, better state found; swapping boards!\n")
            board = tboard
            stateGrade = proposedStateGrade  
            
        elif(prob < entropyProb):
            # swap due to probability...
            print(" --> Great, better state was found; swapping swapping due to probability!\n")
            board = tboard
            stateGrade = proposedStateGrade
        else:
            print(" --> No Better state found\n")
            
        
        
        # increase our steps
        curSteps = curSteps + 1
        totalTries = totalTries + 1
        iterations = iterations + 1

        # append to iteration array
        iterationArray.append(it)

      
    print("Final board grade was: " + str(stateGrade) + " (out of " + str(correctBoardGrade) +")\n")       
    # more tries
    if(maxTries == totalTries):
        return 'more'
    # temporary reached
    elif(tMin >= tCurrent):
        return 'tReached'
    # correct board
    elif(stateGrade == correctBoardGrade):
        return 'correctBoard'
    # nothing found
    else:
        return 'qq'
    
# readFile
#
# This function gets as input a filename and reads it's contents based on the
# TetraVex input guidelines.
def readFile(filename):
    with open(filename, "r") as f:
        for j in range(n):
            #we read each line and then loop for every line in its words containing
            #one number each one. We need 3 lines for every tile (check input.txt)
            line = f.readline()
            words = line.split(' ')
            i=j*n
            for s in words:
                board[i].values['up'] = s[2]
                i = i+1
            #nextline
            line = f.readline()
            words = line.split(' ')
            i=j*n
            for s in words:
                board[i].values['left'] = s[0]
                board[i].values['right'] = s[4]
                i = i+1
            #nextline
            line = f.readline()
            words = line.split(' ')
            i = j*n
            for s in words:
                board[i].values['down'] = s[2]
                i = i+1
            f.readline()                                         #there is a blank line after each whole tile in input files
            
    return

# writeStats
#
# This function is used to write statistics in the file
def writeStats(filename):
    
    global iterationArray
    global iterations
    global n
    correctBoardGrade = n*n*4
    
    with open(filename, "w") as f:
        
        # introductory info
        f.write("# Used for GNU Plot to plot our data for the TetraVenx SA\n")
        f.write("# Generated using TetraVex Solver v1 by A. Grammenos\n")
        f.write("# iterationID \t boardGrade \t Proposed Grade \t correctBoardGrade \t Swaps \t temperature \n")
        
        # swap through the iteration vector and write to file
        for i in range(iterations):
            f.write(str(iterationArray[i].id) + "\t\t\t\t" + str(iterationArray[i].boardGrade) + "\t\t" +
                    str(iterationArray[i].proposedBoardGrade) + "\t\t" + str(correctBoardGrade) + "\t\t" +
                    str(iterationArray[i].randomizedSteps) + "\t\t" + str(iterationArray[i].temperatureNow) + "\n")
            
            
    
    return
   
# main function, gets parameters and calls dfs function in order to attempt to find a solution.
def main():
    # globals
    global n
    global correctBoardTiles
    global graphNodes
    # Board with current Solution and proposed
    global board
    global tboard
    # tiles
    global tiles
    
    global nMax
    # debug ?
    global debug
    global iterations
    # Annealing data
    correctBoardTiles = 0
    
    # used for stats...!
    global iterationArray
    n = 0
    global et
    board = []
    tboard = []
    #tiles = []
    
    n = int(input('Enter board size (NxN): '))
    tCurrent = int(input('Enter max temperature to begin: '))
    tMin = int(raw_input('Enter minimum temperature to end: '))
    maxSteps = int(raw_input('Enter max steps for each temperature iteration: '))
    maxTries = int(raw_input('Enter max global iterations (better be above >5k): '))
    
    # create our tile table
    for i in range(n*n):
        # append  as many object as NxN
        board.append ( Tile(i) )
        
    # get our cutoff limit
    #nMax = raw_input('DFS Cutoff: ')
    # file name for input
    filename = raw_input('Enter input file name:  ')
    
    #tiles = board
    
    # read data from input file
    readFile(filename)
    # print data, for viewing
    print 'Tiles read:' 
    pt(board)
    tboard = board
    gradeBoard(board, False)
    #debug = raw_input('Print execution debug info (y or n): ')
    debug = 'n'
    
    # time it
    st = time.time()
    # search
    r = simulatedAnnealing(board, tboard, tMin, tCurrent, maxSteps, maxTries)
    et = time.time() - st

    
    # print results!
    print "Search made "+str(iterations)+" iterations and lasted approximately: {0:.4f} ".format(et)+" seconds\n\n" 
    if(debug == 'y' or debug == 'Y'):
            print("Debug info was enabled, slowdown due to input redirection is expected...\n")
    # check our search result, we have 3 cases, one we need more search space 
    #(and consequently graph depth), the other is that we exhausted our search space
    # and found no solution and finally...the last outcome is that we found a solution!
    if r == 'tReached':
        print ("Minimum Temperature limit reached!\n")
    # need more!
    elif r == 'more':
        print ("SA Tries limit of: " + str(maxTries) + " reached; expansion needed to find a solution, if any!\n\n" )
    # Solution found!
    elif r == 'correctBoard':
        # write dat nice solution to file!
        print ("Solution found, output file: tetra_anneal.out\n")
    
    # check if the user wants to write to a file
    y = raw_input("Write proposed solution to a file (y/n): ")
    if(y == 'y' or y == 'Y'):          
        r = writeToFile("tetra_anneal.out")
        # ask the user if he wants to view that solution!
        if(r == -1):
            print("Something went wrong, could not print to file! Bye!")
            
    # write statistics for SA to be  used in GNU plot
    print("Writing execution statistics to file tetra_anneal_stats.out")
    writeStats("tetra_anneal_stats")
    
    # display proposed solution?
    y = raw_input("Display Solution? (y or n): ")
    if (y == 'y' or y =='Y'):
        pt(board)
    

if __name__ == '__main__':
        main()
