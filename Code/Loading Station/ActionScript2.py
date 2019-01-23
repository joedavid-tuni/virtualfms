'''
=========================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Loading Station
Connections: 
Description:  This script handles the functioning of the 
Operator Door of the Loading Station and also defines the 
Aisle Door button for the same
=========================================================
'''
# Libraries
# ================

from vcScript import *

# Global Variables
# ================
'''
Global Variables: 
-----------------

comp (vcComponent): comp contains the vcComponent of the component that this script is 
contained in.

servo (vcServoController): servo conatins the VC object of the controller used for driving 
independent joints.

operateDoor (BOOL): operateDoor is the variable in continuous evaluation that determines whether
the door closes or opens

container (vcContainer) : inputContainer is a component container used for simulating buffer or 
storage area to contain pallets

operatorDoorOperateSignal (vcBooleanSignal): operatorDoorOperateSignal is a boolean signal behaviour
that opens (TRUE) or closes (FALSE)the operator door.

operatorDoorDoneSignal (vcBooleanSignal): operatorDoorDoneSignal is a boolean signal that pulses true
when the opereator door has completed either opening or closing.

aisleDoorStatusSignal (vcBooleanSignal): aisleDoorStatusSignal is a boolean signal that has the 
current status of the aisle door, either completely openend (TRUE)or closed (FALSE).

'''

comp = getComponent()
servo = comp.findBehaviour('OperatorDoorServo')
operateDoor = None
container = comp.findBehavioursByType(VC_CONTAINER)[0]
operatorDoorOperateSignal = comp.findBehaviour("OperatorDoorOperate")
operatorDoorDoneSignal = comp.findBehaviour("OperatorDoorDone")
aisleDoorStatusSignal = comp.findBehaviour("AisleDoorStatus")


def doorOperate(component, arrival):
  '''
  Type and Description:
  ---------------------
  This user-defined event handler is trigerred when a there's a transition of any 
  pallet to or from the component container. It manipulates the operateDoor variable.
  
  Arguments:  
  ----------
  component (vcComponent): component is the component that has been transferred
  arrival (BOOL): arrival is TRUE if the component has arrived to the container
  or False if the component has departed.
  
  Returns: NONE 
  --------
  
  Global Variables: operateDoor 
  -----------------
  
  '''
  global operateDoor
  
  if arrival:
    operateDoor= True
  

def OnSignal( signal ):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the script
  signals its value. This function manipulates operateDoor variable
  
  
  Global Variables: operateDoor, inputContainer
  -----------------

  '''
  global operateDoor 
  
  if signal.Name == "OperatorDoorOperate" and signal.Value:
    operateDoor = True
  elif signal.Name == "OperatorDoorOperate" and signal.Value == False:
    operateDoor = False


def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and is used as 
  the main function of script. It continuously monitors the operateDoor variable and
  opens (TRUE) or closes (False) the door depending on its value
  
  Global Variables: operateDoor, container, servo
  -----------------
  
  '''
  global operateDoor,servo, container, operatorDoorDoneSignal
    
  container.OnTransition = doorOperate
   
  while True:
    condition(lambda: operateDoor != None and aisleDoorStatusSignal.Value == False)
    
    if operateDoor:                     # True to open door
      servo.moveJoint(0,60)
    
    else:                               # False to close door
      servo.moveJoint(0,0)
    
    operateDoor = None
    operatorDoorDoneSignal.signal(True)
    delay(0.5)
    operatorDoorDoneSignal.signal(False)
    
 
def OCDoor(arg):
  '''
  Type and Description:
  ---------------------
  This user-defined event handler is invoked whent he OperatorDoor Button is present and
  mainly toggles between opening and closing the door
  
  Global Variables: comp, servo
  -----------------

  '''
  
  comp.rebuild()
  if servo.getJointValue(0)==60:
    servo.moveImmediate(0)
    
  else:
    servo.moveImmediate(60)



# Define Button Property
OC_button = getComponent().getProperty("OperatorDoor")
OC_button.OnChanged = OCDoor