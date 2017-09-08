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

ghenv.Component.Name = "Wall_SkinGenerator"
ghenv.Component.NickName = 'Wall'
ghenv.Component.Message = 'VER 0.0.48\nMar_24_2016'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "02 | Panel Parameters"


# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item
 
for input in range(numInputs):
    access = accessList
    if input == 0: inputName = 'windowFrameWidth' ; access = accessItem
    elif input == 1: inputName = 'windowFrameThickness' ; access = accessItem
    elif input == 2: inputName = 'windowFrameLoc' ; access = accessItem
    elif input == 3: inputName = 'tileWidth' ; access = accessItem
    elif input == 4: inputName = 'tileHeight'; access = accessItem
    elif input == 5: inputName = 'tileThickness' ; access = accessItem
    elif input == 6: inputName = 'tileGap'; access = accessItem
    elif input == 7: inputName = 'tileEdgeOffset'; access = accessItem    
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


# WindowData(wd) = 0=width,1=height,2=fromLeft,3=fromBottom,4=recess
if  numInputs > 3:
    if tileWidth == None or tileHeight == None: tileWidth = tileHeight = 0
    if tileThickness == None:
        if tileWidth > 0: tileThickness = .02*_UNIT_COEF
        else:  tileThickness = 0
    if tileGap == None and tileWidth > 0: tileGap = 0.01*_UNIT_COEF 
    else: tileGap = 0
    if tileEdgeOffset == None : tileEdgeOffset = tileGap/2
else:
    tileWidth = tileHeight = tileThickness = tileGap = tileEdgeOffset = 0

SystemData= [0,0,0,0]
paneName="_P_Clad"
paneThickness = .01*_UNIT_COEF #standard pane thickness (not relevant)
PanelActions = "AddPane('"+ paneName + "', thickness="+str(paneThickness)+", offset="+str(paneThickness)+", offsetEdge="+str(tileEdgeOffset)+\
    ", tileWidth="+str(tileWidth)+", tileHeight="+str(tileHeight)+", tileThickness="+str(tileThickness)+", tileGap="+str(tileGap)+")\r\n"


if windowFrameThickness == None: windowFrameThickness = "max(PanelThickness+0.02*_UNIT_COEF+"+str(paneThickness+tileThickness)+", abs(Window['recess']) + 0.05*_UNIT_COEF + "+str(paneThickness+tileThickness)+")"
if windowFrameWidth == None: windowFrameWidth = .025*_UNIT_COEF
if windowFrameLoc == None: windowFrameLoc = "0"

MullionActions = ""
WindowMullionActions = ""

windowFrameInThickness = "min(max(0.02*_UNIT_COEF,"+"Window['recess']+PanelThickness-0.01*_UNIT_COEF)+"+str(windowFrameLoc)+","+str(windowFrameThickness)+"+0.02*_UNIT_COEF)"
windowFrameOutThickness = "min(max("+str(windowFrameThickness) + "-(" + windowFrameInThickness + "),.02*_UNIT_COEF),"+str(windowFrameThickness)+")"

for mullionType in ['WindowBottom','WindowTop','WindowLeft', 'WindowRight'] :
    WindowMullionActions += "AddMullionType('"+ mullionType+"', width="+ str(windowFrameWidth)+", thickness=[" + \
    str(windowFrameInThickness)+"], capThickness=[" + str(windowFrameOutThickness)+"])\r\n"


SystemData = ["WallSystem" , PanelActions , MullionActions, WindowMullionActions]

print SystemData
 



