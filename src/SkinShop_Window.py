# By Santiago Garay
# Skin Generator

"""
Use this component to generate a panel window
-
Refer to PanelLib API for Definition input functions
    Args:
        width: Window width
        height: Window height
        fromLeft: Distance from left - "C" for center
        fromBottom: Distance from bottom - "C" for center
        recess = Window recess
        
        Variables supported:
            PanelWidth
            PanleHeight
    Returns:
        WindowData: A list with window paramters 

"""


ghenv.Component.Name = "SkinShop_Window"
ghenv.Component.NickName = 'Window'
ghenv.Component.Message = 'VER 0.0.45\nApr_07_2016'
ghenv.Component.Category = "SkinShop"
ghenv.Component.SubCategory = "02 | Parameters"




#import rhinoscriptsyntax as rs
#import Rhino
#import Panel14 as PanelLib
#import scriptcontext as sc

wWidth = "PanelWidth/2"
wHeight = "PanelHeight/2"
wFromLeft = "C"
wFromBottom = "C"
wRecess = 0

if width : wWidth = width
if height : wHeight = height
if fromLeft : wFromLeft = fromLeft
if fromBottom : wFromBottom = fromBottom
if recess : wRecess = recess

WindowData = [wWidth,wHeight, wFromLeft, wFromBottom, wRecess]
print WindowData