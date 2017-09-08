
# By Santiago Garay
# Skin_PanelAreaBreps
"""
Description

-

    Args:
        Param: param

    Returns:
        Nothing
"""

ghenv.Component.Name = "SkinDesigner_PanelAreaBreps"
ghenv.Component.NickName = 'PanelAreaBreps'
ghenv.Component.Message = 'VER 0.0.14\nOct_07_2016'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "04 | Display"



import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
#from types import *
#import random
import copy
#import math

SGLibPanel = sc.sticky["SGLib_Panel"]

#initialize
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

panelGeo = []; wallGeo= []; windowGeo=[]

if _bayData and _skinPanelList:
    #Flatten skin panels list (comes as grouped by each base panel and cutom created)
    skinPanelList = []
    for panelGroup in _skinPanelList:
        for panel in panelGroup: skinPanelList += [panel]
    
    nameList = []
    for panel in skinPanelList :
        panelName = panel[0].GetName()
        #check if is a custom panel and exclude if filter on
        if filterCustomPanel:
            if "-Width" in panelName or "-Height" in panelName:
                nameList.append(0); continue #add placeholder if filtered
        #check if panel name list inlcudes the panel
        filter = False
        if panelNameFilterList :
            filter = True
            for nameFilter in panelNameFilterList :
                if nameFilter in panelName: filter = False
        #add panel name to list or add a placelder if filtered        
        if not filter: nameList.append(panelName)
        else: nameList.append(0) 
        
    #Draw brep of panels 
    #bayData[0] holds each panel block corner point and panel name
    # in the order panel blocks were created as placed through skin
    bayData_Copy = copy.deepcopy(_bayData[0])
    skin_Indices = []    
    for panel in bayData_Copy:
        panelName = panel[1]
        #check if the panel name has not been filtered
        if nameList.count(panelName):
            index = nameList.index(panelName) #get index based on name loc. in list
            p1, p2, p3, p4 = panel[0] #get corner points
            #create panel surface
            brep = Rhino.Geometry.Brep.CreateFromCornerPoints(p1,p2,p4,p3, sc.doc.ModelAbsoluteTolerance)
            panelGeo.append(brep)
            #store index of panels throughout skin
            skin_Indices.append(index)
            
            #tag panel id text at panel location
            #text = rs.AddText(str(index) , p1, fontHeight, font_style=fontStyle)
            
            #Draw Panels in scene
            if drawPanelElements == True:
                tmpPanel = skinPanelList[index][0]
                panelDef = SGLibPanel()
                panelDef.Copy(tmpPanel)
                panelDef.MorphPanel([p1,p2,p3,p4])
                panelDef.Draw()
                geoList =  panelDef.GetBreps("Wall")
                if geoList <> []:
                    for geo in geoList: wallGeo.append(geo.Duplicate())
                else: wallGeo.append(None)
                
                geoList =  panelDef.GetBreps("Window")
                if geoList <> []:
                    for geo in geoList: windowGeo.append(geo.Duplicate())
                else: windowGeo.append(None)
            else:
                wallGeo.append(None)
                windowGeo.append(None)
        else:
            skin_Indices.append(None)
            panelGeo.append(None)
            wallGeo.append(None)
            windowGeo.append(None)
            
       
#Wrapup
rs.EnableRedraw(True)
sc.doc = ghdoc

print "Done"