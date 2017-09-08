


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

ghenv.Component.Name = "SGLibrary_SkinGenerator"
ghenv.Component.NickName = 'S_G_Lib'
ghenv.Component.Message = 'VER 0.0.43\nDEC_14_2015'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "01 | Construction"
# Creates an array of points on a surface
import rhinoscriptsyntax as rs
import copy
from types import *
import scriptcontext as sc

class Panel:
    __m_strName = ""
    __m_dblHeight = 0           #: Wall Height
    __m_dblWidth = 0            #: Wall Width
    __m_dblWallThickness = 0    #: Wall Depth
    
    __m_arrDeformBox = []
    __m_arrBoundingBox = []
    __m_blnShowDeform = 0
    __m_TransformMatrix = []
    
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
    #LadybugParameters
   
    __m_arrLadybugData = []
    __m_LadybugShadeThresh = 0.0
    
    
    __rhObjectSurface = 8       #:Parameters for Boolean
    __rhObjectPolysurface = 16  #:Parameters for Boolean
    
    #----------------------------------------------------------------------------------------------------------------------
    #CONSTRUCTOR ----------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        print" Its on again"
        
        #Panel parameters
        self.__m_strName = ""
        self.__m_arrBlockInstances=[]
        self.__m_strDrawMode = "DEFAULT"
        
        #Wall Default Parameters
        self.__m_dblHeight = 12.0
        self.__m_dblWidth = 5.5
        self.__m_dblWallThickness = 0.1
        self.__m_blnShowWall = True
        self.__m_arrWallObjects = [0]
        
        #Pane Parameters (default feet units)
        self.__m_strPaneName = "Default-Pane"
        self.__m_dblPaneThickness = 0.02
        self.__m_dblPaneOffset = 0.06
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
         
        #Mulions Parameters (default feet units)
        self.__m_dblMullionWidth = 0.25
        self.__m_dblMullionThickness = 0.5
        self.__m_dblMullionCapThickness = 0.25 
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
        #----------------------------------------------------------------------------
        #Ladybug Parameters
        self.__m_LadybugShadeThresh = 0.1   # min value in meters for shading/mullions caps to be created in "LADYBUG"  draw mode)
        
        
        #---------------------------------------------------------------------
        rs.AddLayer ("_P_0") 
        rs.AddLayer ("_P_Glass")        #: To Create in "_P_Glass" Layer
        rs.AddLayer ("_P_Wall")          #: To Create Wall in "_P_Wall" Layer
        rs.AddLayer ("_P_Mullions")   
        rs.AddLayer ("_P_Shading") 
        #---------------------------------------------------------------------
        
    def __del__(self):
        print "Bye"
        
        
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
        if someHeight <= 0 : return
        self.__m_dblHeight = someHeight
        self.__m_arrBoundingBox = self.__ResetBoundingBox()
        
    def GetWidth(self):
        return self.__m_dblWidth
        
    def Width(self, someWidth):
        if someWidth <= 0 : return
        self.__m_dblWidth = someWidth
        self.__m_arrBoundingBox = self.__ResetBoundingBox()
        
    def GetThickness(self):
        return self.__m_dblWallThickness
        
    def Thickness(self, someThickness):
        self.__m_dblWallThickness = someThickness
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
    #Copy objects/properties of provided panel
    
    def Copy(self, myPanel):
        
        #General panel properties
        self.__m_strName = myPanel.GetName()
        self.__m_dblHeight = myPanel.PanelProperty("PanelHeight")      #: Wall Height
        self.__m_dblWidth = myPanel.PanelProperty("PanelWidth")          #: Wall Width             ': Location of Wall
        self.__m_arrDeformBox = myPanel.PanelProperty("DeformBox")
        self.__m_strDrawMode = myPanel.GetDrawMode()
        #self.__m_arrBlockInstances = myPanel.PanelProperty("BlockInstances")
        
        #Wall properties
        self.__m_dblWallThickness = myPanel.PanelProperty("PanelThickness")     #: Wall Depth
        self.__m_blnShowWall = myPanel.PanelProperty("WallVisibility")
        #if self.__m_blnShowWall : self.__m_arrWallObjects = rs.CopyObjects(myPanel.PanelProperty("WallObjects"))
        
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
        
        #if self.__m_blnShowPane : self.__m_arrPaneObjects = rs.CopyObjects(myPanel.PanelProperty("PaneObjects"))
        
        #Window Parameters
        self.__m_blnShowWindow = myPanel.PanelProperty("WindowVisibility") 
        self.__m_dblWinGlassThickness = myPanel.PanelProperty("WindowGlassThickness")
        self.__m_dblWinGlassOffset = myPanel.PanelProperty("WindowGlassOffset")
        
        #if self.__m_blnShowWindow and myPanel.PanelProperty("WindowObjects")[0]:
            #self.__m_arrWindowObjects = rs.CopyObjects(myPanel.PanelProperty("WindowObjects"))
        self.__m_arrWindowPoints = myPanel.PanelProperty("WindowPoints")

        #Mullion Parameters
        self.__m_blnShowMullions = myPanel.PanelProperty("MullionVisibility") 
        self.__m_blnShowMullionsCap = myPanel.PanelProperty("MullionCapVisibility")
        self.__m_dblMullionWidth = myPanel.PanelProperty("MullionWidth")
        self.__m_dblMullionThickness = myPanel.PanelProperty("MullionThickness") 
        self.__m_dblMullionCapThickness = myPanel.PanelProperty("MullionCapThickness") 

        #Copy mullions objects
        #if self.__m_blnShowMullions :
            #self.__m_arrMullionHorObjects = []
            #for i in range(myPanel.PanelProperty("MullionHorNum")):
                #arrMullions = myPanel.PanelPropertyArray("MullionHorObjArray", i)
                #if not type(arrMullions[0]) == IntType :
                    #self.__m_arrMullionHorObjects.append(rs.CopyObjects(arrMullions))
                    
            #self.__m_arrMullionVertObjects = []
            #for i in range(myPanel.PanelProperty("MullionVertNum")):
                #arrMullions = myPanel.PanelPropertyArray("MullionVertObjArray", i)
                #if not type(arrMullions[0]) == IntType :
                    #self.__m_arrMullionVertObjects.append(rs.CopyObjects(arrMullions))

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
        #if self.__m_blnShowShading and myPanel.PanelProperty("ShadingObjects")[0]:
            #self.__m_arrShadingObjects = rs.CopyObjects(myPanel.PanelProperty("ShadingObjects"))
            
        #Copy Shading Data
        self.__m_arrShadingUserData = []
        for i in range(myPanel.PanelProperty("ShadingDataNum")):
            arrShadingData = copy.deepcopy(myPanel.PanelPropertyArray("ShadingDataArray", i))
            if type(arrShadingData) == ListType :
                self.__m_arrShadingUserData.append(arrShadingData)
                
                
        #Deform parameters
        self.__m_arrDeformBox = myPanel.PanelProperty("DeformBox")
        self.__m_arrBoundingBox = myPanel.PanelProperty("BoundingBox")
        self.__m_arrBoundingBox = myPanel.PanelProperty("BoundingBox")
        self.__m_blnShowDeform = myPanel.PanelProperty("DeformVisibility")
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    
    

    def CreateBlockCopy(self, strBlockName, arrAreaPanelPoints):
        
        #create block if not created already
        if not rs.IsBlock(strBlockName) :
            arrBlockObjects = []
            
            if  not type(self.__m_arrWallObjects[0]) == IntType and rs.IsObject(self.__m_arrWallObjects[0]):
                arrBlockObjects += self.__m_arrWallObjects

            if  not type(self.__m_arrWindowObjects[0]) == IntType and rs.IsObject(self.__m_arrWindowObjects[0]):
                arrBlockObjects +=  self.__m_arrWindowObjects

            if  not type(self.__m_arrPaneObjects[0]) == IntType and rs.IsObject(self.__m_arrPaneObjects[0]):
                arrBlockObjects += self.__m_arrPaneObjects

            for i in range(self.PanelProperty("MullionHorNum")):
                arrMullions = self.PanelPropertyArray("MullionHorObjArray", i)
                if arrMullions and not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                    arrBlockObjects += arrMullions

            for i in range(self.PanelProperty("MullionVertNum")):
                arrMullions = self.PanelPropertyArray("MullionVertObjArray", i)
                if arrMullions and not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                    arrBlockObjects += arrMullions

            if  not type(self.__m_arrShadingObjects[0]) == IntType and rs.IsObject(self.__m_arrShadingObjects[0]):
                arrBlockObjects +=  self.__m_arrShadingObjects
            
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
        
        if  not type(self.__m_arrWallObjects[0]) == IntType and rs.IsObject(self.__m_arrWallObjects[0]): 
            rs.DeleteObjects(self.__m_arrWallObjects)

        
        if  not type(self.__m_arrPaneObjects[0]) == IntType and rs.IsObject(self.__m_arrPaneObjects[0]):
            rs.DeleteObjects(self.__m_arrPaneObjects)
             
        if  not type(self.__m_arrWindowObjects[0]) == IntType and rs.IsObject(self.__m_arrWindowObjects[0]): 
            rs.DeleteObjects(self.__m_arrWindowObjects)

        for i in range(self.PanelProperty("MullionHorNum")):
            arrMullions = self.PanelPropertyArray("MullionHorObjArray", i)
            if not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                rs.DeleteObjects(arrMullions)
            
        for i in range(self.PanelProperty("MullionVertNum")):
            arrMullions = self.PanelPropertyArray("MullionVertObjArray", i)
            if not type(arrMullions[0]) == IntType and rs.IsObject(arrMullions[0]):
                rs.DeleteObjects(arrMullions)
                
        if  not type(self.__m_arrShadingObjects[0]) == IntType and rs.IsObject(self.__m_arrShadingObjects[0]): 
            rs.DeleteObjects(self.__m_arrShadingObjects)

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
    #--------ADDING/REMOVING ELEMENTS SECTION------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
            
            
    def AddWindow(self, width=1, height=1, fromLeft="C", fromBottom="C", recess=0, thickness=0.02):
        
        if width > self.PanelProperty("PanelWidth") or \
           height > self.PanelProperty("PanelHeight") : return  #Ignore AddWindow if doesn't fit in panel.
           
        dblGlassWidth = width ; dblGlassHeight = height
        dblGlassThickness = thickness ; dblGlassRecess = recess
        
        if type(fromLeft) is FloatType or type(fromLeft) is IntType : dblGlassDisLeft = fromLeft
        else : dblGlassDisLeft = (self.PanelProperty("PanelWidth")-width)/2.0        
            
        if type(fromBottom) is FloatType or type(fromBottom) is IntType : dblGlassDisBottom = fromBottom
        else : dblGlassDisBottom = (self.PanelProperty("PanelHeight")-height)/2.0       
        
        if (dblGlassDisLeft + dblGlassWidth) > self.PanelProperty("PanelWidth") : print "Invalid Window params" ; return
        if (dblGlassDisBottom + dblGlassHeight) > self.PanelProperty("PanelHeight") : print "Invalid Window params" ; return
        
        self.__m_arrWindowPoints[0] = [dblGlassDisLeft, 0, dblGlassDisBottom]
        self.__m_arrWindowPoints[1] = [dblGlassDisLeft + dblGlassWidth, 0, dblGlassDisBottom]
        self.__m_arrWindowPoints[2] = [dblGlassDisLeft + dblGlassWidth, 0, dblGlassDisBottom + dblGlassHeight]
        self.__m_arrWindowPoints[3] = [dblGlassDisLeft, 0, dblGlassDisBottom + dblGlassHeight]
        self.__m_dblWinGlassThickness = dblGlassThickness
        self.__m_dblWinGlassOffset = dblGlassRecess
        self.__m_blnShowWindow = True
            
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
        
    def AddPane(self, paneName="_P_DefaultPane", thickness=0.02, offset=0.02, offsetEdge=0, tileWidth=0, tileHeight=0, tileThickness=0, tileGap=0):
        
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
    def AddBaseMullions(self, width=0.05, thickness=0.1, capThickness=0.05):
        
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
            self.AddMullionType(strType, width, thickness, capThickness)

        self.__m_blnShowMullions = True



    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def AddWindowMullions(self, width=0.05, thickness=0.1, capThickness=0.05):
        MullionTypes = ["WindowLeft","WindowRight","WindowBottom","WindowTop"]
        for strType in MullionTypes :
            self.AddMullionType(strType, width, thickness, capThickness)


    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def AddPanelMullions(self, width=0.05, thickness=0.1, capThickness=0.05):
        MullionTypes = ["PanelLeft", "PanelRight", "PanelBottom", "PanelTop"]
        for strType in MullionTypes :
            self.AddMullionType(strType, width, thickness, capThickness)
            
            

    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    #Use to add a predefined mullion Type

    def AddMullionType(self, type, width=0.05, thickness=0.1, capWidth=None, capThickness=0.05):
        
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
    def AddMullionAt(self, direction=None, distance="C", width=0.05, thickness=0.1, capThickness=0.05) :
        
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


    def AddShadingType(self, strShadingType, layerName="_P_Shading", fromLeftBottom=[0,0], fromRightTop=None, fromEdge = None, width=.05, thickness=0.05, offset=0, spacing=.1, rotation=0) :
            
        
        ShadingTypes = ["HorizontalShade","VerticalShade", "HorizontalLouver", "VerticalLouver"]
        if  strShadingType not in ShadingTypes : 
            print "Wrong shading type" 
            return
        
         #Check for 2 valid possible methods to specify sunshade values       
        if strShadingType in ["HorizontalLouver", "VerticalLouver"] and type(fromRightTop) <> ListType : 
            print "Wrong or missing Shading: fromRightTop parameter" ; return
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
    # Delete Sghading type: Deletes objects and data strcutures with objects paramters----
    def DeleteShadingType(self, type):
    
        if type not in self.__m_arrShadingUserData[0] : return
        
        i = self.__m_arrShadingUserData[0].index(type)
        for arrIndex in range(len(self.__m_arrShadingUserData)) :
            del self.__m_arrShadingUserData[arrIndex][i]
       
        if len(self.__m_arrShadingUserData[0]) == 0 : self.__m_blnShowShading = False
        
        self.DeleteShadingType(type) #Check again for more cases 
            
    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    
    def RotateShadingType(self, type, rotation):
    
        if type not in self.__m_arrShadingUserData[0] : return
        
        i = self.__m_arrShadingUserData[0].index(type)
        self.__m_arrShadingUserData[7][i] = rotation
            
            



    #----------------------------------------------------------------------------------------------------------------------            
    #PANEL ELEMENTS HIDE/SHOW SECTION--Deletes objects and "Show" varialbles set to off, data strcutures left undtouched----
    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------
    
    def ShowWall(self):
        if not self.__m_blnShowWall :
            self.__m_blnShowWall = True 
            self.DrawWall()

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
            self.DrawPane()	

    def HidePane(self):
        #Delete Old Wall Cover objects if exists.
        if self.__m_arrPaneObjects and not type(self.__m_arrPaneObjects[0]) == IntType and rs.IsObject(self.__m_arrPaneObjects[0]): 
            rs.DeleteObjects(self.__m_arrPaneObjects)
            
        self.__m_blnShowPane = False
        
        
    #----------------------------------------------------------------------------------------------------------------------	
    #----------------------------------------------------------------------------------------------------------------------

    def ShowWindow(self):
        if not self.__m_blnShowWindow :
            self.__m_blnShowWindow = True
            self.ShowMullions()
            self.Draw()
        
        
    def HideWindow(self):
        #Delete Window if Exists.
        if self.__m_arrWindowObjects and not type(self.__m_arrWindowObjects[0]) == IntType and rs.IsObject(self.__m_arrWindowObjects[0]): 
            rs.DeleteObjects(self.__m_arrWindowObjects)
            #self.__m_arrWindowPoints = [0,0,0,0]
            
        self.__m_blnShowWindow = False
        

    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
    def ShowMullions(self):
        if not self.__m_blnShowMullions :
            self.__m_blnShowMullions = True 
            self.DrawMullions()
        
        
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
            self.DrawShading()
        
        
    def HideShading(self):
        #Delete Shadnig if Exists.
        if self.__m_arrShadingObjects and not type(self.__m_arrShadingObjects[0]) == IntType and rs.IsObject(self.__m_arrShadingObjects[0]): 
            rs.DeleteObjects(self.__m_arrShadingObjects)
            
        self.__m_blnShowShading = False
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------

    def HideAll(self):
        self.HideMullions()
        self.HideWindow()
        self.HidePane()
        self.HideWall()
        self.HideShading()
        


    #----------------------------------------------------------------------------------------------------------------------
    #DRAW GEOMETRY SECTION-------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------

    def Draw(self):
        
        if self.__m_blnShowWall : self.DrawWall()
        
        if self.__m_blnShowWindow : self.DrawWindow()
        
        if self.__m_blnShowPane : self.DrawPane()
        
        if self.__m_blnShowMullions : self.DrawMullions()
        
        if self.__m_blnShowShading : self.DrawShading()
        
        if self.__m_blnShowDeform : self.DrawMorph()
        

        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
    def DrawWall(self):
        
        #Delete Old Wall and Window If Exist
        if  type(self.__m_arrWallObjects) == ListType and not type(self.__m_arrWallObjects[0]) == IntType \
            and rs.IsObject(self.__m_arrWallObjects[0]): rs.DeleteObjects(self.__m_arrWallObjects)
        
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
            GlsSurface = rs.AddSrfPt(self.__m_arrWindowPoints)
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
        arrWallObjectsTemp = 0
        
        rs.CurrentLayer("_P_Glass")   #: To Make "_P_Glass" Current
        
        #Create Window Panel
        
        GlsSurface = rs.AddSrfPt(self.__m_arrWindowPoints)
        
        if self.GetDrawMode() <> "LADYBUG" : # extrude panel unless in Ladybug mode
            if self.__m_dblWinGlassThickness > 0 : #create glass pane if thickness > 0 othersie just create opening
                strExtrCurve = rs.AddLine([0, 0, 0], [0, self.__m_dblWinGlassThickness, 0])
                self.__m_arrWindowObjects[0] = rs.ExtrudeSurface(GlsSurface, strExtrCurve)
                #Move to place
                rs.MoveObjects(self.__m_arrWindowObjects, [0, -self.__m_dblWinGlassOffset, 0])
                #clean up
                rs.DeleteObject(strExtrCurve)
            
            #Create Opening if wall is visible
            if self.__m_blnShowWall :
                rs.CurrentLayer("_P_Wall")
                strExtrCurve = rs.AddLine([0, 0, 0], [0, self.__m_dblWallThickness, 0])
                GlassObjectTemp = rs.ExtrudeSurface(GlsSurface, strExtrCurve)
                arrWallObjectsTemp = self.__m_arrWallObjects
                self.__m_arrWallObjects = rs.BooleanDifference(arrWallObjectsTemp[0], GlassObjectTemp, True)
                
                #Clean up
                rs.DeleteObject(strExtrCurve)
                
            rs.DeleteObject(GlsSurface)
            
        else : self.__m_arrWindowObjects[0] = GlsSurface
        
        
        rs.CurrentLayer("_P_0")
        
        self.__m_blnShowWindow = True
        
        
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
        
        dblYOffset = -self.__m_dblPaneOffset + self.__m_dblPaneThickness + 0.125 / 12 / 2.54 ###Use this version to tie panel to mullion face.###
        #dblYOffset = self.__m_dblPaneThickness + 0.125 / 12 / 2.54 # Mullion Y location (2.54 converting feet to meters)
                
        #Populating array with panel dimensions (no window points divisions)
        arrHorPoints = [[0, 0, 0], [self.__m_dblWidth, 0, 0]]
        arrVertPoints = [[0, 0, 0], [0, 0, self.__m_dblHeight]]
        

        if self.__m_blnShowWindow and (type(dblThickness) == ListType or type(dblCapThickness) == ListType) :
            #Populating arrays with points based on window plane location and panel configuration
             #3-piece mullions if curtain-wall with opening
            arrHorPoints = [[0, 0, 0], [self.__m_arrWindowPoints[0][0], 0, 0],[self.__m_arrWindowPoints[1][0], 0, 0], [self.__m_dblWidth, 0, 0]]  
            arrVertPoints = [[0, 0, 0], [0, 0, self.__m_arrWindowPoints[0][2]],[0, 0, self.__m_arrWindowPoints[2][2]], [0, 0, self.__m_dblHeight]]
        elif not self.__m_blnShowPane :#only punched window mullion type
            dblYOffset = -self.__m_dblWinGlassOffset + self.__m_dblWinGlassThickness + 0.125 / 12 / 2.54
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
                        arrXform = rs.XformTranslation([0, -capThickness - self.__m_dblPaneThickness - 0.25 / 12 / 2.54, 0]) #2.54 for Meter units
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
        
        #Populate array with new shadine lements based on Data array
        if len(self.__m_arrShadingUserData[0]) :
            for i in range(len(self.__m_arrShadingUserData[0])) : 
                rs.CurrentLayer(self.__m_arrShadingUserData[8][i])            
                self.__m_arrShadingObjects += self.DrawShadingType(self.__m_arrShadingUserData[0][i], self.__m_arrShadingUserData[1][i], self.__m_arrShadingUserData[2][i],\
                    self.__m_arrShadingUserData[3][i], self.__m_arrShadingUserData[4][i], self.__m_arrShadingUserData[5][i], self.__m_arrShadingUserData[6][i],self.__m_arrShadingUserData[7][i])
        
        if not self.__m_arrShadingObjects : self.__m_arrShadingObjects = [0]
        rs.CurrentLayer(currentLayer)
        
        
        
    def DrawShadingType(self,  strShadingType, fromLeftBottomCorner, fromRightTop, width=.05, thickness=0.05, offset=0, spacing=.1, rotation=0):
        
        #----Setting up parameters common to all shading types
        start = [0,0,0]; end = [0,0,0]
        start[1] = -offset-thickness; end[1] = -offset-thickness
        start[0] = fromLeftBottomCorner[0]; start[2] = fromLeftBottomCorner[1]
        
        #----Setting up parameters based on shading type
        #Single Shade options:
        if strShadingType == "HorizontalShade":  #---Single Vertical Shade
            end[0] = self.PanelProperty("PanelWidth")-fromRightTop
            end[2] = fromLeftBottomCorner[1]
            return [self.DrawMember(start, end, width, thickness, rotation)]
        elif strShadingType == "VerticalShade": #---Single Horizontal Shade
            end[0] = fromLeftBottomCorner[0]
            end[2] = self.PanelProperty("PanelHeight")-fromRightTop
            return [self.DrawMember(start, end, width, thickness, rotation)]
            
        #Louver type options:
        if strShadingType == "HorizontalLouver": #---VerticalLouvers
            end[0] = self.PanelProperty("PanelWidth")-fromRightTop[0]
            valZ = start[2]
            endZ = self.PanelProperty("PanelHeight")-fromRightTop[1]
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
            arrLouvers = []
            while valX <= endX :
                start[0] = end[0] = valX
                arrLouvers.append(self.DrawMember(start, end, width, thickness, rotation))
                valX += spacing
            return arrLouvers        
            
        else: print "Incorrect louver type" ; return
        
        
        
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    
    def DrawMorph(self):
        
        #Apply deformation on exixsting objects
        
        if  self.__m_blnShowWall : self.BoxMorphObject(self.__m_arrWallObjects)
        
        if  self.__m_blnShowWindow and self.__m_dblWinGlassThickness : self.BoxMorphObject(self.__m_arrWindowObjects)
        
        if  self.__m_blnShowPane : self.BoxMorphObject(self.__m_arrPaneObjects)
        
        if  self.__m_blnShowMullions :
            if self.__m_arrMullionVertObjects[0]:
                for arrMullion in self.__m_arrMullionVertObjects :
                    if  not type(arrMullion[0]) == IntType and rs.IsObject(arrMullion[0]) : self.BoxMorphObject(arrMullion)
            if self.__m_arrMullionHorObjects[0] :
                for arrMullion in self.__m_arrMullionHorObjects :
                    if  not type(arrMullion[0]) == IntType and rs.IsObject(arrMullion[0]) :  self.BoxMorphObject(arrMullion)
        
        if  self.__m_blnShowShading : self.BoxMorphObject(self.__m_arrShadingObjects)
        
        #Store deform box as new panel bounding box
        self.__m_arrBoundingBox = self.__m_arrDeformBox
        
        
    #Work around Phyton not implementing yet morphing func(BoxMorphObject) used in DrawMorph()------------------------------------------------
    def BoxMorphObject(self, arrObjects):
        rs.TransformObjects(arrObjects, self.__m_TransformMatrix)
            

#----------------------------------------------------------------------------------------------------------------------

sc.sticky["SGLib_Panel"] = Panel
print "Done"