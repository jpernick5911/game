import random
import math

gridList = []
worldHeight = 500
worldWidth = 500
#the larger open space is the more ceiling there is 
openSpace = math.floor((worldHeight/2)-3)

xResolution = 60
yResolution = 250

#(0,0) is at the top left corner of the screen
playerX = math.floor(worldWidth/2)
playerY = math.floor(worldHeight/2)

brightnessOptions = ["\x1b[38;2;249;221;111m", "\x1b[38;2;230;236;150m", "\x1b[38;2;210;223;200m", "\x1b[38;2;169;213;200m", "\x1b[38;2;137;196;200m", "\x1b[38;2;110;193;200m", "\x1b[38;2;74;165;200m", "\x1b[38;2;48;152;200m", "\x1b[38;2;23;139;200m", "\x1b[38;2;0;88;188m", "\x1b[38;2;249;221;111m"]
resetColor = "\x1b[0m"

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

def drawWalls(y, x, brightness):
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
    print(brightnessOptions[brightness - 1] + "-", end = "")
  elif airRight == True or airLeft == True:
    print(brightnessOptions[brightness - 1] + "|", end = "")
  elif airUp == True:
    print(brightnessOptions[brightness - 1] + "-", end = "")
  else:
    print(brightnessOptions[brightness - 1] + "█", end = "")

def detectDistanceForLighting(sourceY, sourceX, spotY, spotX, lightRadius):
  positionDifferenceY = sourceY - spotY
  positionDifferenceX = sourceX - spotX
  distance = math.sqrt((2*positionDifferenceY)**2 + positionDifferenceX**2)
  if distance < lightRadius:
    brightness = math.floor(distance/(lightRadius/10))
  else:
    brightness = 10
  brightness = rayTrace(sourceY, sourceX, spotY, spotX, brightness)
  return brightness

def rayTrace(sourceY, sourceX, spotY, spotX, previousBrightness):
  slopeNum = sourceY - spotY
  slopeDen = sourceX - spotX
  if slopeDen == 0:
    slopeDen = 1
  slopeNum = round(slopeNum / abs(slopeDen))
  slopeDen = slopeDen / abs(slopeDen)

  Check1 = False
  Check2 = False
  if (spotX - sourceX) > 0:
    for x in range(sourceX, spotX):
      yChange = spotY + (abs(spotX - x) * slopeNum)
      if abs(yChange) > spotY:
        yChange = spotY
      #not equaling eleven stops player from casting a shadow
      if gridList[yChange][x] != 1 and gridList[yChange][x] != 11:
        Check1 = True
      elif gridList[yChange][x] == 1 and Check1 == True:
        Check2 = True
  else:
    for x in range(spotX, sourceX):
      yChange = spotY + (abs(spotX - x) * slopeNum)
      if abs(yChange) > sourceY:
        yChange = sourceY
      if gridList[yChange][x] == 1:
        Check1 = True
      #not equaling eleven stops player from casting shadow
      elif gridList[yChange][x] != 1 and gridList[yChange][x] != 11 and Check1 == True:
        Check2 = True
  
  if Check2 == True:
    previousBrightness = 10
  else:
    previousBrightness = previousBrightness

  return previousBrightness

def addPlayer():
  gridList[playerY][playerX] = 11

def drawScreen():
  for y in range(2, (worldHeight - 2)):
    if (playerY + yResolution) > y > (playerY - yResolution):
      for x in range(2, (worldWidth - 2)):
        if (playerX + xResolution) > x > (playerX - xResolution):
          brightness = detectDistanceForLighting(playerY, playerX, y, x, 50)
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

createGrid()
addBackground()
addRooms(15, 60, 300)
erodeTerrain(10)
addWater(25)
addTrees(125)
addRocks(100)
addPlants(100)
addPlayer()
drawScreen()