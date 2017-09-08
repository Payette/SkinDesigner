


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
        Actions: Text panel that define properties and functions to be used on the skin generation
        Panel_Bay_1: A list of panels that define a bay(Add as many panel bays inputs as necesary_)

    Returns:
        SkinPanel_List: A list containing all the Panel objects used to generate the skin

"""

ghenv.Component.Name = "DesignFunction_SkinGenerator"
ghenv.Component.NickName = 'DesignFunction'
ghenv.Component.Message = 'VER 0.0.43\nDEC_14_2015'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "02 | Parameters"


#import rhinoscriptsyntax as rs
#import Rhino
#import scriptcontext as sc
#from types import *
#import random
#import copy
#import math
#import Panel15 as PanelLib

#GLOBAL PARAMETERS-------------------------------------------------------



#paramters
skip_X=skip_Y=0


FUNCTION_CALL = "DesFunc_Pattern_Panel_Bays(myPanelBays,  l, i, "+str(skip_X)+", "+str(skip_Y)+", DEFAULT_BAY_LIST)" #---Random selection between panel bays
FUNCTION_DEFINITION=functionText
designFunction = FUNCTION_DEFINITION+"\r\n"+FUNCTION_CALL

def DesFunc_Pattern_Panel_Bays(PanelBay_List, level, inLevelIndex, skipX, skipY,  defaultBayList=None):
    
    skipX+=1
    levelPair = math.modf(level/len(defaultBayList)) # relationship between floor number and bay number
    levelShift = (level - levelPair[1] * len(defaultBayList)) * skipY               # number of shifts based on current level
    newInLevelIndex = inLevelIndex * skipX + levelShift
    floorPair = math.modf(newInLevelIndex/len(defaultBayList)) # curent index in list based on bay location
    defBayIndex = newInLevelIndex - floorPair[1]*len(defaultBayList)

    bayIndex  = defaultBayList[int(defBayIndex)]-1

            
    return [PanelBay_List[bayIndex], bayIndex]


