# By Santiago Garay
# Skin Generator

"""
Use this component to generate a panel window
-
Refer to PanelLib API for Definition input functions
    Args:
        Height: Panel height in meters
        Width: Panel width in meters
        Definition: Text panel that define panel properties (refer to PanelLib API)
        Activate: Turns panel on/off

    Returns:
        Panel: A PanelLib object to use as input on Panel_Bay, Skin_Generator or Mock_up components

"""

ghenv.Component.Name = "SkinDesigner_Geometry"
ghenv.Component.NickName = 'Geometry'
ghenv.Component.Message = 'VER 0.0.53\nMar_07_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"


# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item
 
for input in range(numInputs):
    access = accessList
    if input == 0: inputName = '_customGeometry' ; access = accessList
    elif input == 1: inputName = 'upAxisVector' ; access = accessItem
    elif input == 2: inputName = 'offsetVector' ; access = accessItem
    elif input == 3: inputName = 'scaleVector' ; access = accessItem
    elif input == 4: inputName = 'rotation' ; access = accessItem
    elif input == 5: inputName = 'tilable'; access = accessItem
    elif input == 6: inputName = 'trimToPanelSize'; access = accessItem
    elif input == 7: inputName = 'windowVoidDepth'; access = accessItem
    else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    
ghenv.Component.Attributes.Owner.OnPingDocument()

import scriptcontext as sc
import Rhino as rc
import rhinoscriptsyntax as rs
from types import *


#init set up global variables
_UNIT_COEF = 1
sc.doc = rc.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == rc.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == rc.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
sc.doc = ghdoc

newCustomGeometry = None
vecUpAxis = rc.Geometry.Vector3d(0,1,0)
vecPlacement = rc.Geometry.Vector3d(0,0,0)
vecScaleFactor = rc.Geometry.Vector3d(1,1,1) #(non uniform scale can throw error someimtes(ex.cirles))
rotationZ = 0
isTilable = False
isTrimmed = False
dblWindowVoidDepth = 0
customSystem = None

#check for customGeoemtry type : Brep or dynamicGeometry instance

if _customGeometry and _customGeometry[0]:
    if str(type(_customGeometry[0])) == "<type 'Brep'>" :
        newCustomGeometry = _customGeometry
    if str(type(_customGeometry[0])) == "<type 'instance'>" : 
        newCustomGeometry = _customGeometry[0]
    
    if numInputs > 1 and upAxisVector <> None: vecUpAxis = rs.coerce3dvector(upAxisVector)
    if numInputs > 2 and offsetVector <> None: vecPlacement = rs.coerce3dvector(offsetVector)
    if numInputs > 3 and scaleVector <> None: vecScaleFactor = rs.coerce3dvector(scaleVector)
    if numInputs > 4 and rotation < None : rotationZ = eval(str(rotation))
    if numInputs > 5 and tilable <> None : isTilable = tilable
    if numInputs > 6 and trimToPanelSize <> None : isTrimmed = trimToPanelSize
    if numInputs > 7 and windowVoidDepth <> None: dblWindowVoidDepth = windowVoidDepth
        
    customSystem = [newCustomGeometry, vecPlacement, vecScaleFactor, vecUpAxis, isTilable, rotationZ, dblWindowVoidDepth, isTrimmed]

print "Done"
