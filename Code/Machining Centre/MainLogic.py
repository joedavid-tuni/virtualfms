'''
=========================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Machining Center
Connections: 
Description: This python script that functions as the main script of the 
Machining Center and takes care of its initialization and executing tasks.
=========================================================
'''

# Libraries
# ================

from vcScript import *
import xml.etree.ElementTree as ET
import urllib2
import json

# Global Variables
# ================
'''
Global Variables: 
-----------------

app (vcApplication): app contains the object type for the main VC application that gives access 
to the application's GUI, commands and other common properties

comp (vcComponent): comp contains the vcComponent of the component that this script is 
contained in.

IP (STR): IP contains the IP address of the simulator

servo (vcServoController): servo conatins the VC object of the servocontroller that drives the
pallet changer

changeStatusSignal (vcBooleanSignal): changeStatus signal defines a boolean signal that causes
a change in the pallet changer configuration

doorSignal (vcBooleanSignal): doorSignal signal defines a boolean signal that causes the aisle 
door to open or close

tasks (ARR): tasks is an array that contains all the tasks to be done by the Machine Center

receiveComponent (vcComponentSignal): receiveComponent is a component signal that signals that 
a component(pallet) has been placed in the machine center

machineNumber (STR): machineNumber is the instance number of the component in the layout which 
is dervied from the component name. This is necessary while calling the RESTful services

'''

app= getApplication()
comp = getComponent()
IP = app.findComponent("Station Commander").getProperty("Address").Value
servo = comp.findBehaviour("APCServo")
changeStatusSignal = comp.findBehaviour("ChangeStatus")
doorSignal = comp.findBehaviour("AisleDoorOperate")
tasks = []
receiveComponent = False
machineNumber = ""

for char in comp.Name:
  if char.isdigit():
    machineNumber = machineNumber + char

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
  global IP, machineNumber
  temp = ""
  IP = app.findComponent("Station Commander").getProperty("Address").Value
  for char in comp.Name:
    if char.isdigit():
      temp = temp + char
  machineNumber = temp

def initState():
  '''
  Type and Description:
  ---------------------
  This user-defined function that initialises the status of the pallet changer which 
  can be one of two configurations, either "ASideOut" or "BSideOut"
  
  Arguments: NONE 
  ----------
  
  Returns: NONE 
  --------
  
  Global Variables: comp, servo
  -----------------
 
  '''
  
  servicestr = "/Machine"+machineNumber+"TransportService"
  method = "/Rest/IRotatingChangerApi/GetChangerData"
  url = IP + servicestr + method
  response = restQuery(url,"")
  
  if response['Data']['LastHandledStatus'] == 1:
    servo.moveImmediate(0)
    comp.Status = "ASideOut"
  
  elif  response['Data']['LastHandledStatus'] == 2:
    servo.moveImmediate(180)
    comp.Status = "BSideOut"
    ASide = comp.findNode("ASide")
    BSide = comp.findNode("BSide")

    ASide.Behaviours[0].Name = "temp"
    BSide.Behaviours[0].Name = comp.Name+".Changer"
    ASide.Behaviours[0].Name = comp.Name+".Table"
    
  elif response['Data']['LastHandledStatus'] == 3:
    print "Waiting for rotation to complete"
    delay(5)
    initState()
  else:
    print "Unknown Pallet Changer Configuration"

def OnReset():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when simulation is reset to its initial state 
  and simulation clock is set at zero. It mainly reverts the pallet changer configuraiton
  to its default state.
  
  Global Variables: comp, servo
  -----------------
    
  '''
  servo.moveImmediate(0)
  comp.Status = "ASideOut"
  ASide = comp.findNode("ASide")
  BSide = comp.findNode("BSide")
  BSide.Behaviours[0].Name = "temp"
  ASide.Behaviours[0].Name = comp.Name+".Changer"
  BSide.Behaviours[0].Name = comp.Name+".Table"

def OnSignal(signal):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the script signals its value. 
  This function addsTask, grabs components placed at its container.
  
  Global Variables: comp, inputContainer
  -----------------
  
  '''
  global receiveComponent, tasks
  
  if signal.Name == "AddTask":
    tasks.append(signal.Value)
    
  elif signal.Name == "ReceiveComponent":
    receiveComponent == True
    inputContainer = comp.findBehaviour(comp.Name+".Changer")
    inputContainer.grab(signal.Value)
    


def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and is used as the 
  main function of script.
  
  Global Variables: tasks,  receiveComponent, doorSignal, changeStatusSignal
  -----------------
  
  '''
  global tasks, receiveComponent, doorSignal,changeStatusSignal
  
  doorSignal = comp.findBehaviour("AisleDoorOperate")
  del tasks[:]
  initState()
  init()
  initSignal = comp.findBehaviour("InitComplete")
  initSignal.signal(True)
  while True:
    changer = comp.findBehaviour(comp.Name+".Changer")
    table = comp.findBehaviour(comp.Name+".Table")
    condition(lambda: changer.ComponentCount or table.ComponentCount)
    condition(lambda: tasks)
    delay(1)
    task = tasks.pop(0)
    if task == "PalletChange.nc":
      changer = comp.findBehaviour(comp.Name+".Changer")
      condition(lambda: changer.ComponentCount or table.ComponentCount)
      changeStatusSignal.signal(True)
      doorSignal.signal(False)
      delay(0.5)
      changeStatusSignal.signal(False)
      task = None


def init():
  '''
  Type and Description:
  ---------------------
  This user-defined function that initialises the station to its current state, For e.g.
  transfer of pallets.
  
  Arguments: NONE 
  ----------
  
  Returns: NONE 
  --------
  
  Global Variables: comp, app, checkLoadStatus
  -----------------
 
  '''
  global comp, app
  
  containerName1 = comp.findBehavioursByType(VC_COMPONENTCONTAINER)[0].Name
  containerName2 = comp.findBehavioursByType(VC_COMPONENTCONTAINER)[1].Name
  
  # fetching required service
  servicestr = "/PalletService"
  method = "/Rest/IDevicePalletDataApi/GetLocationPalletSummaries"
  params = '{"deviceName":"'+comp.Name+'","locationNames":["'+containerName1+'","'+containerName2+'"]}'
  url = IP + servicestr + method
  response = restQuery(url,params)
    
  for response in response['Data']:

      # storing required information from response
      palletType = response['PalletType']
      palletNumber = response['Number']
      palletId = response['Id']
      palletStatus = response['Status']
      palletCurrentLocation  = response['CurrentLocation']
      #print palletCurrentLocation
      palletName = palletType +'.'+ palletNumber
      
      # searching for component
      pallet = app.findComponent(palletId)
  
      # transferring component if it exisits in the 3D world
      if pallet is not None:
        
        connector = comp.findBehaviour(palletCurrentLocation).getConnector('Input')
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
        connector = comp.findBehaviour(palletCurrentLocation).getConnector('Input')
        newPallet.transfer(connector)
        
        # Assiging Visual Labels for the Pallet
        if palletType=="MaterialPallet":
          newPallet.getFeature("Text").Text = '"'+palletType+palletNumber+'"'
        elif palletType.startswith("MachinePallet"):
          newPallet.getFeature("Text").Text= '"'+palletNumber+'"'
         
        # Assigning Status Colours to the Pallets
        if palletType == "MaterialPallet":
          collar1 = newPallet.findFeature("Block")
          collar2 = newPallet.findFeature("Block_10")
          collar1.Material = palletStatusColours[palletStatus]
          collar2.Material = palletStatusColours[palletStatus]
        newPallet.rebuild()


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

