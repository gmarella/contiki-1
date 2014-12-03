#-----------------------------------------------------------------------------------------------------------
# Filenme: nodePos.py
# Run on command line : python nodePos.py
# Version: v0.2
# Comments: v0.1 -> Base version, will generate node positions randomly with all nodes moving at random speeds
#           v0.2 -> Enchanced version with support for moving nodes in X,Y or XY directions
#                   Support for initial Grid and Uniform topology 
#                   Support to set individual node speeds
#                   Support to restrict the movement of nodes to the required quadrant of terrain
#
#-----------------------------------------------------------------------------------------------------------

import sys
import random
import math
#import glob
#import re 

#=========================== Mobility Models =============================
#Random Walk model
#========================= Lists ==========================================
initialNodePosXList = []
initialNodePosYList = []
currNodePosXList = []
currNodePosYList = []
nodeSpeed = []
nodeDistCovPerTstep = []
testNodeDistCovPerTstep = []
nodePosXList = []
nodePosYList = []
nodeSpeedsList = []
nodeSpeedHitsMaxList = []
nodeSpeedAccRateList = []
nodeSpeedDecRateList = []
#============================= Simulation Params ============================
totSimTime = 60.0; #secs
numNodes = 20; #nodes, for GRID topology no: of nodes must be perfect square!
maxDimX = 60.0; #Maximum X-size [m]
maxDimY = 60.0; #Maximum Y-size [m]

isInitialTopology = 1; # 1-RANDOM, 2-GRID, 3-UNIFORM
gridUnit = 4; #Unit of the grid in (m) only required for GRID topology
#Flag to control the speed assignments to the nodes
isNodeSpeedType = 1; # 1-Random speeds, 2-Individual speeds
#if isNodeSpeedType = 2, set the node speeds individually here, only applicable for constant speed scenario
#nodeSpeedsList = [5,10,15,20];

#Only this flag can be set when isNodeSpeedType = 1, for isNodeSpeedType = 2, below must always be set to 0
isNodeSpeedAccDecc  = 1; #If set, nodes accelerate from minSpeed to maxSpeed and then deaccelerate from maxSpeed to minSpeed at a random rate


minSpeed = 5.0; # Min speed [m/s]
maxSpeed = 10.0; # Max speed [m/s]
timeStep = 0.2; #[s]

#Flags for generating points in the required quadrants, set only one of the flags
isOnlyFirstQuadrant = 0; # Both X and Y co-ordinates are +ve
isTopQuadrants = 0; # X co-ordinates are +ve or -ve, Y co-ordinates always +ve
isAllQuadrants = 1; # All X and Y co-ordinates (+ve and -ve possible)

#Direction of node movement
isNodeMoveDirection = 1; # 1-Both XY directions, 2- Along X direction, 3-Along Y direction
#===============================================================================

#========================== Params Initilizations ==============================

#Uniform Topology
terrainArea = maxDimX*maxDimY;
cellLen = math.sqrt(terrainArea/numNodes); #Physical terrain is divided into a number of cells based on no: of nodes
nodesX = math.ceil(maxDimX/cellLen);
cellLen = maxDimX/nodesX;

if (isTopQuadrants):
  maxTheta = math.pi;
  minTheta = 0.0;
elif (isOnlyFirstQuadrant):
  maxTheta = (math.pi)/2;
  minTheta = 0.0;
elif (isAllQuadrants):
  maxTheta = 2*(math.pi);
  minTheta = 0.0;
  
#print random.randint(1,maxDimX)

totTimeIter = (int)(totSimTime/timeStep) + 1;
#print totTimeIter

for t in range(totTimeIter):
  nodePosXList.append([]);
  nodePosYList.append([]);
  testNodeDistCovPerTstep.append([]);
  nodeSpeed.append([]);
  nodeDistCovPerTstep.append([]);
#===================================================================================

#============================== Generate Node Positions ============================
#Set the values for the nodes at time instant t = 0
for i in range(numNodes):
  #set initial location of the nodes
  #initialNodePosXList.append(random.randint(1,maxDimX));
  #initialNodePosYList.append(random.randint(1,maxDimY));
  if (isInitialTopology == 1): #RANDOM
    #X coordinate
    nodePosXList[0].append(random.uniform(1,maxDimX));
    #Y coordinate
    nodePosYList[0].append(random.uniform(1,maxDimY));
  elif(isInitialTopology == 2): #GRID
    #X coordinate
    nodePosXList[0].append(gridUnit*(i% (math.sqrt(numNodes))));
    #Y coordinate
    nodePosYList[0].append(gridUnit*math.floor((i/math.sqrt(numNodes))));
  elif(isInitialTopology == 3): #UNIFORM
    #X coordinate
    nodePosXList[0].append(cellLen*(i% (math.sqrt(numNodes)))+(cellLen*random.random()));
    #Y coordinate
    nodePosYList[0].append(cellLen*math.floor((i/math.sqrt(numNodes)))+(cellLen*random.random()));
  
  if(isNodeSpeedAccDecc == 1):
    iterMaxPoint = random.randint(math.ceil(0.3*(totTimeIter)),math.floor(0.7*(totTimeIter)));
    nodeSpeedHitsMaxList.append(iterMaxPoint);
    accRate = (maxSpeed-minSpeed)/(iterMaxPoint);
    decRate = (maxSpeed-minSpeed)/(totTimeIter-iterMaxPoint-1);
    #print "totTimeIter", totTimeIter
    #print "iterMaxPoint", iterMaxPoint
    #print "accRate", accRate
    #print "decRate", decRate
    nodeSpeedAccRateList.append(accRate);
    nodeSpeedDecRateList.append(decRate);
    nodeSpeed[0].append(minSpeed);
  #The following cases are for random and constant speeds
  elif(isNodeSpeedType == 1): #Random
    nodeSpeed[0].append(random.uniform(minSpeed,maxSpeed));
  elif(isNodeSpeedType == 2): #Individual speed, constant
    nodeSpeed[0].append(nodeSpeedsList[i]);
    
  nodeDistCovPerTstep[0].append(nodeSpeed[0][i]*timeStep);
  
#Set node speeds and distances convered per time step
for i in range(totTimeIter): 
  if(i == totTimeIter-1):
    break;
  for j in range(numNodes):
    if(isNodeSpeedAccDecc == 0):  
      #Set Node Speed
      if(isNodeSpeedType == 1):
        nodeSpeed[i+1].append(random.uniform(minSpeed,maxSpeed));
      elif(isNodeSpeedType == 2):
        nodeSpeed[i+1].append(nodeSpeedsList[j]);
    elif(isNodeSpeedAccDecc == 1):
      if(i < nodeSpeedHitsMaxList[j]):
        nowSpeed = nodeSpeed[i][j] + nodeSpeedAccRateList[j];
        if(nowSpeed > maxSpeed):
          nowSpeed = maxSpeed;
        nodeSpeed[i+1].append(nowSpeed);
      else:
        nowSpeed = nodeSpeed[i][j] - nodeSpeedDecRateList[j]
        if(nowSpeed < minSpeed):
          nowSpeed = minSpeed;
        nodeSpeed[i+1].append(nowSpeed);
    #Set the distance covered by nodes every time step
    nodeDistCovPerTstep[i+1].append(nodeSpeed[i+1][j]*timeStep);
    #print nodeDistCovPerTstep;
    
#print "Acc-Decc Lists\n"
#print "totTimeIter", totTimeIter
#print "nodeSpeedHitsMaxList",nodeSpeedHitsMaxList
#print "\n"   
#print "nodeSpeedAccRateList",nodeSpeedAccRateList
#print "\n" 
#print "nodeSpeedDecRateList",nodeSpeedDecRateList
#print "\n"
#print "nodeSpeed",nodeSpeed
 
#print initialNodePosXList
#print initialNodePosYList
#print nodePosXList[:]
#print nodePosYList[:]
#print nodeSpeed
#print nodeDistCovPerTstep

#Set the values for the nodes from time instant t > 0
for i in range(totTimeIter):
  if(i == totTimeIter-1):
    break;
  for j in range(numNodes):
    theta = random.uniform(minTheta,maxTheta);  
    if(isNodeMoveDirection == 1):    #Movement Along Both XY directions
      nodePosXList[i+1].append(nodePosXList[i][j]+(nodeDistCovPerTstep[i][j]*math.cos(theta)));
      nodePosYList[i+1].append(nodePosYList[i][j]+(nodeDistCovPerTstep[i][j]*math.sin(theta)));
      testNodeDistCovPerTstep[i+1].append(math.sqrt(math.pow((nodePosXList[i+1][j]-nodePosXList[i][j]),2)+math.pow((nodePosYList[i+1][j]-nodePosYList[i][j]),2)));
    elif(isNodeMoveDirection == 2):   #Movement Along X direction
      nodePosXList[i+1].append(nodePosXList[i][j]+(nodeDistCovPerTstep[i][j]*math.cos(theta)));
      nodePosYList[i+1].append(nodePosYList[i][j]);
      testNodeDistCovPerTstep[i+1].append(math.sqrt(math.pow((nodePosXList[i+1][j]-nodePosXList[i][j]),2)+math.pow((nodePosYList[i+1][j]-nodePosYList[i][j]),2)));
    elif(isNodeMoveDirection == 3):    #Movement Along Y direction
      nodePosXList[i+1].append(nodePosXList[i][j]);
      nodePosYList[i+1].append(nodePosYList[i][j]+(nodeDistCovPerTstep[i][j]*math.sin(theta)));
      testNodeDistCovPerTstep[i+1].append(math.sqrt(math.pow((nodePosXList[i+1][j]-nodePosXList[i][j]),2)+math.pow((nodePosYList[i+1][j]-nodePosYList[i][j]),2)));

#print "nodeXpos:", nodePosXList[:][:]
#print "nodeYpos:", nodePosYList[:][:]
#print testNodeDistCovPerTstep[:][:]
#check distance

# print result
outputFile = "nodePosXY.dat" ;    # Write results to dat file 
opFile = open(outputFile,'w');

time = 0.0;

for nodePosXrow, nodePosYrow in zip(nodePosXList, nodePosYList):
  nodeNo = 1;
  for nodePosX,nodePosY in zip(nodePosXrow, nodePosYrow):
      strToWrt = str(nodeNo)+" "+str(time)+" "+str(nodePosX)+" "+str(nodePosY)+"\n";
      nodeNo = nodeNo + 1;
      opFile.write(strToWrt);
  time = time + timeStep;
opFile.close();

#-----------------------------------------------------------------------------------------------------------
