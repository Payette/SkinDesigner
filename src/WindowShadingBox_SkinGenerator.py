# By Santiago Garay
# Skin Generator

"""
Use this component to generate a panel window
-
Refer to PanelLib API for Definition input functions
    Args:
        Height: Panel height in meters
        Width: Panel width in meters
        Definition: Text panel that define panel properties (refer to PanelLib API)
        Activate: Turns panel on/off

    Returns:
        Panel: A PanelLib object to use as input on Panel_Bay, Skin_Generator or Mock_up components

"""

ghenv.Component.Name = "WindowShadingBox_SkinGenerator"
ghenv.Component.NickName = 'ShadingBox'
ghenv.Component.Message = 'VER 0.0.41\nMar_02_2016'
ghenv.Component.Category = "Skin_Generator"
ghenv.Component.SubCategory = "02 | Panel Parameters"


import scriptcontext as sc
import Rhino


#init set up global variables
_UNIT_COEF = 1
sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
sc.doc = ghdoc



if not shadingThickness : shadingThickness = .015*_UNIT_COEF
if not shadingWidth : shadingWidth = .2*_UNIT_COEF


#WindowData = 0=width,1=height,2=fromLeft,3=fromBottom,4=recess 

offset = -shadingThickness/2

if offsetFromPanel <> None: 
    if offsetFromPanel < 0: offsetFromPanel = 0
    offset = offsetFromPanel + shadingThickness/2
    ShadingData = "AddShadingType('HorizontalShade', fromLeftBottom = ["+str(offset)+", "+str(offset)+"], fromEdge="+str(offset)+",width="+str(shadingThickness)+", thickness="+str(shadingWidth)+", offset=0)\r\n"
    ShadingData +=  "AddShadingType('HorizontalShade', fromLeftBottom = ["+str(offset)+", PanelHeight-"+str(offset)+"], fromEdge="+str(offset)+",width="+str(shadingThickness)+", thickness="+str(shadingWidth)+", offset=0)\r\n"
    ShadingData +=  "AddShadingType('VerticalShade', fromLeftBottom = ["+str(offset)+", "+str(offset)+"], fromEdge="+str(offset)+",width="+str(shadingThickness)+", thickness="+str(shadingWidth)+", offset=0)\r\n"
    ShadingData +=  "AddShadingType('VerticalShade', fromLeftBottom = [PanelWidth-"+str(offset)+", "+str(offset)+"], fromEdge="+str(offset)+",width="+str(shadingThickness)+", thickness="+str(shadingWidth)+", offset=0)"
else:
    if offsetFromWindow <> None: offset = offsetFromWindow - shadingThickness/2
    ShadingData = "AddShadingType('HorizontalShade', fromLeftBottom = [Window['fromLeft']+"+str(offset)+", Window['fromBottom']+"+str(offset)+"], fromEdge=PanelWidth-(Window['fromLeft']+Window['width'])+"+str(offset)+",width="+str(shadingThickness)+", thickness="+str(shadingWidth)+", offset=0)\r\n"
    ShadingData +=  "AddShadingType('HorizontalShade', fromLeftBottom = [Window['fromLeft']+"+str(offset)+", Window['fromBottom']+Window['height']-"+str(offset)+"], fromEdge=PanelWidth-(Window['fromLeft']+Window['width'])+"+str(offset)+",width="+str(shadingThickness)+", thickness="+str(shadingWidth)+", offset=0)\r\n"
    ShadingData +=  "AddShadingType('VerticalShade', fromLeftBottom = [Window['fromLeft']+"+str(offset)+", Window['fromBottom']+"+str(offset)+"], fromEdge=PanelHeight-(Window['fromBottom']+Window['height'])+"+str(offset)+",width="+str(shadingThickness)+", thickness="+str(shadingWidth)+", offset=0)\r\n"
    ShadingData +=  "AddShadingType('VerticalShade', fromLeftBottom = [Window['fromLeft']+Window['width']-"+str(offset)+", Window['fromBottom']+"+str(offset)+"], fromEdge=PanelHeight-(Window['fromBottom']+Window['height'])+"+str(offset)+",width="+str(shadingThickness)+", thickness="+str(shadingWidth)+", offset=0)"

    



print ShadingData
