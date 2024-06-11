import bpy

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='CURVE')
bpy.ops.object.delete()

def create_line(i,coords):
    # create the Curve Datablock
    curveData = bpy.data.curves.new('myCurve'+str(i), type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2

    # map coords to spline
    polyline = curveData.splines.new('NURBS')
    polyline.points.add(len(coords))
    for i, coord in enumerate(coords):
        x,y,z = coord
        polyline.points[i].co = (x, y, z, 1)

    # create Object
    curveOB = bpy.data.objects.new('myCurve'+str(i), curveData)

    # attach to scene and validate context
    scn = bpy.context.scene
    scn.collection.objects.link(curveOB)

# sample data
coords = [(1,1,1), (2,2,2), (1,2,1)]

create_line(0,coords)
