import random
import math
import keyboard
import time
import os


#**all comments reference the line of code below them**, after this comment, any comment with **___** around it indicated a change that needs to be made, anything else is an explantation

gameLoop = True

gridList = []
worldHeight = 500
worldWidth = 500
#the larger open space is the more ceiling there is 
openSpace = math.floor((worldHeight/2)-3)

#controls how much of the world the player sees when playing
xResolution = 70
yResolution = 50

#(0,0) is at the top left corner of the screen
playerX = math.floor(worldWidth/2)
playerY = math.floor(worldHeight/2)

#options for shading color
brightnessOptions = ["\x1b[38;2;249;221;111m", "\x1b[38;2;230;236;150m", "\x1b[38;2;210;223;200m", "\x1b[38;2;169;213;200m", "\x1b[38;2;137;196;200m", "\x1b[38;2;110;193;200m", "\x1b[38;2;74;165;200m", "\x1b[38;2;48;152;200m", "\x1b[38;2;23;139;200m", "\x1b[38;2;0;88;188m", "\x1b[38;2;249;221;111m"]
resetColor = "\x1b[0m"

#creates a list with lists inside of it. each list has a number of characters equal to worldwidth, there are a number, worldheight, of these lists
def createGrid():
  for y in range(0, worldHeight):
    gridList.append([])
    for x in range(0, worldWidth):
      gridList[y].append(0)
      
def addBackground():
  global gridList
  #for every value in the grid of the world, if the y value((0,0) is at top left) falls between two values it is air(1): creates open space in middle of map
  for y in range(0, worldHeight):
    for x in range(0, worldWidth):
      if (worldHeight - openSpace) > y > openSpace:
        gridList[y][x] = 1
      else:
        gridList[y][x] = 0
        
def addRooms(minRoomSize, maxRoomSize, roomAmount):
  for x in range(0, roomAmount):
    #picks random x and y cordinate in grid
    randomX = random.randint(0,worldWidth)
    randomY = random.randint(0,worldHeight)
    #picks random width and height
    randomWidth = random.randint(minRoomSize, maxRoomSize)
    randomHeight = random.randint(minRoomSize, maxRoomSize)
    #cheks to make sure index is in range
    if (randomX + randomWidth) < worldWidth and (randomY + randomHeight) < worldHeight:
      #used random height/width and random position to carve out an area of air
      for y in range(0, randomHeight):
        for x in range(0, randomWidth):
            gridList[y + randomY][x + randomX] = 1

def erodeTerrain(intensity):
  for i in range(0, intensity):
    for y in range(10, (worldHeight-10)):
      for x in range(10, (worldWidth-10)):
        if random.randint(0,60) == 1:
          #removes between five and three chunks of wall for the area between a wall/ground and air
          if gridList[y][x] == 0 and gridList[y-1][x] == 1:
              gridList[y][x] = 1
              gridList[y][x - 1] = 1
              gridList[y][x + 1] = 1
              for x in range(0,random.randint(0,3)):
                gridList[y][x - 1 - x] = 1
                gridList[y][x + 1 + x] = 1

def addTrees(treeAmount):
  treeNumber = 0
  #creates a (treeamount) number of trees
  while treeNumber < treeAmount:
    #picks random x and y in grid
    randomX = random.randint(5,(worldWidth-5))
    randomY = random.randint(5,(worldHeight-5))
    #checks that ground is below randomY and that the ground to the left and right of randomX are not filled
    if gridList[randomY+1][randomX] == 0 and gridList[randomY][randomX + 1] == 1:
      treeNumber = treeNumber + 1
      #sets the two spots next to bottom trunk to air(1)
      gridList[randomY][randomX] = 1
      #sets the middle tree spot to a straight line(3): "|"
      gridList[randomY][randomX+1] = 3
      gridList[randomY][randomX+2] = 1
      randomTreeHeight = random.randint(2,6)
      #adds mid layers of tree(creates random height variation)
      for i in range(1, randomTreeHeight):
        #countinues trunk of tree(3): "|"
        gridList[randomY-i][randomX+1] = 3
        #adds a "/" on left of tree
        gridList[randomY-i][randomX] = 2
        #adds a "\" on the right of tree
        gridList[randomY-i][randomX+2] = 4
      #adds a "^" as a top to the tree(5)
      gridList[randomY-randomTreeHeight][randomX+1] = 5

def addRocks(rockAmount):
  rockNumber = 0
  while rockNumber < rockAmount:
    randomX = random.randint(5,(worldWidth-5))
    randomY = random.randint(5,(worldHeight-5))
    #checks that there will be ground below the rock and air above the rock
    if gridList[randomY][randomX] == 0 and gridList[randomY - 1][randomX] == 1:
      #adds a "@" character as a rock(6)
      rockNumber = rockNumber + 1
      gridList[randomY][randomX] = 6

def addPlants(plantAmount):
  plantNumber = 0
  while plantNumber < plantAmount:
    randomX = random.randint(5,(worldWidth-5))
    randomY = random.randint(5,(worldHeight-5))
    #checks ground will be below plants and air will be above
    if gridList[randomY][randomX] == 0 and gridList[randomY - 1][randomX] == 1:
      #places a plant in the grid at the randomY and randomX
      plantNumber = plantNumber + 1
      if random.randint(0,1) == 1:
        gridList[randomY][randomX] = 9
      elif random.randint(0,1) == 1:
        gridList[randomY][randomX] = 10

def createWaterFall():
  #checks entire grid 
  for y in range(0, worldHeight):
    for x in range(0, worldWidth):
      #detects water and if the spot below it is air
      if gridList[y][x] == 7 and gridList[y+1][x] == 1:
        waterFallHeight = 0
        #adds a water symbol below the current waterfall until it reaches ground
        while gridList[y+waterFallHeight + 1][x] == 1:
          waterFallHeight = waterFallHeight + 1
          gridList[y+waterFallHeight][x] = 8

def addWater(waterAmount):
  #determines water amount, the while loop runs until that amount of water has been placed
  waterNumber = 0
  while waterNumber < waterAmount:
    #chooses random spot
    randomX = random.randint(10,(worldWidth-10))
    randomY = random.randint(10,(worldHeight-10))
    #checks that air is above spot and ground is below
    if gridList[randomY][randomX] == 0 and gridList[randomY - 1][randomX] == 1:
      waterNumber = waterNumber + 1
      gridList[randomY][randomX] = 7
      #adds a random number of water "~" at the random location and to the right and left of it(7)
      for x in range(1, random.randint(2,7)):
        #stops water placement if the water would go through a wall
        if gridList[randomY - 1][randomX + x] == 0 or gridList[randomY - 1][randomX - x] == 0:
          break
        else:
          gridList[randomY][randomX + x] = 7
          gridList[randomY][randomX - x] = 7
  #for any water overhanging air, the water will fall down until it hits ground, where it will stop
  createWaterFall()

def drawWalls(y, x, brightness):
  # there will be list index issues at the edge of the screen dou to adding and subtracting from y and x, could fix by changing range in draw screen function
  airRight = False
  airLeft = False
  airUp = False
  airDown = False
  
  #this sequence detects if their is air(1) in any direction from a wall
  if gridList[y][x + 1] != 0:
    airRight = True
  if gridList[y][x-1] != 0:
    airLeft = True
  if gridList[y+1][x] != 0:
    airDown = True
  if gridList[y-1][x] != 0:
    airUp = True

#for a wall number at the position given(0), if there is air on some side of it, it will not print a wall "█" but the side of a wall depending on where the air is
  if airDown == True:
    print(brightnessOptions[brightness - 1] + "-", end = "")
  elif airRight == True or airLeft == True:
    print(brightnessOptions[brightness - 1] + "|", end = "")
  elif airUp == True:
    print(brightnessOptions[brightness - 1] + "-", end = "")
  else:
    print(brightnessOptions[brightness - 1] + "█", end = "")

def detectDistanceForLighting(sourceY, sourceX, spotY, spotX, lightRadius):
  #finds the distance between a source of light and a spot evaluated for brightness
  positionDifferenceY = sourceY - spotY
  positionDifferenceX = sourceX - spotX
  distance = math.sqrt((2*positionDifferenceY)**2 + positionDifferenceX**2)
  #sets brightness to a value between 1 and 10 within a radius given or sets it to ten if it is outside of the light radius
  if distance < lightRadius:
    brightness = math.floor(distance/(lightRadius/10))
  else:
    brightness = 10
  # the function edits the brightness to be dark if blocked by a wall from the source of the light
  brightness = rayTrace(sourceY, sourceX, spotY, spotX, brightness)
  return brightness

def rayTrace(sourceY, sourceX, spotY, spotX, previousBrightness):
  # this gives the position betwen the Source and Spot for X and Y values
  slopeNum = sourceY - spotY
  slopeDen = sourceX - spotX
  #removes the possibility of dividing by zero if slopeDen = 0
  if slopeDen == 0:
    slopeDen = 1
  #puts the slopeNum and slopeDen in terms of the slopeDen being one, for every one value the x changes, how much does the y change
  slopeNum = slopeNum / abs(slopeDen)
  slopeDen = slopeDen / abs(slopeDen)

  Check1 = False
  Check2 = False

  #this is used when the spot ecaluated is to the right of the source, need to differentiate because slope works differently
  if (spotX - sourceX) > 0:
    #looks at every point between sourceX and spotX
    for x in range(sourceX, spotX):
      #this is the y value at a given x between the two points
      yChange = sourceY + round(abs(sourceX - x) * slopeNum * -1)
      #stops overshooting the target near the end(due to rounding errors)
      if abs(yChange) > spotY:
        yChange = spotY
      #if starting at the source and moving towards the spot(which is to the right of source), a spot will be blocked if...
      #first there is a solid material(anything other than the player, air, and waterfalls)
      if gridList[yChange][x] != 1 and gridList[yChange][x] != 11 and gridList[yChange][x] != 8:
        Check1 = True
      #and then if there is air between the two spots
      elif gridList[yChange][x] == 1 and Check1 == True:
        Check2 = True
  #this is used when the spot calculated is to the left of the light
  else:
    for x in range(spotX, sourceX):
      #this is the y value at a given x between the two points
      yChange = spotY + round(abs(spotX - x) * slopeNum)
      # if, moving from the spot(which is left of the source) towards that source one x at a time, a spot will be blocked if...
      # first there is air between the spot and the source
      if gridList[yChange][x] == 1:
        Check1 = True
      #than if there is a solid material between the spot and source
      elif gridList[yChange][x] != 1 and gridList[yChange][x] != 11 and Check1 == True  and gridList[yChange][x] != 8:
        Check2 = True
  # if the above conditions are met, the spot is dark(10), otherwise there is no change from the expected brightness
  if Check2 == True:
    previousBrightness = 10
  else:
    previousBrightness = previousBrightness

  return previousBrightness

def addPlayer():
  #adds a player "*" at the positon of a plater(11)
  gridList[playerY][playerX] = 11

def drawScreen():
  #checks all grid positions in range of screen ResolutionX and screen Resolution Y, 
  for y in range((playerY - yResolution), (playerY + yResolution)):
      for x in range((playerX - xResolution), (playerX + xResolution)):
          #checks brightness of the spot given using the player as a light source
          brightness = detectDistanceForLighting(playerY, playerX, y, x, 50)
          #prints a chracters based on the returned value from the grid list and the returned brightness
          if gridList[y][x] == 1:
            print(brightnessOptions[brightness - 1] + " ", end = "")
          elif gridList[y][x] == 0:
            drawWalls(y, x, brightness)
          elif gridList[y][x] == 2:
            print(brightnessOptions[brightness - 1] + "/", end = "")
          elif gridList[y][x] == 3:
            print(brightnessOptions[brightness - 1] + "|", end = "")
          elif gridList[y][x] == 4:
            print(brightnessOptions[brightness - 1] + "\\", end = "")
          elif gridList[y][x] == 5:
            print(brightnessOptions[brightness - 1] + "^", end = "")
          elif gridList[y][x] == 6:
            print(brightnessOptions[brightness - 1] + "@", end = "")
          elif gridList[y][x] == 7 or gridList[y][x] == 8:
            print(brightnessOptions[brightness - 1] + "~", end = "")
          elif gridList[y][x] == 9:
            print(brightnessOptions[brightness - 1] + "𓍊", end = "")
          elif gridList[y][x] == 10:
            print(brightnessOptions[brightness - 1] + "𓋼", end = "")
          elif gridList[y][x] == 11:
            print(brightnessOptions[brightness - 1] + "*", end = "")
      print("" + resetColor)

#def playerMovement():
  #if keyboard.is_pressed("d"):
    #playerX = playerX + 1
  #elif keyboard.is_pressed("a"):
   #playerX = playerX - 1

createGrid()
addBackground()
addRooms(15, 40, 300)
erodeTerrain(10)
addWater(25)
addTrees(125)
addRocks(100)
addPlants(100)
addPlayer()
#while gameLoop == True:
  #playerMovement()
drawScreen()
  #time.sleep(.25)
  #os.system('clear')



#**Problem with trees creating straight shadow going down in bottom left quadrant**