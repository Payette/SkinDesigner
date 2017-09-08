


# By Santiago Garay
# Skin Generator

"""
Use this component to apply a Layout Design Function to a SkinGenerator component.

    Args:
        _dataFunctionL: A dataFunction object created by Layout Data Function components such as DataPattern or DataRandom components.
        excludeBayIDs: A list of integers representing the panel bays ID numbers (based on their input number in SkinGenerator) that will not be affected by the Layout Design Function.
        modifierGeometry : A list of geometry objects that limit the area of application of the Desgin Function on the SkinGenerator surfaces. Grasshopper Surface, polysurface and curve types are accepted as well as Rhino scene ID versions of these geometry types. If no modifier geometry is specified, the algorithm is aplied on all SkinGenerator surfaces.
        modifierFalloff: A floating point number that specifies the falloff or blending between the modified and unmodified areas created by the modifier objecs. The default value is 0.0
    Returns:
        designFunction: A designFunction object to be connected to the SkinGenerator component.

"""

ghenv.Component.Name = "SkinDesigner_LayoutFunction"
ghenv.Component.NickName = 'LayoutFunction"'
ghenv.Component.Message = 'VER 0.0.63\nAug_02_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import Grasshopper.Kernel as gh
import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc
from types import *
import random
import copy
import math
import System

SGLibDesignFunction = sc.sticky["SGLib_DesignFunction"]



class LayoutDesignFunction(SGLibDesignFunction):
    
    __m_modifierObjects = []
    __m_functionCall = ''
    __m_functionType = ''
    __m_falloffRadius = 0
    __m_inmuneBayID_List = []
    __m_randomObject = None
    __m_randomSeed = 1
    __m_DataFunction = None
    warningData = []
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        
        sc.doc = rc.RhinoDoc.ActiveDoc

        self.__m_functionType = 'Layout'
        if modifierGeometry : self.__m_modifierObjects = modifierGeometry
            
            
        for index, obj in enumerate(self.__m_modifierObjects) :
            try:
                if type(obj) == System.Guid:
                    if  not rs.IsObject(obj) : 
                        self.warningData.append("Invalid 'modifierGeometry' value at #"+ str(index+1))
                        self.__m_modifierObjects[index] = None
                        continue
                    objData = rs.ObjectName(obj) #extract data if any
                    geo = rc.DocObjects.ObjRef(obj).Brep()
                    if geo == None : geo = rc.DocObjects.ObjRef(obj).Curve()
                    geo.SetUserString('Data', objData)
                    self.__m_modifierObjects[index] = geo
                else: obj.SetUserString('Data', "")
            except:
                self.warningData.append("Invalid 'modifierGeometry' value at #"+ str(index+1))
                self.__m_modifierObjects[index] = None
                continue
        try: 
            while True: self.__m_modifierObjects.remove(None)
        except: pass
        
        if modifierFalloff <> None : self.__m_falloffRadius = modifierFalloff 
        if excludeBayIDs : self.__m_inmuneBayID_List = excludeBayIDs
        self.__m_randomObject = random.Random()    #Global Random generator object
        self.__m_randomObject.seed(self.__m_randomSeed)

        if _dataFunctionL:
            if _dataFunctionL.__class__.__name__ <> "LayoutDataFunction":
                self.warningData.append("Invalid 'dataFunction' input")
                self.__m_DataFunction = None
            else : self.__m_DataFunction = _dataFunctionL
        else: self.warningData.append("Missing 'dataFunction' input")
        sc.doc = ghdoc
        
        
    def IsLayoutType(self):
        if self.__m_functionType == 'Layout': return True
        return False
        
        
    def IsPanelType(self):
        if self.__m_functionType == 'Panel': return True
        return False        

    def Reset(self):
        if self.__m_DataFunction: 
            param = self.__m_DataFunction.GetParameter('RandomSeed')
            if param : self.__m_randomObject.seed(param)
        
        
    #Selection of panel bay base on proximity to modifier curves
    #Refer to Skin API for skinInstance properties available (GetProperty and GetCellProperty)     
    def Run(self, PanelBay_List, currentBay, skinInstance):
        modDistTolerance = 0.1
        level = skinInstance.GetProperty("SKIN_CURRENT_CELL_ROW")  
        inLevelIndex = skinInstance.GetProperty("SKIN_CURRENT_CELL_COLUMN") 
        bayIndex = skinInstance.GetProperty("SKIN_CURRENT_BAY_INDEX")
        ptPanel = skinInstance.GetCellProperty(level, inLevelIndex, "CELL_CORNER_POINTS")
        defaultBayList = skinInstance.GetProperty("BAY_LIST")
        
        # new bay index passed in to this function via currentBay, currentBay is modified by design functions when a panel bay has to be changed.
        # (bayIndex is the original bay index at this cell location before design functions potentialty changed it).
        newBayIndex = PanelBay_List.index(currentBay)  
        if self.__m_DataFunction == None : return [PanelBay_List[bayIndex], bayIndex]          
        
        #check if bayindex should not be changed (bayStayList)
        validBayStayList = copy.deepcopy(self.__m_inmuneBayID_List)
        for i in range(len(validBayStayList)) : validBayStayList[i] -= 1 #convert to cero based list
        if newBayIndex in validBayStayList : return [PanelBay_List[newBayIndex], bayIndex]
        
        
        rndVal = self.__m_randomObject.random()# 0-1 random base value for algorithm
        
        #obtain panel center point to evaluate
        midDist = rs.VectorScale(rs.VectorCreate(ptPanel[3],ptPanel[0]),.5)
        centerPoint = rs.PointAdd(ptPanel[0], midDist)  
      
        #multiple curves can be tested simultaneosly with algorithm
        dist = 0 ; flagPanel = False  
        panelWidth = abs(rs.Distance(ptPanel[0],ptPanel[1]))
        panelHeight = abs(rs.Distance(ptPanel[1],ptPanel[3]))
        panelPlane=rs.PlaneFromPoints(ptPanel[0], ptPanel[1], ptPanel[2]) #panel bay plane
        
        if self.__m_modifierObjects == [] :
            newBayIndex = self.__m_DataFunction.Run(PanelBay_List, [] , level, inLevelIndex,  defaultBayList, self.__m_randomObject, bayIndex, panelPlane) 
            return [PanelBay_List[newBayIndex], bayIndex]  
        
        for obj in self.__m_modifierObjects :
            
            #if not rs.IsObject(obj) : print "Invalid modifier object"; continue
            #look for falloff and bay data stored on curves name (with format: FALLOFF=float, BAY_LIST=integer)
            datalist =[]
            objData = obj.GetUserString('Data')
            dataList = list(objData.rsplit("/"))
            FALLOFF = self.__m_falloffRadius
            for data in dataList : 
                if 'FALLOFF' in data: codeObj= compile(data,'<string>','single') ; eval(codeObj)
                
            if FALLOFF > -1 : # a 0 value will skip the gradient check on current curve
            
                #is a curve?
                if obj.ObjectType == rc.DocObjects.ObjectType.Curve: 
                    #if  a flat closed curve in same plane as panel catch all points inside
                    if obj.IsClosed and obj.IsPlanar(sc.doc.ModelAbsoluteTolerance) and obj.IsInPlane(panelPlane, sc.doc.ModelAbsoluteTolerance):
                        result =  obj.Contains(centerPoint, panelPlane)
                        if result == rc.Geometry.PointContainment.Inside or result == rc.Geometry.PointContainment.Coincident : flagPanel = True
                    if flagPanel == False:
                        paramCurve = 0.0
                        success, paramCurve  = obj.ClosestPoint(centerPoint)
                        closePoint = obj.PointAt(paramCurve)
                        dist = abs((closePoint - centerPoint).Length)
                        if not obj.IsClosed: 
                            #open curves flag panels with distance to panel center point <1/2 panel size
                            heightDist = abs(closePoint.Z - centerPoint.Z)+ sc.doc.ModelAbsoluteTolerance 
                            widthDist = abs((closePoint - rc.Geometry.Point3d(centerPoint.X, centerPoint.Y, closePoint.Z)).Length) + sc.doc.ModelAbsoluteTolerance 
                            if heightDist < panelHeight/2 and widthDist < panelWidth/2: flagPanel = True
                    
                #is a surface/polysurface?
                elif obj.ObjectType == rc.DocObjects.ObjectType.Brep: 
                    #get distance of current modifier object to current panel center point
                    closePoint = obj.ClosestPoint(centerPoint)
                    dist = abs((closePoint - centerPoint).Length)
                    if dist < sc.doc.ModelAbsoluteTolerance + modDistTolerance  : flagPanel = True
                    
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
                newBayIndex = self.__m_DataFunction.Run(PanelBay_List, PATTERN, level, inLevelIndex, defaultBayList, self.__m_randomObject, bayIndex, panelPlane)        
        #return the new panel bay and keep bay index unchanged  
        return [PanelBay_List[newBayIndex], bayIndex]   

        





designFunction = LayoutDesignFunction()
if designFunction.warningData <> []: 
    for warning in designFunction.warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    
if "Invalid 'dataFunction' input" in designFunction.warningData or "Missing 'dataFunction' input" in designFunction.warningData : designFunction = None

print "Done"
