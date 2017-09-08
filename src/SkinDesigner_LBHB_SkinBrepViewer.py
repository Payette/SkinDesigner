


# By Santiago Garay
# Skin Generator

"""
Use this component 
_
_
To add more panels bays in the construction, simply zoom into the component and hit the lowest "+" sign that shows up on the input side.  To remove panels from the construction, zoom into the component and hit the lowest "-" sign that shows up on the input side.
-
    Args:
        

    Returns:
        

"""

ghenv.Component.Name = "SkinDesigner_LBHB_SkinBrepViewer"
ghenv.Component.NickName = 'LBHB_SkinBrepViewer'
ghenv.Component.Message = 'VER 0.0.51\nJun_02_2016'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "04 | Display"


import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
#from types import *
#import random
#import copy
#import math

SGLibPanel = sc.sticky["SGLib_Panel"]


#init 
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

#----------------------------------------------------------------------------------------
# Cleanup old ladybug objects
#----------------------------------------------------------------------------------------



if PostProcData:
    
    for PPData in PostProcData:

        if isinstance(PPData, list) and len(PostProcData) and "LBHB_PanelsOutput" in PPData[0]:
            
            SkinPanel_List = PPData[1]
            if windowStep : stepNumber = windowStep
            else: stepNumber = 1
            
            #Detect Panel with window selection 
            panelBlockList =[]
            for group in SkinPanel_List :
                for item in group :
                    if isinstance(item[0], SGLibPanel) and item[0].PanelProperty("WindowVisibility"): #Panel has a window? 
                        panelBlockList += item[0].PanelProperty("BlockInstances")
        
            panelBlockList = panelBlockList[0:-1:int(stepNumber)] #Nth panel filtering
        
            #--Collect current objects in key layers before exploding targeted blocks
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
            
            #--Prep work:Convert to Brep versions from GUI objects 
            LadybugBrepLists = [[],[],[]]
                
            for obj in lbGlassSet | lbMullionSet | lbShadingSet | lbWallSet:
                tmpBrep = rs.coercebrep(obj)
                if  tmpBrep <> None :
                    if obj in lbGlassSet :
                        LadybugBrepLists[0].append(tmpBrep.DuplicateBrep())
                    if obj in lbMullionSet | lbShadingSet :
                        LadybugBrepLists[1].append(tmpBrep.DuplicateBrep())
                    if obj in lbWallSet : 
                        LadybugBrepLists[2].append(tmpBrep.DuplicateBrep())
                rs.DeleteObject(obj) #delete objects

            WindowGeo = LadybugBrepLists[0]
            ShadingGeo = LadybugBrepLists[1]
            WallGeo = LadybugBrepLists[2]



#Wrapup
rs.EnableRedraw(True)
sc.doc = ghdoc
print "Done"
