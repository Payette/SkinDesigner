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

ghenv.Component.Name = "SkinShop_SkinParameters"
ghenv.Component.NickName = 'SkinParameters'
ghenv.Component.Message = 'VER 0.0.42\nApr_07_2016'
ghenv.Component.Category = "SkinShop"
ghenv.Component.SubCategory = "02 | Parameters"


# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item


import math

for input in range(numInputs):
    access = accessItem
    if input == 0: inputName = 'SkinName'; access = accessItem
    elif input == 1: inputName = 'DefaultBayList'; access= accessList
    else : 
        ParamNum = math.floor(input/2)
        val = 0 if input/2 == math.floor(input/2) else 1 
        if val == 0: inputName = 'Parameter_'+str(int(ParamNum))
        elif val == 1: inputName = 'Value_'+str(int(ParamNum))
        else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    
ghenv.Component.Attributes.Owner.OnPingDocument()

if numInputs > 0 and SkinName : SkinParameters =["SKIN_NAME="+SkinName]
if numInputs > 1 and DefaultBayList : SkinParameters += ["DEFAULT_BAY_LIST="+str(DefaultBayList)]

paramCounter = 1

for input in range(numInputs-2):
    
    paramType = 0 if input/2 == math.floor(input/2) else 1

    if paramType == 0 : 
        paramInput = eval("Parameter_"+str(int(paramCounter)))
        if paramInput <> None : 
            SkinParameters.append(paramInput)
    elif paramInput <> None:
        
        valueInput = eval("Value_"+str(int(paramCounter)))
        if valueInput <> None : SkinParameters[len(SkinParameters)-1] += "=" + str(valueInput)

    paramCounter += 0 if input/2 == math.floor(input/2) else 1 

print SkinParameters