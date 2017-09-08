


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
        SkinPanel_List: A list containing all the Panel objects used to generate the skin

"""

ghenv.Component.Name = "SkinShop_Replacer"
ghenv.Component.NickName = 'Replacer'
ghenv.Component.Message = 'VER 0.0.50\nApr_07_2016'
ghenv.Component.Category = "SkinShop"
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
    
    __m_ModifierCurves = None
    __m_functionCall = ''
    __m_FalloffRadius = 0
    __m_BayID_List = "BAY_LIST"
    __m_ImmuneBayID_List = []
    __m_RandomObject = None
    __m_RandomSeed = 1
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        if ModifierCurves : self.__m_ModifierCurves = ModifierCurves
        if Falloff : self.__m_FalloffRadius = Falloff 
        if BayID_List : self.__m_BayID_List = BayID_List
        if ImmuneBayID_List : self.__m_ImmuneBayID_List = ImmuneBayID_List
        self.__m_RandomObject = random.Random()    #Global Random generator object
        self.__m_RandomObject.seed(self.__m_RandomSeed)
        
        #----- functionCall valid skin parameters to us as inputs ------
        # myPanelBays: List of panel bay instances connected to skinGenerator
        # bayIndex : index of current bay in use from myPanelBays
        # bayPanelIndex :  index of current panel in use 
        # intCurrentLevel : Current level of cell being generated.
        # intCell_Index : Current index of cell being generated (matrix [x,y]= [intCurrentLevel, intCell_Index])
        # bayCornerPoints : corner points defining current bay cell location at skin
        # randomObj: Random object created on skin.
        # bayList : bay indices used in skin [1 based]
        
        
        self.__m_functionCall = "DesFunc_CurveGradient_Panel_Bays(myPanelBays, bayIndex," + str(self.__m_BayID_List)+", "+\
            str(self.__m_ImmuneBayID_List)+", "+ "bayList, bayCornerPoints , "+str(self.__m_FalloffRadius)+")"
            
    def RunString(self):
        return self.__m_functionCall
        
    #Selection of panel bay base on proximity to modifier curves
    def DesFunc_CurveGradient_Panel_Bays(self, PanelBay_List, bayIndex, bayCurveIndexList, bayStayIndexList, defaultBayList, ptPanel, dblFalloffRadius):

        #check if bayindex should not be changed (bayStayList)
        validBayStayList = copy.deepcopy(bayStayIndexList)
        for i in range(len(validBayStayList)) : validBayStayList[i] -= 1 #convert to cero based list
        if bayIndex in validBayStayList : return [PanelBay_List[bayIndex], bayIndex]
        
        newBayIndex = bayIndex # new bay index used to return new bay object
        bayCurveIndex = bayCurveIndexList[self.__m_RandomObject.randint(0,len(bayCurveIndexList)-1)]#randomly select one bay from list to be used if function is true. 
        bayCurveIndex-= 1 # convert from 1 to 0 based index value
        
        # Define new current bay index based on the valid bays listed (or not)
        #validBayList = copy.deepcopy(defaultBayList)        
        #if  validBayList:
            #for i in range(len(validBayList)) : validBayList[i] -=1
        #else: validBayList = range(len(PanelBay_List))
        
        # Filter with default bay list
        #while True:
            #if  bayIndex in validBayList : break
            #bayIndex +=1
            #if bayIndex == len(PanelBay_List) : bayIndex = min(validBayList)
                
        
        rndVal = self.__m_RandomObject.random()# 0-1 random base value for algorithm
        
        #obtain panel center point to evaluate
        midDist = rs.VectorScale(rs.VectorCreate(ptPanel[3],ptPanel[0]),.5)
        centerPoint = rs.PointAdd(ptPanel[0], midDist)  
        
        #multiple curves can be tested simultaneosly with algorithm
        dblDist = 0 ; flagPanel = False
        panelPlane=rs.PlaneFromPoints(ptPanel[0], ptPanel[1], ptPanel[2]) #panel bay plane
   
        
        for strCurve in self.__m_ModifierCurves :
            
            if not rs.IsObject(strCurve) or not rs.IsCurve(strCurve) : continue #check that curve exists.
            
            if not rs.IsCurveInPlane(strCurve, panelPlane):  continue #exclude curves if not on same plane as panel bay

            #look for falloff and bay data stored on curves name (with format: FALLOFF=float, BAY_LIST=integer)
            objData = rs.ObjectName(strCurve) 
            dataList = list(objData.rsplit("/"))
            FALLOFF = dblFalloffRadius

            for data in dataList : 
                if 'FALLOFF' in data: codeObj= compile(data,'<string>','single') ; eval(codeObj)
                
            #if curve is closed all panels inside curve will be flagged to change
            if FALLOFF > -1  and rs.IsCurveClosed(strCurve):
                rs.ViewCPlane(plane=panelPlane)
                if rs.PointInPlanarClosedCurve (centerPoint, strCurve): flagPanel = True
                rs.ViewCPlane(plane=rs.WorldXYPlane())
                        
            if FALLOFF > 0 : # a 0 value will skip the gradient check on current curve
                #RANDOMLY SELECT THE BLOCKS BASED ON THEIR PROXIMITY TO THE GRADIENT CENTERPOINT. 
                dblDist = rs.Distance(rs.EvaluateCurve(strCurve, rs.CurveClosestPoint(strCurve, centerPoint)), centerPoint)
                if rndVal > dblDist/FALLOFF : flagPanel = True 
                elif rndVal > dblDist-FALLOFF/rndVal/15 : flagPanel = True
            
            #replace bayindex data for this panel depending on data specified (generic or specifc index)
            if flagPanel :
                flagPanel = False # ; #BAY_LIST = bayCurveIndex    
                for data in dataList : 
                    if 'BAY_LIST' in data: 
                        codeObj= compile(data,'<string>','single') ; eval(codeObj) 
                        if type(BAY_LIST) == ListType: bayCurveIndex = BAY_LIST[self.__m_RandomObject.randint(0,len(BAY_LIST)-1)]-1
                        else: bayCurveIndex = BAY_LIST
                #return the new panel bay and keep bay indexUnchanged        
                newBayIndex = bayCurveIndex                       
        
        #return 
        return [PanelBay_List[newBayIndex], bayIndex]   

        
        





DesignFunction = DesignFunction()
print "Done"
