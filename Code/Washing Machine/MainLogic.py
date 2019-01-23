from vcScript import *
import urllib2
import json
comp = getComponent()
app= getApplication()
inputContainer = comp.findBehavioursByType(VC_COMPONENTCONTAINER)[0]
IP = app.findComponent("Station Commander").getProperty("Address").Value

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
  global IP, machineNumber
  temp = ""
  IP = app.findComponent("Station Commander").getProperty("Address").Value

def OnSignal( signal ):
  if signal.Name == "ReceiveComponent":
    inputContainer.grab(signal.Value)

def OnRun():
  init()
  pass


def init():
  '''
  Type and Description:
  ---------------------
  This user-defined function that initialises the station to its current state, For e.g.
  transfer of pallets.
  
  Arguments: NONE 
  ----------
  
  Returns: NONE 
  --------
  
  Global Variables: comp, app, checkLoadStatus
  -----------------
 
  '''
  global comp, app
  
  containerName = comp.findBehavioursByType(VC_COMPONENTCONTAINER)[0].Name

  
  # fetching required service
  servicestr = "/PalletService"
  method = "/Rest/IDevicePalletDataApi/GetLocationPalletSummaries"
  params = '{"deviceName":"'+comp.Name+'","locationNames":["'+containerName+'"]}'
  url = IP + servicestr + method
  
  response = restQuery(url,params)
  
    
  for response in response['Data']:

      # storing required information from response
      palletType = response['PalletType']
      palletNumber = response['Number']
      palletId = response['Id']
      palletStatus = response['Status']
      palletCurrentLocation  = response['CurrentLocation']
      #print palletCurrentLocation
      palletName = palletType +'.'+ palletNumber
      
      # searching for component
      pallet = app.findComponent(palletId)
  
      # transferring component if it exisits in the 3D world
      if pallet is not None:
        
        connector = comp.findBehaviour(palletCurrentLocation).getConnector('Input')
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
        connector = comp.findBehaviour(palletCurrentLocation).getConnector('Input')
        newPallet.transfer(connector)
        
        # Assiging Visual Labels for the Pallet
        if palletType=="MaterialPallet":
          newPallet.getFeature("Text").Text = '"'+palletType+palletNumber+'"'
        elif palletType.startswith("MachinePallet"):
          newPallet.getFeature("Text").Text= '"'+palletNumber+'"'
         
        # Assigning Status Colours to the Pallets
        if palletType == "MaterialPallet":
          collar1 = newPallet.findFeature("Block")
          collar2 = newPallet.findFeature("Block_10")
          collar1.Material = palletStatusColours[palletStatus]
          collar2.Material = palletStatusColours[palletStatus]
        newPallet.rebuild()
        
    
def restQuery(url, data):
    #print url
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
      #print "Request Successful"
    except Exception as e:
      print("Rest Server request failed.",e)
    return encodedData


def encodeData(input, encoding):
    if isinstance(input, dict):
        return {encodeData(key, encoding): encodeData(value, encoding)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [encodeData(element, encoding) for element in input]
    elif isinstance(input, unicode):
        return input.encode(encoding)
    else:
        return input