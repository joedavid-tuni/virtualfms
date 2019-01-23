'''
=============================================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Material Station

Description: This script handles the functioning of the Operator Door of the 
Material Station and also defines the Operator Door button for the same
=============================================================================
'''
# Libraries
# ================

from vcScript import *

# Global Variables
# ================
'''
Global Variables: 
-----------------

comp (vcComponent): comp contains the vcComponent of the component that this 
script is contained in.

servo (vcServoController): servo contains the VC object of the controller used 
for driving independent joints.

aisleRaycastPulseSignal (vcBooleanSignal): aisleRaycastPulseSignal is a boolean 
signal behaviour that activates the aisleRaycastSensor. This is necessary for
performance reasons so that the Raycast sensor close to the aisle is not active 
all the time

operateDoor (BOOL): operateDoor is the variable in continuous evaluation 
that determines whether the door closes or opens

inputContainer (vcMotiionPath) : inputContainer is a 2-way path that allows 
to contain and move pallets forward and backwards along a path defined by 
Frame Features. It serves as the conveyor in the Material Station.

operatorDoorOperateSignal (vcBooleanSignal): operatorDoorOperateSignal is a 
boolean signal behaviour that opens (TRUE) or closes (FALSE)the operator 
door.

operatorDoorDoneSignal (vcBooleanSignal): operatorDoorDoneSignal is a boolean
signal that pulses true when the opereator door has completed either opening 
or closing.

aisleDoorStatusSignal (vcBooleanSignal): aisleDoorStatusSignal is a boolean 
signal that has the current status of the aisle door, either completely 
openend (TRUE)or closed (FALSE).

'''

comp = getComponent()
servo = comp.findBehaviour('OperatorDoorServo')
inputContainer = comp.findBehavioursByType('rTwoWayPath')[0]
aisleRaycastPulseSignal = comp.findBehaviour("AisleRaycastPulse")
operateDoor = None
operatorDoorOperateSignal = comp.findBehaviour("OperatorDoorOperate")
operatorDoorDoneSignal = comp.findBehaviour("OperatorDoorDone")
aisleDoorStatusSignal = comp.findBehaviour("AisleDoorStatus")



def doorOperate(component,arrival):
  '''
  Type and Description:
  ---------------------
  This user-defined event handler is trigerred when a there's a transition of 
  any pallet to or from the component container. It manipulates the 
  operateDoor variable.
  
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
    operateDoor = True


def OnSignal( signal ):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the script
  signals its value. This function grabs incoming pallets and manipulates 
  operateDoor variable
  
  
  Global Variables: operateDoor, inputContainer
  -----------------

  '''
  global operateDoor, inputContainer

  if signal.Name == "OperatorDoorOperate" and signal.Value:
    operateDoor = True
    
  elif signal.Name == "OperatorDoorOperate" and signal.Value == False:
    operateDoor = False
    
  elif signal.Name == "OperatorRaycastSense":
    inputContainer.Enabled = False
    inputContainer.Direction = VC_PATH_BACKWARD

  elif signal.Name == "AisleRaycastSense":
    if inputContainer.Direction == VC_PATH_BACKWARD:
      inputContainer.Enabled = False
      inputContainer.Direction = VC_PATH_FORWARD
      aisleRaycastPulseSignal.signal(False)
      operateDoor = False


def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and is 
  used as the main function of script.
  
  Global Variables: operateDoor, inputContainer, servo, comp
  -----------------
  
  '''
    
  global comp, operateDoor,servo, aisleDoorStatusSignal
  
  inputContainer.OnTransition = doorOperate


  while True:

    condition(lambda: operateDoor != None and aisleDoorStatusSignal.Value == False)
    if operateDoor:                     #True to open door
      servo.moveJoint(0,1200)
      inputContainer.Direction = VC_PATH_FORWARD
      inputContainer.Enabled = True
    
    else:                                    #False to close door
      servo.moveJoint(0,0)
     
    operateDoor = None
    
    operatorDoorDoneSignal.signal(True)
    delay(0.5)
    operatorDoorDoneSignal.signal(False)
   


def OnReset():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when simulation is reset to its 
  initial state and simulation clock is set at zero.
  
  Global Variables: comp, servo, checkLoadStatus
  -----------------

  '''
  global comp, servo
  
  servo.findJoint("DoorStroke").CurrentValue = 0
  comp.rebuild()
  
  

def OCDoor(arg):
  '''
  Type and Description:
  ---------------------
  This user-defined event handler is trigerred when the OpenCloseDoor Button 
  Property is changed
  
  Global Variables: comp, servo 
  -----------------

  '''
  global comp, servo

  if servo.findJoint("DoorStroke").CurrentValue == 0:
    servo.findJoint("DoorStroke").CurrentValue = 1200
  else:
    servo.findJoint("DoorStroke").CurrentValue = 0
  comp.rebuild()


# Defining Button Property
OCButton = getComponent().getProperty("OperatorDoor")
OCButton.OnChanged = OCDoor