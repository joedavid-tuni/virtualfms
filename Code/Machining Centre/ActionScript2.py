'''
=========================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Machining Center
Connections: 
Description: This python script that handles the functioning of the (Aisle) Door.
=========================================================
'''

# Libraries
# ================

from vcScript import *

# Global Variables
# ================
'''
Global Variables: 

comp (vcComponent): comp contains the vcComponent of the component that this script is 
contained in.

doorServo (vcServoController): servo conatins the VC object of the controller used for driving 
the door of the Machine Centre.

aisleDoorDoneSignal (vcBooleanSignal): aisleDoorDoneSignal is a boolean signal that pulses true
when the aisle door has completed either opening or closing.

door (BOOL/None) = door is the variable under continuous evaluation that drives its opening or 
closing.
'''

comp = getComponent()
doorServo = comp.findBehaviour("DoorServo")
aisleDoorDoneSignal = comp.findBehaviour("AisleDoorDone")
door = None


def OnSignal( signal ):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the script signals its 
  value. This function manipulates door variable to cause its opening (TRUE) or closing (FALSE)
  
  Global Variables: door
  -----------------

  '''
  global door
  if signal.Name == "AisleDoorOperate" and signal.Value:
    door = True
  elif signal.Name == "AisleDoorOperate" and not signal.Value:
    door = False
  pass

def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and is used as 
  the main function of script. It mainly calls the driveDoor() function with appropriate 
  argument to cause its closing or opening depedning on the value of the door variable
  
  Global Variables: door, aisleDoorDoneSignal
  -----------------
  
  '''
  global door, aisleDoorDoneSignal
  
  
  while True:
    condition(lambda: door !=None)
    if door:
      driveDoor("Open")
    else:
      driveDoor("Close")
      
    aisleDoorDoneSignal.signal(True)
    delay(0.5)
    aisleDoorDoneSignal.signal(False) 
  


def driveDoor(operation):
  '''
  Type and Description:
  ---------------------
  This user-defined function that drives the servocontroller which operates the door of the 
  machine center ancd manipulates the door variable once its done.
  
  Arguemnts:  
  --------
  
  operation (STR) : contains the desired operation, either open or close in a string
  
  Returns: NONE 
  --------
  
  Global Variables: door, doorServo
  -----------------
  
  '''
  
  global door, doorServo
    
  if operation == "Open":
    doorServo.moveJoint(0,-35)
    doorServo.moveJoint(0,-35)
  else:
    doorServo.moveJoint(0,0)
    doorServo.moveJoint(0,0)
  door = None
  
