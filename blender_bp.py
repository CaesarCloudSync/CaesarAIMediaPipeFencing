import numpy as np
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
n, l = 150, 100
x, y = 1,1
#x, y = x.ravel(), y.ravel()
print(x)
z = 1 #np.sin(2*np.pi * x / l)*np.sin(2*np.pi * y / l) * 20
bplt.Scatter(frame, color=(1, 0, 0), name="red",marker_type="spheres")



# Create a new Bezier curve
bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
#note: [255,40,0] is red in RGB


#z = np.sin(4*np.pi * x / l)*np.sin(4*np.pi * y / l) * 20 + 40
#bplt.Scatter(x, y, z, color=(0, 0, 1), name="blue")