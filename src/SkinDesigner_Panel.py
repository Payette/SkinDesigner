# By Santiago Garay
# Skin Generator

"""
Use this component to generate a panel type.
-
Refer to Panel API for panel object functions
    Args:
        name: A string that represents the panel ID. By defualt it uses de component guid (not recommended).
        activate: A boolean that turns the panel on/off. Default is off.        
        definitions: A string with panel functions to be executed on this panel (only for advanced use, refer to Panel API)        
        width: A float number specifying the panel width in scene units
        height: A float number specifying the panel height in scene units
        thickness: A float number specifying the panel wall object thickness in scene units
        panelSystem: A list with data generated by panel system-type components: CurtainWall, Wall, etc.
        windowSystem:  A list with data generated by Window component
        shadingSystems: lists with data generated by shading-type components: Shade, LouverShading, ShadingBox
        customSystem: A list with data generated by a CustomGeometry component 


    Returns:
        panel: A Panel object that represents a Panel data structure to be used as input on Panel_Bay, Skin_Generator or Panel Viewer components
        panelDefinition: A string representing the panel properties as panel functions (refer to Panel API). 
            It can be saved for reference or be used as input on another panel component (as a live reference for instance)
            
"""

ghenv.Component.Name = "SkinDesigner_Panel"
ghenv.Component.NickName = 'Panel'
ghenv.Component.Message = 'VER 0.0.63\nSep_03_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "01 | Construction"

import Grasshopper.Kernel as gh
import GhPython
# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item

typeFloat = GhPython.Component.NewFloatHint()
typeString = GhPython.Component.NewStrHint()
typeNone =  GhPython.Component.NoChangeHint()
typeGHDoc = GhPython.Component.GhDocGuidHint()
typeBool = gh.Parameters.Hints.GH_BooleanHint_CS()
for input in range(numInputs):
    access = accessList ; typeHint = typeString
    if input == 0: inputName = 'name' ; access = accessItem
    elif input == 1: inputName = 'activate'; access = accessItem; typeHint = typeBool   
    elif input == 2: inputName = 'definitions' ; access = accessList; typeHint = typeGHDoc
    elif input == 3: inputName = 'width' ; access = accessItem ; typeHint = typeFloat
    elif input == 4: inputName = 'height' ; access = accessItem ; typeHint = typeFloat
    elif input == 5: inputName = 'thickness'; access = accessItem ; typeHint = typeFloat
    elif input == 6: inputName = 'panelSystem' ; access = accessList; typeHint = typeGHDoc
    elif input == 7: inputName = 'windowSystem' ; access = accessList; typeHint = typeGHDoc
    elif input == 8: inputName = 'shadingSystems' ; access = accessList; typeHint = typeGHDoc
    elif input == 9: inputName = 'customSystem'; access = accessList; typeHint = typeNone 
    else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    ghenv.Component.Params.Input[input].TypeHint = typeHint
    ghenv.Component.Attributes.Owner.OnPingDocument()



import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
import copy
from types import *
SGLibPanel = sc.sticky["SGLib_Panel"]

#init set up global variables

sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
_UNIT_COEF = 1
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == Rhino.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
sc.doc = ghdoc

panel = None
panelDefinition = ""
warningData = []
panelWarningData = []

try:
    SGLibPanel = sc.sticky["SGLib_Panel"]
except:
    warningData.append("I need SkinDesigner_SkinDesigner component")
    
#SKIN GRID GENERATION BASED ON PANEL SIZE
#------------------------------------------------------------------------------
def PanelCreate():

    #initialize
    sc.doc = Rhino.RhinoDoc.ActiveDoc
    rs.EnableRedraw(False)
    global warningData
    
    #Create Skin Panel Matrix
    #Panel dimensions (Units feet or meters)
    
    #--------------------------------------------------------------------
    # PANEL INIT SECTION

    myBasePanel = SGLibPanel()
    panelDefinition = [""]
    tmpDefinition = ["", None, None, None, None, None]
    
    # run size panel properties if avialable
    if numInputs > 2 and definitions and definitions[0] :
        if len(definitions) == 1: 
            tmpDefinition = ["", None, None, None, None, definitions[0]]
        else :
            tmpDefinition = definitions
            runOK = runActions(tmpDefinition[0], myBasePanel)
            if not runOK: warningData.append("Invalid 'definitions' input (panel size data) - data discarded")
            panelDefinition[0] = tmpDefinition[0] 

    #set panel properties from inputs and update Panel Defintion
    if  numInputs > 3 and width:
        try: myBasePanel.SetWidth(width)
        except: warningData.append("Invalid 'width' input - using default value")
        panelDefinition[0] = updateProperty(panelDefinition[0], "Width", myBasePanel.GetPanelProperty("PanelWidth"))
    if numInputs > 4 and height:
        try: myBasePanel.SetHeight(height)
        except: warningData.append("Invalid 'height' input - using default value")
        panelDefinition[0] = updateProperty(panelDefinition[0], "Height", myBasePanel.GetPanelProperty("PanelHeight"))
    if numInputs > 5 and thickness:
        try: myBasePanel.SetThickness(thickness)
        except: warningData.append("Invalid 'thickness' input - using default value")
        panelDefinition[0] = updateProperty(panelDefinition[0], "Thickness", myBasePanel.GetPanelProperty("PanelThickness"))
        
    #set predifined variables:
    PanelName = str(ghenv.Component.InstanceGuid).rsplit("-",1)[1]

    if name <> None: PanelName = name
    myBasePanel.SetName(PanelName) 
    
    PanelHeight = myBasePanel.GetPanelProperty("PanelHeight")
    PanelWidth = myBasePanel.GetPanelProperty("PanelWidth")
    PanelThickness = myBasePanel.GetPanelProperty("PanelThickness")
    
    #----------Create Window -----------------------------------------    
    tmpWindowSystem = None ; Window = None
    if numInputs > 2 and len(tmpDefinition)>1 and tmpDefinition[1] : tmpWindowSystem = tmpDefinition[1]
    if numInputs > 7 and windowSystem : tmpWindowSystem = windowSystem
    if tmpWindowSystem : 
        try:
            Window = dict(width=tmpWindowSystem[0], height=tmpWindowSystem[1], fromLeft=tmpWindowSystem[2], fromBottom=tmpWindowSystem[3], recess=tmpWindowSystem[4])
            windowDef = "AddWindow(width=Window['width'], height=Window['height'], fromLeft=Window['fromLeft'], fromBottom=Window['fromBottom'], recess=Window['recess'])"
        except:  
            warningData.append("Invalid 'windowSystem' input - data discarded")
            Window = None
        else:
            runOK = runActions(windowDef, myBasePanel, Window, PanelWidth, PanelHeight, PanelThickness)
            if not runOK: warningData.append("Invalid 'windoSystem' input - data discarded")
    panelDefinition.append(tmpWindowSystem)
            
    #------------Create Panel System----------------------------------------------
    tmpPanelSystem = None
    if numInputs > 2 and len(tmpDefinition)>2 and tmpDefinition[2] : tmpPanelSystem = tmpDefinition[2]
    if numInputs > 6 and panelSystem and panelSystem[0]: tmpPanelSystem = panelSystem
    if tmpPanelSystem:
        runOK = runActions(tmpPanelSystem[1], myBasePanel, Window, PanelWidth, PanelHeight, PanelThickness)
        if not runOK: warningData.append("Invalid 'panelSystem' input (pane data)- data discarded")
        runOK = runActions(tmpPanelSystem[2], myBasePanel, Window, PanelWidth, PanelHeight, PanelThickness)
        if not runOK: warningData.append("Invalid 'panelSystem' input (mullions data)- data discarded")
        if Window: 
            runOK = runActions(tmpPanelSystem[3], myBasePanel, Window, PanelWidth, PanelHeight, PanelThickness)
            if not runOK: warningData.append("Invalid 'panelSystem' input (window mullions data)- data discarded")
    panelDefinition.append(tmpPanelSystem)
    
    #------------Create Shading----------------------------------------------
    tmpShadeData = None
    if numInputs > 2 and len(tmpDefinition)>3 and tmpDefinition[3] : tmpShadeData = tmpDefinition[3]    
    if numInputs > 8 and shadingSystems: tmpShadeData = shadingSystems
    if tmpShadeData : 
        tmpWindowSystem = None
        if numInputs > 7 and windowSystem: #create window data without variables to avoid error when solving of parameters
            tmpWindowSystem = copy.deepcopy(Window)
            try:
                if type(tmpWindowSystem['width']) == StringType :  tmpWindowSystem['width'] = eval(tmpWindowSystem['width'])
                if type(tmpWindowSystem['height']) == StringType :  tmpWindowSystem['height'] = eval(tmpWindowSystem['height'])
                if tmpWindowSystem['fromLeft'] == 'C' : tmpWindowSystem['fromLeft'] = (PanelWidth-tmpWindowSystem['width'])/2
                if tmpWindowSystem['fromBottom'] == 'C' : tmpWindowSystem['fromBottom'] = (PanelHeight-tmpWindowSystem['height'])/2  
                if type(tmpWindowSystem['fromLeft']) == StringType :  tmpWindowSystem['fromLeft'] = eval(tmpWindowSystem['fromLeft'])
                if type(tmpWindowSystem['fromBottom']) == StringType :  tmpWindowSystem['fromBottom'] = eval(tmpWindowSystem['fromBottom'])
            except: 
                warningData.append("Invalid window parameters - data discarded")
                tmpWindowSystem = None
        for index, shade in enumerate(tmpShadeData):
            runOK = runActions(shade, myBasePanel, tmpWindowSystem, PanelWidth, PanelHeight, PanelThickness)
            if not runOK: warningData.append("Invalid 'shadingSystem' input - shading system #"+str(index)+ " - data discarded")
            
    panelDefinition.append(tmpShadeData)
            
    #-------------Create Custom Geometry --------------------------------------------------------
    tmpGeometryData = None
    if numInputs > 2 and len(tmpDefinition)>4 and tmpDefinition[4] : tmpGeometryData = tmpDefinition[4]
    if numInputs > 9 and customSystem : tmpGeometryData = customSystem
    if tmpGeometryData and len(tmpGeometryData)==8 and tmpGeometryData[0]:
        try:
            myBasePanel.AddCustomGeometry(tmpGeometryData[0], tmpGeometryData[1], tmpGeometryData[2], tmpGeometryData[3],+\
                tmpGeometryData[4], tmpGeometryData[5], tmpGeometryData[6], tmpGeometryData[7])
        except: warningData.append("Invalid 'customSystem' input - data discarded")
    panelDefinition.append(tmpGeometryData)

    # ---------run definition if provided---------------------------------------------------
    if numInputs > 2 and len(tmpDefinition)>5 and tmpDefinition[5]: 
        runOK = runActions(tmpDefinition[5], myBasePanel, Window,  PanelWidth, PanelHeight, PanelThickness)
        if not runOK: warningData.append("Invalid 'definitions' input - process incomplete")
        panelDefinition.append(tmpDefinition[5])
    
    #---------- test Draw -------------
    #myBasePanel.Draw("drawGeometry") #Draw in scene (for checkup geometry only)

    #Wrapup
    rs.EnableRedraw(True)
    sc.doc = ghdoc
    return myBasePanel, panelDefinition

    #----------------------------------------------------------------

def updateProperty(definition, property, value):
    txtStart = definition.find(property+"(")
    if txtStart >= 0 :     
        txtDelete = definition[txtStart : definition.find(")",txtStart)+3]
        definition = definition.replace(txtDelete, "")
        
    definition = property + "(" + str(value) + ")\r\n" + definition

    return definition

def runActions(actionString, myBasePanel, Window=None, PanelWidth=None, PanelHeight=None, PanelThickness=None, brepGeometry=None):
    #print [myBasePanel, Window, PanelWidth, PanelHeight, PanelThickness]
    #print actionString
    
    try:
        actionList = actionString.rsplit("\r\n")
        for action in actionList: 
            if action : 
                if "Window[" in action and Window == None: continue
                action = "myBasePanel." + action
                codeObj= compile(action,'<string>','single')
                eval(codeObj)
    except:
        return False
    return True
    


if activate : 
    panel, panelDefinition = PanelCreate()
    panelWarningData = panel.GetPanelProperty("WarningData")

if warningData <> []: 
    for warning in warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, str(warning))
if panelWarningData <> []:
    for warning in panelWarningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, str("Internal Warning:\n\r" +warning))    
print "done"