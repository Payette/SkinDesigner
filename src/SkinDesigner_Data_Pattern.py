


# By Santiago Garay
# Skin Generator

"""
Use this component to apply a specific pattern panel layout algorithm to a Design Function.

    Args:
        patternBayIDs: A list of integers represetning the sequence of panel bays to be used in the pattern algorithm (based on their input number in SkinGenerator).
        skipX: An integer that represents the number of panel id entries to be skipped from the patternBayIDs list at every new entry along a row of cells. 
        skipY: An integer that represents the number of panel id entries to be skipped from the patternBayIDs list at every new start of a row of cells.
    Returns:
        dataFunction: A DataFunction object that inputs into a Design Function component.

"""

ghenv.Component.Name = "SkinDesigner_Data_Pattern"
ghenv.Component.NickName = 'Data_Pattern'
ghenv.Component.Message = 'VER 0.0.60\nJul_13_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass

#import rhinoscriptsyntax as rs
#import Rhino
#import scriptcontext as sc
from types import *
import random
import copy
import math



class LayoutDataFunction:
    
    __m_pattern = []
    __m_Skip_X = 0
    __m_Skip_Y = 0
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):

        if patternBayIDs : self.__m_pattern = patternBayIDs
        if skipX : self.__m_Skip_X= skipX
        if skipY : self.__m_Skip_Y= skipY
        
        
    def GetParameter(self, strParam):
        
        return None   
        
    #Selection of panel bay based on pattern/panel location
    def Run(self, PanelBay_List, pattern, level, inLevelIndex, defaultBayList, randomObj, bayIndex, panelPlane) :
        
        if pattern == []:
            if  self.__m_pattern<>[]: pattern =  self.__m_pattern
            else: pattern = range(1,len(PanelBay_List)+1)
        
        skipX = self.__m_Skip_X; skipY = self.__m_Skip_Y
        
        #bayList = copy.deepcopy(defaultBayList)
        bayList = pattern
        skipX+=1
        levelPair = math.modf(level/len(bayList)) # relationship between floor number and bay number
        levelShift = (level - levelPair[1] * len(bayList)) * skipY # number of shifts based on current level
        newInLevelIndex = inLevelIndex * skipX + levelShift
        floorPair = math.modf(newInLevelIndex/len(bayList)) # curent index in list based on bay location
        defBayIndex = newInLevelIndex - floorPair[1]*len(bayList)
        bayIndex  = bayList[int(defBayIndex)]-1

        return bayIndex
        
        

            
        



dataFunctionL = LayoutDataFunction()
print "Done"
