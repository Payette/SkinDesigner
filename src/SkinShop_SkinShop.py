


# By Santiago Garay
# Skin Generator Panel Class

"""
Use this component to 
_
_
To add more panels bays in the construction, simply zoom into the component and hit the lowest "+" sign that shows up on the input side.  To remove panels from the construction, zoom into the component and hit the lowest "-" sign that shows up on the input side.
-
    Args:


    Returns:


"""

ghenv.Component.Name = "SkinShop_SkinShop"
ghenv.Component.NickName = 'SkinShop'
ghenv.Component.Message = 'VER 0.0.61\nApr_07_2016'
ghenv.Component.Category = "SkinShop"
ghenv.Component.SubCategory = "01 | Construction"


import rhinoscriptsyntax as rs
import copy
from types import *
import scriptcontext as sc
import Rhino
import random
import math

#init set up global variables

sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
_UNIT_COEF = 1
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
sc.doc = ghdoc



class Panel:
    
    __m_strName = ""
    __m_dblHeight = 0           #: Wall Height
    __m_dblWidth = 0            #: Wall Width
    __m_dblWallThickness = 0    #: Wall Depth
    
    __m_arrDeformBox = []
    __m_arrBoundingBox = []
    __m_blnShowDeform = 0
    __m_TransformMatrix = []
    
    __m_ConditionalDefinitions = {}
    
    __m_arrBlockInstances = [] 
    __m_strDrawMode = ""
    #--------------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    #Wall Parameters
    __m_blnShowWall = 0
    __m_arrWallObjects = 0
    #--------------------------------------------------------
    #Window Parameters
    __m_blnShowWindow = 0
    __m_arrWindowPoints = [] #: 4 Points make Glass Surface
    __m_dblWinGlassThickness = 0    #: Glass Thickness
    __m_dblWinGlassOffset = 0       #: Distance From Outer Surface of Glass to Outer Surface of Wall
    __m_arrWindowObjects = 0
    __m_arrWindowUserData = []
    #--------------------------------------------------------
    #Wall Cover Parameters
    __m_blnShowPane = 0    #: ON and OFF Wall Cover
    __m_dblPaneThickness = 0   #: Wall Cover Thickness
    __m_dblPaneOffset = 0  #: Distance of Wall from Wall Behind, It should be >= 0
    __m_dblPaneOffsetEdge = 0
    __m_arrPaneObjects = 0
    __m_strPaneName = 0    #: To Name Wall Cover Layer
    __m_dblPaneTileWidth = 0
    __m_dblPaneTileHeight = 0
    __m_dblPaneTileThickness = 0
    __m_dblPaneTileGap = 0
    #--------------------------------------------------------
    
    #Mulions Parameters
    __m_blnShowMullions = 0
    __m_blnShowMullionsCap = 0
    __m_dblMullionWidth = 0
    __m_dblMullionThickness = 0
    __m_dblMullionCapThickness = 0
    
    __m_arrMullionVertObjects = []
    __m_arrMullionHorObjects = []
    __m_arrMullionVertUserData = []
    __m_arrMullionHorUserData = []
    
    #-----------------------------------------------------------------------------
    #Shading Parameters
    __m_blnShowShading = 0
    __m_arrShadingObjects = []
    __m_arrShadingUserData = []
    #-----------------------------------------------------------------------------
    #CustomGeometry Paramters
    __m_blnShowCustomGeo = 0
    __m_brepCustomGeo = 0
    __m_brepCustomGeoObject = 0
    __m_vecPlacement = 0
    __m_vecScaleFactors = 0
    __m_vecUpVector = 0
    __m_blnTilable = False
    __m_dblRotation = 0
    __m_brepCustomWindowGeo = 0
    
    #-----------------------------------------------------------------------------
    #LadybugParameters
   
    __m_arrLadybugData = []
    __m_LadybugShadeThresh = 0.0
    
    #Other
    __rhObjectSurface = 8       #:Parameters for Boolean
    __rhObjectPolysurface = 16  #:Parameters for Boolean
    __m_unitCoef = 1 #meter is default unit
    __m_dimRoundCoef = 0 
    
    #----------------------------------------------------------------------------------------------------------------------
    #CONSTRUCTOR ----------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        
        #Doc Parameters
        self.__m_unitCoef = _UNIT_COEF #Coeficient used to adjust dimensions used inside Panel Class (Meter is 1)
        self.__m_dimRoundCoef = 1.01  #Coeficient ot absorb panel grid dimensions rounding errors
        
        #Panel parameters
        self.__m_strName = ""
        self.__m_arrBlockInstances=[]
        self.__m_strDrawMode = "DEFAULT"
        
        #Wall Default Parameters
        self.__m_dblHeight = 3.5 * self.__m_unitCoef
        self.__m_dblWidth = 1.5 * self.__m_unitCoef
        self.__m_dblWallThickness = 0.1 * self.__m_unitCoef
        self.__m_blnShowWall = True
        self.__m_arrWallObjects = [0]
        
        #Pane Parameters (default feet units)
        self.__m_strPaneName = "Default-Pane"
        self.__m_dblPaneThickness = 0.02 * self.__m_unitCoef
        self.__m_dblPaneOffset = 0.06 * self.__m_unitCoef
        self.__m_dblPaneOffsetEdge = 0
        self.__m_blnShowPane = False
        self.__m_arrPaneObjects = [0]
        self.__m_dblPaneTileWidth = 0
        self.__m_dblPaneTileHeight = 0
        self.__m_dblPaneTileThickness = 0
        self.__m_dblPaneTileGap = 0
    
        #Window
        self.__m_arrWindowPoints = [0,0,0,0]
        self.__m_arrWindowObjects = [0]
        self.__m_blnShowWindow = False
        self.__m_arrWindowUserData = dict(width=0, height=0, fromLeft=0, fromBottom=0, recess = 0, thickness = 0)
         
        #Mulions Parameters (default feet units)
        self.__m_dblMullionWidth = 0.05 * self.__m_unitCoef
        self.__m_dblMullionThickness = 0.1 * self.__m_unitCoef
        self.__m_dblMullionCapThickness = 0.05 * self.__m_unitCoef
        self.__m_blnShowMullions = False
        self.__m_blnShowMullionsCap = False
        
        #Initialize mullion data
        self.__m_arrMullionHorObjects = [0]
        self.__m_arrMullionVertObjects = [0]
        self.__m_arrMullionHorObjects[0] = [0]
        self.__m_arrMullionVertObjects[0] = [0]
        
        self.__m_arrMullionVertUserData = [[],[],[],[],[]]
        self.__m_arrMullionHorUserData = [[],[],[],[],[]]
        
        
        #Init Shading data
        self.__m_blnShowShading = False
        self.__m_arrShadingObjects = [0]
        self.__m_arrShadingUserData = [[],[],[],[],[],[],[],[],[]]
        #--------------------------------------------------------
        #Deform Paramters
        
        self.__m_arrDeformBox=[]
        self.__m_arrBoundingBox=[]
        self.__m_blnShowDeform = False
        self.__m_arrBoundingBox = self.__ResetBoundingBox()
        
        self.__m_ConditionalDefinitions = dict()
        #----------------------------------------------------------------------------
        
        #CustomGeometry Paramters
        self.__m_blnShowCustomGeo = 0
        self.__m_brepCustomGeo = 0
        self.__m_brepCustomGeoObject = 0
        self.__m_vecPlacement = Rhino.Geometry.Vector3d(0,0,0)
        self.__m_vecScaleFactor = Rhino.Geometry.Vector3d(1,1,1)
        self.__m_vecUpVector = Rhino.Geometry.Vector3d(0,0,1)
        self.__m_blnTilable = False
        self.__m_dblRotation = 0
        self.__m_brepCustomWindowGeo = 0
        
        #-----------------------------------------------------------------------------        
        #Ladybug Parameters
        self.__m_LadybugShadeThresh = 0.1 * self.__m_unitCoef   # min value (in meters) for shading/mullions caps to be created in "LADYBUG"  draw mode)
        
        
        #---------------------------------------------------------------------
        rs.AddLayer ("_P_0") 
        rs.AddLayer ("_P_Glass")        #: To Create in "_P_Glass" Layer
        rs.AddLayer ("_P_Wall")          #: To Create Wall in "_P_Wall" Layer
        rs.AddLayer ("_P_Mullions")   
        rs.AddLayer ("_P_Shading")
        rs.AddLayer ("_P_CustomGeo")
        #---------------------------------------------------------------------
        
    def __del__(self):
        #print "adios!"
        pass
        
        
    #----------------------------------------------------------------------------------------------------------------------
    #--------PROPERTIES SECTION------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def GetName(self):
        return self.__m_strName        
        
    def SetName(self, someName):
        self.__m_strName = someName
        
    def GetHeight(self):
        return self.__m_dblHeight
        
    def Height(self, someHeight):

        if type(someHeight) == StringType : someHeight = eval(someHeight)
        
        if someHeight <= 0 : return
        self.__m_dblHeight = someHeight
        self.__m_arrBoundingBox = self.__ResetBoundingBox()
                
        self.UpdateWindow() #Check if window does fit in panel
        
        
    def GetWidth(self):
        return self.__m_dblWidth
        
        
    def Width(self, someWidth):
        
        if someWidth <= 0 : return
        
        if type(someWidth) == StringType : someWidth = eval(someWidth)
        
        self.__m_dblWidth = someWidth
        self.__m_arrBoundingBox = self.__ResetBoundingBox()
        
        self.UpdateWindow() #Check if window does fit in panel
        
        
    def GetThickness(self):
        return self.__m_dblWallThickness
        
        
    def Thickness(self, someThickness):
        
        if type(someThickness) == StringType : someThickness = eval(someThickness)
        
        if someThickness == 0 : 
            self.__m_dblWallThickness = 0.001
        else: self.__m_dblWallThickness = someThickness
        
        self.__m_arrBoundingBox = self.__ResetBoundingBox()
        
        
    def SetDrawMode(self, strMode):
        if strMode in ["DEFAULT", "LADYBUG"] : self.__m_strDrawMode = strMode
        
    def GetDrawMode(self):
        return self.__m_strDrawMode
        
    def PanelProperty(self, strPropName):

        PanelProperty = None
        
        #Panel Data        
        if strPropName == "PanelHeight":
            PanelProperty = self.__m_dblHeight
        elif strPropName ==  "PanelWidth":
            PanelProperty = self.__m_dblWidth
        #Wall Data
        elif strPropName ==  "PanelThickness":
            PanelProperty = self.__m_dblWallThickness
        elif strPropName ==  "WallVisibility":
            PanelProperty = self.__m_blnShowWall
        elif strPropName ==  "WallObjects":
            PanelProperty = self.__m_arrWallObjects
        #Deform Data
        elif strPropName == "BoundingBox":
            PanelProperty = self.__m_arrBoundingBox
        elif strPropName ==  "DeformVisibility":
            PanelProperty = self.__m_blnShowDeform
        elif strPropName ==  "DeformBox":
            PanelProperty = self.__m_arrDeformBox
       #Blocks Data
        elif strPropName == "BlockInstances":
            PanelProperty = self.__m_arrBlockInstances
       #Pane Data
        elif strPropName ==  "PaneName":
            PanelProperty = self.__m_strPaneName
        elif strPropName ==  "PaneVisibility":
            PanelProperty = self.__m_blnShowPane
        elif strPropName ==  "PaneThickness":
           PanelProperty = self.__m_dblPaneThickness
        elif strPropName ==  "PaneOffset":
            PanelProperty = self.__m_dblPaneOffset
        elif strPropName ==  "PaneOffsetEdge":
            PanelProperty = self.__m_dblPaneOffsetEdge
        elif strPropName ==  "PaneObjects":
            PanelProperty = self.__m_arrPaneObjects
        elif strPropName ==  "PaneTileWidth":
            PanelProperty = self.__m_dblPaneTileWidth 
        elif strPropName ==  "PaneTileHeight":
            PanelProperty = self.__m_dblPaneTileHeight
        elif strPropName ==  "PaneTileThickness":
            PanelProperty = self.__m_dblPaneTileThickness
        elif strPropName ==  "PaneTileGap":
            PanelProperty = self.__m_dblPaneTileGap
        #Window Data
        elif strPropName ==  "WindowPoints":
            PanelProperty = self.__m_arrWindowPoints 
        elif strPropName ==  "WindowVisibility":
           PanelProperty = self.__m_blnShowWindow
        elif strPropName ==  "WindowGlassThickness":
            PanelProperty = self.__m_dblWinGlassThickness
        elif strPropName ==  "WindowGlassOffset":
            PanelProperty = self.__m_dblWinGlassOffset
        elif strPropName ==  "WindowObjects":
           PanelProperty = self.__m_arrWindowObjects
        elif strPropName == "WindowWidth":
            PanelProperty = self.__m_arrWindowPoints[1][0]-self.__m_arrWindowPoints[0][0]
        elif strPropName == "WindowHeight":
            PanelProperty = self.__m_arrWindowPoints[2][2]-self.__m_arrWindowPoints[1][2]
        elif strPropName == "WindowBottom":
            PanelProperty = self.__m_arrWindowPoints[0][2]
        elif strPropName == "WindowTop":
            PanelProperty = self.GetHeight()-self.__m_arrWindowPoints[2][2]
        elif strPropName == "WindowLeft":
            PanelProperty = self.__m_arrWindowPoints[0][0]
        elif strPropName == "WindowRight":
            PanelProperty = self.GetWidth()-self.__m_arrWindowPoints[1][0]
        elif strPropName == "WindowData":
            PanelProperty = self.__m_arrWindowUserData
        #Mullion Data
        elif strPropName ==  "MullionWidth":
            PanelProperty = self.__m_dblMullionWidth
        elif strPropName ==  "MullionThickness":
            PanelProperty = self.__m_dblMullionThickness
        elif strPropName ==  "MullionCapThickness":
            PanelProperty = self.__m_dblMullionCapThickness
        elif strPropName ==  "MullionVisibility":
            PanelProperty = self.__m_blnShowMullions 
        elif strPropName ==  "MullionCapVisibility":
            PanelProperty = self.__m_blnShowMullionsCap
        elif strPropName ==  "MullionHorNum":
            PanelProperty = len(self.__m_arrMullionHorObjects)
        elif strPropName ==  "MullionVertNum":
           PanelProperty = len(self.__m_arrMullionVertObjects)
        elif strPropName ==  "MullionHorDataNum":
            PanelProperty = len(self.__m_arrMullionHorUserData)
        elif strPropName ==  "MullionVertDataNum":
            PanelProperty = len(self.__m_arrMullionVertUserData)
        #Shading Data
        elif strPropName ==  "ShadingVisibility":
            PanelProperty = self.__m_blnShowShading 
        elif strPropName ==  "ShadingObjects":
           PanelProperty = self.__m_arrShadingObjects
        elif strPropName ==  "ShadingDataNum":
            PanelProperty = len(self.__m_arrShadingUserData)    
        elif strPropName ==  "ConditionalDefinitions":
            PanelProperty = self.__m_ConditionalDefinitions
        #CustomGeometry Parameters
        elif strPropName == "CustomGeoVisibility":
            PanelProperty = self.__m_blnShowCustomGeo
        elif strPropName == "CustomGeoBrep":
            PanelProperty = self.__m_brepCustomGeo
        elif strPropName == "CustomGeoPlacement":
            PanelProperty = self.__m_vecPlacement 
        elif strPropName == "CustomGeoScaleFactor":
            PanelProperty = self.__m_vecScaleFactor
        elif strPropName == "CustomGeoUpVector":
            PanelProperty = self.__m_vecUpVector
        elif strPropName == "CustomGeoTilable":
            PanelProperty = self.__m_blnTilable
        elif strPropName == "CustomGeoRotation":
            PanelProperty = self.__m_dblRotation
        elif strPropName == "CustomGeoWindowBrep":
            PanelProperty = self.__m_brepCustomWindowGeo

        return PanelProperty
        
            
    def PanelPropertyArray(self, strPropName, arrayIndex):
        
        if strPropName ==  "MullionHorObjArray":
            PanelPropertyArray = self.__m_arrMullionHorObjects[arrayIndex]
        elif strPropName ==  "MullionVertObjArray":
            PanelPropertyArray = self.__m_arrMullionVertObjects[arrayIndex]
        elif strPropName ==  "MullionHorDataArray":
            PanelPropertyArray = self.__m_arrMullionHorUserData[arrayIndex]
        elif strPropName ==  "MullionVertDataArray":
            PanelPropertyArray = self.__m_arrMullionVertUserData[arrayIndex]
        elif strPropName ==  "ShadingDataArray":
            PanelPropertyArray = self.__m_arrShadingUserData[arrayIndex]
            
        return PanelPropertyArray
        
            
    def __ResetBoundingBox(self):
        return [[0, 0, 0], [self.__m_dblWidth, 0, 0], [self.__m_dblWidth, self.__m_dblWallThickness, 0], \
            [0, self.__m_dblWallThickness, 0], [0, 0, self.__m_dblHeight], [self.__m_dblWidth, 0, self.__m_dblHeight], \
            [self.__m_dblWidth, self.__m_dblWallThickness, self.__m_dblHeight], [0, self.__m_dblWallThickness, self.__m_dblHeight]]
            
            
    #----------------------------------------------------------------------------------------------------------------------
    #--------UTILITIES SECTION------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    #Copy properties (not geometry) of provided panel
    
    def Copy(self, myPanel):
        
        #General panel properties
        self.__m_strName = myPanel.GetName()
        self.__m_dblHeight = myPanel.PanelProperty("PanelHeight") #: Wall Height
        self.__m_dblWidth = myPanel.PanelProperty("PanelWidth") # Wall Width             
        self.__m_strDrawMode = myPanel.GetDrawMode()
        self.__m_ConditionalDefinitions = copy.deepcopy(myPanel.PanelProperty("ConditionalDefinitions"))
        
        #Wall properties
        self.__m_dblWallThickness = myPanel.PanelProperty("PanelThickness") #: Wall Depth
        self.__m_blnShowWall = myPanel.PanelProperty("WallVisibility")
        
        #Pane parameters
        self.__m_blnShowPane = myPanel.PanelProperty("PaneVisibility")
        self.__m_strPaneName = myPanel.PanelProperty("PaneName")
        self.__m_dblPaneThickness = myPanel.PanelProperty("PaneThickness")
        self.__m_dblPaneOffset = myPanel.PanelProperty("PaneOffset")
        self.__m_dblPaneOffsetEdge = myPanel.PanelProperty("PaneOffsetEdge")
        
        self.__m_dblPaneTileWidth  = myPanel.PanelProperty("PaneTileWidth")
        self.__m_dblPaneTileHeight = myPanel.PanelProperty("PaneTileHeight")
        self.__m_dblPaneTileThickness = myPanel.PanelProperty("PaneTileThickness")
        self.__m_dblPaneTileGap = myPanel.PanelProperty("PaneTileGap")
        
        
        #Window Parameters
        self.__m_blnShowWindow = myPanel.PanelProperty("WindowVisibility") 
        self.__m_dblWinGlassThickness = myPanel.PanelProperty("WindowGlassThickness")
        self.__m_dblWinGlassOffset = myPanel.PanelProperty("WindowGlassOffset")
        self.__m_arrWindowPoints = copy.deepcopy(myPanel.PanelProperty("WindowPoints"))
        self.__m_arrWindowUserData = copy.deepcopy(myPanel.PanelProperty("WindowData"))

        #Mullion Parameters
        self.__m_blnShowMullions = myPanel.PanelProperty("MullionVisibility") 
        self.__m_blnShowMullionsCap = myPanel.PanelProperty("MullionCapVisibility")
        self.__m_dblMullionWidth = myPanel.PanelProperty("MullionWidth")
        self.__m_dblMullionThickness = myPanel.PanelProperty("MullionThickness") 
        self.__m_dblMullionCapThickness = myPanel.PanelProperty("MullionCapThickness") 

        #Copy mullions Data
        
        self.__m_arrMullionVertUserData = []
        self.__m_arrMullionHorUserData = []
        
        for i in range(myPanel.PanelProperty("MullionHorDataNum")):
            arrMullions = copy.deepcopy(myPanel.PanelPropertyArray("MullionHorDataArray", i))
            if type(arrMullions) == ListType :
                self.__m_arrMullionHorUserData.append(arrMullions)
                
        for i in range(myPanel.PanelProperty("MullionVertDataNum")):
            arrMullions = copy.deepcopy(myPanel.PanelPropertyArray("MullionVertDataArray", i))
            if type(arrMullions) == ListType :
                self.__m_arrMullionVertUserData.append(arrMullions)
                
                
        #Copy Shading objects
        
        self.__m_blnShowShading = myPanel.PanelProperty("ShadingVisibility") 
            
        #Copy Shading Data
        self.__m_arrShadingUserData = []
        for i in range(myPanel.PanelProperty("ShadingDataNum")):
            arrShadingData = copy.deepcopy(myPanel.PanelPropertyArray("ShadingDataArray", i))
            if type(arrShadingData) == ListType :
                self.__m_arrShadingUserData.append(arrShadingData)
                
        #CustomGeometry Parameters
        self.__m_blnShowCustomGeo = myPanel.PanelProperty("CustomGeoVisibility")
        self.__m_brepCustomGeo = myPanel.PanelProperty("CustomGeoBrep")
        self.__m_vecPlacement = myPanel.PanelProperty("CustomGeoPlacement")
        self.__m_vecScaleFactor = myPanel.PanelProperty("CustomGeoScaleFactor")
        self.__m_vecUpVector = myPanel.PanelProperty("CustomGeoUpVector")
        self.__m_blnTilable = myPanel.PanelProperty("CustomGeoTilable")
        self.__m_dblRotation = myPanel.PanelProperty("CustomGeoRotation")
        self.__m_brepCustomWindowGeo = myPanel.PanelProperty("CustomGeoWindowBrep")


        #Deform parameters
        self.__m_arrDeformBox = copy.deepcopy(myPanel.PanelProperty("DeformBox")) # Wall Location
        self.__m_arrBoundingBox = copy.deepcopy(myPanel.PanelProperty("BoundingBox"))
        self.__m_blnShowDeform = myPanel.PanelProperty("DeformVisibility")
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    
    

    def CreateBlockCopy(self, strBlockName, arrAreaPanelPoints):
        
        blnNewBlock = False
        
        #create block if not created already
        if not rs.IsBlock(strBlockName) :
            
            blnNewBlock = True
            arrBlockObjects = []

            if  self.__m_arrWallObjects and not type(self.__m_arrWallObjects[0]) == IntType and rs.IsObject(self.__m_arrWallObjects[0]):
                arrBlockObjects += self.__m_arrWallObjects

            if  self.__m_arrWindowObjects and not type(self.__m_arrWindowObjects[0]) == IntType and rs.IsObject(self.__m_arrWindowObjects[0]):
                arrBlockObjects +=  self.__m_arrWindowObjects
            
            if  self.__m_arrPaneObjects and not type(self.__m_arrPaneObjects[0]) == IntType and rs.IsObject(self.__m_arrPaneObjects[0]):
                arrBlockObjects += self.__m_arrPaneObjects

            for i in range(self.PanelProperty("MullionHorNum")):
                arrMullions = self.PanelPropertyArray("MullionHorObjArray", i)
                if arrMullions and not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                    arrBlockObjects += arrMullions

            for i in range(self.PanelProperty("MullionVertNum")):
                arrMullions = self.PanelPropertyArray("MullionVertObjArray", i)
                if arrMullions and not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                    arrBlockObjects += arrMullions

            if self.__m_arrShadingObjects and not type(self.__m_arrShadingObjects[0]) == IntType and rs.IsObject(self.__m_arrShadingObjects[0]):
                arrBlockObjects +=  self.__m_arrShadingObjects
            
            if not type(self.__m_brepCustomGeoObject) == IntType and rs.IsObject(self.__m_brepCustomGeoObject):
                arrBlockObjects +=  [self.__m_brepCustomGeoObject]
            
            
            rs.AddBlock(arrBlockObjects, self.__m_arrBoundingBox[0], strBlockName)
        
        
        #Translate and Scale based on grid points
        
        #Start from Panel Original Bounding Box
        arrBoxPoints = self.__m_arrBoundingBox
        
        #Move Bounding Box to new locatation Plane (to avoid panel depth distortions)
        arrStartPlane = rs.PlaneFromPoints(arrBoxPoints[0], arrBoxPoints[1], arrBoxPoints[4]) #Create Plane from current Boundng Box points
        arrEndPlane = rs.PlaneFromPoints(arrAreaPanelPoints[0], arrAreaPanelPoints[1], arrAreaPanelPoints[2])#Create Plane from Panels Area points
        
        #Apply Transf. Matrix from planes on Bounding Box
        arrXform = rs.XformRotation1(arrStartPlane, arrEndPlane)
        arrNewBoxPoints = rs.PointArrayTransform(arrBoxPoints, arrXform)
        
        arrScaleXform = rs.XformScale([(rs.Distance(arrNewBoxPoints[0], arrAreaPanelPoints[1]) / rs.Distance(arrNewBoxPoints[0], arrNewBoxPoints[1])), 1,\
            (rs.Distance(arrNewBoxPoints[0], arrAreaPanelPoints[2]) / rs.Distance(arrNewBoxPoints[0], arrNewBoxPoints[4]))])
        arrXform = rs.XformMultiply(arrXform, arrScaleXform)
        
        
        #Create Copy and move to location
        if rs.IsBlock(strBlockName) :
            self.__m_arrBlockInstances.append(rs.InsertBlock2(strBlockName, arrXform))
    
        return blnNewBlock
    
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------

    def DeleteBlockCopies(self):

        if self.__m_arrBlockInstances :
            
            if rs.IsBlockInstance(self.__m_arrBlockInstances[0]):
                rs.BlockInstanceName(self.__m_arrBlockInstances[0])
                rs.DeleteBlock(rs.BlockInstanceName(self.__m_arrBlockInstances[0]))
                
            __m_arrBlockInstances = []

    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------

    def DeleteObjects(self):

        if  type(self.__m_arrWallObjects) == ListType and not type(self.__m_arrWallObjects[0]) == IntType and rs.IsObject(self.__m_arrWallObjects[0]): 
            rs.DeleteObjects(self.__m_arrWallObjects)
     
        if  self.__m_arrPaneObjects and not type(self.__m_arrPaneObjects[0]) == IntType and rs.IsObject(self.__m_arrPaneObjects[0]):
            rs.DeleteObjects(self.__m_arrPaneObjects)
             
        if  self.__m_arrWindowObjects and not type(self.__m_arrWindowObjects[0]) == IntType and rs.IsObject(self.__m_arrWindowObjects[0]): 
            rs.DeleteObjects(self.__m_arrWindowObjects)

        for i in range(self.PanelProperty("MullionHorNum")):
            arrMullions = self.PanelPropertyArray("MullionHorObjArray", i)
            if type(arrMullions) == ListType and not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                rs.DeleteObjects(arrMullions)
            
        for i in range(self.PanelProperty("MullionVertNum")):
            arrMullions = self.PanelPropertyArray("MullionVertObjArray", i)
            if type(arrMullions) == ListType and not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                rs.DeleteObjects(arrMullions)
                
        if  self.__m_arrShadingObjects and not type(self.__m_arrShadingObjects[0]) == IntType and rs.IsObject(self.__m_arrShadingObjects[0]): 
            rs.DeleteObjects(self.__m_arrShadingObjects)
            
        if not type(self.__m_brepCustomGeoObject) == IntType and rs.IsObject(self.__m_brepCustomGeoObject):
            rs.DeleteObject(self.__m_brepCustomGeoObject)

    #----------------------------------------------------------------------------------------------------------------------	 
    #PANEL TRANSFORMATION SECTION
    #----------------------------------------------------------------------------------------------------------------------
    
    #Distort/transform Morphing Bounding Box only, leave data ready for DrawMorph command
    def MorphPanel(self, arrAreaPanelPoints):
        
        
        #Start from Panel Original Bounding Box
        arrBoxPoints = self.__m_arrBoundingBox
        
        #Move Bounding Box to new locatation Plane (to avoid panel depth distortions)
        arrStartPlane = rs.PlaneFromPoints(arrBoxPoints[0], arrBoxPoints[1], arrBoxPoints[4]) #Create Plane from current Boundng Box points
        arrEndPlane = rs.PlaneFromPoints(arrAreaPanelPoints[0], arrAreaPanelPoints[1], arrAreaPanelPoints[2])#Create Plane from Panels Area points
        
        #Apply Transf. Matrix from planes on Bounding Box
        arrRotXform = rs.XformRotation1(arrStartPlane, arrEndPlane)
        arrNewBoxPoints = rs.PointArrayTransform(arrBoxPoints, arrRotXform)
        
        arrScaleXform = rs.XformScale([(rs.Distance(arrNewBoxPoints[0], arrAreaPanelPoints[1]) / rs.Distance(arrNewBoxPoints[0], arrNewBoxPoints[1])), 1.0,\
            (rs.Distance(arrNewBoxPoints[0], arrAreaPanelPoints[2]) / rs.Distance(arrNewBoxPoints[0], arrNewBoxPoints[4]))])
        arrXform = rs.XformMultiply(arrRotXform, arrScaleXform)
        
        self.__m_TransformMatrix = arrXform
        
        # Move panel corners to fill new area
        #TopLeft
        #arrTransVector = rs.VectorCreate(arrAreaPanelPoints[2], arrNewBoxPoints[4])
        #arrTransPointXform = rs.XformTranslation(arrTransVector)
        #arrNewBoxPoints[4] = rs.PointTransform(arrNewBoxPoints[4], arrTransPointXform)
        #arrNewBoxPoints[7] = rs.PointTransform(arrNewBoxPoints[7], arrTransPointXform)
        #TopRight
        #arrTransVector = rs.VectorCreate(arrAreaPanelPoints[3], arrNewBoxPoints[5])
        #arrTransPointXform = rs.XformTranslation(arrTransVector)
        #arrNewBoxPoints[5] = rs.PointTransform(arrNewBoxPoints[5], arrTransPointXform)
        #arrNewBoxPoints[6] = rs.PointTransform(arrNewBoxPoints[6], arrTransPointXform)
        #BottomRight'
        #arrTransVector = rs.VectorCreate(arrAreaPanelPoints[1], arrNewBoxPoints[1])
        #arrTransPointXform = rs.XformTranslation(arrTransVector)
        #arrNewBoxPoints[1] = rs.PointTransform(arrNewBoxPoints[1], arrTransPointXform)
        #arrNewBoxPoints[2] = rs.PointTransform(arrNewBoxPoints[2], arrTransPointXform)
        
        
        #Store new Bounding Box ready for Draw()
        self.__m_arrDeformBox = arrNewBoxPoints
        self.__m_blnShowDeform = True


    #----------------------------------------------------------------------------------------------------------------------	 
    #PANEL CONDITIONAL DEFINITIONS SECTION
    #Data Matrix with panel properties-based conditionals and Function-based Definitions (ex: "PanelWidth < 1.0", "DeleteWindow()")    
    #----------------------------------------------------------------------------------------------------------------------

    def AddConditionalDefinition(self, strCondition, strAction):
        
        
        if strCondition not in self.__m_ConditionalDefinitions:
            self.__m_ConditionalDefinitions[strCondition] = []
        self.__m_ConditionalDefinitions[strCondition].append(strAction)



    def DeleteConditionalDefinition(self, strCondition, strAction="All"):
        
        if strCondition not in self.__m_ConditionalDefinitions: return False
        
        if strAction == "All" : 
            del self.__m_ConditionalDefinitions[strCondition]
            return True
            
        tmpDefList = self.__m_ConditionalDefinitions[strCondition]
        if  strAction in tmpCondef : 
            tmpDefList.remove(strAction)
            return True
            
        return False
    
    
    
    def GetConditionalDefinition(self, strCondition="All"):
        if strCondition == "All":
            return copy.deepcopy(self.__m_ConditionalDefinitions)
        else: 
            return copy.deepcopy(self.__m_ConditionalDefinitions[strCondition])
    
    
    def RunConditionalDefinition(self, strCondition=None):
        
        conditionList = []
        if strCondition <> None:
            if strCondition not in self.__m_ConditionalDefinitions: return False
            conditionList = [strCondition]
        else: 
            conditionList = self.__m_ConditionalDefinitions.keys()
            
        for condition in conditionList:
            parsedList = condition.split()
            parsedCondition = "if self.PanelProperty('"+parsedList[0]+"') "+parsedList[1]+" "+parsedList[2]+" : "
            
            actionList = self.__m_ConditionalDefinitions[condition]
            for strAction in actionList:
                strConditionalAction = parsedCondition + "self." + strAction
                exec(strConditionalAction)
        
    #----------------------------------------------------------------------------------------------------------------------
    #--------ADDING/REMOVING/MODIFYING ELEMENTS SECTION------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
            
            
    def AddWindow(self, width=1*_UNIT_COEF, height=1*_UNIT_COEF, fromLeft="C", fromBottom="C", recess=0, thickness=0.02*_UNIT_COEF):
        
        self.__m_arrWindowUserData = dict(width=width, height=height, fromLeft=fromLeft, fromBottom=fromBottom, recess = recess, thickness = thickness)
        #Panel variables
        PanelWidth = self.GetWidth()
        PanelHeight = self.GetHeight()

        if type(width) == StringType : width = eval(width)
        if type(height) == StringType : height = eval(height)
        if type(recess) == StringType : recess = eval(recess)

        dblGlassWidth = width ; dblGlassHeight = height
        dblGlassThickness = thickness ; dblGlassRecess = recess
        
        #Window variables
        Window = dict(width=width, height=height, fromLeft=fromLeft, fromBottom=fromBottom, recess = recess, thickness = thickness)

        if type(fromLeft) is StringType :
            if fromLeft == 'C' : dblGlassDisLeft = (PanelWidth-width)/2.0
            else : dblGlassDisLeft = eval(fromLeft)
        elif type(fromLeft) is FloatType or type(fromLeft) is IntType :
            dblGlassDisLeft = fromLeft
        else: dblGlassDisLeft = (PanelWidth-width)/2.0
            
        if type(fromBottom) is StringType:
            if fromBottom == 'C' : dblGlassDisBottom = (PanelHeight-height)/2.0 
            else : dblGlassDisBottom = eval(fromBottom)
        elif type(fromBottom) is FloatType or type(fromBottom) is IntType :
            dblGlassDisBottom = fromBottom 
        else: dblGlassDisBottom = (PanelHeight-height)/2.0 
        
        #Check window dimensions, hide window if invalid
        if dblGlassWidth <= 0 or dblGlassHeight <= 0 or \
            (dblGlassDisLeft + dblGlassWidth) > self.PanelProperty("PanelWidth")*self.__m_dimRoundCoef or \
            dblGlassDisBottom + dblGlassHeight > self.PanelProperty("PanelHeight")*self.__m_dimRoundCoef: 
            self.HideWindow(); print " Window won't fit- erased"; return
                    
        #load processed data in window array
        self.__m_arrWindowPoints[0] = [dblGlassDisLeft, 0, dblGlassDisBottom]
        self.__m_arrWindowPoints[1] = [dblGlassDisLeft + dblGlassWidth, 0, dblGlassDisBottom]
        self.__m_arrWindowPoints[2] = [dblGlassDisLeft + dblGlassWidth, 0, dblGlassDisBottom + dblGlassHeight]
        self.__m_arrWindowPoints[3] = [dblGlassDisLeft, 0, dblGlassDisBottom + dblGlassHeight]
        self.__m_dblWinGlassThickness = dblGlassThickness
        self.__m_dblWinGlassOffset = dblGlassRecess
        
            
        self.ShowWindow()
        
        
    def ModifyWindow(self, newWidth=None, newHeight=None, newFromLeft=None, newFromBottom=None, newRecess=None, newThickness=None):
        if self.__m_arrWindowPoints == [0,0,0,0] : return False
        
        self.__m_arrWindowUserData['width'] = newWidth if newWidth else self.__m_arrWindowUserData['width'] 
        self.__m_arrWindowUserData['height'] = newHeight if newHeight else self.__m_arrWindowUserData['height'] 
        self.__m_arrWindowUserData['fromLeft'] = newFromLeft if newFromLeft else self.__m_arrWindowUserData['fromLeft'] 
        self.__m_arrWindowUserData['fromBottom'] = newFromBottom if newFromBottom else self.__m_arrWindowUserData['fromBottom'] 
        self.__m_arrWindowUserData['recess'] = newRecess if newRecess else self.__m_arrWindowUserData['recess']
        self.__m_arrWindowUserData['thickness'] = newThickness if newThickness else self.__m_arrWindowUserData['thickness']        
                                
        Window = self.__m_arrWindowUserData
        self.AddWindow(width=Window['width'], height=Window['height'], fromLeft=Window['fromLeft'], fromBottom=Window['fromBottom'], recess=Window['recess'], thickness=Window['thickness'])
        
        
        
    def UpdateWindow(self):
        if self.__m_arrWindowPoints == [0,0,0,0] : return False
        Window = self.__m_arrWindowUserData
        self.AddWindow(width=Window['width'], height=Window['height'], fromLeft=Window['fromLeft'], fromBottom=Window['fromBottom'], recess=Window['recess'], thickness=Window['thickness'])
        
        
    def DeleteWindow(self):
        self.HideWindow()
        self.__m_arrWindowPoints = [0,0,0,0]
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
        
    def AddPane(self, paneName="_P_DefaultPane", thickness=0.02*_UNIT_COEF, offset=0.02*_UNIT_COEF, offsetEdge=0, tileWidth=0, tileHeight=0, tileThickness=0, tileGap=0.01*_UNIT_COEF):
        
        self.__m_strPaneName = paneName
        self.__m_dblPaneThickness = thickness
        self.__m_dblPaneOffset = offset
        self.__m_dblPaneOffsetEdge = offsetEdge
        self.__m_dblPaneTileWidth = tileWidth
        self.__m_dblPaneTileHeight = tileHeight
        self.__m_dblPaneTileThickness = tileThickness
        self.__m_dblPaneTileGap = tileGap
        
        self.__m_blnShowPane = True


    #----------------------------------------------------------------------------------------------------------------------
    # Mullions Actions
    #----------------------------------------------------------------------------------------------------------------------
    def AddBaseMullions(self, width=0.05*_UNIT_COEF, thickness=0.1*_UNIT_COEF, capThickness=0.05*_UNIT_COEF):

        #Storing panel generic values using provided data
        if width > 0 : self.__m_dblMullionWidth = width
        if thickness > 0 : self.__m_dblMullionThickness = thickness
        
        #Caps also?
        
        if capThickness > 0.0 :
            self.__m_dblMullionCapThickness = capThickness
            self.__m_blnShowMullionsCap = True
        else :
            self.__m_blnShowMullionsCap = False
            
        if  self.__m_blnShowWindow :
            MullionTypes = ["PanelLeft", "PanelRight", "PanelBottom", "PanelTop", \
                "WindowLeft","WindowRight","WindowBottom","WindowTop"]
        else : MullionTypes = ["PanelLeft", "PanelRight", "PanelBottom", "PanelTop"]
            
            
        for strType in MullionTypes :
            self.AddMullionType(strType, width, thickness, width, capThickness)

        self.__m_blnShowMullions = True



    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def AddWindowMullions(self, width=0.05*_UNIT_COEF, thickness=0.1*_UNIT_COEF, capThickness=0.05*_UNIT_COEF):
        MullionTypes = ["WindowLeft","WindowRight","WindowBottom","WindowTop"]
        for strType in MullionTypes :
            self.AddMullionType(strType, width, thickness, width, capThickness)


    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def AddPanelMullions(self, width=0.05*_UNIT_COEF, thickness=0.1*_UNIT_COEF, capThickness=0.05*_UNIT_COEF):
        MullionTypes = ["PanelLeft", "PanelRight", "PanelBottom", "PanelTop"]
        for strType in MullionTypes :
            self.AddMullionType(strType, width, thickness, width, capThickness)
            
            

    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    #Use to add a predefined mullion Type

    def AddMullionType(self, type, width=0.05*_UNIT_COEF, thickness=0.1*_UNIT_COEF, capWidth=None, capThickness=0.05*_UNIT_COEF):

        if capWidth == None : capWidth = width 
        if "Bottom" in type or "Top" in type :
            self.__m_arrMullionHorUserData[0] = self.__m_arrMullionHorUserData[0] + [type]
            self.__m_arrMullionHorUserData[1] = self.__m_arrMullionHorUserData[1] + [width]
            self.__m_arrMullionHorUserData[2] = self.__m_arrMullionHorUserData[2] + [thickness]
            self.__m_arrMullionHorUserData[3] = self.__m_arrMullionHorUserData[3] + [capWidth]
            self.__m_arrMullionHorUserData[4] = self.__m_arrMullionHorUserData[4] + [capThickness]


        if "Left" in type or "Right" in type :
            self.__m_arrMullionVertUserData[0] = self.__m_arrMullionVertUserData[0] + [type]
            self.__m_arrMullionVertUserData[1] = self.__m_arrMullionVertUserData[1] + [width]
            self.__m_arrMullionVertUserData[2] = self.__m_arrMullionVertUserData[2] + [thickness]
            self.__m_arrMullionVertUserData[3] = self.__m_arrMullionVertUserData[3] + [capWidth]
            self.__m_arrMullionVertUserData[4] = self.__m_arrMullionVertUserData[4] + [capThickness]
            
    
        self.__m_blnShowMullions = True

    #-----------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    def AddMullionAt(self, direction=None, distance="C", width=0.05*_UNIT_COEF, thickness=0.1*_UNIT_COEF, capThickness=0.05*_UNIT_COEF) :
        
        strType = ""
        if  direction == "horizontal" or direction == "Horizontal" and distance :
            if distance == "C" : distance = self.PanelProperty("PanelHeight")/2.0
            strType = "Hor_fromBottom=" + str(distance)
            self.__m_arrMullionHorUserData[0] = self.__m_arrMullionHorUserData[0] + [strType]
            self.__m_arrMullionHorUserData[1] = self.__m_arrMullionHorUserData[1] + [width]
            self.__m_arrMullionHorUserData[2] = self.__m_arrMullionHorUserData[2] + [thickness]
            self.__m_arrMullionHorUserData[3] = self.__m_arrMullionHorUserData[3] + [width]
            self.__m_arrMullionHorUserData[4] = self.__m_arrMullionHorUserData[4] + [capThickness]

        if  direction == "vertical" or direction == "Vertical" and distance:
            if distance == "C" : distance = self.PanelProperty("PanelWidth")/2.0 
            strType = "Vert_fromLeft=" + str(distance)
            self.__m_arrMullionVertUserData[0] = self.__m_arrMullionVertUserData[0] + [strType]
            self.__m_arrMullionVertUserData[1] = self.__m_arrMullionVertUserData[1] + [width]
            self.__m_arrMullionVertUserData[2] = self.__m_arrMullionVertUserData[2] + [thickness]
            self.__m_arrMullionVertUserData[3] = self.__m_arrMullionVertUserData[3] + [width]
            self.__m_arrMullionVertUserData[4] = self.__m_arrMullionVertUserData[4] + [capThickness]
    
        self.__m_blnShowMullions = True
        
    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------

    def ChangeMullionType(self, type=None, width=None, thickness=None, capThickness=None):


        if len(self.__m_arrMullionHorUserData[0]) :
            for i in range(len(self.__m_arrMullionHorUserData[0])):
                if  self.__m_arrMullionHorUserData[0][i] == type :
                    if width <> None : self.__m_arrMullionHorUserData[1][i] = width
                    if thickness <> None : self.__m_arrMullionHorUserData[2][i] = thickness
                    if width <> None: self.__m_arrMullionHorUserData[3][i] = width
                    if capThickness <> None : self.__m_arrMullionHorUserData[4][i] = capThickness
                    return
                
                
        if len(self.__m_arrMullionVertUserData[0]) :
            for i in range(len(self.__m_arrMullionVertUserData[0])) :
                if  self.__m_arrMullionVertUserData[0][i] == type :
                    if  width <> None : self.__m_arrMullionVertUserData[1][i] = width
                    if  thickness <> None : self.__m_arrMullionVertUserData[2][i] = thickness
                    if width <> None : self.__m_arrMullionVertUserData[3][i] = width
                    if  capThickness <> None : self.__m_arrMullionVertUserData[4][i] = capThickness
                    return
                
                
    #------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------
    # Delete functions:  Deletes objects and data structures with objects parameters----
    
    def DeleteMullionType(self, type):
    
        if type in self.__m_arrMullionHorUserData[0] :
            i = self.__m_arrMullionHorUserData[0].index(type)
            del self.__m_arrMullionHorUserData[0][i]
            del self.__m_arrMullionHorUserData[1][i]
            del self.__m_arrMullionHorUserData[2][i]
            del self.__m_arrMullionHorUserData[3][i]
            del self.__m_arrMullionHorUserData[4][i]
        elif type in self.__m_arrMullionVertUserData[0] :
            i = self.__m_arrMullionVertUserData[0].index(type)
            del self.__m_arrMullionVertUserData[0][i]
            del self.__m_arrMullionVertUserData[1][i]
            del self.__m_arrMullionVertUserData[2][i]
            del self.__m_arrMullionVertUserData[3][i]
            del self.__m_arrMullionVertUserData[4][i]
        else: return
        
        if len(self.__m_arrMullionHorUserData[0]) == 0 and  len(self.__m_arrMullionVertUserData[0]) == 0 :
             self.__m_blnShowMullions = False
             
        self.DeleteMullionType(type)

    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------

    def DeleteWindowMullions(self):
        self.DeleteMullionType("WindowTop")
        self.DeleteMullionType("WindowBottom")
        self.DeleteMullionType("WindowLeft")
        self.DeleteMullionType("WindowRight")

    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    
    def DeleteMullionAt(self, direction, distance=None):
        
        strType = ""
        
        if  direction == "horizontal" or direction == "Horizontal" :
            if  distance <> None:
                if distance == "C" : distance = self.PanelProperty("PanelHeight")/2.0
                elif  type(distance) <> StringType : strType = "Hor_fromBottom=" + str(distance)
            else: strType = "Hor_"
            
            i=0
            while i < len(self.__m_arrMullionHorUserData[0]):
                if  strType in self.__m_arrMullionHorUserData[0][i]:
                    del self.__m_arrMullionHorUserData[0][i]
                    del self.__m_arrMullionHorUserData[1][i]
                    del self.__m_arrMullionHorUserData[2][i]
                    del self.__m_arrMullionHorUserData[3][i]
                    del self.__m_arrMullionHorUserData[4][i]
                else: i+=1
            return

        if  direction == "vertical" or direction == "Vertical" :
            if  distance <> None:
                if distance == "C" : distance = self.PanelProperty("PanelWidth")/2.0
                elif  type(distance) <> StringType : strType = "Vert_fromLeft=" + str(distance)
            else: strType = "Vert_"   
            
            i=0
            while i < len(self.__m_arrMullionVertUserData[0]):
                if  strType in self.__m_arrMullionVertUserData[0][i]:
                    del self.__m_arrMullionVertUserData[0][i]
                    del self.__m_arrMullionVertUserData[1][i]
                    del self.__m_arrMullionVertUserData[2][i]
                    del self.__m_arrMullionVertUserData[3][i]
                    del self.__m_arrMullionVertUserData[4][i]
                else: i+=1
                
        if len(self.__m_arrMullionHorUserData[0]) == 0 and  len(self.__m_arrMullionVertUserData[0]) == 0 :
             self.__m_blnShowMullions = False
             
             
    #------------------------------------------------------------------------------------------------------------------------------------
    #Shading actions
    #------------------------------------------------------------------------------------------------------------------------------------


    def AddShadingType(self, strShadingType, layerName="_P_Shading", fromLeftBottom=[0,0], fromRightTop=None, fromEdge = None, width=.05*_UNIT_COEF, thickness=0.05*_UNIT_COEF, offset=0, spacing=.1*_UNIT_COEF, rotation=0) :

        
        #handling Predefined variables as string paramters
        Window = self.__m_arrWindowUserData
        PanelWidth = self.GetWidth()
        PanelHeight = self.GetHeight()
        if type(fromLeftBottom) == StringType : fromLeftBottom = eval(width)
        if type(fromEdge) == StringType : fromEdge = eval(height)
        if type(fromRightTop) == StringType : fromRightTop = eval(width)        
        
        
        ShadingTypes = ["HorizontalShade","VerticalShade", "HorizontalLouver", "VerticalLouver"]
        if  strShadingType not in ShadingTypes : 
            print "Wrong shading type" 
            return
        
         #Check for 2 valid possible methods to specify sunshade values       
        if strShadingType in ["HorizontalLouver", "VerticalLouver"] :
            if type(fromRightTop) <> ListType : print "Wrong or missing Shading: fromRightTop parameter" ; return
            if spacing < width : spacing = width
            if spacing < 0.02*self.__m_unitCoef : spacing = 0.02*self.__m_unitCoef
        elif strShadingType in ["HorizontalShade", "VerticalShade"] and fromEdge == None : 
            print "Wrong or missing Shading: fromEdge parameter" ; return
            
        self.__m_arrShadingUserData[0] = self.__m_arrShadingUserData[0] + [strShadingType]
        self.__m_arrShadingUserData[1] = self.__m_arrShadingUserData[1] + [fromLeftBottom]
        
        if fromRightTop <> None : self.__m_arrShadingUserData[2] += [fromRightTop]
        else : self.__m_arrShadingUserData[2] += [fromEdge]
        
        self.__m_arrShadingUserData[3] += [width]
        self.__m_arrShadingUserData[4] += [thickness]
        self.__m_arrShadingUserData[5] += [offset]
        self.__m_arrShadingUserData[6] += [spacing]
        self.__m_arrShadingUserData[7] += [rotation]
        self.__m_arrShadingUserData[8] += [layerName]

        self.__m_blnShowShading = True



    #------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------
    # DeleteShadingType: Deletes objects and data strcutures with objects paramters----
    def DeleteShadingType(self, type):
    
        if type not in self.__m_arrShadingUserData[0] : return
        
        i = self.__m_arrShadingUserData[0].index(type)
        for arrIndex in range(len(self.__m_arrShadingUserData)) :
            del self.__m_arrShadingUserData[arrIndex][i]
       
        if len(self.__m_arrShadingUserData[0]) == 0 : self.__m_blnShowShading = False
        
        self.DeleteShadingType(type) #Check again for more cases 
            
    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    
    def DeleteShading(self):
    
        for type in self.__m_arrShadingUserData[0]:
            self.DeleteShadingType(type)
            
        self.__m_arrShadingObjects = [0]
    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    def RotateShadingType(self, type, rotation):
    
        if type not in self.__m_arrShadingUserData[0] : return
        
        i = self.__m_arrShadingUserData[0].index(type)
        self.__m_arrShadingUserData[7][i] = rotation
            
            


    #------------------------------------------------------------------------------------------------------------------------------------
    #Custom Geometry actions
    #------------------------------------------------------------------------------------------------------------------------------------


    def AddCustomGeometry(self, brepCustomGeo, vecPlacement=None, vecScaleFactors=None, vecUpVector=None, blnTilable=None, dblRotation=None, brepCustomWindowGeo=None):

        #store parameters
        if brepCustomGeo : self.__m_brepCustomGeo = brepCustomGeo.DuplicateBrep()
        else: return

        if vecPlacement : self.__m_vecPlacement = vecPlacement
        if vecUpVector.IsUnitVector : self.__m_vecUpVector = vecUpVector
        self.__m_blnTilable = blnTilable
        if dblRotation : self.__m_dblRotation = dblRotation

        #get size data
        tmpGeoBBox = self.__m_brepCustomGeo.GetBoundingBox(False)
        tmpGeoSize = tmpGeoBBox.Max - tmpGeoBBox.Min

        #place custom geometry at 0,0,0        
        vecTranslate = Rhino.Geometry.Vector3d(tmpGeoBBox.Min)
        self.__m_brepCustomGeo.Translate(-vecTranslate)


        #rotate based on Z up value
        if self.__m_vecUpVector.X == 1 :
            ptOrigin = Rhino.Geometry.Point3d(0,tmpGeoSize.Y,0)
            ptVectorX = Rhino.Geometry.Point3d(0,tmpGeoSize.Y-1,0)
            ptVectorY = Rhino.Geometry.Point3d(1,tmpGeoSize.Y,0)
        elif self.__m_vecUpVector.X == -1 :
            ptOrigin = Rhino.Geometry.Point3d(tmpGeoSize.X,0,0)
            ptVectorX = Rhino.Geometry.Point3d(tmpGeoSize.X,1,0)
            ptVectorY = Rhino.Geometry.Point3d(tmpGeoSize.X-1,0,0)
        elif self.__m_vecUpVector.Y == 1 :
            ptOrigin = Rhino.Geometry.Point3d(0,0,0)
            ptVectorX = Rhino.Geometry.Point3d(1,0,0)
            ptVectorY = Rhino.Geometry.Point3d(0,1,0)
        elif self.__m_vecUpVector.Y == -1 :
            ptOrigin = Rhino.Geometry.Point3d(tmpGeoSize.X, tmpGeoSize.Y,0)
            ptVectorX = Rhino.Geometry.Point3d(tmpGeoSize.X-1, tmpGeoSize.Y,0)
            ptVectorY = Rhino.Geometry.Point3d(tmpGeoSize.X, tmpGeoSize.Y-1,0)
        elif self.__m_vecUpVector.Z == 1 :
            ptOrigin = Rhino.Geometry.Point3d(0, tmpGeoSize.Y, 0)
            ptVectorX = Rhino.Geometry.Point3d(1, tmpGeoSize.Y, 0)
            ptVectorY = Rhino.Geometry.Point3d(0, tmpGeoSize.Y, 1)
        elif self.__m_vecUpVector.Z == -1 :
            ptOrigin = Rhino.Geometry.Point3d(tmpGeoSize.X, tmpGeoSize.Y, tmpGeoSize.Z)
            ptVectorX = Rhino.Geometry.Point3d(tmpGeoSize.X-1, tmpGeoSize.Y, tmpGeoSize.Z)
            ptVectorY = Rhino.Geometry.Point3d(tmpGeoSize.X, tmpGeoSize.Y, tmpGeoSize.Z-1)
        #apply rotation
        if True:
            plFrom = Rhino.Geometry.Plane(ptOrigin, ptVectorX, ptVectorY)
            plTo = Rhino.Geometry.Plane(Rhino.Geometry.Point3d(0,0,0), Rhino.Geometry.Point3d(1,0,0), Rhino.Geometry.Point3d(0,0,1))
            brepTransform = Rhino.Geometry.Transform.PlaneToPlane(plFrom, plTo)
            self.__m_brepCustomGeo.Transform(brepTransform)
            
        #scale based on scale factor
        if vecScaleFactors <> self.__m_vecScaleFactor: 
            self.__m_vecScaleFactor = vecScaleFactors
            plOrigin = Rhino.Geometry.Plane(Rhino.Geometry.Point3d(0,0,0), Rhino.Geometry.Point3d(1,0,0), Rhino.Geometry.Point3d(0,1,0))
            brepTransform = Rhino.Geometry.Transform.Scale(plOrigin, self.__m_vecScaleFactor.X, self.__m_vecScaleFactor.Y, self.__m_vecScaleFactor.Z)
            self.__m_brepCustomGeo.Transform(brepTransform)

        #move based on placement data
        if not self.__m_vecPlacement.IsZero:
            self.__m_brepCustomGeo.Translate(self.__m_vecPlacement)

        #tile geometry 
        if self.__m_blnTilable:

            tmpGeoBBox = self.__m_brepCustomGeo.GetBoundingBox(True)
            tmpGeoSize = tmpGeoBBox.Max - tmpGeoBBox.Min
            #move geometry to the left if not at origin
            xPos = round(tmpGeoBBox.Min.X, 3); xStep = round(tmpGeoSize.X, 3)
            vecWidth = Rhino.Geometry.Vector3d(-xStep,0,0)            
            while xPos > 0 :
                self.__m_brepCustomGeo.Translate(vecWidth)
                xPos -= xStep
            #move geometry to the bottom if not at origin
            zPos = round(tmpGeoBBox.Min.Z, 3); zStep = round(tmpGeoSize.Z, 3)
            vecHeight = Rhino.Geometry.Vector3d(0, 0, -zStep)
            while zPos > 0 :
                self.__m_brepCustomGeo.Translate(vecHeight)
                zPos -= zStep
            #create array of breps to cover panel
            tmpGeoList = []
            xTrans = 0; zTrans = 0
            while True:
                while xPos < self.GetWidth():        
                    tmpGeo = self.__m_brepCustomGeo.DuplicateBrep()
                    vecWidth = Rhino.Geometry.Vector3d(xTrans,0,zTrans)                    
                    tmpGeo.Translate(vecWidth)
                    tmpGeoList.append(tmpGeo)
                    xPos += xStep ; xTrans += xStep
                zPos += zStep ; zTrans += zStep
                if zPos < self.GetHeight(): xPos -= xTrans; xTrans =0     
                else: break
            #unify all breps into one
            tolerance = sc.doc.ModelAbsoluteTolerance
            self.__m_brepCustomGeo = Rhino.Geometry.Brep.CreateBooleanUnion(tmpGeoList, tolerance)[0]


        self.__m_blnShowCustomGeo = True
        
        




    #----------------------------------------------------------------------------------------------------------------------            
    #PANEL ELEMENTS HIDE/SHOW SECTION--Deletes objects and "Show" varialbles set to off, data strcutures left undtouched----
    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------
    
    def ShowWall(self):
        if not self.__m_blnShowWall :
            self.__m_blnShowWall = True 
            #self.DrawWall()

    def HideWall(self):
        #Delete Old Wall If Exists.
        if self.__m_arrWallObjects and not type(self.__m_arrWallObjects[0]) == IntType and rs.IsObject(self.__m_arrWallObjects[0]):
           rs.DeleteObjects(self.__m_arrWallObjects)
            
        self.__m_blnShowWall = False
            
            
            
    #----------------------------------------------------------------------------------------------------------------------	
    #----------------------------------------------------------------------------------------------------------------------

    def ShowPane(self):
        if not self.__m_blnShowPane :
            self.__m_blnShowPane = True 
            #self.DrawPane()	

    def HidePane(self):
        #Delete Old Wall Cover objects if exists.
        if self.__m_arrPaneObjects and not type(self.__m_arrPaneObjects[0]) == IntType and rs.IsObject(self.__m_arrPaneObjects[0]): 
            rs.DeleteObjects(self.__m_arrPaneObjects)
        self.__m_blnShowPane = False
        
        
    #----------------------------------------------------------------------------------------------------------------------	
    #----------------------------------------------------------------------------------------------------------------------

    def ShowWindow(self):
        if not self.__m_blnShowWindow and self.__m_arrWindowPoints <> [0,0,0,0]:
            self.__m_blnShowWindow = True
            #self.ShowMullions()
            #self.Draw()
        
        
    def HideWindow(self):
        #Delete Window if Exists.
        if self.__m_arrWindowObjects and not type(self.__m_arrWindowObjects[0]) == IntType and rs.IsObject(self.__m_arrWindowObjects[0]): 
            rs.DeleteObjects(self.__m_arrWindowObjects)
        self.__m_blnShowWindow = False
        

    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
    def ShowMullions(self):
        if not self.__m_blnShowMullions :
            self.__m_blnShowMullions = True  
            #self.DrawMullions()
        
        
    def HideMullions(self):
        
        #Delete Mullions if Exist.
        for i in range(self.PanelProperty("MullionHorNum")):
            arrMullions = self.PanelPropertyArray("MullionHorObjArray", i)
            if arrMullions  and not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                rs.DeleteObjects(arrMullions)
                #print "mullion H deleted"
            #else: print "No mullion H to delete"
            
        for i in range(self.PanelProperty("MullionVertNum")):
            arrMullions = self.PanelPropertyArray("MullionVertObjArray", i)
            if arrMullions and not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                rs.DeleteObjects(arrMullions)
                #print "mullion Vdeleted"
            #else: print "No mullion V to delete"
            
        self.__m_blnShowMullions = False
        
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------

    def ShowShading(self):
        if not self.__m_blnShowShading :
            self.__m_blnShowShading = True
            #self.DrawShading()
        
        
    def HideShading(self):
        #Delete Shadnig if Exists.
        if self.__m_arrShadingObjects and not type(self.__m_arrShadingObjects[0]) == IntType and rs.IsObject(self.__m_arrShadingObjects[0]): 
            rs.DeleteObjects(self.__m_arrShadingObjects)
            
        self.__m_arrShadingObjects = [0]
        self.__m_blnShowShading = False
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
    def ShowCustomGeometry(self):
        if not self.__m_blnShowCustomGeo :
            self.__m_blnShowCustomGeo = True
            #self.DrawCustomGeometry()
        
        
    def HideCustomGeometry(self):
        #Delete Shadnig if Exists.
        if self.__m_brepCustomGeoObject and rs.IsObject(self.__m_brepCustomGeoObject) : rs.DeleteObject(self.__m_brepCustomGeoObject)
            
        self.__m_brepCustomGeoObject = 0
        self.__m_blnShowCustomGeo = False
        
    
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------

    def HideAll(self):
        self.HideMullions()
        self.HideWindow()
        self.HidePane()
        self.HideWall()
        self.HideShading()
        self.HideCustomGeometry()        


    #----------------------------------------------------------------------------------------------------------------------
    #DRAW GEOMETRY SECTION-------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------

    def Draw(self):
        
        if self.__m_blnShowWall : self.DrawWall()
        
        if self.__m_blnShowWindow : self.DrawWindow()
        
        if self.__m_blnShowPane : self.DrawPane()
        
        if self.__m_blnShowMullions : self.DrawMullions()
        
        if self.__m_blnShowShading : self.DrawShading()
        
        if self.__m_blnShowCustomGeo : self.DrawCustomGeometry()
        
        if self.__m_blnShowDeform : self.DrawMorph()
        

        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
    def DrawWall(self):
        

        if  type(self.__m_arrWallObjects) == ListType and not type(self.__m_arrWallObjects[0]) == IntType and rs.IsObject(self.__m_arrWallObjects[0]): 
            rs.DeleteObjects(self.__m_arrWallObjects)     
        
        #Delete Old Wall If Exists
        #if  type(self.__m_arrWallObjects) == ListType and not type(self.__m_arrWallObjects[0]) == IntType \
            #and rs.IsObject(self.__m_arrWallObjects[0]): rs.DeleteObjects(self.__m_arrWallObjects)
        
        #Ignore draw wall if window is as large as panel
        if self.PanelProperty("WindowVisibility") and self.GetWidth() <= self.PanelProperty("WindowWidth") and \
            self.GetHeight() <= self.PanelProperty("WindowHeight"):
            return 
            
        if self.GetDrawMode() == "LADYBUG" : return #Wall excluded from Ladybug draw mode
        
        rs.CurrentLayer("_P_Wall")     #: To Make "_P_Wall" Current

        # Create Wall Geometry
        WallSurface = rs.AddSrfPt([[0, 0, 0], [self.__m_dblWidth, 0, 0], [self.__m_dblWidth, 0, self.__m_dblHeight], [0, 0, self.__m_dblHeight]])
        strExtrCurve = rs.AddLine([0, 0, 0], [0, self.__m_dblWallThickness, 0])   #:Make Path To Exturde Wall Surface
        self.__m_arrWallObjects[0] = rs.ExtrudeSurface(WallSurface, strExtrCurve) #:Extude Surface Via Path
        
        #Clean Up
        rs.DeleteObject(WallSurface)     #:Delete Surface
        rs.DeleteObject(strExtrCurve)    #:Delete Path
        
        rs.CurrentLayer("_P_0")       #:Make "Default" Layer Current
        self.__m_blnShowWall = True
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    
    def DrawPane(self):
        if  type(self.__m_arrPaneObjects) == ListType and not type(self.__m_arrPaneObjects[0]) == IntType \
            and rs.IsObject(self.__m_arrPaneObjects[0]): rs.DeleteObjects(self.__m_arrPaneObjects)
            
        #Ignore draw pane if window is as large as panel
        if self.PanelProperty("WindowVisibility") and self.GetWidth() <= self.PanelProperty("WindowWidth") and \
            self.GetHeight() <= self.PanelProperty("WindowHeight"):
            return 
            
        if self.GetDrawMode() == "LADYBUG" : return   #pane excluded from Ladybug draw mode
        
        GlsSurface = 0          # Surface of Subtracting Object
        CoverSurface = 0        # Surface of Wall Cover 
        strExtrCurve = 0        #: Path is used to Extude, Length of line is equal to Thickness of Wall Cover
        strExtrCurve2 = 0       #: Path is used to Extude Surface of Subtracting Object, Length of line is equal to Thickness of Wall Cover+ Distance between Wall Cover and wall
        OpeningObject = 0
        arrPaneObjects = []
        
        rs.AddLayer(self.__m_strPaneName)      #: To Create in Wall Cover Layer
        
        rs.CurrentLayer(self.__m_strPaneName)  #: To Make New Layer Current
        
        #set up pane overal dimensions
        
        if type(self.__m_dblPaneOffsetEdge)==ListType :                 #if a list was provided
            paneOffset = self.__m_dblPaneOffsetEdge     
            for i in range(len(paneOffset),4): paneOffset.append(0)         #complete with ceros if less than 4 values.
        else:  #else repeat 4 times the number
            paneOffset = [self.__m_dblPaneOffsetEdge, self.__m_dblPaneOffsetEdge, self.__m_dblPaneOffsetEdge, self.__m_dblPaneOffsetEdge]

        #Create pane base object
        CoverSurface = rs.AddSrfPt([[paneOffset[0], 0, paneOffset[1]], [self.__m_dblWidth-paneOffset[2], 0, paneOffset[1]],\
            [self.__m_dblWidth-paneOffset[2], 0, self.__m_dblHeight-paneOffset[3]], [paneOffset[0], 0, self.__m_dblHeight-paneOffset[3]]])
        strExtrCurve = rs.AddLine([0, 0, 0], [0, self.__m_dblPaneThickness, 0])        #:Make Path To Exturde Wall Surface
        self.__m_arrPaneObjects[0] = rs.ExtrudeSurface(CoverSurface, strExtrCurve)    #:Extrude Surface Via Path
        
        
        #Create pane tiles if parameters configured
        
        if self.__m_dblPaneTileWidth and self.__m_dblPaneTileHeight and self.__m_dblPaneTileThickness :
            
            y = -self.__m_dblPaneTileThickness # lay tiles in front of pane base object
            tileHeight = self.__m_dblPaneTileHeight
            z = tileHeight/2 + paneOffset[1]; zStep = tileHeight + self.__m_dblPaneTileGap
            
            while z-tileHeight/2 < (self.__m_dblHeight-paneOffset[3]) : #loop through vertical spacing
                if z + tileHeight/2 >  (self.__m_dblHeight-paneOffset[3]) : #create custom piece height at the top
                    tileHeight = (self.__m_dblHeight-paneOffset[3]) - (z-tileHeight/2)
                    z = (self.__m_dblHeight-paneOffset[3]) - tileHeight/2
                x = paneOffset[0] ; xStep = self.__m_dblPaneTileWidth + self.__m_dblPaneTileGap
                while x <  (self.__m_dblWidth-paneOffset[2]) : #loop through horizontal spacing
                    start = [x,y,z] ; end = [x+self.__m_dblPaneTileWidth,y,z]
                    if end[0] > (self.__m_dblWidth-paneOffset[2]) : end[0] = (self.__m_dblWidth-paneOffset[2]) #create custom piece width at the right end
                    #create tile
                    member = self.DrawMember(start, end, tileHeight, self.__m_dblPaneTileThickness)
                    if member : self.__m_arrPaneObjects.append(member)
                    x += xStep
                z += zStep
                
        #Move to place(front of wall)
        rs.MoveObjects(self.__m_arrPaneObjects, [0, -1 * self.__m_dblPaneOffset, 0]) # Move Objects Forward in front of the Wall
        
        
        
        #Create Opening
        if self.__m_blnShowWindow :                #: If Window exists we need to subtract Window from panel base and tiles.
            arrOpeningPoints = copy.deepcopy(self.__m_arrWindowPoints)

            #Avoid boolean error when subraction boxes align with panel edges
            if round(self.PanelProperty("WindowLeft"),3) == 0 : arrOpeningPoints[0][0] = arrOpeningPoints[3][0] = -.1 
            if round(self.PanelProperty("WindowRight"),3) == 0 : arrOpeningPoints[1][0] = arrOpeningPoints[2][0] = self.GetWidth()+.1 
            if round(self.PanelProperty("WindowBottom"),3) == 0 : arrOpeningPoints[0][2] = arrOpeningPoints[1][2] = -.1 
            if round(self.PanelProperty("WindowTop"),3) == 0 : arrOpeningPoints[2][2] = arrOpeningPoints[3][2] = self.GetHeight()+.1
            
            #create subraction object and subract
            GlsSurface = rs.AddSrfPt(arrOpeningPoints)
            rs.MoveObject(GlsSurface, [0, 2, 0]) 
            strExtrCurve2 = rs.AddLine([0, 2 , 0], [0, -2, 0]) #: Make a Path to Exturde
            OpeningObject = rs.ExtrudeSurface(GlsSurface, strExtrCurve2)
            arrPaneObjects = self.__m_arrPaneObjects
            self.__m_arrPaneObjects = rs.BooleanDifference(arrPaneObjects, OpeningObject, True)

            #Clean up
            rs.DeleteObject(GlsSurface)   #:Delete Surface of Glass
            rs.DeleteObject(strExtrCurve2)#:Delete Path
            
        #Clean up
        rs.DeleteObject(CoverSurface) #:Delete Surface of Pane
        rs.DeleteObject(strExtrCurve)#:Delete Path
        
        rs.CurrentLayer("_P_0")    #:Make "Default" Layer Current
        self.__m_blnShowPane = True
        
    
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    
    def DrawWindow(self):
        
        if type(self.__m_arrWindowObjects) == ListType and not type(self.__m_arrWindowObjects[0]) == IntType \
            and rs.IsObject(self.__m_arrWindowObjects[0]) : rs.DeleteObjects(self.__m_arrWindowObjects)
                
                
        GlsSurface = 0                #:Surface of Glass
        strExtrCurve = 0              #:Path used to Extrude Subtracting Object, Lenght equal to Wall Depth
        GlassObjectTemp = 0
        wallObjectTemp = 0 #bollean window operation result
        
        rs.CurrentLayer("_P_Glass")   #: To Make "_P_Glass" Current
        
        #Create Window Panel
        GlsSurface = rs.AddSrfPt(self.__m_arrWindowPoints)

        if self.GetDrawMode() == "LADYBUG" :
            self.__m_arrWindowObjects[0] = GlsSurface #in LADYBUG mode only glass pane is drawn
            rs.CurrentLayer("_P_0")
            self.__m_blnShowWindow = True
            return
            
        if self.__m_dblWinGlassThickness > 0 : #create glass pane if thickness > 0 othersie just create opening
            strExtrCurve = rs.AddLine([0, 0, 0], [0, self.__m_dblWinGlassThickness, 0])
            self.__m_arrWindowObjects[0] = rs.ExtrudeSurface(GlsSurface, strExtrCurve)
            #Move to place
            rs.MoveObjects(self.__m_arrWindowObjects, [0, -self.__m_dblWinGlassOffset, 0])
            #clean up
            rs.DeleteObject(strExtrCurve)
      
        #Create Opening if wall is visible
        if self.__m_blnShowWall and self.__m_arrWallObjects <> [0]:
            rs.CurrentLayer("_P_Wall")
            strExtrCurve = rs.AddLine([0, 0, 0], [0, self.__m_dblWallThickness, 0])
            GlassObjectTemp = rs.ExtrudeSurface(GlsSurface, strExtrCurve)
            wallObjectTemp = self.__m_arrWallObjects[0]
            self.__m_arrWallObjects = rs.BooleanDifference(wallObjectTemp, GlassObjectTemp, True)

                
            #Clean up
            rs.DeleteObject(strExtrCurve)
        
        rs.DeleteObject(GlsSurface)
        rs.CurrentLayer("_P_0")
        
        self.__m_blnShowWindow = True
        
        if self.__m_arrWallObjects == None : 
            if wallObjectTemp : rs.DeleteObjects([wallObjectTemp, GlassObjectTemp])
            self.__m_arrWallObjects = [0]
            #self.__m_blnShowWindow = False
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
    def DrawMullions(self):
        
        #Detlete Horizontal mullions
        for arrMullions in self.__m_arrMullionHorObjects:
            if type(arrMullions) == ListType and not type(arrMullions[0]) == IntType and rs.IsObject(str(arrMullions[0])) : rs.DeleteObjects(arrMullions)
            
        #Delete Verticals
        for arrMullions in self.__m_arrMullionVertObjects:
            if type(arrMullions) == ListType and not type(arrMullions[0]) == IntType and rs.IsObject(str(arrMullions[0])) : rs.DeleteObjects(arrMullions)
            
        self.__m_arrMullionHorObjects = []
        self.__m_arrMullionVertObjects = []
            
        #Populate array with new mullions based on Mullion Data array
        #Horizontal
        if len(self.__m_arrMullionHorUserData[0]) :
            for i in range(len(self.__m_arrMullionHorUserData[0])) :
                mullionObjList = self.DrawMullionType(self.__m_arrMullionHorUserData[0][i], self.__m_arrMullionHorUserData[1][i], self.__m_arrMullionHorUserData[2][i],\
                    self.__m_arrMullionHorUserData[3][i], self.__m_arrMullionHorUserData[4][i])
                if type(mullionObjList) == ListType and rs.IsObject(mullionObjList[0]): 
                    self.__m_arrMullionHorObjects.append(mullionObjList)
                    rs.ObjectLayer(mullionObjList, "_P_Mullions")
                
        #Vertical
        if len(self.__m_arrMullionVertUserData[0])  :
            for i in range(len(self.__m_arrMullionVertUserData[0])):
                mullionObjList = self.DrawMullionType(self.__m_arrMullionVertUserData[0][i], self.__m_arrMullionVertUserData[1][i], self.__m_arrMullionVertUserData[2][i],\
                    self.__m_arrMullionVertUserData[3][i], self.__m_arrMullionVertUserData[4][i])
                if type(mullionObjList) == ListType and rs.IsObject(mullionObjList[0]): 
                    self.__m_arrMullionVertObjects.append(mullionObjList)
                    rs.ObjectLayer(mullionObjList, "_P_Mullions")
                
        if not self.__m_arrMullionHorObjects : self.__m_arrMullionHorObjects = [0]
        if not self.__m_arrMullionVertObjects : self.__m_arrMullionVertObjects = [0]
        
    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    #    Mullion/Cap creation data based on their type 
    
    def DrawMullionType(self, strMullionType, dblWidth, dblThickness, dblCapWidth, dblCapThickness):

        if dblThickness == 0 or dblWidth == 0 : return
        if not self.__m_blnShowWindow and "Window" in strMullionType : return #ignore window mullions if no window
        
        arrHorPoints = [] #'Four Horizontal  points defined by panel width and window location stored as(X,0,0) 
        arrVertPoints = [] #'Four Vertical  points defined by panel width and window location stored as (0,0,Z)
        arrDeltaPoint = [] # 'Distance from 0,0,0 depending the mullion type (an X value for vertical mullions, Z value for Horizonal)

        arrMullionPoints = [] 
        arrCapMullionPoints= [] #'The final points that result from adding arrDeltaPoint to arrVertPoints or arrHorPoints
        
        arrXform = [] #'Transformation Matrix needed for the addition of arrDeltaPont
        arrMullions = [] # 'array storing the mullions

        dblYOffset = -self.__m_dblPaneOffset + self.__m_dblPaneThickness + .004 * self.__m_unitCoef ###Use this version to tie panel to mullion face.###
        #dblYOffset = self.__m_dblPaneThickness + 0.125 / 12 / 2.54 # Mullion Y location (2.54 converting feet to meters)
        
        bWindowFrame = False #sets on window frame mode (vs mullion mode)
        
        #Populating array with panel dimensions (no window points divisions)
        arrHorPoints = [[0, 0, 0], [self.__m_dblWidth, 0, 0]]
        arrVertPoints = [[0, 0, 0], [0, 0, self.__m_dblHeight]]
        

        if self.__m_blnShowWindow :
            #elif not self.__m_blnShowPane :#only punched window mullion type
            if (type(dblThickness) == ListType or type(dblCapThickness) == ListType):
                if len(dblThickness) > 1 or len(dblCapThickness) > 1:
                    #3-piece mullions if curtain-wall with opening
                    arrHorPoints = [[0, 0, 0], [self.__m_arrWindowPoints[0][0], 0, 0],[self.__m_arrWindowPoints[1][0], 0, 0], [self.__m_dblWidth, 0, 0]]  
                    arrVertPoints = [[0, 0, 0], [0, 0, self.__m_arrWindowPoints[0][2]],[0, 0, self.__m_arrWindowPoints[2][2]], [0, 0, self.__m_dblHeight]]
                else: #if one list item will be used for Window frame only    
                    bWindowFrame = True
            #if full window panel? (no pane object) also use window frame settings
            if not self.__m_arrPaneObjects or self.__m_arrPaneObjects == [0] or not rs.IsObject(self.__m_arrPaneObjects[0]) :
                if type(dblThickness) == ListType and len(dblThickness) > 1 : dblThickness = dblThickness[1]
                if type(dblCapThickness) == ListType and len(dblCapThickness) > 1 : dblCapThickness = dblCapThickness[1]
                bWindowFrame = True 

            if bWindowFrame == True :
                dblYOffset = -self.__m_dblWinGlassOffset + self.__m_dblWinGlassThickness + .004 * self.__m_unitCoef
                arrHorPoints = [[self.__m_arrWindowPoints[0][0], 0, 0],[self.__m_arrWindowPoints[1][0], 0, 0]]
                arrVertPoints = [[0, 0, self.__m_arrWindowPoints[0][2]],[0, 0, self.__m_arrWindowPoints[2][2]]]   
        
        
        #Mullion type specific settings
        if strMullionType ==  "PanelBottom":
           arrMullionPoints = arrHorPoints     #start from the base horizontal or vertical points depending if its hor or vert mullion 
           arrDeltaPoint = [0, dblYOffset, 0]  # Store the appropiate distance from 0 based on the mullion type/location 
        elif strMullionType ==  "WindowBottom":
            arrMullionPoints = arrHorPoints
            arrDeltaPoint = [0, dblYOffset, self.__m_arrWindowPoints[0][2]]
        elif strMullionType ==  "WindowTop":
            arrMullionPoints = arrHorPoints
            arrDeltaPoint = [0, dblYOffset, self.__m_arrWindowPoints[2][2]]
        elif strMullionType ==  "PanelTop":
            arrMullionPoints = arrHorPoints
            arrDeltaPoint = [0, dblYOffset, self.__m_dblHeight]
            
        elif strMullionType ==  "PanelLeft":
            arrMullionPoints = arrVertPoints
            arrDeltaPoint = [0, dblYOffset, 0]
        elif strMullionType ==  "WindowLeft":
            arrMullionPoints = arrVertPoints
            arrDeltaPoint = [self.__m_arrWindowPoints[0][0], dblYOffset, 0]
        elif strMullionType ==  "WindowRight":
            arrMullionPoints = arrVertPoints
            arrDeltaPoint =[self.__m_arrWindowPoints[1][0], dblYOffset, 0]
        elif strMullionType ==  "PanelRight":
            arrMullionPoints = arrVertPoints
            arrDeltaPoint = [self.__m_dblWidth, dblYOffset, 0]
            
            #if Hor : format is Hor_fromBottom=number. Compile line to use value
        elif "Hor_" in strMullionType :
            arrMullionPoints = arrHorPoints
            fromBottom=0
            strData = strMullionType[4:len(strMullionType)]
            codeObj= compile(strData,'<string>','single')
            eval(codeObj)
            arrDeltaPoint = [0, dblYOffset, fromBottom]
            
            #if Vert : format is Vert_fromLeft=number. Compile line to use value
        elif "Vert_" in strMullionType :
            arrMullionPoints = arrVertPoints
            fromLeft=0
            strData = strMullionType[5:len(strMullionType)]
            codeObj= compile(strData,'<string>','single')
            eval(codeObj)
            arrDeltaPoint = [fromLeft, dblYOffset, 0]
            
        else:
            print "Wrong mullion type"
            return
    
        arrXform = rs.XformTranslation(arrDeltaPoint) # create matrix from vector to add delta(distance) to base points in one line
        arrMullionPoints = rs.PointArrayTransform(arrMullionPoints, arrXform) # add delta(distance) to base mullions to get final 4 points locations
        
        
        #Create 1 or 3 mullions using the obtained points sending them in pairs (end points of each mullion)
   
        for i in range(len(arrMullionPoints)-1) :
            
            if rs.PointCompare(arrMullionPoints[i], arrMullionPoints[i + 1]) : continue #skip if points on same location
            #detect if thickness is one value or three(varying thinkness along mullion)
            if type(dblThickness) is ListType and len(dblThickness)> i: mullThickness = dblThickness[i]
            else : mullThickness = dblThickness
            
            if mullThickness > 0 and self.GetDrawMode() <> "LADYBUG" : 
                
                arrMullions.append(self.DrawMember(arrMullionPoints[i], arrMullionPoints[i + 1], dblWidth, mullThickness))
            else:
                arrMullions.append(rs.AddPoint(self.__m_arrBoundingBox[0])) #just a point as placeholder at Panel origin
 
            if  dblCapWidth > 0.0 :
                #detect if thickness is one value or three(varying thinkness along mullion)
                if type(dblCapThickness) is ListType and len(dblCapThickness)> i: capThickness = dblCapThickness[i]
                else : capThickness = dblCapThickness
                if  capThickness > 0.0 : #Cap data?
                    if self.GetDrawMode() <> "LADYBUG" or (self.GetDrawMode() == "LADYBUG" and capThickness >= self.__m_LadybugShadeThresh) :
                        # create matrix with  translation to get cap Y location
                        arrXform = rs.XformTranslation([0, -capThickness - (self.__m_dblWinGlassThickness if bWindowFrame else self.__m_dblPaneThickness) - .008 * self.__m_unitCoef, 0])
                        arrCapMullionPoints = rs.PointArrayTransform(arrMullionPoints, arrXform) # new points location
                        arrMullions.append(self.DrawMember(arrCapMullionPoints[i], arrCapMullionPoints[i + 1], dblCapWidth, capThickness))
            #else:
                #arrMullions.append(rs.AddPoint(self.__m_arrBoundingBox[0])) #just a point as placeholder at Panel origin
                
        
        
        #return the array of mullion back to function call
        return arrMullions
        
        
    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    
    #Member creation using start/end, width, thickness parameters
    
    def DrawMember(self, arrStartPoint, arrEndPoint, dblWidth, dblThickness, dblRotation=0) :

        if rs.PointCompare(arrStartPoint, arrEndPoint) : return #return if same points start,end
        
        #To create 4 surface points based on 2 points a vertical or horizontal offset need to be defined
        #depending on member type:horizontal or verical
        rotVector = []

        if arrStartPoint[0] == arrEndPoint[0] :     #Is Vertical?
            arrOffset = [dblWidth / 2, 0, 0]
            rotVector = [0,0,1]
        elif arrStartPoint[2] == arrEndPoint[2] :   #Is Horizontal?
            arrOffset = [0, 0, dblWidth / 2]
            rotVector = [1,0,0]
        else:
            return
                
                
        #Create points using offset obtained above
        arrStartP = [[],[]]
        arrEndP = [[],[]]
        arrStartP[0] = rs.PointAdd(arrStartPoint, arrOffset)        #create first surface point 
        arrStartP[1] = rs.PointSubtract(arrStartPoint, arrOffset)   #create second surface point
        arrEndP[0] = rs.PointSubtract(arrEndPoint, arrOffset)    #create third point of surface
        arrEndP[1] = rs.PointAdd(arrEndPoint, arrOffset)         #create fourth point of surface
        
        #Create surface using 4 points 
        objMemberSurface = rs.AddSrfPt([arrStartP[0], arrStartP[1], arrEndP[0], arrEndP[1]])
        objMemberExtLine = rs.AddLine([0, 0, 0], [0, dblThickness, 0])         #extrusion line
        #Create object and store it to return it to function call
        objMember = rs.ExtrudeSurface(objMemberSurface, objMemberExtLine)#extrude surface 
    
        rs.DeleteObject(objMemberSurface)          #Clean up
        rs.DeleteObject(objMemberExtLine)
        
        if dblRotation <> 0 : 
            rotCenter = [arrStartPoint[0],arrStartPoint[1]+dblThickness/2,arrStartPoint[2]]            
            rs.TransformObject(objMember, rs.XformRotation2(dblRotation, rotVector, rotCenter))

        return objMember
        
        
        
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def DrawShading(self):

        #Detlete Horizontal mullions
        if type(self.__m_arrShadingObjects) == ListType and not type(self.__m_arrShadingObjects[0]) == IntType \
            and rs.IsObject(self.__m_arrShadingObjects[0]) : rs.DeleteObjects(self.__m_arrShadingObjects)
        
        currentLayer = rs.CurrentLayer()
        
        self.__m_arrShadingObjects = []
    
        #Populate array with new shadine elements based on Data array
        if len(self.__m_arrShadingUserData[0]) :
            for i in range(len(self.__m_arrShadingUserData[0])) : 
                rs.CurrentLayer(self.__m_arrShadingUserData[8][i]) 
                tmpShadingObject = self.DrawShadingType(self.__m_arrShadingUserData[0][i], self.__m_arrShadingUserData[1][i], self.__m_arrShadingUserData[2][i],\
                    self.__m_arrShadingUserData[3][i], self.__m_arrShadingUserData[4][i], self.__m_arrShadingUserData[5][i], self.__m_arrShadingUserData[6][i],self.__m_arrShadingUserData[7][i])
                if tmpShadingObject <> None : self.__m_arrShadingObjects += tmpShadingObject
        if not self.__m_arrShadingObjects or self.__m_arrShadingObjects[0] == None : self.__m_arrShadingObjects = [0]
        
        rs.CurrentLayer(currentLayer)
        
        
        
    def DrawShadingType(self,  strShadingType, fromLeftBottomCorner, fromRightTop, width=.05*_UNIT_COEF, thickness=0.05*_UNIT_COEF, offset=0, spacing=.1*_UNIT_COEF, rotation=0):

        #----Setting up parameters common to all shading types
        start = [0,0,0]; end = [0,0,0]
        start[1] = -offset-thickness; end[1] = -offset-thickness
        start[0] = fromLeftBottomCorner[0]; start[2] = fromLeftBottomCorner[1]
        
        #----Setting up parameters based on shading type
        #Single Shade options:
        if strShadingType == "HorizontalShade":  #---Single Vertical Shade
            end[0] = self.PanelProperty("PanelWidth")-fromRightTop
            end[2] = fromLeftBottomCorner[1]
            if start[0] >= end[0] or start[2] > self.GetHeight()*self.__m_dimRoundCoef: return None #check for wrong data
            return [self.DrawMember(start, end, width, thickness, rotation)]
            
        elif strShadingType == "VerticalShade": #---Single Horizontal Shade
            end[0] = fromLeftBottomCorner[0]
            end[2] = self.PanelProperty("PanelHeight")-fromRightTop
            if start[2] >= end[2] or start[0] > self.GetWidth()*self.__m_dimRoundCoef: return None #check for wrong data
            return [self.DrawMember(start, end, width, thickness, rotation)]
            
        #Louver type options:
        if strShadingType == "HorizontalLouver": #---VerticalLouvers
            end[0] = self.PanelProperty("PanelWidth")-fromRightTop[0]
            valZ = start[2]
            endZ = self.PanelProperty("PanelHeight")-fromRightTop[1]
            if start[0] >= end[0] or start[2] > self.GetHeight()*self.__m_dimRoundCoef: return None #check for wrong data
            arrLouvers = []
            while valZ <= endZ :
                start[2] = end[2] = valZ
                arrLouvers.append(self.DrawMember(start, end, width, thickness, rotation))
                valZ += spacing
            return arrLouvers
            
        if strShadingType == "VerticalLouver": #---Horizontal Louvers
            end[2] = self.PanelProperty("PanelHeight")-fromRightTop[1]
            valX = start[0]
            endX = self.PanelProperty("PanelWidth")-fromRightTop[0]
            if start[2] >= end[2] or start[0] > self.GetWidth()*self.__m_dimRoundCoef: return None #check for wrong data
            arrLouvers = []
            while valX <= endX :
                start[0] = end[0] = valX
                arrLouvers.append(self.DrawMember(start, end, width, thickness, rotation))
                valX += spacing
            return arrLouvers        
            
        else: print "Incorrect louver type" ; return
        
        
        
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def DrawCustomGeometry(self):

        if self.__m_brepCustomGeoObject and rs.IsObject(self.__m_brepCustomGeoObject) : rs.DeleteObject(self.__m_brepCustomGeoObject)
        
        if self.GetDrawMode() == "LADYBUG" : return #Custom geo not used in ladybug mode
        
        currentLayer = rs.CurrentLayer()
        rs.CurrentLayer("_P_CustomGeo")
        
        tolerance = sc.doc.ModelAbsoluteTolerance
        tmpCustomGeo = self.__m_brepCustomGeo
        customGeoBBox = self.__m_brepCustomGeo.GetBoundingBox(True)
        customGeoMin = customGeoBBox.Min
        customGeoMax = customGeoBBox.Max 
        customGeoSize = customGeoMax - customGeoMin

        # Trim Custom Geometry to match panel size if extends beyond        
        if round(customGeoMin.X, 3) < 0 or round(customGeoMax.X, 3) > self.GetWidth() or \
            round(customGeoMin.Y, 3) < 0 or round(customGeoMax.Y, 3) > self.GetHeight():
            #create substraction object and subract
            pt1 = Rhino.Geometry.Point3d(0,1,0)
            pt2 = Rhino.Geometry.Point3d(self.GetWidth(), -customGeoSize.Y*1.1, self.GetHeight())
            tmpBBox = Rhino.Geometry.BoundingBox(pt1, pt2)
            tmpBoxBrep = Rhino.Geometry.Brep.CreateFromBox(tmpBBox)
            tmpBrepList = Rhino.Geometry.Brep.CreateBooleanDifference(tmpCustomGeo, tmpBoxBrep, tolerance)
            #unify result pieces in one brep
            for index in range(len(tmpBrepList)-1):
                tmpBrepList[0].Append(tmpBrepList[index+1])
            if tmpBrepList : tmpCustomGeo = tmpBrepList[0] 
            else: tmpCustomGeo = None     
            
        # if window exists subtract window from custom geometry
        if tmpCustomGeo and self.__m_blnShowWindow :
            arrOpeningPoints = copy.deepcopy(self.__m_arrWindowPoints)
            
            #Avoid boolean error when subraction boxes align with panel edges
            if round(self.PanelProperty("WindowLeft"),3) == 0 : arrOpeningPoints[0][0] = arrOpeningPoints[3][0] = -.1 
            if round(self.PanelProperty("WindowRight"),3) == 0 : arrOpeningPoints[1][0] = arrOpeningPoints[2][0] = self.GetWidth()+.1 
            if round(self.PanelProperty("WindowBottom"),3) == 0 : arrOpeningPoints[0][2] = arrOpeningPoints[1][2] = -.1 
            if round(self.PanelProperty("WindowTop"),3) == 0 : arrOpeningPoints[2][2] = arrOpeningPoints[3][2] = self.GetHeight()+.1
            
            #create subraction object
            pt1 = Rhino.Geometry.Point3d(arrOpeningPoints[0][0], 1, arrOpeningPoints[0][2])
            pt2 = Rhino.Geometry.Point3d(arrOpeningPoints[2][0], -customGeoSize.Y*1.1, arrOpeningPoints[2][2])
            tmpWinBox = Rhino.Geometry.BoundingBox(pt1, pt2)
            
            #check if both window and custom geometry overlap before creating opening
            tmpGeoBBox = tmpCustomGeo.GetBoundingBox(True)
            if tmpGeoBBox.Min.X < tmpWinBox.Max.X and tmpGeoBBox.Min.Z < tmpWinBox.Max.Z: 
                tmpWinBoxBrep = Rhino.Geometry.Brep.CreateFromBox(tmpWinBox)
                tmpBrepList = Rhino.Geometry.Brep.CreateBooleanIntersection(tmpCustomGeo, tmpWinBoxBrep, tolerance)
                #unify pieces in one brep
                if tmpBrepList <> None : 
                    for index in range(len(tmpBrepList)-1):
                        tmpBrepList[0].Append(tmpBrepList[index+1])
                    if tmpBrepList : tmpCustomGeo = tmpBrepList[0] 
                    else: tmpCustomGeo = None
                else : print "Boolean error - discarding geometry" 
            
        if tmpCustomGeo : self.__m_brepCustomGeoObject = sc.doc.Objects.AddBrep(tmpCustomGeo)
            
        rs.CurrentLayer(currentLayer)
    
    
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def DrawMorph(self):
        
        #Apply deformation on exixsting objects
        
        if  self.__m_blnShowWall and self.__m_arrWallObjects and self.__m_arrWallObjects <> [0]: self.BoxMorphObject(self.__m_arrWallObjects)
        
        if  self.__m_blnShowWindow and self.__m_dblWinGlassThickness : self.BoxMorphObject(self.__m_arrWindowObjects)

        if  self.__m_blnShowPane and self.__m_arrPaneObjects and self.__m_arrPaneObjects <> [0]: self.BoxMorphObject(self.__m_arrPaneObjects)
        
        if  self.__m_blnShowMullions :
            if self.__m_arrMullionVertObjects and self.__m_arrMullionVertObjects[0]:
                for arrMullion in self.__m_arrMullionVertObjects :
                    if  not type(arrMullion[0]) == IntType and rs.IsObject(arrMullion[0]) : self.BoxMorphObject(arrMullion)
            if self.__m_arrMullionHorObjects and self.__m_arrMullionHorObjects[0] :
                for arrMullion in self.__m_arrMullionHorObjects :
                    if  not type(arrMullion[0]) == IntType and rs.IsObject(arrMullion[0]) :  self.BoxMorphObject(arrMullion)
        
        if  self.__m_blnShowShading and self.__m_arrShadingObjects and self.__m_arrShadingObjects <> [0]: self.BoxMorphObject(self.__m_arrShadingObjects)
        
        if  self.__m_blnShowCustomGeo and self.__m_brepCustomGeoObject <> 0: self.BoxMorphObject(self.__m_brepCustomGeoObject)
        
        #Store deform box as new panel bounding box
        self.__m_arrBoundingBox = self.__m_arrDeformBox
        
        
    #Work around Phyton not implementing yet morphing func(BoxMorphObject) used in DrawMorph()------------------------------------------------
    def BoxMorphObject(self, arrObjects):
        rs.TransformObjects(arrObjects, self.__m_TransformMatrix)
            

#----------------------------------------------------------------------------------------------------------------------

SGLibPanel = Panel


class Skin:
    
    __m_skinGenName = "" # Name id (avoids overlapping block names between skin instances
    
    __m_dblOffsetLevel = 0  #Offset in elevation from path to be considered bottom of panel. Any value > 0 creates custom panel. 
    __m_dblOffsetPath = 0 #Offset x distance of first panel at segments.Use list for different dimensions at each segment
    __m_blnSkinWrap = True #Wrap at corners or create custom corner panels
    
    
    __m_resetBayAtPoints = True #Start new bay at new segment
    
    __m_dblMinPanelWidth = 0 #if surface cell width is below this number it will be ignored and panel won't be created.
    __m_dblMinPanelHeight = 0 #if surface cell height is below this number will be ignored and panel won't be created.
    
    __m_flatMode = False  #Low geoemtry mode
    __m_drawMode = ""   #"LADYBUG", "DEFAULT" 
    __m_random = None #Global Random generator object
    
    __m_bayList = None # bays used in skin - 'None' will use all panel bays connected

    # Internal members
    __m_objSkinSurface = None #skin surface from skin generator
    __m_panelBays = [] #panel bay data from skin generator
    __m_DesignFunctions = [] 
    
    __m_arrBayMatrix = [] #surface matrix of bay points
    __m_intLevels = 0 #number of floors on surface
    

    
    
    
    
    
    def __init__(self, skinName = "DEFAULT", objSkinSurface=None, panelBays=None):
        
        #Skin generator paramters
        self.__m_skinGenName = skinName        
        self.__m_objSkinSurface = objSkinSurface
        self.__m_panelBays = panelBays        
        self.__m_DesignFunctions = []
        
        self.__m_dblOffsetLevel = 0
        self.__m_dblOffsetPath = 0
        self.__m_blnSkinWrap = True
        
        self.__m_resetBayAtPoints = True
        
        self.__m_dblMinPanelWidth = .1 * _UNIT_COEF
        self.__m_dblMinPanelHeight = .1 * _UNIT_COEF
        
        self.__m_flatMode = False
        self.__m_drawMode = "DEFAULT" 
        self.__m_objRandom = random.Random() 
        
        self.__m_bayList = None 
      
        #Internal members        
        self.__m_arrBayMatrix = [] 
        self.__m_intLevels = 0  
        
        #load paramters from surface object name property
        self.LoadSurfaceProperties()
        
        
    def __del__(self):
        #print "adios!"
        pass
        
        
    def LoadSurfaceProperties(self):
        
        if self.__m_objSkinSurface == None : return
        
        # init from stored paramters
        OFFSET_LEVEL = self.__m_dblOffsetLevel
        OFFSET_PATH = self.__m_dblOffsetPath
        SKIN_WRAP = self.__m_blnSkinWrap
        BAY_LIST = self.__m_bayList
        
        #look for Surface-specific parameters stored on object name 
        #with format: OFFSET_LEVEL=float/OFFSET_PATH=float/SKIN_WRAP=bool/BAY_LIST = [int,..]
        objData = rs.ObjectName(self.__m_objSkinSurface)
        dataList = list(objData.rsplit("/"))
        for data in dataList : 
            if 'OFFSET_LEVEL' in data or 'OFFSET_PATH' in data or 'SKIN_WRAP' in data or 'BAY_LIST' in data :
                codeObj= compile(data,'<string>','single') ; eval(codeObj)
                
        # parameters update
        self.__m_dblOffsetLevel = OFFSET_LEVEL
        self.__m_dblOffsetPath = OFFSET_PATH
        self.__m_blnSkinWrap = SKIN_WRAP
        self.__m_bayList = BAY_LIST     
        


        
    def SetProperty(self, strProperty, value):
    
        if strProperty == "SKIN_NAME" : self.__m_skinGenName = value
        elif strProperty == "OFFSET_LEVEL" : self.__m_dblOffsetLevel = value
        elif strProperty == "OFFSET_PATH" : self.__m_dblOffsetPath = value
        elif strProperty == "SKIN_WRAP" : self.__m_blnSkinWrap = value
        elif strProperty == "RESET_BAY_AT_POINTS" : self.__m_resetBayAtPoints = value
        elif strProperty == "FLAT_MODE" : self.__m_flatMode = value
        elif strProperty == "DRAW_MODE" : self.__m_drawMode = value
        elif strProperty == "BAY_LIST" : self.__m_bayList = value
        elif strProperty == "MIN_PANEL_WIDTH" : self.__m_dblMinPanelWidth = value
        elif strProperty == "MIN_PANEL_HEIGHT" : self.__m_dblMinPanelHeight = value        
        elif strProperty == "RANDOM_OBJECT" : self.__m_objRandom = value
        
        elif strProperty == "SKIN_SURFACE" : self.__m_objSkinSurface = value
        elif strProperty == "PANEL_BAY_LIST" : self.__m_panelBays = value
        elif strProperty == "DESIGN_FUNCTIONS" : self.__m_DesignFunctions = value
        
        
    #--------------------------------------------------------------------------------
    #Generate matrix of corner points of a surface based on panel bay dimensions
    #--------------------------------------------------------------------------------
    def GeneratePanelMatrix(self, dblBayWidth, dblFloorToFloor):
        
        self.__m_arrBayMatrix = [] #Stores array of bay corner points

        #Create top/bottom curves from Surface(only extruded curves ar evalid at the moment)
        paramU = rs.SurfaceDomain(self.__m_objSkinSurface,0)   
        paramV = rs.SurfaceDomain(self.__m_objSkinSurface,1)
        CurveBottom = rs.ExtractIsoCurve (self.__m_objSkinSurface, [paramU[0],paramV[0]], 0)
        CurveTop = rs.ExtractIsoCurve (self.__m_objSkinSurface, [paramU[1],paramV[1]], 0)
        
        #Create points based on panelwidth on top/bottom two curves
        
        arrPointsBottom = self.DividePoints(CurveBottom, dblBayWidth, self.__m_dblOffsetPath, self.__m_blnSkinWrap)
        arrPointsTop = self.DividePoints(CurveTop, dblBayWidth, self.__m_dblOffsetPath, self.__m_blnSkinWrap)
        rs.DeleteObjects([CurveBottom,CurveTop])
        
        #Create plane to define panel grid Vertical points
        arrPlane = rs.WorldXYPlane()
        dblFloorTop = arrPointsTop[0][2]
        
        if self.__m_dblOffsetLevel: dblFloorLevel = arrPointsBottom[0][2] + self.__m_dblOffsetLevel
        else: dblFloorLevel = arrPointsBottom[0][2] + dblFloorToFloor
        
        #Initialize array to store grid points
        self.__m_arrBayMatrix.append(arrPointsBottom)
        intLevel = 0
        
        #Create array of grid points
        while dblFloorLevel < dblFloorTop :
    
            arrPlane = rs.WorldXYPlane()
            levelMove = rs.XformTranslation([0, 0, dblFloorLevel])
            arrPlane = rs.PlaneTransform(arrPlane, levelMove)
            pointIndex = 0
            arrInterPoints = [] #Intersection points in current level
            
            for arrPoint in arrPointsTop:
                
                #if intLevel == 0 : rs.AddLine(arrPointsBottom[pointIndex], arrPointsTop[pointIndex]) #--to visualize vertical lines
                arrLine = [arrPointsBottom[pointIndex], arrPointsTop[pointIndex]]  #Create Line from Top / bottom curves
                arrIntPoint = rs.LinePlaneIntersection(arrLine, arrPlane)#Intersect with level plane to obtain vertial points
                
                arrInterPoints.append(arrIntPoint)
                pointIndex = pointIndex + 1
    
            intLevel = intLevel + 1
            self.__m_arrBayMatrix.append(arrInterPoints)
            
            #rs.AddPolyline(self.__m_arrBayMatrix[intLevel]) #--to visualize horizontal lines
            dblFloorLevel = dblFloorLevel + dblFloorToFloor
            
        self.__m_arrBayMatrix.append(arrPointsTop)
        self.__m_intLevels = intLevel
        
        
    
    #--------------------------------------------------------------------------------
    #Select and divide curve in specific segments
    #--------------------------------------------------------------------------------
    def DividePoints(self, strObject, dblLength, dblOffset, skinWrap) :
        
        if not rs.IsCurve(strObject) : print "Invalid Curve" ; return
        
        newPoints = [] ; segmentList = []
    
        if  not skinWrap and rs.CurvePointCount(strObject) > 2 : segmentList = rs.ExplodeCurves(strObject)#create individual segements to avoid wrapping
        else : segmentList.append(rs.CopyObject(strObject)) #treat as a single segment

        #process each segment individually
        for i in range(len(segmentList)):
    
            #----If offset used create new curve to divide at offset start point
            offset = 0
            if type(dblOffset)== ListType :
                if len(dblOffset) > i : offset = dblOffset[i]
                else: offset = dblOffset[len(dblOffset)-1]
            else : offset = dblOffset
    
            if offset and offset <> round(rs.CurveLength(segmentList[i]),4):
    
                domain = rs.CurveDomain(segmentList[i])
                newPoints.append(rs.CurveStartPoint(segmentList[i]))
                coefOffset = (dblLength/(dblLength/offset))/rs.CurveLength(segmentList[i])
                domain[0] = rs.CurveParameter(segmentList[i], coefOffset)
                tmpSegment = segmentList[i]
                segmentList[i] = rs.TrimCurve(tmpSegment,domain, True)
            
            newPoints.extend(rs.DivideCurveEquidistant(segmentList[i], dblLength))
            
            #Adjusting last Panel to absorb leftover dimension(not working)
            #remainderDist = rs.Distance(newPoints[len(newPoints)-1], rs.CurveEndPoint(segmentList[i]))
            #if  remainderDist > MIN_PANEL_WIDTH  : newPoints[len(newPoints)-1] = rs.CurveEndPoint(segmentList[i])
            
        #remainderDist = rs.Distance(newPoints[len(newPoints)-1], rs.CurveEndPoint(strObject))
        #if  remainderDist > MIN_PANEL_WIDTH  : newPoints.append(rs.CurveEndPoint(strObject))
        newPoints.append(rs.CurveEndPoint(strObject))
        
        # remove duplicate points
        index=1
        while index < len(newPoints):
            if rs.PointCompare(newPoints[index], newPoints[index-1], 0.01) : del newPoints[index]
            else: index += 1 
            
        #--Wrap up----------------------------------------
    
        rs.DeleteObjects(segmentList)
    
        return newPoints
    
    
    
    
    def GeneratePanelBlocks(self, PanelTypes, BayData):
        
        #INIT SECTION-------------------------------------------------------------------------

        #Design functions class variables issue - fixed by replacing them with local variables
        myPanelBays = self.__m_panelBays 
        randomObj = self.__m_objRandom 
        bayList = self.__m_bayList #bay indices used in skin [1 based]
        
        #intial loop settings
        currBayPanel = None ; bayPanelIndex = -1  #Holds current panel in bay; Holds index of current panel in use 
        currentBay = self.__m_panelBays[0] ; bayIndex = -1 # Stores current bay; Stores index of current bay 
        PanelDef = None #Stores current panel of the bay used
        BlockName = "" #Holds block name based on panel data  
        
        self.__m_arrBayMatrix = self.__m_arrBayMatrix   
        intLevels = self.__m_intLevels
        intCurrentLevel = 0 ; intCell_Index = -1          #init level and index counters 
        intBaysPerLevel = len(self.__m_arrBayMatrix[0])        
        
        #Change flags store specific panel modifications to ID'd when stored and loaded from database
        ChangeFlag = [0, 0]     #[panel height , panel width , .... ]
    

        
        #------------------------Iteration through bay grid------------------------
        while True :
            
            #-BAY & PANEL LOCATION AND SELECTION SECTION-----------------------------------------------------------
            
            bayPanelIndex += 1 # next panel of current bay
            
            if bayPanelIndex == len(currentBay) or bayPanelIndex == 0: #when done with current bay panels
                bayPanelIndex = 0; bayIndex += 1 #move on to next panel bay
                if bayIndex == len(self.__m_panelBays) : bayIndex = 0  #and loop when done with all bays

                intCell_Index +=  1 # move to next cell on row
                
                #--------Level End detection and action
                if intCell_Index == intBaysPerLevel-1 :
                    intCell_Index = 0 ; intCurrentLevel += 1 ; #start next row up
                    intBaysPerLevel = len(self.__m_arrBayMatrix[intCurrentLevel])
                    if self.__m_resetBayAtPoints : bayPanelIndex = 0; currentBay = self.__m_panelBays[0]; bayIndex=-1 #reset bay at beginng of row
                    if intCurrentLevel > intLevels : break        #exit at end of grid
                    
                #---------Run Design Functions----------------------------------
                currentBay, bayIndex = self.DesFunc_Default_Panel_Bays(self.__m_panelBays, bayIndex, bayList)#Run default function on bays
                if self.__m_DesignFunctions: #Run skin design functions if avialable
                    #store current bay corner points (needed by some functions)
                    bayCornerPoints = [self.__m_arrBayMatrix[intCurrentLevel][intCell_Index], self.__m_arrBayMatrix[intCurrentLevel][intCell_Index + 1],\
                        self.__m_arrBayMatrix[intCurrentLevel + 1][intCell_Index], self.__m_arrBayMatrix[intCurrentLevel + 1][intCell_Index + 1]]
                    
                    for dsFunc in self.__m_DesignFunctions:
                        currentBay, bayIndex = eval("dsFunc."+dsFunc.RunString())                   

                BayData[BayData.index(currentBay)+len(self.__m_panelBays)] += 1 #update bay type counters
                
                panelMatrix = self.GetPanelMatrix(self.__m_arrBayMatrix, intCurrentLevel, intCell_Index, currentBay) #get array of corner points of all panels in bay
                
                    
            currBayPanel = currentBay[bayPanelIndex]
            if bayPanelIndex > len(panelMatrix[0])-2  : continue #skip rest of bay if not finished at end of row
            #store panel corner points in skin
            arrAreaPanelPoints = self.GetPanelCorners(panelMatrix, bayPanelIndex)
            
            #-TYPE PROFILE SECTION -----------------------------------------------------------------------

            #ChangeFlag[0]stores panel height number (in unit/1000), used to store and retrieve panels in database 
            panelHeight = rs.Distance(arrAreaPanelPoints[0], arrAreaPanelPoints[2])
            ChangeFlag[0] = int(round(panelHeight,3)*1000) 
            #ChangeFlag[1] stores panel width number (in unit/1000 ), used to store and retrieve panels in database 
            panelWidth =rs.Distance(arrAreaPanelPoints[0],arrAreaPanelPoints[1])
            ChangeFlag[1] = int(round(panelWidth,3)*1000)
            
            

            
            #-----------------------------------------------------------------------------------------------
            #Look for panel type in database - check for same panel type with same changeFlags 
            #Database format: Dictionary = {BasePanelType_Name_A:[[PanelType Object 1, ChangeFlag],[PanelType Object 2, ChangeFlag],.....],
            #                               BasePanelType_Name_B:[[PanelType Object 1, ChangeFlag],.....],BasePanelType_Name_C:....}
            
            #Check first if panel size is large enough
            if panelHeight < self.__m_dblMinPanelHeight or panelWidth < self.__m_dblMinPanelWidth : continue            
            
            PanelDef = None
            if currBayPanel.GetName() in PanelTypes :
                for ptype in range(len(PanelTypes[currBayPanel.GetName()])):
                    if PanelTypes[currBayPanel.GetName()][ptype][1] == ChangeFlag :
                        PanelDef = PanelTypes[currBayPanel.GetName()][ptype][0] #retrieve panel object stored
                        if  len(PanelDef.PanelProperty("BlockInstances")) == 0 : BlockName = ""; break #panels with empty blocks (ex.Ladybug) are skipped
                        BlockName = rs.BlockInstanceName(PanelDef.PanelProperty("BlockInstances")[0])
                        #print "Found: "; print currBayPanel.GetName(); print PanelTypes[currBayPanel.GetName()][ptype]
                        break
                
            else: PanelTypes[currBayPanel.GetName()] = [] 
            #----------------------------------------------------------------------------------------------------
            #A new panel type is generated if no match found in database
            if PanelDef == None :
    
                #-----Create panel copy if unique ----------------------------
                #PanelTypeCount += 1
                PanelDef = SGLibPanel()
                PanelDef.Copy(currBayPanel)
                
                #---CUSTOM PANEL CHANGES SECTION-------------------------------
                
                #-----Name tag panel (used by Panel Inventory component) 
                if round(panelHeight,3) <> round(PanelDef.PanelProperty("PanelHeight"),3) : 
                    PanelDef.SetName(PanelDef.GetName() + " -Height:"+str(round(panelHeight,2)))
                if round(panelWidth,3) <> round(PanelDef.PanelProperty("PanelWidth"),3) : 
                    PanelDef.SetName(PanelDef.GetName() + " -Width:"+str(round(panelWidth,2)))
                
                #-----Resize panel ----
                PanelDef.Height(panelHeight)
                PanelDef.Width(panelWidth)

                
                #----Run Conditional SkinParameters on Panel
                PanelDef.RunConditionalDefinition()
                
                #Draw panel geometry to create block
                PanelDef.Draw() 
                
                #Add new panel type to Database
                CurrBayList = PanelTypes.get(currBayPanel.GetName())
                CurrBayList.append([PanelDef, copy.deepcopy(ChangeFlag)])
                PanelTypes[currBayPanel.GetName()] = CurrBayList
                
                #-----Generate new Panel Block params --------------------------------------------------
                
                BlockName = "_P_ID-" + self.__m_skinGenName + "_" + str(ChangeFlag) + currBayPanel.GetName()
                #blockCounter = 1
                #print "New"; print BlockName
                
            #-----Create Block instance with current panel design
            blnIsNew = PanelDef.CreateBlockCopy(BlockName, arrAreaPanelPoints)
            if  blnIsNew : PanelDef.DeleteObjects() #Delete panel objects if creted for the new block (panel type)
            
            #-------Post current panel checkups
            
            #if  RESET_BAY_AT_POINTS and panelWidth/PanelDef.GetWidth() <  .99: #cheap new-segment-checkup (to be improved)
                #bayIndex = 0 #start with full new bay if start of new facade segment
                
    
        return PanelTypes, BayData
    
    
    #--------------------------------------------------------------------------------
    #Retrieve 4 cornes on grid array of skin
    #--------------------------------------------------------------------------------
    def GetPanelMatrix(self, bayMatrix, intLevel, intBayID, currentBay):
        
        arrAreaBayPoints = [bayMatrix[intLevel][intBayID], bayMatrix[intLevel][intBayID + 1],\
            bayMatrix[intLevel + 1][intBayID], bayMatrix[intLevel + 1][intBayID + 1]]
        panelMatrix = []
        bayLength = 0
        for panel in currentBay :
            bayLength += panel.PanelProperty("PanelWidth")        
            
        linesBay = [0,0]
        for pairIndex in [0,1]:
            linesBay[pairIndex]= rs.AddLine(arrAreaBayPoints[pairIndex*2], arrAreaBayPoints[pairIndex*2+1])
            lengthLine = rs.CurveLength(linesBay[pairIndex])
            coefLength = 1
            lengthTotals = 0
            for panel in currentBay :
                
                if intBayID == len(bayMatrix[intLevel])-2:
                    prevCoefLength = 1
                    if intBayID > 0 :
                        prevCoefLength = rs.Distance(bayMatrix[intLevel][intBayID-1], bayMatrix[intLevel][intBayID])/bayLength
                    if (bayLength-lengthTotals)< panel.PanelProperty("PanelWidth")*prevCoefLength:
                        coefLength = lengthLine/bayLength
                lengthTotals += panel.PanelProperty("PanelWidth")*coefLength
                if lengthTotals < lengthLine : rs.InsertCurveKnot(linesBay[pairIndex], lengthTotals)
                
            panelMatrix.append(rs.CurveEditPoints(linesBay[pairIndex]))
            rs.DeleteObject(linesBay[pairIndex])
        
        return panelMatrix
        
        
        
    
    #--------------------------------------------------------------------------------
    #Retrieve 4 cornes on grid array of skin
    #--------------------------------------------------------------------------------
    def GetPanelCorners(self, arrPanelMatrix, bayPanelIndex):
    
        return [arrPanelMatrix[0][bayPanelIndex], arrPanelMatrix[0][bayPanelIndex + 1],\
            arrPanelMatrix[1][bayPanelIndex], arrPanelMatrix[1][bayPanelIndex + 1]]


    #--------------------------------------------------------------------------------------------------
    # DESIGN FUNCTIONS SECTION
    #--------------------------------------------------------------------------------------------------
    def DesFunc_Default_Panel_Bays(self, PanelBay_List, bayIndex, defaultBayList=None):

        validBayList = copy.deepcopy(defaultBayList)
        
        # Define new current bay index based on the exclude bays listed 
        if  validBayList:   
            for index in range(len(validBayList)) : validBayList[index] -=1 #cero based indexes
        else: validBayList = range(len(PanelBay_List))
        
        while True:
            if  bayIndex in validBayList : break
            bayIndex +=1
            if bayIndex == len(PanelBay_List) : bayIndex = min(validBayList)
                
                
        return [PanelBay_List[bayIndex], bayIndex]
        
        

sc.sticky["SGLib_Panel"] = Panel

sc.sticky["SGLib_Skin"] = Skin


print "Done"