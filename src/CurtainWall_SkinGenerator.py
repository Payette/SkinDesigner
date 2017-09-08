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

ghenv.Component.Name = "CurtainWall_SkinGenerator"
ghenv.Component.NickName = 'CurtainWall'
ghenv.Component.Message = 'VER 0.0.42\nMar_02_2016'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "02 | Panel Parameters"


# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item

for input in range(numInputs):
    access = accessList
    if input == 0: inputName = 'width'
    elif input == 1: inputName = 'thickness'
    elif input == 2: inputName = 'capThickness'
    elif input == 3: inputName = 'windowThickness'
    elif input == 4: inputName = 'windowCapThickness'
    elif input == 5: inputName = 'thickness_H'
    elif input == 6: inputName = 'capThickness_H'
    elif input == 7: inputName = 'thickness_V'
    elif input == 8: inputName = 'capThickness_V'
    elif input == 9: inputName = 'windowThickness_H'
    elif input == 10: inputName = 'windowCapThickness_H'
    elif input == 11: inputName = 'windowThickness_V'
    elif input == 12: inputName = 'windowCapThickness_V'
    else: continue
        
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = accessItem
    
    
# reset to None deleted inputs. They keep last data otherwise.
inputNames = ['width','thickness','capThickness','windowThickness','windowCapThickness','thickness_H','capThickness_H',\
    'thickness_V', 'capThickness_V', 'windowThickness_H', 'windowCapThickness_H','windowThickness_V','windowCapThickness_V']
for num in range(13-numInputs) :
    inputString = inputNames[12-num]
    inputString += '=None'
    codeObj= compile(inputString,'<string>','single')
    eval(codeObj)
    
    
    
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

if width == None : width = .05*_UNIT_COEF
if thickness == None : thickness = 0.1* _UNIT_COEF
if windowThickness == None : windowThickness = thickness
if capThickness == None : capThickness = 0.02*_UNIT_COEF
if windowCapThickness == None : windowCapThickness = capThickness

if thickness_H == None : thickness_H = thickness
if thickness_V == None : thickness_V = thickness
if capThickness_H == None : capThickness_H = capThickness
if capThickness_V == None : capThickness_V = capThickness
    

if windowThickness_H == None : windowThickness_H = windowThickness
if windowThickness_V == None : windowThickness_V = windowThickness
if windowCapThickness_H == None : windowCapThickness_H = windowCapThickness
if windowCapThickness_V == None : windowCapThickness_V = windowCapThickness

SystemData= [0,0,0,0]

PanelActions = "AddPane('_P_Glass_SP',thickness="+str(0.02*_UNIT_COEF)+", offset="+str(0.02*_UNIT_COEF)+", offsetEdge="+str(0.02*_UNIT_COEF)+")\r\n"
MullionActions = ""
WindowMullionActions = "" #WindowMullionActions = "ShowWall()\r\n"

for mullionType in ['PanelLeft', 'PanelRight','PanelTop','PanelBottom','WindowBottom','WindowTop','WindowLeft', 'WindowRight'] :
    
    if mullionType in ['PanelBottom', 'PanelTop'] :
        if thickness_H: thickness  = thickness_H
        else :continue
        capThickness = capThickness_H
    if mullionType in ['PanelLeft', 'PanelRight'] :
        if thickness_V: thickness = thickness_V
        else :continue
        capThickness = capThickness_V
    if mullionType in ['PanelLeft', 'PanelRight','PanelTop','PanelBottom'] :
        MullionActions += "AddMullionType('"+ mullionType+"', width="+ str(width)+", thickness=" + str(thickness)+", capThickness=" + str(capThickness)+")\r\n"

    if mullionType in ['WindowBottom','WindowTop'] :
        if windowThickness_H : windowThickness = windowThickness_H
        else : continue
        windowCapThickness = windowCapThickness_H
    if mullionType in ['WindowLeft', 'WindowRight'] :
        if windowThickness_V : windowThickness = windowThickness_V
        else : continue
        windowCapThickness = windowCapThickness_V
        
    if mullionType in ['WindowLeft', 'WindowRight','WindowBottom','WindowTop'] :
        WindowMullionActions += "AddMullionType('"+ mullionType+"', width="+ str(width)+", thickness=" + str(windowThickness)+", capThickness=" + str(windowCapThickness)+")\r\n"


SystemData = ["CurtainWall" , PanelActions , MullionActions, WindowMullionActions]

print SystemData
 
#thickness= thicknessA = thicknessC="max(thickness, wd[4]*-1)" # use wall thickness or glass recess on punched window
#MullionData = "AddWindowMullions(width="+ str(width)+", thickness=[" + str(thicknessA)+","+ str(thickness)+","+ str(thicknessC)+\
#    "], capThickness=[0,0.05,0])\r\n"


