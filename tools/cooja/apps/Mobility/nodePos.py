#-----------------------------------------------------------------------------------------------------------
# Filenme: nodePos.py
# Author: Abhilash Hegde
# Run on command line : python nodePos.py
# Version: v0.1
# Comments: Base version, will generate node positions randomly with all nodes moving at random speeds
#-----------------------------------------------------------------------------------------------------------
import sys
import random
import math
#import glob
#import re 

#======= Lists ==========
initialNodePosXList = []
initialNodePosYList = []
currNodePosXList = []
currNodePosYList = []
nodeSpeed = []
nodeDistCovPerTstep = []
testNodeDistCovPerTstep = []
nodePosXList = []
nodePosYList = []

#======= Simulation Params ======
totSimTime = 100.0; #secs
numNodes = 1; #nodes
maxDimX = 150.0; #Maximum X-size [m]
maxDimY = 150.0; #Maximum Y-size [m]

minSpeed = 2.0; # Min speed [m/s]
maxSpeed = 10.0; # Max speed [m/s]
timeStep = 0.2; #[s]

maxTheta = 2*(math.pi);
minTheta = 0.0;
#print random.randint(1,maxDimX)

totTimeIter = (int)(totSimTime/timeStep) + 1;
#print totTimeIter

for t in range(totTimeIter):
  nodePosXList.append([]);
  nodePosYList.append([]);
  testNodeDistCovPerTstep.append([]);

for i in range(numNodes):
  #set initial location of the nodes
  #initialNodePosXList.append(random.randint(1,maxDimX));
  #initialNodePosYList.append(random.randint(1,maxDimY));
  nodePosXList[0].append(random.randint(1,maxDimX));
  nodePosYList[0].append(random.randint(1,maxDimY));
  #Set Node Speed
  nodeSpeed.append(random.randint(minSpeed,maxSpeed));
  #Set the distance covered by nodes every time step
  nodeDistCovPerTstep.append(nodeSpeed[i]*timeStep);
  
#print initialNodePosXList
#print initialNodePosYList
#print nodePosXList[:]
#print nodePosYList[:]
#print nodeSpeed
#print nodeDistCovPerTstep

for i in range(totTimeIter):
  if(i == totTimeIter-1):
    break;
  for j in range(numNodes):
    theta = random.uniform(minTheta,maxTheta);    
    nodePosXList[i+1].append(nodePosXList[i][j]+(nodeDistCovPerTstep[j]*math.cos(theta)));
    nodePosYList[i+1].append(nodePosYList[i][j]+(nodeDistCovPerTstep[j]*math.sin(theta)));
    testNodeDistCovPerTstep[i+1].append(math.sqrt(math.pow((nodePosXList[i+1][j]-nodePosXList[i][j]),2)+math.pow((nodePosYList[i+1][j]-nodePosYList[i][j]),2)));

print "nodeXpos:", nodePosXList[:][:]
print "nodeYpos:", nodePosYList[:][:]
#print testNodeDistCovPerTstep[:][:]
#check distance

# print result
outputFile = "nodePosXY.dat" ;    # Write results to dat file 
opFile = open(outputFile,'w');

time = 0.0;

for nodePosXrow, nodePosYrow in zip(nodePosXList, nodePosYList):
  nodeNo = 0;
  for nodePosX,nodePosY in zip(nodePosXrow, nodePosYrow):
      strToWrt = str(nodeNo)+" "+str(time)+" "+str(nodePosX)+" "+str(nodePosY)+"\n";
      nodeNo = nodeNo + 1;
      opFile.write(strToWrt);
  time = time + timeStep
opFile.close();

#-----------------------------------------------------------------------------------------------------------
