'''
=========================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Machining Center
Connections: 
Description: This python script handles the scheduling of tasks for the Machining Center
=========================================================
'''

# Libraries
# ================

from vcScript import *
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

initComplete (vcBooleanSignal): initComplete is a boolean signal signals that initialization of
the machine center is complete

previousProgram (DICT): previousProgram contains the previously executed program by the machine
center

previousProgramStatus (DICT): previousProgramStatus contains the status of the previous program

machineNumber (STR): machineNumber is the instance number of the component in the layout which 
is dervied from the component name. This is necessary while calling the RESTful services

'''
app= getApplication()
comp = getComponent()
IP = app.findComponent("Station Commander").getProperty("Address").Value
addTaskSignal = comp.findBehaviour("AddTask")
initComplete = False
previousProgram = None
previousProgramStatus = None
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


def OnSignal( signal ):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the script
  signals its value. This function manipulates initComplete variable 
  
  Global Variables: initComplete
  -----------------

  '''
  global initComplete
  if signal.Name == "InitComplete" and signal.Value:
    initComplete = True
  elif signal.Name == "InitComplete" and not signal.Value:
    initComplete = False
  pass


def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and is used as 
  the main function of script. This mainly calls the checkForActiveProgram() function 
  once intialization is complete
  
  Global Variables: changeStatus
  -----------------
  
  '''
  global initComplete
  
  while True:
    
    condition(lambda: initComplete == True)
    checkForActiveProgram()
    delay(0.2)


def checkForActiveProgram():
  
  '''
  Type and Description:
  ---------------------
  This user=defined function checks for the currently active program and stores is it
  as tasks to be done.
  
  Global Variables: previousProgram, previousProgramStatus, addTaskSignal
  -----------------
  
  '''
  
  global previousProgram, previousProgramStatus, addTaskSignal
  
  #Service Description
  servicestr = "/Machine"+machineNumber+"Service"
  method = "/Rest/IMachineStatusApi/GetActiveProgram"
  url = IP + servicestr + method
  
  response = restQuery(url,"")
  
  currentProgram =  response['Data']['Name']
  currentProgramStatus =  response['Data']['Status']
  
  if currentProgram != previousProgram or  currentProgramStatus != previousProgramStatus:
    previousProgram = currentProgram
    previousProgramStatus = currentProgramStatus
    
    if currentProgramStatus == 4:
      addTaskSignal.signal(currentProgram)

    
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
