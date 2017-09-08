
"""
Use this to update your version of Skin Generator.
-
Provided by Ladybug 0.0.61
    
    Args:
        _updateAllUObjects: Set to "True" to sync all the skinGenerator userObjects in your Grasshopper folder with the F drive.
    Returns:
        readMe!: ...
"""

ghenv.Component.Name = "SkinDesigner_UpdateSkinDesigner"
ghenv.Component.NickName = 'UpdateSkinDesigner'
ghenv.Component.Message = 'VER 0.0.50\nApr_07_2016'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "10 | Developers"


import scriptcontext as sc
import Grasshopper.Kernel as gh
import os
import shutil
import zipfile
import time
import urllib
import Grasshopper.Folders as folders
import System


def main(sourceDirectory, updateAllUObjects):
    lb_preparation = sc.sticky["ladybug_Preparation"]()
    
    userObjectsFolder = sourceDirectory
    
    destinationDirectory = folders.ClusterFolders[0]
    
    
    # copy files from source to destination
    if updateAllUObjects:
        if not userObjectsFolder  or not os.path.exists(userObjectsFolder):
            warning = 'source directory address is not a valid address!'
            print warning
            w = gh.GH_RuntimeMessageLevel.Warning
            ghenv.Component.AddRuntimeMessage(w, warning)
            return -1
        
        srcFiles = os.listdir(userObjectsFolder)
        print 'Removing Old Version...'
        # remove userobjects that are currently removed
        fileNames = os.listdir(destinationDirectory)
        for fileName in fileNames:
            # check for ladybug userObjects and delete the files if they are not
            # in source anymore
            if not fileName.StartsWith('Ladybug') and not fileName.StartsWith('Honeybee') and not fileName.StartsWith('Dragonfly')and fileName not in srcFiles:
                fullPath = os.path.join(destinationDirectory, fileName)
                os.remove(fullPath)                

        print 'Updating...'
        
        for srcFileName in srcFiles:
            srcFullPath = os.path.join(userObjectsFolder, srcFileName)
            dstFullPath = os.path.join(destinationDirectory, srcFileName) 
            
            # check if a newer version is not aleady exist
            if not os.path.isfile(dstFullPath): shutil.copy2(srcFullPath, dstFullPath)
            # or is older than the new file
            elif os.stat(srcFullPath).st_mtime - os.stat(dstFullPath).st_mtime > 1: shutil.copy2(srcFullPath, dstFullPath)
        
        return "Done!" , True

if _updateAllUObjects:
    msg, success = main('F:\\Research+Innovation\\1_Skin_Generator\\userObjects\\', _updateAllUObjects)
    if not success:
        ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, msg)
    else:
        print msg
else:
    print " "
