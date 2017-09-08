
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

ghenv.Component.Name = "SkinDesigner_LBHB_PanelGeometry"
ghenv.Component.NickName = 'LBHB_PanelGeoemtry'
ghenv.Component.Message = 'VER 0.0.10\nMay_10_2016'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "04 | Display"




import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
from types import *
SGLibPanel = sc.sticky["SGLib_Panel"]
import copy

PANEL_TYPES_ID=str(ghenv.Component.InstanceGuid)

def DeleteMockup():
    
    if not sc.sticky["PanelTypes_Data"+ PANEL_TYPES_ID] : return
    
    for data in sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] :
        if isinstance(data, SGLibPanel): data.HideAll() #same as deleting all panel objects
        elif rs.IsObject(data) : rs.DeleteObject(data)
 
    

#initialize
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

if  LocCircle and rs.IsObject(LocCircle) and rs.IsCircle(LocCircle): 
    Loc = rs.CircleCenterPoint(LocCircle)
    offsetX = Loc[0] ; offsetY = Loc[1] ; offsetZ = Loc[2]
else: print "I need a circle for location"
if _panelIndex <> None : pIndex = _panelIndex
else : pIndex = 1 

Mockup_Bay = [] ; textTypes = [] 


if "PanelTypes_Data"+PANEL_TYPES_ID not in sc.sticky : sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] = []

DeleteMockup()

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
                    
        #for rotation in range(0,360, 360/_orientationSamples): 
        if panel:
            widthOffset = panel.PanelProperty("PanelWidth")/2
            if angle == None : angle = 0
            arrBoxPoints = [[offsetX-widthOffset, offsetY, offsetZ],[offsetX + widthOffset, offsetY, offsetZ],\
                [offsetX-widthOffset, offsetY, offsetZ+panel.PanelProperty("PanelHeight")],\
                [offsetX + widthOffset, offsetY, offsetZ+panel.PanelProperty("PanelHeight")]]
                
            xform = rs.XformTranslation((0,-rs.CircleRadius(LocCircle), 0))
            arrBoxPoints = rs.PointArrayTransform(arrBoxPoints, xform)
            xform = rs.XformRotation2(angle,(0,0,1), Loc)
            arrBoxPoints = rs.PointArrayTransform(arrBoxPoints, xform)
            
            #create text info
            rs.CurrentLayer("_P_0")
            panelName = panel.GetName()
            textTypes.append(rs.AddText(panelName, rs.PointSubtract(arrBoxPoints[0], [0,1,0]), fontHeight, font_style=fontStyle))
            rs.RotateObject(textTypes[len(textTypes)-1], rs.TextObjectPoint(textTypes[len(textTypes)-1]), 270)
            
            #create and draw panel selected
            newPanel = SGLibPanel()
            newPanel.Copy(panel)
            newPanel.MorphPanel(arrBoxPoints)
            newPanel.Draw()
            
            #collect relevant objects 
            wallObjects =  newPanel.PanelProperty("WallObjects")
            windowObjects = newPanel.PanelProperty("WindowObjects")
            shadingObjects = newPanel.PanelProperty("ShadingObjects")
            for i in range(newPanel.PanelProperty("MullionHorNum")):
                shadingObjects.extend(newPanel.PanelPropertyArray("MullionHorObjArray", i))
            for i in range(newPanel.PanelProperty("MullionVertNum")):
                shadingObjects.extend(newPanel.PanelPropertyArray("MullionVertObjArray", i))
            
            #create panel surface by adding wall and window
            if not windowObjects[0] : panelObjects = rs.CopyObjects(wallObjects)
            elif not wallObjects[0] : panelObjects = rs.CopyObjects(windowObjects)
            else: panelObjects = rs.BooleanUnion(windowObjects + wallObjects, False)
            
            #place geometry in LB layers and convert geometry into breps

            geoLists = [windowObjects, shadingObjects, wallObjects, panelObjects]            
            layerList = ["_P_LB_Window", "_P_LB_Context", "_P_LB_Wall", "_P_LB_Panel"]
            for i in range(len(geoLists)):
                tmpList = []
                for geo in geoLists[i]:
                    if geo : rs.ObjectLayer(geo, layerList[i])
                    tmpBrep = rs.coercebrep(geo)
                    if tmpBrep <> None : tmpList.append(tmpBrep)
                geoLists[i] = tmpList
                
            WindowGeo = geoLists[0]
            ShadingGeo = geoLists[1]
            WallGeo = geoLists[2]
            PanelGeo = geoLists[3]
            #if  Context : ShadingGeo.append(Context)
        
            #save panel and text on sticky for cleanup on next iteration
            sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] = [newPanel] + [textTypes] + panelObjects
    else:
        DeleteMockup()

#Wrapup
rs.EnableRedraw(True)
sc.doc = ghdoc


print "Done"