


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

ghenv.Component.Name = "SkinDesigner_PP-DrawLadybug"
ghenv.Component.NickName = 'PP-DrawLadybug'
ghenv.Component.Message = 'VER 0.0.44\nApr_07_2016'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"


import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
#from types import *
#import random
#import copy
#import math

SGLibPanel = sc.sticky["SGLib_Panel"]

#GLOBAL PARAMETERS-------------------------------------------------------


#paramters
#init 
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

class PP_LadybugFunction:
    
    __m_functionCall = ''
    __m_WindowStep = 1
    __m_PPDrawMode = None
    __m_ShadeWidthThresh = None
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        if windowStep : self.__m_WindowStep = windowStep
        self.__m_functionCall = "LadyBugFunc_Panel_NthWindow(SkinPanel_List,"+str(self.__m_WindowStep)+")"
        self.__m_PPDrawMode = "LADYBUG"
        if ShadeWidthThreshold <> None : self.__m_ShadeWidthThresh = ShadeWidthThreshold
        
        
    def PP_SetPanelsProperties(self, PanelBay_List):
        
        for panelBay in PanelBay_List:
            for panel  in panelBay :
                panel.SetDrawMode(self.__m_PPDrawMode)
                if self.__m_ShadeWidthThresh <> None :
                    panel.SetProperty("LB_ShadeThreshold", self.__m_ShadeWidthThresh)

        
    def PPShadeWidthThreshold(self):
        return self.__m_ShadeWidthThresh

    def RunString(self):
        return self.__m_functionCall
        
        
    #----------------------------------------------------------------------------------------
    # Prepares Ladybug data (extracts optimized glass and shading geoemetry for analysis)
    #-----------------------------------------------------------------------------------------
    
    def LadyBugFunc_Panel_NthWindow(self, SkinPanel_List, stepNumber):
        
        #Detect Panel with window selection 
        panelBlockList =[]
        for group in SkinPanel_List.values() :
            for item in group :
                if isinstance(item[0], SGLibPanel) and item[0].PanelProperty("WindowVisibility"): #Panel has a window? 
                    panelBlockList += item[0].PanelProperty("BlockInstances")

        panelBlockList = panelBlockList[0:-1:int(stepNumber)] #Nth panel filtering
    
        #--Collect current objects in key LB layers before exploding targeted blocks
        initDocGlassSet = set(rs.ObjectsByLayer("_P_Glass"))
        initDocMullionSet = set(rs.ObjectsByLayer("_P_Mullions"))
        initDocShadingSet = set(rs.ObjectsByLayer("_P_Shading"))
        initDocWallSet = set(rs.ObjectsByLayer("_P_Wall"))
        
        #Explode blocks of seleted panels
        tmpPanelElements = []
        tmpPanelBlockList = rs.CopyObjects(panelBlockList)
        for tmpPanelBlock in tmpPanelBlockList :
            tmpPanelElements += rs.ExplodeBlockInstance(tmpPanelBlock)

        #--Collect new objects in key layers
        newDocGlassSet = set(rs.ObjectsByLayer("_P_Glass"))
        newDocMullionSet = set(rs.ObjectsByLayer("_P_Mullions"))
        newDocShadingSet = set(rs.ObjectsByLayer("_P_Shading"))
        newDocWallSet = set(rs.ObjectsByLayer("_P_Wall"))        
      
        #Store Ladybug elements and delete leftovers
        lbGlassSet = set()
        lbMullionSet = set()
        lbShadingSet = set()
        lbWallSet = set()
        lbGlassSet = newDocGlassSet - initDocGlassSet
        lbMullionSet = newDocMullionSet - initDocMullionSet
        lbShadingSet = newDocShadingSet - initDocShadingSet
        lbWallSet = newDocWallSet - initDocWallSet
        rs.DeleteObjects(set(tmpPanelElements)-lbGlassSet-lbMullionSet-lbShadingSet-lbWallSet)
        
        #--Prep work:Convert to Brep versions from GUI objects and pack in a 2D list and move to LB layers 
        rs.AddLayer("_P_LB_Window")
        rs.AddLayer("_P_LB_Context")
        rs.AddLayer("_P_LB_Wall")
        
        LadybugBrepLists = [[],[],[]]
            
        for obj in lbGlassSet | lbMullionSet | lbShadingSet | lbWallSet:
            tmpBrep = rs.coercebrep(obj)
            if  tmpBrep <> None :
                if obj in lbGlassSet :
                    rs.ObjectLayer(obj,"_P_LB_Window")
                    LadybugBrepLists[0].append(tmpBrep)
                if obj in lbMullionSet | lbShadingSet : 
                    rs.ObjectLayer(obj,"_P_LB_Context")
                    LadybugBrepLists[1].append(tmpBrep)
                if obj in lbWallSet : 
                    rs.ObjectLayer(obj,"_P_LB_Wall")
                    LadybugBrepLists[2].append(tmpBrep)                
            else : rs.DeleteObject(obj) #delete point objects included as mullion placeholder in blocks
                 
        rs.LayerVisible("_P_LB_Window", False)
        rs.LayerVisible("_P_LB_Context", False)
        rs.LayerVisible("_P_LB_Wall", False)
        sc.sticky["Panel_Ladybug_Data"] = lbGlassSet | lbMullionSet | lbShadingSet |lbWallSet

        return LadybugBrepLists


PostProcFunction = PP_LadybugFunction()
print "Done"
