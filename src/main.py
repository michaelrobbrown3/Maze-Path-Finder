from tkinter import Tk, Canvas
import random
from numpy import sqrt
from time import sleep
import sys

# Define parameters
side=20
rows = 35
cols = 50
screenHeight= side*rows
screenWidth = side*cols


#choose mode (1,2)
mode = 2

#mode 1: Start and end are in standard positions
if mode == 1:
    start_point=[0,0]
    end_point = [cols-1,rows-1]

#mode 2: Start and end are in random positions
else:
    randomX=random.randint(0,cols)
    randomY=random.randint(0,rows)
    start_point=[randomX,randomY]

    end_point=start_point
    while end_point == start_point:
        randomX=random.randint(0,cols)
        randomY=random.randint(0,rows)
        end_point = [randomX,randomY]

wallRatio=1/3
no_walls=int(wallRatio*rows*cols)




# Matrix of the state of (whats in) each square
boardDefinitionMatrix=[['free' for x in range(cols)] for x in range(rows)]
boardDefinitionMatrix[start_point[1]][start_point[0]]='start'
boardDefinitionMatrix[end_point[1]][end_point[0]]='end'

firstSpace=chr(33)

checkedSquares = []
frontierSquares= [firstSpace]

squareDistance = 1
paths = [firstSpace]

distanceDictionary={firstSpace:0}



RED_COLOR = "#EE4035"
BLUE_COLOR = "#0492CF"
Green_color = "#7BC043"
BLUE_COLOR_LIGHT = '#67B0CF'
RED_COLOR_LIGHT = '#EE7E77'
GREY_COLOUR = '#808A87'
BLACK_COLOUR = '#000000'




class Board:
# ------------------------------------------------------------------
# Initialization Functions:
# ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title("Route Finder")
        self.canvas = Canvas(self.window, width=screenWidth, height=screenHeight)
        self.canvas.pack()
        self.botPosition=start_point
        
        #ensures there is always a solution
        self.botRoute=[]
        while len(self.botRoute)<=1:
            #Clears any spaces are set to "blocked"
            for y in range (len( boardDefinitionMatrix)):
                for x in range (len( boardDefinitionMatrix[y])): 
                    if boardDefinitionMatrix[y][x] == "blocked":
                        self.remove_wall([x,y])
            #Initialises board
            self.initialize_board()
            #Searches for a solution
            self.search()

        self.loop=True


    def initialize_board(self):
        self.board = []
        self.wallDictionary = {}

        #print(self.wallDictionary)

    
        self.wallList = []
        for n in range(no_walls):
            randomY=start_point[1]
            randomX=start_point[0]
            coordinates=[]

            count=0
            found=True
            while boardDefinitionMatrix[randomY][randomX] != 'free' or coordinates in self.wallList:
                count+=1
                randomX=random.randint(0,cols-1)
                randomY=random.randint(0,rows-1)
                coordinates=[randomX,randomY]
                if count > rows*cols:
                    found=False
                    break
                else:
                    found=True
            if found:
                self.wallList.append(coordinates)
            

        for i in range(rows):
            for j in range(cols):
                self.board.append((i, j))
        #Create grid
        for i in range(rows):
            self.canvas.create_line( 0, i * screenHeight/ rows, screenWidth, i * screenHeight/rows )
        for i in range(cols):
            self.canvas.create_line( i * screenWidth/ cols, 0, i * screenWidth / cols, screenHeight )


        for wall in self.wallList:
            self.display_wall(wall)
        self.start_point()
        self.end_point()
        self.bot_footsteps(start_point)
        self.display_vehicle(start_point,RED_COLOR)

        self.search()

        self.window.update()





    def mainloop(self):


        self.exit=0
        while not self.exit:
            self.ready=0
            while not self.ready:
                self.window.bind('<Button-1>', self.click)
                
                #Update the window
                self.window.update()


            self.ready=0
            while not self.ready:

                #Run search algorithm to find the shortest route
                game_instance.search()

                #Initialise variables
                self.ghostRoute=[]


                if len(self.botRoute)>1:
                    #Set square as the next square the 'bot' will move to on path
                    square=self.botRoute[1]

                    #Creates an array of the 'ghost' positions
                    for n in range(1,len(self.botRoute)):
                        self.ghosts(self.spacesDictionary[self.botRoute[n]])

                    #Deletes old 'bot' display
                    self.canvas.delete(self.bot)
                    #Displays 'footsteps' and new 'bot' position
                    self.bot_footsteps(self.spacesDictionary[square])
                    self.display_vehicle(self.spacesDictionary[square],RED_COLOR)

                    #Updates 'bot's' position
                    self.botPosition=self.spacesDictionary[square]

                    #Update the window 
                    self.window.update()

                #If there isnt a path, display 'bot' as black
                else:
                    self.canvas.delete(self.bot)
                    self.display_vehicle(self.botPosition,BLACK_COLOUR)


                self.window.bind('<Button-1>', self.click)
                self.window.update()
                sleep(0.1)


                #Deletes ghost display
                for ghost in self.ghostRoute:
                        self.canvas.delete(ghost)


                #If 'bot' is at the end, exit
                if boardDefinitionMatrix[self.botPosition[1]][self.botPosition[0]] == 'end':
                    #print("It has got to the end!")
                    sys.exit(0)




# ------------------------------------------------------------------
# Drawing Functions:
# The modules required to draw required game based object on canvas
# ------------------------------------------------------------------
    def display_wall(self,coordinates):
        boardDefinitionMatrix[coordinates[1]][coordinates[0]]='blocked'

        x1 = side*coordinates[0]+2
        y1 = side*coordinates[1]+2
        x2 = side*(coordinates[0]+1)-2
        y2 = side*(coordinates[1]+1)-2

        wall = self.canvas.create_rectangle( x1, y1, x2, y2, fill=BLUE_COLOR, outline=BLUE_COLOR )

        key=str(coordinates[0])+","+str(coordinates[1])
        self.wallDictionary[key]=wall


    def remove_wall(self,coordinates):
        boardDefinitionMatrix[coordinates[1]][coordinates[0]]='free'

        key=str(coordinates[0])+","+str(coordinates[1])
        wall = self.wallDictionary[key]
        self.canvas.delete(wall)
        self.wallDictionary.pop(key)


    def start_point(self):
        x1 = side*start_point[0]+1
        y1 = side*start_point[1]+1
        x2 = side*(start_point[0]+1)-1
        y2 = side*(start_point[1]+1)-1
        self.start = self.canvas.create_rectangle( x1, y1, x2, y2, fill=Green_color, outline=Green_color )


    def end_point(self):
        x1 = side*end_point[0]+1
        y1 = side*end_point[1]+1
        x2 = side*(end_point[0]+1)-1
        y2 = side*(end_point[1]+1)-1
        self.end = self.canvas.create_rectangle( x1, y1, x2, y2, fill=RED_COLOR_LIGHT, outline=RED_COLOR_LIGHT )


    def display_vehicle(self,bot_Position,colour):
        x1 = side*bot_Position[0]+5
        y1 = side*bot_Position[1]+5
        x2 = side*(bot_Position[0]+1)-5
        y2 = side*(bot_Position[1]+1)-5
        self.bot = self.canvas.create_oval( x1, y1, x2, y2, fill=colour, outline=colour )


    def bot_footsteps(self,point):
        size=side*2/5
        x1 = side*point[0]+size
        y1 = side*point[1]+size
        x2 = side*(point[0]+1)-size
        y2 = side*(point[1]+1)-size
        self.path = self.canvas.create_oval( x1, y1, x2, y2, fill=RED_COLOR, outline=RED_COLOR )


    def ghosts(self,point):
        size=side*2/5
        x1 = side*point[0]+size
        y1 = side*point[1]+size
        x2 = side*(point[0]+1)-size
        y2 = side*(point[1]+1)-size
        ghost = self.canvas.create_oval( x1, y1, x2, y2, fill=GREY_COLOUR, outline=GREY_COLOUR )
        self.ghostRoute.append(ghost)


# ------------------------------------------------------------------
# Logical Functions:
# The modules required to carry out game logic
# ------------------------------------------------------------------
    def click(self, event):

        grid_position = [int(event.x/side), int(event.y/side)]
        botPosition=self.spacesDictionary[self.botRoute[0]]
    

        if boardDefinitionMatrix[grid_position[1]][grid_position[0]] == "free" and grid_position != botPosition :
            self.display_wall(grid_position)
        elif boardDefinitionMatrix[grid_position[1]][grid_position[0]] == "blocked":
            self.remove_wall(grid_position)
        elif boardDefinitionMatrix[grid_position[1]][grid_position[0]] == "start":
            self.ready=1
        elif boardDefinitionMatrix[grid_position[1]][grid_position[0]] == "end":
            self.ready=1
            self.exit=1






    def search(self):
        latestSpace=firstSpace
        frontierSquares= [firstSpace]
        paths = [firstSpace]
        self.spacesDictionary={firstSpace:self.botPosition}
        distanceDictionary={firstSpace:0}


        count=0
        currentPath=firstSpace
        while count <= rows*cols:
            count+=1

            #Find shortest path so far
            shortestPathLength=rows*cols
            newScoutPosition = self.botPosition
            for square in frontierSquares:
                if distanceDictionary[square] < shortestPathLength:
                    shortestPath = square
                    shortestPathLength = distanceDictionary[square]
                    newScoutPosition = self.spacesDictionary[square]
            scoutPosition = newScoutPosition


            #find its path history
            for path in paths:
                if shortestPath == path[-1]:
                    currentPath=path
                    previousSquare=path[-1]
            currentDistance = distanceDictionary.get(previousSquare)


            #If end square is found exit
            if boardDefinitionMatrix[scoutPosition[1]][scoutPosition[0]] == 'end':
                break

            elif len(frontierSquares) == 0:
                currentPath=firstSpace
                break


            #Finds potential new squares the bot could move to
            movablePositions=[[scoutPosition[0]+1,scoutPosition[1]], [scoutPosition[0]-1,scoutPosition[1]],
                        [scoutPosition[0],scoutPosition[1]+1], [scoutPosition[0],scoutPosition[1]-1]]

            for potentialSquare in movablePositions:
                if 0<=potentialSquare[1]<rows and 0<=potentialSquare[0]<cols:
                    dictionaryValues=self.spacesDictionary.values()
                    
                    if ( boardDefinitionMatrix[potentialSquare[1]][potentialSquare[0]]  == 'free' or  boardDefinitionMatrix[potentialSquare[1]][potentialSquare[0]]  == 'end' or  boardDefinitionMatrix[potentialSquare[1]][potentialSquare[0]]  == 'start')  and potentialSquare not in dictionaryValues:

                        distanceWeighting=sqrt((end_point[0]-potentialSquare[0])**2+(end_point[1]-potentialSquare[1])**2)/5
                        latestSpace=chr(ord(latestSpace)+1)
                        paths.append(currentPath+latestSpace)
                        frontierSquares.append(latestSpace)
                        distanceDictionary[latestSpace]=currentDistance+squareDistance+distanceWeighting
                        self.spacesDictionary[latestSpace]=potentialSquare
            distanceDictionary.pop(previousSquare)
            frontierSquares.remove(previousSquare)
            paths.remove(currentPath)


        self.botRoute = currentPath




    def key_input(self, event):
        key_pressed = event.keysym
        # Check if the pressed key is a valid key
        if key_pressed.lower() == "q":
            self.loop = False
        else:
            self.loop = True


# ------------------------------------------------------------------
game_instance = Board()
game_instance.mainloop()

