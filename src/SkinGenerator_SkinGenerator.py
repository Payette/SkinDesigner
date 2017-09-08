# By Santiago Garay
# Skin Generator

"""
Use this component to generate your building skin.
_
_
To add more panels bays in the construction, simply zoom into the component and hit the lowest "+" sign that shows up on the input side.  To remove panels from the construction, zoom into the component and hit the lowest "-" sign that shows up on the input side.
-
    Args:
        SkinSurfaceList: List of surfaces to be used as base skins where the panels will be mapped to. 
        ModifierCurves : List of curve objects that modify the default algorithms used oni the surface> SHould be coplanar to the surfaces they affect.
        SkinParameters: Text panel that define properties and functions to be used on the skin generation
        Panel_Bay_1: A list of panels that define a bay(Add as many panel bays inputs as necesary_)

    Returns:
        SkinPanel_List: A list containing all the Panel objects used to generate the skin

"""

ghenv.Component.Name = "SkinGenerator_SkinGenerator"
ghenv.Component.NickName = 'Skin_Generator'
ghenv.Component.Message = 'VER 0.0.50\nApr_03_2016'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "01 | Construction"

# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item
 
for input in range(numInputs):
    access = accessList
    if input == 0: inputName = 'Activate'; access = accessItem    
    elif input == 1: inputName = 'SkinSurfaceList' ; access = accessList
    elif input == 2: inputName = 'SkinParameters' ; access = accessList
    elif input == 3: inputName = 'DesignFunctions'; access = accessList   
    elif input == 4: inputName = 'PostProcFunctions'; access = accessList   
    else: inputName = 'Panel_Bay_' + str(input-4)

    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    
ghenv.Component.Attributes.Owner.OnPingDocument()


import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
from types import *
import random
import copy
import math

SGLibPanel = sc.sticky["SGLib_Panel"]
SGLibSkin = sc.sticky["SGLib_Skin"]

#GLOBAL PARAMETERS-------------------------------------------------------
SKIN_NAME = "DEFAULT"

DEFAULT_OFFSET_LEVEL = 0.0          #Offset distance of first panel at segments.Use list for different dimensions at each segment 
DEFAULT_OFFSET_PATH = 0.0           #Offset in elevation from path to be considered bottom of panel. Any value > 0 creates custom panel. 

DEFAULT_SKIN_WRAP = True            #Wrap at corners or create custom corner panels
SKIN_WRAP = True

RESET_BAY_AT_POINTS = True  #Start new bay at new segment

FLAT_MODE = False           #Low geoemtry mode
DRAW_MODE = "DEFAULT"       #"LADYBUG", "DEFAULT" 

DEFAULT_BAY_LIST = None     #default bays used in skin - 'None' will use all panel bays connected

MIN_PANEL_WIDTH = .1        #if surface cell width is below this number it will be ignored and panel won't be created.
MIN_PANEL_HEIGHT = .1       #if surface cell height is below this number will be ignored and panel won't be created.

RANDOM = random.Random()    #Global Random generator object


#---------------------------------------------------------------------------------------------------------
#SKIN GENERATION SECTION
#---------------------------------------------------------------------------------------------------------


def SkinGenerator(myPanelBays, DesignFunctions):


    #Create Skin matrix (grid with panel bay dimensions)
    SkinList = []  #Skin class instances (one per polysurface)
    
    #-----Skin Vertices Matrix creation data ----------------------------------- 
    dblFloorToFloor = myPanelBays[0][0].PanelProperty("PanelHeight") #get bay height from first panel
    dblBayWidth = 0
    for panel in myPanelBays[0]:
        dblBayWidth += panel.PanelProperty("PanelWidth")#get bay width from adding up its panel widths
        
    #-----Skin generation data -----------------------------------------------------------------------------
    PanelTypes = {} #Stores panel types created throughout skin surfaces
    BayData = myPanelBays + [0 for x in myPanelBays] #bay counters in format [list of bays, list of  counters]    
    
    #Parameter/valuse list used to transfer data from Skin Generator component to Skin object 
    skinParams = [["OFFSET_LEVEL", DEFAULT_OFFSET_LEVEL], ["OFFSET_PATH", DEFAULT_OFFSET_PATH], ["SKIN_WRAP", DEFAULT_SKIN_WRAP],\
        ["RESET_BAY_AT_POINTS", RESET_BAY_AT_POINTS], ["FLAT_MODE", FLAT_MODE], ["DRAW_MODE", DRAW_MODE], ["BAY_LIST", DEFAULT_BAY_LIST],\
        ["MIN_PANEL_WIDTH", MIN_PANEL_WIDTH], ["MIN_PANEL_HEIGHT", MIN_PANEL_HEIGHT], ["RANDOM_OBJECT", RANDOM],\
        ["DESIGN_FUNCTIONS", DesignFunctions]]

    #Create Panel Matrix and Panel Blocks one surface object at a a time
    for objSkinSurface in SkinSurfaceList:
        #create skin object
        tmpSkin = SGLibSkin(SKIN_NAME, objSkinSurface, myPanelBays)
        #load default parameters
        for param in skinParams: tmpSkin.SetProperty(param[0], param[1])
        #generate panel vertex matrix
        tmpSkin.GeneratePanelMatrix(dblBayWidth, dblFloorToFloor)
        #generate panel blocks
        PanelTypes, BayData = tmpSkin.GeneratePanelBlocks(PanelTypes, BayData) 
        
        SkinList.append(tmpSkin)
           

    return PanelTypes, Bay_Data


#-----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
#Set Draw mode for panel bays(and their panels) provided
#----------------------------------------------------------------------------------------
def SetDrawMode(panelBayList, DRAW_MODE):
    
    for panelBay in panelBayList:
        for panel  in panelBay :panel.SetDrawMode(DRAW_MODE)
            

    
#---CLEAN UP SECTION--------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
#Delete Panels and its block instances 
#----------------------------------------------------------------------------------------
def DeletePanelObjects():
    result = "Del False"
    if not sc.sticky["Panel_Data"+SKIN_NAME] : return
    for group in sc.sticky["Panel_Data"+SKIN_NAME].values() :
        for item in group :
            if isinstance(item[0], SGLibPanel):
                item[0].DeleteBlockCopies() #Delete blocks first if blocks created   
                item[0].HideAll() #same as deleting all panel objects
                result ="Del True"
                
    print result
#----------------------------------------------------------------------------------------
# Cleanup old ladybug objects
#----------------------------------------------------------------------------------------

def DeleteLadybugObjects():
    
    if "Panel_Ladybug_Data"  in sc.sticky and len(sc.sticky["Panel_Ladybug_Data"]):
        rs.DeleteObjects(sc.sticky["Panel_Ladybug_Data"])
        
        sc.sticky["Panel_Ladybug_Data"] = []
        #sc.sticky["Panel_DaylightHours"] = []
        #sc.sticky["Panel_SolarRadiation"] = []
           



#---RUN---------------------------------------------------------------------------------------------------

#init
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)


#Run skin paramters -----------------------------------------
if  SkinParameters :
    for action in SkinParameters: 
        if action : 
            codeObj= compile(action,'<string>','single')
            eval(codeObj)


# Add skin variables to the sticky dict
if "Panel_Data"+SKIN_NAME not in sc.sticky: sc.sticky["Panel_Data"+SKIN_NAME] = []
if "count" not in sc.sticky : sc.sticky["count"] = 0


#Delete previous skin if present
DeletePanelObjects()


SkinPanel_List = []
Bay_Data = []
sc.sticky["count"] += 1


# -------Execute Panel Skin Comamands  -----------------------------------------------
PanelBay_List = [] 

# Reset values
if not Activate:
    sc.sticky["count"] = 0

    #Clean up Panels data
    sc.sticky["Panel_Data"+SKIN_NAME] = []
    
    # Cleanup old ladybug data
    DeleteLadybugObjects()
    
#  If activated , store paramters and run skin generator  

elif  SkinSurfaceList != []: 
    numInputs = ghenv.Component.Params.Input.Count
    
    #Load panel bays from inputs to PanelBay_List
    for input in range(numInputs):
        item = ghenv.Component.Params.Input[input]
        if "Panel_Bay" in item.Name and item.VolatileDataCount > 0: 
            pList = []
            for i in range(item.VolatileDataCount) : 
                if item.VolatileData.get_DataItem(i):
                    pList.append(item.VolatileData.get_DataItem(i).Value)
            if pList : PanelBay_List.append(pList)
            
    if PanelBay_List:
        
        #Run Post Proc. (Draw mode) functions if available
        drawModeSet = False
        for ppf in PostProcFunctions:
            if ppf.PPDrawMode() :
                SetDrawMode(PanelBay_List, ppf.PPDrawMode())
                drawModeSet = True
                break
        if not drawModeSet: SetDrawMode(PanelBay_List, 'DEFAULT')
        
        #create default list if empty
        #if not DEFAULT_BAY_LIST :  DEFAULT_BAY_LIST = range(len(myPanelBays))   
        #------Run Skin Generator-----------------------------------
        
        SkinPanel_List, Bay_Data = SkinGenerator(PanelBay_List, DesignFunctions)
        #Store in memory (for cleanup in next iteration)
        sc.sticky["Panel_Data"+SKIN_NAME] = SkinPanel_List

#Ladybug Run Section------------------------------------------------------------------

# Ladybug init
LadybugGeo = []
if "Panel_Ladybug_Data" not in sc.sticky : sc.sticky["Panel_Ladybug_Data"] = []
if "Panel_DaylightHours" not in sc.sticky : sc.sticky["Panel_DaylightHours"] = []
if "Panel_SolarRadiation" not in sc.sticky : sc.sticky["Panel_SolarRadiation"] = []

#Delete previous ladybug objects if created
DeleteLadybugObjects()

# ---- Post Processing functions-------------------------------------------------
if Activate and SkinSurfaceList != [] and PanelBay_List != []:
    if  PostProcFunctions :       
        for ppFunc in PostProcFunctions:
            LadybugGeo = eval("ppFunc."+ppFunc.RunString())
            
#Wrap up--------------------------------------------------------------------------

print sc.sticky["count"]
if SkinPanel_List : SkinPanel_List = SkinPanel_List.values()

rs.EnableRedraw(True)
sc.doc = ghdoc

