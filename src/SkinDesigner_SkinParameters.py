# By Santiago Garay
# Skin Generator

"""
Use this component to load skin-specific paramters to skinGenerator

    Args:
        skinName:  String containing the name of the skin generator solution. The name is used to create a root folder that will contain the panels. Also the panel blocks created will include the skin name. By defaule will use the SkinGenerator component instant ID (not recommended).
        defaultBayList: List of panel IDs connected to SkinGenerator to use in the facade solution. If not provided, the default list of panels will include all the panels connected to SkinGenerator.
        parameter_1: (paramter_2, ...)A string with the name of the parameter to use. The parameter types available are provided as a drop down list (SKIN GENERATOR PARAMETERS).
        value_1: (value_2, ...)A value to assign to the specified parameter. 

    Returns:
        skinParameters: The list of parameter/value pairs to be input to the SkinGenerator component _skinParameters input.

"""


ghenv.Component.Name = "SkinDesigner_skinParameters"
ghenv.Component.NickName = 'skinParameters'
ghenv.Component.Message = 'VER 0.0.46\nSep_22_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "01 | Construction"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass

# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item


import math

for input in range(numInputs):
    access = accessItem
    if input == 0: inputName = 'skinName'; access = accessItem
    elif input == 1: inputName = 'defaultBayList'; access= accessList
    else : 
        ParamNum = math.floor(input/2)
        val = 0 if input/2 == math.floor(input/2) else 1 
        if val == 0: inputName = 'parameter_'+str(int(ParamNum))
        elif val == 1: inputName = 'value_'+str(int(ParamNum))
        else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    
ghenv.Component.Attributes.Owner.OnPingDocument()

skinParameters = []
if numInputs > 0 and skinName : 
    if "'" not in skinName : skinName = "'" + skinName + "'"  
    skinParameters =["SKIN_NAME="+skinName]
if numInputs > 1 and defaultBayList : skinParameters += ["DEFAULT_BAY_LIST="+str(defaultBayList)]

paramCounter = 1

for input in range(numInputs-2):
    
    paramType = 0 if input/2 == math.floor(input/2) else 1

    if paramType == 0 : 
        paramInput = eval("parameter_"+str(int(paramCounter)))
        if paramInput <> None : 
            skinParameters.append(paramInput)
    elif paramInput <> None:
        
        valueInput = eval("value_"+str(int(paramCounter)))
        if valueInput <> None : skinParameters[len(skinParameters)-1] += "=" + str(valueInput)

    paramCounter += 0 if input/2 == math.floor(input/2) else 1 

print skinParameters