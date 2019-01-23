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

servo (vcServoController): servo conatins the VC object of the controller 
used for driving independent joints.

inputContainer (vcMotiionPath) : inputContainer is a 2-way path that allows 
to conatin and move pallets forward and backwards along a path defined by 
Frame Features. It serves as the conveyorin the Material Station.

operateDoor (BOOL): operateDoor is the variable in continuous evaluation that
determines whether the door closes or opens

aisleDoorOperateSignal (vcBooleanSignal): aisleDoorOperateSignal is a boolean
signal behaviour that opens (TRUE) or closes (FALSE)the aisle door.

aisleDoorDoneSignal (vcBooleanSignal): aisleDoorDoneSignal is a boolean signal
that pulses true when the aisle door has completed either opening or closing.

aisleDoorStatusSignal (vcBooleanSignal): aisleDoorStatusSignal is a boolean 
signal that has the current status of the aisle door, either completely 
openend (TRUE)or closed (FALSE).

'''
comp = getComponent()
servo = comp.findBehaviour('AisleDoorServo')
inputContainer = comp.findBehavioursByType('rTwoWayPath')[0]
operateDoor = None
aisleDoorOperateSignal = comp.findBehaviour("AisleDoorOperate")
aisleDoorDoneSignal = comp.findBehaviour("AisleDoorDone")
aisleDoorStatusSignal  = comp.findBehaviour("AisleDoorStatus")

def doorOperate(component,arrival):
  '''
  Type and Description:
  ---------------------
  This user-defined event handler is trigerred when a there's a transition of
  any pallet to or from the component container. It manipulates the 
  operateDoor variable.
  
  Arguments:  
  ----------
  component (vcComponent):  component is the component that has been 
  transferred
  arrival (BOOL): arrival is TRUE if the component has arrived to the 
  container or False if the component has departed.
  
  Returns: NONE 
  --------
  
  Global Variables: operateDoor 
  -----------------
  
  '''
  
  global operateDoor, aisleDoorOperateSignal
  if arrival:
    operateDoor = False
    aisleDoorOperateSignal.signal(False)
    

def OnSignal( signal ):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the 
  script signals its value. This function grabs incoming pallets and 
  manipulates operateDoor variable
  
  Global Variables: operateDoor
  -----------------

  '''
  global operateDoor 
    
  if signal.Name == "AisleDoorOperate" and signal.Value:
    operateDoor = True
  elif signal.Name == "AisleDoorOperate" and signal.Value == False:
    operateDoor = False
  elif signal.Name == "AisleRaycastSense":
    operateDoor = True


def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and 
  is used as the main function of script.
  
  Global Variables: operateDoor, inputContainer, servo, comp
  -----------------
  
  '''
  global operateDoor,servo
    
  inputContainer.OnTransition = doorOperate
 
  while True:
    
    condition(lambda: operateDoor != None)
    
    if operateDoor:         # True to open door
      servo.moveJoint(0,1200)
      aisleDoorStatusSignal.signal(True)
      
      # If operateDoor has not changed during the time it was moving the Joint
      if operateDoor:       
        operateDoor = None
    else:                   # False to close door
      servo.moveJoint(0,0)
      aisleDoorStatusSignal.signal(False)
      
      if not operateDoor:   
        operateDoor = None
    
    # signal that the door completed current operation
    aisleDoorDoneSignal.signal(True)
    delay(0.5)
    aisleDoorDoneSignal.signal(False)
   

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
  servo.findJoint("BDoorStroke").CurrentValue = 0
  comp.rebuild()
  

def OC_Door(arg):
  '''
  Type and Description:
  ---------------------
  This user-defined event handler is invoked whent he AisleDoor Buttin is 
  present and mainly toggles between opening and closing the door
  
  Global Variables: comp, servo
  -----------------

  '''
  global comp, servo
  if servo.findJoint("BDoorStroke").CurrentValue == 0:
    servo.findJoint("BDoorStroke").CurrentValue = 1200
  else:
    servo.findJoint("BDoorStroke").CurrentValue = 0
  comp.rebuild()

# Define Button Property
OC_button = getComponent().getProperty("AisleDoor")
OC_button.OnChanged = OC_Door
