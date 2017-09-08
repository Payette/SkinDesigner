


# By Santiago Garay
# Skin Generator

"""
Use this component to apply a post-processing function(representation properties of the skin) to a SkinGenerator component. This component optimizes the display of the panel geometry for better facade analysis with Ladybug Tools. 

    Args:
        ShadeWidthThreshold: A floating point value indicating the minimum shading and mullion caps projections to be included in the final geometry of the panels. Default value is 0.1m
    Returns:
        PostProcFunction:  A PPFunction object to be connected to the SkinGenerator postProcFunctions input.
"""

ghenv.Component.Name = "SkinDesigner_PP-LBHB_Output"
ghenv.Component.NickName = 'PP-LBHB_Output'
ghenv.Component.Message = 'VER 0.0.50\nSep_03_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"
try: ghenv.Component.AdditionalHelpFromDocStrings = "3"
except: pass

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
#from types import *
#import random
#import copy
#import math

SGLibPanel = sc.sticky["SGLib_Panel"]

#GLOBAL PARAMETERS-------------------------------------------------------
#init set up global variables
_UNIT_COEF = 1
sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == Rhino.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
sc.doc = ghdoc


#paramters
#init 
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

class PP_LadybugFunction:
    
    __m_functionCall = ''
    __m_PPDrawMode = None
    __m_ShadeWidthThresh = 0.1*_UNIT_COEF
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        self.__m_functionCall = "LBHB_PanelsOutput(skinPanelData)"
        self.__m_PPDrawMode = "LADYBUG"
        
        if  ShadeWidthThreshold <> None : self.__m_ShadeWidthThresh = ShadeWidthThreshold
        
    def PP_SetPanelsProperties(self, PanelBay_List):
        
        for panelBay in PanelBay_List:
            for panel  in panelBay :
                panel.SetDrawMode(self.__m_PPDrawMode)
                if self.__m_ShadeWidthThresh <> None :
                    panel.SetPanelProperty("LB_ShadeThreshold", self.__m_ShadeWidthThresh)
    
    
    def RunString(self):
        return self.__m_functionCall
        
        
    #----------------------------------------------------------------------------------------
    # Prepares Ladybug data (extracts optimized glass and shading geoemetry for analysis)
    #-----------------------------------------------------------------------------------------
    
    def LBHB_PanelsOutput(self, skinPanelData):
        
   
        
        #--Prep work:Convert to Brep versions from GUI objects and pack in a 2D list and move to LB layers 
        return [self.RunString(), skinPanelData.values()]


PostProcFunction = PP_LadybugFunction()
print "Done"
