
# By Santiago Garay
# Skin Generator

"""
Use this component to apply a panel algorithms to a SkinGenerator component.

    Args:
        dataList: A list of floating point numbers that will be used to generate the range of values to apply to the panel property. A one mid-point of range constant number is used if not provided.
        dataFunctionPList: A list of Panel Data Functions to be run over the data list created. Panel DataFunction objects are created by Data Function components such as DataProximity.
        panelNamesFilter: A list of strings indicating the panel names to be affected by the panel function. If not provided the fucntion applies to all panels used by the SkinGenerator solution.
        _panelParameters: A list of strings indicating the panel properties that will be modified with the resulting data to create a new panel.
        valueMin: A floating point value indicating the minumin value of the range to map the data list to, defaults to minimum number in list.
        valuemax: the maximum number of the range of values to map the Data List to. Defaults to the maximuim number in list
        numSamples: the number of in-between steps the data list will be snapped to. Defaults is 2. 
    Returns:
        designFunction: A designFunction object to be connected to the SkinGenerator component.

"""

ghenv.Component.Name = "SkinDesigner_PanelFunction"
ghenv.Component.NickName = 'PanelFunction'
ghenv.Component.Message = 'VER 0.0.75\nJul_13_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import Grasshopper.Kernel as gh
import rhinoscriptsyntax as rs
#import Rhino
import scriptcontext as sc
from types import *
import random
import copy
#import math
#import imp

SGLibDesignFunction = sc.sticky["SGLib_DesignFunction"]

class PanelDesignFunction(SGLibDesignFunction):
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
    __m_DataFunctions = []
    warningData = []
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self, valueMin, valueMax, numSamples):
        
        self.__m_functionType = 'Panel'
        self.__m_dataIndex = 0
        self.__m_customPanelIndex = 1
        
        if dataList  <> []: 
            self.__m_dataList = copy.deepcopy(dataList)
            while True:
                try:
                    self.__m_dataList.remove("valueMin")
                except:break
            while True:
                try:
                    self.__m_dataList.remove("valueMax")
                except:break                    
            self.__m_dataList = list((float(eval(data)) for data in self.__m_dataList))

        if panelNamesFilter <> []: self.__m_panelNameList = panelNamesFilter
        
        excludeCustomSize = False
        if excludeCustomSize : self.__m_excludeCustomSizePanels = excludeCustomSize
        
        if _panelParameters == []: self.warningData.append("Missing '_panelParameters' input")
        try:
            if type(_panelParameters)==ListType and len(_panelParameters): 
                for param in _panelParameters:
                    self.__m_parameterList.append(eval(param))
        except:
            self.warningData.append("Invalid '_panelParameters' input")
        
        if numSamples < 1 or type(numSamples) <> IntType :
            numSamples = 2
            print"invalid number of samples , default = 2 samples"
        
        if valueMin == None :
            if len(self.__m_dataList): valueMin = min(self.__m_dataList)
            else: valueMin = 0

        if valueMax == None : 
            if len(self.__m_dataList): valueMax = max(self.__m_dataList)
            else: valueMax = valueMin+1
            
            
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
                    
                    # save and print new sample values to align data to
                    layerList = []
                    for val in tmpList: layerList.append('Layer_'+ (str(val)[0:7] if val>0 else str(val)[0:8]))
                    print "Available layer list: " + str(layerList)
                    
                    tmpDataList = []
                    for i in range(len(self.__m_dataList)):
                        mappedList = map(lambda x: abs(x-self.__m_dataList[i]),tmpList)
                        index = mappedList.index(min(mappedList))
                        tmpDataList.append(tmpList[index]) 
                    self.__m_dataList = tmpDataList
                    
        else:
            #if no list provided create default list based on range and sample steps
            if not "valueMin" in dataList and not "valueMax" in dataList:
                valSample = valueMin
                for i in range(numSamples):
                    self.__m_dataList.append(valSample)                
                    valSample += (valueMax-valueMin)/(numSamples-1) if numSamples > 1 else 1
                
        self.__m_valueMin = valueMin
        self.__m_valueMax = valueMax
        self.__m_valueSamples = numSamples

        #add variables used in list if any
        numInserts = 0
        for index, element in enumerate(dataList):
            if element == "valueMin" or element == "valueMax" : 
                self.__m_dataList.insert(index, eval(element))
                numInserts +=1

        if dataFunctionPList <> []:
            for index, df in enumerate(dataFunctionPList):
                if df.__class__.__name__ <> "PanelDataFunction":
                    self.warningData.append("Invalid dataFunction #"+str(index+1)+": "+str(df))
                    dataFunctionPList[index] = None
            try: 
                while True: dataFunctionPList.remove(None)
            except: pass
        if dataFunctionPList <> []: self.__m_DataFunctions = dataFunctionPList    
        print self.__m_DataFunctions
        #print "Parameter list: " + str(self.__m_parameterList)
        print "data steps: " + str(list((self.__m_valueMin + n*(self.__m_valueMax-self.__m_valueMin)/((numSamples-1) if numSamples > 1 else 1)\
            for n in range(self.__m_valueSamples))))
        print "data steps adjusted to list: " + str(tmpList)
        print "data List: "+ str(self.__m_dataList)
        #print len(self.__m_dataList)
        

    def Reset(self):
        self.__m_dataIndex = 0
        self.__m_customPanelIndex = 1
        for df in self.__m_DataFunctions: df.Reset()
        
    def IsLayoutType(self):
        if self.__m_functionType == 'Layout': return True
        return False
        
        
    def IsPanelType(self):
        if self.__m_functionType == 'Panel': return True
        return False        
        
        
    #def RunString(self):
        #return
        
        #----- functionCall valid skin parameters to us as inputs ------
        # skinInstance :  a reference to the skin object calling this function
        # ChangeFlag : List used in Skin Generator to identify panel changes - format: [panel height , panel width , PropertyDictionary ]
        # BasePanel : Panel used as base for new custom panel (can only be used on callState=1 section

    ##1st call - Flagging panel modifications
    def Run_Flag(self, skinInstance, ChangeFlag, BasePanel):
        
        PanelWidth = ChangeFlag[1]/1000
        PanelHeight = ChangeFlag[0]/1000  

        if self.__m_panelNameList == None or BasePanel.GetName() in self.__m_panelNameList :
            
            if self.__m_excludeCustomSizePanels:
                if BasePanel.GetHeight() <> PanelHeight: return
                if BasePanel.GetWidth() <> PanelWidth: return
            
            dataInstance = self.__m_dataList[self.__m_dataIndex]
            
            #run data functions provided
            if len(self.__m_DataFunctions) : 
                for df in self.__m_DataFunctions:
                    dataInstance = df.Run(dataInstance=dataInstance, valueMin=self.__m_valueMin, \
                    valueMax = self.__m_valueMax, numSamples = self.__m_valueSamples, skinInstance=skinInstance, panelFlags=ChangeFlag[2])
                    
            #store parameters and data in panel change flag 
            propDict = ChangeFlag[2]
            for param in self.__m_parameterList:
                if param[0] not in propDict : propDict[param[0]] = []
                propDict[param[0]].append(param[1]+"="+str(dataInstance))
            
            # update data counter for next panel
            self.__m_dataIndex += 1
            if self.__m_dataIndex == len(self.__m_dataList) : self.__m_dataIndex = 0
            


    #2nd call - Performing panel modifications 
    def Run_Modify(self, ChangeFlag, BasePanel):
        
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
                        strData = value[0]
                        if "layerName" in value[0]: 
                            splitData = value[0].rsplit("=",1)
                            splitData[1] = splitData[1][0:7] if splitData[1].find("-") else  splitData[1][0:8]
                            strData = splitData[0]+"='Layer_"+splitData[1]+"'"
                        if "type=" in value[0]:
                            exec("BasePanel.ModifyShadingType("+strData+")")
                            del value[0]
                        elif  "index=" in value[0]:
                            exec("BasePanel.ModifyShadingIndex("+strData+")")
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
                            BasePanel.SetPanelProperty(param, value)

        #Add Version number (.x)  to the panel name (used on panel inventory viewer)
        if customFlag :
            panelName = BasePanel.GetName()+"."+str(self.__m_customPanelIndex)
            BasePanel.SetName(panelName)
            self.__m_customPanelIndex +=1
                    
        return 


designFunction = PanelDesignFunction(valueMin, valueMax, numSamples)
if designFunction.warningData <> []: 
    for warning in designFunction.warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, str(warning))

if designFunction.warningData <> []: designFunction = None

print "Done"
