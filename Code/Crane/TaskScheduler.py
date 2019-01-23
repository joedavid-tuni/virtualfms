
'''
===================================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Crane
Description: This script acts as the task scheduler obtaining tasks
real-time from the simulator and scheduling it for the crane in VC
===================================================================
'''

# Libraries
# ================

from vcScript import *
import urllib2
import json


# Global Variables
# ================
'''
'''
tasks = {}
doneTasks = []
comp = getComponent()
app = getApplication()
addTaskSignal =  comp.findBehaviour("AddTask")
IP = app.findComponent("Station Commander").getProperty("Address").Value
doneTaskIds = []


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
  global IP
  IP = app.findComponent("Station Commander").getProperty("Address").Value


def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and is used as the 
  main function of script. It mainly checks for the current tasks real-time and signals it 
  to the MainLogic 
  
  Global Variables:  tasks
  -----------------
  
  '''
  global tasks, doneTaskIds
  
  #Service Description
  servicestr = "/CraneTransportService"
  method = "/Rest/ICraneTransportApi/GetTransportTasks"
  url = IP + servicestr + method

  while True:
    response = restQuery(url, "")
    activeTasks = response['Data']['ActiveTasks']
    noOfActiveTasks = len(activeTasks)
    
    if noOfActiveTasks > 0:
      
      for activeTask in activeTasks:
        activeTaskId = activeTask['Id']
        
        if activeTask['Priority'] == 9999 and not activeTaskId in doneTaskIds:
          
          # Filtering function
          if not activeTaskId in tasks:
            tasks[activeTaskId] = "Bogus Task"
          elif activeTaskId in tasks and tasks [activeTaskId] == "Bogus Task":
            tasks[activeTaskId] = activeTask
            doneTaskIds.append(activeTaskId)
    
    if tasks:
      
      for taskID, task in tasks.items():
        if isinstance(task,dict): #if not Bogus Task
          addTaskSignal.signal(str(task))  
          del tasks[taskID]

    delay(0.2)


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
  except Exception as e:
    print("Rest Server request failed.")
    print e
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
