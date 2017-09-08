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

ghenv.Component.Name = "Geometry_SkinGenerator"
ghenv.Component.NickName = 'Geometry'
ghenv.Component.Message = 'VER 0.0.47\nMar_15_2016'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "02 | Panel Parameters"


# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item
 
for input in range(numInputs):
    access = accessList
    if input == 0: inputName = 'CustomGeometry' ; access = accessItem
    elif input == 1: inputName = 'upAxisVector' ; access = accessItem
    elif input == 2: inputName = 'offsetVector' ; access = accessItem
    elif input == 3: inputName = 'scaleVector' ; access = accessItem
    elif input == 4: inputName = 'tilable'; access = accessItem
    else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    
ghenv.Component.Attributes.Owner.OnPingDocument()

import scriptcontext as sc
import Rhino as rc
import rhinoscriptsyntax as rs

#init set up global variables
_UNIT_COEF = 1
sc.doc = rc.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == rc.UnitSystem.Feet: _UNIT_COEF = 3.28084
sc.doc = ghdoc

vecUpAxis = rc.Geometry.Vector3d(0,1,0)
vecPlacement = rc.Geometry.Vector3d(0,0,0)
vecScaleFactor = rc.Geometry.Vector3d(1,1,1) #(non uniform scale can throw error someimtes(ex.cirles))
isTilable = False

if numInputs > 1 and upAxisVector : vecUpAxis = rs.coerce3dvector(upAxisVector)
if numInputs > 2 and offsetVector : vecPlacement = rs.coerce3dvector(offsetVector)
if numInputs > 3 and scaleVector : vecScaleFactor = rs.coerce3dvector(scaleVector)
if numInputs > 4 and tilable : isTilable = tilable

GeometryData = [CustomGeometry, vecPlacement, vecScaleFactor, vecUpAxis, isTilable, None, None]
print "Done"