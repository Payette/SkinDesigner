


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

ghenv.Component.Name = "PF_Ladybug_Window_SkinGenerator"
ghenv.Component.NickName = 'PF_Ladybug_Window'
ghenv.Component.Message = 'VER 0.0.44\nJan_13_2016'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "04 | Functions"


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
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        if windowStep : self.__m_WindowStep = windowStep
        self.__m_functionCall = "LadyBugFunc_Panel_NthWindow(SkinPanel_List,"+str(self.__m_WindowStep)+")"
        self.__m_PPDrawMode = "LADYBUG"
        
    def PPDrawMode(self):
        return self.__m_PPDrawMode
        
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
        #print panelBlockList
        panelBlockList = panelBlockList[0:-1:int(stepNumber)] #Nth panel filtering
    
        #--Collect current objects in key LB layers before exploding targeted blocks
        initDocGlassSet = set(rs.ObjectsByLayer("_P_Glass"))
        initDocMullionSet = set(rs.ObjectsByLayer("_P_Mullions"))
        initDocShadingSet = set(rs.ObjectsByLayer("_P_Shading"))

        #Explode blocks of seleted panels
        tmpPanelElements = []
        tmpPanelBlockList = rs.CopyObjects(panelBlockList)
        for tmpPanelBlock in tmpPanelBlockList :
            tmpPanelElements += rs.ExplodeBlockInstance(tmpPanelBlock)

        #--Collect new objects in key layers
        newDocGlassSet = set(rs.ObjectsByLayer("_P_Glass"))
        newDocMullionSet = set(rs.ObjectsByLayer("_P_Mullions"))
        newDocShadingSet = set(rs.ObjectsByLayer("_P_Shading"))
      
        #Store Ladybug elements and delete leftovers
        lbGlassSet = set()
        lbMullionSet = set()
        lbShadingSet = set()
        lbGlassSet = newDocGlassSet - initDocGlassSet
        lbMullionSet = newDocMullionSet - initDocMullionSet
        lbShadingSet = newDocShadingSet - initDocShadingSet
        rs.DeleteObjects(set(tmpPanelElements)-lbGlassSet-lbMullionSet-lbShadingSet)
        
        #--Prep work:Convert to Brep versions from GUI objects and pack in a 2D list and move to LB layers 
        rs.AddLayer("_P_LB_Geometry")
        rs.AddLayer("_P_LB_Context")
        LadybugBrepLists = [[],[]]
        for obj in lbGlassSet | lbMullionSet | lbShadingSet :
        #for obj in lbGlassSet | lbShadingSet:
            if obj in lbGlassSet : rs.ObjectLayer(obj,"_P_LB_Geometry")
            else: rs.ObjectLayer(obj,"_P_LB_Context")
            tmpBrep = rs.coercebrep(obj)
            if  tmpBrep <> None : LadybugBrepLists[not obj in lbGlassSet].append(tmpBrep)
            else : rs.DeleteObject(obj) #delete point objects included as mullion placeholder in blocks
        
        sc.sticky["Panel_Ladybug_Data"] = lbGlassSet | lbMullionSet | lbShadingSet
        print LadybugBrepLists
        return LadybugBrepLists


PostProcFunction = PP_LadybugFunction()
#print PostProcFunction.RunString()
