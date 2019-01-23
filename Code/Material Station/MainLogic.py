'''
=============================================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Material Station

Description: This script handles the the main functioning of the 
Material Station like signaling appropriate signals, initialization of state, 
in-voking services and so on.
=============================================================================
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

app (vcApplication): app contains the object type for the main VC application 
that gives access to the application's GUI, commands and other common 
properties

comp (vcComponent): comp contains the vcComponent of the component that this 
script is contained in.

IP (STR): IP contains the IP address of the simulator

checkLoadStatus (BOOL): checkLoadStatus checks if the pallet in the 
corresponding Loading Station is Loaded

inputContainer (vcMotiionPath) : inputContainer is a 2-way path that allows 
to contain and move pallets forward and backwards along a path defined by 
Frame Features. It serves as the conveyor in the Material Station.

ivory_ceramic, tan, darkBrown (vcMaterial): is the material used by 
geometries (pallets).

palletStatusColours (dict): palletStatusColours contains a diotionary of the 
above materials

RefNode (vcProperty): RefNode is a property whose value is the loading 
station component which determines when the pallet is loaded. For more 
details refer to thesis in comments included in the program header.

'''
app= getApplication()
comp = getComponent()
IP = app.findComponent("Station Commander").getProperty("Address").Value
checkLoadStatus = False
inputContainer = comp.findBehavioursByType('rTwoWayPath')[0]
inputContainer.Name = comp.Name + ".User"
connector = inputContainer.getConnector('Input')
ivory_ceramic= app.findMaterial("ivory_ceramic")
tan= app.findMaterial("tan")
darkBrown= app.findMaterial("material:51:Strarrag France_Angebot")
palletStatusColours = {2:"",100:ivory_ceramic,101:tan,102:darkBrown}
RefNode = comp.getProperty("RefNode")

#create RefNode Property if it doesn't exist
if not RefNode:
  comp.createProperty("Ref<Component>","RefNode")
elif RefNode.Value == None:
  print "WARN: RefNode Property of Material Station ",comp.Name, "not asisigned"

def OnStart():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred Triggered at the immediate 
  start of simulation. It updates the IP address of the station commander
  selected at the time of running for use by the component
  
  Global Variables: IP
  -----------------
  
  '''
  global IP, app, inputContainer
  IP = app.findComponent("Station Commander").getProperty("Address").Value
  inputContainer.Name = comp.Name + ".User"
  inputContainer = comp.findBehavioursByType('rTwoWayPath')[0]
  inputContainer.Direction = VC_PATH_FORWARD


def OnSignal( signal ):
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when a signal connected to the 
  script signals its value. This function grabs incoming pallets and 
  manipulates checkLoadStatus variable
  
  Global Variables: checkLoadStatus
  -----------------
  
  '''
  global checkLoadStatus, inputContainer
  
  if signal.Name == "ReceiveComponent":
    inputContainer.grab(signal.Value)
    checkLoadStatus = True
    
  elif signal.Name == "AisleRaycastSense":
    checkLoadStatus = False


def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and 
  is used as the main function of script. This function mainly calls the 
  init function on running the simulation and checks whether the 
  corresponding machine pallet on the machine station is loaded.
  
  Global Variables: checkLoadStatus, inputContainer
  -----------------
  
  '''
  global checkLoadStatus, inputContainer, app
  
  checkLoadStatus = False
  inputContainer.Speed = 5
  inputContainer.Enabled = True
  init()
  inputContainer.Enabled = False
  inputContainer.Speed = 300
  
  if RefNode.Value is not None:
  
    while True:
      
      # waits until a pallet is received to check if the pallet is Loaded
      loadingStationComp = RefNode.Value 
      condition(lambda: checkLoadStatus) 
      loadingStationContainer= loadingStationComp.findBehavioursByType(VC_CONTAINER)[0]
      
      if len(loadingStationContainer.Components)>0: # if at all there is any pallet in the corresponding Loading Station
        loadingStationPalletName= loadingStationContainer.Components[0].Name
        
        # Service Description
        servicestr = "/FMSInventoryService"
        method = "/Rest/IPalletManagementApi/GetPalletDetails"
        params = '{"ids":["'+loadingStationPalletName+'"]}'
        url = IP + servicestr + method
        
        response = restQuery(url,params)
         
        # If there's a pallet in the corresponding Loading Station
        if len(response['Data'])>0: 
          status = response['Data'][0]['Status']
          
          # if pallet is on-route (after loading) or idle (after unloading)
          if status ==1 or status ==4:
            inputContainer.Direction = VC_PATH_BACKWARD
            inputContainer.Enabled = True
            aisleRaycastPulseSignal = comp.findBehaviour("AisleRaycastPulse")
            aisleRaycastPulseSignal.signal(True)
            
      delay(0.2)
      
  else:
    print "No Reference Node for ", comp.Name


def init():
  '''
  Type and Description:
  ---------------------
  This user-defined function that initialises the station to its current 
  state, For e.g. transfer of pallets.
  
  Arguments: NONE 
  ----------
  
  Returns: NONE 
  --------
  
  Global Variables: checkLoadStatus, inputContainer, palletStatusColours
  -----------------
 
  '''
  global checkLoadStatus, inputContainer, palletStatusColours
  
  # fetching required service
  servicestr = "/PalletService"
  method = "/Rest/IDevicePalletDataApi/GetLocationPalletSummaries"
  params = '{"deviceName":"'+comp.Name+'","locationNames":["'+inputContainer.Name+'"]}'
  url = IP + servicestr + method
  response = restQuery(url,params)
    
  if len(response['Data']) > 0:
      checkLoadStatus = True
      # storing required information from response
      palletType = response['Data'][0]['PalletType']
      palletNumber = response['Data'][0]['Number']
      palletId = response['Data'][0]['Id']
      palletStatus = response['Data'][0]['Status']
      palletName = palletType +'.'+ palletNumber
      
      # searching for component
      pallet = app.findComponent(palletId)
  
      # transferring component if it exisits in the 3D world
      if pallet is not None:
        
        connector = inputContainer.getConnector('Input')
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
        connector = inputContainer.getConnector('Input')
        newPallet.transfer(connector)
        
        # Assiging Visual Labels for the Pallet
        if palletType=="MaterialPallet":
          newPallet.getFeature("Text").Text = '"'+palletType+palletNumber+'"'
        elif palletType=="MachinePallet":
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
  encodedData (DICT): contains encoded Object response from the simulator
  
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
  This user-defined function encodes unicode data to an encoding specified 
  by the argument (utf-8)
  
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


