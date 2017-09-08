
# By Santiago Garay
# Skin Generator

"""
Use this component to generate custom panels based on provided paramters.

    Args:
        panelNames: A string with panel names (separated by a space) to use as base panels, uses all panels if not provided.
        _parameter: A string with a panel property to be used to generate new custom panels
        valueMin: the minumin value of the range of values to map the Data list to, defaults to minimum number in list.
        valuemax: the maximum number of the range of values to map the Data List to, defaults to the maximuim number in list
        numSamples: the number of in-between values the range should have, defaults to 2. 
        DataList: a list of numbers to use to generate the values to apply to the panel property. A one mid-point of range constant number is used if not provided.
        DataFunction: a DataFunction object generated from its dedicated component
    Returns:
        DesignFunction: A function object that inputs into the Skin Generator component

"""

ghenv.Component.Name = "SkinDesigner_Customizer"
ghenv.Component.NickName = 'Panel_Customizer'
ghenv.Component.Message = 'VER 0.0.69\nOct_10_2016'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"


import rhinoscriptsyntax as rs
#import Rhino
#import scriptcontext as sc
from types import *
import random
import copy
#import math
#import imp



class DesignFunction:
    __m_parameterList = []
    __m_valueMin = 0
    __m_valueMax = 0
    __m_valueSamples = 0
    __m_dataList = []
    __m_dataIndex = 0
    __m_panelNameList= None
    __m_excludeCustomSizePanels = False
    __m_functionType = ''
    __m_customPanelIndex = 0
    __m_DataFunction = None
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self, valueMin, valueMax, numSamples):
        
        self.__m_functionType = 'Panel'
        self.__m_dataIndex = 0
        self.__m_customPanelIndex = 1
        
        if DataList : self.__m_dataList = DataList
               
        if panelNames : self.__m_panelNameList = panelNames.split(" ")  
        
        excludeCustomSize = True
        if excludeCustomSize : self.__m_excludeCustomSizePanels = excludeCustomSize
        
        if type(_parameters)==ListType and len(_parameters): 
            for param in _parameters:
                self.__m_parameterList.append(eval(param))
        
        if numSamples  : numSamples = int(eval(str(numSamples)))
        
        if numSamples < 1 or type(numSamples) <> IntType :
            numSamples = 1
            print "invalid number of samples , default = 2 samples"
        
        if valueMin == None :
            if len(self.__m_dataList): valueMin = min(self.__m_dataList)
            else: valueMin = 0
        else: valueMin = eval(str(valueMin))
       
        if valueMax == None : 
            if len(self.__m_dataList): valueMax = max(self.__m_dataList)
            else: valueMax = valueMin+1
        else : valueMax = eval(str(valueMax))  
            
            
        
        #Mapping data list to min/max range and allowed samples
        tmpList = []
       
        if len(self.__m_dataList):
            #convert data list to new range
            
            # snap to middle point of range  if only one number in found in list
            if max(self.__m_dataList) ==  min(self.__m_dataList):
                if valueMax > valueMin : self.__m_dataList = [(valueMax - abs(valueMin))/2]
                else: self.__m_dataList = [(valueMin - abs(valueMax))/2]
            else : 
                dataCoef = (valueMax - valueMin)/(max(self.__m_dataList) - min(self.__m_dataList))
            
                for i in range(len(self.__m_dataList)):
                    tmpList.append((self.__m_dataList[i] - min(self.__m_dataList))*dataCoef + valueMin)
                self.__m_dataList = tmpList
    
                tmpList =[]
                for i in self.__m_dataList : 
                    if i not in tmpList : tmpList.append(i)
                #snap data items to sample steps
                if numSamples < len(tmpList):
                    tmpList =[]
                    dataStep = (valueMax-valueMin)/(numSamples-1) if numSamples > 1 else 1
                    for i in range(numSamples):tmpList.append(i*dataStep+valueMin)
                    tmpDataList = []
                    for i in range(len(self.__m_dataList)):
                        mappedList = map(lambda x: abs(x-self.__m_dataList[i]),tmpList)
                        index = mappedList.index(min(mappedList))
                        tmpDataList.append(tmpList[index]) 
                    self.__m_dataList = tmpDataList
        else:
            #if no list provided create default list based on range and sample steps
            valSample = valueMin
            for i in range(numSamples):
                self.__m_dataList.append(valSample)                
                valSample += (valueMax-valueMin)/(numSamples-1) if numSamples > 1 else 1

            
        self.__m_valueMin = valueMin
        self.__m_valueMax = valueMax
        self.__m_valueSamples = numSamples
        
        if DataFunction : self.__m_DataFunction = DataFunction
        
        print "Parameter list: " + str(self.__m_parameterList)
        print "Range: "+str([self.__m_valueMin, self.__m_valueMax])          
        print "DataList: "+ str(self.__m_dataList)
        print len(self.__m_dataList)
        #----- functionCall valid skin parameters to us as inputs ------
        # myPanelBays: List of panel bay instances connected to skinGenerator
        # bayIndex : index of current bay in use from myPanelBays
        # bayPanelIndex :  index of current panel in use 
        # intCurrentLevel : Current level of cell being generated.
        # intCell_Index : Current index of cell being generated (matrix [x,y]= [intCurrentLevel, intCell_Index, ])
        # bayCornerPoints : corner points defining current bay cell location at skin
        # randomObj: Random object created on skin.
        # bayList : bay indices used from skin component bay inputs[1 based]
        # ChangeFlag : List used in Skin Generator to identify panel changes - format: [panel height , panel width , PropertyDictionary ]
        # BasePanel : Panel used as base for new custom panel (can only be used on callState=1 section

    def Reset(self):
        self.__m_dataIndex = 0
        self.__m_customPanelIndex = 1
        if DataFunction : self.__m_DataFunction.Reset()
        
    def IsBayType(self):
        if self.__m_functionType == 'Bay': return True
        return False
        
        
    def IsPanelType(self):
        if self.__m_functionType == 'Panel': return True
        return False        
        
        
    def RunString(self):
        return
        

    ##1st call - Flagging panel modifications
    def DesFunc_Panels_Flag(self, myPanelBays, bayIndex, bayPanelIndex, intCurrentLevel, intCell_Index, bayCornerPoints, ChangeFlag, BasePanel):
        
        PanelWidth = ChangeFlag[1]/1000
        PanelHeight = ChangeFlag[0]/1000  
        
        
        if self.__m_panelNameList == None or BasePanel.GetName() in self.__m_panelNameList :
            
            if self.__m_excludeCustomSizePanels:
                if BasePanel.GetHeight() <> PanelHeight: return
                if BasePanel.GetWidth() <> PanelWidth: return
            
            dataInstance = self.__m_dataList[self.__m_dataIndex]
            
            #get runtime data if data function provided
            if self.__m_DataFunction :
                dataInstance = self.__m_DataFunction.Run(dataInstance=dataInstance, valueMin=self.__m_valueMin, \
                    valueMax = self.__m_valueMax, numSamples = self.__m_valueSamples, bayCornerPoints=bayCornerPoints )
                    
            #store parameters and data in panel change flag 
            propDict = ChangeFlag[2]
            for param in self.__m_parameterList:
                if param[0] not in propDict : propDict[param[0]] = []
                propDict[param[0]].append(param[1]+"="+str(dataInstance))
                
            # update data counter for next panel
            self.__m_dataIndex += 1
            if self.__m_dataIndex == len(self.__m_dataList) : self.__m_dataIndex = 0



    #2nd call - Performing panel modifications 
    def DesFunc_Panels_Modify(self, myPanelBays, bayIndex, bayPanelIndex, intCurrentLevel, intCell_Index, bayCornerPoints, ChangeFlag, BasePanel):
        
        if self.__m_panelNameList <> None and BasePanel.GetName().partition('.')[0] not in self.__m_panelNameList : return

        PanelWidth = ChangeFlag[1]/1000
        PanelHeight = ChangeFlag[0]/1000  

        propDict = ChangeFlag[2]
        if propDict == 0 : return
        
        #go through flagged changes on panel
        customFlag = False
        for param, value in zip(propDict.keys(), propDict.values()):
            
            #compare with each of the parameter changes specified in paramterList
            for parameter in self.__m_parameterList:                        
                if parameter[0] == param and parameter[1] in value[0]: #found a match?
                    customFlag = True
                    #run panel funcitons based on type of parameter change
                    if  param == "Shading":
                        if "type=" in value[0]:
                            exec("BasePanel.ModifyShadingType("+value[0]+")")
                            del value[0]
                        elif  "index=" in value[0]:
                            exec("BasePanel.ModifyShadingIndex("+value[0]+")")
                            del value[0]
                    elif param == "Window":
                        exec("BasePanel.ModifyWindow("+value[0]+")")
                        del value[0]
                    elif param == "Mullion":
                        exec("BasePanel.ChangeMullionType("+value[0]+")")
                        del value[0]
                    elif param == "CustomGeometry":
                        exec("BasePanel.ModifyCustomGeometry("+value[0]+")")
                        del value[0]
                    else:
                        if BasePanel.PanelProperty(param) <> value:
                            BasePanel.SetProperty(param, value)

        #Add Version number (.x)  to the panel name (used on panel inventory viewer)
        if customFlag :
            panelName = BasePanel.GetName()+"."+str(self.__m_customPanelIndex)
            BasePanel.SetName(panelName)
            self.__m_customPanelIndex +=1
                    
        return 


DesignFunction = DesignFunction(valueMin, valueMax, numSamples)
print "Done"
print DataList