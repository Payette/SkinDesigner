
# By Santiago Garay
# LBHB_PanelGeometry

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

ghenv.Component.Name = "SkinDesigner_LBHB_PanelBrepViewer"
ghenv.Component.NickName = 'LBHB_PanelBrepViewer'
ghenv.Component.Message = 'VER 0.0.13\nMay_23_2016'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "04 | Display"



import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
from types import *
SGLibPanel = sc.sticky["SGLib_Panel"]
import copy
import math

PANEL_TYPES_ID=str(ghenv.Component.InstanceGuid)

        
 
    

#initialize
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

if  LocCircle: 
    Loc = LocCircle.Center
    offsetX = Loc.X ; offsetY = Loc.Y ; offsetZ = Loc.Z
else: print "I need a circle for location"
if _panelIndex <> None : pIndex = _panelIndex
else : pIndex = 1 

Mockup_Bay = [] ; textTypes = [] 


WallGeo =  []
WindowGeo = []
ShadingGeo = []
ShadingGeo = []
PanelGeo = []

for PPData in PostProcData:

    if isinstance(PPData, list) and len(PostProcData) and "LBHB_PanelsOutput" in PPData[0]:
    
        SkinPanel_List = PPData[1]
        panel = None ; pCounter = 0
        for panelData in SkinPanel_List :
            for i in range(len(panelData)):
                    
                    
                panelName = panelData[i][0].GetName()
                if (panelName.find("-Width")>0 or panelName.find("-Height")>0): 
                    if ShowCustom :fontHeight = 0.5 ; fontStyle=0 ; pCounter +=1
                    else: continue #skip custom panel if ShowCustom off 
                else: fontHeight= .6 ; fontStyle = 1; pCounter +=1
                
                if pCounter == _panelIndex :
                    panel = panelData[i][0]; break
                    
        if panel:
            for ang in angle:
                widthOffset = panel.PanelProperty("PanelWidth")/2
                if ang == None : ang = 0
                arrBoxPoints = [[offsetX-widthOffset, offsetY, offsetZ],[offsetX + widthOffset, offsetY, offsetZ],\
                    [offsetX-widthOffset, offsetY, offsetZ+panel.PanelProperty("PanelHeight")],\
                    [offsetX + widthOffset, offsetY, offsetZ+panel.PanelProperty("PanelHeight")]]
                    
                xform = rs.XformTranslation((0,-LocCircle.Radius, 0))
                arrBoxPoints = rs.PointArrayTransform(arrBoxPoints, xform)
                xform = Rhino.Geometry.Transform.Rotation(math.radians(ang), Rhino.Geometry.Vector3d.ZAxis, Loc)
                for point in arrBoxPoints:
                    point.Transform(xform)
                
                #create text info
                #rs.CurrentLayer("_P_0")
                #panelName = panel.GetName()
                #textTypes.append(rs.AddText(panelName, rs.PointSubtract(arrBoxPoints[0], [0,1,0]), fontHeight, font_style=fontStyle))
                #rs.RotateObject(textTypes[len(textTypes)-1], rs.TextObjectPoint(textTypes[len(textTypes)-1]), 270)
                
                #create and draw panel selected
                newPanel = SGLibPanel()
                newPanel.Copy(panel)
                newPanel.MorphPanel(arrBoxPoints)
                newPanel.Draw()

                #collect relevant objects 
                WallGeo.extend(newPanel.GetBreps("Wall"))
                WindowGeo.extend(newPanel.GetBreps("Window"))
                ShadingGeo.extend(newPanel.GetBreps("Shading"))
                ShadingGeo.extend(newPanel.GetBreps("Mullions"))
                rg = Rhino.Geometry
                pt1, pt2, pt3, pt4= arrBoxPoints  
                PanelGeo.append(rg.Brep.CreateFromCornerPoints(rg.Point3d(pt1[0],pt1[1],pt1[2]), rg.Point3d(pt2[0],pt2[1],pt2[2]),\
                    rg.Point3d(pt4[0],pt4[1],pt4[2]), rg.Point3d(pt3[0],pt3[1],pt3[2]), sc.doc.ModelAbsoluteTolerance))



#Wrapup
rs.EnableRedraw(True)
sc.doc = ghdoc


print "Done"