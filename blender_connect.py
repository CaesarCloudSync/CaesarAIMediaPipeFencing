import bpy
import blender_plots as bplt

import json
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='CURVE')
bpy.ops.object.delete()

with open("/home/amari/Desktop/CaesarAIFencing/karate_frames.json","r") as f:
    frame = json.load(f)["frames"][0]["frame_0"]["landmarks"]
    
with open("/home/amari/Desktop/CaesarAIFencing/karate_frames.json","r") as f:
    connections = json.load(f)["frames"][0]["frame_0"]["connections"]

bplt.Scatter(frame, color=(1, 0, 0), name="red",marker_type="spheres")

def create_line(ind,coords):
    # create the Curve Datablock
    curveData = bpy.data.curves.new('myCurve'+str(ind), type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2

    # map coords to spline
    polyline = curveData.splines.new('NURBS')
    polyline.points.add(len(coords))
    for i, coord in enumerate(coords):
        x,y,z = coord
        polyline.points[i].co = (x, y, z, 1)

    # create Object
    curveOB = bpy.data.objects.new('myCurve'+str(ind), curveData)

    # attach to scene and validate context
    scn = bpy.context.scene
    scn.collection.objects.link(curveOB)

# sample data

coords = [(1,1,2),(2,2,3)]
for ind,conn in enumerate(connections):
    x = conn[0]
    y = conn[1]
    z = conn[2]
    create_line(ind,[(x[0],y[0],z[0]),(x[1],y[1],z[1])])