


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

ghenv.Component.Name = "SkinDesigner_PP-LBHB_PanelsOutput"
ghenv.Component.NickName = 'PP-LBHB_PanelsOutput'
ghenv.Component.Message = 'VER 0.0.45\nMay_10_2016'
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
    __m_PPDrawMode = None
    __m_ShadeWidthThresh = None
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        self.__m_functionCall = "LBHB_PanelsOutput(SkinPanel_List)"
        self.__m_PPDrawMode = "LADYBUG"
        if ShadeWidthThreshold <> None : self.__m_ShadeWidthThresh = ShadeWidthThreshold
        
        
    def PP_SetPanelsProperties(self, PanelBay_List):
        
        for panelBay in PanelBay_List:
            for panel  in panelBay :
                panel.SetDrawMode(self.__m_PPDrawMode)
                if self.__m_ShadeWidthThresh <> None :
                    panel.SetProperty("LB_ShadeThreshold", self.__m_ShadeWidthThresh)
    
    
    def RunString(self):
        return self.__m_functionCall
        
        
    #----------------------------------------------------------------------------------------
    # Prepares Ladybug data (extracts optimized glass and shading geoemetry for analysis)
    #-----------------------------------------------------------------------------------------
    
    def LBHB_PanelsOutput(self, SkinPanel_List):
        
   
        
        #--Prep work:Convert to Brep versions from GUI objects and pack in a 2D list and move to LB layers 
        rs.AddLayer("_P_LB_Window")
        rs.AddLayer("_P_LB_Context")
        rs.AddLayer("_P_LB_Wall")
        rs.AddLayer("_P_LB_Panel")
        
        LadybugBrepLists = [[],[],[]]
 

        return [self.RunString(), SkinPanel_List.values()]


PostProcFunction = PP_LadybugFunction()
print "Done"
