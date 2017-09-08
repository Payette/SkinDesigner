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

ghenv.Component.Name = "WindowShade_SkinGenerator"
ghenv.Component.NickName = 'Shade'
ghenv.Component.Message = 'VER 0.0.41\nMar_02_2016'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "02 | Panel Parameters"



# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item


for input in range(numInputs):
    access = accessList
    if input == 0: inputName = 'shadingWidth'; access = accessItem
    elif input == 1: inputName = 'shadingThickness'; access = accessItem
    elif input == 2: inputName = 'offset'; access = accessItem
    elif input == 3: inputName = 'vertical'; access = accessItem
    elif input == 4: inputName = 'windowShade'; access = accessItem
    elif input == 5: inputName = 'fromLeftEdge' ; access = accessItem
    elif input == 6: inputName = 'fromBottomEdge' ; access = accessItem
    elif input == 7: inputName = 'fromEdgeEnd'; access = accessItem
    else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    
ghenv.Component.Attributes.Owner.OnPingDocument()


import scriptcontext as sc
import Rhino


#init set up global variables
_UNIT_COEF = 1
sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
sc.doc = ghdoc



shadingType = ''

if shadingWidth == None : shadingWidth = .1*_UNIT_COEF
if shadingThickness == None : shadingThickness = .02*_UNIT_COEF
if offset == None : offset = .02*_UNIT_COEF
if fromLeftEdge == None : fromLeftEdge = 0
if fromBottomEdge == None : fromBottomEdge = 0
if fromEdgeEnd == None : fromEdgeEnd = 0

fromEdge = fromEdgeEnd
fromLeft = fromLeftEdge
fromBottom = fromBottomEdge


if vertical == True : shadingType = "VerticalShade"
else : shadingType = 'HorizontalShade'
    
if windowShade == True:
    fromLeft = "Window['fromLeft']+"+str(fromLeftEdge);fromBottom = "Window['fromBottom']+"+str(fromBottomEdge)
    if shadingType == 'HorizontalShade' : fromEdge = "PanelWidth-Window['width']-Window['fromLeft']+"+str(fromEdge)
    elif shadingType == 'VerticalShade' : fromEdge = "PanelHeight-Window['height']-Window['fromBottom']+"+str(fromEdge)



# WindowData(wd) = 0=width,1=height,2=fromLeft,3=fromBottom,4=recess 

ShadingData = "AddShadingType('" + shadingType +"', fromLeftBottom = ["+str(fromLeft)+", "+str(fromBottom)+"], fromEdge="+str(fromEdge)+",width="+str(shadingThickness)+", thickness="+str(shadingWidth)+", offset="+str(offset)+")\r\n"


print ShadingData
