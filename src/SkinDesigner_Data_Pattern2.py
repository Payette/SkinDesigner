


# By Santiago Garay
# Skin Generator

"""
Use this component to apply a specific pattern panel layout algorithm to a Design Function. 
DattaPattern2 places each pattern on different rows: pattern_1 will be used on the 1st row of the facade, pattern_2 on the second, etc., repeating the sequence of patterns to complete all the rows if neccesary.

    Args:
        pattern_1: (pattern_2, etc.) A list of integers represetning the the sequence of panel bay IDs to be used in the pattern algorithm.
                    Addtitional patterns can be aded with the '+' sign to be used on the subsequent levels.
   Returns:
        dataFunction: A DataFunction object that inputs into a Design Function component.

"""

ghenv.Component.Name = "SkinDesigner_Data_Pattern2"
ghenv.Component.NickName = 'Data_Pattern2'
ghenv.Component.Message = 'VER 0.0.60\nJul_13_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass

# automnatically set the right input names and types (when using + icon) 
import Grasshopper.Kernel as gh
import GhPython
import scriptcontext as sc

numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
typeInt = gh.Parameters.Hints.GH_IntegerHint_CS()


for input in range(numInputs):
    access = accessList
    inputName = 'pattern_' + str(input+1)

    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = accessList
    ghenv.Component.Params.Input[input].TypeHint = typeInt
    
ghenv.Component.Attributes.Owner.OnPingDocument()

import Grasshopper.Kernel as gh
#import rhinoscriptsyntax as rs
#import Rhino
#import scriptcontext as sc
from types import *
import random
import copy
import math



class LayoutDataFunction:
    
    __m_patterns = []
    __m_Skip_X = 0
    __m_Skip_Y = 0
    warningData = []
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        
        self.__m_Skip_X= 0
        self.__m_Skip_Y= 0
        
        for input in range(numInputs):
            list = eval('pattern_'+str(input+1))
            if list <> []: self.__m_patterns.append(list)
        if self.__m_patterns <> []:
            if  len(self.__m_patterns) > 1:
                    newLength = 1
                    for list in self.__m_patterns : newLength *= len(list)
                    newPattern = []
                    for entry in range(newLength):
                        for list in self.__m_patterns:
                            index = int(math.fmod(entry,len(list)))
                            newPattern.append(list[index])
                            
                    self.__m_Skip_X = len(self.__m_patterns)-1
                    self.__m_Skip_Y= 1
                    self.__m_patterns = newPattern
            else: self.__m_patterns = self.__m_patterns[0]
        else:
            self.warningData.append("Provide at least one pattern") 
        print "Compiled pattern="+ str(self.__m_patterns)
        print "SkipX=" + str(self.__m_Skip_X)
        print "SkipY="+ str(self.__m_Skip_Y)
            
    def GetParameter(self, strParam):
        
        return None   
        
    #Selection of panel bay based on pattern/panel location
    def Run(self, PanelBay_List, pattern, level, inLevelIndex, defaultBayList, randomObj, bayIndex, panelPlane) :
        
        if pattern == []:
            if  self.__m_patterns<>[]: pattern =  self.__m_patterns
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
if dataFunctionL.warningData <> []: 
    for warning in dataFunction.warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, str(warning))

print "Done"
