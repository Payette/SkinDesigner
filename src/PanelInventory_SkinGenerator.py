
# By Santiago Garay
# Panel_Types

"""
Use this component to display all panel types used to generate the skin. Also a count of each panelis provided
On bold are dicplayed the panels defined as Panel objects. The additional panels created by Skin_Automata

-

    Args:
        SkinPanel_List: List  
        Loc: ID of point object that defines mock up location

    Returns:
        Nothing
"""

ghenv.Component.Name = "PanelInventory_SkinGenerator"
ghenv.Component.NickName = 'Panel_Inventory'
ghenv.Component.Message = 'VER 0.0.45\nApr_06_2016'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "03 | Output"




import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
from types import *
SGLibPanel = sc.sticky["SGLib_Panel"]


PANEL_TYPES_ID=str(ghenv.Component.ComponentGuid)

def DeleteMockup():
    
    if not sc.sticky["PanelTypes_Data"+ PANEL_TYPES_ID] : return
        
    for data in sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] :
        if isinstance(data, SGLibPanel): data.HideAll() #same as deleting all panel objects
        elif rs.IsText(data) : rs.DeleteObject(data)
    

#initialize
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

if  LocCircle and rs.IsObject(LocCircle) and rs.IsCircle(LocCircle): 
    Loc = rs.CircleCenterPoint(LocCircle)
    offsetX = Loc[0] ; offsetY = Loc[1] ; offsetZ = Loc[2]
else: print "I need a circle for location"


Mockup_Bay = [] ; textTypes = [] 


if "PanelTypes_Data"+PANEL_TYPES_ID not in sc.sticky : sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] = []

DeleteMockup()

if SkinPanel_List:
    for panelData in SkinPanel_List :
        for i in range(len(panelData)):
                
                
            panelName = panelData[i][0].GetName()
            #print panelName
            if (panelName.find("-Width")>0 or panelName.find("-Height")>0): 
                if ShowCustom :fontHeight = 0.5 ; fontStyle=0 
                else: continue #skip custom panel if ShowCustom off 
            else: fontHeight= .6 ; fontStyle = 1
            
            arrBoxPoints = [[offsetX, offsetY, offsetZ],[offsetX + panelData[i][0].PanelProperty("PanelWidth"), offsetY, offsetZ],\
                [offsetX, offsetY, offsetZ+panelData[i][0].PanelProperty("PanelHeight")],\
                [offsetX + panelData[i][0].PanelProperty("PanelWidth"), offsetY, offsetZ+panelData[i][0].PanelProperty("PanelHeight")]]
                
            #create text info
            blockCount = len(panelData[i][0].PanelProperty("BlockInstances"))
            textTypes.append(rs.AddText(panelName + "   Count: " + str(blockCount), rs.PointSubtract(arrBoxPoints[0], [0,1,0]), fontHeight, font_style=fontStyle))
            rs.RotateObject(textTypes[len(textTypes)-1], rs.TextObjectPoint(textTypes[len(textTypes)-1]), 270)
            
            #create panel copy
            Mockup_Bay.append(SGLibPanel())
            Mockup_Bay[len(Mockup_Bay)-1].Copy(panelData[i][0])
            Mockup_Bay[len(Mockup_Bay)-1].MorphPanel(arrBoxPoints)
            #print i; print panelData
            
            Mockup_Bay[len(Mockup_Bay)-1].Draw()

            offsetX = offsetX + Mockup_Bay[len(Mockup_Bay)-1].PanelProperty("PanelWidth")+ 1
            
    sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] = Mockup_Bay + textTypes
else:
    DeleteMockup()
    
#Wrapup
rs.EnableRedraw(True)
sc.doc = ghdoc
