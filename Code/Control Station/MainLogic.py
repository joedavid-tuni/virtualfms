
'''
=============================================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Station Commander

Description: This script that pings the physical station commander and checks 
for connectivity
=============================================================================
'''
# Libraries
# ================

from vcScript import *
import os
import subprocess, platform

# Global Variables
# ===========
'''
app (vcApplication): app contains the object type for the main VC application 
that gives access to the application's GUI, commands and other common 
properties

IP (STR): IP contains the IP address of the simulator

'''
app= getApplication()
comp = getComponent()
currentAddress = getComponent().getProperty("Address").Value
IP=  currentAddress[7:-5]




def ping(host):
  '''
  Type and Description:
  ---------------------
  This user-defined function that pings the physical station commander
  
  Arguments: NONE 
  ----------
  
  Returns: NONE 
  --------
  
  Global Variables: NONE
  -----------------
 
  '''
  
  # Ping parameters as function of OS
  ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
  args = "ping " + " " + ping_str + " " + host
  need_sh = False if  platform.system().lower()=="windows" else True

  # Ping
  return subprocess.call(args, shell=need_sh) == 0



def OnStart():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred Triggered at the immediate 
  start of simulation. It pings the physical station commander and stops 
  the simulation in case its unable to communicate with it
  
  Global Variables: app, IP
  -----------------
  
  '''
  global app, IP
  
  currentAddress = getComponent().getProperty("Address").Value
  IP=  currentAddress[7:-5]

  
  if ping(IP):
    print "Successfully Connected to Station Commander"
  else:
    app.stopSimulation()
    print "Unable to Communicate to Station Commander"
    print "Things you can do"
    print "1. Check if the right IP address is selected from the 'Address' Property"
    print "    of the Station Commander in the layout. If you are in the Laboratory"
    print "    and connected to the local network it should start with 192.X.X.X"
    print "2. Check Connectivity to the Station Commander, ethernet cable or WLAN"
    print "    connection"
    
 
def buttonPing(arg):
  '''
  Type and Description:
  ---------------------
  This user-defined function that pings the physical station commander
  
  Arguments: NONE 
  ----------
  
  Returns: NONE 
  --------
  
  Global Variables: IP
  -----------------
 
  '''
  currentAddress = getComponent().getProperty("Address").Value
  IP=  currentAddress[7:-5]


  # Ping parameters as function of OS
  ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
  args = "ping " + " " + ping_str + " " + IP
  need_sh = False if  platform.system().lower()=="windows" else True

  # Ping
  result = subprocess.call(args, shell=need_sh) == 0
  
  
  if result:
    print "Station Commander can be reached successfully"
  else:
    print "Unable to contact Staion Commander"
  return 
  
  
if not ping(IP):
  print "Unable to Communicate to Station Commander in current setting"
  print "Things you can do"
  print "1. Check if the right IP address is selected from the 'Address' Property"
  print "    of the Station Commander in the layout. If you are in the Laboratory"
  print "    and connected to the local network it should start with 192.X.X.X"
  print "2. Check Connectivity to the Station Commander, ethernet cable or WLAN"
  print "    connection"
  
  
else:
  print "Station Commander reachable"
  
button = comp.getProperty("TestConnection")
if not button:
  comp.createProperty(VC_BUTTON, "TestConnection")

button.OnChanged = buttonPing