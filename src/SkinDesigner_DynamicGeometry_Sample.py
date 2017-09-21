# By Santiago Garay

"""
Use this component's python structure to generate dynamic geoemtry objects. 
This is a sample file that generates a fin of specified shape and that can be scaled its thickness at top and bottom.
The scale paramters can be controlled while its mapped in a skin surface with a Panel function and a PanelData DynamicGeometry Controller(sample provided)
For more infomation refer to the Dynamic geometry grasshoper example file.
    Args:
        
    Returns:
        dynamicGeometry: dynamicGeometry object(class instance)to be connected to the geometry input of the CustomGeometry component 

"""
import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc
import copy


ghenv.Component.Name = "SkinDesigner_DynamicGeometry_Sample"
ghenv.Component.NickName = 'DynamicGeometrySample'
ghenv.Component.Message = 'VER 0.0.01\nSep_21_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"
try: ghenv.Component.AdditionalHelpFromDocStrings = "4"
except: pass


class DynamicGeometry:
    
    __m_baseParameters = []
    __m_dynamicParameters = []

    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self, baseParameters, dynamicParameters):
        
        self.__m_baseParameters = baseParameters
        self.__m_dynamicParameters = dynamicParameters
        

        
    def SetParameter(self, value, numParam=None):
        
        if numParam >= len(self.__m_dynamicParameters) : return False
        
        if numParam == None: self.__m_dynamicParameters =list((value for n in self.__m_dynamicParameters))
        else: self.__m_dynamicParameters[numParam] = value
        
        return True
        
        
    def Run(self):
        
        curveSections, curvePath = copy.deepcopy(self.__m_baseParameters)
        
        scaleList = copy.deepcopy(self.__m_dynamicParameters)
        o = curvePath.PointAt(0); stepZ = curvePath.Domain[1]
        x= rc.Geometry.Point3d(o.X+1,o.Y,o.Z); y = rc.Geometry.Point3d(o.X, o.Y-1,o.Z)
        Xplane = rc.Geometry.Plane(o,x,y)
        
        for crvIndex, curve in enumerate(curveSections):
            if scaleList[crvIndex]<> None:
                Xscale = rc.Geometry.Transform.Scale(Xplane, 1, scaleList[crvIndex] , 1)
                Xplane.OriginZ = Xplane.OriginZ + stepZ
                curve.Transform(Xscale)
        sweep = rc.Geometry.SweepOneRail()
        sweep.MiterType = 0
        sweepBrep = sweep.PerformSweep(curvePath, curveSections)
        sweepFinal = sweepBrep[0].CapPlanarHoles(.1)
        return [sweepFinal]
        
    




dynamicGeometry = DynamicGeometry([curveSections, curvePath], [scale1, scale2])
brep = dynamicGeometry.Run()
print "Done"