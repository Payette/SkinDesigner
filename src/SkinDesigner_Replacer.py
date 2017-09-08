


# By Santiago Garay
# Skin Generator

"""
Use this component to generate your building skin.
_
_
To add more panels bays in the construction, simply zoom into the component and hit the lowest "+" sign that shows up on the input side.  To remove panels from the construction, zoom into the component and hit the lowest "-" sign that shows up on the input side.
-
    Args:
        modifierObjects : List of curve and surface objects that modify the default algorithms used on the surface.


    Returns:
        SkinPanel_List: A list containing all the Panel objects used to generate the skin

"""

ghenv.Component.Name = "SkinDesigner_Replacer"
ghenv.Component.NickName = 'Replacer'
ghenv.Component.Message = 'VER 0.0.56\nOct_14_2016'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"


import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc
from types import *
import random
import copy
import math
#import imp



class DesignFunction:
    
    __m_modifierObjects = None
    __m_functionCall = ''
    __m_functionType = ''
    __m_falloffRadius = 0
    #__m_BayID_List = "BAY_LIST"
    __m_inmuneBayID_List = []
    __m_randomObject = None
    __m_randomSeed = 1
    __m_DataFunction = None
    
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        
        self.__m_functionType = 'Bay'
        if modifierObjects : self.__m_modifierObjects = modifierObjects
        if falloff : self.__m_falloffRadius = falloff 
        #if BayID_List : self.__m_BayID_List = BayID_List
        if inmuneBayIDs : self.__m_inmuneBayID_List = inmuneBayIDs
        self.__m_randomObject = random.Random()    #Global Random generator object
        self.__m_randomObject.seed(self.__m_randomSeed)
        
        self.__m_functionType = 'Bay'
        if _dataFunction : self.__m_DataFunction = _dataFunction
        
        #----- functionCall valid skin parameters to us as inputs ------
        # myPanelBays: List of panel bay instances connected to skinGenerator
        # bayIndex : index of current bay in use from myPanelBays
        # bayPanelIndex :  index of current panel in use 
        # intCurrentLevel : Current level of cell being generated.
        # intCell_Index : Current index of cell being generated (matrix [x,y]= [intCurrentLevel, intCell_Index])
        # bayCornerPoints : corner points defining current bay cell location at skin
        # randomObj: Random object created on skin.
        # bayList : bay indices used in skin [1 based]
        
        
        self.__m_functionCall = "DesFunc_CurveGradient_Panel_Bays(myPanelBays, bayIndex, bayPanelIndex," +\
            str(self.__m_inmuneBayID_List)+", "+ "bayList, bayCornerPoints , "+str(self.__m_falloffRadius)+", intCurrentLevel, intCell_Index)"

    def IsBayType(self):
        if self.__m_functionType == 'Bay': return True
        return False
        
        
    def IsPanelType(self):
        if self.__m_functionType == 'Panel': return True
        return False        

    def Reset(self):
        if self.__m_DataFunction: 
            param = self.__m_DataFunction.GetParameter('RandomSeed')
            if param : self.__m_randomObject.seed(param)
        
    def RunString(self):
        return self.__m_functionCall
        
    #Selection of panel bay base on proximity to modifier curves
    def DesFunc_CurveGradient_Panel_Bays(self, PanelBay_List, bayIndex, bayPanelIndex, bayStayIndexList, defaultBayList, ptPanel, dblFalloffRadius, level, inLevelIndex):
        
        if self.__m_DataFunction == None : return [PanelBay_List[bayIndex], bayIndex]  
        
        #check if bayindex should not be changed (bayStayList)
        validBayStayList = copy.deepcopy(bayStayIndexList)
        for i in range(len(validBayStayList)) : validBayStayList[i] -= 1 #convert to cero based list
        if bayIndex in validBayStayList : return [PanelBay_List[bayIndex], bayIndex]
        
        newBayIndex = bayIndex # new bay index used to return new bay object
        
        rndVal = self.__m_randomObject.random()# 0-1 random base value for algorithm
        #obtain panel center point to evaluate
        midDist = rs.VectorScale(rs.VectorCreate(ptPanel[3],ptPanel[0]),.5)
        centerPoint = rs.PointAdd(ptPanel[0], midDist)  
        
        #multiple curves can be tested simultaneosly with algorithm
        dist = 0 ; flagPanel = False
        panelPlane=rs.PlaneFromPoints(ptPanel[0], ptPanel[1], ptPanel[2]) #panel bay plane
        
        if self.__m_modifierObjects == None :
            newBayIndex = self.__m_DataFunction.Run(PanelBay_List, [] , level, inLevelIndex,  defaultBayList, self.__m_randomObject, bayIndex, bayPanelIndex) 
            return [PanelBay_List[newBayIndex], bayIndex]  

        for obj in self.__m_modifierObjects :
            
            if not rs.IsObject(obj) : continue
            #look for falloff and bay data stored on curves name (with format: FALLOFF=float, BAY_LIST=integer)
            objData = rs.ObjectName(obj) 
            dataList = list(objData.rsplit("/"))
            FALLOFF = dblFalloffRadius

            for data in dataList : 
                if 'FALLOFF' in data: codeObj= compile(data,'<string>','single') ; eval(codeObj)
                
                        
            if FALLOFF > -1 : # a 0 value will skip the gradient check on current curve
            
                #get distance of current modifier object to current panel
                if rs.IsBrep(obj): #is a surface/polysurface?
                    closePoint = rs.BrepClosestPoint(obj, centerPoint)[0]
                    dist = rs.Distance(closePoint, centerPoint)
                    if  dist <= rs.VectorLength(midDist)*.1: flagPanel = True
                #is a curve?
                elif rs.IsCurve(obj): 
                    #if  a flat closed curve in same plane as panel catch all points inside.
                    if rs.IsCurveClosed(obj) and rs.IsCurvePlanar(obj) and rs.IsCurveInPlane(obj, panelPlane):
                        rs.ViewCPlane(plane=panelPlane)
                        if rs.PointInPlanarClosedCurve (centerPoint, obj): flagPanel = True
                        rs.ViewCPlane(plane=rs.WorldXYPlane())
                    if flagPanel == False: 
                        closePoint = rs.EvaluateCurve(obj, rs.CurveClosestPoint(obj, centerPoint))
                        distData = rs.Angle(closePoint, centerPoint, panelPlane)
                        dist = rs.Distance(closePoint, centerPoint)
                        if abs(distData[2])+sc.doc.ModelAbsoluteTolerance <=  abs(rs.Distance(ptPanel[0],ptPanel[1]))/2 and \
                            abs(distData[3])+sc.doc.ModelAbsoluteTolerance <=  abs(rs.Distance(ptPanel[1],ptPanel[3]))/2 : flagPanel = True
                        
                # Invalid object, skip
                else: continue 
            
            
            
                #RANDOMLY SELECT THE BLOCKS BASED ON THEIR PROXIMITY TO THE GRADIENT CENTERPOINT. 
                #dblDist = rs.Distance(rs.EvaluateCurve(obj, rs.CurveClosestPoint(obj, centerPoint)), centerPoint)
                if flagPanel == False and FALLOFF>0:
                    if rndVal > dist/FALLOFF : flagPanel = True
                    elif rndVal > dist-FALLOFF/rndVal/15 : flagPanel = True
            
            #replace bayindex data for this panel depending on data specified (generic or specifc index)
            if flagPanel :
                flagPanel = False
                PATTERN = []
                for data in dataList : 
                    if 'PATTERN' in data: 
                        codeObj= compile(data,'<string>','single') ; eval(codeObj) 
                        
                newBayIndex = self.__m_DataFunction.Run(PanelBay_List, PATTERN, level, inLevelIndex, defaultBayList, self.__m_randomObject, bayIndex, bayPanelIndex)        
                #return the new panel bay and keep bay index unchanged  
                     
        return [PanelBay_List[newBayIndex], bayIndex]   

        





designFunction = DesignFunction()
print "Done"
