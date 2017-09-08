# By Santiago Garay
# Skin Generator

"""
Use this component to generate a panel type.
-
Refer to PanelLib API for Definition input functions
    Args:
        Name: Panel ID string
        Definition: Text panel with panel definitions(commands) (refer to PanelLib API)        
        width: Panel width in scene units
        height: Panel height in scene units
        thickness: Panel wall thickness in scene units
        SystemData: inputs SystemData output from system-type components: CurtainWall, Wall.
        WindowData: inputs data from Window component
        ShadeData: inputs one or more outputs from shading-type components: Shade, LouverShading, ShadingBox
        GeometryData: inputs a list of data from Geometry component 
        Activate: Turns panel on/off

    Returns:
        Panel: A PanelLib object to use as input on Panel_Bay, Skin_Generator or Mock_up components
        PanelDefinition: A text output of the panel properties defined to be used as input on another panel component (as a live reference for instance)
"""

ghenv.Component.Name = "Panel_SkinGenerator"
ghenv.Component.NickName = 'Panel'
ghenv.Component.Message = 'VER 0.0.52\nMar_25_2016'
ghenv.Component.Category = "Skin_Generator"
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
    if input == 0: inputName = 'Name' ; access = accessItem
    elif input == 1: inputName = 'Activate'; access = accessItem; typeHint = typeBool   
    elif input == 2: inputName = 'Definition' ; access = accessList; typeHint = typeGHDoc
    elif input == 3: inputName = 'width' ; access = accessItem ; typeHint = typeFloat
    elif input == 4: inputName = 'height' ; access = accessItem ; typeHint = typeFloat
    elif input == 5: inputName = 'thickness'; access = accessItem ; typeHint = typeFloat
    elif input == 6: inputName = 'SystemData' ; access = accessList; typeHint = typeGHDoc
    elif input == 7: inputName = 'WindowData' ; access = accessList; typeHint = typeGHDoc
    elif input == 8: inputName = 'ShadeData' ; access = accessList; typeHint = typeGHDoc
    elif input == 9: inputName = 'GeometryData'; access = accessList; typeHint = typeNone 
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
sc.doc = ghdoc

Panel = None
PanelDefinition = ""


#SKIN GRID GENERATION BASED ON PANEL SIZE
#------------------------------------------------------------------------------
def PanelCreate():

    #initialize
    sc.doc = Rhino.RhinoDoc.ActiveDoc
    rs.EnableRedraw(False)

    #Create Skin Panel Matrix
    #Panel dimensions (Units feet or meters)
    
    #--------------------------------------------------------------------
    # PANEL INIT SECTION

    myBasePanel = SGLibPanel()
    PanelDefinition = [""]
    tmpDefinition = ["", None, None, None, None, None]
    
    # run size panel properties if avialable
    if numInputs > 2 and Definition and Definition[0] :
        if len(Definition) == 1: 
            tmpDefinition = ["", None, None, None, None, Definition[0]]
        else :
            tmpDefinition = Definition
            runActions(tmpDefinition[0], myBasePanel)
            PanelDefinition[0] = tmpDefinition[0] 

    #set panel properties from inputs and update Panel Defintion
    if  numInputs > 3 and width:
        try: myBasePanel.Width(width)
        except: print"width error"
        PanelDefinition[0] = updateProperty(PanelDefinition[0], "Width", myBasePanel.PanelProperty("PanelWidth"))
    if numInputs > 4 and height:
        try: myBasePanel.Height(height)
        except: print"height error"
        PanelDefinition[0] = updateProperty(PanelDefinition[0], "Height", myBasePanel.PanelProperty("PanelHeight"))
    if numInputs > 5 and thickness:
        try: myBasePanel.Thickness(thickness)
        except: print"thickness error"
        PanelDefinition[0] = updateProperty(PanelDefinition[0], "Thickness", myBasePanel.PanelProperty("PanelThickness"))
        
    #set predifined variables:
    PanelName = "'DefaultPanel'"
    if Name <> None: PanelName = Name
    myBasePanel.SetName(PanelName) 
    
    PanelHeight = myBasePanel.PanelProperty("PanelHeight")
    PanelWidth = myBasePanel.PanelProperty("PanelWidth")
    PanelThickness = myBasePanel.PanelProperty("PanelThickness")
    
    #----------Create Window -----------------------------------------    
    tmpWindowData = None ; Window = None
    if numInputs > 2 and tmpDefinition[1] : tmpWindowData = tmpDefinition[1]
    if numInputs > 7 and WindowData : tmpWindowData = WindowData
    if tmpWindowData : 
        Window = dict(width=tmpWindowData[0], height=tmpWindowData[1], fromLeft=tmpWindowData[2], fromBottom=tmpWindowData[3], recess=tmpWindowData[4])
        windowDef = "AddWindow(width=Window['width'], height=Window['height'], fromLeft=Window['fromLeft'], fromBottom=Window['fromBottom'], recess=Window['recess'])"
        runActions(windowDef, myBasePanel, Window, PanelWidth, PanelHeight, PanelThickness)
    PanelDefinition.append(tmpWindowData)
            
    #------------Create System----------------------------------------------
    tmpSystemData = None
    if numInputs > 2 and tmpDefinition[2] : tmpSystemData = tmpDefinition[2]
    if numInputs > 6 and SystemData and SystemData[0]: tmpSystemData = SystemData
    if tmpSystemData:
        runActions(tmpSystemData[1], myBasePanel, Window, PanelWidth, PanelHeight, PanelThickness)
        runActions(tmpSystemData[2], myBasePanel, Window, PanelWidth, PanelHeight, PanelThickness)
        if Window: runActions(tmpSystemData[3], myBasePanel, Window, PanelWidth, PanelHeight, PanelThickness)
    PanelDefinition.append(tmpSystemData)
    
    #------------Create Shading----------------------------------------------
    tmpShadeData = None
    if numInputs > 2 and tmpDefinition[3] : tmpShadeData = tmpDefinition[3]    
    if numInputs > 8 and ShadeData: tmpShadeData = ShadeData
    if tmpShadeData : 
        tmpWindowData = None
        if numInputs > 7 and WindowData: #create window data without variables to avoid error when solving of parameters
            tmpWindowData = copy.deepcopy(Window)
            if type(tmpWindowData['width']) == StringType :  tmpWindowData['width'] = eval(tmpWindowData['width'])
            if type(tmpWindowData['height']) == StringType :  tmpWindowData['height'] = eval(tmpWindowData['height'])
            if tmpWindowData['fromLeft'] == 'C' : tmpWindowData['fromLeft'] = (PanelWidth-tmpWindowData['width'])/2
            if tmpWindowData['fromBottom'] == 'C' : tmpWindowData['fromBottom'] = (PanelHeight-tmpWindowData['height'])/2  
            
        for shade in tmpShadeData:
            runActions(shade, myBasePanel, tmpWindowData, PanelWidth, PanelHeight, PanelThickness)
    PanelDefinition.append(tmpShadeData)
            
    #-------------Create Custom Geometry --------------------------------------------------------
    tmpGeometryData = None
    if numInputs > 2 and tmpDefinition[4] : tmpGeometryData = tmpDefinition[4]
    if numInputs > 9 and GeometryData : tmpGeometryData = GeometryData
    if tmpGeometryData:
        myBasePanel.AddCustomGeometry(tmpGeometryData[0], tmpGeometryData[1], tmpGeometryData[2], tmpGeometryData[3],+\
            tmpGeometryData[4], tmpGeometryData[5], tmpGeometryData[6])
    PanelDefinition.append(tmpGeometryData)

    # ---------run definition if provided---------------------------------------------------
    if numInputs > 2 and tmpDefinition[5] : 
        runActions(tmpDefinition[5], myBasePanel, Window,  PanelWidth, PanelHeight, PanelThickness)
    PanelDefinition.append(tmpDefinition[5])
    
    #---------- test Draw -------------
    #myBasePanel.Draw() #Draw in scene (for checkup geometry only)

    #Wrapup
    rs.EnableRedraw(True)
    sc.doc = ghdoc
    return myBasePanel, PanelDefinition

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
    actionList = actionString.rsplit("\r\n")
    for action in actionList: 
        if action : 
            action = "myBasePanel." + action
            codeObj= compile(action,'<string>','single')
            eval(codeObj)

if Activate : Panel, PanelDefinition = PanelCreate()

print "done"