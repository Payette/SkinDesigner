


# By Santiago Garay
# Skin Generator

"""
Use this component to generate your building skin.
_
_
To add more panels bays in the construction, simply zoom into the component and hit the lowest "+" sign that shows up on the input side.  To remove panels from the construction, zoom into the component and hit the lowest "-" sign that shows up on the input side.
-
    Args:
        a: a
        b: b
    Returns:
        c: c

"""

ghenv.Component.Name = "SkinShop_Pattern"
ghenv.Component.NickName = 'Pattern'
ghenv.Component.Message = 'VER 0.0.46\nApr_07_2016'
ghenv.Component.Category = "SkinShop"
ghenv.Component.SubCategory = "03 | Functions"


#import rhinoscriptsyntax as rs
#import Rhino
#import scriptcontext as sc
#from types import *
#import random
import copy
import math


class DesignFunction:
    
    __m_functionCall = ''
    __m_Skip_X = 0
    __m_Skip_Y = 0
    __m_pattern = []
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        if Pattern : self.__m_pattern = eval(Pattern)

        if Skip_X : self.__m_Skip_X= Skip_X
        if Skip_Y : self.__m_Skip_Y= Skip_Y
        
        #----- functionCall valid skin parameters to us as inputs ------
        # myPanelBays: List of panel bay instances connected to skinGenerator
        # bayIndex : index of current bay in use from myPanelBays
        # bayPanelIndex :  index of current panel in use 
        # intCurrentLevel : Current level of cell being generated.
        # intCell_Index : Current index of cell being generated (matrix [x,y]= [intCurrentLevel, intCell_Index])
        # bayCornerPoints : corner points defining current bay cell location at skin
        # randomObj: Random object created on skin.
        # bayList : bay indices used in skin [1 based]
        
        self.__m_functionCall = "DesFunc_Pattern_Panel_Bays"+\
            "(myPanelBays,  intCurrentLevel, intCell_Index, " + str(self.__m_Skip_X)+", " + str(self.__m_Skip_Y)+",  bayList)"
            
    def RunString(self):
        return self.__m_functionCall

        
    def DesFunc_Pattern_Panel_Bays(self, PanelBay_List, level, inLevelIndex, skipX, skipY,  defaultBayList):
        
        if not self.__m_pattern : self.__m_pattern = copy.deepcopy(defaultBayList)

        #bayList = copy.deepcopy(defaultBayList)
        bayList = self.__m_pattern
        skipX+=1
        levelPair = math.modf(level/len(bayList)) # relationship between floor number and bay number
        levelShift = (level - levelPair[1] * len(bayList)) * skipY # number of shifts based on current level
        newInLevelIndex = inLevelIndex * skipX + levelShift
        floorPair = math.modf(newInLevelIndex/len(bayList)) # curent index in list based on bay location
        defBayIndex = newInLevelIndex - floorPair[1]*len(bayList)
        bayIndex  = bayList[int(defBayIndex)]-1

        return [PanelBay_List[bayIndex], bayIndex]



DesignFunction = DesignFunction()
print "Done"
