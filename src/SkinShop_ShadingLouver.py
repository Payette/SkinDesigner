# By Santiago Garay
# Skin Generator

"""
Use this component to generate a panel window
-
Refer to PanelLib API for Definition input functions
    Args:


    Returns:


"""
# WindowData(wd) = 0=width,1=height,2=fromLeft,3=fromBottom,4=recess 

ghenv.Component.Name = "SkinShop_ShadingLouver"
ghenv.Component.NickName = 'ShadingLouver'
ghenv.Component.Message = 'VER 0.0.41\nApr_07_2016'
ghenv.Component.Category = "SkinShop"
ghenv.Component.SubCategory = "02 | Parameters"


# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item


for input in range(numInputs):
    access = accessList
    if input == 0: inputName = 'layerName'; access = accessItem
    elif input == 1: inputName = 'louverWidth'; access = accessItem
    elif input == 2: inputName = 'louverThickness'; access = accessItem
    elif input == 3: inputName = 'spacing'; access = accessItem
    elif input == 4: inputName = 'rotation'; access = accessItem
    elif input == 5: inputName = 'offset'; access = accessItem
    elif input == 6: inputName = 'vertical' ; access = accessItem
    elif input == 7: inputName = 'windowLouver'; access = accessItem
    elif input == 8: inputName = 'fromLeftEdge' ; access = accessItem
    elif input == 9: inputName = 'fromRightEdge'; access = accessItem
    elif input == 10: inputName = 'fromBottomEdge' ; access = accessItem
    elif input == 11: inputName = 'fromTopEdge'; access = accessItem
    else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    
ghenv.Component.Attributes.Owner.OnPingDocument()



import scriptcontext as sc
import Rhino


#init set up global variables
_UNIT_COEF = 1
sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
sc.doc = ghdoc


#if  isinstance(fromBottomEdge, str) : print "String"
if louverWidth == None : louverWidth = .1*_UNIT_COEF
if louverThickness== None : louverThickness = .02*_UNIT_COEF
if spacing == None : spacing = .15*_UNIT_COEF
if fromLeftEdge == None : fromLeftEdge = 0
if fromBottomEdge == None : fromBottomEdge = 0
if fromRightEdge == None : fromRightEdge = 0
if fromTopEdge == None : fromTopEdge = 0
if rotation == None : rotation = 0
if offset == None : offset = .02*_UNIT_COEF
if layerName == None : layerName = "_P_Shading"

if vertical == True : shadingType = 'VerticalLouver'; hOffset = spacing/2; vOffset=0
else: shadingType = 'HorizontalLouver'; hOffset = 0; vOffset=spacing/2

if windowLouver == True:
    fromLeftEdge = "Window['fromLeft']+"+str(fromLeftEdge+hOffset) ; fromBottomEdge = "Window['fromBottom']+"+str(fromBottomEdge+vOffset)
    fromRightEdge = "PanelWidth-Window['width']-Window['fromLeft']+"+str(fromRightEdge+hOffset) ; fromTopEdge = "PanelHeight-Window['height']-Window['fromBottom']+"+str(fromTopEdge+vOffset)
    offset = str(offset)+"+Window['recess']"


ShadingData = "AddShadingType('" + shadingType +"', layerName='"+ layerName +"', fromLeftBottom = ["+str(fromLeftEdge)+", "+str(fromBottomEdge)+\
    "], fromRightTop=["+str(fromRightEdge)+", "+str(fromTopEdge)+"],width="+str(louverThickness)+", thickness="+str(louverWidth)+\
    ", spacing="+str(spacing)+", offset="+str(offset)+", rotation="+str(rotation)+")\r\n"

print ShadingData
print "Done"