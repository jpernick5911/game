import random
import math

gridList = []
worldHeight = 500
worldWidth = 500
#the larger open space is the more ceiling there is 
openSpace = math.floor((worldHeight/2)-3)

xResolution = 75
yResolution = 250

#(0,0) is at the top left corner of the screen
playerX = math.floor(worldWidth/2)
playerY = math.floor(worldHeight/2)

rayList = []

def createGrid():
  for y in range(0, worldHeight):
    gridList.append([])
    for x in range(0, worldWidth):
      gridList[y].append(0)
      
def addBackground():
  global gridList
  for y in range(0, worldHeight):
    for x in range(0, worldWidth):
      if (worldHeight - openSpace) > y > openSpace:
        gridList[y][x] = 1
      else:
        gridList[y][x] = 0
        
def addRooms(minRoomSize, maxRoomSize, roomAmount):
  for x in range(0, roomAmount):
    randomX = random.randint(0,worldWidth)
    randomY = random.randint(0,worldHeight)
    randomWidth = random.randint(minRoomSize, maxRoomSize)
    randomHeight = random.randint(minRoomSize, maxRoomSize)
    if (randomX + randomWidth) < worldWidth and (randomY + randomHeight) < worldHeight:
      for y in range(0, randomHeight):
        for x in range(0, randomWidth):
            gridList[y + randomY][x + randomX] = 1

def erodeTerrain(intensity):
  for i in range(0, intensity):
    for y in range(10, (worldHeight-10)):
      for x in range(10, (worldWidth-10)):
        if random.randint(0,60) == 1:
          if gridList[y][x] == 0 and gridList[y-1][x] == 1:
              gridList[y][x] = 1
              gridList[y][x - 1] = 1
              gridList[y][x + 1] = 1
              for x in range(0,random.randint(0,3)):
                gridList[y][x - 1 - x] = 1
                gridList[y][x + 1 + x] = 1

def addTrees(treeAmount):
  treeNumber = 0
  while treeNumber < treeAmount:
    randomX = random.randint(5,(worldWidth-5))
    randomY = random.randint(5,(worldHeight-5))
    if gridList[randomY+1][randomX] == 0 and gridList[randomY][randomX] == 1 and gridList[randomY][randomX + 1] == 1:
      treeNumber = treeNumber + 1
      gridList[randomY][randomX] = 1
      gridList[randomY][randomX+1] = 3
      gridList[randomY][randomX-1] = 1
      randomTreeHeight = random.randint(2,6)
      for i in range(1, randomTreeHeight):
        gridList[randomY-i][randomX+1] = 3
        gridList[randomY-i][randomX] = 2
        gridList[randomY-i][randomX+2] = 4
      gridList[randomY-randomTreeHeight][randomX+1] = 5

def addRocks(rockAmount):
  rockNumber = 0
  while rockNumber < rockAmount:
    randomX = random.randint(5,(worldWidth-5))
    randomY = random.randint(5,(worldHeight-5))
    if gridList[randomY][randomX] == 0 and gridList[randomY - 1][randomX] == 1:
      rockNumber = rockNumber + 1
      gridList[randomY][randomX] = 6

def addPlants(plantAmount):
  plantNumber = 0
  while plantNumber < plantAmount:
    randomX = random.randint(5,(worldWidth-5))
    randomY = random.randint(5,(worldHeight-5))
    if gridList[randomY][randomX] == 0 and gridList[randomY - 1][randomX] == 1:
      plantNumber = plantNumber + 1
      if random.randint(0,1) == 1:
        gridList[randomY][randomX] = 9
      elif random.randint(0,1) == 1:
        gridList[randomY][randomX] = 10
      else:
        gridList[randomY][randomX] = 11

def createWaterFall():
  for y in range((playerY - yResolution), (playerY + yResolution)):
    for x in range((playerX - xResolution), (playerX + xResolution)):
      if gridList[y][x] == 7 and gridList[y+1][x] == 1:
        waterFallHeight = 0
        while gridList[y+waterFallHeight + 1][x] == 1:
          waterFallHeight = waterFallHeight + 1
          gridList[y+waterFallHeight][x] = 8

def addWater(waterAmount):
  waterNumber = 0
  while waterNumber < waterAmount:
    randomX = random.randint(10,(worldWidth-10))
    randomY = random.randint(10,(worldHeight-10))
    if gridList[randomY][randomX] == 0 and gridList[randomY - 1][randomX] == 1:
      waterNumber = waterNumber + 1
      gridList[randomY][randomX] = 7
      for x in range(1, random.randint(2,7)):
        if gridList[randomY - 1][randomX + x] == 0 or gridList[randomY - 1][randomX - x] == 0:
          break
        else:
          gridList[randomY][randomX + x] = 7
          gridList[randomY][randomX - x] = 7
  createWaterFall()

def drawWalls(y, x):
  # there will be list index issues at the edge of the screen dou to adding and subtracting from y and x, could fix by changing range in draw screen function
  airRight = False
  airLeft = False
  airUp = False
  airDown = False
  
  if gridList[y][x + 1] == 1:
    airRight = True
  if gridList[y][x-1] == 1:
    airLeft = True
  if gridList[y+1][x] == 1:
    airDown = True
  #line below also detects when trees are above so their isnt air below trees 
  if gridList[y-1][x] == 1 or gridList[y-1][x] == 3:
    airUp = True

  if airDown == True:
    print("-", end = "")
  elif airRight == True or airLeft == True:
    print("|", end = "")
  elif airUp == True:
    print("-", end = "")
  else:
    print("█", end = "")
  
def rayTrace(sourceY, sourceX, lightRadius, rayTraceResolution):
  global rayList
  
  
  if ((playerY + yResolution) > sourceY > (playerY - yResolution)) and (((playerX + xResolution) > sourceX > (playerX - xResolution))):
    rayList = []
    for y in range(0, worldHeight):
      rayList.append([])
      for x in range(0, worldWidth):
        rayList[y].append(0)
  
    raySlopeNum = 1
    raySlopeDen = rayTraceResolution
    for x in range(0, (rayTraceResolution - 1)):
      raySlopeNum = raySlopeNum + 1
      changePositionY = 0
      changePositionX = 0
      while gridList[sourceY - changePositionY][sourceX + changePositionX] == 1:
        changePositionY = changePositionY + raySlopeNum
        changePositionX = changePositionX + raySlopeDen
      distance = math.sqrt(changePositionY**2 + changePositionX**2)
      if distance < lightRadius:
        #sets distance to a value from 1 to 10 if within the light radius
        brightness = math.floor(distance/(lightRadius/10))
        #puts brightness at position ray collides with wall in brightness list
        rayList[sourceY + changePositionY][sourceX + changePositionX] = brightness
    
  
def drawScreen():
  for y in range(2, (worldHeight - 2)):
    if (playerY + yResolution) > y > (playerY - yResolution):
      for x in range(2, (worldWidth - 2)):
        if (playerX + xResolution) > x > (playerX - xResolution):
          if gridList[y][x] == 1:
            print(" ", end = "")
          elif gridList[y][x] == 0:
            drawWalls(y, x)
          elif gridList[y][x] == 2:
            print("/", end = "")
          elif gridList[y][x] == 3:
            print("|", end = "")
          elif gridList[y][x] == 4:
            print("\\", end = "")
          elif gridList[y][x] == 5:
            print("^", end = "")
          elif gridList[y][x] == 6:
            print("@", end = "")
          elif gridList[y][x] == 7 or gridList[y][x] == 8:
            print("~", end = "")
          elif gridList[y][x] == 9:
            print("𓍊", end = "")
          elif gridList[y][x] == 10:
            print("𓋼", end = "")
      print("")

createGrid()
addBackground()
addRooms(15, 60, 300)
erodeTerrain(10)
addWater(25)
addTrees(125)
addRocks(100)
addPlants(100)
#drawScreen()

rayTrace(playerY, playerX, 50, )
print(rayList)

#print("hi")
#print("\033[38;5;242mhi \n")
