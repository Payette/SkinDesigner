# By Santiago Garay
# Panel Bay

"""
Use this component to create a panel bay (group of panels)
_
_
To add more panels in the construction, simply zoom into the component and hit the lowest "+" sign that shows up on the input side.  
To remove panels from the construction, zoom into the component and hit the lowest "-" sign that shows up on the input side.
-
    Args:
        Pattern: Text with panel names separated with spaces to arrange them accordingly
        Panel_A (B,C, etc): A Panel Object. Add as many inputs as neccesary.

    Returns:
        Panel_Bay: A list containing all the Panel objects used to generate the skin

"""

ghenv.Component.Name = "SkinShop_PanelBay"
ghenv.Component.NickName = 'PanelBay'
ghenv.Component.Message = 'VER 0.0.44\nApr_07_2016'
ghenv.Component.Category = "SkinShop"
ghenv.Component.SubCategory = "01 | Construction"

# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
access = ghenv.Component.Params.Input[0].Access.item
 
for input in range(numInputs):
    
    if input == 0: inputName = 'Pattern'
    else: inputName = 'Panel_' + str(input)
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    
ghenv.Component.Attributes.Owner.OnPingDocument()



import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
SGLibPanel = sc.sticky["SGLib_Panel"]

Panel_Bay = []
Panel_List ={}

numInputs = ghenv.Component.Params.Input.Count
for input in range(numInputs):
    item = ghenv.Component.Params.Input[input]
    if "Panel" in item.Name and item.VolatileDataCount > 0:
        pList = []
        if item.VolatileData.get_DataItem(0):
            panel = item.VolatileData.get_DataItem(0).Value
            Panel_List[panel.GetName()] = panel

if Panel_List:

    if Pattern:
        Letters_List = Pattern.split(" ")
        for i in range(len(Letters_List)):
            if Letters_List[i] in Panel_List :
                Panel_Bay.append(Panel_List[Letters_List[i]])
    else:
        Panel_Bay = Panel_List.values()

print "r"
print Panel_List