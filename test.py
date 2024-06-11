
import json

with open("/home/amari/Desktop/CaesarAIFencing/karate_frames.json","r") as f:
    frames = json.load(f)["frames"]
    
with open("/home/amari/Desktop/CaesarAIFencing/karate_frames.json","r") as f:
    connections = json.load(f)["frames"][0]["frame_0"]["connections"]



for ind in range(len(frames)):
    print(frames[ind][f"frame_{ind}"]["landmarks"])