
# By Santiago Garay
# Mock_up

"""
Use this component to generate a panel or panel bay mock up.
-
Refer to PanelLib API for Definition input functions
    Args:
        Panel_Bay: Panel object or Panel_Bay (list of Panels) 
        Loc: ID of point object that defines mock up location

    Returns:
        Nothing
"""

ghenv.Component.Name = "Panel_Viewer_SkinGenerator"
ghenv.Component.NickName = 'Panel_Viewer'
ghenv.Component.Message = 'VER 0.0.46\nApr_07_2016'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "03 | Output"

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
#import sys
SGLibPanel = sc.sticky["SGLib_Panel"]


def DeleteMockup():
    
    if not sc.sticky["Mockup_Data"] : return
        
    for panel in sc.sticky["Mockup_Data"] :
        if isinstance(panel, SGLibPanel):
            panel.HideAll() #same as deleting all panel objects
    

#initialize
offsetX = 0; offsetY = 0; offsetZ = 0
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

if  LocCircle and rs.IsObject(LocCircle) and rs.IsCircle(LocCircle): 
    Loc = rs.CircleCenterPoint(LocCircle)
    offsetX = Loc[0] ; offsetY = Loc[1] ; offsetZ = Loc[2]
else: print "I need a circle for location"

Mockup_Bay = []


if "Mockup_Data" not in sc.sticky : sc.sticky["Mockup_Data"] = []

DeleteMockup()
    
if Panel_Bay and Panel_Bay[0]:
    for i in range(len(Panel_Bay)):
        arrBoxPoints = [[offsetX, offsetY, offsetZ],[offsetX + Panel_Bay[i].PanelProperty("PanelWidth"), offsetY, offsetZ],\
            [offsetX, offsetY, offsetZ+Panel_Bay[i].PanelProperty("PanelHeight")],\
            [offsetX + Panel_Bay[i].PanelProperty("PanelWidth"), offsetY, offsetZ+Panel_Bay[i].PanelProperty("PanelHeight")]]
        try:
            Mockup_Bay.append(SGLibPanel())
            Mockup_Bay[i].Copy(Panel_Bay[i])
            Mockup_Bay[i].RunConditionalDefinition()
            Mockup_Bay[i].MorphPanel(arrBoxPoints)
            Mockup_Bay[i].Draw()
        except Exception:
            DeleteMockup()
            raise
        offsetX = offsetX + Mockup_Bay[i].PanelProperty("PanelWidth")
    sc.sticky["Mockup_Data"] = Mockup_Bay
else:
    DeleteMockup()
    
#Wrapup
rs.EnableRedraw(True)
sc.doc = ghdoc

print "done"