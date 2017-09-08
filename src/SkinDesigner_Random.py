


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
        DesignFunction:

"""

ghenv.Component.Name = "SkinDesigner_Random"
ghenv.Component.NickName = 'Random'
ghenv.Component.Message = 'VER 0.0.52\nMay_27_2016'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"


#import rhinoscriptsyntax as rs
#import Rhino
#import scriptcontext as sc
#from types import *
import random
import copy
#import math


#GLOBAL PARAMETERS-------------------------------------------------------



#paramters


class DesignFunction:
    
    __m_functionCall = ''
    __m_functionType = ''
    __m_Random = None
    __m_RandomSeed = 1 
    __m_BayID_List = "bayList"
    
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    
    def __init__(self):
        
        self.__m_functionType = 'Bay'
        if BayID_List : self.__m_BayID_List = BayID_List 
        
                
        #----- functionCall valid skin parameters to us as inputs ------
        # myPanelBays: List of panel bay instances connected to skinGenerator
        # bayIndex : index of current bay in use from myPanelBays
        # bayPanelIndex :  index of current panel in use 
        # intCurrentLevel : Current level of cell being generated.
        # intCell_Index : Current index of cell being generated (matrix [x,y]= [intCurrentLevel, intCell_Index])
        # bayCornerPoints : corner points defining current bay cell location at skin
        # randomObj: Random object created on skin.
        # bayList : bay indices used in skin [1 based]
        
        self.__m_functionCall = "DesFunc_Random_Panel_Bays(myPanelBays, bayIndex, bayPanelIndex, " + str(self.__m_BayID_List) + ", randomObj)" 


    def IsBayType(self):
        if self.__m_functionType == 'Bay': return True
        return False
        
        
    def IsPanelType(self):
        if self.__m_functionType == 'Panel': return True
        return False     

    def RunString(self):
        return self.__m_functionCall
        
        
        # Random selection of panel bays
    def DesFunc_Random_Panel_Bays(self, PanelBay_List, bayIndex, bayPanelIndex, randomBayList, randomObj):

        # Define new current bay index based on the exclude bays listed 
        validBayList = copy.deepcopy(randomBayList)
        if  validBayList:   
            for i in range(len(validBayList)) : validBayList[i] -=1
        else: validBayList = range(len(PanelBay_List))
            
        # search for valid panel randomly
        newBayIndex = randomObj.choice(validBayList)
        
        #print "random";print validBayList; print newBayIndex
        return [PanelBay_List[newBayIndex], newBayIndex]
    



DesignFunction = DesignFunction()
print "Done"
