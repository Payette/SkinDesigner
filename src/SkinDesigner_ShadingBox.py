# By Santiago Garay
# Skin Generator

"""
Use this component to generate four shade objects placed around the window to be added to a panel component.

    Args:
        layerName: A string indicating the layer the louver shade geometry will use when drawn in the scene. Default is _P_Shading
        width: A floating point value that represents the louvers' horizontal dimension in scene units. Default is 0.25m (10 inches aprox.)
        thickness: A floating point value that represents the louvers'  vertical dimension in scene units. Default value is 0.025m (1 inch)
        offsetFromWall: A floating point value that represenets a separation distance from panel wall's exterior surface  (not including panel systems applied).Default value is 0.025 m (1 inch)
        offsetFromWindow: A floating point value that represents the distance from the window edges where the sunshades will be located. Positive values offset the sunshades towards inside the window. Default value is 0.0.
        offsetFromPanel: A floating point value that represents the distance from the panel edges where the sunshades will be located. Positive values offset the sunshades towards inside the panel. Default value is 0.0.
        shiftCorners: A list of one to four vectors that is used to shift in scene units on x,y,z the outside end point of the shading box corners. It is provided to be able to create custom-shaped shading elements. Default value is 0,0,0 on all corners.
    Returns:
        shadingSystem: A list with shading data packed to be connected to a Panel component shadingSystem input



"""


ghenv.Component.Name = "SkinDesigner_ShadingBox"
ghenv.Component.NickName = 'ShadingBox'
ghenv.Component.Message = 'VER 0.0.46\nApr_28_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"
try: ghenv.Component.AdditionalHelpFromDocStrings = "3"
except: pass


import scriptcontext as sc
import Rhino


#init set up global variables
_UNIT_COEF = 1
sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == Rhino.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
sc.doc = ghdoc


if layerName == None : layerName = "'_P_Shading'"
if not thickness : thickness = .015*_UNIT_COEF
if not width : width = .2*_UNIT_COEF
if not offsetFromWall : offsetFromWall = 0
offset = -thickness/2

# shift data 
shiftEndVectors = []
for v in range(4) : 
    shiftVector = None
    if v < len(shiftCorners): 
        corner = eval(str(shiftCorners[v]))
        shiftVector = [corner[0], corner[1], corner[2]]
    shiftEndVectors.append(shiftVector)



#WindowData = 0=width,1=height,2=fromLeft,3=fromBottom,4=recess 
if offsetFromPanel <> None: 
    offsetFromPanel = eval(str(offsetFromPanel))
    if offsetFromPanel < 0: offsetFromPanel = 0
    offset = offsetFromPanel + thickness/2
    shadingSystem = "AddShadingType('HorizontalShade'"+", layerName="+ layerName +", fromLeftBottom = ["+str(offset)+", "+str(offset)+"], fromEdge="+str(offset)+\
        ",width="+str(thickness)+", thickness="+str(width)+", offset="+str(offsetFromWall)+", shiftEnds="+str([shiftEndVectors[3],shiftEndVectors[2]])+")\r\n"
    shadingSystem +=  "AddShadingType('HorizontalShade'"+", layerName="+ layerName +", fromLeftBottom = ["+str(offset)+", PanelHeight-"+str(offset)+"], fromEdge="+str(offset)+\
        ",width="+str(thickness)+", thickness="+str(width)+", offset="+str(offsetFromWall)+", shiftEnds="+str([shiftEndVectors[0],shiftEndVectors[1]])+")\r\n"
    shadingSystem +=  "AddShadingType('VerticalShade'"+", layerName="+ layerName +", fromLeftBottom = ["+str(offset)+", "+str(offset)+"], fromEdge="+str(offset)+\
        ",width="+str(thickness)+", thickness="+str(width)+", offset="+str(offsetFromWall)+", shiftEnds="+str([shiftEndVectors[3],shiftEndVectors[0]])+")\r\n"
    shadingSystem +=  "AddShadingType('VerticalShade'"+", layerName="+ layerName +", fromLeftBottom = [PanelWidth-"+str(offset)+", "+str(offset)+"], fromEdge="+str(offset)+\
        ",width="+str(thickness)+", thickness="+str(width)+", offset="+str(offsetFromWall)+", shiftEnds="+str([shiftEndVectors[2],shiftEndVectors[1]])+")\r\n"
else:
    if offsetFromWindow <> None: offset = - eval(str(offsetFromWindow)) - thickness/2
    shadingSystem = "AddShadingType('HorizontalWindowShade'"+", layerName="+ layerName +", fromLeftBottom = [-Window['width']+"+str(offset)+", Window['height']+"+str(-offset)+\
        "], fromEdge="+str(offset)+",width="+str(thickness)+", thickness="+str(width)+", offset="+str(offsetFromWall)+", shiftEnds="+str([shiftEndVectors[3],shiftEndVectors[2]])+")\r\n"
    shadingSystem +=  "AddShadingType('HorizontalWindowShade'"+", layerName="+ layerName +", fromLeftBottom = [-Window['width']+"+str(offset)+", -Window['height']+"+str(offset)+\
        "], fromEdge="+str(offset)+",width="+str(thickness)+", thickness="+str(width)+", offset="+str(offsetFromWall)+", shiftEnds="+str([shiftEndVectors[0],shiftEndVectors[1]])+")\r\n"
    shadingSystem += "AddShadingType('VerticalWindowShade'"+", layerName="+ layerName +", fromLeftBottom = [-Window['width']+"+str(offset)+", -Window['height']+"+str(offset)+\
        "], fromEdge="+str(offset)+",width="+str(thickness)+", thickness="+str(width)+", offset="+str(offsetFromWall)+", shiftEnds="+str([shiftEndVectors[3],shiftEndVectors[2]])+")\r\n"
    shadingSystem +=  "AddShadingType('VerticalWindowShade'"+", layerName="+ layerName +", fromLeftBottom = [Window['width']+"+str(-offset)+", -Window['height']+"+str(offset)+\
        "], fromEdge="+str(offset)+",width="+str(thickness)+", thickness="+str(width)+", offset="+str(offsetFromWall)+", shiftEnds="+str([shiftEndVectors[0],shiftEndVectors[1]])+")\r\n"

    



print shadingSystem
