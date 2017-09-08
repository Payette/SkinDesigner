# By Santiago Garay
# Skin Generator

"""
Use this component to generate a window to be added to a Panel component.
-
Refer to PanelLib API for Definition input functions
    Args:
        width: A floating point number representing the window opening width in scene units. Panel properties 'PanelWidth' and 'PanelHeights' are valid. Default value is 'PanelWidth/2'.
        height: A floating point number representing the window opening height in scene units. Panel properties 'PanelWidth' and 'PanelThickness' are valid. Default value is 'PanelHeight/2'.
        fromLeft: A floating point value indicating in scene units the horizontal placement of the window from the left edge of the panel. Panel properties 'PanelWidth',  'PanelHeight' and 'C'(centered on panel) are valid. Default value is 'C'.
        fromBottom: A floating point value indicating in scene units the vertical placement of the window from the bottom edge of the panel. Panel properties 'PanelWidth', 'PanelHeight' and 'C'(centered on panel) are valid. Default value is 'C'.
        recess : A floating point value indicating in scene units the location of the glass pane relative to the front face of the wall element. Positive values place the glass pane inbound from the wall surface, negative values project the glass pane outbound. Default value is 0.0.

    Returns:
        windowSystem: A list with window data packed to be connected to a Panel component windowSystem input

"""


ghenv.Component.Name = "SkinDesigner_Window"
ghenv.Component.NickName = 'Window'
ghenv.Component.Message = 'VER 0.0.49\nJul_13_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass



#import rhinoscriptsyntax as rs
#import Rhino
#import Panel14 as PanelLib
#import scriptcontext as sc

wWidth = "PanelWidth/2"
wHeight = "PanelHeight/2"
wFromLeft = "C"
wFromBottom = "C"
wRecess = 0.0

if width<>None : wWidth = width
if height <> None : wHeight = height
if fromLeft <> None : wFromLeft = fromLeft
if fromBottom <> None : wFromBottom = fromBottom
if recess <> None : wRecess = -recess

windowSystem = [wWidth,wHeight, wFromLeft, wFromBottom, wRecess]
print windowSystem