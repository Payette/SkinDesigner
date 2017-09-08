


# By Santiago Garay
# SkinDesigner

"""
Use this component to apply a random panel layout algorithm to a Design Function.

    Args:
        patternBayIDs: A list of integers represetning the panel bay IDs to be used on the random algorithm ( IDs are based on their input number in SkinGenerator)  it is possible to include the same bay ID more than once. If no list is provided, the SkinGenerator default bay list is used.
        randomSeed: An integer that represents a random seed number to generate different random solutions. Defualt value is 1.
    Returns:
        dataFunction: A DataFunction object that inputs into a Layout Design Function component.

"""

ghenv.Component.Name = "SkinDesigner_Data_Random"
ghenv.Component.NickName = 'Data_Random'
ghenv.Component.Message = 'VER 0.0.60\nJul_13_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass

#import rhinoscriptsyntax as rs
#import Rhino
#import scriptcontext as sc
#from types import *
import random
import copy
#import math


#GLOBAL PARAMETERS-------------------------------------------------------



#paramters


class LayoutDataFunction:
    
    __m_RandomObject = None
    __m_RandomSeed = 1
    __m_PanelBayIndeces = []
    
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    
    def __init__(self):

        if patternBayIDs <> []: self.__m_PanelBayIndeces = patternBayIDs
        if randomSeed : self.__m_RandomSeed = randomSeed  #Global Random generator seed


    def GetParameter(self, strParam):
        
        if strParam == 'RandomSeed': return self.__m_RandomSeed
        
        return None
        

    def Run(self, PanelBay_List, pattern, level, inLevelIndex, defaultBayList, randomObj, bayIndex, panelPlane):
        
        if pattern == []:
            if  self.__m_PanelBayIndeces <>[]: validBayList = copy.deepcopy(self.__m_PanelBayIndeces)
            else: validBayList = copy.deepcopy(defaultBayList)
        else: validBayList = copy.deepcopy(pattern)
        
        # make cero based indices 
        if  validBayList:   
            for i in range(len(validBayList)) : validBayList[i] -=1
        else: validBayList = range(len(PanelBay_List))
        
        # search for valid panel randomly
        newBayIndex = randomObj.choice(validBayList)


        return newBayIndex
    



dataFunctionL = LayoutDataFunction()
print "Done"
