'''
=========================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Loading Station
Description:  This script handles the functioning of the 
Aisle Door of the Loading Station and also defines the 
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

aisleDoorOperateSignal (vcBooleanSignal): aisleDoorOperateSignal is a boolean signal behaviour
that opens (TRUE) or closes (FALSE)the aisle door.

aisleDoorDoneSignal (vcBooleanSignal): aisleDoorDoneSignal is a boolean signal that pulses true
when the aisle door has completed either opening or closing.

aisleDoorStatusSignal (vcBooleanSignal): aisleDoorStatusSignal is a boolean signal that has the 
current status of the aisle door, either completely openend (TRUE)or closed (FALSE).


'''

comp = getComponent()
servo = comp.findBehaviour('AisleDoorServo')
operateDoor = None
container = comp.findBehavioursByType(VC_CONTAINER)[0]
aisleDoorOperateSignal = comp.findBehaviour("AisleDoorOperate")
aisleDoorDoneSignal = comp.findBehaviour("AisleDoorDone")
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
  global operateDoor, aisleDoorOperateSignal
  
  if arrival:
    aisleDoorOperateSignal.signal(False)

 

def driveDoor(operation):
  '''
  Type and Description:
  ---------------------
  This user-defined function opens or closes the aisle door depending on the value
  of the operation argument
  
  Arguments:  
  ----------
  operataion (STR): operation contains the string, either "open" or "close" to perform
  opening or closing of the aisle door respectievely 
  
  Returns: True if the function receives to achieve a state that its already in 
  --------
  
  Global Variables: comp, operateDoor, servo, aisleDoorStatusSignal
  -----------------
  '''
  global comp, servo, aisleDoorStatusSignal
  
  dcount = comp.getProperty('dcount')
  CloneFeat = comp.findFeature('Panel Clone')
  DoorHeight = comp.getProperty("DoorHeight")
  FloorGap = comp.getProperty('FloorGap')
  LSF_Height = comp.getProperty("LSF_Height")
  DoorHeight =  LSF_Height.Value-555
  stepsReal = DoorHeight/120
  steps = int(stepsReal)
 
  if operation == "open":
    increment = -120
    count = -1
  else:
    increment = 120
    count = 1
    if servo.getJointValue(0) > 0:
      Stroke = servo.getJointValue(0)
      stepsReal = (DoorHeight-Stroke)/120
      steps = int(stepsReal)
  
  if operation == "open" and servo.getJointValue(0) == 0:
    delay(0.5)
    return True
  elif operation == "close" and servo.getJointValue(0) == stepsReal*abs(increment):
    delay(0.5)
    return True

  position =  servo.getJointValue(0)
  
  for i in range(steps):
    
    if count >0:
      servo.moveJoint(0,position+increment)
      dcount.Value = dcount.Value +count
      CloneFeat.rebuild()
   
    else:
      dcount.Value = dcount.Value +count
      CloneFeat.rebuild()
      servo.moveJoint(0,position+increment)
      
    position =  servo.getJointValue(0)
    
  if operation == "open":
    aisleDoorStatusSignal.signal(True)
    
  else:
    aisleDoorStatusSignal.signal(False)
  LastIncrement =  (stepsReal-steps)*increment
  servo.moveJoint(0,position+LastIncrement)


def OnSignal( signal ):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the script
  signals its value. THis function manipulates the operateDoor variable that is
  in coninuous evalution in the OnRun event-handler
  
  
  Global Variables: operateDoor, inputContainer
  -----------------

  '''
  global operateDoor 
    
  if signal.Name == "AisleDoorOperate" and signal.Value:
    operateDoor = True
  elif signal.Name == "AisleDoorOperate" and signal.Value == False:
    operateDoor = False


def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and is used as the 
  main function of script.
  
  Global Variables: container, aisleDoorOperateSignal, aisleDoorDoneSignal
  -----------------
  
  '''
  global operateDoor 
  
  operateDoor= None
  
  container.OnTransition = doorOperate

  while True:
    condition(lambda: operateDoor != None)
    if operateDoor:                       # True to open door
      driveDoor("open")
      
      if operateDoor:
        operateDoor = None                # If operateDoor has not changed during the time it was moving the Joint
        
    else:                                 # False to close door
      driveDoor("close")
      
      if not operateDoor:                 # If operateDoor has not changed during the time it was moving the Joint
        operateDoor = None
    
    # signal that the door completed current operation
    aisleDoorDoneSignal.signal(True)
    delay(0.5)
    aisleDoorDoneSignal.signal(False)


def OnReset():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when simulation is reset to its initial 
  state and simulation clock is set at zero.
  
  Global Variables: comp, servo, checkLoadStatus
  -----------------

  '''
  global comp, servo
  
  dcount = getComponent().getProperty('dcount')
  CloneFeat = comp.findFeature('Panel Clone')

  LSF_Height = comp.getProperty("LSF_Height")
  DoorHeight =  LSF_Height.Value-555
 
  steps = int( (servo.findJoint("DoorStroke").CurrentValue)/120)
  dcount.Value = steps+1

  comp.rebuild()

def OCDoor(arg):
  '''
  Type and Description:
  ---------------------
  This user-defined event handler is invoked whent he AisleDoor Buttin is present and
  mainly toggles between opening and closing the door
  
  Global Variables: comp, servo
  -----------------

  '''
  
  FloorFrames = comp.getProperty("FloorFrames")
  LSF_Height = comp.getProperty("LSF_Height")
  dcount = comp.getProperty('dcount')
  Add_RYLOStroke = comp.getProperty('Options::Add_RYLOStroke')
  CloneFeat = comp.findFeature('Panel Clone')
  DoorHeight =  LSF_Height.Value-555
  stepsReal = DoorHeight/120
  steps = int(stepsReal)
  
  if servo.findJoint("DoorStroke").CurrentValue == 0:
    servo.findJoint("DoorStroke").CurrentValue = stepsReal*120
    dcount.Value = steps+1
  else:
    servo.findJoint("DoorStroke").CurrentValue = 0
    dcount.Value = 1
  
  comp.rebuild()

# Define Button Property
OC_button = getComponent().getProperty("AisleDoor")
OC_button.OnChanged = OCDoor





