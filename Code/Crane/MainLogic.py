'''
===================================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Crane
Description: This script handles the main logic for the functioning
of the Crane, including intialization of state, execution of Pick and
Place tasks and so on.
===================================================================
'''

# Libraries
# ================

from vcScript import *
import urllib2
import json
from vcHelpers.Robot2 import * 
import vcMatrix as mat  
import vcVector
import ast

# Global Variables
# ================
'''
app (vcApplication): app contains the object type for the main VC application that gives access 
to the application's GUI, commands and other common properties

comp (vcComponent): comp contains the vcComponent of the component that this script is 
contained in.

IP (STR): IP contains the IP address of the simulator

crane (vcHelpers.Robot.vcRobot): crane is a vcRobot object for the crane

robotController (vcRobotController); robotController is the controller that allows to control the 
crane and drive its joints

container (vcContainer): container is a component container used for simulating buffer or 
storage area to contain pallets in the forks of the crane

pickSignal (vcBooleanSignal): pickSignal is a Boolean signal that is True when the crane picks a
component (pallet)

placeSignal (vcBooleanSignal):  placeSignal is a Boolean signal that is True when the crane places a
component (pallet)

RefNode (vcProperty): RefNode is a property that links the crane to the storage area to which in acts
as a meanso of transport

palletParentName (STR): palletParentName is variable used to denote the name of the node that contains
the said pallet
'''



comp = getComponent()
app = getApplication()
IP = app.findComponent("Station Commander").getProperty("Address").Value
crane = None
robotController = None
container = comp.findBehavioursByType(VC_COMPONENTCONTAINER)[0]
pickSignal = comp.findBehaviour("Pick")
placeSignal = comp.findBehaviour("Place")
RefNode = comp.getProperty("RefNode").Value
palletParentName = ""


ivory_ceramic= app.findMaterial("ivory_ceramic")
tan= app.findMaterial("tan")  
darkBrown= app.findMaterial("material:51:Strarrag France_Angebot")
palletStatusColours = {2:"",100:ivory_ceramic,101:tan,102:darkBrown}
tasks = []


def mapXCoordinate(coordinate):
  '''
  Type and Description:
  ---------------------
  This user-defined function maps the location of the crane in the simulator
  in the X-direction with that in the VC Layout
  
  Arguments: 
  ----------
  
  coordinate (STR): cooridnate is the coordinate of the Crane along the X-direction
  in the Simulator Space
  
  Returns:
  --------
  
  mappedCoordinate (STR): mappedCoordinate is the coordinate of the Crane along the 
  X-direction in the 3D World Space of VC
  
  '''
  
  extremeLeftVCCoord=RefNode.findFeature("Crane.Storage.1000").FramePositionMatrix.P.X
  extremeRightVCCoord=RefNode.findFeature("Crane.Storage.84").FramePositionMatrix.P.X
  sumVC = abs(extremeRightVCCoord) + abs(extremeLeftVCCoord)
  sumFS = 46550 + 2500    # extreme right 46550; extremem left X2500 
  x = float(coordinate)/float(sumFS) * sumVC
  mappedCoordinate = x+extremeLeftVCCoord
  return mappedCoordinate

 
def OnStart():
  '''
  Type and Description:
  ---------------------
  This user-defined event handler is trigerred Triggered at the immediate 
  start of simulation. It updates the IP address of the station commander
  selected at the time of running for use by the component
  
  Global Variables: IP
  -----------------
  
  '''
  global IP, crane, robotController
  IP = app.findComponent("Station Commander").getProperty("Address").Value
  crane = getRobot()
  robotController = crane.Controller
  MoveImmediateToCurrentLocation()

  
def MoveImmediateToCurrentLocation():
  '''
  Type and Description:
  ---------------------
  This user-defined function called by the OnStart() function at the start of every 
  simulation moves the crane to its current location
  
  Arguments: NONE
  ----------
  
  Returns: NONE
  --------
  
  '''
  global crane, robotController
  currentToolXPosition = robotController.Tools[0].Node.WorldPositionMatrix.P.X
  currentToolYPosition = robotController.Tools[0].Node.WorldPositionMatrix.P.Y
  currentToolZPosition = robotController.Tools[0].Node.WorldPositionMatrix.P.Z
  newToolXPosition = currentToolXPosition
  
  servicestr = "/CraneService"
  method = "/Rest/IDeviceStatusApi/GetDeviceDiagnosticData"
  url = IP + servicestr + method
  
  response = restQuery(url,"")
  
  for data in response['Data']:
    if data['Key']=="Xposition":
      newToolXPosition = float(data['Value'])    
      break
      
  newToolXPosition = mapXCoordinate(newToolXPosition)
  matrix=mat.new()
  vec = vcVector.new(newToolXPosition,currentToolYPosition,currentToolZPosition)
  matrix.P = vec
  motionTarget = robotController.createTarget()
  motionTarget.MotionType = VC_MOTIONTARGET_MT_JOINT
  motionTarget.UseJoints = True
  motionTarget.TargetMode = VC_MOTIONTARGET_TM_WORLDTARGET
  motionTarget.Target = matrix
  robotController.moveImmediate(motionTarget)

def OnReset():
  '''
  Type and Description:
  ---------------------
  This ubuit-in event handler is triggered when simulation is reset to its initial state and 
  simulation clock is set at zero.
  
  Arguments: NONE
  ----------
  
  Returns: NONE
  --------
  
  '''
  del tasks[:]
  

def OnSignal(signal):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the script signals its value. 
  This function checks for the AddTask signal and appends any task to the global tasks array.
  
  Global Variables: tasks
  -----------------
  
  '''
  global tasks
  if signal.Name == "AddTask":
    tasks.append(ast.literal_eval(signal.Value))


def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and is used as the 
  main function of script.
  
  Global Variables: crane, comp, app, tasks
  -----------------
  
  '''
  global crane, comp, app, tasks
  
  # call init function to initialize the state of the crane
  init()
  
  # set the crane joint speed and force
  crane.JointForce = comp.getProperty("CraneAcceleration").Value
  crane.JointSpeed = comp.getProperty("CraneSpeed").Value


  while True:
    # waits for any task
    condition(lambda: tasks)
    newTask = tasks.pop(0)
    
    #get details of the new task
    newTaskId = newTask['Id']
    sourceLocation = newTask['SourceLocation']
    sourceComponentName = sourceLocation.rsplit('.',1)[0]
    sourceComponent = app.findComponent(sourceComponentName)
    palletId = newTask['PalletId']
    pallet = app.findComponent(palletId)
    targetLocation = newTask['TargetLocation']
    targetComponentName = targetLocation.rsplit('.',1)[0]
    #print "SourceLocation: ", sourceLocation
    #print "SourceComponentName", sourceComponentName
    #print "TargetComponentName", targetComponentName
    targetComponent = app.findComponent(targetComponentName)
    
    # Open Aisle Door of Source Location
    if not sourceComponentName == "Crane.Storage" and not sourceComponentName == "Crane":
      aisleDoorOperateSignal= sourceComponent.findBehaviour("AisleDoorOperate")
      aisleDoorOperateSignal.signal(True)
    
    # Open Aisle Door of Target Location
    if not targetComponentName == "Crane.Storage" and not targetComponentName == "Crane" : 
      aisleDoorOperateSignal= targetComponent.findBehaviour("AisleDoorOperate")
      aisleDoorOperateSignal.signal(True)
    
    # pick and place
    
    try:
      Pick(pallet)
      delay(0.1)
      Place(pallet, targetLocation)
    except Exception as e:
      print e
      print "Exception thrown with the following tranport details: "
      print "SourceLocation: ", sourceLocation
      print "SourceComponentName", sourceComponentName
      print "TargetComponentName", targetComponentName
    
    delay(0.5)


def init():
  '''
  Type and Description:
  ---------------------
  This user-defined function that initialises the Crane to its current 
  state, For e.g. transfer of pallets.
  
  Arguments: NONE 
  ----------
  
  Returns: NONE 
  --------
  
  Global Variables: comp, container, palletStatusColours
  -----------------
 
  '''
  global comp, container, palletStatusColours
  
  # fetching required service
  servicestr = "/PalletService"
  method = "/Rest/IDevicePalletDataApi/GetLocationPalletSummaries"
  url = IP + servicestr + method
  params = '{"deviceName":"Crane","locationNames":["'+container.Name+'"]}'
  
  response = restQuery(url,params)

  if len(response['Data']) > 0:
    
    # storing required information from response
    palletType = response['Data'][0]['PalletType']
    palletNumber = response['Data'][0]['Number']
    palletId = response['Data'][0]['Id']
    palletStatus = response['Data'][0]['Status']
    palletName = palletType +'.'+ palletNumber
    
    # searching for component
    pallet = app.findComponent(palletId)
    
    # transferring component if it exisits in the 3D world
    if pallet is not None:
      
      connector = container.getConnector('Input')
      pallet.transfer(connector)
      pallet.rebuild()

    # if component does not exist in the 3D world
    else:

      # Setting Template (either Machine or Material Pallet
      template = app.findComponent(palletType)
      
      # Creating a New Pallet 
      newPallet=template.clone(0)
      
      # Creating Id Property and assigning Fastems Pallet ID and Setting Name
      id = newPallet.createProperty(VC_STRING,"HRName")
      id.Value= str(palletName)
      newPallet.Name = palletId
      
      # Transferring Pallet to appropriate Storage Location
      connector = container.getConnector('Input')
      newPallet.transfer(connector)
      text = newPallet.getFeature("Text")
      
      # Assiging Visual Labels for the Pallet
      if palletType=="MaterialPallet":
        text.Text = '"'+palletType+palletNumber+'"'
      elif palletType.startswith("MachinePallet"):
        text.Text= '"'+palletNumber+'"'  
        
      # Assigning Status Colours to the Pallets
      if palletType == "MaterialPallet":
        collar1 = newPallet.findFeature("Block")
        collar2 = newPallet.findFeature("Block_10")
        collar1.Material = palletStatusColours[palletStatus]
        collar2.Material = palletStatusColours[palletStatus]
      newPallet.rebuild()



def getParentNode(node):
  '''
  Type and Description:
  ---------------------
  This user-defined recursive function returns the parent node for a node 
  passed in as an argument
  
  Arguments: 
  ----------
  node (vcNode): node contains the node for which the parent is requested for
  
  Returns:
  --------
  
  '''
  global palletParentName
  if node.Parent.Name != "ROOT":
    parentNode= node.Parent
    getParentNode(parentNode)
  else:
    palletParentName = node.Name
  return palletParentName
  
  
def Pick(pallet):
  '''
  Type and Description:
  ---------------------
  This user-defined function picks a pallet passed in as an argument
  
  Arguments: 
  ----------
  
  pallet (vcComponent): pallet requested to pick
  
  Returns: NONSE
  --------
   
  
  '''
  global crane, robotController, container
    
  # Set True to Pick Signal to indicate the the Crane is in Picking currently
  pickSignal.signal(True)
  
  # get the container, parent node of the container, and component object of 
  # current location of the pallet
  palletContainer = pallet.Container
  
  # get parent node of the container and its component object
  parentNodeName = getParentNode(palletContainer)
  palletLocationComponent = app.findComponent(parentNodeName)
  
  # get the World Position Coordinates of the pallet's and crane's current position 
  targetWPMatrix = pallet.WorldPositionMatrix
  craneWPMatrix = comp.WorldPositionMatrix
  
  # get the differences between the two position matrices
  vec = craneWPMatrix.P - targetWPMatrix.P
  
  # define a new appraoch matrix to define crane's approach
  approachMatrix = vcMatrix.new(targetWPMatrix)
  approachMatrix.translateAbs(0,vec.Y,0)
  
  # make the crane approach the pallet to be picked in the Y direction
  crane.jointMoveToMtx( approachMatrix )
  
  # make the crane to extend its forks and grab it
  crane.linearMoveToMtx( targetWPMatrix )
  container.grab(pallet)
  
  # make the crane to get back to the approach matrix
  crane.linearMoveToMtx( approachMatrix )
  
  # If not picking from the crane close the component's aisle door after picking
  if not parentNodeName == "Crane.Storage" :
    palletParentComp = app.findComponent(parentNodeName)
    aisleDoorOperateSignal = palletParentComp.findBehaviour("AisleDoorOperate")
    aisleDoorOperateSignal.signal(False)
    
  # Signal False to the pick signal to indicate completion of picking
  pickSignal.signal(False)

  
def Place(pallet, targetLocation):
  '''
  Type and Description:
  ---------------------
  This user-defined function  
  
  Arguments: 
  ----------
  
  pallet (vcComponent): pallet requested to pick
  targetLocation (STR): location where the pallet is to be placed
  
  Returns:  NONE
  --------
  
  '''
  global crane, robotController
  
  # Set True to Place  Signal to indicate the the Crane is in placing currently
  placeSignal.signal(True)

  # get place target details

  targetComponentName = targetLocation.rsplit('.',1)[0]
  targetComponent = app.findComponent(targetComponentName)
  targetWPMatrix = targetComponent.WorldPositionMatrix
  targetContainer = targetComponent.findBehaviour(targetLocation)
  
  # if the target continer is a two way conveyor, i.e.  material station
  if targetContainer.Type == 'rTwoWayPath':
    targetFrameFeature = targetContainer.Path[0]
  else:
    targetFrameFeature = targetContainer.Location
    
  # get World Position Matrix of Target
  targetFramePositionMatrix = targetFrameFeature.PositionMatrix
  targetContainerPWPMatrix = targetContainer.Parent.WorldPositionMatrix
  targetFrameWPMatrix = targetFramePositionMatrix * targetContainerPWPMatrix
  
  # get World Position Matrix of Crane
  craneWPMatrix = comp.WorldPositionMatrix
  
  # get the differences between the two position matrices 
  vec = craneWPMatrix.P - targetFrameWPMatrix.P
  
  # define a new appraoch matrix to define crane's approach
  approachMatrix = vcMatrix.new(targetFrameWPMatrix)
  approachMatrix.translateAbs(0, vec.Y, 0)
  
  # make the crane approach the pallet to be picked in the Y direction
  crane.jointMoveToMtx( approachMatrix )
  
  # make the crane to extend its forks and grab it
  crane.linearMoveToMtx( targetFrameWPMatrix )
  
  if targetContainer.Name.startswith("Crane.Storage"): # defined explicitly for performance reasons
    targetContainer.grab(pallet)
  else:
    receiveComponentSignal  = targetComponent.findBehaviour("ReceiveComponent")
    receiveComponentSignal.signal(pallet)
    
  # make the crane to get back to the approach matrix
  crane.linearMoveToMtx( approachMatrix )
  
  # Signal False to the place signal to indicate completion of placing
  placeSignal.signal(False)


def restQuery(url, data):
  '''
  Type and Description:
  ---------------------
  This user-defined function  makes RESTful queries to the Simulator
  
  Arguments: 
  ----------
  url (STR): contains the query URL
  data (STR): contains the additional information to be sent to the server
  
  Returns:
  --------
  encodedData : contains encoded Object response from the simulator
  
  '''
  if data == "":
      request = urllib2.Request(url, data="")
  else:
      request = urllib2.Request(url, data=data)
  encodedData = None
  try:
    response = urllib2.urlopen(request)
    data = response.read()
    objectData = json.loads(data) 
    encodedData = encodeData(objectData, "utf-8") 
  except:
    print("Rest Server request failed.")
  return encodedData


def encodeData(input, encoding):
  '''
  Type and Description:
  ---------------------
  This user-defined function encodes unicode data to an encoding specified by 
  the argument
  
  Arguments: 
  ----------
  input (STR): contains the data to be encoded
  encoding (STR): contains the desired encoding
 
  Returns:
  --------
  input : returns encoded data
  
  '''
  if isinstance(input, dict):
      return {encodeData(key, encoding): encodeData(value, encoding)
              for key, value in input.iteritems()}
  elif isinstance(input, list):
      return [encodeData(element, encoding) for element in input]
  elif isinstance(input, unicode):
      return input.encode(encoding)
  else:
      return input

  
