'''
=========================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Machining Center
Description: This Script  handles the functioning of the Automatic Pallet Changer
(APC).
=========================================================
'''

# Libraries
# ================

from vcScript import *

'''
Global Variables: 
-----------------

comp (vcComponent): comp contains the vcComponent of the component that this script is 
contained in.

servo (vcServoController): servo conatins the VC object of the controller used for driving 
independent joints.

changeStatus (BOOL): changeStatus is the variable under conituous evaluation to call function
that causes a change in the status of the palletChanger

'''

comp = getComponent()
servo = comp.findBehaviour("APCServo")
changeStatus = False

def OnSignal(signal):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the script
  signals its value. This function manipulates changeStatus variable 
  
  Global Variables: changeStatus
  -----------------

  '''
  global changeStatus
  
  if signal.Name == "ChangeStatus":
    changeStatus = True
   

def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and is used as 
  the main function of script. This mainly calls the statusChange() function with a toStatus
  depending on the current status which is essential the opposite status as there are only
  two possible statuses.
  
  Global Variables: changeStatus
  -----------------
  
  '''
  global changeStatus
  while True:
    condition(lambda: changeStatus)
    currentStatus = comp.Status
    if currentStatus == "ASideOut":
      statusChange("BSideOut")
    elif currentStatus == "BSideOut":
      statusChange("ASideOut")
    else:
      print "Request to Change Status failed as current status is not recognized"
    

def statusChange(toStatus):
  '''
  Type and Description:
  ---------------------
  This user-defined function is responsible for driving the servocontroller to which the 
  pallet changer is connected to.
  
  Arguments: 
  ----------
  toStatus (STR): toStatus containts the desired configuration in a string.
  
  Returns: NONE 
  --------
  
  Global Variables: servo, changeStatus
  -----------------
  
  '''
  global changeStatus
  if toStatus == "ASideOut":
    servo.moveJoint(0,0)
    comp.Status = "ASideOut"
    comp.findNode("BSide").Behaviours[0].Name = "temp"
    comp.findNode("ASide").Behaviours[0].Name = comp.Name+".Changer"
    comp.findNode("BSide").Behaviours[0].Name = comp.Name+".Table"
  else:
    servo.moveJoint(0,180)
    comp.Status = "BSideOut"
    comp.findNode("ASide").Behaviours[0].Name = "temp"
    comp.findNode("BSide").Behaviours[0].Name = comp.Name+".Changer"
    comp.findNode("ASide").Behaviours[0].Name = comp.Name+".Table"
  changeStatus = False

# Properties
prop = comp.getProperty("Process_Time")
if not prop:
  prop = comp.createProperty(VC_REAL,"Process_Time",VC_PROPERTY_DEFAULT)
  prop.Value = 4
prop = comp.getProperty("Status")
if not prop:
  prop = comp.createProperty(VC_STRING,"Status",VC_PROPERTY_STEP)
  prop.StepValues=["ASideOut","BSideOut"]
  prop.Value = prop.StepValues[0]


