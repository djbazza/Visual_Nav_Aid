from m5stack import *
from m5ui import *
from uiflow import *
import time
import imu
dispMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
rgb.set_screen(dispMatrix)
imu0 = imu.IMU()
colour = 0xffff00
dispType = "arrow"
i = 0
j = 0

def dispMatrix(i,j):
  DispMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for x in range(5):
    for y in range(5):
      if x == i: 
        DispMatrix[x*5+y] = colour
      elif y == j:
        DispMatrix[x*5+y] = colour
      else:
        DispMatrix[x*5+y] = 0
  return DispMatrix

def rotMatrix(m,q):
  if q == 1:
    for o in range(5):
      m[(o*5)-5] = 0
  elif q == 5:
    for o in range(5):
      m[o] = 0
  for a in range(q):
    m.insert(len(m) - 1, m.pop(0))
  return m

def revMatrix(m,q):
  if q == 1:
    for o in range(5):
      m[(o*5)-1] = 0
  elif q == 5:
    for o in range(5):
      m[24-o] = 0
  for a in range(q):
    m.insert(0, m.pop(len(m) - 1))
  return m
  
 
def goForward():
  global i
  global dispMatrix
  dispMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  if dispType == "arrow":
    dispMatrix = [0,0,0x37ff00,0,0,0,0x37ff00,0x37ff00,0x37ff00,0,0x37ff00,0,0x37ff00,0,0x37ff00,0,0,0x37ff00,0,0,0,0,0x37ff00,0,0]
  elif dispType == "shortArrow":
    dispMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,colour,0,0,0,colour,0,colour,0,colour,0,0,0,colour]
  elif dispType == "2lines":
    dispMatrix = [colour,colour,colour,colour,colour,colour,colour,colour,colour,colour,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  else:
    dispMatrix = [colour,colour,colour,colour,colour,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for i in range(5):
    #dispMatrix = dispMatrix [5: ] + dispMatrix[ :5]
    dispMatrix = rotMatrix(dispMatrix, 5)
    rgb.set_screen(dispMatrix)
    wait(0.1)

#    global i
#    global j
#    j=6
#    rgb.set_screen(dispMatrix(i,j))
#    if i < 0:
#      i=5
#    else:
#      i=i-1
  
def goBack():
  global i
  global dispMatrix
  dispMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  if dispType == "arrow":
    dispMatrix = [0,0,0x37ff00,0,0,0,0,0x37ff00,0,0,0x37ff00,0,0x37ff00,0,0x37ff00,0,0x37ff00,0x37ff00,0x37ff00,0,0,0,0x37ff00,0,0]
  elif dispType == "shortArrow":
    dispMatrix = [colour,0,0,0,colour,0,colour,0,colour,0,0,0,colour,0,0,0,0,0,0,0,0,0,0,0,0]
  elif dispType == "2lines":
    dispMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,colour,colour,colour,colour,colour,colour,colour,colour,colour,colour]
  else:
    dispMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,colour,colour,colour,colour,colour]
  for i in range(5):
    rgb.set_screen(dispMatrix)
    dispMatrix = revMatrix(dispMatrix, 5)
    wait(0.1)
#    global i
#    global j
#    j=6
#    rgb.set_screen(dispMatrix(i,j))
#    if i > 4:
#      i=0
#    else:
#      i=i+1
      
def goLeft():
  global i
  global dispMatrix
  dispMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  if dispType == "arrow":
    dispMatrix = [0,0,0x18ff14,0,0,0,0x18ff14,0,0,0,0x18ff14,0x18ff14,0x18ff14,0x18ff14,0x18ff14,0,0x18ff14,0,0,0,0,0,0x18ff14,0,0]
  elif dispType == "shortArrow":
    dispMatrix = [0,0,0,0,colour, 0,0,0,colour,0, 0,0,colour,0,0, 0,0,0,colour,0, 0,0,0,0,colour]
  elif dispType == "2lines":
    dispMatrix = [0,0,0,colour,colour,0,0,0,colour,colour,0,0,0,colour,colour,0,0,0,colour,colour,0,0,0,colour,colour]
  else:
    dispMatrix = [0,0,0,0,colour,0,0,0,0,colour,0,0,0,0,colour,0,0,0,0,colour,0,0,0,0,colour]
  for i in range(5):
    rgb.set_screen(dispMatrix)
    dispMatrix = rotMatrix(dispMatrix, 1)
    #dispMatrix.insert(len(dispMatrix) - 1, dispMatrix.pop(0))
    wait(0.1)
#    global i
#    global j
#    i=6
#    rgb.set_screen(dispMatrix(i,j))
#    if j < 0:
#      j=4
#    else:
#      j=j-1

def goRight():
  global i
  global dispMatrix
  dispMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  if dispType == "arrow":
    dispMatrix = [0,0,0x18ff14,0,0,0,0,0,0x18ff14,0,0x18ff14,0x18ff14,0x18ff14,0x18ff14,0x18ff14,0,0,0,0x18ff14,0,0,0,0x18ff14,0,0]
  elif dispType == "shortArrow":
    dispMatrix = [colour,0,0,0,0, 0,colour,0,0,0, 0,0,colour,0,0, 0,colour,0,0,0, colour,0,0,0,0]
  elif dispType == "2lines":
    dispMatrix = [colour,colour,0,0,0,colour,colour,0,0,0,colour,colour,0,0,0,colour,colour,0,0,0,colour,colour,0,0,0]
  else:
    dispMatrix = [0,0,0,0,colour,0,0,0,0,colour,0,0,0,0,colour,0,0,0,0,colour,0,0,0,0,colour]
  for i in range(5):
    rgb.set_screen(dispMatrix)
    dispMatrix = revMatrix(dispMatrix, 1)
    #dispMatrix.insert(0, dispMatrix.pop(len(dispMatrix) - 1))
    wait(0.1)
#    global i
#    global j
#    i=6
#    rgb.set_screen(dispMatrix(i,j))
#    if j > 4:
#      j=0
#    else:
#      j=j+1
 
  
while True:
  if (imu0.ypr[1]) > (imu0.ypr[2]) and (imu0.ypr[1]) - (imu0.ypr[2]) > 60:
    if (imu0.ypr[1]) > 0:
      goForward()
    else:
      goLeft()
  elif (imu0.ypr[1]) < (imu0.ypr[2]) and (imu0.ypr[2]) - (imu0.ypr[1]) > 60:
    if (imu0.ypr[2]) > 0:
      goRight()
    else:
      goBack()
  else:
    rgb.set_screen([0,0,0xff0000,0,0,0,0xff0000,0,0xff0000,0,0xff0000,0,0,0,0xff0000,0,0xff0000,0,0xff0000,0,0,0,0xff0000,0,0])
  wait(0.1)
  wait_ms(2)
