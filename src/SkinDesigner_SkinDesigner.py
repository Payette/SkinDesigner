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


# By Santiago Garay
# SkinDesigner_SkinDesigner


"""
This is the main SkinDesigner component which contains the Panel, Skin and BaseDesignFunction APIs. 
-
    Args:


    Returns:


"""

ghenv.Component.Name = "SkinDesigner_SkinDesigner"
ghenv.Component.NickName = 'SkinDesigner'
ghenv.Component.Message = 'VER 0.1.17\nDec_17_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "01 | Construction"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

# push ladybug component to back
ghenv.Component.OnPingDocument().SelectAll()
ghenv.Component.Attributes.Selected = False
ghenv.Component.OnPingDocument().BringSelectionToTop()
ghenv.Component.OnPingDocument().DeselectAll()

import rhinoscriptsyntax as rs
import copy
from types import *
import scriptcontext as sc
import Rhino
import Rhino.Geometry as rg
import random
import math




#init set up global variables

sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
_UNIT_COEF = 1
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == Rhino.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
if unitSystem == Rhino.UnitSystem.Millimeters: _UNIT_COEF = 1000
sc.doc = ghdoc



class Panel:
    
    
    
    #----------------------------------------------------------------------------------------------------------------------
    #CONSTRUCTOR ----------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        
        #Doc Parameters
        self.__m_unitCoef = _UNIT_COEF #Coeficient used to adjust dimensions used inside Panel Class (Meter is 1)
        self.__m_dimRoundCoef = 1.01  #Coeficient ot absorb panel grid dimensions rounding errors
        
        #Skin Context Parameters
        self.__m_SkinParent = None
        self.__m_SkinParentName = None
        self.__m_SkinPlacementType = None

        #Panel Parameters
        self.__m_strName = ""
        self.__m_arrBlockInstances=[]
        self.__m_strDrawMode = "DEFAULT"
        self.__m_warningData = [] # panel warning data will be stored here
        
        #Wall Default Parameters
        self.__m_dblHeight = 3.5 * self.__m_unitCoef
        self.__m_dblWidth = 1.5 * self.__m_unitCoef
        self.__m_dblWallThickness = 0.1 * self.__m_unitCoef
        self.__m_blnShowWall = True
        self.__m_arrWallObjects = [0]
        self.__m_arrWallBreps = [0] 
        
        #Pane Parameters (default feet units)
        self.__m_strPaneName = "Default-Pane"
        self.__m_dblPaneThickness = 0.02 * self.__m_unitCoef
        self.__m_dblPaneOffset = 0.06 * self.__m_unitCoef
        self.__m_dblPaneOffsetEdge = 0
        self.__m_blnShowPane = False
        self.__m_arrPaneObjects = [0]
        self.__m_arrPaneBreps = [0]
        self.__m_dblPaneTileWidth = 0
        self.__m_dblPaneTileHeight = 0
        self.__m_dblPaneTileThickness = 0
        self.__m_dblPaneTileGap = 0
    
        #Window
        self.__m_arrWindowPoints = [0,0,0,0]
        self.__m_dblWinGlassThickness = 0    #: Glass Thickness
        self.__m_dblWinGlassOffset = 0       #: Distance From Outer Surface of Glass to Outer Surface of Wall
        self.__m_arrWindowObjects = [0]
        self.__m_arrWindowBreps = [0]
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
        self.__m_arrMullionHorBreps = [[0]]
        self.__m_arrMullionVertBreps = [[0]]
        
        self.__m_arrMullionVertUserData = [[],[],[],[],[]]
        self.__m_arrMullionHorUserData = [[],[],[],[],[]]
        
        
        #Init Shading data
        self.__m_blnShowShading = False
        self.__m_arrShadingObjects = [0]
        self.__m_arrShadingUserData = [[],[],[],[],[],[],[],[],[],[]]
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
        self.__m_CustomGeoBreps = []
        self.__m_CustomGeoBaseData = []
        self.__m_CustomGeoDrawBreps = []
        self.__m_CustomGeoObjects = []
        self.__m_CG_vecPlacement = rg.Vector3d(0,0,0)
        self.__m_CG_vecScaleFactor = rg.Vector3d(1,1,1)
        self.__m_CG_vecUpVector = rg.Vector3d(0,0,1)
        self.__m_CG_blnTilable = False
        self.__m_CG_dblRotation = 0
        self.__m_CG_windowDepth = 0
        self.__m_CG_trimToPanelSize = False
        
        #-----------------------------------------------------------------------------        
        #Ladybug Parameters
        self.__m_LadybugShadeThresh = 0.1 * self.__m_unitCoef   # min value (in meters) for shading/mullions caps to be created in "LADYBUG"  draw mode)
        
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
        if "\n" in someName : self.__m_warningData.append("Invalid Name - data ignored"); return False 
        self.__m_strName = someName
        
    def GetHeight(self):
        return self.__m_dblHeight
        
    def SetHeight(self, someHeight):

        if type(someHeight) == StringType : someHeight = eval(someHeight)
        
        if someHeight <= 0 : return
        self.__m_dblHeight = someHeight
        self.__m_arrBoundingBox = self.__ResetBoundingBox()
                
        self.UpdateWindow() #Check if window does fit in panel
        
    def GetWidth(self):
        return self.__m_dblWidth
        
        
    def SetWidth(self, someWidth):
        
        if someWidth <= 0 : return
        
        if type(someWidth) == StringType : someWidth = eval(someWidth)
        
        self.__m_dblWidth = someWidth
        self.__m_arrBoundingBox = self.__ResetBoundingBox()
        
        self.UpdateWindow() #Check if window does fit in panel
        
    def GetThickness(self):
        return self.__m_dblWallThickness
        
        
    def SetThickness(self, someThickness):
        
        if type(someThickness) == StringType : someThickness = eval(someThickness)
        
        if someThickness == 0 : 
            self.__m_dblWallThickness = 0.001
        else: self.__m_dblWallThickness = someThickness
        
        self.__m_arrBoundingBox = self.__ResetBoundingBox()
        
        
    def SetDrawMode(self, strMode):
        if strMode in ["DEFAULT", "LADYBUG"] : self.__m_strDrawMode = strMode
        
    def GetDrawMode(self):
        return self.__m_strDrawMode
        
    def GetPanelProperty(self, strPropName):
        properties= ["PanelHeight", "PanelWidth", "PanelThickness", 'WindowData', "WindowVisibility", "SkinPlacement", \
            "BoundingBox", "BlockInstances", "WarningData"]
        if strPropName in  properties :
            return self.__GetPanelProperty(strPropName)
        
    def __GetPanelProperty(self, strPropName):

        PanelProperty = None
        
        #Panel Data        
        if strPropName == "PanelHeight":PanelProperty = self.__m_dblHeight
        elif strPropName ==  "PanelWidth":PanelProperty = self.__m_dblWidth
        #Wall Data
        elif strPropName ==  "PanelThickness":PanelProperty = self.__m_dblWallThickness
        elif strPropName ==  "WallVisibility":PanelProperty = self.__m_blnShowWall
        elif strPropName ==  "WallObjects":PanelProperty = self.__m_arrWallBreps
        #Deform Data
        elif strPropName == "BoundingBox":PanelProperty = self.__m_arrBoundingBox
        elif strPropName ==  "DeformVisibility":PanelProperty = self.__m_blnShowDeform
        elif strPropName ==  "DeformBox":PanelProperty = self.__m_arrDeformBox
       #Blocks Data
        elif strPropName == "BlockInstances":PanelProperty = self.__m_arrBlockInstances
       #Pane Data
        elif strPropName ==  "PaneName":PanelProperty = self.__m_strPaneName
        elif strPropName ==  "PaneVisibility":PanelProperty = self.__m_blnShowPane
        elif strPropName ==  "PaneThickness":PanelProperty = self.__m_dblPaneThickness
        elif strPropName ==  "PaneOffset":PanelProperty = self.__m_dblPaneOffset
        elif strPropName ==  "PaneOffsetEdge":PanelProperty = self.__m_dblPaneOffsetEdge
        elif strPropName ==  "PaneObjects":PanelProperty = self.__m_arrPaneBreps
        elif strPropName ==  "PaneTileWidth":PanelProperty = self.__m_dblPaneTileWidth
        elif strPropName ==  "PaneTileHeight":PanelProperty = self.__m_dblPaneTileHeight
        elif strPropName ==  "PaneTileThickness":PanelProperty = self.__m_dblPaneTileThickness
        elif strPropName ==  "PaneTileGap":PanelProperty = self.__m_dblPaneTileGap
        #Window Data
        elif strPropName ==  "WindowPoints":PanelProperty = self.__m_arrWindowPoints 
        elif strPropName ==  "WindowVisibility":PanelProperty = self.__m_blnShowWindow
        elif strPropName ==  "WindowGlassThickness":PanelProperty = self.__m_dblWinGlassThickness
        elif strPropName ==  "WindowGlassOffset":PanelProperty = self.__m_dblWinGlassOffset
        elif strPropName ==  "WindowObjects":PanelProperty = self.__m_arrWindowBreps
        elif strPropName == "WindowWidth":PanelProperty = self.__m_arrWindowPoints[1][0]-self.__m_arrWindowPoints[0][0]
        elif strPropName == "WindowHeight":PanelProperty = self.__m_arrWindowPoints[2][2]-self.__m_arrWindowPoints[1][2]
        elif strPropName == "WindowBottom":PanelProperty = self.__m_arrWindowPoints[0][2]
        elif strPropName == "WindowTop":PanelProperty = self.GetHeight()-self.__m_arrWindowPoints[2][2]
        elif strPropName == "WindowLeft":PanelProperty = self.__m_arrWindowPoints[0][0]
        elif strPropName == "WindowRight":PanelProperty = self.GetWidth()-self.__m_arrWindowPoints[1][0]
        elif strPropName == "WindowData":PanelProperty = self.__m_arrWindowUserData
        #Mullion Data
        elif strPropName ==  "MullionWidth":PanelProperty = self.__m_dblMullionWidth
        elif strPropName ==  "MullionThickness":PanelProperty = self.__m_dblMullionThickness
        elif strPropName ==  "MullionCapThickness":PanelProperty = self.__m_dblMullionCapThickness
        elif strPropName ==  "MullionVisibility":PanelProperty = self.__m_blnShowMullions 
        elif strPropName ==  "MullionCapVisibility":PanelProperty = self.__m_blnShowMullionsCap
        elif strPropName ==  "MullionHorNum":PanelProperty = len(self.__m_arrMullionHorBreps)
        elif strPropName ==  "MullionVertNum":PanelProperty = len(self.__m_arrMullionVertBreps)
        elif strPropName ==  "MullionHorDataNum":PanelProperty = len(self.__m_arrMullionHorUserData)
        elif strPropName ==  "MullionVertDataNum":PanelProperty = len(self.__m_arrMullionVertUserData)
        #Shading Data
        elif strPropName ==  "ShadingVisibility":PanelProperty = self.__m_blnShowShading 
        elif strPropName ==  "ShadingObjects":PanelProperty = self.__m_arrShadingBreps
        elif strPropName ==  "ShadingDataNum":PanelProperty = len(self.__m_arrShadingUserData)  
        #Conditional definitions
        elif strPropName ==  "ConditionalDefinitions":PanelProperty = self.__m_ConditionalDefinitions
        #CustomGeometry Parameters
        elif strPropName == "CustomGeoVisibility":PanelProperty = self.__m_blnShowCustomGeo
        elif strPropName == "CustomGeoBrep":PanelProperty = self.__m_CustomGeoBreps
        elif strPropName == "CustomGeoOriginalBrep":PanelProperty = self.__m_CustomGeoBaseData  
        elif strPropName == "CustomGeoPlacement":PanelProperty = self.__m_CG_vecPlacement 
        elif strPropName == "CustomGeoScaleFactor":PanelProperty = self.__m_CG_vecScaleFactor
        elif strPropName == "CustomGeoUpVector":PanelProperty = self.__m_CG_vecUpVector
        elif strPropName == "CustomGeoTilable":PanelProperty = self.__m_CG_blnTilable
        elif strPropName == "CustomGeoRotation":PanelProperty = self.__m_CG_dblRotation
        elif strPropName == "CustomGeoWindowDepth":PanelProperty = self.__m_CG_windowDepth
        elif strPropName == "CustomGeoTrimToPanel":PanelProperty = self.__m_CG_trimToPanelSize
        #Energy Analysis Parameters
        elif strPropName == "LB_ShadeThreshold":PanelProperty = self.__m_LadybugShadeThresh    
        #Skin Context Paramters
        elif strPropName == "SkinParent":PanelProperty = self.__m_SkinParent
        elif strPropName == "SkinParentName":PanelProperty = self.__m_SkinParentName
        elif strPropName == "SkinPlacement":PanelProperty = self.__m_SkinPlacementType
        #Misc. parameters
        elif strPropName == "WarningData":PanelProperty = self.__m_warningData
            
        return PanelProperty
        
            
    def __GetPanelPropertyArray(self, strPropName, arrayIndex):
        
        if strPropName ==  "MullionHorObjArray":PanelPropertyArray = self.__m_arrMullionHorBreps[arrayIndex]
        elif strPropName ==  "MullionVertObjArray":PanelPropertyArray = self.__m_arrMullionVertBreps[arrayIndex]
        elif strPropName ==  "MullionHorDataArray":PanelPropertyArray = self.__m_arrMullionHorUserData[arrayIndex]
        elif strPropName ==  "MullionVertDataArray":PanelPropertyArray = self.__m_arrMullionVertUserData[arrayIndex]
        elif strPropName ==  "ShadingDataArray":PanelPropertyArray = self.__m_arrShadingUserData[arrayIndex]
            
        return PanelPropertyArray


    def SetPanelProperty(self, strPropName, value ):
        if strPropName in ["DrawMode", "SkinPlacement", "LB_ShadeThreshold", "SkinParentName"] :
            self.__SetPanelProperty(strPropName, value)
        else:
            self.__m_warningData.append("Panel Parameter "+ strPropName + " is not valid")
            
    def __SetPanelProperty(self, strPropName, value ):
        
        #Panel Data        
        if strPropName == "PanelHeight":self.__m_dblHeight = value
        elif strPropName ==  "PanelWidth":self.__m_dblWidth = value
        #Wall Data
        elif strPropName ==  "PanelThickness":self.__m_dblWallThickness = value
        elif strPropName ==  "WallVisibility":self.__m_blnShowWall = value
       #Pane Data
        elif strPropName ==  "PaneName":self.__m_strPaneName = value
        elif strPropName ==  "PaneVisibility":self.__m_blnShowPane = value
        elif strPropName ==  "PaneThickness":self.__m_dblPaneThickness = value
        elif strPropName ==  "PaneOffset":self.__m_dblPaneOffset = value
        elif strPropName ==  "PaneOffsetEdge":self.__m_dblPaneOffsetEdge = value
        elif strPropName ==  "PaneTileWidth":self.__m_dblPaneTileWidth = value
        elif strPropName ==  "PaneTileHeight":self.__m_dblPaneTileHeight = value
        elif strPropName ==  "PaneTileThickness":self.__m_dblPaneTileThickness = value
        elif strPropName ==  "PaneTileGap":self.__m_dblPaneTileGap = value
        #Window Data
        elif strPropName ==  "WindowPoints":self.__m_arrWindowPoints = value
        elif strPropName ==  "WindowVisibility":self.__m_blnShowWindow = value
        elif strPropName ==  "WindowGlassThickness":self.__m_dblWinGlassThickness = value
        elif strPropName ==  "WindowGlassOffset":self.__m_dblWinGlassOffset = value
        elif strPropName == "WindowWidth":self.__m_arrWindowUserData['width'] = value
        elif strPropName == "WindowHeight":self.__m_arrWindowUserData['height'] = value
        elif strPropName == "WindowBottom":self.__m_arrWindowUserData['fromBottom'] = value
        elif strPropName == "WindowLeft":self.__m_arrWindowUserData['fromLeft'] = value
        elif strPropName == "WindowData":self.__m_arrWindowUserData = value
        #Mullion Data
        elif strPropName ==  "MullionWidth":self.__m_dblMullionWidth = value
        elif strPropName ==  "MullionThickness":self.__m_dblMullionThickness = value
        elif strPropName ==  "MullionCapThickness":self.__m_dblMullionCapThickness = value
        elif strPropName ==  "MullionVisibility":self.__m_blnShowMullions = value 
        elif strPropName ==  "MullionCapVisibility":self.__m_blnShowMullionsCap = value
        #Shading Data
        elif strPropName ==  "ShadingVisibility":self.__m_blnShowShading = value
        #array value format: [index, array data]
        elif strPropName ==  "ShadingIndexArray": self.__m_arrShadingUserData[value[0]] = value[1]
        #Conditional Defintitions
        elif strPropName ==  "ConditionalDefinitions": self.__m_ConditionalDefinitions = value
        #CustomGeometry Parameters
        elif strPropName == "CustomGeoVisibility":self.__m_blnShowCustomGeo = value
        elif strPropName == "CustomGeoBrep":self.__m_CustomGeoBreps = value
        elif strPropName == "CustomGeoOriginalBrep":self.__m_CustomGeoBaseData = value   
        elif strPropName == "CustomGeoPlacement":self.__m_CG_vecPlacement = value
        elif strPropName == "CustomGeoScaleFactor":self.__m_CG_vecScaleFactor = value
        elif strPropName == "CustomGeoUpVector":self.__m_CG_vecUpVector = value
        elif strPropName == "CustomGeoTilable":self.__m_CG_blnTilable = value
        elif strPropName == "CustomGeoRotation":self.__m_CG_dblRotation = value
        elif strPropName == "CustomGeoWindowDepth":self.__m_CG_windowDepth = value
        elif strPropName == "CustomGeoTrimToPanel":self.__m_CG_trimToPanelSize = value
        #Energy Anlaysis Parameters
        elif strPropName == "LB_ShadeThreshold":self.__m_LadybugShadeThresh = value
        #Skin Context Parameters
        elif strPropName == "SkinParent":self.__m_SkinParent = value
        elif strPropName == "SkinParentName":self.__m_SkinParentName = value
        elif strPropName == "SkinPlacement":self.__m_SkinPlacementType = value
        else: self.__m_warningData.append("Invalid panel property: " + strPropName)
        
        return
        




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
        self.__m_SkinParent = myPanel.__GetPanelProperty("SkinParent")
        self.__m_SkinParentName = myPanel.__GetPanelProperty("SkinParentName")        
        self.__m_SkinPlacementType = myPanel.__GetPanelProperty("SkinPlacement")

        self.__m_strName = myPanel.GetName()
        self.__m_dblHeight = myPanel.__GetPanelProperty("PanelHeight") #: Wall Height
        self.__m_dblWidth = myPanel.__GetPanelProperty("PanelWidth") # Wall Width  
        
        self.__m_strDrawMode = myPanel.GetDrawMode()
        self.__m_ConditionalDefinitions = copy.deepcopy(myPanel.__GetPanelProperty("ConditionalDefinitions"))
        
        #Wall properties
        self.__m_dblWallThickness = myPanel.__GetPanelProperty("PanelThickness") #: Wall Depth
        self.__m_blnShowWall = myPanel.__GetPanelProperty("WallVisibility")
        
        #Pane parameters
        self.__m_blnShowPane = myPanel.__GetPanelProperty("PaneVisibility")
        self.__m_strPaneName = myPanel.__GetPanelProperty("PaneName")
        self.__m_dblPaneThickness = myPanel.__GetPanelProperty("PaneThickness")
        self.__m_dblPaneOffset = myPanel.__GetPanelProperty("PaneOffset")
        self.__m_dblPaneOffsetEdge = myPanel.__GetPanelProperty("PaneOffsetEdge")
        
        self.__m_dblPaneTileWidth  = myPanel.__GetPanelProperty("PaneTileWidth")
        self.__m_dblPaneTileHeight = myPanel.__GetPanelProperty("PaneTileHeight")
        self.__m_dblPaneTileThickness = myPanel.__GetPanelProperty("PaneTileThickness")
        self.__m_dblPaneTileGap = myPanel.__GetPanelProperty("PaneTileGap")
        
        
        #Window Parameters
        self.__m_blnShowWindow = myPanel.__GetPanelProperty("WindowVisibility") 
        self.__m_dblWinGlassThickness = myPanel.__GetPanelProperty("WindowGlassThickness")
        self.__m_dblWinGlassOffset = myPanel.__GetPanelProperty("WindowGlassOffset")
        self.__m_arrWindowPoints = copy.deepcopy(myPanel.__GetPanelProperty("WindowPoints"))
        self.__m_arrWindowUserData = copy.deepcopy(myPanel.__GetPanelProperty("WindowData"))
        
        #Mullion Parameters
        self.__m_blnShowMullions = myPanel.__GetPanelProperty("MullionVisibility") 
        self.__m_blnShowMullionsCap = myPanel.__GetPanelProperty("MullionCapVisibility")
        self.__m_dblMullionWidth = myPanel.__GetPanelProperty("MullionWidth")
        self.__m_dblMullionThickness = myPanel.__GetPanelProperty("MullionThickness") 
        self.__m_dblMullionCapThickness = myPanel.__GetPanelProperty("MullionCapThickness") 

        #Copy mullions Data
        self.__m_arrMullionVertUserData = []
        self.__m_arrMullionHorUserData = []
        
        for i in range(myPanel.__GetPanelProperty("MullionHorDataNum")):
            arrMullions = copy.deepcopy(myPanel.__GetPanelPropertyArray("MullionHorDataArray", i))
            if type(arrMullions) == ListType :
                self.__m_arrMullionHorUserData.append(arrMullions)
                
        for i in range(myPanel.__GetPanelProperty("MullionVertDataNum")):
            arrMullions = copy.deepcopy(myPanel.__GetPanelPropertyArray("MullionVertDataArray", i))
            if type(arrMullions) == ListType :
                self.__m_arrMullionVertUserData.append(arrMullions)
                
                
        #shading Parameetrs
        self.__m_blnShowShading = myPanel.__GetPanelProperty("ShadingVisibility")    
        
        self.__m_arrShadingUserData = []
        for i in range(myPanel.__GetPanelProperty("ShadingDataNum")):
            arrShadingData = copy.deepcopy(myPanel.__GetPanelPropertyArray("ShadingDataArray", i))
            if type(arrShadingData) == ListType :
                self.__m_arrShadingUserData.append(arrShadingData)

        #CustomGeometry Parameters
        self.__m_blnShowCustomGeo = myPanel.__GetPanelProperty("CustomGeoVisibility")
        self.__m_CustomGeoBreps = myPanel.__GetPanelProperty("CustomGeoBrep")
        self.__m_CustomGeoBaseData = myPanel.__GetPanelProperty("CustomGeoOriginalBrep")
        self.__m_CG_vecPlacement = myPanel.__GetPanelProperty("CustomGeoPlacement")
        self.__m_CG_vecScaleFactor = myPanel.__GetPanelProperty("CustomGeoScaleFactor")
        self.__m_CG_vecUpVector = myPanel.__GetPanelProperty("CustomGeoUpVector")
        self.__m_CG_blnTilable = myPanel.__GetPanelProperty("CustomGeoTilable")
        self.__m_CG_dblRotation = myPanel.__GetPanelProperty("CustomGeoRotation")
        self.__m_CG_windowDepth = myPanel.__GetPanelProperty("CustomGeoWindowDepth")
        self.__m_CG_trimToPanelSize = myPanel.__GetPanelProperty("CustomGeoTrimToPanel")
        
        #Deform parameters
        self.__m_arrDeformBox = copy.deepcopy(myPanel.__GetPanelProperty("DeformBox")) # Wall Location
        self.__m_arrBoundingBox = copy.deepcopy(myPanel.__GetPanelProperty("BoundingBox"))
        self.__m_blnShowDeform = myPanel.__GetPanelProperty("DeformVisibility")
        
        #Energy Analysis
        self.__m_LadybugShadeThresh = myPanel.__GetPanelProperty("LB_ShadeThreshold")

    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    
    

    def CreateBlockCopy(self, strBlockName, arrAreaPanelPoints, blnFitToArea):
        
        blnNewBlock = False
        
        parentLayerName = "SKIN_DESIGNER"
        if self.__m_SkinParentName <> None: parentLayerName = self.__m_SkinParentName.split("::")[0]
        if not rs.IsLayer(parentLayerName) : rs.AddLayer(parentLayerName)

        currentLayer = rs.CurrentLayer() 
        
        if not rs.IsLayer(parentLayerName+"::_P_0") : rs.AddLayer("_P_0", parent=parentLayerName)
        
        rs.CurrentLayer(parentLayerName+"::_P_0")
        
        #create block if not created already
        if not rs.IsBlock(strBlockName) :
            
            blnNewBlock = True
            
            self.DrawSceneObjects()
            
            arrBlockObjects = []
            if  self.__m_arrWallObjects and not type(self.__m_arrWallObjects[0]) == IntType and rs.IsObject(self.__m_arrWallObjects[0]):
                arrBlockObjects += self.__m_arrWallObjects

            if  self.__m_arrWindowObjects and not type(self.__m_arrWindowObjects[0]) == IntType and rs.IsObject(self.__m_arrWindowObjects[0]):
                arrBlockObjects +=  self.__m_arrWindowObjects
            
            if  self.__m_arrPaneObjects and not type(self.__m_arrPaneObjects[0]) == IntType and rs.IsObject(self.__m_arrPaneObjects[0]):
                arrBlockObjects += self.__m_arrPaneObjects

            if self.__m_arrMullionHorObjects and not type(self.__m_arrMullionHorObjects[0]) == IntType and rs.IsObject(self.__m_arrMullionHorObjects[0]):
                arrBlockObjects += self.__m_arrMullionHorObjects
            
            if self.__m_arrMullionVertObjects and not type(self.__m_arrMullionVertObjects[0]) == IntType and rs.IsObject(self.__m_arrMullionVertObjects[0]):
                arrBlockObjects += self.__m_arrMullionVertObjects
            
            if self.__m_arrShadingObjects and not type(self.__m_arrShadingObjects[0]) == IntType and rs.IsObject(self.__m_arrShadingObjects[0]):
                arrBlockObjects +=  self.__m_arrShadingObjects
            
            if self.__m_CustomGeoObjects and type(self.__m_CustomGeoObjects) == ListType and len(self.__m_CustomGeoObjects) > 0 and rs.IsObject(self.__m_CustomGeoObjects[0]):
                arrBlockObjects += self.__m_CustomGeoObjects
            
            rs.AddBlock(arrBlockObjects, self.__m_arrBoundingBox[0], strBlockName)
            self.DeleteSceneObjects()
            
        #Translate and Scale based on grid points
        
        #Start from Panel Original Bounding Box
        arrBoxPoints = self.__m_arrBoundingBox
        
        #Move Bounding Box to new locatation Plane (to avoid panel depth distortions)
        arrStartPlane = rs.PlaneFromPoints(arrBoxPoints[0], arrBoxPoints[1], arrBoxPoints[4]) #Create Plane from current Boundng Box points
        arrEndPlane = rs.PlaneFromPoints(arrAreaPanelPoints[0], arrAreaPanelPoints[1], arrAreaPanelPoints[2])#Create Plane from Panels Area points
        
        #Apply Transf. Matrix from planes on Bounding Box
        arrXform = rs.XformRotation1(arrStartPlane, arrEndPlane)
        arrNewBoxPoints = rs.PointArrayTransform(arrBoxPoints, arrXform)
        
        if blnFitToArea : #scale to fit area only if specified
            arrScaleXform = rs.XformScale([(rs.Distance(arrNewBoxPoints[0], arrAreaPanelPoints[1]) / rs.Distance(arrNewBoxPoints[0], arrNewBoxPoints[1])), 1,\
                (rs.Distance(arrNewBoxPoints[0], arrAreaPanelPoints[2]) / rs.Distance(arrNewBoxPoints[0], arrNewBoxPoints[4]))])
            arrXform = rs.XformMultiply(arrXform, arrScaleXform)
        
        
        #Create Copy and move to location
        if rs.IsBlock(strBlockName) :
            self.__m_arrBlockInstances.append(rs.InsertBlock2(strBlockName, arrXform))
            
        rs.CurrentLayer(currentLayer)
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

    def DeleteSceneObjects(self):

        if  type(self.__m_arrWallObjects) == ListType and not type(self.__m_arrWallObjects[0]) == IntType and rs.IsObject(self.__m_arrWallObjects[0]): 
            rs.DeleteObjects(self.__m_arrWallObjects)
     
        if  self.__m_arrPaneObjects and not type(self.__m_arrPaneObjects[0]) == IntType and rs.IsObject(self.__m_arrPaneObjects[0]):
            rs.DeleteObjects(self.__m_arrPaneObjects)
             
        if  self.__m_arrWindowObjects and not type(self.__m_arrWindowObjects[0]) == IntType and rs.IsObject(self.__m_arrWindowObjects[0]): 
            rs.DeleteObjects(self.__m_arrWindowObjects)

        if self.__m_arrMullionHorObjects and not type(self.__m_arrMullionHorObjects[0]) == IntType and rs.IsObject(self.__m_arrMullionHorObjects[0]):
            rs.DeleteObjects(self.__m_arrMullionHorObjects)
        
        if self.__m_arrMullionVertObjects and not type(self.__m_arrMullionVertObjects[0]) == IntType and rs.IsObject(self.__m_arrMullionVertObjects[0]):
            rs.DeleteObjects(self.__m_arrMullionVertObjects)
                
        if  self.__m_arrShadingObjects and not type(self.__m_arrShadingObjects[0]) == IntType and rs.IsObject(self.__m_arrShadingObjects[0]): 
            rs.DeleteObjects(self.__m_arrShadingObjects)
            
        if self.__m_CustomGeoObjects and type(self.__m_CustomGeoObjects) == ListType and len(self.__m_CustomGeoObjects) > 0 and rs.IsObject(self.__m_CustomGeoObjects[0]):
            rs.DeleteObjects(self.__m_CustomGeoObjects)

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
            parsedCondition = "if self.GetPanelProperty('"+parsedList[0]+"') "+parsedList[1]+" "+parsedList[2]+" : "
            
            actionList = self.__m_ConditionalDefinitions[condition]
            for strAction in actionList:
                strConditionalAction = parsedCondition + "self." + strAction
                #print strConditionalAction
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
            (dblGlassDisLeft + dblGlassWidth) > self.__GetPanelProperty("PanelWidth")*self.__m_dimRoundCoef or \
            dblGlassDisBottom + dblGlassHeight > self.__GetPanelProperty("PanelHeight")*self.__m_dimRoundCoef: 
            self.HideWindow(); print ">>> Panel " + self.GetName()+" - Window fixed size won't fit in panel - window erased"; return
        
        #load processed data in window array
        self.__m_arrWindowPoints[0] = [dblGlassDisLeft, 0, dblGlassDisBottom]
        self.__m_arrWindowPoints[1] = [dblGlassDisLeft + dblGlassWidth, 0, dblGlassDisBottom]
        self.__m_arrWindowPoints[2] = [dblGlassDisLeft + dblGlassWidth, 0, dblGlassDisBottom + dblGlassHeight]
        self.__m_arrWindowPoints[3] = [dblGlassDisLeft, 0, dblGlassDisBottom + dblGlassHeight]
        self.__m_dblWinGlassThickness = dblGlassThickness
        self.__m_dblWinGlassOffset = dblGlassRecess
            
        self.ShowWindow()
        
        
    def ModifyWindow(self, width=None, height=None, fromLeft=None, fromBottom=None, recess=None, thickness=None):
        
        if self.__m_arrWindowPoints == [0,0,0,0] : return False
        
        self.__m_arrWindowUserData['width'] = width if width<>None else self.__m_arrWindowUserData['width'] 
        self.__m_arrWindowUserData['height'] = height if height<>None else self.__m_arrWindowUserData['height'] 
        self.__m_arrWindowUserData['fromLeft'] = fromLeft if fromLeft<>None else self.__m_arrWindowUserData['fromLeft'] 
        self.__m_arrWindowUserData['fromBottom'] = fromBottom if fromBottom<>None else self.__m_arrWindowUserData['fromBottom'] 
        self.__m_arrWindowUserData['recess'] = recess if recess<>None else self.__m_arrWindowUserData['recess']
        self.__m_arrWindowUserData['thickness'] = thickness if thickness<>None else self.__m_arrWindowUserData['thickness']        
                                
        Window = self.__m_arrWindowUserData
        self.AddWindow(width=Window['width'], height=Window['height'], fromLeft=Window['fromLeft'], fromBottom=Window['fromBottom'], recess=Window['recess'], thickness=Window['thickness'])
        
        
        
    def UpdateWindow(self):
        if self.__m_arrWindowPoints == [0,0,0,0] : return False
        Window = self.__m_arrWindowUserData
        self.AddWindow(width=Window['width'], height=Window['height'], fromLeft=Window['fromLeft'], fromBottom=Window['fromBottom'], recess=Window['recess'], thickness=Window['thickness'])
        
        
    def DeleteWindow(self):
        self.HideWindow()
        self.__m_arrWindowPoints = [0,0,0,0]
        self.__m_arrWindowObjects = [0]
        self.__m_arrWindowBreps = [0]
        self.__m_blnShowWindow = False
        self.__m_arrWindowUserData = dict(width=0, height=0, fromLeft=0, fromBottom=0, recess = 0, thickness = 0)

        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
        
    def AddPane(self, paneName="_P_DefaultPane", thickness=0.02*_UNIT_COEF, offset=0.02*_UNIT_COEF, offsetEdge=0, tileWidth=0, tileHeight=0, tileThickness=0, tileGap=0.01*_UNIT_COEF):
        
        self.__m_strPaneName = str(paneName)
        self.__m_dblPaneThickness = float(thickness)
        self.__m_dblPaneOffset = float(offset)
        self.__m_dblPaneOffsetEdge = float(offsetEdge)
        self.__m_dblPaneTileWidth = float(tileWidth)
        self.__m_dblPaneTileHeight = float(tileHeight)
        self.__m_dblPaneTileThickness = float(tileThickness)
        self.__m_dblPaneTileGap = float(tileGap)
        
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

    def AddMullionType(self, strType, width=0.05*_UNIT_COEF, thickness=0.1*_UNIT_COEF, capWidth=None, capThickness=0.05*_UNIT_COEF):
        
        if strType not in ["WindowLeft","WindowRight","WindowBottom","WindowTop", "PanelLeft", "PanelRight", "PanelBottom", "PanelTop"] and \
            "Hor_fromBottom=" not in strType and "Vert_fromLeft=" not in strType: return
        try:
            if type(width) == ListType: width = width[0]
            width = float(width)
        except:
            self.__m_warningData.append("Wrong width parameter on mullion "+ strType) ; return
        try:
            if type(capWidth) == ListType: capWidth = capWidth[0]
            if capWidth <> None : capWidth = float(capWidth)
        except:
            self.__m_warningData.append("Wrong capWidth parameter on mullion "+ strType) ; return

        try:  
            if type(thickness) == ListType : thickness = list(float(num) for num in thickness)
            else: thickness = float(thickness)
        except:
            self.__m_warningData.append("Wrong thickness parameter on mullion "+ strType) ; return
        try:  
            if type(capThickness) == ListType : capThickness = list(float(num) for num in capThickness)
            else: capThickness = float(capThickness)
        except:
            self.__m_warningData.append("Wrong capThickness parameter on mullion "+ strType) ; return
            
        if capWidth == None : capWidth = width 
        
        if "Bottom" in strType or "Top" in strType or "Hor_fromBottom=" in strType:
            self.__m_arrMullionHorUserData[0] = self.__m_arrMullionHorUserData[0] + [strType]
            self.__m_arrMullionHorUserData[1] = self.__m_arrMullionHorUserData[1] + [width]
            self.__m_arrMullionHorUserData[2] = self.__m_arrMullionHorUserData[2] + [thickness]
            self.__m_arrMullionHorUserData[3] = self.__m_arrMullionHorUserData[3] + [capWidth]
            self.__m_arrMullionHorUserData[4] = self.__m_arrMullionHorUserData[4] + [capThickness]


        if "Left" in strType or "Right" in strType or "Vert_fromLeft=" in strType:
            self.__m_arrMullionVertUserData[0] = self.__m_arrMullionVertUserData[0] + [strType]
            self.__m_arrMullionVertUserData[1] = self.__m_arrMullionVertUserData[1] + [width]
            self.__m_arrMullionVertUserData[2] = self.__m_arrMullionVertUserData[2] + [thickness]
            self.__m_arrMullionVertUserData[3] = self.__m_arrMullionVertUserData[3] + [capWidth]
            self.__m_arrMullionVertUserData[4] = self.__m_arrMullionVertUserData[4] + [capThickness]
            
    
        self.__m_blnShowMullions = True

    #-----------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    def AddMullionAt(self, direction=None, distance="C", width=0.05*_UNIT_COEF, thickness=0.1*_UNIT_COEF, capThickness=0.05*_UNIT_COEF) :
        
        strType = ""
        if  (direction == "horizontal" or direction == "Horizontal") and distance :
            if distance == "C" : distance = self.__GetPanelProperty("PanelHeight")/2.0
            strType = "Hor_fromBottom=" + str(distance)
        elif  direction == "vertical" or direction == "Vertical" and distance:
            if distance == "C" : distance = self.__GetPanelProperty("PanelWidth")/2.0 
            strType = "Vert_fromLeft=" + str(distance)
        else: 
            self.__m_warningData.append("Wrong 'direction' parameter on mullion: " + str(direction)) ; return
            
        self.AddMullionType(strType, width, thickness, width, capThickness)
        self.__m_blnShowMullions = True
        
    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------

    def ChangeMullionType(self, strType=None, width=None, thickness=None, capThickness=None):


        if len(self.__m_arrMullionHorUserData[0]) :
            for i in range(len(self.__m_arrMullionHorUserData[0])):
                if  self.__m_arrMullionHorUserData[0][i] == strType or strType in self.__m_arrMullionHorUserData[0][i]:
                    if width <> None : self.__m_arrMullionHorUserData[1][i] = width
                    if thickness <> None : self.__m_arrMullionHorUserData[2][i] = thickness
                    if width <> None: self.__m_arrMullionHorUserData[3][i] = width
                    if capThickness <> None : self.__m_arrMullionHorUserData[4][i] = capThickness
                
                
        if len(self.__m_arrMullionVertUserData[0]) :
            for i in range(len(self.__m_arrMullionVertUserData[0])) :
                if  self.__m_arrMullionVertUserData[0][i] == strType or strType in self.__m_arrMullionVertUserData[0][i] :
                    if  width <> None : self.__m_arrMullionVertUserData[1][i] = width
                    if  thickness <> None : self.__m_arrMullionVertUserData[2][i] = thickness
                    if width <> None : self.__m_arrMullionVertUserData[3][i] = width
                    if  capThickness <> None : self.__m_arrMullionVertUserData[4][i] = capThickness
                
                
    #------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------
    # Delete functions:  Deletes objects and data structures based on objects' parameters----
    
    def DeleteMullionType(self, strType):
    
        if strType in self.__m_arrMullionHorUserData[0] :
            i = self.__m_arrMullionHorUserData[0].index(strType)
            del self.__m_arrMullionHorUserData[0][i]
            del self.__m_arrMullionHorUserData[1][i]
            del self.__m_arrMullionHorUserData[2][i]
            del self.__m_arrMullionHorUserData[3][i]
            del self.__m_arrMullionHorUserData[4][i]
        elif strType in self.__m_arrMullionVertUserData[0] :
            i = self.__m_arrMullionVertUserData[0].index(strType)
            del self.__m_arrMullionVertUserData[0][i]
            del self.__m_arrMullionVertUserData[1][i]
            del self.__m_arrMullionVertUserData[2][i]
            del self.__m_arrMullionVertUserData[3][i]
            del self.__m_arrMullionVertUserData[4][i]
        else: return
        
        if len(self.__m_arrMullionHorUserData[0]) == 0 and  len(self.__m_arrMullionVertUserData[0]) == 0 :
             self.__m_blnShowMullions = False
             
        self.DeleteMullionType(strType)

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
                if distance == "C" : distance = self.__GetPanelProperty("PanelHeight")/2.0
                elif  strType(distance) <> StringType : strType = "Hor_fromBottom=" + str(distance)
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
                if distance == "C" : distance = self.__GetPanelProperty("PanelWidth")/2.0
                elif  strType(distance) <> StringType : strType = "Vert_fromLeft=" + str(distance)
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


    def AddShadingType(self, strShadingType, layerName="_P_Shading", fromLeftBottom=[0.0,0.0], fromRightTop=[0.0,0.0], fromEdge = 0.0, \
        width=.05*_UNIT_COEF, thickness=0.05*_UNIT_COEF, offset=0.0, spacing=.1*_UNIT_COEF, rotation=0.0, shiftEnds=[None, None]) :

        
        if  thickness <= 0 or width <= 0 : return
        
        #handling predefined variables as string paramters
        Window = self.__m_arrWindowUserData
        PanelWidth = self.GetWidth()
        PanelHeight = self.GetHeight()
        if type(fromLeftBottom) == StringType : fromLeftBottom = eval(fromLeftBottom)
        if type(fromRightTop) == StringType : fromRightTop = eval(fromRightTop)
        
        if type(fromLeftBottom) <> ListType or (type(fromLeftBottom[0]) <> FloatType and type(fromLeftBottom[0]) <> IntType) or \
            (type(fromLeftBottom[1]) <> FloatType and type(fromLeftBottom[1])<> IntType):
            self.__m_warningData.append("Wrong Shading fromLeftBottom parameter: "+ str(fromLeftBottom) + " at "+ strShadingType)  ; return
        if type(fromEdge) == StringType : fromEdge = eval(fromEdge)
        if type(fromEdge) <> FloatType and type(fromEdge) <> IntType:
            self.__m_warningData.append("Wrong Shading fromEdge parameter: "+ strShadingType)  ; return        
        if type(fromRightTop) == StringType : fromRightTop = eval(fromRightTop)        
        if type(fromRightTop) <> ListType or (type(fromRightTop[0]) <> FloatType and type(fromRightTop[0])<> IntType) or \
            (type(fromRightTop[1]) <> FloatType and type(fromRightTop[1])<> IntType) :
            self.__m_warningData.append("Wrong Shading fromRightTop parameter: "+ strShadingType)  ; return
        
        ShadingTypes = ["HorizontalShade","VerticalShade", "HorizontalLouver", "VerticalLouver", "HorizontalWindowShade", "VerticalWindowShade", "HorizontalWindowLouver", "VerticalWindowLouver"]
        if strShadingType not in ShadingTypes: self.__m_warningData.append("Wrong shading type: "+ strShadingType) ;return   
               
         #Check for valid possible methods to specify sunshade values       
        if strShadingType in ["HorizontalLouver", "VerticalLouver"] :
            #if type(fromRightTop) <> ListType or type(fromLeftBottom[0]) <> FloatType: 
                #self.__m_warningData.append("Wrong Shading parameter fromRightTop: "+ strShadingType)  ; return
            if spacing < width : spacing = width
            if spacing < 0.02*self.__m_unitCoef : spacing = 0.02*self.__m_unitCoef
            fromEdge = None
        elif strShadingType in ["HorizontalShade", "VerticalShade", "HorizontalWindowShade", "VerticalWindowShade"] :
            if fromEdge == None : self.__m_warningData.append("Wrong Shading parameter fromEdge: "+ strShadingType) ; return
            fromRightTop = None
        elif strShadingType in ["HorizontalWindowShade", "VerticalWindowShade", "HorizontalWindowLouver", "VerticalWindowLouver"]:
            if self.__m_arrWindowPoints == [0,0,0,0]: self.__m_warningData.append("Window shading type ignored, no window present: " + strShadingType) ; return
            
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
        self.__m_arrShadingUserData[9] += [shiftEnds]

        self.__m_blnShowShading = True



    #------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------
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
    #------------------------------------------------------------------------------------------------------------------------------------
    def ModifyShadingType(self, type, fromLeftBottom=None,fromLeft=None, fromBottom=None, fromRightTop=None, fromRight=None,\
        fromTop=None, fromEdge=None, width=None, thickness=None, offset=None, spacing=None, rotation=None, layerName=None, \
        shiftEnds=None ,shiftEnd1=None, shiftEnd2=None, shiftEnd1X = None, shiftEnd1Y = None, shiftEnd1Z=None, shiftEnd2X = None,\
        shiftEnd2Y = None, shiftEnd2Z=None):
        
        if type not in self.__m_arrShadingUserData[0] : return
        
        shadingIndex = self.__m_arrShadingUserData[0].index(type)
        
        self.ModifyShadingIndex( shadingIndex, None, fromLeftBottom, fromLeft, fromBottom, fromRightTop, fromRight, fromTop, fromEdge,\
            width, thickness, offset, spacing, rotation, layerName, shiftEnds,shiftEnd1, shiftEnd2, shiftEnd1X, shiftEnd1Y, shiftEnd1Z,\
            shiftEnd2X, shiftEnd2Y, shiftEnd2Z)
        
    
    def ModifyShadingIndex(self, index, type=None, fromLeftBottom=None, fromLeft=None, fromBottom=None, fromRightTop=None, fromRight=None,\
        fromTop=None, fromEdge=None, width=None, thickness=None, offset=None, spacing=None, rotation=None, layerName=None, shiftEnds=None,\
        shiftEnd1=None, shiftEnd2=None, shiftEnd1X = None, shiftEnd1Y = None, shiftEnd1Z=None, shiftEnd2X = None, shiftEnd2Y = None, shiftEnd2Z=None):
              
        if index >= len(self.__m_arrShadingUserData[0]) : return
        
        i = index 
        if type  <> None : self.__m_arrShadingUserData[0][i] = type        
        if fromLeftBottom  <> None : self.__m_arrShadingUserData[1][i] = fromLeftBottom
        if fromLeft  <> None : self.__m_arrShadingUserData[1][i][0] = fromLeft       
        if fromBottom  <> None : self.__m_arrShadingUserData[1][i][1] = fromBottom   
        if fromRightTop <> None : self.__m_arrShadingUserData[2][i] = fromRightTop
        if fromRight  <> None : self.__m_arrShadingUserData[2][i][0] = fromRight      
        if fromTop  <> None : self.__m_arrShadingUserData[2][i][1] = fromTop  
        if fromEdge <> None : self.__m_arrShadingUserData[2][i] = fromEdge
        if width <> None : self.__m_arrShadingUserData[3][i] = width
        if thickness <> None : self.__m_arrShadingUserData[4][i] = thickness
        if offset <> None : self.__m_arrShadingUserData[5][i] = offset
        if spacing <> None : self.__m_arrShadingUserData[6][i] = spacing
        if rotation<> None : self.__m_arrShadingUserData[7][i] = rotation
        if layerName <> None : self.__m_arrShadingUserData[8][i] = layerName
        if shiftEnds <> None : self.__m_arrShadingUserData[9][i] = shiftEnds

        currShiftEnds = self.__m_arrShadingUserData[9][i] 
        if shiftEnd1 <> None : currShiftEnds[0] = shiftEnd1
        if shiftEnd2 <> None : currShiftEnds[1] = shiftEnd2
        if (shiftEnd1X <> None or shiftEnd1Y<>None or shiftEnd1Z<>None) and not isinstance(currShiftEnds[0], list):
            currShiftEnds[0]=[0,0,0]
        if (shiftEnd2X <> None or shiftEnd2Y<>None or shiftEnd2Z<>None) and not isinstance(currShiftEnds[1], list):
            currShiftEnds[1]=[0,0,0]
        if shiftEnd1X <> None : currShiftEnds[0][0] = shiftEnd1X
        if shiftEnd1Y <> None : currShiftEnds[0][1] = shiftEnd1Y
        if shiftEnd1Z <> None : currShiftEnds[0][2] = shiftEnd1Z
        if shiftEnd2X <> None : currShiftEnds[1][0] = shiftEnd2X
        if shiftEnd2Y <> None : currShiftEnds[1][1] = shiftEnd2Y
        if shiftEnd2Z <> None : currShiftEnds[1][2] = shiftEnd2Z
        

    def UpdateShading(self):
        shadingUserData = copy.deepcopy(self.__m_arrShadingUserData)
        if len(shadingUserData[0]) :
            self.DeleteShading()
            for i in range(len(shadingUserData[0])) :
                if shadingUserData[0][i] in ["HorizontalLouver", "VerticalLouver", "HorizontalWindowLouver", "VerticalWindowLouver"]:
                    self.AddShadingType(shadingUserData[0][i], layerName=shadingUserData[8][i], fromLeftBottom=shadingUserData[1][i], fromRightTop=shadingUserData[2][i],\
                        width=shadingUserData[3][i], thickness=shadingUserData[4][i], offset=shadingUserData[5][i], spacing=shadingUserData[6][i],\
                        rotation=shadingUserData[7][i], shiftEnds=shadingUserData[9][i])
                if shadingUserData[0][i] in ["HorizontalShade", "VerticalShade", "HorizontalWindowShade", "VerticalWindowShade"]:
                    self.AddShadingType(shadingUserData[0][i], layerName=shadingUserData[8][i], fromLeftBottom=shadingUserData[1][i], fromEdge=shadingUserData[2][i],\
                        width=shadingUserData[3][i], thickness=shadingUserData[4][i], offset=shadingUserData[5][i], spacing=shadingUserData[6][i],\
                        rotation=shadingUserData[7][i], shiftEnds=shadingUserData[9][i])
                        

    #------------------------------------------------------------------------------------------------------------------------------------
    #Custom Geometry actions
    #------------------------------------------------------------------------------------------------------------------------------------


    def AddCustomGeometry(self, brepCustomGeo, vecPlacement=None, vecScaleFactors=None, vecUpVector=None, blnTilable=None, \
        dblRotation=None, windowDepth=None, trimToPanelSize=None):
        
        if str(type(brepCustomGeo)) <> "<type 'instance'>" and  type(brepCustomGeo) <> ListType: 
            self.__m_warningData.append("Panel '"+self.GetName()+"': Invalid Custom Geometry Object"); return
            
        if brepCustomGeo == None or  brepCustomGeo == []: 
            self.__m_warningData.append("Panel '"+self.GetName()+"': Invalid Custom Geometry Object"); return
        
        #store parameters
        self.__m_CustomGeoBaseData = brepCustomGeo      
        
        if str(type(self.__m_CustomGeoBaseData)) == "<type 'instance'>" : 
            self.__m_CustomGeoBreps = self.__m_CustomGeoBaseData.Run()
            if self.__m_CustomGeoBreps == None : self.__m_CustomGeoBreps = [rg.Brep()]
        else:
            self.__m_CustomGeoBreps = list(brep.DuplicateBrep() for brep in self.__m_CustomGeoBaseData)
        
        if vecPlacement : self.__m_CG_vecPlacement = vecPlacement
        if vecUpVector.IsUnitVector : self.__m_CG_vecUpVector = vecUpVector
        self.__m_CG_blnTilable = blnTilable
        if dblRotation <> None : self.__m_CG_dblRotation = dblRotation
        if windowDepth <> None : self.__m_CG_windowDepth = windowDepth
        if trimToPanelSize <> None: self.__m_CG_trimToPanelSize = trimToPanelSize
        
        #get size data
        tmpGeoBBox = rg.Brep().GetBoundingBox(True)
        for brep in self.__m_CustomGeoBreps:
            tmpGeoBBox.Union(brep.GetBoundingBox(True))
        tmpGeoSize = tmpGeoBBox.Max - tmpGeoBBox.Min
        
        #place custom geometry at coordinates origon 0,0,0 (actually 0.001, 0.001, 0.001 to avoid potential boolean errors)       
        vecTranslate = rg.Vector3d(tmpGeoBBox.Min)
        for brep in self.__m_CustomGeoBreps: 
            brep.Translate(-vecTranslate)
            #brep.Translate(rg.Vector3d(0.001,0.001,0.001))
            
        #rotate based on Z up value
        if self.__m_CG_vecUpVector.X == 1 :
            ptOrigin = rg.Point3d(0,tmpGeoSize.Y,0)
            ptVectorX = rg.Point3d(0,tmpGeoSize.Y-1,0)
            ptVectorY = rg.Point3d(1,tmpGeoSize.Y,0)
        elif self.__m_CG_vecUpVector.X == -1 :
            ptOrigin = rg.Point3d(tmpGeoSize.X,0,0)
            ptVectorX = rg.Point3d(tmpGeoSize.X,1,0)
            ptVectorY = rg.Point3d(tmpGeoSize.X-1,0,0)
        elif self.__m_CG_vecUpVector.Y == 1 :
            ptOrigin = rg.Point3d(0,0,0)
            ptVectorX = rg.Point3d(1,0,0)
            ptVectorY = rg.Point3d(0,1,0)
        elif self.__m_CG_vecUpVector.Y == -1 :
            ptOrigin = rg.Point3d(tmpGeoSize.X, tmpGeoSize.Y,0)
            ptVectorX = rg.Point3d(tmpGeoSize.X-1, tmpGeoSize.Y,0)
            ptVectorY = rg.Point3d(tmpGeoSize.X, tmpGeoSize.Y-1,0)
        elif self.__m_CG_vecUpVector.Z == 1 :
            ptOrigin = rg.Point3d(0, tmpGeoSize.Y, 0)
            ptVectorX = rg.Point3d(1, tmpGeoSize.Y, 0)
            ptVectorY = rg.Point3d(0, tmpGeoSize.Y, 1)
        elif self.__m_CG_vecUpVector.Z == -1 :
            ptOrigin = rg.Point3d(tmpGeoSize.X, tmpGeoSize.Y, tmpGeoSize.Z)
            ptVectorX = rg.Point3d(tmpGeoSize.X-1, tmpGeoSize.Y, tmpGeoSize.Z)
            ptVectorY = rg.Point3d(tmpGeoSize.X, tmpGeoSize.Y, tmpGeoSize.Z-1)
            
        #apply vectorUp orientation
        plFrom = rg.Plane(ptOrigin, ptVectorX, ptVectorY)
        plTo = rg.Plane(rg.Point3d(0,0,0), rg.Point3d(1,0,0), rg.Point3d(0,0,1))
        brepTransform = rg.Transform.PlaneToPlane(plFrom, plTo)
        for brep in self.__m_CustomGeoBreps: brep.Transform(brepTransform)
            
        #scale based on scale factor
        if vecScaleFactors <> rg.Vector3d(1,1,1) : 
            self.__m_CG_vecScaleFactor = vecScaleFactors
            plOrigin = rg.Plane(rg.Point3d(0,0,0), rg.Point3d(1,0,0), rg.Point3d(0,1,0))
            brepTransform = rg.Transform.Scale(plOrigin, self.__m_CG_vecScaleFactor.X, self.__m_CG_vecScaleFactor.Y, self.__m_CG_vecScaleFactor.Z)
            for brep in self.__m_CustomGeoBreps: brep.Transform(brepTransform)
            # flip normals if negative scaling
            flipCG = False
            if self.__m_CG_vecScaleFactor.X < 0 : flipCG = not flipCG
            if self.__m_CG_vecScaleFactor.Y < 0 : flipCG = not flipCG
            if self.__m_CG_vecScaleFactor.Z < 0: flipCG = not flipCG
            if flipCG : 
                for brep in self.__m_CustomGeoBreps: brep.Flip()
            
        #move based on placement data
        if not self.__m_CG_vecPlacement.IsZero:
            for brep in self.__m_CustomGeoBreps: brep.Translate(self.__m_CG_vecPlacement)
        
        #create rotation transformation based on rotation data
        rotXform = rg.Transform.Rotation(math.radians(self.__m_CG_dblRotation), rg.Vector3d(0,1,0), rg.Point3d(self.GetWidth()/2,0,self.GetHeight()/2))
        
        #tile geometry if turned on
        if self.__m_CG_blnTilable:
            #define tiling base area
            tileAreaWidth = self.GetWidth()
            tileAreaHeight = self.GetHeight()
            tolerance = sc.doc.ModelAbsoluteTolerance
            #recalculate required area to tile based on customGeo rotation
            if self.__m_CG_dblRotation <> 0:
                tilePlane = rg.Plane(rg.Point3d(0,0,0), rg.Point3d(1,0,0), rg.Point3d(0,0,1))
                tileAreaBox =  rg.Box(tilePlane, [rg.Point3d(0,0,0), rg.Point3d(self.GetWidth(),0,0),rg.Point3d(0,0,self.GetHeight())]) 
                tileAreaBox.Transform(rotXform)      
                tileAreaBBox = tileAreaBox.BoundingBox
                tileAreaSize = tileAreaBBox.Max - tileAreaBBox.Min
                tileAreaWidth = tileAreaSize.X
                tileAreaHeight = tileAreaSize.Z
            tmpGeoBBox = rg.Brep().GetBoundingBox(True)
            for brep in self.__m_CustomGeoBreps:
                tmpGeoBBox.Union(brep.GetBoundingBox(True))
            tmpGeoSize = tmpGeoBBox.Max - tmpGeoBBox.Min
            #process tiling for each brep in list
            tmpCustomGeoBreps = []
            for index, brep in enumerate(self.__m_CustomGeoBreps):
                #move geometry to the left if not at origin
                xPos = round(tmpGeoBBox.Min.X, 3); xStep = round(tmpGeoSize.X, 3)
                vecWidth = rg.Vector3d(-xStep,0,0)            
                while xPos > 0 :
                    brep.Translate(vecWidth)
                    xPos -= xStep
                #move geometry to the bottom if not at origin
                zPos = round(tmpGeoBBox.Min.Z, 3); zStep = round(tmpGeoSize.Z, 3)
                vecHeight = rg.Vector3d(0, 0, -zStep)
                while zPos > 0 :
                    brep.Translate(vecHeight)
                    zPos -= zStep
                #create array of breps to cover panel
                tmpGeoList = []
                xTrans = 0; zTrans = 0
                while True:
                    while xPos < tileAreaWidth:        
                        tmpGeo = brep.DuplicateBrep()
                        vecWidth = rg.Vector3d(xTrans,0,zTrans)                    
                        tmpGeo.Translate(vecWidth)
                        tmpGeoList.append(tmpGeo)
                        xPos += xStep ; xTrans += xStep
                    zPos += zStep ; zTrans += zStep
                    if zPos < tileAreaHeight: xPos -= xTrans; xTrans =0     
                    else: break
                tmpCustomGeoBreps += tmpGeoList
                
            self.__m_CustomGeoBreps = tmpCustomGeoBreps
            # relocate tiles brep to right location before rotation
            if self.__m_CG_dblRotation <> 0: 
                for brep in self.__m_CustomGeoBreps: brep.Translate(tileAreaBBox.Min.X, 0, tileAreaBBox.Min.Z)
                
        # perform rotation on final brep
        if self.__m_CG_dblRotation <> 0: 
            for brep in self.__m_CustomGeoBreps: brep.Transform(rotXform)
        
        self.__m_blnShowCustomGeo = True
        
        
        
    def ModifyCustomGeometry(self, brepCustomGeo=None, vecPlacement=None,placementX=None, placementY=None,placementZ=None,\
        vecScaleFactors=None, scaleX=None, scaleY=None, scaleZ=None, vecUpVector=None, upVectorX=None, upVectorY=None, upVectorZ=None,\
        blnTilable=None, rotation=None, windowDepth=None, dynamicGeoParams=None, trimToPanelSize = None):
        
        if brepCustomGeo == None : brepCustomGeo = self.__m_CustomGeoBaseData
        
        #set dynamic geometry parameters if available
        if dynamicGeoParams <> None and str(type(self.__m_CustomGeoBaseData)) == "<type 'instance'>" : 
            if type(dynamicGeoParams) == ListType:
                
                for param, value in dynamicGeoParams: self.__m_CustomGeoBaseData.SetParameter(param, value)
            else: self.__m_CustomGeoBaseData.SetParameter(dynamicGeoParams)
        
        if vecPlacement == None : 
            vecPlacement = self.__m_CG_vecPlacement
            if placementX <> None : vecPlacement.X = placementX
            if placementY <> None : vecPlacement.Y = placementY
            if placementZ <> None : vecPlacement.Z = placementZ
        
        if vecScaleFactors == None : 
            vecScaleFactors = self.__m_CG_vecScaleFactor
            if scaleX <> None : vecScaleFactors.X = scaleX
            if scaleY <> None : vecScaleFactors.Y = scaleY
            if scaleZ <> None : vecScaleFactors.Z = scaleZ
        
        if vecUpVector == None : 
            vecUpVector = self.__m_CG_vecUpVector
            if upVectorX <> None : vecUpVector.X = upVectorX
            if upVectorY <> None : vecUpVector.Y = upVectorY
            if upVectorZ <> None : vecUpVector.Z = upVectorZ
            
        #if vecScaleFactors == None : vecScaleFactors = self.__m_CG_vecScaleFactor
        if vecUpVector == None : vecUpVector = self.__m_CG_vecUpVector      
        if blnTilable == None : blnTilable = self.__m_CG_blnTilable
        if rotation == None : rotation = self.__m_CG_dblRotation
        if windowDepth == None : windowDepth = self.__m_CG_windowDepth
        if trimToPanelSize == None : trimToPanelSize = self.__m_CG_trimToPanelSize

        self.AddCustomGeometry(brepCustomGeo, vecPlacement, vecScaleFactors, vecUpVector, blnTilable, rotation, windowDepth, trimToPanelSize)
        
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

        if self.__m_arrMullionHorObjects and not type(self.__m_arrMullionHorObjects[0]) == IntType and rs.IsObject(self.__m_arrMullionHorObjects[0]):
            rs.DeleteObjects(self.__m_arrMullionHorObjects)

        
        if self.__m_arrMullionVertObjects and not type(self.__m_arrMullionVertObjects[0]) == IntType and rs.IsObject(self.__m_arrMullionVertObjects[0]):
            rs.DeleteObjects(self.__m_arrMullionVertObjects)

            
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
        
        
    def HideCustomGeometry(self):
        #Delete Shadnig if Exists.
        if self.__m_CustomGeoObjects and len(self.__m_CustomGeoObjects) > 0 and rs.IsObject(self.__m_CustomGeoObjects[0]) : \
            rs.DeleteObjects(self.__m_CustomGeoObjects)
            
        self.__m_CustomGeoObjects  = []
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

    def Draw(self, sceneObjects = False):
        
        if self.__m_blnShowWall : self.DrawWall()
        
        if self.__m_blnShowWindow : self.DrawWindow()
        
        if self.__m_blnShowPane : self.DrawPane()
        
        if self.__m_blnShowMullions : self.DrawMullions()
        
        if self.__m_blnShowShading : self.DrawShading()
        
        if self.__m_blnShowCustomGeo : self.DrawCustomGeometry()
        
        if self.__m_blnShowDeform : self.DrawMorph()
        
        if sceneObjects : self.DrawSceneObjects()
            
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
    def DrawWall(self):
        
        
        #Ignore draw wall if window is as large as panel
        if self.__GetPanelProperty("WindowVisibility") and self.GetWidth() <= self.__GetPanelProperty("WindowWidth") and \
            self.GetHeight() <= self.__GetPanelProperty("WindowHeight"):
            return 
        
        if self.GetDrawMode() == "LADYBUG" : #Wall as single sided in Ladybug draw mode
            cornerPt1 = rg.Point3d(0,0,0)
            cornerPt2 = rg.Point3d(self.__m_dblWidth,0,0)
            cornerPt3 = rg.Point3d(self.__m_dblWidth, 0, self.__m_dblHeight)
            cornerPt4 = rg.Point3d(0, 0, self.__m_dblHeight)
            self.__m_arrWallBreps[0] = rg.Brep.CreateFromCornerPoints(cornerPt1, cornerPt2, cornerPt3, cornerPt4, sc.doc.ModelAbsoluteTolerance)
            
        else: #DEFAULT MODE 
            #create opposite corner points for box and wall Geometry
            cornerPt1 = rg.Point3d(0,0,0)
            cornerPt2 = rg.Point3d(self.__m_dblWidth, self.__m_dblWallThickness, self.__m_dblHeight)   
            self.__m_arrWallBreps[0] = rg.Brep.CreateFromBox(rg.BoundingBox(cornerPt1, cornerPt2))
            
        self.__m_blnShowWall = True
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    
    def DrawPane(self):
        
            
        #Ignore draw pane if window is as large as panel
        if self.__GetPanelProperty("WindowVisibility") and self.GetWidth() <= self.__GetPanelProperty("WindowWidth") and \
            self.GetHeight() <= self.__GetPanelProperty("WindowHeight"):
            return 
            
        if self.GetDrawMode() == "LADYBUG" : return   #pane excluded from Ladybug draw mode
        
        GlsSurface = 0          # Surface of Subtracting Object
        CoverSurface = 0        # Surface of Wall Cover 
        strExtrCurve = 0        #: Path is used to Extude, Length of line is equal to Thickness of Wall Cover
        strExtrCurve2 = 0       #: Path is used to Extude Surface of Subtracting Object, Length of line is equal to Thickness of Wall Cover+ Distance between Wall Cover and wall
        OpeningObject = 0
        arrPaneObjects = []
        
        
        #set up pane overal dimensions
        
        if type(self.__m_dblPaneOffsetEdge)==ListType :                 #if a list was provided
            paneOffset = self.__m_dblPaneOffsetEdge     
            for i in range(len(paneOffset),4): paneOffset.append(0)         #complete with ceros if less than 4 values.
        else:  #else repeat 4 times the number
            paneOffset = [self.__m_dblPaneOffsetEdge, self.__m_dblPaneOffsetEdge, self.__m_dblPaneOffsetEdge, self.__m_dblPaneOffsetEdge]

        #Create pane base object
        rcTolerance = sc.doc.ModelAbsoluteTolerance
        pt1 = [paneOffset[0], 0, paneOffset[1]]
        pt2 = [self.__m_dblWidth-paneOffset[2], 0, paneOffset[1]]
        pt3 = [self.__m_dblWidth-paneOffset[2], 0, self.__m_dblHeight-paneOffset[3]]
        pt4 = [paneOffset[0], 0, self.__m_dblHeight-paneOffset[3]]
        CoverSurface = rg.Brep.CreateFromCornerPoints(rg.Point3d(pt1[0],pt1[1],pt1[2]), rg.Point3d(pt2[0],pt2[1],pt2[2]),\
            rg.Point3d(pt3[0],pt3[1],pt3[2]), rg.Point3d(pt4[0],pt4[1],pt4[2]), rcTolerance)
        self.__m_arrPaneBreps[0] = CoverSurface.Faces.Item[0].CreateExtrusion(\
            rg.LineCurve(rg.Point3d(0,0,0), rg.Point3d(0, self.__m_dblPaneThickness, 0)), True)

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
                    if member : self.__m_arrPaneBreps.append(member)
                    x += xStep
                z += zStep
                
        #Move to place(front of wall)
        #rs.MoveObjects(self.__m_arrPaneObjects, [0, -1 * self.__m_dblPaneOffset, 0]) # Move Objects Forward in front of the Wall
        for obj in self.__m_arrPaneBreps: obj.Translate(0, -1 * self.__m_dblPaneOffset, 0)
        
        
        #Create Opening
        if self.__m_blnShowWindow :                #: If Window exists we need to subtract Window from panel base and tiles.
            arrOpeningPoints = copy.deepcopy(self.__m_arrWindowPoints)

            #Avoid boolean error when subraction boxes align with panel edges
            if round(self.__GetPanelProperty("WindowLeft"),3) == 0 : arrOpeningPoints[0][0] = arrOpeningPoints[3][0] = -.1*self.__m_unitCoef
            if round(self.__GetPanelProperty("WindowRight"),3) == 0 : arrOpeningPoints[1][0] = arrOpeningPoints[2][0] = self.GetWidth()+.1*self.__m_unitCoef
            if round(self.__GetPanelProperty("WindowBottom"),3) == 0 : arrOpeningPoints[0][2] = arrOpeningPoints[1][2] = -.1*self.__m_unitCoef 
            if round(self.__GetPanelProperty("WindowTop"),3) == 0 : arrOpeningPoints[2][2] = arrOpeningPoints[3][2] = self.GetHeight()+.1*self.__m_unitCoef
            

            pt1, pt2, pt3, pt4 = arrOpeningPoints
            GlsSurface = rg.Brep.CreateFromCornerPoints(rg.Point3d(pt1[0],pt1[1],pt1[2]), rg.Point3d(pt2[0],pt2[1],pt2[2]),\
                rg.Point3d(pt3[0],pt3[1],pt3[2]), rg.Point3d(pt4[0],pt4[1],pt4[2]), rcTolerance)
            OpeningObject = GlsSurface.Faces.Item[0].CreateExtrusion(\
                rg.LineCurve(rg.Point3d(0,0,0), rg.Point3d(0, 4*self.__m_unitCoef, 0)), True)
            OpeningObject.Translate(0,-2*self.__m_unitCoef,0)
            
            arrPaneObjects = self.__m_arrPaneBreps
            self.__m_arrPaneBreps = []
            for index, obj in enumerate(arrPaneObjects):
                if OpeningObject.GetBoundingBox(True).Contains(obj.GetBoundingBox(True), False) :
                    continue
                #boolean only works on large pane object(first item), use split on tiles
                if  index == 0 : 
                    boolResult = list(rg.Brep.CreateBooleanDifference(obj, OpeningObject, rcTolerance))
                else:    
                    boolResult = list(rg.Brep.Split(obj, OpeningObject , rcTolerance))
                
                if not len(boolResult) :self.__m_arrPaneBreps += [obj]
                
                for piece in boolResult : 
                    bbox = OpeningObject.GetBoundingBox(True)
                    bbox.Inflate(.02*self.__m_unitCoef)
                    if bbox.Contains(piece.GetBoundingBox(True), False): continue
                    if index > 0 : piece.Flip() #flip boolean result of pane tiles (bug)
                    self.__m_arrPaneBreps += [piece]
                
        self.__m_blnShowPane = True
        
    
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    
    def DrawWindow(self):
        
        GlsSurface = 0                #:Surface of Glass
        strExtrCurve = 0              #:Path used to Extrude Subtracting Object, Lenght equal to Wall Depth
        GlassObjectTemp = 0
        wallObjectTemp = 0 #bollean window operation result
        
        #Create Window Panel
        rcTolerance = sc.doc.ModelAbsoluteTolerance
        pt1, pt2, pt3, pt4 = self.__m_arrWindowPoints
        GlsSurface = rg.Brep.CreateFromCornerPoints(rg.Point3d(pt1[0],pt1[1],pt1[2]), rg.Point3d(pt2[0],pt2[1],pt2[2]),\
            rg.Point3d(pt3[0],pt3[1],pt3[2]), rg.Point3d(pt4[0],pt4[1],pt4[2]), rcTolerance)
        
        if self.GetDrawMode() == "LADYBUG" and self.__m_dblWinGlassThickness > 0:
            self.__m_arrWindowBreps[0] = GlsSurface #in LADYBUG mode only glass pane is drawn
            #Move to place
            self.__m_arrWindowBreps[0].Translate(0, -self.__m_dblWinGlassOffset, 0)
            self.__m_blnShowWindow = True
            if self.__m_blnShowWall and self.__m_arrWallBreps <> [0]:
                tmpObject = rg.Brep.CreateBooleanDifference(self.__m_arrWallBreps[0], GlsSurface, rcTolerance)
                if tmpObject : self.__m_arrWallBreps = tmpObject
                
            return
            
        if self.__m_dblWinGlassThickness > 0 : #create glass pane if thickness > 0 otherwise just create opening
            self.__m_arrWindowBreps[0]= GlsSurface.Faces.Item[0].CreateExtrusion(\
                rg.LineCurve(rg.Point3d(0,0,0), rg.Point3d(0, self.__m_dblWinGlassThickness, 0)), True)
            #Move to place
            self.__m_arrWindowBreps[0].Translate(0, -self.__m_dblWinGlassOffset, 0)

            
        #Create Opening if wall is visible
        if self.__m_blnShowWall and self.__m_arrWallBreps <> [0]:

            GlassObjectTemp = GlsSurface.Faces.Item[0].CreateExtrusion(\
                rg.LineCurve(rg.Point3d(0,0,0), rg.Point3d(0, self.__m_dblWallThickness, 0)), True)
            wallObjectTemp = self.__m_arrWallBreps[0]
            wallBreps = rg.Brep.CreateBooleanDifference(wallObjectTemp, GlassObjectTemp, rcTolerance)
            if wallBreps : self.__m_arrWallBreps = list(wallBreps)
            else: self.__m_arrWallBreps = [0]

        self.__m_blnShowWindow = True
        
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
        
    def DrawMullions(self):
        
            
        self.__m_arrMullionHorBreps = []
        self.__m_arrMullionVertBreps = []
            
        #Populate array with new mullions based on Mullion Data array
        #Horizontal
        if len(self.__m_arrMullionHorUserData[0]) :
            for i in range(len(self.__m_arrMullionHorUserData[0])) :
                mullionObjList = self.DrawMullionType(self.__m_arrMullionHorUserData[0][i], self.__m_arrMullionHorUserData[1][i], self.__m_arrMullionHorUserData[2][i],\
                    self.__m_arrMullionHorUserData[3][i], self.__m_arrMullionHorUserData[4][i])
                if type(mullionObjList) == ListType and mullionObjList[0]: 
                    self.__m_arrMullionHorBreps.append(mullionObjList)

                
        #Vertical
        if len(self.__m_arrMullionVertUserData[0])  :
            for i in range(len(self.__m_arrMullionVertUserData[0])):
                mullionObjList = self.DrawMullionType(self.__m_arrMullionVertUserData[0][i], self.__m_arrMullionVertUserData[1][i], self.__m_arrMullionVertUserData[2][i],\
                    self.__m_arrMullionVertUserData[3][i], self.__m_arrMullionVertUserData[4][i])
                if type(mullionObjList) == ListType and mullionObjList[0]: 
                    self.__m_arrMullionVertBreps.append(mullionObjList)
                    
        if not self.__m_arrMullionHorBreps : self.__m_arrMullionHorBreps = [0]
        if not self.__m_arrMullionVertBreps : self.__m_arrMullionVertBreps = [0]
        
        
    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    #    Mullion/Cap creation data based on their type 
    
    def DrawMullionType(self, strMullionType, dblWidth, dblThickness, dblCapWidth, dblCapThickness):
        
        if dblThickness == 0 or dblWidth == 0 : return None
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
                if (type(dblThickness) == ListType and len(dblThickness) > 1) or (type(dblCapThickness) == ListType and len(dblCapThickness) > 1):
                    #3-piece mullions if curtain-wall with opening
                    arrHorPoints = [[0, 0, 0], [self.__m_arrWindowPoints[0][0], 0, 0],[self.__m_arrWindowPoints[1][0], 0, 0], [self.__m_dblWidth, 0, 0]]  
                    arrVertPoints = [[0, 0, 0], [0, 0, self.__m_arrWindowPoints[0][2]],[0, 0, self.__m_arrWindowPoints[2][2]], [0, 0, self.__m_dblHeight]]
                else: #if one list item will be used for Window frame only    
                    bWindowFrame = True
            #if full window panel? (no pane object) also use window frame settings
            if not self.__m_arrPaneBreps or self.__m_arrPaneBreps == [0] :
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
            self.__m_warningData.append("Wrong mullion type" + strMullionType)
            return
    
        arrXform = rs.XformTranslation(arrDeltaPoint) # create matrix from vector to add delta(distance) to base points in one line
        arrMullionPoints = rs.PointArrayTransform(arrMullionPoints, arrXform) # add delta(distance) to base mullions to get final 4 points locations
        
        
        #Create 1 or 3 mullions using the obtained points sending them in pairs (end points of each mullion)

        for i in range(len(arrMullionPoints)-1) :
            
            if rs.PointCompare(arrMullionPoints[i], arrMullionPoints[i + 1]) :
                continue #skip if points on same location
            
            #detect if thickness is one value or three(varying thinkness along mullion)
            if type(dblThickness) is ListType and len(dblThickness)> i: mullThickness = dblThickness[i]
            else : mullThickness = dblThickness
            
            if mullThickness > 0 and self.GetDrawMode() <> "LADYBUG" : 
                
                arrMullions.append(self.DrawMember(arrMullionPoints[i], arrMullionPoints[i + 1], dblWidth, mullThickness))

            #else:
                #arrMullions.append(rs.AddPoint(self.__m_arrBoundingBox[0])) #just a point as placeholder at Panel origin
            
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
        
        
        if arrMullions == [] : arrMullions = None       
        #return the array of mullions back to function call
        return arrMullions
        
        
    #------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    
    #Member creation using start/end, width, thickness parameters
    
    def DrawMember(self, arrStartPoint, arrEndPoint, dblWidth, dblThickness, dblRotation=0, arrOffsetStart=None, arrOffsetEnd=None) :

        if rs.PointCompare(arrStartPoint, arrEndPoint) : return #return if same points start,end
        
        
        #To create 4 surface points based on 2 points a vertical or horizontal offset need to be defined
        #depending on member type:horizontal or verical
        if arrStartPoint[0] == arrEndPoint[0] :     #Is Vertical?
            cornerPt1 = rg.Point3d(arrStartPoint[0]-dblWidth/2, arrStartPoint[1]+dblThickness, arrStartPoint[2])
            cornerPt2 = rg.Point3d(cornerPt1[0], arrStartPoint[1], cornerPt1[2])
            cornerPt3 = rg.Point3d(cornerPt2[0], cornerPt2[1], arrEndPoint[2])
            cornerPt4 = rg.Point3d(cornerPt1[0], cornerPt1[1], cornerPt3[2])
            
            ptExtrusion = rg.Point3d(dblWidth,0,0)
            vecRot = rg.Vector3d(0,0,1) #for rotation
            
        elif arrStartPoint[2] == arrEndPoint[2] :   #Is Horizontal?
            cornerPt1 = rg.Point3d(arrStartPoint[0], arrStartPoint[1]+dblThickness, arrStartPoint[2]-dblWidth/2)
            cornerPt2 = rg.Point3d(cornerPt1[0], arrStartPoint[1], cornerPt1[2])
            cornerPt3 = rg.Point3d(arrEndPoint[0], cornerPt2[1], cornerPt2[2])
            cornerPt4 = rg.Point3d(cornerPt3[0], cornerPt1[1], cornerPt3[2])
            
            ptExtrusion = rg.Point3d(0,0,dblWidth)
            vecRot = rg.Vector3d(1,0,0) #for rotation
        else:
            return
        
        #apply offset values on outside points of object.
        if arrOffsetStart : 
            cornerPt2 = cornerPt2 + rg.Point3d(arrOffsetStart[0], arrOffsetStart[1], arrOffsetStart[2] )
        if arrOffsetEnd :
            cornerPt3 = cornerPt3 + rg.Point3d(arrOffsetEnd[0], arrOffsetEnd[1], arrOffsetEnd[2] )     
        
        rcTolerance = sc.doc.ModelAbsoluteTolerance
        #create ocorner points for surface
        brepMember = rg.Brep.CreateFromCornerPoints(cornerPt1 ,cornerPt2, cornerPt3, cornerPt4, rcTolerance)
        brepMember = brepMember.Faces.Item[0].CreateExtrusion(rg.LineCurve(rg.Point3d(0,0,0), ptExtrusion), True)    
        
        if dblRotation <> 0 : 
            ptCenter = rg.Point3d(arrStartPoint[0],arrStartPoint[1]+dblThickness/2,arrStartPoint[2])            
            brepMember.Rotate(math.radians(dblRotation), vecRot, ptCenter)
            
        return brepMember
        
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def DrawShading(self):

        
        self.__m_arrShadingBreps = []

        #Populate array with new shadine elements based on Data array
        if len(self.__m_arrShadingUserData[0]) :
            self.__m_arrShadingBreps = []
            for i in range(len(self.__m_arrShadingUserData[0])) :
                tmpShadingObjects = self.DrawShadingType(self.__m_arrShadingUserData[0][i], self.__m_arrShadingUserData[1][i], self.__m_arrShadingUserData[2][i],\
                    self.__m_arrShadingUserData[3][i], self.__m_arrShadingUserData[4][i], self.__m_arrShadingUserData[5][i], self.__m_arrShadingUserData[6][i],\
                    self.__m_arrShadingUserData[7][i], self.__m_arrShadingUserData[9][i])
                if tmpShadingObjects <> None : self.__m_arrShadingBreps.append(tmpShadingObjects)
        if not self.__m_arrShadingBreps or self.__m_arrShadingBreps[0] == None : self.__m_arrShadingBreps = [0]
        
        
    def DrawShadingType(self,  strShadingType, fromLeftBottomCorner, fromRightTop, width=.05*_UNIT_COEF, thickness=0.05*_UNIT_COEF, offset=0, spacing=.1*_UNIT_COEF, rotation=0, shiftEnds=[None,None]):
        
        if thickness <= 0 or width <= 0 : return
        
        #----Setting up parameters common to all shading types
        start = [0,0,0]; end = [0,0,0]
        start[1] = -offset-thickness; end[1] = -offset-thickness
        tmpFromLeftBottomCorner = copy.deepcopy(fromLeftBottomCorner)
        tmpFromRightTop = copy.deepcopy(fromRightTop)
        #----Setting up parameters based on shading type
        #Single Shade options:
        if strShadingType in ["HorizontalShade", "HorizontalWindowShade"]:  #---Single Vertical Shade
            if strShadingType == "HorizontalWindowShade":
                if self.__m_blnShowWindow : 
                    # - negative value defines distance from window head 
                    if tmpFromLeftBottomCorner[1] < 0 :  tmpFromLeftBottomCorner[1] = self.__GetPanelProperty("WindowHeight") + tmpFromLeftBottomCorner[1]
                    if tmpFromLeftBottomCorner[0] < 0 :  tmpFromLeftBottomCorner[0] = self.__GetPanelProperty("WindowWidth") + tmpFromLeftBottomCorner[0]
                    # add values to remap distances from window lower left corner
                    tmpFromLeftBottomCorner[0] += self.__GetPanelProperty("WindowLeft")
                    tmpFromLeftBottomCorner[1] += self.__GetPanelProperty("WindowBottom")
                    tmpFromRightTop  += self.__GetPanelProperty("WindowRight")
                else: return
            start[0] = tmpFromLeftBottomCorner[0]; start[2] = tmpFromLeftBottomCorner[1]
            end[0] = self.__GetPanelProperty("PanelWidth")-tmpFromRightTop
            end[2] = tmpFromLeftBottomCorner[1]
            if start[0] >= end[0] or start[0] < 0 or start[0] > self.GetWidth()*self.__m_dimRoundCoef or start[2] < 0 or start[2] > self.GetHeight()*self.__m_dimRoundCoef:
                self.__m_warningData.append("Invalid "+ strShadingType + " data"); return None #check for wrong data
            if  rotation <> 0 : #adjust start-end points of shade to offset rotation from center of sunshade to side closer to panel.
                start[2] -= math.sin(math.radians(rotation))*thickness/2
                end[2] -= math.sin(math.radians(rotation))*thickness/2
                start[1] += thickness/2 - math.cos(math.radians(rotation))*thickness/2
                end[1] += thickness/2 - math.cos(math.radians(rotation))*thickness/2
            return [self.DrawMember(start, end, width, thickness, rotation, shiftEnds[0], shiftEnds[1])]
            
        elif strShadingType in ["VerticalShade", "VerticalWindowShade"]: #---Single Horizontal Shade
            if strShadingType == "VerticalWindowShade":
                if self.__m_blnShowWindow:
                   # - negative value defines distance from window head and right jamb
                    if tmpFromLeftBottomCorner[1] < 0 :  tmpFromLeftBottomCorner[1] = self.__GetPanelProperty("WindowHeight") + tmpFromLeftBottomCorner[1]
                    if tmpFromLeftBottomCorner[0] < 0 :  tmpFromLeftBottomCorner[0] = self.__GetPanelProperty("WindowWidth") + tmpFromLeftBottomCorner[0]
                    # add values to remap distances from window lwer left corner
                    tmpFromLeftBottomCorner[0] += self.__GetPanelProperty("WindowLeft")
                    tmpFromLeftBottomCorner[1] += self.__GetPanelProperty("WindowBottom")
                    tmpFromRightTop  += self.__GetPanelProperty("WindowTop")
                else: return               
            start[0] = tmpFromLeftBottomCorner[0]; start[2] = tmpFromLeftBottomCorner[1]
            end[0] = tmpFromLeftBottomCorner[0]
            end[2] = self.__GetPanelProperty("PanelHeight")-tmpFromRightTop
            if start[2] >= end[2] or start[0] < 0 or start[0] > self.GetWidth()*self.__m_dimRoundCoef or start[2] < 0 or start[2] > self.GetHeight()*self.__m_dimRoundCoef:
                self.__m_warningData.append("Invalid "+ strShadingType + " data"); return None #check for wrong data
            if  rotation <> 0 : #adjust start-end points of shade to offset rotation from center of sunshade to side closer to panel.
                start[0] += math.sin(math.radians(rotation))*thickness/2
                end[0] += math.sin(math.radians(rotation))*thickness/2
                start[1] += thickness/2 - math.cos(math.radians(rotation))*thickness/2
                end[1] += thickness/2 - math.cos(math.radians(rotation))*thickness/2
            return [self.DrawMember(start, end, width, thickness, rotation, shiftEnds[0], shiftEnds[1])]
            
        #Louver type options:
        elif strShadingType in ["HorizontalLouver", "HorizontalWindowLouver"] : #---VerticalLouvers
            if strShadingType == "HorizontalWindowLouver":
                if self.__m_blnShowWindow : 
                    tmpFromLeftBottomCorner[0] += self.__GetPanelProperty("WindowLeft")
                    tmpFromLeftBottomCorner[1] += self.__GetPanelProperty("WindowBottom")
                    tmpFromRightTop[0]  += self.__GetPanelProperty("WindowRight")
                    tmpFromRightTop[1]  += self.__GetPanelProperty("WindowTop")
                else: return
            start[0] = tmpFromLeftBottomCorner[0]; start[2] = tmpFromLeftBottomCorner[1]        
            end[0] = self.__GetPanelProperty("PanelWidth")-tmpFromRightTop[0]
            valZ = start[2]
            endZ = self.__GetPanelProperty("PanelHeight")-tmpFromRightTop[1]
            if start[0] >= end[0] or start[2] < 0 or start[2] > self.GetHeight()*self.__m_dimRoundCoef: return None #check for wrong data
            arrLouvers = []
            #adjust start-end points of shade to offset rotation from center of sunshade to side closer to panel.
            offsetZ = 0; offsetY = 0
            if  rotation <> 0 : 
                offsetZ = math.sin(math.radians(rotation))*thickness/2
                offsetY = thickness/2 - math.cos(math.radians(rotation))*thickness/2
                start[1] += offsetY; end[1] += offsetY
            while valZ <= endZ :
                start[2] = end[2] = valZ - offsetZ
                arrLouvers.append(self.DrawMember(start, end, width, thickness, rotation, shiftEnds[0], shiftEnds[1]))
                valZ += spacing
            return arrLouvers
            
        if strShadingType in ["VerticalLouver", "VerticalWindowLouver" ]: #---Horizontal Louvers
            if strShadingType == "VerticalWindowLouver":
                if self.__m_blnShowWindow:
                    tmpFromLeftBottomCorner[0] += self.__GetPanelProperty("WindowLeft")
                    tmpFromLeftBottomCorner[1] += self.__GetPanelProperty("WindowBottom")
                    tmpFromRightTop[0]  += self.__GetPanelProperty("WindowRight")
                    tmpFromRightTop[1]  += self.__GetPanelProperty("WindowTop")
                else: return               
            start[0] = tmpFromLeftBottomCorner[0]; start[2] = tmpFromLeftBottomCorner[1]        
            end[2] = self.__GetPanelProperty("PanelHeight")-tmpFromRightTop[1]
            valX = start[0]
            endX = self.__GetPanelProperty("PanelWidth")-tmpFromRightTop[0]
            if start[2] >= end[2] or start[0] < 0 or start[0] > self.GetWidth()*self.__m_dimRoundCoef: return None #check for wrong data
            arrLouvers = []
            #adjust start-end points of shade to offset rotation from center of sunshade to side closer to panel.
            offsetX = 0; offsetY = 0
            if  rotation <> 0 : 
                offsetX = math.sin(math.radians(rotation))*thickness/2
                offsetY = thickness/2 - math.cos(math.radians(rotation))*thickness/2
                start[1] += offsetY; end[1] += offsetY
            
            while valX <= endX :
                start[0] = end[0] = valX+offsetX
                arrLouvers.append(self.DrawMember(start, end, width, thickness, rotation, shiftEnds[0], shiftEnds[1]))
                valX += spacing
            return arrLouvers
            
        else: self.__m_warningData.append("Incorrect louver type: " + strShadingType) ; return
        
        
        
        
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def DrawCustomGeometry(self):


        if self.__m_CustomGeoBreps == None or self.__m_CustomGeoBreps == [] : return
        tolerance = sc.doc.ModelAbsoluteTolerance
        self.__m_CustomGeoDrawBreps = []
  
        for brep in self.__m_CustomGeoBreps:
            tmpCustomGeo = brep.DuplicateBrep()
            customGeoBBox = tmpCustomGeo.GetBoundingBox(True)
            customGeoMin = customGeoBBox.Min
            customGeoMax = customGeoBBox.Max
            customGeoSize = customGeoMax - customGeoMin
            
            # if Trim enabled, trim Custom Geometry to match panel size if extends beyond  
            if self.__m_CG_trimToPanelSize:
                if round(customGeoMin.X, 3) < 0 or round(customGeoMax.X, 3) > self.GetWidth() or \
                    round(customGeoMin.Y, 3) < 0 or round(customGeoMax.Y, 3) > self.GetHeight():
                    #create substraction object and subract
                    pt1 = rg.Point3d(0,-customGeoSize.Y*self.__m_CG_vecScaleFactor.Y+self.__m_CG_vecPlacement.Y-2,0)
                    pt2 = rg.Point3d(self.GetWidth(), self.__m_CG_vecPlacement.Y+1, self.GetHeight())
                    tmpBBox = rg.BoundingBox(pt1, pt2)
                    tmpBoxBrep = rg.Brep.CreateFromBox(tmpBBox)
                    tmpBrepList = rg.Brep.CreateBooleanIntersection(tmpCustomGeo, tmpBoxBrep, tolerance)
                    
                    if tmpBrepList == None : self.__m_warningData.append("Panel '"+self.GetName()+"': Panel sizing boolean Error - discarding custom geometry") ; return
                    
                    for index in range(len(tmpBrepList)-1):
                        tmpBrepList[0].Append(tmpBrepList[index+1])
                    if tmpBrepList : tmpCustomGeo = tmpBrepList[0]
                    else: tmpCustomGeo = None
                
            # if window exists and Window Void enabled subtract window from custom geometry
            if self.__m_CG_windowDepth and tmpCustomGeo and self.__m_blnShowWindow:
                arrOpeningPoints = copy.deepcopy(self.__m_arrWindowPoints)
    
                #Avoid boolean error when subraction boxes align with panel edges
                if round(self.__GetPanelProperty("WindowLeft"),3) == 0 : arrOpeningPoints[0][0] = arrOpeningPoints[3][0] = -.1 
                if round(self.__GetPanelProperty("WindowRight"),3) == 0 : arrOpeningPoints[1][0] = arrOpeningPoints[2][0] = self.GetWidth()+.1 
                if round(self.__GetPanelProperty("WindowBottom"),3) == 0 : arrOpeningPoints[0][2] = arrOpeningPoints[1][2] = -.1 
                if round(self.__GetPanelProperty("WindowTop"),3) == 0 : arrOpeningPoints[2][2] = arrOpeningPoints[3][2] = self.GetHeight()+.1
              
                #create subraction object
                voidDepth = 0
                if self.__m_CG_windowDepth == "True" : voidDepth = -customGeoSize.Y * self.__m_CG_vecScaleFactor.Y + self.__m_CG_vecPlacement.Y
                else : voidDepth = -self.__m_CG_windowDepth+self.__m_CG_vecPlacement.Y
                pt1 = rg.Point3d(arrOpeningPoints[0][0], voidDepth - self.__m_dblWinGlassOffset, arrOpeningPoints[0][2])
                pt2 = rg.Point3d(arrOpeningPoints[2][0], self.__m_CG_vecPlacement.Y-self.__m_dblWinGlassOffset, arrOpeningPoints[2][2])
                tmpWinBox = rg.BoundingBox(pt1, pt2)
    
                #check if both window and custom geometry overlap before creating opening
                tmpGeoBBox = tmpCustomGeo.GetBoundingBox(True)
                if tmpGeoBBox.Min.X < tmpWinBox.Max.X and tmpGeoBBox.Min.Z < tmpWinBox.Max.Z: 
                    tmpWinBoxBrep = rg.Brep.CreateFromBox(tmpWinBox)
                    tmpBrepList = rg.Brep.CreateBooleanDifference(tmpCustomGeo, tmpWinBoxBrep, tolerance)
                    #unify pieces in one brep
                    if tmpBrepList <> None : 
                        for index in range(len(tmpBrepList)-1):
                            tmpBrepList[0].Append(tmpBrepList[index+1])
                        if tmpBrepList : tmpCustomGeo = tmpBrepList[0] 
                    else : 
                        self.__m_warningData.append("Panel '"+self.GetName()+"': Window Boolean error - discarding boolean")
                
            if tmpCustomGeo : self.__m_CustomGeoDrawBreps.append(tmpCustomGeo)
        
        #if in Ladybug draw mode check if custom geometry projection off facade is les than Ladybug shading threshhold 
        if self.GetDrawMode() == "LADYBUG" :
            bbox = rg.BoundingBox.Empty
            for  brep in self.__m_CustomGeoDrawBreps:
                bbox.Union(brep.GetBoundingBox(True))
                if bbox.Max.Y-bbox.Min.Y < self.__m_LadybugShadeThresh: 
                    self.__m_CustomGeoDrawBreps = []
                    return
    
    #----------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------
    def DrawMorph(self):
        
        panelBrepList = self.GetBreps()
        self.BoxMorphObject(panelBrepList)
        
        #Store deform box as new panel bounding box
        self.__m_arrBoundingBox = self.__m_arrDeformBox
        
        
    #Work around Phyton not implementing yet morphing func(BoxMorphObject) used in DrawMorph()------------------------------------------------
    def BoxMorphObject(self, arrObjects):
        
        for obj in arrObjects : 
            obj.Transform(self.__m_TransformMatrix)
    
    
    def GetBreps(self, objectType=None):
        
        brepList = []
        
        if objectType == "Wall" or objectType == None :
            if  self.__m_blnShowWall and len(self.__m_arrWallBreps) and self.__m_arrWallBreps <> [0]: 
                if objectType == "Wall" : return self.__m_arrWallBreps
                brepList += self.__m_arrWallBreps

        if objectType == "Window" or objectType == None :                
            if  self.__m_blnShowWindow and self.__m_dblWinGlassThickness and self.__m_arrWindowBreps <> [0]:
                if objectType == "Window" : return self.__m_arrWindowBreps
                brepList += self.__m_arrWindowBreps

        if objectType == "Pane" or objectType == None :
            if  self.__m_blnShowPane and len(self.__m_arrPaneBreps) and self.__m_arrPaneBreps <> [0]:
                if objectType == "Pane" : return self.__m_arrPaneBreps
                brepList += self.__m_arrPaneBreps

        if objectType == "Mullions" or objectType == None :
            if  self.__m_blnShowMullions :
                brepObjects = []
                if len(self.__m_arrMullionHorBreps) and self.__m_arrMullionHorBreps[0]:
                    for i in range(self.__GetPanelProperty("MullionHorNum")):
                        arrMullions = self.__GetPanelPropertyArray("MullionHorObjArray", i)
                        if arrMullions and arrMullions[0] and not type(arrMullions[0]) == IntType:
                            brepObjects.extend(arrMullions)
                if len(self.__m_arrMullionVertBreps) and self.__m_arrMullionVertBreps[0]:
                    for i in range(self.__GetPanelProperty("MullionVertNum")):
                        arrMullions = self.__GetPanelPropertyArray("MullionVertObjArray", i)
                        if arrMullions and arrMullions[0] and not type(arrMullions[0]) == IntType:
                            brepObjects.extend(arrMullions)
                if objectType == "Mullions" : return brepObjects
                brepList += brepObjects
                
        if objectType == "Shading" or objectType == None :
            if  self.__m_blnShowShading and self.__m_arrShadingBreps and self.__m_arrShadingBreps <> [0]:
                brepObjects = []
                for arrShading in self.__m_arrShadingBreps : brepObjects += arrShading
                if objectType == "Shading" : return brepObjects
                brepList += brepObjects
                
        if objectType == "CustomGeometry" or objectType == None :
            if  self.__m_blnShowCustomGeo:
                if objectType == "CustomGeometry" : return self.__m_CustomGeoDrawBreps        
                brepList += self.__m_CustomGeoDrawBreps
            
        return brepList
        
        
        
    def DrawSceneObjects(self, objectType=None):
        
        parentLayerName = "SKIN_DESIGNER"
        if self.__m_SkinParentName <> None : parentLayerName = self.__m_SkinParentName.split("::")[0]
        if not rs.IsLayer(parentLayerName) : rs.AddLayer(parentLayerName)
        
        currentLayer = rs.CurrentLayer()
        
        
        if objectType == "Wall" or objectType == None:
            #Delete Old Wall If Exists
            if  type(self.__m_arrWallObjects) == ListType and not type(self.__m_arrWallObjects[0]) == IntType and rs.IsObject(self.__m_arrWallObjects[0]): 
                rs.DeleteObjects(self.__m_arrWallObjects)
            if  self.__m_blnShowWall and len(self.__m_arrWallBreps) and self.__m_arrWallBreps <> [0]: 
                if not rs.IsLayer(parentLayerName+"::_P_Wall") : rs.AddLayer("_P_Wall", parent=parentLayerName)
                rs.CurrentLayer(parentLayerName+"::_P_Wall")
                self.__m_arrWallObjects = []
                for brep in self.__m_arrWallBreps : self.__m_arrWallObjects += [sc.doc.Objects.AddBrep(brep)]
            
        if objectType == "Pane" or objectType == None:
            if  type(self.__m_arrPaneObjects) == ListType and not type(self.__m_arrPaneObjects[0]) == IntType \
                and rs.IsObject(self.__m_arrPaneObjects[0]): rs.DeleteObjects(self.__m_arrPaneObjects)
            if  self.__m_blnShowPane and len(self.__m_arrPaneBreps) and self.__m_arrPaneBreps <> [0]:
                if not rs.IsLayer(parentLayerName+"::"+self.__m_strPaneName) : rs.AddLayer(self.__m_strPaneName, parent=parentLayerName)
                rs.CurrentLayer(parentLayerName+"::"+self.__m_strPaneName)
                self.__m_arrPaneObjects = []
                for brep in self.__m_arrPaneBreps : self.__m_arrPaneObjects += [sc.doc.Objects.AddBrep(brep)]
                
        if objectType == "Window" or objectType == None:
            if type(self.__m_arrWindowObjects) == ListType and not type(self.__m_arrWindowObjects[0]) == IntType \
                and rs.IsObject(self.__m_arrWindowObjects[0]) : rs.DeleteObjects(self.__m_arrWindowObjects)
            if  self.__m_blnShowWindow and self.__m_dblWinGlassThickness and self.__m_arrWindowBreps <> [0]:
                if not rs.IsLayer(parentLayerName+"::_P_Glass") : rs.AddLayer("_P_Glass", parent=parentLayerName)
                rs.CurrentLayer(parentLayerName+"::_P_Glass")
                self.__m_arrWindowObjects = []
                for brep in self.__m_arrWindowBreps : self.__m_arrWindowObjects += [sc.doc.Objects.AddBrep(brep)]
                
        if objectType == "Mullions" or objectType == None:
            #Horizontal mullions
            if type(self.__m_arrMullionHorObjects) == ListType and len(self.__m_arrMullionHorObjects) and not type(self.__m_arrMullionHorObjects[0]) == IntType \
                and rs.IsObject(self.__m_arrMullionHorObjects[0]) : rs.DeleteObjects(self.__m_arrMullionHorObjects)
            if len(self.__m_arrMullionHorBreps) and self.__m_arrMullionHorBreps[0]:
                self.__m_arrMullionHorObjects = []
                if not rs.IsLayer(parentLayerName+"::_P_Mullions") : rs.AddLayer("_P_Mullions", parent=parentLayerName)
                rs.CurrentLayer(parentLayerName+"::_P_Mullions")
                for i in range(self.__GetPanelProperty("MullionHorNum")):
                    arrMullions = self.__GetPanelPropertyArray("MullionHorObjArray", i)
                    if arrMullions and arrMullions[0] and not type(arrMullions[0]) == IntType:
                        for brep in arrMullions : self.__m_arrMullionHorObjects += [sc.doc.Objects.AddBrep(brep)]

            #Delete Verticals mullions
            if type(self.__m_arrMullionVertObjects) == ListType and len(self.__m_arrMullionVertObjects) and not type(self.__m_arrMullionVertObjects[0]) == IntType \
                and rs.IsObject(self.__m_arrMullionVertObjects[0]) : rs.DeleteObjects(self.__m_arrMullionVertObjects)
            if len(self.__m_arrMullionVertBreps) and self.__m_arrMullionVertBreps[0]:
                self.__m_arrMullionVertObjects = []
                if not rs.IsLayer(parentLayerName+"::_P_Mullions") : rs.AddLayer("_P_Mullions", parent=parentLayerName)
                rs.CurrentLayer(parentLayerName+"::_P_Mullions")
                for i in range(self.__GetPanelProperty("MullionVertNum")):
                    arrMullions = self.__GetPanelPropertyArray("MullionVertObjArray", i)
                    if arrMullions and arrMullions[0] and not type(arrMullions[0]) == IntType:
                        for brep in arrMullions : self.__m_arrMullionVertObjects += [sc.doc.Objects.AddBrep(brep)]
                
        if objectType == "Shading" or objectType == None:
            #Detlete Shading
            if type(self.__m_arrShadingObjects) == ListType and not type(self.__m_arrShadingObjects[0]) == IntType \
                and rs.IsObject(self.__m_arrShadingObjects[0]) : rs.DeleteObjects(self.__m_arrShadingObjects)
            if  self.__m_blnShowShading and self.__m_arrShadingBreps and self.__m_arrShadingBreps <> [0]:
                self.__m_arrShadingObjects = []; i=0
                for arrShading in self.__m_arrShadingBreps :
                    if not rs.IsLayer(parentLayerName+"::"+self.__m_arrShadingUserData[8][i]) : rs.AddLayer(self.__m_arrShadingUserData[8][i], parent=parentLayerName)
                    rs.CurrentLayer(parentLayerName+"::"+self.__m_arrShadingUserData[8][i])
                    for brep in arrShading : self.__m_arrShadingObjects += [sc.doc.Objects.AddBrep(brep)]
                    i += 1
                    
        if objectType == "CustomGeometry" or objectType == None:
            if type(self.__m_CustomGeoObjects) == ListType and len(self.__m_CustomGeoObjects) > 0 \
                and rs.IsObject(self.__m_CustomGeoObjects[0]) : rs.DeleteObjects(self.__m_CustomGeoObjects)
            self.__m_CustomGeoObjects = []
            if  self.__m_blnShowCustomGeo and self.__m_CustomGeoDrawBreps <> [] :
                for brep in self.__m_CustomGeoDrawBreps:
                    CGLayerName = brep.GetUserString("Layer")
                    if CGLayerName == "" : CGLayerName = "CustomGeo"
                    if not rs.IsLayer(parentLayerName+"::_P_"+CGLayerName) : rs.AddLayer("_P_"+CGLayerName, parent=parentLayerName)
                    rs.CurrentLayer(parentLayerName+"::_P_"+CGLayerName)
                    self.__m_CustomGeoObjects.append(sc.doc.Objects.AddBrep(brep))
            
        rs.CurrentLayer(currentLayer)
        
#----------------------------------------------------------------------------------------------------------------------

SGLibPanel = Panel




class Skin:
    
    __m_skinGenName = "" # Name id (avoids overlapping block names between skin instances
    __m_GeneratePanelsOnly = False
    
    __m_dblOffsetLevel = 0  #Offset in elevation from path to be considered bottom of panel. Any value > 0 creates custom panel. 
    __m_dblOffsetPath = 0 #Offset x distance of first panel at segments.Use list for different dimensions at each segment
    __m_blnSkinWrap = True #Wrap at corners or create custom corner panels
    
    
    __m_resetBayAtPoints = True #Start new bay at new segment
    
    __m_dblFloorToFloor = 4 * _UNIT_COEF #Floor height
    __m_dblMinPanelWidth = 0 #if surface cell width is below this number it will be ignored and panel won't be created.
    __m_dblMinPanelHeight = 0 #if surface cell height is below this number will be ignored and panel won't be created.
        
    
    __m_flatMode = False  #Low geoemtry mode
    __m_drawMode = ""   #"LADYBUG", "DEFAULT" 
    __m_random = None #Global Random generator object
    
    __m_bayList = None # bays used in skin - 'None' will use all panel bays connected

    # Internal members
    __m_objSkinSurface = None #skin surface from skin generator
    __m_surfCurves = [] #top and bottom curves of validated surface
    __m_userData = [] #user parameters stored in skin surface
    __m_panelBays = [] #panel bay data from skin generator
    __m_DesignFunctions = [] 
    
    __m_arrBayMatrix = [] #surface matrix of bay points
    __m_intRows = 0 #number of rows on surface
    __m_intColumns = 0 #number of columns on surface
    __m_intCurrCellColumn = 0
    __m_intCurrCellRow = 0
    __m_intCurrBayIndex = 0
    __m_intCurrBayPanelIndex = 0
    
    __m_arrCornerPoints = []
    
    __m_PanelData = {}
    __m_BayData = {}
    __m_warningData = []
    
    
    
    def __init__(self, skinName = "DEFAULT", objSkinSurface=None, panelBays=None, designFunctions=None):
        
        #Skin generator paramters
        self.__m_skinGenName = skinName 
        
        #create rc geometry if it's a document object and extract user surface paramters
        geo = None; objData = None        
        if str(type(objSkinSurface)) == "<type 'Guid'>" :
            if  not rs.IsObject(objSkinSurface) : return False #Abort skin creation if object is not valid
            objData = rs.ObjectName(objSkinSurface) #extract data if any
            self.__m_objSkinSurface = Rhino.DocObjects.ObjRef(objSkinSurface).Brep()
            
        elif type(objSkinSurface) ==  Rhino.Geometry.Brep :
            self.__m_objSkinSurface = objSkinSurface
            objData = objSkinSurface.GetUserString('Data')
            
        else: return False #Abort skin creation if object is not valid
        
        if  self.__m_objSkinSurface == None : return False #Abort skin creation if object is not valid
        
        #parse user surface-specific parameters (stored on brep user string or object name)
        if  objData : self.__m_userData = list(objData.rsplit("/"))  


        self.__m_surfCurves = self.ExtractEdges(self.__m_objSkinSurface)
        
        self.__m_panelBays = panelBays
        self.__m_DesignFunctions = designFunctions
        self.__m_GeneratePanelsOnly = False
        
        self.__m_dblOffsetLevel = 0
        self.__m_dblOffsetPath = 0
        self.__m_blnSkinWrap = True
        
        self.__m_resetBayAtPoints = True
        
        self.__m_dblFloorToFloor = panelBays[0][0].GetPanelProperty("PanelHeight")
        self.__m_dblMinPanelWidth = .1 * _UNIT_COEF
        self.__m_dblMinPanelHeight = .1 * _UNIT_COEF
        
        self.__m_flatMode = False
        self.__m_drawMode = "DEFAULT" 
        self.__m_objRandom = random.Random() 
        
        self.__m_bayList = None 
      
        #Internal members        
        self.__m_arrBayMatrix = [] 
        self.__m_intRows = 0  
        self.__m_intColumns = 0
        self.__m_intCurrCellColumn = 0
        self.__m_intCurrCellRow = 0
        self.__m_intCurrBayIndex = 0
        self.__m_intCurrBayPanelIndex = 0
        self.__m_arrCornerPoints = []
        self.__m_warningData = []
        
        self.__m_PanelData = {}
        self.__m_BayData = {'BayCounter':[], 'PanelIndices':[], 'BayIndices':[]}
        self.__m_BayData['BayCounter'] = self.__m_panelBays + [0 for x in self.__m_panelBays] #bay counters in format [list of bays, list of  counters]
        
        return True

    def __del__(self):
        #print "adios!"
        pass
        
        
    def ExtractEdges(self, surface):

            
        #get flat base curves and heights of single surfaces
        curveList = []; elevList = []
        for face in  surface.Faces:
            curve, elev = self.GetParametersFromFace(face)
            curveList.append(curve)
            elevList.append(elev)
            
        #unify bottom and top edges to one common top/bottom elevation
        sortedCurves = sorted(curveList, key=lambda curve: curve.PointAtStart.Z)
        sortedElevs = sorted(elevList) 
        bottomElev = sortedCurves[-1].PointAtStart.Z
        for curve in sortedCurves:
            deltaElev =  bottomElev - curve.PointAtStart.Z
            curve.Translate(Rhino.Geometry.Vector3d(0,0,deltaElev))
        bottomCurve = Rhino.Geometry.Curve.JoinCurves(sortedCurves, sc.doc.ModelAbsoluteTolerance, False)[0]
        #create offset of bottom curve for top curve
        topCurve = bottomCurve.DuplicateCurve()
        topCurve.Translate(Rhino.Geometry.Vector3d(0,0,sortedElevs[0]-bottomCurve.PointAtStart.Z))
        
        return [bottomCurve, topCurve]
        
        

    def GetParametersFromFace(self, face):
        
        #Create valid 2d versions of 3d curves
        def MakeValidEdge(edge, type):
            
            ptStart = edge.PointAtStart
            ptEnd = edge.PointAtEnd
            if ptStart.Z == ptEnd.Z: return edge
            else: 
                if  type == "Bottom" : curveElev = max(ptStart.Z,ptEnd.Z)
                elif type == "Top" : curveElev = min(ptStart.Z,ptEnd.Z)
                else: return None
                plane = Rhino.Geometry.Plane(Rhino.Geometry.Point3d(0,0, curveElev), Rhino.Geometry.Vector3d(0,0,1))
                return Rhino.Geometry.Curve.ProjectToPlane(edge, plane)
        
        #find top/bottom curves and make them 2D
        edges = face.DuplicateFace(False).DuplicateEdgeCurves()
        sortedEdges = sorted(edges, key=lambda edge: edge.PointAtNormalizedLength(0.5).Z)
        bottomEdge = MakeValidEdge(sortedEdges[0].DuplicateCurve(), "Bottom")
        topEdge = MakeValidEdge(sortedEdges[-1].DuplicateCurve(), "Top")
        topElev = topEdge.PointAtStart.Z
            
        return bottomEdge, topElev
        
        
        
    def LoadSurfaceProperties(self):
        
        #if self.__m_objSkinSurface == None : return
        
        # init from stored paramters
        OFFSET_LEVEL = self.__m_dblOffsetLevel
        OFFSET_PATH = self.__m_dblOffsetPath
        SKIN_WRAP = self.__m_blnSkinWrap
        PATTERN = self.__m_bayList
        
        #look for Surface-specific parameters stored on object name 
        #with format: OFFSET_LEVEL=float/OFFSET_PATH=float/SKIN_WRAP=bool/PATTERN = [int,..]
        for data in self.__m_userData : 
            if 'OFFSET_LEVEL' in data or 'OFFSET_PATH' in data or 'SKIN_WRAP' in data or 'PATTERN' in data :
                codeObj= compile(data,'<string>','single') ; eval(codeObj)
        
        # parameters update
        self.__m_dblOffsetLevel = OFFSET_LEVEL
        self.__m_dblOffsetPath = OFFSET_PATH
        self.__m_blnSkinWrap = SKIN_WRAP
        self.__m_bayList = PATTERN if type(PATTERN) == ListType else self.__m_bayList
              
        
        
    def SetProperty(self, strProperty, value):
    
        if strProperty in ["SKIN_NAME", "OFFSET_LEVEL", "OFFSET_PATH", "SKIN_WRAP", "RESET_BAY_AT_POINTS", \
            "FLAT_MODE", "DRAW_MODE", "BAY_LIST", "MIN_PANEL_WIDTH", "MIN_PANEL_HEIGHT", "RANDOM_OBJECT", \
            "FLOOR_HEIGHT", "GENERATE_PANELS_ONLY"] :
            self.__SetProperty(strProperty, value)
        else:
            "Skin Parameter "+ strProperty + " is not valid"
        #elif strProperty == "SKIN_SURFACE" : self.__m_objSkinSurface = value
        #elif strProperty == "PANEL_BAY_LIST" : self.__m_panelBays = value
        #elif strProperty == "DESIGN_FUNCTIONS" : self.__m_DesignFunctions = value
        
    def __SetProperty(self, strProperty, value):
    
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
        elif strProperty == "FLOOR_HEIGHT" : 
            if value > 0 : self.__m_dblFloorToFloor = value
        elif strProperty == "GENERATE_PANELS_ONLY" : self.__m_GeneratePanelsOnly = value   
        
        elif strProperty == "SKIN_SURFACE" : self.__m_objSkinSurface = value
        elif strProperty == "PANEL_BAY_LIST" : self.__m_panelBays = value
        elif strProperty == "DESIGN_FUNCTIONS" : self.__m_DesignFunctions = value
        elif strProperty == "PANEL_DATA" : self.__m_PanelData = value
        elif strProperty == "BAY_DATA" : self.__m_BayData = value
        
        
    def GetProperty(self, strProperty):
        
        #if strProperty == "SKIN_SURFACE" : return self.__m_objSkinSurface
        if strProperty == "SKIN_NAME" : return self.__m_skinGenName
        elif strProperty == "SKIN_SURFACE_TYPE" : return str(type(self.__m_objSkinSurface))
        elif strProperty == "SKIN_CELL_ROWS" : return self.__m_intRows
        elif strProperty == "SKIN_CELL_COLUMNS" : return self.__m_intColumns
        elif strProperty == "SKIN_CURRENT_CELL_COLUMN" : return self.__m_intCurrCellColumn
        elif strProperty == "SKIN_CURRENT_CELL_ROW" : return self.__m_intCurrCellRow       
        elif strProperty == "SKIN_CURRENT_BAY_INDEX" : return self.__m_intCurrBayIndex      
        elif strProperty == "SKIN_CURRENT_BAY_PANEL_INDEX" : return self.__m_intCurrBayPanelIndex   
        elif strProperty == "BAY_LIST" : return copy.deepcopy(self.__m_bayList)
        elif strProperty == "FLOOR_HEIGHT" : return self.__m_dblFloorToFloor
        elif strProperty == "WARNING_DATA": return self.__m_warningData
            
    #--------------------------------------------------------------------------------
    #Retrieves a range of Bay and Panel Properties given cell data. 
    #Needs panel number within bay for specific panel data.
    #--------------------------------------------------------------------------------    
    def GetCellProperty(self, intRow, intColumn,  strProperty, bayPanelIndex=0):
        
        
        #TYPE 1 - Cell properties
        
        try:
            bayCornerPts = [self.__m_arrBayMatrix[intRow][intColumn], self.__m_arrBayMatrix[intRow][intColumn + 1],\
                self.__m_arrBayMatrix[intRow + 1][intColumn], self.__m_arrBayMatrix[intRow + 1][intColumn + 1]]    
        except:
            self.__m_warningData.append("GetCellPreoperty: Invalid row/column cell data") 
            return None
        
        #Properties
        if strProperty == "CELL_CORNER_POINTS": return bayCornerPts
        if strProperty == "CELL_PLANE" or strProperty == "PANEL_PLANE": 
            return Rhino.Geometry.Plane(bayCornerPts[0], bayCornerPts[1], bayCornerPts[2])
        if strProperty == "CELL_NORMAL_VECTOR" or strProperty == "PANEL_NORMAL_VECTOR": 
            return  Rhino.Geometry.Plane(bayCornerPts[0], bayCornerPts[1], bayCornerPts[2]).Normal

        #TYPE 2 - Cell Bay assigment properties
        #Bay ID assignement
        cellBayIDsAssigned = list((id for id, points in self.__m_BayData['BayIndices']))
        cellBayPtsAssigned = list((points for id, points in self.__m_BayData['BayIndices']))
        bayIndexAssigned = cellBayIDsAssigned[cellBayPtsAssigned.index(bayCornerPts)]
        #Panel specific vertex data
        bayPanelMatrix = self.GetPanelMatrix(self.__m_arrBayMatrix, intRow, intColumn, self.__m_panelBays[bayIndexAssigned]) #array of panels corner points in bay
        
        
        #Properties
        if strProperty == "BAY_INDEX" : return bayIndexAssigned
        if strProperty == "BAY_POINTS_PANELS" : return bayPanelMatrix 
        if strProperty == "BAY_BASE_PANELS" : return self.__m_panelBays[bayIndexAssigned]
        if strProperty == "BAY_NUM_PANELS" : return len(bayPanelMatrix[0])-1
        
        #Type 3 - Panel instance properties
        
        try: panelCornerPts = self.GetPanelCorners(bayPanelMatrix, bayPanelIndex)
        except: panelCornerPts = None
        #current cell data assigned
        try: cellPtsAssigned = list((pts for pts, n in self.__m_BayData['PanelIndices'] ))
        except: cellPtsAssigned = None
        try: cellNamesAssigned = list((n for pts, n in self.__m_BayData['PanelIndices'] ))
        except: cellNamesAssigned = None
        
        #current panel instance data
        try:
            skinPanelList = []
            for panelGroup in self.__m_PanelData.values():
                for panel in panelGroup: skinPanelList += [panel]                            
            panelsCreated = list((panel for panel, changeFlag in skinPanelList))
            panelNamesCreated = list((panel.GetName() for panel in panelsCreated))
            panelChgFlagCreated = list((changeFlag for panel, changeFlag in skinPanelList))
        except: panelNamesCreated = panelChgFlagCreated = None        
        
        #Properties
        if strProperty == "PANEL_CORNER_POINTS":
            if panelCornerPts: return panelCornerPts
            else: self.__m_warningData.append("GetCellProperty: invalid panel index in bay"); return None
        
        if strProperty == "PANEL_NAME":
            if cellPtsAssigned and cellNamesAssigned :
                panelIndex = cellPtsAssigned.index(panelCornerPts)
                return cellNamesAssigned[panelIndex]
            else: 
                self.__m_warningData.append("GetCellProperty: cell name data not found")
                return None
                
        if strProperty == "PANEL_CELL_ID":
            if  cellPtsAssigned : return cellPtsAssigned.index(panelCornerPts)
            else:
                self.__m_warningData.append("GetCellProperty: cell id data not found")
                return None
                
        if strProperty == "PANEL_INSTANCE":
            if  cellNamesAssigned and cellPtsAssigned and panelNamesCreated:
                cellIndex = cellPtsAssigned.index(panelCornerPts)
                name = cellNamesAssigned[cellIndex]
                panelIndex = panelNamesCreated.index(name)
                return panelsCreated[panelIndex]
            else: 
                self.__m_warningData.append("GetCellProperty: panel instance data not found")
                return None
                
        if strProperty == "PANEL_CHANGE_FLAG":
            if  cellNamesAssigned and cellPtsAssigned and panelChgFlagCreated:
                try: cellIndex = cellPtsAssigned.index(panelCornerPts)
                except: self.__m_warningData.append("GetCellProperty: panel change flag data not found"); return None
                name = cellNamesAssigned[cellIndex]
                panelIndex = panelNamesCreated.index(name)
                return panelChgFlagCreated[panelIndex]
            else: 
                self.__m_warningData.append("GetCellProperty: panel change flag data not found")
                return None
                
        self.__m_warningData.append("GetCellProperty: Invalid property: "+ strProperty)
        
        
        
        
    #--------------------------------------------------------------------------------
    #Generate matrix of corner points of a surface based on panel bay dimensions
    #--------------------------------------------------------------------------------
    def GeneratePanelMatrix(self, dblBayWidth, dblFloorToFloor):
        
        
        #use surface floor to floor value if provided
        if self.__m_dblFloorToFloor > 0 : dblFloorToFloor = self.__m_dblFloorToFloor
        
        
        self.__m_arrBayMatrix = [] #Stores array of bay corner points
        
        CurveBottom = Rhino.RhinoDoc.ActiveDoc.Objects.AddCurve(self.__m_surfCurves[0])
        CurveTop = Rhino.RhinoDoc.ActiveDoc.Objects.AddCurve(self.__m_surfCurves[1])
        
        #Create top/bottom curves from Surface(only extruded curves are evalid at the moment)
        #paramU = rs.SurfaceDomain(self.__m_objSkinSurface,0)   
        #paramV = rs.SurfaceDomain(self.__m_objSkinSurface,1)
        #CurveBottom = rs.ExtractIsoCurve (self.__m_objSkinSurface, [paramU[0],paramV[0]], 0)
        #CurveTop = rs.ExtractIsoCurve (self.__m_objSkinSurface, [paramU[1],paramV[1]], 0)

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
        self.__m_intRows = intLevel+1
        self.__m_intColumns = len(self.__m_arrBayMatrix[0])-1
        
    
    #--------------------------------------------------------------------------------
    #Select and divide curve in specific segments
    #--------------------------------------------------------------------------------
    def DividePoints(self, strObject, dblLength, dblOffset, skinWrap) :
        
        if not rs.IsCurve(strObject) : self.__m_warningData.append("DividePoints: Invalid Curve") ; return
        
        newPoints = [] ; segmentList = []
        
        if  not skinWrap and rs.CurvePointCount(strObject) > 2 : segmentList = rs.ExplodeCurves(strObject)#create individual segements to avoid wrapping
        else : segmentList.append(rs.CopyObject(strObject)) #treat as a single segment

        #store corner points to use on panel placement data
        self.__m_arrCornerPoints = []
        for segment in segmentList:
            self.__m_arrCornerPoints.append(rs.CurveStartPoint(segment))
        self.__m_arrCornerPoints.append(rs.CurveEndPoint(segment))

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
        print "> Skin "+ self.GetProperty("SKIN_NAME")
        #load created panel/bay data already created on previous surfaces
        self.__SetProperty("PANEL_DATA", PanelTypes)
        self.__SetProperty("BAY_DATA", BayData)
        
        #Design functions class variables issue - fixed by replacing them with local variables
        myPanelBays = self.__m_panelBays 
        randomObj = self.__m_objRandom 
        bayList = self.__m_bayList #bay indices used in skin [1 based]
        
        #intial loop settings
        currBayPanel = None ; bayPanelIndex = -1  #Holds current panel in bay; Holds index of current panel in use 
        currentBay = self.__m_panelBays[0] ; self.__m_intCurrBayIndex = -1 # Stores current bay; Stores index of current bay 
        PanelDef = None #Stores current panel of the bay used
        BlockName = "" #Holds block name based on panel data  
         
        intLevels = self.__m_intRows-1
        self.__m_intCurrCellRow = 0 ; self.__m_intCurrCellColumn = -1          #init level and index counters 
        intBaysPerLevel = len(self.__m_arrBayMatrix[0])        
        
        #Change flags store specific panel modifications to ID'd when stored and loaded from database
        ChangeFlag = [0, 0, dict()]     #[panel height , panel width , PropertyDictionary]
        
        blnFloorPanelHeight = False #change panel height to match floor to floor height
        
        #-----------------------Iteration through skin Bay grid---------------------------------------------------------
        #-----------------------BAY & PANEL selection, design and generation--------------------------------------------
        while True :
            
            bayPanelIndex += 1 # next panel of current bay
            
            if bayPanelIndex == len(currentBay) or bayPanelIndex == 0: #when done with current bay panels
                bayPanelIndex = 0; self.__m_intCurrBayIndex += 1 #move on to next panel bay
                if self.__m_intCurrBayIndex == len(self.__m_panelBays) : self.__m_intCurrBayIndex = 0  #and loop when done with all bays
                
                #------------BAY SECTION---------------------------------------------------
                self.__m_intCurrCellColumn +=  1 # move to next cell on row
                
                #--------Level End detection and action
                if self.__m_intCurrCellColumn == intBaysPerLevel-1 :
                    self.__m_intCurrCellColumn = 0 ; self.__m_intCurrCellRow += 1 ; #start next row up
                    intBaysPerLevel = len(self.__m_arrBayMatrix[self.__m_intCurrCellRow])
                    if self.__m_resetBayAtPoints : bayPanelIndex = 0; currentBay = self.__m_panelBays[0]; self.__m_intCurrBayIndex=-1 #reset bay at beginng of row
                    if self.__m_intCurrCellRow > intLevels : break        #exit at end of grid
                    
                #---------Run BAY-TYPE Design Functions (run when a new bay is started)
                
                #store current bay corner points (needed by some functions)
                bayCornerPoints = [self.__m_arrBayMatrix[self.__m_intCurrCellRow][self.__m_intCurrCellColumn], self.__m_arrBayMatrix[self.__m_intCurrCellRow][self.__m_intCurrCellColumn + 1],\
                        self.__m_arrBayMatrix[self.__m_intCurrCellRow + 1][self.__m_intCurrCellColumn], self.__m_arrBayMatrix[self.__m_intCurrCellRow + 1][self.__m_intCurrCellColumn + 1]]    
                #Run default function on bay first.        
                currentBay, self.__m_intCurrBayIndex = self.DesFunc_Default_Panel_Bays(self.__m_panelBays, bayList)
                
                #Run all bay-type Design Functions available
                if self.__m_DesignFunctions: 
                    for dsFunc in self.__m_DesignFunctions:
                        if dsFunc and dsFunc.IsLayoutType() : currentBay, self.__m_intCurrBayIndex = dsFunc.Run(myPanelBays, currentBay, self)
                
                #----------Update Bay data
                BayDataCounter = self.__m_BayData['BayCounter']
                BayDataCounter[BayDataCounter.index(currentBay)+len(self.__m_panelBays)] += 1 #update bay type counters
                self.__m_BayData['BayIndices'].append([self.__m_panelBays.index(currentBay), bayCornerPoints])
                
                panelMatrix = self.GetPanelMatrix(self.__m_arrBayMatrix, self.__m_intCurrCellRow, self.__m_intCurrCellColumn, currentBay) #get array of corner points of all panels in bay
                
            
            #---------------PANEL SECTION------------------------------------------------------------------------------------------------
            PanelDef = None     #reset variable (needed by panel-type function calls)
            currBayPanel = currentBay[bayPanelIndex] 
            if bayPanelIndex > len(panelMatrix[0])-2  : continue #skip rest of bay if not finished at end of row
            
            #store panel corner points in skin
            arrAreaPanelPoints = self.GetPanelCorners(panelMatrix, bayPanelIndex)
            
            #----------------Panel Profile: Flagging Size data
            ChangeFlag = [0, 0, dict(), ""]     #[panel height , panel width , Property_Dictionary, skin_placement (string)]
            
            #ChangeFlag[0]stores panel height number (in unit/1000), used to store and retrieve panels in database 
            panelHeight = rs.Distance(arrAreaPanelPoints[0], arrAreaPanelPoints[2])
            # panel height limited to current panel height, regardless of floor to floor value
            if not blnFloorPanelHeight and panelHeight >= currBayPanel.GetHeight() - sc.doc.ModelAbsoluteTolerance : panelHeight = currBayPanel.GetHeight() 
            ChangeFlag[0] = int(round(panelHeight,3)*1000)
            
            #ChangeFlag[1] stores panel width number (in unit/1000 ), used to store and retrieve panels in database 
            panelWidth = rs.Distance(arrAreaPanelPoints[0],arrAreaPanelPoints[1])
            ChangeFlag[1] = int(round(panelWidth,3)*1000)
            
            #Check first if panel size is large enough
            if panelHeight < self.__m_dblMinPanelHeight or panelWidth < self.__m_dblMinPanelWidth :
                print ">>>  Panel [Floor:"+str(self.__m_intCurrCellRow)+" Bay:"+str(self.__m_intCurrCellColumn)+" Panel:"+str(bayPanelIndex)+\
                    "] under minimum size ("+str(round(panelWidth,4))+","+str(round(panelHeight,4))+") Discarded"
                continue
                
                
            #--------------Panel Profile:Flagging placement data in ChangeFlag[3] 
            strSkinPlacement = 'Field'
            placementList = ['Left', 'Right']
            for side in [0,1]: #corner detection    
                indexPoint = rs.PointArrayClosestPoint(self.__m_arrCornerPoints, arrAreaPanelPoints[side])
                cornerPoint = copy.deepcopy(self.__m_arrCornerPoints[indexPoint])
                cornerPoint[2] = arrAreaPanelPoints[side][2]
                if rs.PointCompare(cornerPoint, arrAreaPanelPoints[side], self.__m_dblMinPanelWidth + sc.doc.ModelAbsoluteTolerance) :
                    if strSkinPlacement == 'Field': strSkinPlacement = placementList[side]
                    elif strSkinPlacement == 'Left': strSkinPlacement += placementList[side]
            #tagging placement
            ChangeFlag[3] = strSkinPlacement
            
            #---------Run PANEL DESIGN FUNCTION First call / Flagging Changes in ChangeFlag[2] - run in every panel.
            if self.__m_DesignFunctions: #Run all Panel Design Functions available
                for dsFunc in self.__m_DesignFunctions:
                    if dsFunc and dsFunc.IsPanelType() : dsFunc.Run_Flag(self, ChangeFlag, currBayPanel)
                    
                     
            
            #---------Search Panel Type and Profile in Panel Database
            #Checks for same panel type with same changeFlags.
            #Database format: Dictionary = {BasePanelType_Name_A:[[PanelType Object 1, ChangeFlag],[PanelType Object 2, ChangeFlag],.....],
            #                               BasePanelType_Name_B:[[PanelType Object 1, ChangeFlag],.....], BasePanelType_Name_C:....}
            
            
            if currBayPanel.GetName() in self.__m_PanelData : #found panel type?
                for pIndex in range(len(self.__m_PanelData[currBayPanel.GetName()])):
                    if self.__m_PanelData[currBayPanel.GetName()][pIndex][1] == ChangeFlag : #found same profile?
                        PanelDef = self.__m_PanelData[currBayPanel.GetName()][pIndex][0] #retrieve panel object stored
                        if  len(PanelDef.GetPanelProperty("BlockInstances")) == 0 : BlockName = ""; break #panels with empty blocks (ex.Ladybug) are skipped
                        BlockName = rs.BlockInstanceName(PanelDef.GetPanelProperty("BlockInstances")[0])
                        break
                
            else: self.__m_PanelData[currBayPanel.GetName()] = [] 
            #----------------------------------------------------------------------------------------------------
            #NEW PANEL TYPE: A new panel type is generated if no match found in database
            if PanelDef == None :
                
                #-----Create panel copy if unique ----------------------------
                #PanelTypeCount += 1
                PanelDef = SGLibPanel()
                PanelDef.Copy(currBayPanel)
                
                #PANEL DESIGN FUNCTION SECTION - Second Call / Apply custom properties based on ChangeFlag[2] data
                tmpChangeFlag = copy.deepcopy(ChangeFlag) #create a copy (protect from Design Functions modif.) 
                if self.__m_DesignFunctions: #Run all Panel Design Functions available
                    for dsFunc in self.__m_DesignFunctions:
                        if dsFunc and dsFunc.IsPanelType() : dsFunc.Run_Modify(tmpChangeFlag, PanelDef)
                        
                        
                #ChangeFlag = tmpChangeFlag #restore change flag data
                
                #CUSTOM PANEL SIZE SECTION (automated edge conditions)
                #-----Name tag panel (used by Panel Inventory component) 

                PanelDef.SetName(PanelDef.GetName() + " "+strSkinPlacement)
                if round(panelHeight,3) <> round(PanelDef.GetPanelProperty("PanelHeight"),3) : 
                    PanelDef.SetName(PanelDef.GetName() + " -Height:"+str(round(panelHeight,2)))
                if round(panelWidth,3) <> round(PanelDef.GetPanelProperty("PanelWidth"),3) : 
                    PanelDef.SetName(PanelDef.GetName() + " -Width:"+str(round(panelWidth,2)))
                #-----Resize panel ----
                PanelDef.SetHeight(panelHeight)
                PanelDef.SetWidth(panelWidth)
                #----Skin Context Paramters----
                PanelDef.SetPanelProperty("SkinPlacement", strSkinPlacement)
                
                
                #CONDITIONAL DEFINITIONS SECTION
                #----Run Conditional definitions on Panel (from panel component input)
                PanelDef.RunConditionalDefinition()
                
                
                #Draw panel geometry to create block
                PanelDef.Draw() 
                
                #Add new panel type to Database
                CurrBayList = self.__m_PanelData.get(currBayPanel.GetName())
                CurrBayList.append([PanelDef, copy.deepcopy(ChangeFlag)])
                self.__m_PanelData[currBayPanel.GetName()] = CurrBayList
                
                #-----Generate new Panel Block params --------------------------------------------------
                
                BlockName = "_P_ID-" + self.__m_skinGenName + "_" + str(ChangeFlag) + currBayPanel.GetName()
                
            #-----Create Block instance with current panel design
            if not self.__m_GeneratePanelsOnly:
                PanelDef.CreateBlockCopy(BlockName, arrAreaPanelPoints, False)
            
            PanelIndeces = self.__m_BayData ['PanelIndices']
            PanelIndeces.append([arrAreaPanelPoints, PanelDef.GetName()])
            
        #cRow = 1;cCol = 3; cPanel =0 
        #bayBasePanels = self.GetCellProperty(cRow,cCol,"BAY_BASE_PANELS") ; bayPoints = self.GetCellProperty(cRow,cCol,"BAY_POINTS_PANELS")
        #for i,p in enumerate(bayBasePanels): print ["bay panels & points", p.GetName()]
        
        #print list((p for pts in bayPoints for p in pts ))
        #for index in range(self.GetCellProperty(cRow,cCol,"BAY_NUM_PANELS")): 
            #print ["panel instance & chngflag", self.GetCellProperty(cRow,cCol,"PANEL_INSTANCE",index).GetName(), self.GetCellProperty(cRow,cCol,"PANEL_CHANGE_FLAG",index)]
        #print self.__m_BayData['BayIndices']
        return self.__m_PanelData, self.__m_BayData
    
    
    #--------------------------------------------------------------------------------
    #Retrieve corner points of each panel in cell (bays have 1+ panels)
    #--------------------------------------------------------------------------------
    def GetPanelMatrix(self, bayMatrix, intLevel, intBayID, currentBay):
        
        arrAreaBayPoints = [bayMatrix[intLevel][intBayID], bayMatrix[intLevel][intBayID + 1],\
            bayMatrix[intLevel + 1][intBayID], bayMatrix[intLevel + 1][intBayID + 1]]
        panelMatrix = []
        bayLength = 0
        for panel in currentBay :
            bayLength += panel.GetPanelProperty("PanelWidth")        
            
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
                    if (bayLength-lengthTotals)< panel.GetPanelProperty("PanelWidth")*prevCoefLength:
                        coefLength = lengthLine/bayLength
                lengthTotals += panel.GetPanelProperty("PanelWidth")*coefLength
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
    def DesFunc_Default_Panel_Bays(self, PanelBay_List, defaultBayList=None):

        validBayList = copy.deepcopy(defaultBayList)
        
        # Define new current bay index based on the exclude bays listed 
        if  validBayList:   
            for index in range(len(validBayList)) : validBayList[index] -=1 #cero based indexes
        else: validBayList = range(len(PanelBay_List))
        
        while True:
            if  self.__m_intCurrBayIndex in validBayList : break
            self.__m_intCurrBayIndex +=1
            if self.__m_intCurrBayIndex == len(PanelBay_List) : self.__m_intCurrBayIndex = min(validBayList)
                
        if self.__m_intCurrBayIndex >= len(PanelBay_List) : 
            self.__m_warningData.append("DesFunc_Default_Panel_Bays: Invalid bay index, using bay 1")
            return [PanelBay_List[0], 0]
        return  [PanelBay_List[self.__m_intCurrBayIndex], self.__m_intCurrBayIndex]
        

# Design Function  Class
# Base class used for all DesignFunctions

class BaseDesignFunction:
    
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        pass
      
    def IsLayoutType(self):
        pass
        
    def IsPanelType(self):
        pass  
    
    def Reset(self):
        pass
        
    #Layout Design Function
    def Run(self, PanelBay_List, currentBay, skinInstance):
        pass
        
    #Panel Design Function
    def Run_Flag(self, skinInstance, ChangeFlag, BasePanel):
        pass
        
    #Panel Deisgn Function
    def Run_Modify(self, ChangeFlag, BasePanel):
        pass
        

sc.sticky["SGLib_Panel"] = Panel

sc.sticky["SGLib_Skin"] = Skin

sc.sticky["SGLib_DesignFunction"] = BaseDesignFunction


print "SkinDesigner Running..."