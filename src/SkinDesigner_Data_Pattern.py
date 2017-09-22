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
ghenv.Component.Message = 'VER 0.1.16\nSep_22_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
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
