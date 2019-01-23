'''
=============================================================================
Author: Joe David (joe.david@tut.fi)
Date: 21.09.2018
Language: Stackless Python v2.7.1
Version: 1.0

Component: Crane Storage

Description: This script handles the functioning of the Crane Storage by
initialization of state by creation and transfer of pallets
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

app (vcApplication): app contains the object type for the main VC application 
that gives access to the application's GUI, commands and other common 
properties

comp (vcComponent): comp contains the vcComponent of the component that this 
script is contained in.

IP (STR): IP contains the IP address of the simulator

ivory_ceramic, tan, darkBrown (vcMaterial): is the material used by 
geometries (pallets).

palletStatusColours (dict): palletStatusColours contains a diotionary of the 
above materials

'''


app= getApplication()
comp = getComponent()
IP = app.findComponent("Station Commander").getProperty("Address").Value
#print comp.findBehaviour("Crane.Storage.2").getConnector('Input').Index

ivory_ceramic= app.findMaterial("ivory_ceramic")
tan= app.findMaterial("tan")
darkBrown= app.findMaterial("material:51:Strarrag France_Angebot")
palletStatusColours = {2:"",100:ivory_ceramic,101:tan,102:darkBrown}


def createPallets(pallets):
  '''
  Type and Description:
  ---------------------
  This user-defined function creates the pallets and transfers them to the
  crane storage.
  
  Arguments:  
  ----------
  palletDetails (DICT): palletDetails contains a dictionary of the details of 
  the pallet to be created
  
  Returns: NONE 
  --------
  
  Global Variables: app, comp
  -----------------
 
  '''
  global app , comp
  
  for pallet in pallets:
  
    palletNumber = pallet['Number']
    palletType = pallet['PalletType']
    palletCurrentLocation = pallet['CurrentLocation']
    palletStatus = pallet['Status']
    palletId = pallet['Id']
    palletName = palletType+'.'+palletNumber

    
    if palletCurrentLocation.startswith("Crane.Storage"):
    # Setting Template (either Machine or Material Pallet)
      template = app.findComponent(palletType)
        
      #Creating a New Pallet  
      newPallet=template.clone(0)

      # Creating Id Property and assigning Fastems Pallet ID and Setting Name
      id = newPallet.createProperty(VC_STRING,"HRName")
      id.Value= str(palletName)
      newPallet.Name = palletId
     
      # Transferring Pallet to appropriate Storage Location
      
      storageLocation = comp.findBehaviour(palletCurrentLocation)
      connectorIndex = storageLocation.getConnector('Input').Index
      newPallet.transferNonBlocking(storageLocation,connectorIndex)
      
      # Assiging Visual Labels for the Pallets
      text = newPallet.getFeature("Text")
      if palletType=="MaterialPallet":
        text.Text = '"'+palletType+palletNumber+'"'
      elif palletType.startswith("MachinePallet"):
        text.Text= '"'+palletNumber+'"'
     
      # Assigning Status Colours to the Pallets
      if palletType == "MaterialPallet":
        collar1 = newPallet.findFeature("Block")
        collar2 = newPallet.findFeature("Block_10")
        collar1.Material = palletStatusColours[palletStatus]
        collar2.Material = palletStatusColours[palletStatus]
      # Rebuild  
      newPallet.rebuild()

  return
  
def deletePallet(palletDetails):
  '''
  Type and Description:
  ---------------------
  This user-defined function delets a pallet from the 3D world
  
  Arguments:  
  ----------
  palletDetails (DICT): palletDetails contains a dictionary of all the pallets
  returned as a response from the simualtor
  
  Returns: NONE 
  --------
  
  Global Variables: app, comp
  -----------------
 
  '''
  palletId = palletDetails['Id']
  pallet = app.findComponent(palletId)
  app.deleteComponent(pallet)
  return
  
def OnReset():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred when simulation is reset to its 
  initial state and simulation clock is set at zero. It deletes all the pallets
  so that the layout is ready for the next time when the pallets are
  created
  
  Global Variables: IP, app
  -----------------
  
  '''
  servicestr = "/FMSInventoryService"
  method = "/Rest/IPalletManagementApi/GetInventoryPallets"
  url = IP + servicestr + method
  data  = '{"ids":null}'
  
  response = restQuery(url,data)
  
  pallets = response['Data']
  for pallet in pallets:
    deletePallet(pallet)


def OnStart():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred  at the immediate 
  start of simulation. It updates the IP address of the station commander
  selected at the time of running for use by the component
  
  Global Variables: IP, app
  -----------------
  
  '''
  global IP, app
  IP = app.findComponent("Station Commander").getProperty("Address").Value
  
  
def OnRun():
  '''
  Type and Description:
  ---------------------
  This built-in event handler is trigerred at the start of a simulation and 
  is used as the main function of script. This function mainly creates the
  pallets by calling the createPallets() function
  
  '''
  
  servicestr = "/FMSInventoryService"
  method = "/Rest/IPalletManagementApi/GetInventoryPallets"
  url = IP + servicestr + method
  data  = '{"ids":null}'
  
  response = restQuery(url,data)
  
  pallets = response['Data']
  
  createPallets(pallets)
  

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

