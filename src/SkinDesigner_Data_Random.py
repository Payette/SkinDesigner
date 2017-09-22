# SkinDesigner: A Plugin for Building Skin Design (GPL) started by Santiago Garay

# This file is part of SkinDesigner.
# 
# Copyright (c) 2017, Santiago Garay <sgaray1970@gmail.com> 
# SkinDesigner is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# SkinDesigner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with SkinDesigner; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

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
ghenv.Component.Message = 'VER 0.1.16\nSep_22_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
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
